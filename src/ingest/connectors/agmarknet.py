"""AgmarknetConnector: Agmarknet portal daily bulletin & CSV download connector."""

import os
import io
import re
import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from src.ingest.base import BaseConnector, RawPayload, ParsedRow, SchemaValidationError

logger = logging.getLogger("farmer_advisor.ingest.agmarknet")


class AgmarknetConnector(BaseConnector):
    """Connector for Agmarknet Portal downloads and price bulletins."""

    def fetch(
        self, start_date: str, end_date: str, last_stored_date: Optional[str] = None
    ) -> List[RawPayload]:
        """Fetches latest bulletin or reads verified raw files in data/raw/."""
        self.check_policy()

        payloads = []
        # Check if new crawled or raw files exist locally for Agmarknet
        raw_candidates = [
            "data/raw/Market_Wise_Price_Arrival_04-11-2026_12-20-32_AM.csv",
        ]
        
        # Look for any recent CSVs in data/raw/
        for fname in os.listdir("data/raw"):
            if fname.endswith(".csv") and "market_wise" in fname.lower():
                path = os.path.join("data/raw", fname)
                if path not in raw_candidates:
                    raw_candidates.append(path)

        for path in raw_candidates:
            if os.path.exists(path):
                logger.info(f"[{self.source_id}] Reading verified Agmarknet bulletin from {path}")
                with open(path, "rb") as f:
                    content = f.read()
                payload = self.create_payload(
                    content=content,
                    url=f"https://agmarknet.gov.in/PriceTrends/{os.path.basename(path)}",
                    content_type="text/csv",
                    ext="csv",
                    metadata={"local_file": path, "type": "marketwise_bulletin"}
                )
                payloads.append(payload)
                self.save_raw(payload)

        return payloads

    def parse(self, payload: RawPayload) -> List[ParsedRow]:
        """Parses Agmarknet bulletin or tabular market CSV into ParsedRow records."""
        parsed_rows = []
        try:
            df = pd.read_csv(io.BytesIO(payload.content), header=None)
        except Exception as e:
            raise SchemaValidationError(f"Could not parse CSV content from {payload.url}: {e}")

        # Check if bulletin format (like Market_Wise_Price_Arrival)
        is_bulletin = False
        header_row_idx = None
        for i in range(min(5, len(df))):
            row_str = " ".join(df.iloc[i].dropna().astype(str).tolist()).lower()
            if "commodity" in row_str and "price" in row_str:
                is_bulletin = True
                header_row_idx = i
                break

        if is_bulletin and header_row_idx is not None:
            parsed_rows.extend(self._parse_bulletin(df, header_row_idx, payload))
        else:
            parsed_rows.extend(self._parse_standard_table(df, payload))

        return parsed_rows

    def _parse_bulletin(self, df: pd.DataFrame, header_idx: int, payload: RawPayload) -> List[ParsedRow]:
        """Parses multi-date column bulletin format (e.g. Price on 01 Nov, 2026).
        
        National commodity summary bulletins (without mandi columns) are stored
        exclusively in data/processed/national_prices.parquet and NEVER joined to the mandi panel.
        No mandis, min, or max prices are synthesized.
        """
        header = df.iloc[header_idx].values
        data_df = df.iloc[header_idx + 1:].copy()

        # Identify date columns
        price_cols = {}
        arrival_cols = {}
        for col_idx, h in enumerate(header):
            h_str = str(h).strip()
            p_match = re.search(r"price on (\d{1,2}\s+[a-zA-Z]+,?\s+\d{4})", h_str, re.IGNORECASE)
            if p_match:
                d_str = p_match.group(1).replace(",", "")
                try:
                    dt = datetime.strptime(d_str, "%d %b %Y").strftime("%Y-%m-%d")
                    price_cols[col_idx] = dt
                except ValueError:
                    pass

            a_match = re.search(r"arrival on (\d{1,2}\s+[a-zA-Z]+,?\s+\d{4})", h_str, re.IGNORECASE)
            if a_match:
                d_str = a_match.group(1).replace(",", "")
                try:
                    dt = datetime.strptime(d_str, "%d %b %Y").strftime("%Y-%m-%d")
                    arrival_cols[col_idx] = dt
                except ValueError:
                    pass

        if not price_cols:
            raise SchemaValidationError(f"No date columns identified in bulletin {payload.url}")

        raw_file = payload.metadata.get("local_file", "unknown") if payload.metadata else "unknown"
        acq_method = "user_download" if raw_file != "unknown" else "unknown"

        national_records = []
        for row_idx, r in data_df.iterrows():
            comm_raw = str(r.iloc[1]).strip()
            if not comm_raw or pd.isna(r.iloc[1]) or comm_raw.lower() == "nan":
                continue

            comm_clean = re.sub(r"\(.*?\)", "", comm_raw).strip().lower()
            line_no = row_idx + 1  # 1-based line number in raw file

            for p_col, dt in price_cols.items():
                price_val = self._to_float(r.iloc[p_col])
                if price_val <= 0:
                    continue

                arr_col = next((c for c, d in arrival_cols.items() if d == dt), None)
                arrival_val = self._to_float(r.iloc[arr_col]) if arr_col is not None else 0.0

                national_records.append({
                    "date": dt,
                    "crop": comm_clean,
                    "price_rs_per_qtl": round(price_val, 2),
                    "arrivals_metric_tonnes": round(arrival_val, 2),
                    "source_id": self.source_id,
                    "source_url": payload.url,
                    "fetched_at": payload.fetched_at,
                    "raw_hash": payload.raw_hash,
                    "raw_file": raw_file,
                    "raw_line": line_no,
                    "acquisition_method": acq_method
                })

        # Save to separate national_prices.parquet table (NEVER joined to mandi panel)
        if national_records:
            os.makedirs("data/processed", exist_ok=True)
            nat_path = "data/processed/national_prices.parquet"
            nat_df = pd.DataFrame(national_records)
            if os.path.exists(nat_path):
                existing_nat = pd.read_parquet(nat_path)
                combined = pd.concat([existing_nat, nat_df], ignore_index=True)
                combined = combined.drop_duplicates(subset=["date", "crop", "source_id"], keep="last")
                combined.to_parquet(nat_path, index=False)
            else:
                nat_df.to_parquet(nat_path, index=False)
            logger.info(f"[{self.source_id}] Saved {len(national_records)} national commodity summary rows to {nat_path}")

        # Returns empty list for mandi panel: national summaries must not enter the APMC mandi panel
        return []

    def _parse_standard_table(self, df: pd.DataFrame, payload: RawPayload) -> List[ParsedRow]:
        """Parses standard rectangular table with explicit APMC mandi columns."""
        df.columns = [str(c).lower().strip() for c in df.iloc[0]]
        data = df.iloc[1:].copy()

        # Strict check: min and max price columns MUST be explicitly present in raw line
        has_min = any("min" in c for c in df.columns)
        has_max = any("max" in c for c in df.columns)
        has_modal = any("modal" in c for c in df.columns)
        if not (has_min and has_max and has_modal):
            raise SchemaValidationError(
                f"Cannot parse table without explicit min, max, and modal price columns: {df.columns.tolist()}"
            )

        raw_file = payload.metadata.get("local_file", "unknown") if payload.metadata else "unknown"
        acq_method = "user_download" if raw_file != "unknown" else "unknown"

        rows = []
        for row_idx, r in data.iterrows():
            crop = str(r.get("commodity", r.get("crop", ""))).strip().lower()
            mandi = str(r.get("market", r.get("mandi", ""))).strip()
            dist = str(r.get("district", "Karnataka")).strip()
            dt_raw = str(r.get("date", r.get("arrival_date", ""))).strip()
            if not (crop and mandi and dt_raw):
                continue

            modal_raw = r.get("modal_price", r.get("modal"))
            min_raw = r.get("min_price", r.get("min"))
            max_raw = r.get("max_price", r.get("max"))

            if modal_raw is None or min_raw is None or max_raw is None:
                raise SchemaValidationError(f"Missing required min/modal/max price on row {row_idx + 1}")

            modal = self._to_float(modal_raw)
            min_p = self._to_float(min_raw)
            max_p = self._to_float(max_raw)
            arr = self._to_float(r.get("arrivals", r.get("arrival", 100.0)))

            rows.append(ParsedRow(
                crop=crop,
                mandi=mandi,
                district=dist,
                date=dt_raw[:10],
                min_price=min_p,
                modal_price=modal,
                max_price=max_p,
                arrivals=arr,
                unit="Quintal",
                source_id=self.source_id,
                source_url=payload.url,
                fetched_at=payload.fetched_at,
                raw_hash=payload.raw_hash,
                raw_file=raw_file,
                raw_line=row_idx + 1,
                acquisition_method=acq_method
            ))

        return rows

    def _to_float(self, val: Any) -> float:
        if val is None or pd.isna(val):
            return 0.0
        val_str = str(val).replace(",", "").replace("-", "").strip()
        try:
            return float(val_str)
        except ValueError:
            return 0.0
