"""Validation, cross-source reconciliation, and quarantine routing for ingested agricultural data."""

import os
import json
import logging
from datetime import datetime, date
from dataclasses import asdict
from typing import List, Dict, Any, Tuple, Optional
import pandas as pd
import numpy as np

from src.ingest.base import ParsedRow
from src.data.units import normalize_price_to_quintal, normalize_arrival_to_quintal, UnknownUnitError

logger = logging.getLogger("farmer_advisor.ingest.validate")

# Default crop price bounds (Rs / Quintal) based on historical AGMARKNET/NHB bands
DEFAULT_CROP_BOUNDS = {
    "onion": (200.0, 15000.0),
    "potato": (200.0, 10000.0),
    "tomato": (150.0, 18000.0),
}

# Comprehensive manual overrides for commodity price bounds (Rs / Quintal)
# High-value cash crops, spices, dry fruits, and commercial crops
MANUAL_CROP_BOUNDS = {
    # Spices & Dry Fruits
    "black_pepper": (5000.0, 150000.0),
    "pepper_garbled": (5000.0, 150000.0),
    "cardamom": (10000.0, 350000.0),
    "walnut": (8000.0, 180000.0),
    "almond(badam)": (10000.0, 200000.0),
    "cashewnuts": (10000.0, 160000.0),
    "cinamon(dalchini)": (5000.0, 120000.0),
    "cummin_seed(jeera)": (5000.0, 80000.0),
    "poppy_seeds": (10000.0, 250000.0),
    "nigella": (5000.0, 60000.0),
    "nigella_seeds": (5000.0, 60000.0),
    "soanf": (3000.0, 50000.0),
    "dry_chillies": (3000.0, 65000.0),
    "chili_red": (3000.0, 65000.0),
    "garlic": (500.0, 45000.0),
    
    # Commercial & Plantation Crops
    "copra": (3000.0, 50000.0),
    "coconut_oil": (5000.0, 60000.0),
    "arecanut(betelnut/supari)": (8000.0, 95000.0),
    "betelnuts": (8000.0, 95000.0),
    "rubber": (4000.0, 45000.0),
    "ghee": (10000.0, 100000.0),
    
    # Flowers & Exotic Horticulture
    "jasmine": (1000.0, 60000.0),
    "kakada": (1000.0, 50000.0),
    "rose(local)": (1000.0, 40000.0),
    "tube_flower": (1000.0, 40000.0),
    "marigold(calcutta)": (500.0, 25000.0),
    "lotus": (500.0, 30000.0),
    "astera": (500.0, 25000.0),
    "tulip": (1000.0, 50000.0),
    "jarbara": (1000.0, 50000.0),
    "raibel": (1000.0, 50000.0),
    "mushroom": (2000.0, 75000.0),

    # Standard Field Vegetables
    "onion": (150.0, 15000.0),
    "onion_green": (150.0, 15000.0),
    "potato": (150.0, 12000.0),
    "tomato": (100.0, 18000.0),
    "green_chilli": (300.0, 35000.0),
    "brinjal": (150.0, 12000.0),
    "cabbage": (100.0, 10000.0),
    "cauliflower": (100.0, 12000.0),
    "spinach": (100.0, 12000.0),
    "mint(pudina)": (200.0, 15000.0),
    "coriander(leaves)": (200.0, 25000.0),
    "methi(leaves)": (200.0, 15000.0),
    "amaranthus": (100.0, 12000.0),
    "raddish": (100.0, 10000.0),
    "carrot": (150.0, 15000.0),
    "ashgourd": (100.0, 10000.0),
    "bottle_gourd": (100.0, 10000.0),
    "ridgeguard(tori)": (150.0, 12000.0),
    "tinda": (150.0, 12000.0),
    "wild_cucumber": (100.0, 10000.0),
    "green_peas": (500.0, 25000.0),
    "lemon": (300.0, 20000.0),
    
    # Fruits
    "banana": (200.0, 15000.0),
    "apple": (1000.0, 40000.0),
    "pomegranate": (1000.0, 45000.0),
    
    # Cereals, Pulses & Oilseeds
    "ragi": (800.0, 9000.0),
    "paddy": (1000.0, 8000.0),
    "paddy(common)": (800.0, 8000.0),
    "rice": (1000.0, 12000.0),
    "wheat": (1000.0, 7000.0),
    "maize": (800.0, 6000.0),
    "jowar": (800.0, 7000.0),
    "bengal_gram": (1500.0, 16000.0),
    "red_gram": (2000.0, 20000.0),
    "cotton": (2000.0, 18000.0),
    "groundnut": (1500.0, 15000.0),
    "jowar(sorghum)": (800.0, 7000.0),
    "bajra(pearl_millet/cumbu)": (800.0, 6000.0),
    "bengal_gram(gram)(whole)": (1500.0, 16000.0),
    "red_gram/arhar/tur(whole)": (2000.0, 20000.0),
    "green_gram(moong)(whole)": (2000.0, 20000.0),
    "black_gram(urd_beans)(whole)": (2000.0, 20000.0),
    "groundnut": (1500.0, 18000.0),
    "soyabean": (1500.0, 14000.0),
    "cotton": (2000.0, 20000.0),
    "sunflower/sunflower_seed": (1500.0, 16000.0),
    "sesamum(sesame,gingelly,til)": (3000.0, 30000.0),
    "mustard": (1500.0, 16000.0),
    
    # Livestock
    "cow": (5000.0, 150000.0),
    "she_buffalo": (5000.0, 150000.0),
    "fish": (1000.0, 50000.0),
    
    # Default broad band for unlisted commodities
    "default": (50.0, 100000.0)
}


