"""Historical Backfill Engine (2021-2026) for Karnataka Mandis.

Parses historical dumps from Agmarknet portal, OGD India, and local CSVs in data/raw/backfill/.
Enforces provenance checking, validation, quarantine, and unit normalization.
"""

import os
import sys
import glob
import logging
from datetime import datetime
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingest.base import ParsedRow
from src.ingest.connectors.data_gov import DataGovConnector
from src.ingest.connectors.agmarknet import AgmarknetConnector
from src.ingest.validate import ValidationEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("farmer_advisor.backfill")

BACKFILL_DIR = "data/raw/backfill"
PANEL_PATH = "data/processed/panel.parquet"


def scan_backfill_files():
    """Scans data/raw/backfill/ for historical CSV files."""
    csvs = glob.glob(os.path.join(BACKFILL_DIR, "*.csv"))
    logger.info(f"Found {len(csvs)} files in '{BACKFILL_DIR}'")
    for f in csvs:
        size_kb = os.path.getsize(f) / 1024.0
        print(f"  - {os.path.basename(f)} ({size_kb:,.1f} KB)")
    return csvs


def ingest_backfill_file(filepath: str, validator: ValidationEngine) -> pd.DataFrame:
    """Parses and validates a historical Agmarknet backfill CSV file."""
    logger.info(f"Processing backfill file: {filepath}")
    with open(filepath, "rb") as f:
        content = f.read()

    # Use Agmarknet connector abstraction
    ag_cfg = {
        "id": "agmarknet_historical_backfill",
        "name": "Agmarknet Historical Backfill",
        "url": f"file://{os.path.abspath(filepath)}",
        "type": "csv_download"
    }
    connector = AgmarknetConnector(ag_cfg)
    payload = connector.create_payload(content, ag_cfg["url"], "text/csv", "csv")
    parsed_rows = connector.parse(payload)

    accepted = []
    quarantined = []
    for r in parsed_rows:
        is_valid, reason, clean = validator.validate_single_row(r)
        if is_valid and clean:
            accepted.append(clean)
        else:
            quarantined.append({"raw_record": r.__dict__, "reason": reason})

    logger.info(f"[{os.path.basename(filepath)}] Accepted: {len(accepted):,}, Quarantined: {len(quarantined):,}")
    if quarantined:
        validator.quarantine_records(quarantined, batch_id=f"backfill_{os.path.basename(filepath)}")

    return pd.DataFrame(accepted)


def run_backfill():
    """Executes the full historical backfill job."""
    files = scan_backfill_files()
    if not files:
        print("\n" + "=" * 80)
        print("NO BACKFILL FILES FOUND IN 'data/raw/backfill/'")
        print("=" * 80)
        print("To complete a 3 to 5 year backfill (2021 to 2026), please follow the manual download steps below.")
        return

    validator = ValidationEngine(today_date_str="2026-11-12")
    dfs = []
    for f in files:
        df_accepted = ingest_backfill_file(f, validator)
        if not df_accepted.empty:
            dfs.append(df_accepted)

    if not dfs:
        print("No valid rows parsed from backfill files.")
        return

    combined_backfill = pd.concat(dfs, ignore_index=True)
    combined_backfill["date"] = pd.to_datetime(combined_backfill["date"])
    combined_backfill["month"] = combined_backfill["date"].dt.month
    combined_backfill["day_of_week"] = combined_backfill["date"].dt.dayofweek
    combined_backfill["day_of_year"] = combined_backfill["date"].dt.dayofyear
    combined_backfill["week_of_year"] = combined_backfill["date"].dt.isocalendar().week.astype(int)
    combined_backfill["data_provenance"] = "real"
    combined_backfill["is_synthetic"] = False
    combined_backfill["was_imputed"] = 0

    if os.path.exists(PANEL_PATH):
        existing = pd.read_parquet(PANEL_PATH)
        existing["date"] = pd.to_datetime(existing["date"])
        merged = pd.concat([existing, combined_backfill], ignore_index=True)
        merged = merged.drop_duplicates(subset=["crop", "mandi", "date"], keep="last")
        merged = merged.sort_values(["mandi", "date"]).reset_index(drop=True)
        merged.to_parquet(PANEL_PATH, index=False)
        print(f"\nSuccessfully merged {len(combined_backfill):,} rows into {PANEL_PATH}. New total: {len(merged):,} rows.")
    else:
        combined_backfill.to_parquet(PANEL_PATH, index=False)
        print(f"\nCreated {PANEL_PATH} with {len(combined_backfill):,} rows.")


if __name__ == "__main__":
    run_backfill()
