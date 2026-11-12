"""Importer for manually downloaded Agmarknet / KSAMB files in data/raw/user_download/.

Strictly enforces:
1. Presence of required columns: mandi, date, min, modal, max.
2. Rejection of files missing any required column with SchemaValidationError.
3. Exact physical line numbering (1-based raw_line) and relative raw_file tracking.
4. Setting acquisition_method='user_download', data_provenance='real', is_synthetic=False.
5. Quarantine of rows failing plausibility, bounds, or logical constraints (min <= modal <= max).
"""

import os
import csv
import json
import hashlib
import logging
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

import pandas as pd

from src.ingest.base import BaseConnector, RawPayload, ParsedRow, SchemaValidationError
from src.ingest.validate import ValidationEngine

logger = logging.getLogger("farmer_advisor.ingest.user_download")

REQUIRED_LOGICAL_COLUMNS = ["mandi", "date", "min", "modal", "max"]

COLUMN_ALIASES: Dict[str, List[str]] = {
    "mandi": [
        "mandi", "market", "market_name", "apmc", "market_yard", "center",
        "mandi_name", "market name", "mandi name", "market center"
    ],
    "date": [
        "date", "arrival_date", "report_date", "trade_date", "price_date",
        "arrival date", "report date", "trade date"
    ],
    "min": [
        "min", "min_price", "minimum", "min_price_rs_quintal", "min_price_rs_qtl",
        "min_price_(rs/quintal)", "min price", "minimum price", "min_price_rs"
    ],
    "modal": [
        "modal", "modal_price", "modal_price_rs_quintal", "modal_price_rs_qtl",
        "modal_price_(rs/quintal)", "modal price", "modal price rs", "modal_price_rs"
    ],
    "max": [
        "max", "max_price", "maximum", "max_price_rs_quintal", "max_price_rs_qtl",
        "max_price_(rs/quintal)", "max price", "maximum price", "max_price_rs"
    ],
    "crop": [
        "crop", "commodity", "commodity_name", "commodity name", "crop_name"
    ],
    "district": [
        "district", "district_name", "district name"
    ],
    "arrivals": [
        "arrivals", "arrival", "arrivals_in_qtl", "arrivals_qtl", "arrival_tonnes",
        "arrivals (tonnes)", "arrivals_tonnes", "quantity"
    ],
    "unit": [
        "unit", "unit_of_price", "price_unit"
    ]
}


def normalize_col_name(col: str) -> str:
    """Normalizes header string for robust matching."""
    return str(col).lower().strip().replace(".", "").replace("/", "_").replace(" ", "_")


def parse_date_flexible(val: str) -> Optional[str]:
    """Parses date string across common formats into ISO YYYY-MM-DD."""
    if not val or not str(val).strip():
        return None
    s = str(val).strip().split(" ")[0].replace("/", "-")
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d-%b-%Y", "%d-%B-%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


