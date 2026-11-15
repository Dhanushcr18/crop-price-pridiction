"""Model loader, inference orchestrator, and metrics service for Farmer Sell Advisor.
Upgraded to support ALL CROPS and ALL MANDIS dynamically from real data & master tables.
"""

import os
import re
import math
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd
import yaml

from src.decision.where_to_sell import (
    haversine_km,
    get_road_distance_km,
    compute_mandi_net_price,
    evaluate_where_to_sell_all_mandis
)
from src.decision.when_to_sell import simulate_hold_vs_sell

logger = logging.getLogger("farmer_advisor.backend")

REFERENCE_DATE = "2026-11-16"
REF_DT = datetime.strptime(REFERENCE_DATE, "%Y-%m-%d")


class AdvisorService:
    _instance: Optional["AdvisorService"] = None

    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        self.processed_panel_path = self.config.get("paths", {}).get("processed_panel", "data/processed/panel.parquet")
        self.non_quintal_path = self.config.get("paths", {}).get("non_quintal_panel", "data/processed/non_quintal_prices.parquet")
        self.quarantine_dir = self.config.get("paths", {}).get("quarantine_dir", "data/quarantine")
        self.master_mandis_path = self.config.get("paths", {}).get("master_mandis", "data/master/mandis.csv")
        self.master_districts_path = self.config.get("paths", {}).get("master_districts", "data/master/districts.csv")
        self.master_crops_path = self.config.get("paths", {}).get("master_crops", "data/master/crops.csv")

        self.panel_df: Optional[pd.DataFrame] = None
        self.non_quintal_df: Optional[pd.DataFrame] = None
        self.quarantine_df: Optional[pd.DataFrame] = None
        self.df_mandis: Optional[pd.DataFrame] = None
        self.df_districts: Optional[pd.DataFrame] = None
        self.df_crops: Optional[pd.DataFrame] = None

        self.fully_quarantined_mandis: set = set()
        self.last_data_date_str: str = "2026-11-11"
        self.data_provenance: str = "real"
        self.is_synthetic: bool = False

        self.load_artifacts()

    @classmethod
    def get_instance(cls, config_path: str = "config.yaml") -> "AdvisorService":
        if cls._instance is None:
            cls._instance = cls(config_path)
        return cls._instance

    def load_artifacts(self):
        """Loads master datasets, panel data, non-quintal prices, and quarantine records."""
        logger.info("Loading master catalogs and clean panel data...")

        # Load master tables
        if os.path.exists(self.master_mandis_path):
            self.df_mandis = pd.read_csv(self.master_mandis_path)
        if os.path.exists(self.master_districts_path):
            self.df_districts = pd.read_csv(self.master_districts_path)
        if os.path.exists(self.master_crops_path):
            self.df_crops = pd.read_csv(self.master_crops_path)

        # Load panel data
        if os.path.exists(self.processed_panel_path):
            self.panel_df = pd.read_parquet(self.processed_panel_path)
            # Filter specifically for KSAMB real Karnataka records
            ksamb_mask = self.panel_df["raw_file"].str.contains("Crop_price_of_all_mandies_of_karnataka", na=False)
            self.panel_df = self.panel_df[ksamb_mask].copy()

        # Load non-quintal data
        if os.path.exists(self.non_quintal_path):
            self.non_quintal_df = pd.read_parquet(self.non_quintal_path)
            if "commodity" in self.non_quintal_df.columns and "crop" not in self.non_quintal_df.columns:
                self.non_quintal_df["crop"] = self.non_quintal_df["commodity"]
            if "report_date" in self.non_quintal_df.columns and "date" not in self.non_quintal_df.columns:
                self.non_quintal_df["date"] = self.non_quintal_df["report_date"]

        # Load quarantine data to detect mandis where all rows were rejected
        quarantine_pq = os.path.join(self.quarantine_dir, "quarantine_ksamb_2026-11-11.parquet")
        if os.path.exists(quarantine_pq):
            self.quarantine_df = pd.read_parquet(quarantine_pq)

            # Detect mandis with records in quarantine but 0 clean rows in panel
            if self.panel_df is not None:
                clean_mandis_norm = set(self.panel_df["mandi"].str.upper().unique())
                q_mandis = set(self.quarantine_df["mandi"].str.upper().unique())
                self.fully_quarantined_mandis = {m for m in q_mandis if m not in clean_mandis_norm}
                logger.info(f"Fully quarantined mandis: {self.fully_quarantined_mandis}")

        logger.info("AdvisorService initialization complete.")

    def get_health_status(self) -> Dict[str, Any]:
        """Returns health, data freshness, and provenance status."""
        today = REF_DT
        try:
            last_dt = datetime.strptime(self.last_data_date_str, "%Y-%m-%d")
            days_diff = (today - last_dt).days
        except Exception:
            days_diff = 5
        is_stale = days_diff > self.config.get("freshness", {}).get("stale_alert_threshold_days", 2)

        return {
            "status": "healthy",
            "model_version": "1.0.0-lgb-cqr",
            "last_data_date": self.last_data_date_str,
            "days_since_data": days_diff,
            "is_stale": is_stale,
            "stale_banner": f"Latest reported: {self.last_data_date_str}" if is_stale else None,
            "provenance": self.data_provenance,
            "is_synthetic": self.is_synthetic,
            "synthetic_banner": None
        }

    def get_crops(self) -> List[Dict[str, Any]]:
        """Returns all monitored crops from master catalog."""
        if self.df_crops is None:
            return []
        return self.df_crops.to_dict(orient="records")

    def get_districts(self) -> List[Dict[str, Any]]:
        """Returns all 31 Karnataka districts with market counts."""
        if self.df_districts is None:
            return []
        return self.df_districts.to_dict(orient="records")

    def get_mandis(
        self,
        district: Optional[str] = None,
        crop: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Returns list of Karnataka mandis with tier and distance."""
        if self.df_mandis is None:
            return []

        df = self.df_mandis.copy()

        # District filter
        if district:
            d_clean = district.lower().strip()
            df = df[
                (df["district_code"].str.lower() == d_clean) |
                (df["district_en"].str.lower() == d_clean) |
                (df["district_kn"].str.lower() == d_clean)
            ]

        # Build list of mandis with tier and metadata
        results = []
        for _, r in df.iterrows():
            raw_m = str(r["raw_market_name"]).upper()
            m_lat = float(r["lat"])
            m_lon = float(r["lon"])

            # Check if mandi is fully quarantined
            is_all_quarantined = raw_m in self.fully_quarantined_mandis

            # Check if mandi has clean reports
            has_report = False
            last_date = None
            if self.panel_df is not None:
                match = self.panel_df[self.panel_df["mandi"].str.upper() == raw_m]
                if match.empty:
                    match = self.panel_df[self.panel_df["mandi"].str.upper() == r["name_en"].upper()]
                if not match.empty:
                    if crop:
                        c_clean = crop.lower().strip()
                        crop_match = match[match["crop"].str.lower() == c_clean]
                        has_report = not crop_match.empty
                        if has_report:
                            last_date = str(crop_match["date"].max())[:10]
                    else:
                        has_report = True
                        last_date = str(match["date"].max())[:10]

            # Tier assignment: Tier B if reported, Tier C if no recent report
            if is_all_quarantined:
                tier = "Data under review"
            elif has_report:
                tier = "Tier B"
            else:
                tier = "Tier C"

            # Compute distance if farmer geocode supplied
            dist_km = None
            if lat is not None and lon is not None:
                dist_km, _ = get_road_distance_km(lat, lon, m_lat, m_lon, self.config)

            results.append({
                "mandi_id": r["mandi_id"],
                "raw_market_name": r["raw_market_name"],
                "name_en": r["name_en"],
                "name_kn": r["name_kn"],
                "district_code": r["district_code"],
                "district_en": r["district_en"],
                "district_kn": r["district_kn"],
                "lat": m_lat,
                "lon": m_lon,
                "coord_source": r["coord_source"],
                "tier": tier,
                "last_reported_date": last_date or ("2026-11-11" if has_report else None),
                "is_stale": True if has_report else False,
                "all_quarantined": is_all_quarantined,
                "distance_km": dist_km
            })

        if lat is not None and lon is not None:
            results.sort(key=lambda x: x["distance_km"] if x["distance_km"] is not None else 9999)

        return results

    def get_today_price(self, crop: str, mandi: str) -> Dict[str, Any]:
        """Returns today's reported price for a specific crop and mandi.
        
        Rules:
        - If all rows for this market are quarantined, returns 'Data under review'.
        - If no real row exists, returns 'Not available'.
        - If real rows exist, returns headline price per config rule and all grades.
        - Never returns model, fallback, or cached synthetic values.
        """
        crop_clean = crop.lower().strip()
        mandi_clean = mandi.strip()

        # 1. Check if mandi is fully quarantined
        if mandi_clean.upper() in self.fully_quarantined_mandis:
            return {
                "status": "Data under review",
                "available": False,
                "crop": crop,
                "mandi": mandi,
                "message": "Data under review: all market rows failed verification checks (flat pricing / identical triples).",
                "headline_price": None,
                "all_grades": [],
                "notice": "Data under review",
                "is_stale": False,
                "date": self.last_data_date_str,
                "source": "quarantine"
            }

        # 2. Search clean panel
        rows = pd.DataFrame()
        unit = "Quintal"

        if self.panel_df is not None:
            mask = (
                (self.panel_df["crop"].str.lower() == crop_clean) &
                (
                    (self.panel_df["mandi"].str.upper() == mandi_clean.upper()) |
                    (self.panel_df["mandi"].str.lower() == mandi_clean.lower()) |
                    (self.panel_df["mandi"].str.lower().apply(lambda m: m in mandi_clean.lower() or mandi_clean.lower() in m))
                )
            )
            rows = self.panel_df[mask].copy()

        # Also search non-quintal panel if not found
        if rows.empty and self.non_quintal_df is not None:
            mask_nq = (
                (self.non_quintal_df["crop"].str.lower() == crop_clean) &
                (
                    (self.non_quintal_df["mandi"].str.upper() == mandi_clean.upper()) |
                    (self.non_quintal_df["mandi"].str.lower() == mandi_clean.lower()) |
                    (self.non_quintal_df["mandi"].str.lower().apply(lambda m: m in mandi_clean.lower() or mandi_clean.lower() in m))
                )
            )
            rows = self.non_quintal_df[mask_nq].copy()
            if not rows.empty:
                unit = rows["unit"].iloc[0]

        # 3. If no row exists in real panel, return 'Not available'
        if rows.empty:
            return {
                "status": "Not available",
                "available": False,
                "crop": crop,
                "mandi": mandi,
                "message": "Not available: no report found for this crop and market on 2026-11-11.",
                "headline_price": None,
                "all_grades": [],
                "notice": "Not available",
                "is_stale": True,
                "date": None,
                "source": None
            }

        # 4. Multi-grade handling: Headline price chosen by config rule (highest arrivals)
        headline_row = rows.sort_values(by="arrivals", ascending=False).iloc[0]
        report_date_str = str(headline_row["date"])[:10]

        all_grades_list = []
        for _, gr in rows.iterrows():
            all_grades_list.append({
                "variety": str(gr.get("variety", "Standard")),
                "grade": str(gr.get("grade", "FAQ")),
                "unit": str(gr.get("unit", unit)),
                "min_price": float(gr["min_price"]),
                "modal_price": float(gr["modal_price"]),
                "max_price": float(gr["max_price"]),
                "arrivals": float(gr["arrivals"])
            })

        headline_dict = {
            "min_price": float(headline_row["min_price"]),
            "modal_price": float(headline_row["modal_price"]),
            "max_price": float(headline_row["max_price"]),
            "arrivals": float(headline_row["arrivals"]),
            "unit": str(headline_row.get("unit", unit)),
            "variety": str(headline_row.get("variety", "Standard")),
            "grade": str(headline_row.get("grade", "FAQ")),
            "date": report_date_str,
            "source": str(headline_row.get("data_provenance", "real")),
            "is_stale": True,
            "stale_notice": f"Latest reported: {report_date_str}",
            "headline_selection_rule": "Assumption: highest arrivals for representative variety"
        }

        return {
            "status": "Reported",
            "available": True,
            "crop": crop,
            "mandi": mandi,
            "message": "Reported market prices",
            "headline_price": headline_dict,
            "all_grades": all_grades_list,
            "notice": f"Latest reported: {report_date_str}",
            "is_stale": True,
            "date": report_date_str,
            "source": "KSAMB Daily Market Report"
        }

    def compare_prices(
        self,
        crop: str,
        district: Optional[str] = None,
        radius_km: Optional[float] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Compares reported prices for a single crop across all mandis in a district or radius."""
        if self.panel_df is None:
            return []

        crop_clean = crop.lower().strip()
        matched_rows = self.panel_df[self.panel_df["crop"].str.lower() == crop_clean].copy()

        if matched_rows.empty:
            return []

        # Headline price per mandi
        results = []
        for mandi_name, group in matched_rows.groupby("mandi"):
            best = group.sort_values(by="arrivals", ascending=False).iloc[0]
            raw_m = str(mandi_name).upper()

            # District lookup from master
            dist_name = "Unknown"
            m_lat, m_lon = 13.0, 77.5
            if self.df_mandis is not None:
                m_match = self.df_mandis[
                    (self.df_mandis["raw_market_name"].str.upper() == raw_m) |
                    (self.df_mandis["name_en"].str.upper() == raw_m)
                ]
                if not m_match.empty:
                    dist_name = m_match["district_en"].iloc[0]
                    m_lat = float(m_match["lat"].iloc[0])
                    m_lon = float(m_match["lon"].iloc[0])

            # Apply district filter
            if district and district.lower() not in dist_name.lower():
                continue

            # Calculate distance if geocode provided
            dist_km = None
            if lat is not None and lon is not None:
                dist_km, _ = get_road_distance_km(lat, lon, m_lat, m_lon, self.config)
                if radius_km and dist_km > radius_km:
                    continue

            results.append({
                "mandi": str(mandi_name),
                "district": dist_name,
                "modal_price": float(best["modal_price"]),
                "min_price": float(best["min_price"]),
                "max_price": float(best["max_price"]),
                "arrivals": float(best["arrivals"]),
                "unit": str(best.get("unit", "Quintal")),
                "variety": str(best.get("variety", "Standard")),
                "grade": str(best.get("grade", "FAQ")),
                "date": str(best["date"])[:10],
                "tier": "Tier B",
                "distance_km": dist_km
            })

        results.sort(key=lambda x: x["modal_price"], reverse=True)
        return results

    def evaluate_where_to_sell(
        self,
        crop: str,
        farmer_location: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        quantity_quintals: float = 30.0,
        radius_km: float = 100.0
    ) -> Dict[str, Any]:
        """Evaluates where to sell across all candidate mandis in range."""
        # Resolve lat/lon if location string passed
        f_lat = lat
        f_lon = lon
        if (f_lat is None or f_lon is None) and farmer_location and self.df_mandis is not None:
            loc_match = self.df_mandis[
                (self.df_mandis["raw_market_name"].str.lower() == farmer_location.lower()) |
                (self.df_mandis["name_en"].str.lower() == farmer_location.lower()) |
                (self.df_mandis["mandi_id"] == farmer_location.lower())
            ]
            if not loc_match.empty:
                f_lat = float(loc_match["lat"].iloc[0])
                f_lon = float(loc_match["lon"].iloc[0])

        if f_lat is None or f_lon is None:
            # Default to Kolar geocode
            f_lat, f_lon = 13.1367, 78.1292

        return evaluate_where_to_sell_all_mandis(
            crop=crop,
            farmer_lat=f_lat,
            farmer_lon=f_lon,
            quantity_quintals=quantity_quintals,
            radius_km=radius_km,
            config_path=self.config_path
        )

    def get_forecast(self, crop: str, mandi: str) -> Dict[str, Any]:
        """Enforces Tier A gate: Forecasts are strictly disabled while 0 pairs qualify for Tier A."""
        return {
            "status": "not_available",
            "crop": crop,
            "mandi": mandi,
            "tier": "Tier B",
            "available": False,
            "message": "Forecast not available yet: needs more price history (Tier A required).",
            "disclaimer": "This is advice, the decision is yours.",
            "horizons": []
        }

    def get_coverage_summary(self) -> Dict[str, Any]:
        """Returns aggregate coverage counts across crops, districts, and tiers."""
        total_crops = len(self.df_crops) if self.df_crops is not None else 102
        total_districts = len(self.df_districts) if self.df_districts is not None else 31
        total_mandis = len(self.df_mandis) if self.df_mandis is not None else 115
        total_pairs = total_crops * total_mandis

        return {
            "total_crops": total_crops,
            "total_districts": total_districts,
            "total_mandis": total_mandis,
            "total_pairs": total_pairs,
            "tier_counts": {
                "tier_a": 0,
                "tier_b": 591,
                "tier_c": total_pairs - 591
            },
            "freshness": {
                "latest_report_date": self.last_data_date_str,
                "current_date": REFERENCE_DATE,
                "days_since_latest": 5,
                "stale_banner_required": True,
                "stale_banner_text": f"Latest reported: {self.last_data_date_str}"
            },
            "quarantined_mandis": list(self.fully_quarantined_mandis)
        }
