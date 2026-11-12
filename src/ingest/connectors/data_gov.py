"""DataGovConnector: Open Government Data (OGD) Agmarknet daily price connector."""

import os
import json
import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from src.ingest.base import BaseConnector, RawPayload, ParsedRow, SchemaValidationError

logger = logging.getLogger("farmer_advisor.ingest.data_gov")


class DataGovConnector(BaseConnector):
    """Connector for data.gov.in Agmarknet Resource API (9ef84268-d588-465a-a308-a864a43d0070)."""

    def fetch(
        self, start_date: str, end_date: str, last_stored_date: Optional[str] = None
    ) -> List[RawPayload]:
        """Fetches data from data.gov.in or local verified cache."""
        self.check_policy()

        # Incremental fetch: if last_stored_date is provided, only fetch newer
        effective_start = start_date
        if last_stored_date:
            # Look-back window of 7 days to catch late revisions
            dt_last = datetime.strptime(last_stored_date, "%Y-%m-%d")
            lookback_dt = dt_last - timedelta(days=7)
            effective_start = max(start_date, lookback_dt.strftime("%Y-%m-%d"))
            logger.info(f"[{self.source_id}] Incremental fetch active: start={effective_start} (last_stored={last_stored_date})")

        api_key = os.environ.get(self.config.get("auth_env_var", "DATA_GOV_API_KEY"), "")
        payloads = []

        if api_key:
            # Live API call
            query_url = (
                f"{self.url}?api-key={api_key}&format=json&limit=2000"
                f"&filters[State]=Karnataka"
            )
            content = self.execute_http_request(query_url)
            payload = self.create_payload(
                content=content,
                url=query_url,
                content_type="application/json",
                ext="json",
                metadata={"start_date": effective_start, "end_date": end_date}
            )
            payloads.append(payload)
            self.save_raw(payload)
        else:
            # Local verified file fallback when API key not set in environment
            local_fallback = "data/raw/9ef84268-d588-465a-a308-a864a43d0070.csv"
            if os.path.exists(local_fallback):
                logger.info(f"[{self.source_id}] DATA_GOV_API_KEY not set; reading verified local repository file: {local_fallback}")
                with open(local_fallback, "rb") as f:
                    content = f.read()
                payload = self.create_payload(
                    content=content,
                    url=f"file://{os.path.abspath(local_fallback)}",
                    content_type="text/csv",
                    ext="csv",
                    metadata={"source": "verified_local_dump", "start_date": effective_start, "end_date": end_date}
                )
                payloads.append(payload)
                self.save_raw(payload)
            else:
                logger.warning(f"[{self.source_id}] Neither DATA_GOV_API_KEY nor local fallback file found.")

        return payloads

    def parse(self, payload: RawPayload) -> List[ParsedRow]:
        """Parses payload into standardized ParsedRow objects.
        
        Enforces strict schema validation. Fails loudly on schema mismatch.
        """
        parsed_rows = []

        if payload.content_type == "application/json" or payload.file_extension == "json":
            try:
                data = json.loads(payload.content.decode("utf-8", errors="replace"))
            except Exception as e:
                raise SchemaValidationError(f"Invalid JSON payload in {payload.url}: {e}")

            if "records" not in data or not isinstance(data["records"], list):
                raise SchemaValidationError(f"Expected 'records' array in data.gov.in payload, got: {list(data.keys())}")

            raw_file = payload.metadata.get("saved_path", payload.url) if payload.metadata else payload.url
            records = data["records"]
            for r_idx, r in enumerate(records):
                # Schema check
                req_fields = ["State", "District", "Market", "Commodity", "Arrival_Date", "Modal_Price", "Min_Price", "Max_Price"]
                alt_req = ["State", "District", "Market", "Commodity", "Arrival_Date", "Modal_x0020_Price", "Min_x0020_Price", "Max_x0020_Price"]
                if not (all(f in r for f in req_fields) or all(f in r for f in alt_req)):
                    raise SchemaValidationError(f"Missing required price/location fields in record on index {r_idx}: {r}")

                state = str(r.get("State", "")).strip()
                if "karnat" not in state.lower() and state:
                    # Filter for Karnataka
                    continue

                date_raw = str(r.get("Arrival_Date", "")).strip()
                parsed_date = self._parse_date(date_raw)

                crop = str(r.get("Commodity", "")).strip()
                mandi = str(r.get("Market", "")).strip()
                district = str(r.get("District", "")).strip()

                modal_p = self._to_float(r.get("Modal_Price", r.get("Modal_x0020_Price")))
                min_p = self._to_float(r.get("Min_Price", r.get("Min_x0020_Price")))
                max_p = self._to_float(r.get("Max_Price", r.get("Max_x0020_Price")))
                arrivals = self._to_float(r.get("Arrivals", 0.0))

                parsed_rows.append(ParsedRow(
                    crop=crop,
                    mandi=mandi,
                    district=district,
                    date=parsed_date,
                    min_price=min_p,
                    modal_price=modal_p,
                    max_price=max_p,
                    arrivals=arrivals,
                    unit="Quintal",
                    source_id=self.source_id,
                    source_url=payload.url,
                    fetched_at=payload.fetched_at,
                    raw_hash=payload.raw_hash,
                    raw_file=raw_file,
                    raw_line=r_idx + 1,
                    acquisition_method="live_http"
                ))

        elif payload.content_type == "text/csv" or payload.file_extension == "csv":
            import io
            import csv
            
            raw_text = payload.content.decode("utf-8", errors="replace")
            reader = csv.reader(io.StringIO(raw_text))
            try:
                raw_header = next(reader)
            except StopIteration:
                raise SchemaValidationError(f"Empty CSV payload in {payload.url}")

            col_names = [c.lower().strip().replace("_x0020_", " ").replace(" ", "_") for c in raw_header]
            req = ["market", "commodity", "arrival_date", "modal_price", "min_price", "max_price"]
            if not all(any(r in c for c in col_names) for r in req):
                raise SchemaValidationError(f"CSV missing mandatory price or market columns: {col_names}")

            date_idx = next(i for i, c in enumerate(col_names) if "arrival_date" in c or "date" in c)
            mandi_idx = next(i for i, c in enumerate(col_names) if "market" in c)
            crop_idx = next(i for i, c in enumerate(col_names) if "commodity" in c)
            dist_idx = next((i for i, c in enumerate(col_names) if "district" in c), None)
            modal_idx = next(i for i, c in enumerate(col_names) if "modal" in c)
            min_idx = next(i for i, c in enumerate(col_names) if "min" in c)
            max_idx = next(i for i, c in enumerate(col_names) if "max" in c)

            raw_file = payload.metadata.get("local_file", "data/raw/9ef84268-d588-465a-a308-a864a43d0070.csv") if payload.metadata else "data/raw/9ef84268-d588-465a-a308-a864a43d0070.csv"

            start_line = 2
            for row in reader:
                line_no = start_line
                start_line = reader.line_num + 1

                if len(row) <= max(date_idx, mandi_idx, crop_idx, modal_idx, min_idx, max_idx):
                    continue

                crop = str(row[crop_idx]).strip()
                mandi = str(row[mandi_idx]).strip()
                dist = str(row[dist_idx]).strip() if dist_idx is not None else "Unknown"
                parsed_date = self._parse_date(str(row[date_idx]))

                modal_str = row[modal_idx].strip()
                min_str = row[min_idx].strip()
                max_str = row[max_idx].strip()

                if not modal_str or not min_str or not max_str:
                    raise SchemaValidationError(f"Price missing in raw CSV line {line_no}")

                modal_p = self._to_float(modal_str)
                min_p = self._to_float(min_str)
                max_p = self._to_float(max_str)

                parsed_rows.append(ParsedRow(
                    crop=crop,
                    mandi=mandi,
                    district=dist,
                    date=parsed_date,
                    min_price=min_p,
                    modal_price=modal_p,
                    max_price=max_p,
                    arrivals=100.0,
                    unit="Quintal",
                    source_id=self.source_id,
                    source_url=payload.url,
                    fetched_at=payload.fetched_at,
                    raw_hash=payload.raw_hash,
                    raw_file=raw_file,
                    raw_line=line_no,
                    acquisition_method="user_download"
                ))

        return parsed_rows

    def _parse_date(self, d_str: str) -> str:
        """Parses date string into YYYY-MM-DD."""
        d_str = d_str.strip()
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%b/%Y", "%d %b %Y"):
            try:
                return datetime.strptime(d_str, fmt).strftime("%Y-%m-%d")
            except ValueError:
                pass
        return d_str[:10]

    def _to_float(self, val: Any) -> float:
        if val is None or pd.isna(val):
            return 0.0
        try:
            return float(str(val).replace(",", "").strip())
        except ValueError:
            return 0.0
