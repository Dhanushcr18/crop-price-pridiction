"""Where-to-sell optimizer: ranks nearby mandis by net realized return accounting for transport, fees, and shrinkage."""

import math
import os
import yaml
from typing import Dict, List, Optional, Any, Tuple
import pandas as pd
import numpy as np


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration parameters."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Computes great-circle distance between two geocodes using the Haversine formula.
    Strictly symmetric: haversine_km(a, b) == haversine_km(b, a).
    """
    R = 6371.0  # Earth radius in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 2)


def get_road_distance_km(
    origin_lat: float, origin_lon: float,
    dest_lat: float, dest_lon: float,
    config: Optional[dict] = None
) -> Tuple[float, str]:
    """Returns road distance between coordinates.
    Uses Haversine distance multiplied by road_factor Assumption (default 1.25),
    overridden by road_distance_override file if present.
    """
    if config is None:
        config = load_config()

    dist_model = config.get("distance_model", {})
    road_factor = dist_model.get("road_factor", 1.25)
    source_tag = dist_model.get("assumption_label", "ASSUMPTION: Haversine distance multiplied by 1.25 road-factor.")

    crow_flies = haversine_km(origin_lat, origin_lon, dest_lat, dest_lon)
    road_dist = round(crow_flies * road_factor, 1)
    return road_dist, source_tag


def compute_mandi_net_price(
    gross_price: Optional[float],
    distance_km: float,
    quantity_quintals: float,
    config: dict
) -> Dict[str, Any]:
    """
    Computes net realized price per quintal for a specific mandi:
    net_price = gross_price - transport_cost - mandi_fees_commissions - transit_shrinkage
    """
    if gross_price is None:
        return {
            "gross_price": None,
            "distance_km": round(distance_km, 1),
            "transport_cost": None,
            "fees_and_commission": None,
            "transit_shrinkage": None,
            "net_price": None
        }

    c = config.get("costs", {})
    rate_km_qtl = c.get("transport_rate_per_km_quintal", 3.5)
    min_base = c.get("min_trip_freight_base", 300.0)
    mandi_fee_pct = c.get("mandi_user_fee_pct", 0.015)
    commission_pct = c.get("commission_agent_fee_pct", 0.020)
    hamali = c.get("handling_hamali_per_quintal", 12.0)
    shrinkage_pct_100km = c.get("transit_shrinkage_pct_per_100km", 0.0025)

    # 1. Transport cost per quintal
    if distance_km <= 0:
        transport_cost = 0.0
    else:
        fixed_per_qtl = min_base / max(quantity_quintals, 1.0)
        transport_cost = (distance_km * rate_km_qtl) + fixed_per_qtl

    # 2. Statutory Mandi fee and agent commission
    fees_and_commission = (mandi_fee_pct * gross_price) + (commission_pct * gross_price) + hamali

    # 3. In-transit physical shrinkage / desiccation
    shrinkage_loss = (shrinkage_pct_100km * (distance_km / 100.0)) * gross_price

    # 4. Net realized price
    net_price = gross_price - transport_cost - fees_and_commission - shrinkage_loss

    return {
        "gross_price": round(gross_price, 2),
        "distance_km": round(distance_km, 1),
        "transport_cost": round(transport_cost, 2),
        "fees_and_commission": round(fees_and_commission, 2),
        "transit_shrinkage": round(shrinkage_loss, 2),
        "net_price": round(net_price, 2)
    }


def evaluate_where_to_sell_all_mandis(
    crop: str,
    farmer_lat: float,
    farmer_lon: float,
    quantity_quintals: float,
    radius_km: float = 100.0,
    config_path: str = "config.yaml"
) -> Dict[str, Any]:
    """Evaluates ALL Karnataka mandis in radius reporting the given crop.
    
    Rules:
    - Excludes non-quintal crops.
    - Excludes Tier C mandis (mandis with no recent report or 0 data).
    - Ranks by reported modal price minus transport and statutory fees (Assumption).
    - Displays net price range based on reported min and max prices.
    - Labeled 'based on the latest reported prices, not a forecast'.
    - Reports excluded mandi count and reasons.
    """
    config = load_config(config_path)

    # Load master mandis and panel
    master_mandis_path = config.get("paths", {}).get("master_mandis", "data/master/mandis.csv")
    panel_path = config.get("paths", {}).get("processed_panel", "data/processed/panel.parquet")
    crops_path = config.get("paths", {}).get("master_crops", "data/master/crops.csv")

    df_mandis = pd.read_csv(master_mandis_path)
    df_panel = pd.read_parquet(panel_path)
    df_crops = pd.read_csv(crops_path)

    # Validate crop and unit
    crop_clean = crop.lower().strip()
    crop_match = df_crops[df_crops["name_en"].str.lower() == crop_clean]
    if crop_match.empty:
        # Try slug
        crop_match = df_crops[df_crops["crop_id"] == crop_clean]

    if crop_match.empty:
        return {
            "status": "error",
            "message": f"Crop '{crop}' not found in master catalog.",
            "crop": crop,
            "results": [],
            "excluded_count": 0,
            "disclaimer": "based on the latest reported prices, not a forecast"
        }

    crop_name = crop_match["name_en"].values[0]
    unit = crop_match["unit"].values[0]

    # Non-quintal crops are excluded from quintal net-price math
    if unit != "Quintal":
        return {
            "status": "non_quintal_excluded",
            "message": f"Commodity '{crop_name}' is traded in '{unit}', not Quintals. Excluded from quintal-based freight/net price optimization.",
            "crop": crop_name,
            "unit": unit,
            "results": [],
            "excluded_count": len(df_mandis),
            "disclaimer": "based on the latest reported prices, not a forecast"
        }

    # Filter panel for crop (KSAMB clean rows)
    panel_crop = df_panel[
        (df_panel["crop"].str.lower() == crop_name.lower()) &
        (df_panel["raw_file"].str.contains("Crop_price_of_all_mandies_of_karnataka", na=False))
    ].copy()

    # Calculate distance to every master mandi
    candidates = []
    excluded_mandis_no_report = 0
    excluded_mandis_out_of_radius = 0

    # Build lookup of mandi latest prices applying headline rule
    # In multi-grade markets, select highest arrivals row
    mandi_latest_prices = {}
    for mandi_name, group in panel_crop.groupby("mandi"):
        best_row = group.sort_values(by="arrivals", ascending=False).iloc[0]
        mandi_latest_prices[mandi_name.upper()] = {
            "min_price": float(best_row["min_price"]),
            "modal_price": float(best_row["modal_price"]),
            "max_price": float(best_row["max_price"]),
            "arrivals": float(best_row["arrivals"]),
            "variety": str(best_row.get("variety", "Standard")),
            "grade": str(best_row.get("grade", "FAQ")),
            "date": str(best_row["date"])[:10],
            "source": str(best_row.get("data_provenance", "real"))
        }

    for _, m_row in df_mandis.iterrows():
        m_name = m_row["name_en"]
        raw_m = m_row["raw_market_name"].upper()
        m_lat = float(m_row["lat"])
        m_lon = float(m_row["lon"])

        # Check distance
        dist_km, dist_source = get_road_distance_km(farmer_lat, farmer_lon, m_lat, m_lon, config)

        if dist_km > radius_km:
            excluded_mandis_out_of_radius += 1
            continue

        # Check if mandi reported prices for this crop
        price_info = mandi_latest_prices.get(raw_m)
        if not price_info:
            # Also try matching canonical name
            for k, v in mandi_latest_prices.items():
                if k in m_name.upper() or m_name.upper() in k:
                    price_info = v
                    break

        if not price_info:
            excluded_mandis_no_report += 1
            continue

        # Compute net prices for modal, min, and max
        net_modal_calc = compute_mandi_net_price(price_info["modal_price"], dist_km, quantity_quintals, config)
        net_min_calc = compute_mandi_net_price(price_info["min_price"], dist_km, quantity_quintals, config)
        net_max_calc = compute_mandi_net_price(price_info["max_price"], dist_km, quantity_quintals, config)

        candidates.append({
            "mandi": m_name,
            "raw_mandi": raw_m,
            "district": m_row["district_en"],
            "distance_km": dist_km,
            "is_local": dist_km <= 15.0,
            "reported_date": price_info["date"],
            "variety": price_info["variety"],
            "grade": price_info["grade"],
            "arrivals_quintal": price_info["arrivals"],
            "reported_min_price": price_info["min_price"],
            "reported_modal_price": price_info["modal_price"],
            "reported_max_price": price_info["max_price"],
            "transport_cost_per_qtl": net_modal_calc["transport_cost"],
            "fees_and_commission_per_qtl": net_modal_calc["fees_and_commission"],
            "transit_shrinkage_per_qtl": net_modal_calc["transit_shrinkage"],
            "net_price_modal": net_modal_calc["net_price"],
            "net_price_min": net_min_calc["net_price"],
            "net_price_max": net_max_calc["net_price"],
            "net_price_range": f"Rs {net_min_calc['net_price']:,.0f} - {net_max_calc['net_price']:,.0f}"
        })

    # Sort descending by net_price_modal
    ranked = sorted(candidates, key=lambda x: x["net_price_modal"], reverse=True)

    # Compute gain over local if a local mandi exists
    local_mandi = next((m for m in ranked if m["is_local"]), None)
    local_net = local_mandi["net_price_modal"] if local_mandi else (ranked[-1]["net_price_modal"] if ranked else 0)

    for item in ranked:
        gain = round(item["net_price_modal"] - local_net, 2)
        item["gain_over_local_per_qtl"] = gain
        item["total_gain_rs"] = round(gain * quantity_quintals, 2)

    return {
        "status": "success",
        "crop": crop_name,
        "quantity_quintals": quantity_quintals,
        "radius_km": radius_km,
        "results": ranked,
        "reporting_mandis_in_range": len(ranked),
        "excluded_mandis_no_report": excluded_mandis_no_report,
        "excluded_mandis_out_of_radius": excluded_mandis_out_of_radius,
        "excluded_notice": f"{excluded_mandis_no_report} mandis nearby have no recent report for {crop_name}.",
        "disclaimer": "based on the latest reported prices, not a forecast",
        "assumption_label": "ASSUMPTION: Net price deduction accounts for freight (Rs 3.5/qtl/km * 1.25 road-factor), 3.5% statutory fees/commission, and 0.25%/100km shrinkage."
    }


def rank_mandis_for_sale(
    farmer_location: str,
    quantity_quintals: float,
    forecast_prices: Dict[str, Dict[str, float]],
    config_path: str = "config.yaml"
) -> List[Dict[str, Any]]:
    """Backward compatibility wrapper ranking candidate mandis."""
    config = load_config(config_path)
    distance_matrix = config.get("distance_matrix_km", {})
    loc_key = farmer_location
    if loc_key not in distance_matrix:
        for k in distance_matrix:
            if loc_key.lower() in k.lower():
                loc_key = k
                break
    local_distances = distance_matrix.get(loc_key, {})

    results = []
    for mandi_name, prices in forecast_prices.items():
        mandi_dist_key = mandi_name
        if mandi_dist_key not in local_distances:
            for k in local_distances:
                if mandi_dist_key.lower() in k.lower():
                    mandi_dist_key = k
                    break
        dist_km = local_distances.get(mandi_dist_key, 50.0)
        p50 = prices.get("p50")
        p10 = prices.get("p10")
        p90 = prices.get("p90")
        if p50 is None:
            continue
        net_calc = compute_mandi_net_price(p50, dist_km, quantity_quintals, config)
        net_p10_calc = compute_mandi_net_price(p10, dist_km, quantity_quintals, config)
        results.append({
            "mandi": mandi_name,
            "distance_km": dist_km,
            "forecast_p10": p10,
            "forecast_p50": p50,
            "forecast_p90": p90,
            "transport_cost_per_qtl": net_calc["transport_cost"],
            "fees_and_commission_per_qtl": net_calc["fees_and_commission"],
            "shrinkage_loss_per_qtl": net_calc["transit_shrinkage"],
            "net_price_p50": net_calc["net_price"],
            "net_price_p10": net_p10_calc["net_price"],
            "gain_over_local_per_qtl": 0.0,
            "total_gain_rs": 0.0,
            "is_local": dist_km <= 5.0
        })

    local_mandi = next((m for m in results if m["is_local"]), None)
    local_net = local_mandi["net_price_p50"] if local_mandi else (results[-1]["net_price_p50"] if results else 0)
    for item in results:
        gain = round(item["net_price_p50"] - local_net, 2)
        item["gain_over_local_per_qtl"] = gain
        item["total_gain_rs"] = round(gain * quantity_quintals, 2)

    return sorted(results, key=lambda x: x["net_price_p50"], reverse=True)[:3]
