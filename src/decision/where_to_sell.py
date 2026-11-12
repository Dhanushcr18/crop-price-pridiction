"""Where-to-sell optimizer: ranks nearby mandis by net realized return accounting for transport, fees, and shrinkage."""

import yaml
from typing import Dict, List, Optional, Any
import numpy as np


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration parameters."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


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

    c = config["costs"]
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
        # Distance variable freight + fixed base trip charge divided by quantity
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


def rank_mandis_for_sale(
    farmer_location: str,
    quantity_quintals: float,
    forecast_prices: Dict[str, Dict[str, float]],
    config_path: str = "config.yaml"
) -> List[Dict]:
    """
    Ranks all candidate mandis by expected net price (P50) and downside net price (P10).
    Calculates gain over farmer's local mandi in Rs/quintal and total Rs for farmer's lot.

    forecast_prices format:
    {
        "Bengaluru (Yeshwanthpur)": {"p10": 3400.0, "p50": 3950.0, "p90": 4300.0},
        "Kolar": {"p10": 3200.0, "p50": 3750.0, "p90": 4100.0},
        "Chikkaballapur": {"p10": 3150.0, "p50": 3700.0, "p90": 4050.0}
    }
    """
    config = load_config(config_path)
    distance_matrix = config.get("distance_matrix_km", {})

    # Normalize location lookup
    loc_key = farmer_location
    if loc_key not in distance_matrix:
        for k in distance_matrix:
            if loc_key.lower() in k.lower():
                loc_key = k
                break

    local_distances = distance_matrix.get(loc_key, {})

    results = []
    local_net_p50 = None
    local_net_p10 = None

    # First pass: evaluate each mandi
    for mandi, prices in forecast_prices.items():
        dist = local_distances.get(mandi, 25.0)
        p10_res = compute_mandi_net_price(prices["p10"], dist, quantity_quintals, config)
        p50_res = compute_mandi_net_price(prices["p50"], dist, quantity_quintals, config)
        p90_res = compute_mandi_net_price(prices["p90"], dist, quantity_quintals, config)

        is_local = (mandi == loc_key) or (dist <= 10.0)

        res_item = {
            "mandi": mandi,
            "distance_km": dist,
            "is_local": is_local,
            "forecast_p10": prices["p10"],
            "forecast_p50": prices["p50"],
            "forecast_p90": prices["p90"],
            "transport_cost_per_qtl": p50_res["transport_cost"],
            "fees_and_commission_per_qtl": p50_res["fees_and_commission"],
            "shrinkage_loss_per_qtl": p50_res["transit_shrinkage"],
            "net_price_p50": p50_res["net_price"],
            "net_price_p10": p10_res["net_price"],
            "net_price_p90": p90_res["net_price"],
        }
        results.append(res_item)

        if is_local and local_net_p50 is None:
            local_net_p50 = p50_res["net_price"]
            local_net_p10 = p10_res["net_price"]

    # Fallback if local not identified or local has no price
    valid_results = [r for r in results if r["net_price_p50"] is not None]
    if not valid_results:
        return []

    if local_net_p50 is None:
        local_net_p50 = min(r["net_price_p50"] for r in valid_results)
        local_net_p10 = min(r["net_price_p10"] for r in valid_results)

    # Second pass: compute gain over local mandi and rank
    for item in valid_results:
        gain_per_qtl = round(item["net_price_p50"] - local_net_p50, 2)
        gain_p10_per_qtl = round(item["net_price_p10"] - local_net_p10, 2)
        total_gain = round(gain_per_qtl * quantity_quintals, 2)

        item["gain_over_local_per_qtl"] = gain_per_qtl
        item["gain_p10_over_local_per_qtl"] = gain_p10_per_qtl
        item["total_gain_rs"] = total_gain

    # Rank descending by expected net price (P50)
    ranked = sorted(valid_results, key=lambda x: x["net_price_p50"], reverse=True)
    return ranked[:3]


if __name__ == "__main__":
    sample_forecast = {
        "Bengaluru (Yeshwanthpur)": {"p10": 3450.0, "p50": 4050.0, "p90": 4450.0},
        "Kolar": {"p10": 3200.0, "p50": 3720.0, "p90": 4100.0},
        "Chikkaballapur": {"p10": 3150.0, "p50": 3680.0, "p90": 4050.0}
    }
    top_mandis = rank_mandis_for_sale(
        farmer_location="Kolar",
        quantity_quintals=50.0,
        forecast_prices=sample_forecast
    )
    print("=== TOP MANDIS FOR KOLAR FARMER (50 Quintals) ===")
    for idx, m in enumerate(top_mandis, 1):
        print(f"Rank {idx}: {m['mandi']}")
        print(f"  Distance: {m['distance_km']} km | Transport: Rs {m['transport_cost_per_qtl']}/qtl")
        print(f"  Expected Net Price: Rs {m['net_price_p50']}/qtl | Downside (P10): Rs {m['net_price_p10']}/qtl")
        print(f"  Gain over Local Mandi: Rs {m['gain_over_local_per_qtl']}/qtl (Total: Rs {m['total_gain_rs']:,})")

