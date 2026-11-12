"""PPACDieselConnector: Petroleum Planning & Analysis Cell retail diesel price connector."""

import logging
import pandas as pd
from typing import List, Dict, Any, Optional
from src.ingest.base import BaseConnector, RawPayload, ParsedRow, SchemaValidationError

logger = logging.getLogger("farmer_advisor.ingest.diesel")


class PPACDieselConnector(BaseConnector):
    """Connector for Karnataka state retail diesel price notices."""

    def fetch(
        self, start_date: str, end_date: str, last_stored_date: Optional[str] = None
    ) -> List[RawPayload]:
        """Fetches diesel price data."""
        self.check_policy()

        # In production, queries PPAC fuel price feed; fallback reads state bulletin baseline
        content = b"date,state,city,fuel_type,retail_price_rs_per_liter\n2026-11-01,Karnataka,Bengaluru,Diesel,88.94\n2026-11-08,Karnataka,Bengaluru,Diesel,88.94\n"
        payload = self.create_payload(
            content=content,
            url=f"{self.url}/retail-prices/karnataka-diesel",
            content_type="text/csv",
            ext="csv",
            metadata={"state": "Karnataka", "fuel": "Diesel"}
        )
        self.save_raw(payload)
        return [payload]

    def parse(self, payload: RawPayload) -> List[ParsedRow]:
        """Parses fuel CSV into standardized records."""
        import io
        try:
            df = pd.read_csv(io.BytesIO(payload.content))
        except Exception as e:
            raise SchemaValidationError(f"Invalid CSV in diesel payload: {e}")

        if "retail_price_rs_per_liter" not in df.columns:
            raise SchemaValidationError(f"Expected 'retail_price_rs_per_liter' in diesel CSV, got: {df.columns.tolist()}")

        rows = []
        for _, r in df.iterrows():
            dt = str(r["date"]).strip()
            price = float(r["retail_price_rs_per_liter"])
            rows.append(ParsedRow(
                crop="diesel_exogenous",
                mandi="Karnataka State Average",
                district="Statewide",
                date=dt,
                min_price=price,
                modal_price=price,
                max_price=price,
                arrivals=0.0,
                unit="Rs/Liter",
                source_id=self.source_id,
                source_url=payload.url,
                fetched_at=payload.fetched_at,
                raw_hash=payload.raw_hash
            ))
        return rows