class UserDownloadImporter:
    """Imports, verifies, quarantines, and ingests manual Agmarknet/KSAMB download files."""

    def __init__(
        self,
        raw_dir: str = "data/raw/user_download",
        quarantine_dir: str = "data/quarantine",
        today_date_str: str = "2026-11-12",
        mandis_master_path: str = "data/master/mandis.csv"
    ):
        self.raw_dir = raw_dir
        self.quarantine_dir = quarantine_dir
        self.today_date_str = today_date_str
        self.validator = ValidationEngine(quarantine_dir=quarantine_dir, today_date_str=today_date_str)
        self.mandi_district_map = self._load_mandi_district_map(mandis_master_path)
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.quarantine_dir, exist_ok=True)

    def _load_mandi_district_map(self, master_path: str) -> Dict[str, str]:
        """Loads mandi -> district mapping from master data if available."""
        mapping = {}
        if os.path.exists(master_path):
            try:
                df = pd.read_csv(master_path)
                for _, r in df.iterrows():
                    dist = str(r.get("district_en", "")).strip()
                    m_id = str(r.get("mandi_id", "")).strip().lower()
                    name_en = str(r.get("name_en", "")).strip().lower()
                    raw_name = str(r.get("raw_market_name", "")).strip().lower()
                    if dist:
                        if m_id:
                            mapping[m_id] = dist
                        if name_en:
                            mapping[name_en] = dist
                        if raw_name:
                            mapping[raw_name] = dist
            except Exception as e:
                logger.warning(f"Could not load mandis master map from {master_path}: {e}")
        return mapping

    def detect_columns(self, headers: List[str]) -> Tuple[Dict[str, int], List[str]]:
        """Maps file column indices to standard logical fields.
        
        Returns:
            (mapped_indices, missing_required_fields)
        """
        norm_headers = [normalize_col_name(h) for h in headers]
        mapped: Dict[str, int] = {}

        for logical_field, aliases in COLUMN_ALIASES.items():
            for idx, nh in enumerate(norm_headers):
                if nh in aliases or any(alias == nh or alias in nh for alias in aliases):
                    if logical_field not in mapped:
                        mapped[logical_field] = idx
                        break

        missing_required = [req for req in REQUIRED_LOGICAL_COLUMNS if req not in mapped]
        return mapped, missing_required

    def import_file(self, file_path: str, default_crop: str = "onion") -> Dict[str, Any]:
        """Processes a single manual download file.
        
        Strictly raises SchemaValidationError if any of [mandi, date, min, modal, max] is absent.
        Quarantines invalid rows and preserves exact line traceability.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Normalize relative path for audit-trace compliance
        try:
            rel_file_path = os.path.relpath(file_path, os.getcwd()).replace("\\", "/")
        except Exception:
            rel_file_path = file_path.replace("\\", "/")

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            raw_lines = f.readlines()

        if not raw_lines:
            raise SchemaValidationError(f"File '{rel_file_path}' is completely empty.")

        # Read header with CSV sniffer or standard dialect
        sample = "".join(raw_lines[:5])
        delimiter = "\t" if "\t" in raw_lines[0] and "," not in raw_lines[0] else ","
        reader = csv.reader(raw_lines, delimiter=delimiter)

        try:
            header_row = next(reader)
        except StopIteration:
            raise SchemaValidationError(f"File '{rel_file_path}' contains no header line.")

        col_map, missing_cols = self.detect_columns(header_row)
        if missing_cols:
            msg = (
                f"File '{rel_file_path}' rejected: missing required columns: {missing_cols}. "
                f"Found columns: {header_row}. Required columns are: {REQUIRED_LOGICAL_COLUMNS}."
            )
            logger.error(msg)
            raise SchemaValidationError(msg)

        accepted_rows: List[Dict[str, Any]] = []
        quarantined_rows: List[Dict[str, Any]] = []

        line_num = 1  # header was line 1
        fetched_at = datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()

        for row in reader:
            line_num += 1
            if not row or not any(cell.strip() for cell in row):
                continue  # skip empty lines

            raw_line_str = raw_lines[line_num - 1].rstrip("\r\n")
            line_hash = hashlib.sha256(raw_line_str.encode("utf-8")).hexdigest()

            # Helper to safely extract cell
            def get_cell(field: str) -> str:
                idx = col_map.get(field)
                if idx is not None and idx < len(row):
                    return str(row[idx]).strip()
                return ""

            raw_mandi = get_cell("mandi")
            raw_date = get_cell("date")
            raw_min = get_cell("min").replace(",", "")
            raw_modal = get_cell("modal").replace(",", "")
            raw_max = get_cell("max").replace(",", "")
            raw_crop = get_cell("crop") or default_crop
            raw_dist = get_cell("district")
            raw_arr = get_cell("arrivals").replace(",", "") or "0.0"
            raw_unit = get_cell("unit") or "Rs/Quintal"

            # Failure check: missing mandatory cell values
            if not raw_mandi:
                quarantined_rows.append({
                    "raw_file": rel_file_path,
                    "raw_line": line_num,
                    "raw_content": raw_line_str,
                    "rejection_reason": "Missing mandi/market name in row",
                    "row_data": row
                })
                continue

            parsed_d = parse_date_flexible(raw_date)
            if not parsed_d:
                quarantined_rows.append({
                    "raw_file": rel_file_path,
                    "raw_line": line_num,
                    "raw_content": raw_line_str,
                    "rejection_reason": f"Unparseable date '{raw_date}'",
                    "row_data": row
                })
                continue

            # Parse numeric price values
            try:
                min_p = float(raw_min)
                modal_p = float(raw_modal)
                max_p = float(raw_max)
            except ValueError as e:
                quarantined_rows.append({
                    "raw_file": rel_file_path,
                    "raw_line": line_num,
                    "raw_content": raw_line_str,
                    "rejection_reason": f"Non-numeric price values (min='{raw_min}', modal='{raw_modal}', max='{raw_max}'): {e}",
                    "row_data": row
                })
                continue

            try:
                arr_val = float(raw_arr) if raw_arr else 0.0
            except ValueError:
                arr_val = 0.0

            # District lookup if missing
            if not raw_dist:
                raw_dist = self.mandi_district_map.get(raw_mandi.lower(), raw_mandi)

            parsed_record = ParsedRow(
                crop=raw_crop.lower().strip(),
                mandi=raw_mandi.strip(),
                district=raw_dist.strip(),
                date=parsed_d,
                min_price=min_p,
                modal_price=modal_p,
                max_price=max_p,
                arrivals=arr_val,
                unit=raw_unit,
                source_id="user_download",
                source_url=f"file://{rel_file_path}",
                fetched_at=fetched_at,
                raw_hash=line_hash,
                raw_file=rel_file_path,
                raw_line=line_num,
                acquisition_method="user_download"
            )

            is_valid, reason, clean_dict = self.validator.validate_single_row(parsed_record)
            if is_valid and clean_dict is not None:
                accepted_rows.append(clean_dict)
            else:
                quarantined_rows.append({
                    "raw_file": rel_file_path,
                    "raw_line": line_num,
                    "raw_content": raw_line_str,
                    "rejection_reason": reason or "Failed validation check",
                    "parsed_record": parsed_record.__dict__
                })

        # Persist quarantine records if any
        if quarantined_rows:
            batch_id = Path(file_path).stem
            self.validator.quarantine_records(quarantined_rows, batch_id=f"user_download_{batch_id}")

        return {
            "file": rel_file_path,
            "status": "success",
            "total_lines": line_num,
            "total_data_rows": len(accepted_rows) + len(quarantined_rows),
            "accepted_count": len(accepted_rows),
            "quarantined_count": len(quarantined_rows),
            "accepted_rows": accepted_rows,
            "quarantined_rows": quarantined_rows
        }

    def import_directory(self, directory: Optional[str] = None, default_crop: str = "onion") -> Dict[str, Any]:
        """Scans the user_download directory and imports all CSV files."""
        target_dir = directory or self.raw_dir
        csv_files = [
            os.path.join(target_dir, f)
            for f in os.listdir(target_dir)
            if f.lower().endswith((".csv", ".tsv", ".txt"))
        ]

        summary = {
            "directory": target_dir,
            "files_found": len(csv_files),
            "files_processed": 0,
            "files_rejected": 0,
            "rejections": [],
            "total_accepted": 0,
            "total_quarantined": 0,
            "accepted_records": [],
            "quarantined_records": []
        }

        for fpath in sorted(csv_files):
            try:
                res = self.import_file(fpath, default_crop=default_crop)
                summary["files_processed"] += 1
                summary["total_accepted"] += res["accepted_count"]
                summary["total_quarantined"] += res["quarantined_count"]
                summary["accepted_records"].extend(res["accepted_rows"])
                summary["quarantined_records"].extend(res["quarantined_rows"])
            except SchemaValidationError as e:
                summary["files_rejected"] += 1
                summary["rejections"].append({"file": fpath, "reason": str(e)})
            except Exception as e:
                logger.error(f"Error processing {fpath}: {e}")
                summary["files_rejected"] += 1
                summary["rejections"].append({"file": fpath, "reason": str(e)})

        return summary

    def merge_into_panel(
        self,
        accepted_rows: List[Dict[str, Any]],
        panel_path: str = "data/processed/panel.parquet"
    ) -> pd.DataFrame:
        """Merges newly accepted rows into panel.parquet with strict deduplication."""
        if not accepted_rows:
            if os.path.exists(panel_path):
                return pd.read_parquet(panel_path)
            return pd.DataFrame()

        new_df = pd.DataFrame(accepted_rows)

        if os.path.exists(panel_path):
            existing_df = pd.read_parquet(panel_path)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            combined_df = new_df

        # Deduplicate on key: crop, mandi, date
        # If user_download is imported, keep the latest or user_download record
        dedup_cols = ["crop", "mandi", "date"]
        combined_df = combined_df.drop_duplicates(subset=dedup_cols, keep="last").reset_index(drop=True)

        os.makedirs(os.path.dirname(panel_path), exist_ok=True)
        combined_df.to_parquet(panel_path, index=False)
        logger.info(f"Updated {panel_path}: total rows now {len(combined_df)}")
        return combined_df


class UserDownloadConnector(BaseConnector):
    """Connector wrapper for local manual user download directory."""

    def __init__(self, source_config: Dict[str, Any], global_config: Optional[Dict[str, Any]] = None):
        super().__init__(source_config, global_config)
        self.raw_dir = source_config.get("raw_dir", "data/raw/user_download")
        self.importer = UserDownloadImporter(
            raw_dir=self.raw_dir,
            quarantine_dir=self.global_config.get("quarantine_dir", "data/quarantine")
        )

    def fetch(self, start_date: str, end_date: str) -> List[RawPayload]:
        """Scans user_download directory and wraps raw files in RawPayload."""
        payloads = []
        if not os.path.exists(self.raw_dir):
            return payloads

        for fname in os.listdir(self.raw_dir):
            if fname.lower().endswith((".csv", ".tsv", ".txt")):
                fpath = os.path.join(self.raw_dir, fname)
                with open(fpath, "rb") as f:
                    content = f.read()
                fhash = hashlib.sha256(content).hexdigest()
                payloads.append(RawPayload(
                    source_id=self.source_id,
                    url=f"file://{fpath.replace(chr(92), '/')}",
                    content=content,
                    content_type="text/csv",
                    fetched_at=datetime.fromtimestamp(os.path.getmtime(fpath)).isoformat(),
                    raw_hash=fhash,
                    file_extension="csv",
                    metadata={"file_path": fpath, "acquisition_method": "user_download"}
                ))
        return payloads

    def parse(self, payload: RawPayload) -> List[ParsedRow]:
        """Parses raw payload using UserDownloadImporter."""
        # Write to temporary or use file directly
        fpath = payload.metadata.get("file_path") if payload.metadata else None
        if not fpath or not os.path.exists(fpath):
            return []
        res = self.importer.import_file(fpath)
        # Convert accepted records back into ParsedRows if needed by runner
        parsed_list = []
        for r in res["accepted_rows"]:
            parsed_list.append(ParsedRow(
                crop=r["crop"],
                mandi=r["mandi"],
                district=r["district"],
                date=r["date"],
                min_price=r["min_price"],
                modal_price=r["modal_price"],
                max_price=r["max_price"],
                arrivals=r["arrivals"],
                unit=r["unit"],
                source_id=r["source_id"],
                source_url=r["source_url"],
                fetched_at=r["fetched_at"],
                raw_hash=r["raw_hash"],
                raw_file=r["raw_file"],
                raw_line=r["raw_line"],
                acquisition_method=r["acquisition_method"]
            ))
        return parsed_list

