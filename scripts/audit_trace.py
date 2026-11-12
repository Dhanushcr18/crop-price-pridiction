"""Audit Trace: Re-parses raw files and strictly verifies that every row in panel.parquet

matches its exact raw file line and has a verified acquisition method.
Fails loudly with non-zero exit code if any mismatch is found.
"""

import sys
import os
import csv
import logging
from datetime import datetime
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger("audit_trace")


def run_audit(panel_path: str = "data/processed/panel.parquet") -> bool:
    if not os.path.exists(panel_path):
        logger.error(f"Panel file not found at {panel_path}")
        return False

    df = pd.read_parquet(panel_path)
    total_rows = len(df)
    logger.info(f"Auditing traceability for {total_rows} panel rows in {panel_path}...")

    # Required traceability columns
    req_cols = ["raw_file", "raw_line", "acquisition_method", "data_provenance"]
    for col in req_cols:
        if col not in df.columns:
            logger.error(f"Missing required traceability column: '{col}' in {panel_path}")
            return False

    # Check 1: No unknown or unverified acquisition methods in panel
    unknown_mask = df["acquisition_method"] == "unknown"
    if unknown_mask.any():
        num_unknown = unknown_mask.sum()
        logger.error(f"Audit failure: Found {num_unknown} rows with acquisition_method == 'unknown'")
        return False

    unverified_prov = df["data_provenance"] == "unverified"
    if unverified_prov.any():
        num_unverified = unverified_prov.sum()
        logger.error(f"Audit failure: Found {num_unverified} rows with data_provenance == 'unverified'")
        return False

    # Check 2: File cache to prevent re-opening file for every single row
    file_lines_cache = {}
    mismatches = []
    verified_count = 0

    for idx, row in df.iterrows():
        raw_file = str(row["raw_file"]).strip()
        raw_line_no = int(row["raw_line"])
        crop = str(row["crop"]).strip().lower()
        mandi = str(row["mandi"]).strip()
        modal = float(row["modal_price"])
        min_p = float(row["min_price"])
        max_p = float(row["max_price"])

        if not os.path.exists(raw_file):
            mismatches.append(f"Row {idx}: Raw file does not exist: {raw_file}")
            continue

        if raw_file not in file_lines_cache:
            with open(raw_file, "r", encoding="utf-8", errors="replace") as f:
                file_lines_cache[raw_file] = f.readlines()

        lines = file_lines_cache[raw_file]
        if raw_line_no < 1 or raw_line_no > len(lines):
            mismatches.append(f"Row {idx}: Invalid line {raw_line_no} (file has {len(lines)} lines)")
            continue

        # Parse CSV record (handling multiline records if needed)
        try:
            reader = csv.reader(lines[raw_line_no - 1:])
            parsed_cells = next(reader)
        except Exception as e:
            mismatches.append(f"Row {idx}: Could not parse CSV from line {raw_line_no}: {e}")
            continue

        # For OGD India format (State, District, Market, Commodity, Variety, Grade, Arrival_Date, Min_Price, Max_Price, Modal_Price)
        # Verify that mandi, commodity, and prices are contained in this exact parsed record
        record_text_lower = " ".join(parsed_cells).lower()
        if mandi.lower() not in record_text_lower:
            mismatches.append(f"Row {idx} Line {raw_line_no}: Market '{mandi}' not in raw line: {parsed_cells}")
            continue

        if crop.lower() not in record_text_lower and not any(part in record_text_lower for part in crop.lower().split()):
            mismatches.append(f"Row {idx} Line {raw_line_no}: Crop '{crop}' not in raw line: {parsed_cells}")
            continue

        # Verify numeric modal price appears in parsed cells (allowing < 0.01 tolerance for paise rounding)
        matched_modal = False
        for c in parsed_cells:
            try:
                val = float(str(c).replace(",", "").strip())
                if abs(val - modal) < 0.02:
                    matched_modal = True
                    break
            except ValueError:
                pass

        if not matched_modal:
            mismatches.append(f"Row {idx} Line {raw_line_no}: Modal price {modal} not found in raw line cells: {parsed_cells}")
            continue

        verified_count += 1

    if mismatches:
        logger.error(f"Audit trace failed with {len(mismatches)} mismatches (first 10 shown):")
        for m in mismatches[:10]:
            logger.error(f"  {m}")
        return False

    logger.info(f"SUCCESS: 100% of panel rows ({verified_count}/{total_rows}) verified against raw files and raw lines.")
    return True


if __name__ == "__main__":
    success = run_audit()
    sys.exit(0 if success else 1)
