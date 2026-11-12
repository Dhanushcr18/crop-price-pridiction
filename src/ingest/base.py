"""Base connector interface, data classes, and throttling abstractions for data collection."""

import os
import time
import json
import hashlib
import logging
from datetime import datetime, date
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
import urllib.request
import urllib.error
import ssl

logger = logging.getLogger("farmer_advisor.ingest")


class PolicyBlockedError(RuntimeError):
    """Raised when crawling/scraping is blocked by robots.txt or terms of service policy."""
    pass


class SchemaValidationError(ValueError):
    """Raised when incoming raw payload violates expected structure or changed layout."""
    pass


@dataclass
class RawPayload:
    """Byte-for-byte untouched raw response from a data source."""
    source_id: str
    url: str
    content: bytes
    content_type: str
    fetched_at: str
    raw_hash: str
    file_extension: str = "json"
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ParsedRow:
    """Standardized commodity price & arrival record."""
    crop: str
    mandi: str
    district: str
    date: str  # YYYY-MM-DD
    min_price: float
    modal_price: float
    max_price: float
    arrivals: float
    unit: str
    source_id: str
    source_url: str
    fetched_at: str
    raw_hash: str
    raw_file: str = "unknown"
    raw_line: int = 0
    acquisition_method: str = "unknown"  # "live_http" | "user_download" | "unknown"


@dataclass
class NationalPriceRow:
    """National or multi-market aggregate commodity price record (no individual APMC mandi)."""
    date: str
    crop: str
    price_rs_per_qtl: float
    arrivals_metric_tonnes: float
    source_id: str
    source_url: str
    fetched_at: str
    raw_hash: str
    raw_file: str
    raw_line: int
    acquisition_method: str = "user_download"


class BaseConnector:
    """Abstract base class for all data source connectors."""

    def __init__(self, source_config: Dict[str, Any], global_config: Optional[Dict[str, Any]] = None):
        self.config = source_config
        self.global_config = global_config or {}
        self.source_id = source_config["id"]
        self.name = source_config["name"]
        self.url = source_config["url"]
        self.source_type = source_config.get("type", "api")
        self.enabled = bool(source_config.get("enabled", True))
        self.robots_allowed = bool(source_config.get("robots_allowed", True))
        self.priority = int(source_config.get("priority", 5))

        self.user_agent = self.global_config.get(
            "user_agent",
            "FarmerSellAdvisorBot/1.0 (+https://farmer-sell-advisor.org; contact@farmer-sell-advisor.org)"
        )
        self.delay_seconds = float(self.global_config.get("default_delay_seconds", 2.0))
        self.max_retries = int(self.global_config.get("max_retries", 3))
        self.backoff_factor = float(self.global_config.get("backoff_factor", 2.0))
        self.timeout_seconds = int(self.global_config.get("timeout_seconds", 15))
        self.raw_storage_dir = self.global_config.get("raw_storage_dir", "data/raw/crawled")

        self.ssl_ctx = ssl.create_default_context()
        self.ssl_ctx.check_hostname = False
        self.ssl_ctx.verify_mode = ssl.CERT_NONE

    def check_policy(self):
        """Enforces robots.txt and terms-of-service compliance.
        
        Strictly raises PolicyBlockedError if source is disabled or forbidden by policy.
        """
        if not self.enabled or not self.robots_allowed:
            reason = self.config.get("status_reason", "Automated access disallowed by policy or robots.txt")
            logger.warning(f"Source '{self.source_id}' is BLOCKED by policy: {reason}")
            raise PolicyBlockedError(f"Source '{self.source_id}' is blocked by policy: {reason}")

    def execute_http_request(self, target_url: str, headers: Optional[Dict[str, str]] = None) -> bytes:
        """Executes HTTP GET with User-Agent, politeness throttling, and exponential backoff."""
        self.check_policy()

        req_headers = {"User-Agent": self.user_agent}
        if headers:
            req_headers.update(headers)

        time.sleep(self.delay_seconds)

        attempt = 0
        current_delay = self.delay_seconds
        last_error = None

        while attempt < self.max_retries:
            attempt += 1
            try:
                logger.info(f"[{self.source_id}] Fetching {target_url} (Attempt {attempt}/{self.max_retries})")
                req = urllib.request.Request(target_url, headers=req_headers)
                with urllib.request.urlopen(req, timeout=self.timeout_seconds, context=self.ssl_ctx) as response:
                    content = response.read()
                    logger.info(f"[{self.source_id}] Successfully received {len(content)} bytes from {target_url}")
                    return content
            except urllib.error.HTTPError as e:
                last_error = e
                logger.warning(f"[{self.source_id}] HTTP error {e.code} on {target_url}: {e.reason}")
                if e.code in [401, 403, 404]:
                    # Unrecoverable or forbidden
                    break
            except Exception as e:
                last_error = e
                logger.warning(f"[{self.source_id}] Network error on attempt {attempt}: {e}")

            time.sleep(current_delay)
            current_delay *= self.backoff_factor

        raise RuntimeError(f"Failed to fetch {target_url} after {attempt} attempts: {last_error}")

    def save_raw(self, payload: RawPayload) -> str:
        """Saves raw bytes untouched to data/raw/crawled/<source_id>/<date>/<hash>.<ext>."""
        date_folder = payload.fetched_at[:10]  # YYYY-MM-DD
        target_dir = os.path.join(self.raw_storage_dir, self.source_id, date_folder)
        os.makedirs(target_dir, exist_ok=True)

        filename = f"{payload.raw_hash[:16]}.{payload.file_extension}"
        filepath = os.path.join(target_dir, filename)

        with open(filepath, "wb") as f:
            f.write(payload.content)

        # Also write sidecar metadata
        meta_filepath = os.path.join(target_dir, f"{payload.raw_hash[:16]}_meta.json")
        with open(meta_filepath, "w", encoding="utf-8") as f:
            json.dump({
                "source_id": payload.source_id,
                "url": payload.url,
                "fetched_at": payload.fetched_at,
                "raw_hash": payload.raw_hash,
                "bytes": len(payload.content),
                "content_type": payload.content_type,
                "metadata": payload.metadata or {}
            }, f, indent=2)

        return filepath

    def create_payload(
        self, content: bytes, url: str, content_type: str = "text/csv", ext: str = "csv", metadata: Optional[Dict[str, Any]] = None
    ) -> RawPayload:
        """Creates RawPayload with computed SHA-256 hash and timestamp."""
        raw_hash = hashlib.sha256(content).hexdigest()
        now_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return RawPayload(
            source_id=self.source_id,
            url=url,
            content=content,
            content_type=content_type,
            fetched_at=now_iso,
            raw_hash=raw_hash,
            file_extension=ext,
            metadata=metadata
        )

    def fetch(
        self, start_date: str, end_date: str, last_stored_date: Optional[str] = None
    ) -> List[RawPayload]:
        """Fetches raw data for specified date window. Must be implemented by subclasses."""
        raise NotImplementedError

    def parse(self, payload: RawPayload) -> List[ParsedRow]:
        """Parses raw payload into standardized ParsedRow records. Must be implemented by subclasses."""
        raise NotImplementedError
