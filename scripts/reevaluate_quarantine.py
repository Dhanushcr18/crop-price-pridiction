"""Re-evaluates quarantined records against the updated crop price bounds."""

import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingest.base import ParsedRow
from src.ingest.validate import ValidationEngine

validator = ValidationEngine(today_date_str="2026-11-12")
q_dir = "data/quarantine"
rescued = []
still_invalid = []

seen_hashes = set()

for fname in os.listdir(q_dir):
    if fname.endswith(".json"):
        with open(os.path.join(q_dir, fname), "r") as f:
            records = json.load(f)
        for r in records:
            raw = r.get("raw_record", {})
            key = (raw.get("crop"), raw.get("mandi"), raw.get("date"), raw.get("modal_price"))
            if key in seen_hashes:
                continue
            seen_hashes.add(key)
            parsed_args = {k: v for k, v in raw.items() if k in ParsedRow.__dataclass_fields__}
            row = ParsedRow(**parsed_args)
            is_valid, reason, clean = validator.validate_single_row(row)
            if is_valid:
                rescued.append(clean)
            else:
                still_invalid.append((row.crop, row.modal_price, reason))

print("\n" + "=" * 80)
print("QUARANTINE RE-EVALUATION WITH COMMODITY PRICE BOUNDS")
print("=" * 80)
print(f"Total Unique Quarantined Evaluated : {len(rescued) + len(still_invalid)}")
print(f"Successfully Rescued & Accepted    : {len(rescued)}")
print(f"Still Quarantined (True Anomalies) : {len(still_invalid)}")

print("\n--- SAMPLE RESCUED HIGH-VALUE CROPS (PEPPER, WALNUT, COPRA, SPICES) ---")
for idx, r in enumerate(rescued[:15], 1):
    c_name = r["crop"].title()
    m_name = r["mandi"]
    p_val = r["modal_price"]
    print(f"{idx:2d}. {c_name:25s} | {m_name:28s} | Rs {p_val:10,.2f}/qtl")

if still_invalid:
    print("\n--- STILL QUARANTINED ANOMALIES (OUT OF SANE BOUNDS) ---")
    for idx, (crop, price, reason) in enumerate(still_invalid[:10], 1):
        print(f"{idx:2d}. {crop:25s} | Rs {price:10,.2f} | Reason: {reason}")
