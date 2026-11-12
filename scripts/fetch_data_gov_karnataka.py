"""Fetch daily real price records from data.gov.in filtered to Karnataka (Onion, Tomato, Potato).

Strict provenance rules:
- Does NOT schedule any cron or background daemon.
- Reads API key strictly from DATA_GOV_API_KEY environment variable.
- Saves raw untouched HTTP responses to data/raw/crawled/data_gov_in/<YYYY-MM-DD>/.
- Never invents, fills, or synthesizes missing rows.
"""

import os
import sys
import json
import hashlib
import logging
from datetime import datetime
from typing import Dict, Any, List
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger("fetch_data_gov_karnataka")

RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
BASE_URL = f"https://api.data.gov.in/resource/{RESOURCE_ID}"
TARGET_CROPS = ["Onion", "Tomato", "Potato"]
TARGET_STATE = "Karnataka"


def fetch_karnataka_daily_records() -> Dict[str, Any]:
    api_key = os.environ.get("DATA_GOV_API_KEY", "").strip()
    if not api_key:
        logger.warning(
            "DATA_GOV_API_KEY is not set in environment. "
            "Please obtain a free API key from https://data.gov.in and set "
            "DATA_GOV_API_KEY=<your_api_key> before running."
        )
        return {
            "status": "missing_api_key",
            "message": "DATA_GOV_API_KEY environment variable is missing",
            "records_count": 0
        }

    today_str = datetime.now().strftime("%Y-%m-%d")
    out_dir = os.path.join("data", "raw", "crawled", "data_gov_in", today_str)
    os.makedirs(out_dir, exist_ok=True)

    records_collected: List[Dict[str, Any]] = []
    
    for crop in TARGET_CROPS:
        params = {
            "api-key": api_key,
            "format": "json",
            "offset": 0,
            "limit": 1000,
            "filters[state]": TARGET_STATE,
            "filters[commodity]": crop
        }
        
        logger.info(f"Querying data.gov.in for State={TARGET_STATE}, Commodity={crop}...")
        try:
            resp = requests.get(BASE_URL, params=params, timeout=30)
            status_code = resp.status_code
            raw_bytes = resp.content
            raw_hash = hashlib.sha256(raw_bytes).hexdigest()

            # Save raw untouched response bytes
            raw_file_name = f"response_{crop.lower()}_{datetime.now().strftime('%H%M%S')}.json"
            raw_file_path = os.path.join(out_dir, raw_file_name)
            with open(raw_file_path, "wb") as f:
                f.write(raw_bytes)

            data = resp.json() if status_code == 200 else {}
            records = data.get("records", []) if isinstance(data, dict) else []
            records_collected.extend(records)

            # Save metadata alongside
            meta = {
                "url": resp.url.split("api-key=")[0] + "api-key=REDACTED",
                "http_status": status_code,
                "timestamp": datetime.now().isoformat(),
                "crop": crop,
                "state": TARGET_STATE,
                "raw_file": raw_file_path,
                "sha256": raw_hash,
                "records_returned": len(records),
                "acquisition_method": "live_http"
            }
            meta_path = os.path.join(out_dir, f"meta_{crop.lower()}_{datetime.now().strftime('%H%M%S')}.json")
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)

            logger.info(f"Saved {len(records)} records for {crop} (HTTP {status_code}) -> {raw_file_path}")

        except Exception as e:
            logger.error(f"Failed to fetch {crop} from data.gov.in: {e}")

    return {
        "status": "success",
        "records_count": len(records_collected),
        "target_dir": out_dir
    }


if __name__ == "__main__":
    result = fetch_karnataka_daily_records()
    print(json.dumps(result, indent=2))