class ValidationEngine:
    """Validates raw parsed rows, enforces bounds, cross-source checks, and routes invalid records to quarantine."""

    def __init__(
        self,
        quarantine_dir: str = "data/quarantine",
        today_date_str: str = "2026-11-12",
        crop_bounds: Optional[Dict[str, Tuple[float, float]]] = None
    ):
        self.quarantine_dir = quarantine_dir
        self.today = datetime.strptime(today_date_str, "%Y-%m-%d").date()
        self.crop_bounds = crop_bounds or DEFAULT_CROP_BOUNDS
        self.crop_bounds = crop_bounds or MANUAL_CROP_BOUNDS
        os.makedirs(self.quarantine_dir, exist_ok=True)

    def get_bounds_for_crop(self, crop_name: str) -> Tuple[float, float]:
        """Resolves plausible price bounds using manual overrides or broad default."""
        clean = str(crop_name).lower().strip().replace(" ", "_")
        if clean in self.crop_bounds:
            return self.crop_bounds[clean]
        for k, b in self.crop_bounds.items():
            if k in clean or clean in k:
                return b
        return self.crop_bounds["default"]

    def validate_single_row(
        self, row: ParsedRow, rolling_median_price: Optional[float] = None
    ) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Validates a single ParsedRow.
        
        Returns:
            (is_valid: bool, rejection_reason: Optional[str], clean_row_dict: Optional[dict])
        Preserves original integer price values without introducing artificial decimals.
        """
        # 1. Required fields present
        if not row.crop or not str(row.crop).strip():
            return False, "Missing mandatory crop name", None
        if not row.mandi or not str(row.mandi).strip():
            return False, "Missing mandatory mandi location", None
        if not row.date or not str(row.date).strip():
            return False, "Missing mandatory trade date", None

        # 2. Date parsing and future date check
        try:
            row_date = datetime.strptime(str(row.date)[:10], "%Y-%m-%d").date()
        except ValueError:
            return False, f"Invalid date format '{row.date}'. Expected YYYY-MM-DD", None

        if row_date > self.today:
            return False, f"Date {row_date} is in the future (today is {self.today})", None

        # 3. Unit normalization and unknown unit quarantine
        # If exogenous weather/diesel, bypass commodity unit converter
        if row.crop in ["weather_exogenous", "diesel_exogenous"]:
            norm_modal = float(row.modal_price)
            norm_min = float(row.min_price)
            norm_max = float(row.max_price)
            norm_arrivals = float(row.arrivals)
            std_unit = row.unit
        else:
            try:
                norm_modal, std_unit = normalize_price_to_quintal(row.modal_price, row.unit, row.crop)
                norm_min, _ = normalize_price_to_quintal(row.min_price, row.unit, row.crop)
                norm_max, _ = normalize_price_to_quintal(row.max_price, row.unit, row.crop)
                norm_arrivals = normalize_arrival_to_quintal(row.arrivals, row.unit, row.crop)
            except UnknownUnitError as e:
                return False, f"Quarantined due to unknown unit: {e}", None
            except ValueError as e:
                return False, f"Unit conversion value error: {e}", None

        # 4. Plausibility checks on prices
        if norm_modal <= 0:
            return False, f"Modal price must be strictly positive, got {norm_modal}", None
        if norm_min < 0 or norm_max < 0:
            return False, f"Min/Max prices cannot be negative (min={norm_min}, max={norm_max})", None

        # Check min <= modal <= max
        if norm_min > norm_modal:
            return False, f"Plausibility failure: min_price ({norm_min}) > modal_price ({norm_modal})", None
        if norm_modal > norm_max:
            return False, f"Plausibility failure: modal_price ({norm_modal}) > max_price ({norm_max})", None

        # Strict rule: reject any row with exactly synthesized 0.90 / 1.10 min/max ratios
        if norm_modal > 0 and round(norm_min, 2) == round(0.9 * norm_modal, 2) and round(norm_max, 2) == round(1.1 * norm_modal, 2):
            return False, f"Suspicious synthesized min/max ratio: min={norm_min}, modal={norm_modal}, max={norm_max}", None

        # 5. Crop bounds check (for agricultural commodities)
        # 5. Crop bounds check
        if row.crop not in ["weather_exogenous", "diesel_exogenous"]:
            crop_key = row.crop.lower().strip().replace(" ", "_")
            bounds = self.crop_bounds.get(crop_key, self.crop_bounds["default"])
            min_bound, max_bound = bounds
            min_bound, max_bound = self.get_bounds_for_crop(row.crop)
            if norm_modal < min_bound or norm_modal > max_bound:
                return False, f"Price Rs {norm_modal}/qtl outside plausible bounds [{min_bound}, {max_bound}] for {row.crop}", None

            # 6. Sane multiple of rolling median check (3x jump rule)
            if rolling_median_price and rolling_median_price > 0:
                ratio = norm_modal / rolling_median_price
                if ratio > 3.0:
                    return False, f"Suspicious price spike: Rs {norm_modal} is {ratio:.1f}x higher than mandi rolling median ({rolling_median_price})", None
                elif ratio < 0.33:
                    return False, f"Suspicious price drop: Rs {norm_modal} is {ratio:.1f}x of mandi rolling median ({rolling_median_price})", None

        # 7. Non-negative arrivals check
        if norm_arrivals < 0:
            return False, f"Arrival volume cannot be negative, got {norm_arrivals}", None

        # 8. Traceability & Acquisition method check: anything 'unknown' stays out of panel
        if getattr(row, "acquisition_method", "unknown") == "unknown" or not getattr(row, "raw_file", None) or row.raw_file == "unknown":
            return False, "Traceability failure: acquisition_method or raw_file is unknown/unverified", None

        # Record passes all validation checks
        clean_dict = {
            "crop": row.crop.lower().strip(),
            "mandi": row.mandi.strip(),
            "district": row.district.strip(),
            "date": str(row_date),
            "min_price": norm_min,
            "modal_price": norm_modal,
            "max_price": norm_max,
            "arrivals": norm_arrivals,
            "unit": std_unit,
            "source_id": row.source_id,
            "source_url": row.source_url,
            "fetched_at": row.fetched_at,
            "raw_hash": row.raw_hash,
            "raw_file": row.raw_file,
            "raw_line": row.raw_line,
            "acquisition_method": row.acquisition_method,
            "data_provenance": "real",
            "is_synthetic": False
        }
        return True, None, clean_dict

    def quarantine_records(self, quarantined_rows: List[Dict[str, Any]], batch_id: str):
        """Saves quarantined rows with detailed diagnostic reasons to data/quarantine/."""
        if not quarantined_rows:
            return

        date_stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = f"quarantine_{batch_id}_{date_stamp}.json"
        filepath = os.path.join(self.quarantine_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(quarantined_rows, f, indent=2)

        logger.warning(f"Quarantined {len(quarantined_rows)} invalid records to {filepath}")

    def cross_source_reconciliation(
        self, accepted_records: List[Dict[str, Any]], source_priorities: Dict[str, int]
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Deduplicates and cross-checks records from multiple sources.
        
        - Key: (crop, mandi, date)
        - When multiple sources report same key:
          - Logs disagreement if modal prices differ by > 10%
          - Resolves conflict using source priority (lower number = higher authority)
        Key: (crop, mandi, date)
        """
        grouped = {}
        for r in accepted_records:
            key = (r["crop"], r["mandi"], r["date"])
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(r)

        reconciled = []
        discrepancies = []

        for key, recs in grouped.items():
            if len(recs) == 1:
                reconciled.append(recs[0])
            else:
                # Compare prices
                prices = [r["modal_price"] for r in recs]
                min_p, max_p = min(prices), max(prices)
                if min_p > 0:
                    pct_diff = ((max_p - min_p) / min_p) * 100.0
                    if pct_diff > 10.0:
                        discrepancies.append({
                            "key": list(key),
                            "percent_diff": round(pct_diff, 1),
                            "sources_competing": [
                                {"source": r["source_id"], "price": r["modal_price"], "priority": source_priorities.get(r["source_id"], 99)}
                                for r in recs
                            ]
                        })

                # Pick highest priority source
                best_rec = min(recs, key=lambda r: source_priorities.get(r["source_id"], 99))
                reconciled.append(best_rec)

        return reconciled, discrepancies
