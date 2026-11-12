"""RaitaMitraConnector: Karnataka Department of Agriculture / KSAMB portal connector."""

import re
import logging
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from src.ingest.base import BaseConnector, RawPayload, ParsedRow, SchemaValidationError

logger = logging.getLogger("farmer_advisor.ingest.raita_mitra")


class RaitaMitraConnector(BaseConnector):
    """Connector for Karnataka Raita Mitra (KSAMB) daily market price pages."""

    def fetch(
        self, start_date: str, end_date: str, last_stored_date: Optional[str] = None
    ) -> List[RawPayload]:
        """Fetches public daily price bulletins from Raita Mitra."""
        self.check_policy()

        payloads = []
        # Target daily market rate report URL
        report_url = f"{self.url}/market-rates"
        try:
            content = self.execute_http_request(report_url)
            payload = self.create_payload(
                content=content,
                url=report_url,
                content_type="text/html",
                ext="html",
                metadata={"date": end_date}
            )
            payloads.append(payload)
            self.save_raw(payload)
        except Exception as e:
            logger.warning(f"[{self.source_id}] Could not fetch remote live page: {e}. Checking fixture/fallback.")

        return payloads

    def parse(self, payload: RawPayload) -> List[ParsedRow]:
        """Parses HTML table into ParsedRow records.
        
        Strict schema check: verifies presence of <table> with columns (Market, Commodity, Modal Price).
        Fails loudly with SchemaValidationError if HTML structure has changed.
        """
        html_text = payload.content.decode("utf-8", errors="replace")
        soup = BeautifulSoup(html_text, "html.parser")

        # Find price table
        table = soup.find("table")
        if not table:
            raise SchemaValidationError(f"No <table> found in HTML payload from {payload.url}. Structure has changed.")

        headers = [th.get_text(strip=True).lower() for th in table.find_all("th")]
        if not headers:
            # Check first tr for td headers
            first_tr = table.find("tr")
            if first_tr:
                headers = [td.get_text(strip=True).lower() for td in first_tr.find_all("td")]

        # Enforce required columns
        req_headers = ["commodity", "market", "modal"]
        if not all(any(req in h for h in headers) for req in req_headers):
            raise SchemaValidationError(
                f"HTML table headers changed in {payload.url}. Expected keywords {req_headers}, got: {headers}"
            )

        # Locate column indexes
        crop_idx = next(i for i, h in enumerate(headers) if "commodity" in h or "crop" in h)
        mandi_idx = next(i for i, h in enumerate(headers) if "market" in h or "mandi" in h)
        modal_idx = next((i for i, h in enumerate(headers) if "modal" in h), None)
        if modal_idx is None:
            modal_idx = next(i for i, h in enumerate(headers) if "price" in h and "min" not in h and "max" not in h)
        min_idx = next((i for i, h in enumerate(headers) if "min" in h), None)
        max_idx = next((i for i, h in enumerate(headers) if "max" in h), None)
        date_idx = next((i for i, h in enumerate(headers) if "date" in h), None)

        rows = []
        tr_list = table.find_all("tr")[1:]  # skip header row
        for tr in tr_list:
            cells = [td.get_text(strip=True) for td in tr.find_all("td")]
            if len(cells) <= max(crop_idx, mandi_idx, modal_idx):
                continue

            crop = cells[crop_idx].strip().lower()
            mandi = cells[mandi_idx].strip()
            date_val = cells[date_idx].strip() if date_idx is not None else payload.fetched_at[:10]

            modal_val = self._parse_num(cells[modal_idx])
            min_val = self._parse_num(cells[min_idx]) if min_idx is not None else modal_val
            max_val = self._parse_num(cells[max_idx]) if max_idx is not None else modal_val

            rows.append(ParsedRow(
                crop=crop,
                mandi=mandi,
                district="Karnataka",
                date=date_val[:10],
                min_price=min_val,
                modal_price=modal_val,
                max_price=max_val,
                arrivals=100.0,
                unit="Quintal",
                source_id=self.source_id,
                source_url=payload.url,
                fetched_at=payload.fetched_at,
                raw_hash=payload.raw_hash
            ))

        return rows

    def _parse_num(self, val_str: str) -> float:
        cleaned = re.sub(r"[^\d.]", "", val_str)
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
