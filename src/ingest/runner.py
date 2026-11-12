"""Ingestion pipeline coordinator: fetches, validates, quarantines, reconciles, and reports daily."""

import os
import yaml
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pandas as pd

from src.ingest.base import PolicyBlockedError
from src.ingest.connectors import get_connector
from src.ingest.validate import ValidationEngine

logger = logging.getLogger("farmer_advisor.ingest.runner")


class IngestionRunner:
    """Runs data ingestion across registered sources, enforces quarantine, and writes audit reports."""

    def __init__(self, sources_config_path: str = "config/sources.yaml", today_date: str = "2026-11-12"):
        self.sources_config_path = sources_config_path
        self.today_date = today_date

        with open(sources_config_path, "r", encoding="utf-8") as f:
            self.registry = yaml.safe_load(f)

        self.crawler_defaults = self.registry.get("crawler_defaults", {})
        self.sources = self.registry.get("sources", [])
        self.validator = ValidationEngine(
            quarantine_dir=self.crawler_defaults.get("quarantine_dir", "data/quarantine"),
            today_date_str=today_date
        )

    def run(
        self,
        lookback_days: int = 30,
        source_id_filter: Optional[str] = None,
        update_panel: bool = True
    ) -> Dict[str, Any]:
        """
        Executes ingestion across all enabled sources.
        
        Args:
            lookback_days: Number of historical days to fetch up to today (2026-11-12)
            source_id_filter: Optional specific source ID to run in isolation
            update_panel: If True, merges accepted rows idempotently into data/processed/panel.parquet
        """
        end_dt = datetime.strptime(self.today_date, "%Y-%m-%d")
        start_dt = end_dt - timedelta(days=lookback_days)
        start_str = start_dt.strftime("%Y-%m-%d")
        end_str = self.today_date

        audit_summary = {
            "execution_date": self.today_date,
            "start_date": start_str,
            "end_date": end_str,
            "sources_evaluated": [],
            "total_fetched": 0,
            "total_accepted": 0,
            "total_quarantined": 0,
            "per_source_stats": {},
            "discrepancies": [],
            "mandi_stats": {},
            "sample_rows": []
        }

        all_accepted_rows = []
        source_priorities = {s["id"]: int(s.get("priority", 5)) for s in self.sources}

        for s_cfg in self.sources:
            s_id = s_cfg["id"]
            if source_id_filter and s_id != source_id_filter:
                continue

            audit_summary["sources_evaluated"].append(s_id)
            source_stat = {
                "name": s_cfg["name"],
                "type": s_cfg.get("type", "api"),
                "status": "pending",
                "fetched": 0,
                "accepted": 0,
                "quarantined": 0,
                "reasons": {},
                "raw_files": []
            }

            # Policy Check
            if not s_cfg.get("enabled", True) or not s_cfg.get("robots_allowed", True):
                source_stat["status"] = "blocked_by_policy"
                source_stat["reasons"]["policy"] = s_cfg.get("status_reason", "Automated access disallowed by policy or robots.txt")
                audit_summary["per_source_stats"][s_id] = source_stat
                logger.info(f"Source {s_id} skipped: blocked by policy.")
                continue

            try:
                connector = get_connector(s_cfg, self.crawler_defaults)
                payloads = connector.fetch(start_date=start_str, end_date=end_str)
                source_stat["raw_files"] = [p.url for p in payloads]

                parsed_rows = []
                for p in payloads:
                    try:
                        p_rows = connector.parse(p)
                        parsed_rows.extend(p_rows)
                    except Exception as e:
                        logger.error(f"[{s_id}] Parsing error for {p.url}: {e}")
                        source_stat["reasons"]["parser_schema_error"] = str(e)

                source_stat["fetched"] = len(parsed_rows)
                audit_summary["total_fetched"] += len(parsed_rows)

                # Validation & Quarantine
                quarantined_for_source = []
                accepted_for_source = []

                for row in parsed_rows:
                    is_valid, reason, clean_dict = self.validator.validate_single_row(row)
                    if is_valid and clean_dict:
                        accepted_for_source.append(clean_dict)
                    else:
                        quarantined_for_source.append({
                            "raw_record": row.__dict__,
                            "reason": reason,
                            "source_id": s_id,
                            "timestamp": datetime.now().isoformat()
                        })
                        source_stat["reasons"][reason] = source_stat["reasons"].get(reason, 0) + 1

                source_stat["accepted"] = len(accepted_for_source)
                source_stat["quarantined"] = len(quarantined_for_source)
                audit_summary["total_accepted"] += len(accepted_for_source)
                audit_summary["total_quarantined"] += len(quarantined_for_source)

                if quarantined_for_source:
                    self.validator.quarantine_records(quarantined_for_source, batch_id=s_id)

                all_accepted_rows.extend(accepted_for_source)
                source_stat["status"] = "success" if source_stat["fetched"] > 0 else "returned_no_data"

            except PolicyBlockedError as e:
                source_stat["status"] = "blocked_by_policy"
                source_stat["reasons"]["policy"] = str(e)
            except Exception as e:
                source_stat["status"] = "degraded"
                source_stat["reasons"]["execution_error"] = str(e)
                logger.error(f"[{s_id}] Failed during ingestion: {e}", exc_info=True)

            audit_summary["per_source_stats"][s_id] = source_stat

        # Cross-Source Reconciliation and Deduplication
        reconciled_rows, discrepancies = self.validator.cross_source_reconciliation(
            all_accepted_rows, source_priorities
        )
        audit_summary["discrepancies"] = discrepancies

        # Compute mandi stats and sample rows
        if reconciled_rows:
            df_reconciled = pd.DataFrame(reconciled_rows)
            for mandi_name, group in df_reconciled.groupby("mandi"):
                audit_summary["mandi_stats"][mandi_name] = {
                    "count": len(group),
                    "min_date": str(group["date"].min()),
                    "max_date": str(group["date"].max()),
                    "crops": group["crop"].unique().tolist()
                }

            # Select sample rows with raw hash linkage
            sample_candidates = df_reconciled.head(10).to_dict(orient="records")
            audit_summary["sample_rows"] = sample_candidates

        # Update panel.parquet if requested
        if update_panel and reconciled_rows:
            self._update_panel_parquet(reconciled_rows)

        # Generate reports/ingest_daily.md
        self._write_daily_report(audit_summary)

        return audit_summary

    def _update_panel_parquet(self, new_records: List[Dict[str, Any]]):
        """Merges new validated records into panel.parquet idempotently."""
        panel_path = "data/processed/panel.parquet"
        new_df = pd.DataFrame(new_records)

        # Standard panel column schema
        new_df["date"] = pd.to_datetime(new_df["date"])
        new_df["month"] = new_df["date"].dt.month
        new_df["day_of_week"] = new_df["date"].dt.dayofweek
        new_df["day_of_year"] = new_df["date"].dt.dayofyear
        new_df["week_of_year"] = new_df["date"].dt.isocalendar().week.astype(int)
        new_df["data_provenance"] = "real"
        new_df["is_synthetic"] = False
        new_df["was_imputed"] = 0

        if os.path.exists(panel_path):
            existing_df = pd.read_parquet(panel_path)
            existing_df["date"] = pd.to_datetime(existing_df["date"])

            # Merge and deduplicate by (crop, mandi, date) keeping latest fetched
            combined = pd.concat([existing_df, new_df], ignore_index=True)
            if "crop" in combined.columns:
                combined = combined.drop_duplicates(subset=["crop", "mandi", "date"], keep="last")
            else:
                combined = combined.drop_duplicates(subset=["mandi", "date"], keep="last")

            combined = combined.sort_values(["mandi", "date"]).reset_index(drop=True)
            combined.to_parquet(panel_path, index=False)
            logger.info(f"Updated {panel_path}: total rows {len(combined):,} (merged {len(new_df):,} real rows)")
        else:
            new_df.to_parquet(panel_path, index=False)
            logger.info(f"Created new {panel_path} with {len(new_df):,} rows.")

    def _write_daily_report(self, summary: Dict[str, Any]):
        """Writes reports/ingest_daily.md."""
        report_path = "reports/ingest_daily.md"
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        md = f"""# Daily Data Ingestion & Quality Audit Report

**Run Timestamp**: {now_str}  
**Ingestion Window**: {summary['start_date']} to {summary['end_date']} (Last 30 Days up to Today 12 Nov 2026)  
**Total Records Processed**: {summary['total_fetched']:,} | **Accepted**: {summary['total_accepted']:,} | **Quarantined**: {summary['total_quarantined']:,}

---

## 1. Per-Source Ingestion & Policy Execution Status

| Source ID | Name | Type | Status | Fetched | Accepted | Quarantined | Key Reasons / Directives |
|---|---|---|---|---|---|---|---|
"""
        for s_id, stat in summary["per_source_stats"].items():
            reasons_str = "; ".join([f"{k}: {v}" for k, v in stat["reasons"].items()]) if stat["reasons"] else "Clean ingest"
            md += f"| `{s_id}` | {stat['name']} | {stat['type']} | **{stat['status']}** | {stat['fetched']} | {stat['accepted']} | {stat['quarantined']} | {reasons_str[:60]}... |\n"

        md += """
---

## 2. Ingested Data Distribution by Mandi (Last 30 Days)

| Mandi Location | Verified Real Rows | First Trade Date | Last Trade Date | Commodities Observed |
|---|---|---|---|---|
"""
        for mandi, m_stat in summary["mandi_stats"].items():
            crops_str = ", ".join(m_stat["crops"][:4])
            md += f"| **{mandi}** | {m_stat['count']} | {m_stat['min_date']} | {m_stat['max_date']} | {crops_str} |\n"

        md += """
---

## 3. Provenance Linkage: Sample Accepted Rows vs Raw Crawled Files

Every accepted row is tagged with `data_provenance='real'`, `is_synthetic=False`, and linked to its SHA-256 byte payload:

| Crop | Mandi | Date | Modal Price (₹/qtl) | Source | Raw Crawled SHA-256 Hash |
|---|---|---|---|---|---|
"""
        for r in summary["sample_rows"]:
            md += f"| {r['crop'].title()} | {r['mandi']} | {r['date']} | ₹{r['modal_price']:,.2f} | `{r['source_id']}` | `{r['raw_hash'][:20]}...` |\n"

        md += """
---

## 4. Quarantined Records Diagnostic Summary

Quarantined records are isolated byte-for-byte in `data/quarantine/`. No quarantined row is ever allowed to enter `data/processed/panel.parquet` or training pipelines.

- **Plausibility Violations**: Rows where $P_{\\min} > P_{\\text{modal}}$ or $P_{\\text{modal}} > P_{\\max}$ are routed to quarantine.
- **Out of Bounds**: Extreme values outside biological and historical price boundaries are blocked.
- **Unknown Units**: Any non-standard unit that cannot be converted to Rs/quintal is quarantined without silent estimation.
"""
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(md)

        logger.info(f"Daily ingest report written to {report_path}")
