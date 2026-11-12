"""Run real ingest for the last 30 days and display complete diagnostics."""

import os
import sys
import json
import pandas as pd

# Add repo root to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingest.runner import IngestionRunner

runner = IngestionRunner(today_date="2026-11-12")
summary = runner.run(lookback_days=30, update_panel=True)

print("\n" + "=" * 80)
print("REAL INGESTION EXECUTION SUMMARY (LAST 30 DAYS)")
print("=" * 80)
print(f"Execution Date : {summary['execution_date']}")
print(f"Date Window    : {summary['start_date']} to {summary['end_date']}")
print(f"Total Fetched  : {summary['total_fetched']}")
print(f"Total Accepted : {summary['total_accepted']}")
print(f"Quarantined    : {summary['total_quarantined']}")

print("\n--- PER-SOURCE BREAKDOWN ---")
for s_id, stat in summary["per_source_stats"].items():
    print(f"\nSource ID: {s_id}")
    print(f"  Name        : {stat['name']}")
    print(f"  Status      : {stat['status']}")
    print(f"  Fetched     : {stat['fetched']}")
    print(f"  Accepted    : {stat['accepted']}")
    print(f"  Quarantined : {stat['quarantined']}")
    if stat["reasons"]:
        print(f"  Reasons     : {stat['reasons']}")
    if stat["raw_files"]:
        print(f"  Raw Payloads: {len(stat['raw_files'])} file(s)")

print("\n--- MANDI COVERAGE (DATE RANGE & ROW COUNTS) ---")
for mandi, m_stat in summary["mandi_stats"].items():
    print(f"Mandi: {mandi:30s} | Rows: {m_stat['count']:3d} | Dates: {m_stat['min_date']} to {m_stat['max_date']} | Commodities: {', '.join(m_stat['crops'][:4])}")

print("\n--- 10 RANDOM / REPRESENTATIVE ROWS NEXT TO RAW FILES ---")
for idx, r in enumerate(summary["sample_rows"][:10], 1):
    raw_hash = r.get("raw_hash", "")[:16]
    s_id = r.get("source_id", "")
    date_f = r.get("fetched_at", "")[:10]
    expected_path = f"data/raw/crawled/{s_id}/{date_f}/{raw_hash}.*"
    print(f"{idx:2d}. [{r['crop'].title():12s}] {r['mandi']:25s} | {r['date']} | Modal: Rs {r['modal_price']:8.2f}/qtl | Source: {s_id:18s} | Raw: {expected_path}")
