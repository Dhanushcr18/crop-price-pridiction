"""Shared unit conversion utilities for agricultural measurements, prices, and volumes.

Includes:
1. Land area conversions (acres <-> hectares)
2. Agricultural price & volume normalization to Rs per quintal
"""

import re
from typing import Tuple, Optional


class UnknownUnitError(ValueError):
    """Raised when an unrecognized or unsupported trading unit is encountered."""
    pass


# Land Area Constants
ACRES_PER_HECTARE = 2.47105
HECTARES_PER_ACRE = 1.0 / ACRES_PER_HECTARE


def acres_to_hectares(acres: float) -> float:
    """Convert land area from acres to hectares."""
    if acres < 0:
        raise ValueError(f"Acres cannot be negative, got {acres}")
    return float(acres * HECTARES_PER_ACRE)


def hectares_to_acres(hectares: float) -> float:
    """Convert land area from hectares to acres."""
    if hectares < 0:
        raise ValueError(f"Hectares cannot be negative, got {hectares}")
    return float(hectares * ACRES_PER_HECTARE)


# ---------------------------------------------------------------------------
# Price and Volume Normalization
# ---------------------------------------------------------------------------

# Multipliers to convert price in given unit to Price in Rs / Quintal (100 kg)
# Price(Rs/qtl) = Price(unit) * factor
PRICE_TO_QUINTAL_FACTORS = {
    "quintal": 1.0,
    "qtl": 1.0,
    "q": 1.0,
    "rs/quintal": 1.0,
    "rs./quintal": 1.0,
    "rs / quintal": 1.0,
    "100 kg": 1.0,
    "kg": 100.0,
    "kilogram": 100.0,
    "per kg": 100.0,
    "tonne": 0.10,
    "ton": 0.10,
    "metric tonne": 0.10,
    "mt": 0.10,
    "bag (50kg)": 2.0,
    "bag (100kg)": 1.0,
}

# Multipliers to convert arrival volume in given unit to Quintals
# Arrival(qtl) = Arrival(unit) * factor
ARRIVAL_TO_QUINTAL_FACTORS = {
    "quintal": 1.0,
    "qtl": 1.0,
    "q": 1.0,
    "kg": 0.01,
    "kilogram": 0.01,
    "tonne": 10.0,
    "ton": 10.0,
    "metric tonne": 10.0,
    "mt": 10.0,
    "metric tonnes": 10.0,
    "bag (50kg)": 0.50,
    "bag (100kg)": 1.0,
    "bags": 0.50,  # standard APMC grain/produce bag convention ~50kg
}

# Crop-specific count equivalences (approximate weight per unit)
# e.g., 1000 mature coconuts ~ 1,400 kg = 14 quintals
COUNT_CROP_QUINTAL_WEIGHT = {
    "coconut": {
        "numbers": 0.014,    # 1 coconut ~ 1.4 kg = 0.014 qtl
        "thousands": 14.0,   # 1,000 coconuts ~ 14 quintals
        "thousand": 14.0,
    },
    "banana": {
        "dozen": 0.018,      # 1 dozen banana ~ 1.8 kg = 0.018 qtl
        "numbers": 0.0015,
    }
}


def clean_unit_string(unit: str) -> str:
    """Normalize raw unit string: lower case, strip punctuation/spaces."""
    if not unit:
        return ""
    u = str(unit).lower().strip()
    u = re.sub(r"\s+", " ", u)
    u = u.replace("_x0020_", " ")
    return u


def normalize_price_to_quintal(
    price: float, raw_unit: str, crop: Optional[str] = None
) -> Tuple[float, str]:
    """
    Converts a trade price in raw_unit to standard Rs / Quintal.
    
    Returns:
        (normalized_price_rs_per_qtl, display_unit)
        
    Raises:
        UnknownUnitError: If raw_unit is unknown and cannot be converted.
    """
    if price is None:
        raise ValueError("Price cannot be None")
    if price < 0:
        raise ValueError(f"Price cannot be negative, got {price}")

    u = clean_unit_string(raw_unit)

    # Check direct price mapping
    if u in PRICE_TO_QUINTAL_FACTORS:
        factor = PRICE_TO_QUINTAL_FACTORS[u]
        return round(float(price * factor), 2), "Rs/Quintal"

    # Check count-based units with crop context
    crop_clean = crop.lower().strip() if crop else ""
    if crop_clean in COUNT_CROP_QUINTAL_WEIGHT:
        crop_counts = COUNT_CROP_QUINTAL_WEIGHT[crop_clean]
        for c_unit, qtl_weight in crop_counts.items():
            if c_unit in u:
                # If price is per thousand coconuts, 1000 nuts = 14 qtl -> price/qtl = price / 14.0
                price_per_qtl = price / qtl_weight
                return round(float(price_per_qtl), 2), f"Rs/Quintal (from {raw_unit})"

    # If already formatted with quintal anywhere
    if "quintal" in u or "qtl" in u:
        return round(float(price), 2), "Rs/Quintal"

    # Fail loudly on unknown unit
    raise UnknownUnitError(
        f"Unknown or unsupported trading unit '{raw_unit}' for crop '{crop}'. "
        f"Cannot safely convert to Rs/Quintal without risking false advice."
    )


def normalize_arrival_to_quintal(
    arrival: float, raw_unit: str, crop: Optional[str] = None
) -> float:
    """
    Converts an arrival quantity in raw_unit to standard Quintals.
    
    Raises:
        UnknownUnitError: If raw_unit cannot be safely converted.
    """
    if arrival is None:
        return 0.0
    if arrival < 0:
        raise ValueError(f"Arrival volume cannot be negative, got {arrival}")

    u = clean_unit_string(raw_unit)

    if u in ARRIVAL_TO_QUINTAL_FACTORS:
        factor = ARRIVAL_TO_QUINTAL_FACTORS[u]
        return round(float(arrival * factor), 2)

    crop_clean = crop.lower().strip() if crop else ""
    if crop_clean in COUNT_CROP_QUINTAL_WEIGHT:
        crop_counts = COUNT_CROP_QUINTAL_WEIGHT[crop_clean]
        for c_unit, qtl_weight in crop_counts.items():
            if c_unit in u:
                return round(float(arrival * qtl_weight), 2)

    if "quintal" in u or "qtl" in u:
        return round(float(arrival), 2)

    raise UnknownUnitError(f"Unknown arrival unit '{raw_unit}' for crop '{crop}'.")
