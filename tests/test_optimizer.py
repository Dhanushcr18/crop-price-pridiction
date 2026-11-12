"""Test net price calculation and mandi optimization."""

import pytest
from src.decision.where_to_sell import compute_mandi_net_price, rank_mandis_for_sale, load_config


def test_net_price_calculation_math():
    """Verify net price calculation matches: gross - transport - fees - transit shrinkage."""
    config = load_config()
    gross_price = 4000.0
    distance_km = 70.0
    quantity = 50.0

    res = compute_mandi_net_price(gross_price, distance_km, quantity, config)

    # Expected transport = (70 * 3.5) + (300 / 50) = 245.0 + 6.0 = 251.0
    assert abs(res["transport_cost"] - 251.0) < 1e-2

    # Fees = 1.5% APMC (60.0) + 2.0% Comm (80.0) + Hamali (12.0) = 152.0
    assert abs(res["fees_and_commission"] - 152.0) < 1e-2

    # Shrinkage = 0.25% * (70/100) * 4000 = 0.00175 * 4000 = 7.0
    assert abs(res["transit_shrinkage"] - 7.0) < 1e-2

    # Net = 4000 - 251 - 152 - 7 = 3590.0
    expected_net = 4000.0 - 251.0 - 152.0 - 7.0
    assert abs(res["net_price"] - expected_net) < 1e-2


def test_transport_monotonicity_with_distance():
    """Verify that longer transit distance strictly increases freight and transit loss."""
    config = load_config()
    res_near = compute_mandi_net_price(4000.0, 10.0, 50.0, config)
    res_far = compute_mandi_net_price(4000.0, 80.0, 50.0, config)

    assert res_far["transport_cost"] > res_near["transport_cost"]
    assert res_far["transit_shrinkage"] > res_near["transit_shrinkage"]
    assert res_far["net_price"] < res_near["net_price"]


def test_ranking_and_local_gain():
    """Verify rank_mandis_for_sale correctly ranks and sets local gain to zero for local mandi."""
    forecasts = {
        "Kolar": {"p10": 3200.0, "p50": 3700.0, "p90": 4100.0},
        "Bengaluru (Yeshwanthpur)": {"p10": 3500.0, "p50": 4200.0, "p90": 4600.0},
        "Chikkaballapur": {"p10": 3100.0, "p50": 3600.0, "p90": 4000.0}
    }
    ranked = rank_mandis_for_sale("Kolar", 50.0, forecasts)
    assert len(ranked) == 3

    # Check that entries are sorted descending by net_price_p50
    assert ranked[0]["net_price_p50"] >= ranked[1]["net_price_p50"]
    assert ranked[1]["net_price_p50"] >= ranked[2]["net_price_p50"]

    # Local mandi should have gain_over_local == 0
    local_entry = [r for r in ranked if r["is_local"]]
    assert len(local_entry) > 0
    assert local_entry[0]["gain_over_local_per_qtl"] == 0.0

