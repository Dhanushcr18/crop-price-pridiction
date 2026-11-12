"""Area reports repository and official area statistics loader.

Manages farmer-reported acreage with device hashing, anomaly flagging,
and official agricultural statistics loading from NHB / DES.
"""

import os
import sqlite3
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
import pandas as pd
import yaml

from src.data.units import acres_to_hectares, hectares_to_acres


class AreaRepository:
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        area_cfg = self.config.get("area_outlook", {})
        self.db_path = area_cfg.get("db_path", "data/area_reports.db")
        self.official_data_path = area_cfg.get(
            "official_data_path", "data/raw/official_crop_area/onion_area_production.csv"
        )
        self.max_acres = float(area_cfg.get("max_single_entry_acres", 500.0))
        self.min_entries_threshold = int(area_cfg.get("min_farmer_entries_threshold", 30))
        self.min_coverage_pct_threshold = float(area_cfg.get("min_coverage_pct_threshold", 5.0))
        self.known_districts = area_cfg.get("known_districts", [])
        self.known_seasons = area_cfg.get("known_seasons", ["Kharif", "Late Kharif", "Rabi", "Total"])
        
        # Ensure DB directory exists and schema is initialized
        os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize SQLite table for farmer area reports with unique constraint for upsert."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS farmer_area_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    district TEXT NOT NULL,
                    season TEXT NOT NULL,
                    year TEXT NOT NULL,
                    acres REAL NOT NULL,
                    device_id_hash TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    is_anomaly INTEGER DEFAULT 0,
                    anomaly_reason TEXT,
                    UNIQUE(device_id_hash, district, season, year)
                )
            """)
            conn.commit()

    @staticmethod
    def hash_device_id(device_id: str) -> str:
        """Hash device_id using SHA-256 to protect privacy."""
        if not device_id:
            device_id = "unknown_device"
        return hashlib.sha256(device_id.encode("utf-8")).hexdigest()

    def submit_report(
        self,
        district: str,
        season: str,
        year: str,
        acres: float,
        device_id: str
    ) -> Dict[str, Any]:
        """Validate, check anomalies, and upsert a farmer area report.
        
        Hard rules:
        - acres > 0 and <= max_acres (500)
        - known district
        - one entry per device per district per season (updates if existing)
        - no personal data stored; device_id is hashed
        """
        # 1. Validation
        if acres <= 0:
            raise ValueError(f"Acres must be greater than zero, got {acres}")
        if acres > self.max_acres:
            raise ValueError(
                f"Reported area ({acres:.1f} acres) exceeds the single-holding limit of {self.max_acres:.0f} acres. "
                f"Please verify your land size."
            )

        # Normalize district
        matched_district = None
        for kd in self.known_districts:
            if kd.lower() == district.strip().lower():
                matched_district = kd
                break
        if not matched_district:
            raise ValueError(
                f"Unknown district '{district}'. Valid Karnataka districts include: {', '.join(self.known_districts[:6])}..."
            )

        # Normalize season
        matched_season = None
        for ks in self.known_seasons:
            if ks.lower() == season.strip().lower():
                matched_season = ks
                break
        matched_season = matched_season or season.strip()

        device_hash = self.hash_device_id(device_id)
        now = datetime.utcnow().isoformat()

        # 2. Anomaly Checks
        is_anomaly = 0
        anomaly_reasons = []

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Check frequency from this device (e.g. > 15 submissions in total)
            cursor.execute(
                "SELECT COUNT(*) FROM farmer_area_reports WHERE device_id_hash = ?",
                (device_hash,)
            )
            device_reports_count = cursor.fetchone()[0]
            if device_reports_count >= 10:
                is_anomaly = 1
                anomaly_reasons.append("High report frequency from single device")

            # Check if updating an existing record
            cursor.execute(
                "SELECT id, acres FROM farmer_area_reports WHERE device_id_hash = ? AND district = ? AND season = ? AND year = ?",
                (device_hash, matched_district, matched_season, str(year))
            )
            existing = cursor.fetchone()

            if existing:
                record_id, prev_acres = existing
                if abs(acres - prev_acres) > 200:
                    is_anomaly = 1
                    anomaly_reasons.append(f"Drastic acreage change ({prev_acres} -> {acres})")

                cursor.execute("""
                    UPDATE farmer_area_reports
                    SET acres = ?, updated_at = ?, is_anomaly = ?, anomaly_reason = ?
                    WHERE id = ?
                """, (acres, now, is_anomaly, "; ".join(anomaly_reasons) if anomaly_reasons else None, record_id))
                action = "updated"
            else:
                cursor.execute("""
                    INSERT INTO farmer_area_reports (
                        district, season, year, acres, device_id_hash, created_at, updated_at, is_anomaly, anomaly_reason
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    matched_district, matched_season, str(year), acres, device_hash, now, now,
                    is_anomaly, "; ".join(anomaly_reasons) if anomaly_reasons else None
                ))
                record_id = cursor.lastrowid
                action = "created"

            conn.commit()

        return {
            "status": "success",
            "action": action,
            "record_id": record_id,
            "district": matched_district,
            "season": matched_season,
            "year": str(year),
            "reported_acres": acres,
            "reported_hectares": round(acres_to_hectares(acres), 2),
            "is_anomaly": bool(is_anomaly),
            "timestamp": now
        }

    def get_farmer_reports_summary(
        self, district: str, season: str, year: str
    ) -> Dict[str, Any]:
        """Aggregate farmer-reported acreage for a district, season, and year."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*), COALESCE(SUM(acres), 0.0)
                FROM farmer_area_reports
                WHERE LOWER(district) = LOWER(?) AND LOWER(season) = LOWER(?) AND year = ?
                  AND is_anomaly = 0
            """, (district, season, str(year)))
            count, total_acres = cursor.fetchone()

        return {
            "district": district,
            "season": season,
            "year": str(year),
            "entry_count": int(count),
            "total_reported_acres": float(total_acres),
            "total_reported_hectares": round(acres_to_hectares(total_acres), 2)
        }

    def get_officer_review_data(self, district: str = "Mysuru", limit: int = 20) -> Dict[str, Any]:
        """Fetch anonymized farmer submissions and statistics for FPO officer review."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*), COALESCE(SUM(acres), 0.0)
                FROM farmer_area_reports
                WHERE is_anomaly = 0
            """)
            valid_count, valid_acres = cursor.fetchone()

            cursor.execute("""
                SELECT COUNT(*)
                FROM farmer_area_reports
                WHERE is_anomaly = 1
            """)
            anomaly_count = cursor.fetchone()[0]

            cursor.execute("""
                SELECT device_id_hash, acres, district, season, year, is_anomaly, anomaly_reason, created_at
                FROM farmer_area_reports
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()

        submissions = []
        for r in rows:
            dev_hash = str(r[0])
            acres_val = float(r[1])
            hectares_val = round(acres_to_hectares(acres_val), 2)
            masked_hash = f"{dev_hash[:4]}...{dev_hash[-4:]}" if len(dev_hash) >= 8 else dev_hash
            submissions.append({
                "device_hash": masked_hash,
                "acres": acres_val,
                "hectares": hectares_val,
                "district": str(r[2]),
                "season": str(r[3]),
                "year": str(r[4]),
                "is_anomaly": bool(r[5]),
                "anomaly_reason": str(r[6]) if r[6] else None,
                "created_at": str(r[7])
            })

        return {
            "total_valid_submissions": int(valid_count),
            "total_reported_acres": float(valid_acres),
            "flagged_anomalies": int(anomaly_count),
            "submissions": submissions
        }

    def load_official_dataset(self) -> pd.DataFrame:
        """Load official NHB/DES onion statistics with provenance check."""
        if not os.path.exists(self.official_data_path):
            raise FileNotFoundError(f"Official area dataset not found at {self.official_data_path}")

        df = pd.read_csv(self.official_data_path)
        # Verify provenance
        if "data_provenance" in df.columns:
            non_real = df[df["data_provenance"] != "real"]
            if len(non_real) > 0 and not self.config.get("allow_synthetic_training", False):
                raise ValueError("Official area dataset contains non-real rows!")

        return df

    def get_official_area_metrics(
        self, region_name: str, level: str, season: str, year: str
    ) -> Optional[Dict[str, Any]]:
        """Look up official area/production for a specific region, season, and year.
        
        Calculates 5-year baseline average and comparisons.
        """
        df = self.load_official_dataset()
        
        # Filter matching region and level
        mask_region = (df["level"] == level) & (df["region_name"].str.lower() == region_name.lower())
        reg_df = df[mask_region]

        if reg_df.empty:
            return None

        # Try specific season, fallback to Total if season-specific not present
        season_match = reg_df[reg_df["season"].str.lower() == season.lower()]
        target_df = season_match if not season_match.empty else reg_df[reg_df["season"] == "Total"]

        # Exact year record
        year_row = target_df[target_df["year"] == year]
        if year_row.empty:
            # Try latest available year in target_df
            if target_df.empty:
                return None
            year_row = target_df.sort_values(by="year", ascending=False).iloc[0:1]
            actual_year_used = year_row["year"].values[0]
        else:
            actual_year_used = year

        current = year_row.iloc[0]
        curr_ha = float(current["area_hectares"])
        curr_acres = hectares_to_acres(curr_ha)
        curr_prod = float(current["production_tonnes"])
        curr_yield = float(current["yield_tonnes_per_ha"])

        # 5-year history for baseline
        hist_rows = target_df[target_df["year"] != actual_year_used].tail(5)
        if len(hist_rows) > 0:
            avg_5yr_ha = float(hist_rows["area_hectares"].mean())
            avg_5yr_prod = float(hist_rows["production_tonnes"].mean())
        else:
            avg_5yr_ha = curr_ha
            avg_5yr_prod = curr_prod

        avg_5yr_acres = hectares_to_acres(avg_5yr_ha)

        # Supply signal ratio vs 5-year average
        area_ratio = curr_ha / avg_5yr_ha if avg_5yr_ha > 0 else 1.0
        prod_ratio = curr_prod / avg_5yr_prod if avg_5yr_prod > 0 else 1.0

        higher_thresh = self.config.get("area_outlook", {}).get("supply_signal_thresholds", {}).get("higher_ratio", 1.05)
        lower_thresh = self.config.get("area_outlook", {}).get("supply_signal_thresholds", {}).get("lower_ratio", 0.95)

        if prod_ratio >= higher_thresh:
            signal_category = "higher"
        elif prod_ratio <= lower_thresh:
            signal_category = "lower"
        else:
            signal_category = "normal"

        # 5-year historical series for charts
        history_series = []
        for _, r in target_df.tail(5).iterrows():
            history_series.append({
                "year": str(r["year"]),
                "season": str(r["season"]),
                "area_hectares": float(r["area_hectares"]),
                "area_acres": round(hectares_to_acres(float(r["area_hectares"])), 0),
                "production_tonnes": float(r["production_tonnes"]),
                "is_current": str(r["year"]) == actual_year_used
            })

        return {
            "level": level,
            "region_name": current["region_name"],
            "year": str(actual_year_used),
            "season": str(current["season"]),
            "area_hectares": round(curr_ha, 1),
            "area_acres": round(curr_acres, 0),
            "production_tonnes": round(curr_prod, 1),
            "yield_tonnes_per_ha": round(curr_yield, 2),
            "avg_5yr_hectares": round(avg_5yr_ha, 1),
            "avg_5yr_acres": round(avg_5yr_acres, 0),
            "area_ratio_vs_5yr": round(area_ratio, 3),
            "prod_ratio_vs_5yr": round(prod_ratio, 3),
            "signal_category": signal_category,
            "source_name": str(current["source_name"]),
            "publication_date": str(current["publication_date"]),
            "is_official": True,
            "history": history_series
        }

    def get_complete_area_summary(
        self, district: str, season: str, year: str
    ) -> Dict[str, Any]:
        """Aggregate farmer reports and official district, state, and country statistics.
        
        Enforces:
        - Farmer-entered acreage NEVER extrapolated to state/country.
        - If district data missing (e.g. Mysuru), label 'Not available' and fallback to state.
        - Coverage ratio = reported / official district area.
        - If coverage < 5% or N < 30, flag 'too_few_reports' = True.
        """
        # 1. Farmer reports in district
        farmer_summary = self.get_farmer_reports_summary(district, season, year)
        n_farmers = farmer_summary["entry_count"]
        reported_acres = farmer_summary["total_reported_acres"]
        reported_hectares = farmer_summary["total_reported_hectares"]

        # 2. Official District Area
        official_district = self.get_official_area_metrics(district, "district", season, year)

        # 3. Official State Area (Karnataka)
        official_state = self.get_official_area_metrics("Karnataka", "state", season, year)

        # 4. Official National Area (India)
        official_country = self.get_official_area_metrics("India", "country", season, year)

        # 5. Coverage calculation
        if official_district and official_district["area_acres"] > 0:
            coverage_pct = round((reported_acres / official_district["area_acres"]) * 100.0, 3)
            district_official_available = True
        else:
            coverage_pct = None
            district_official_available = False

        # Coverage / Sample Size Rule: below 5% or N < 30 => Too few reports to trust
        too_few_reports = (
            n_farmers < self.min_entries_threshold
            or (coverage_pct is not None and coverage_pct < self.min_coverage_pct_threshold)
            or (coverage_pct is None and n_farmers < self.min_entries_threshold)
        )

        return {
            "district": district,
            "season": season,
            "year": str(year),
            "farmer_reported": {
                "reported_acres": reported_acres,
                "reported_hectares": reported_hectares,
                "entry_count": n_farmers,
                "coverage_pct": coverage_pct,
                "too_few_reports": too_few_reports,
                "warning_message": (
                    f"Too few reports to trust ({n_farmers} entries, {coverage_pct or 0:.1f}% coverage; "
                    f"minimum {self.min_entries_threshold} reports and {self.min_coverage_pct_threshold:.0f}% coverage required)."
                    if too_few_reports else None
                )
            },
            "district_official": official_district,
            "district_official_available": district_official_available,
            "state_official": official_state,
            "country_official": official_country,
            "sowing_to_harvest_lag_days": self.config.get("area_outlook", {}).get("sowing_to_harvest_lag_days", 105),
            "assumptions": [
                {
                    "item": "Unit Conversion",
                    "value": "1 Hectare = 2.47105 Acres",
                    "status": "Standard international physical constant"
                },
                {
                    "item": "Sowing-to-Harvest Gap",
                    "value": f"{self.config.get('area_outlook', {}).get('sowing_to_harvest_lag_days', 105)} days (~3.5 months)",
                    "status": "Config Assumption"
                },
                {
                    "item": "Acreage Extrapolation Restriction",
                    "value": "Farmer reports are strictly isolated and never extrapolated to state or national totals.",
                    "status": "Hard Rule"
                }
            ]
        }

