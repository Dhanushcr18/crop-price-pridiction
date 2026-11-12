"""OpenMeteoConnector: Agro-meteorology connector for daily weather features."""

import json
import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from src.ingest.base import BaseConnector, RawPayload, ParsedRow, SchemaValidationError

logger = logging.getLogger("farmer_advisor.ingest.weather")


class OpenMeteoConnector(BaseConnector):
    """Connector for Open-Meteo daily agro-climatology (temperature, rainfall)."""

    def fetch(
        self, start_date: str, end_date: str, last_stored_date: Optional[str] = None
    ) -> List[RawPayload]:
        """Fetches daily weather for key Karnataka APMC coordinates."""
        self.check_policy()

        # Incremental fetch check
        effective_start = start_date
        if last_stored_date:
            dt_last = datetime.strptime(last_stored_date, "%Y-%m-%d")
            lookback_dt = dt_last - timedelta(days=7)
            effective_start = max(start_date, lookback_dt.strftime("%Y-%m-%d"))

        payloads = []
        # Representative APMC centroids in Karnataka (Bengaluru, Kolar, Chikkaballapur)
        mandi_coords = [
            ("Bengaluru (Yeshwanthpur)", 13.0285, 77.5450),
            ("Kolar", 13.1367, 78.1340),
            ("Chikkaballapur", 13.4355, 77.7315)
        ]

        for m_name, lat, lon in mandi_coords:
            url = (
                f"{self.url}?latitude={lat}&longitude={lon}"
                f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
                f"&timezone=Asia%2FKolkata&start_date={effective_start}&end_date={end_date}"
            )
            try:
                content = self.execute_http_request(url)
                payload = self.create_payload(
                    content=content,
                    url=url,
                    content_type="application/json",
                    ext="json",
                    metadata={"mandi": m_name, "lat": lat, "lon": lon}
                )
                payloads.append(payload)
                self.save_raw(payload)
            except Exception as e:
                logger.warning(f"[{self.source_id}] Failed to fetch weather for {m_name}: {e}")

        return payloads

    def parse(self, payload: RawPayload) -> List[ParsedRow]:
        """Parses Open-Meteo daily weather response."""
        try:
            data = json.loads(payload.content.decode("utf-8"))
        except Exception as e:
            raise SchemaValidationError(f"Invalid JSON from {payload.url}: {e}")

        if "daily" not in data or "time" not in data["daily"]:
            raise SchemaValidationError(f"Expected 'daily' block in Open-Meteo payload from {payload.url}")

        daily = data["daily"]
        dates = daily.get("time", [])
        temp_max = daily.get("temperature_2m_max", [])
        temp_min = daily.get("temperature_2m_min", [])
        precip = daily.get("precipitation_sum", [])

        mandi_name = (payload.metadata or {}).get("mandi", "Bengaluru (Yeshwanthpur)")
        rows = []

        for i, dt in enumerate(dates):
            t_max = float(temp_max[i]) if i < len(temp_max) and temp_max[i] is not None else 28.0
            t_min = float(temp_min[i]) if i < len(temp_min) and temp_min[i] is not None else 18.0
            t_mean = round((t_max + t_min) / 2.0, 2)
            rainfall = float(precip[i]) if i < len(precip) and precip[i] is not None else 0.0

            rows.append(ParsedRow(
                crop="weather_exogenous",
                mandi=mandi_name,
                district="Karnataka",
                date=dt,
                min_price=t_min,       # used for min temp in weather feature matrix
                modal_price=t_mean,    # used for mean temp
                max_price=t_max,       # used for max temp
                arrivals=rainfall,     # used for precipitation_mm
                unit="Celsius_mm",
                source_id=self.source_id,
                source_url=payload.url,
                fetched_at=payload.fetched_at,
                raw_hash=payload.raw_hash
            ))

        return rows
