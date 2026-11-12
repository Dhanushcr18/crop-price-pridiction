"""Data pipeline module: builds cleaned, standardized daily panel with strict DATA_PROVENANCE tagging."""

import os
import sys
import glob
import yaml
import logging
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def load_config(config_path: str = "config.yaml") -> dict:
    """Load system configuration from YAML."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def map_mandi_name(raw_name: str, target_mandis: list) -> str:
    """Fuzzy maps raw Agmarknet mandi names to normalized target mandis."""
    raw_lower = str(raw_name).lower()
    if any(k in raw_lower for k in ["yeshwanthpur", "bengaluru", "bangalore", "binny"]):
        return "Bengaluru (Yeshwanthpur)"
    elif "chikkaballapur" in raw_lower or "chickballapur" in raw_lower:
        return "Chikkaballapur"
    elif "kolar" in raw_lower:
        return "Kolar"
    
    for tm in target_mandis:
        if tm.lower() in raw_lower or raw_lower in tm.lower():
            return tm
    return raw_name


def load_real_agmarknet_panel(real_dir: str, config: dict) -> pd.DataFrame:
    """
    Parses real Agmarknet CSV files from data/raw/real/.
    Standardizes schema, cleans duplicates, converts units, and tags data_provenance='real'.
    """
    csv_files = glob.glob(os.path.join(real_dir, "*.csv"))
    if not csv_files:
        return None

    logger.info(f"Found {len(csv_files)} real Agmarknet CSV file(s) in '{real_dir}'.")
    target_mandis = config["project"]["target_mandis"]

    all_dfs = []
    for f in csv_files:
        try:
            temp_df = pd.read_csv(f)
            # Normalize column names: lower case, strip whitespace, remove _x0020_
            col_map = {}
            for col in temp_df.columns:
                cleaned = col.lower().strip().replace("_x0020_", " ").replace("_", " ")
                col_map[col] = cleaned
            temp_df = temp_df.rename(columns=col_map)

            # Identify column mappings
            date_col = next((c for c in temp_df.columns if "date" in c), None)
            mandi_col = next((c for c in temp_df.columns if "market" in c or "mandi" in c), None)
            comm_col = next((c for c in temp_df.columns if "commodity" in c or "crop" in c), None)
            modal_col = next((c for c in temp_df.columns if "modal" in c or c == "price"), None)
            min_col = next((c for c in temp_df.columns if "min" in c), None)
            max_col = next((c for c in temp_df.columns if "max" in c), None)
            arrival_col = next((c for c in temp_df.columns if "arrival" in c), None)

            if not (date_col and mandi_col and modal_col):
                logger.warning(f"File {f} is missing essential columns (date, mandi, modal_price). Skipping.")
                continue

            # Filter for onion if commodity column exists
            if comm_col:
                temp_df = temp_df[temp_df[comm_col].astype(str).str.contains("onion", case=False, na=False)]

            temp_df["parsed_mandi"] = temp_df[mandi_col].apply(lambda m: map_mandi_name(m, target_mandis))
            # Filter strictly to target mandis
            temp_df = temp_df[temp_df["parsed_mandi"].isin(target_mandis)].copy()

            if temp_df.empty:
                logger.info(f"No onion records matching target mandis in {f}.")
                continue

            parsed_dates = pd.to_datetime(temp_df[date_col], dayfirst=True, errors="coerce")
            temp_df["parsed_date"] = parsed_dates
            temp_df = temp_df.dropna(subset=["parsed_date"])

            # Clean prices
            temp_df["modal_price"] = pd.to_numeric(temp_df[modal_col].astype(str).str.replace(",", ""), errors="coerce")
            temp_df["min_price"] = pd.to_numeric(temp_df[min_col].astype(str).str.replace(",", ""), errors="coerce") if min_col else temp_df["modal_price"]
            temp_df["max_price"] = pd.to_numeric(temp_df[max_col].astype(str).str.replace(",", ""), errors="coerce") if max_col else temp_df["modal_price"]
            temp_df["arrivals"] = pd.to_numeric(temp_df[arrival_col].astype(str).str.replace(",", ""), errors="coerce") if arrival_col else 100.0

            # Unit sanity check: if modal price is in Rs/kg (< 100), convert to quintal (* 100)
            kg_mask = temp_df["modal_price"] < 100.0
            if kg_mask.any():
                temp_df.loc[kg_mask, "modal_price"] *= 100.0
                temp_df.loc[kg_mask, "min_price"] *= 100.0
                temp_df.loc[kg_mask, "max_price"] *= 100.0

            sub_df = pd.DataFrame({
                "date": temp_df["parsed_date"],
                "mandi": temp_df["parsed_mandi"],
                "modal_price": temp_df["modal_price"],
                "min_price": temp_df["min_price"].fillna(temp_df["modal_price"]),
                "max_price": temp_df["max_price"].fillna(temp_df["modal_price"]),
                "arrivals": temp_df["arrivals"].fillna(0.0),
                "data_provenance": "real",
                "is_synthetic": False
            })
            all_dfs.append(sub_df)
        except Exception as e:
            logger.error(f"Error parsing real CSV {f}: {e}")

    if not all_dfs:
        return None

    combined = pd.concat(all_dfs, ignore_index=True)
    logger.info(f"Successfully loaded {len(combined):,} real records from Agmarknet CSVs.")

    # Deduplicate and sort
    combined = combined.drop_duplicates(subset=["date", "mandi"]).sort_values(["mandi", "date"]).reset_index(drop=True)

    # Impute short gaps (<= 3 days) and add exogenous calendar features
    cleaned = clean_and_impute_panel(combined, is_synthetic=False)
    return cleaned


def build_daily_panel(config: dict) -> pd.DataFrame:
    """
    Constructs standardized daily panel.
    PRIORITY 1: If real CSVs exist in data/raw/real/, builds EXCLUSIVELY from real data.
    PRIORITY 2: If data/raw/real/ is empty, builds baseline demo panel tagged as SYNTHETIC.
    """
    real_dir = config["paths"].get("real_data_dir", "data/raw/real")
    os.makedirs(real_dir, exist_ok=True)

    real_panel = load_real_agmarknet_panel(real_dir, config)
    if real_panel is not None and len(real_panel) > 0:
        logger.info(
            f"DATA_PROVENANCE: Built panel from REAL Agmarknet data ({len(real_panel):,} rows). "
            f"data_provenance='real', is_synthetic=False."
        )
        return real_panel

    logger.warning(
        "\n" + "!" * 75 + "\n"
        "DATA_PROVENANCE NOTICE:\n"
        "No real CSVs found in 'data/raw/real/'.\n"
        "Constructing baseline demo panel with explicit SYNTHETIC tags.\n"
        "All rows tagged: data_provenance='synthetic', is_synthetic=True.\n"
        "The model training pipeline will REFUSE to train on this data until real CSVs are placed in 'data/raw/real/'.\n"
        + "!" * 75
    )

    seed = config["project"].get("random_seed", 42)
    np.random.seed(seed)

    raw_dir = config["paths"]["raw_data_dir"]
    mandis = config["project"]["target_mandis"]

    dates = pd.date_range(start="2023-01-01", end="2026-11-03", freq="D")
    n_days = len(dates)

    # Monthly arrival weights from CommMktArrivals2012
    month_arrival_weights = {
        1: 0.85, 2: 0.70, 3: 0.95, 4: 1.10, 5: 0.90, 6: 0.80,
        7: 0.85, 8: 1.05, 9: 1.30, 10: 1.65, 11: 1.45, 12: 1.00
    }

    weather_file = os.path.join(raw_dir, "data_season.csv")
    mean_temp_base = 25.0
    if os.path.exists(weather_file):
        try:
            ws = pd.read_csv(weather_file)
            bang_ws = ws[ws["Location"].str.contains("Bangalore", case=False, na=False)]
            if not bang_ws.empty:
                mean_temp_base = float(bang_ws["Temperature"].mean())
        except Exception:
            pass

    diesel_base = config["costs"]["diesel_price_per_liter"]

    # Generate grounded synthetic series
    t = np.arange(n_days)
    annual_cycle = -450 * np.cos(2 * np.pi * t / 365.25) + 350 * np.sin(4 * np.pi * t / 365.25)
    macro_trend = 2800 + 1.1 * t
    shock = np.zeros(n_days)
    for i in range(1, n_days):
        shock[i] = 0.94 * shock[i-1] + np.random.normal(0, 55)

    base_price_series = np.clip(macro_trend + annual_cycle + shock, 1200.0, 7500.0)

    panel_records = []
    for mandi in mandis:
        mandi_cfg = config["mandis"].get(mandi, {})
        mandi_offset = mandi_cfg.get("base_modal_price_offset", 0.0)
        mandi_noise = np.random.normal(0, 25, size=n_days)
        modal_prices = base_price_series + mandi_offset + mandi_noise
        spread = np.random.uniform(250, 650, size=n_days)
        min_prices = modal_prices - spread * 0.45
        max_prices = modal_prices + spread * 0.55

        if "Bengaluru" in mandi:
            base_daily_arr = 18000.0
        elif "Kolar" in mandi:
            base_daily_arr = 350.0
        else:
            base_daily_arr = 220.0

        for idx, dt in enumerate(dates):
            m_weight = month_arrival_weights[dt.month]
            day_mult = 0.2 if dt.weekday() == 6 else (1.2 if dt.weekday() in [0, 3] else 1.0)
            arrival_vol = base_daily_arr * m_weight * day_mult * np.random.uniform(0.75, 1.25)
            temp = mean_temp_base + 4.5 * np.sin(2 * np.pi * (dt.dayofyear - 80) / 365.25) + np.random.normal(0, 1.2)
            rain_prob = 0.55 if dt.month in [6, 7, 8, 9, 10] else 0.12
            rainfall = np.random.exponential(scale=14.0) if np.random.rand() < rain_prob else 0.0
            diesel = diesel_base + (idx / n_days) * 6.5 + np.random.normal(0, 0.4)

            panel_records.append({
                "date": dt,
                "mandi": mandi,
                "modal_price": round(float(modal_prices[idx]), 2),
                "min_price": round(float(min_prices[idx]), 2),
                "max_price": round(float(max_prices[idx]), 2),
                "arrivals": round(float(arrival_vol), 1),
                "rainfall": round(float(rainfall), 2),
                "temperature": round(float(temp), 2),
                "diesel_price": round(float(diesel), 2),
                "festival_flag": 0,
                "month": dt.month,
                "day_of_week": dt.dayofweek,
                "day_of_year": dt.dayofyear,
                "week_of_year": int(dt.isocalendar().week),
                "data_provenance": "synthetic",
                "is_synthetic": True
            })

    df = pd.DataFrame(panel_records)

    # Introduce realistic market gaps and clean
    gap_mask = (np.random.rand(len(df)) < 0.025) & (df["date"] > "2023-02-01")
    df.loc[gap_mask, "modal_price"] = np.nan
    df.loc[gap_mask, "arrivals"] = np.nan

    cleaned_df = clean_and_impute_panel(df, is_synthetic=True)
    return cleaned_df


def clean_and_impute_panel(df: pd.DataFrame, is_synthetic: bool = False) -> pd.DataFrame:
    """
    Handle duplicates, unit mismatches, outliers, and gaps.
    Forward-fill only short gaps (<= 3 days) and add 'was_imputed' flag.
    Maintains strict 'data_provenance' and 'is_synthetic' columns.
    """
    df = df.drop_duplicates(subset=["date", "mandi"]).copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["mandi", "date"]).reset_index(drop=True)

    df["modal_price"] = df["modal_price"].clip(lower=100.0)
    df["arrivals"] = df["arrivals"].clip(lower=0.0)

    # Winsorize extreme anomalies (> 4 standard deviations)
    mean_p = df["modal_price"].mean()
    std_p = df["modal_price"].std()
    upper_bound = mean_p + 4.0 * std_p
    lower_bound = max(100.0, mean_p - 4.0 * std_p)
    df["modal_price"] = df["modal_price"].clip(lower=lower_bound, upper=upper_bound)

    cleaned_mandis = []
    for mandi, m_group in df.groupby("mandi"):
        m_group = m_group.sort_values("date").set_index("date")
        full_idx = pd.date_range(m_group.index.min(), m_group.index.max(), freq="D")
        reindexed = m_group.reindex(full_idx)
        reindexed["mandi"] = mandi

        missing_before = reindexed["modal_price"].isna()
        reindexed["modal_price"] = reindexed["modal_price"].ffill(limit=3)
        reindexed["min_price"] = reindexed["min_price"].ffill(limit=3)
        reindexed["max_price"] = reindexed["max_price"].ffill(limit=3)
        reindexed["arrivals"] = reindexed["arrivals"].ffill(limit=3)

        if "diesel_price" in reindexed.columns:
            reindexed["diesel_price"] = reindexed["diesel_price"].ffill(limit=3).fillna(88.0)
        else:
            reindexed["diesel_price"] = 88.0

        if "temperature" in reindexed.columns:
            reindexed["temperature"] = reindexed["temperature"].ffill(limit=3).fillna(25.0)
        else:
            reindexed["temperature"] = 25.0

        if "rainfall" in reindexed.columns:
            reindexed["rainfall"] = reindexed["rainfall"].fillna(0.0)
        else:
            reindexed["rainfall"] = 0.0

        reindexed["festival_flag"] = 0
        reindexed["month"] = reindexed.index.month
        reindexed["day_of_week"] = reindexed.index.dayofweek
        reindexed["day_of_year"] = reindexed.index.dayofyear
        reindexed["week_of_year"] = [int(w) for w in reindexed.index.isocalendar().week]

        was_imputed = missing_before & reindexed["modal_price"].notna()
        reindexed["was_imputed"] = was_imputed.astype(int)

        reindexed["data_provenance"] = "synthetic" if is_synthetic else "real"
        reindexed["is_synthetic"] = is_synthetic

        reindexed = reindexed.dropna(subset=["modal_price"])
        reindexed = reindexed.reset_index().rename(columns={"index": "date"})
        cleaned_mandis.append(reindexed)

    result_df = pd.concat(cleaned_mandis, ignore_index=True)
    result_df = result_df.sort_values(["date", "mandi"]).reset_index(drop=True)

    logger.info(
        f"Cleaned panel shape: {result_df.shape} | Imputed: {result_df['was_imputed'].sum():,} | "
        f"Data Provenance: '{result_df['data_provenance'].iloc[0]}' (is_synthetic={is_synthetic})"
    )
    return result_df


def run_pipeline():
    """Main pipeline execution routine."""
    logger.info("Starting Data Pipeline execution...")
    config = load_config()
    output_path = config["paths"]["processed_panel"]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    panel_df = build_daily_panel(config)
    panel_df.to_parquet(output_path, index=False)
    logger.info(f"Successfully saved panel with provenance tags to {output_path}")

    assert os.path.exists(output_path), "Target parquet file missing!"
    logger.info("Data Pipeline execution complete.")


if __name__ == "__main__":
    run_pipeline()
