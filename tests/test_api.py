"""Unit tests for FastAPI backend endpoints."""

import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_version" in data
    assert "provenance" in data
    assert data["provenance"] in ["real", "synthetic"]
    assert "is_synthetic" in data
    if data["is_synthetic"]:
        assert data["synthetic_banner"] == "SYNTHETIC DATA - NOT FOR REAL DECISIONS"


def test_mandis_endpoint():
    response = client.get("/api/mandis")
    assert response.status_code == 200
    mandis = response.json()
    assert len(mandis) >= 3
    names = [m["name"] for m in mandis]
    assert any("Kolar" in n for n in names)
    assert any("Yeshwanthpur" in n for n in names)
    for m in mandis:
        assert "lat" in m and "lon" in m
        assert 12.0 <= m["lat"] <= 15.0  # Karnataka bounds
        assert 75.0 <= m["lon"] <= 79.0


def test_forecast_endpoint_quantiles_and_confidence():
    response = client.get("/api/forecast?mandi=Kolar")
    assert response.status_code == 200
    data = response.json()
    assert data["crop"] == "onion"
    if data.get("status") in ["not_available", "no_trained_models"]:
        assert data["horizons"] == []
        assert data.get("spot_price_today") is None
    else:
        assert len(data["horizons"]) == 3
        for h_info in data["horizons"]:
            p10 = h_info["p10_downside"]
            p50 = h_info["p50_expected"]
            p90 = h_info["p90_upside"]
            # Quantile ordering rule: P10 <= P50 <= P90
            assert p10 <= p50 <= p90, f"Quantile ordering failed: {p10} <= {p50} <= {p90}"
            assert h_info["interval_width"] == round(p90 - p10, 2)
            # Test low confidence flag
            assert "is_low_confidence" in h_info
            if h_info["coverage_pct"] < 70.0 or not h_info["beats_naive"]:
                assert h_info["is_low_confidence"] is True
                assert h_info["confidence_reason"] is not None


def test_where_to_sell_net_price_and_ranking():
    payload = {
        "farmer_location": "Kolar",
        "quantity_quintals": 30.0,
        "horizon_days": 7
    }
    response = client.post("/api/where-to-sell", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "ranked_mandis" in data
    if len(data["ranked_mandis"]) >= 1:
        top = data["ranked_mandis"][0]
        # Check net price math: net = gross - transport - fees - shrinkage
        computed_net = round(
            top["gross_price_p50"]
            - top["transport_cost_per_qtl"]
            - top["fees_and_commission_per_qtl"]
            - top["shrinkage_loss_per_qtl"],
            2
        )
        assert abs(top["net_price_p50"] - computed_net) <= 0.05
        assert top["net_price_p10_downside"] <= top["net_price_p50"] <= top["net_price_p90_upside"]
    else:
        # Panel has no real price data for Karnataka mandis
        assert data["local_mandi_net_p50"] is None


def test_when_to_sell_simulation():
    payload = {
        "farmer_location": "Kolar",
        "quantity_quintals": 30.0,
        "storage_type": "open",
        "has_trader_debt": True,
        "simulate_credit_comparison": True
    }
    response = client.post("/api/when-to-sell", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "simulation_results" in data
    if data.get("price_today") is not None:
        assert len(data["simulation_results"]) >= 4  # 0, 7, 14, 30 days
        for r in data["simulation_results"]:
            assert 0.0 <= r["prob_wait_beats_today_pct"] <= 100.0
            assert "expected_gain_per_qtl" in r
            assert "worst_case_p10_gain" in r
        assert data["credit_comparison"] is not None
        assert "trader_debt_rate_annual_pct" in data["credit_comparison"]
    else:
        assert data["price_today"] is None
        assert data["simulation_results"] == []


def test_advice_endpoint_multilingual():
    for lang in ["en", "hi", "kn"]:
        payload = {
            "farmer_location": "Kolar",
            "quantity_quintals": 30.0,
            "storage_type": "open",
            "has_trader_debt": True,
            "language": lang
        }
        response = client.post("/api/advice", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert len(data["summary_sentence"]) > 10
        assert "disclaimer" in data
        assert "The farmer makes the final decision" in data["full_advice_text"] or \
               "ಅಂತಿಮ ನಿರ್ಧಾರ" in data["full_advice_text"] or \
               "अंतिम निर्णय" in data["full_advice_text"]


def test_model_report_transparency():
    response = client.get("/api/model-report")
    assert response.status_code == 200
    data = response.json()
    assert "metrics_table" in data
    assert len(data["metrics_table"]) == 3  # 7, 14, 30 days
    assert "coverage_audit" in data
    assert "assumptions" in data
    assert "transport_rate_per_km_quintal" in data["assumptions"]
    assert "limitations" in data
    assert len(data["limitations"]) > 0


def test_input_validation_negative_quantity():
    payload = {
        "farmer_location": "Kolar",
        "quantity_quintals": -10.0,
        "horizon_days": 7
    }
    response = client.post("/api/where-to-sell", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "friendly_message" in data


def test_no_price_returned_when_karnataka_panel_is_empty():
    """Ensure mandis without onion report not_available, and mandis without trained models report empty horizons."""
    for mandi in ["Kolar", "Chikkaballapur"]:
        response = client.get(f"/api/forecast?mandi={mandi}")
        assert response.status_code == 200
        data = response.json()
        assert data.get("spot_price_today") is None
        assert data.get("status") == "not_available"

    # Bengaluru has real observed onion spot price today, but no trained models (Tier C)
    res_blr = client.get("/api/forecast?mandi=Bengaluru (Yeshwanthpur)")
    assert res_blr.status_code == 200
    blr_data = res_blr.json()
    assert blr_data.get("spot_price_today") == 3500.0
    assert blr_data.get("status") == "no_trained_models"
    assert blr_data.get("horizons") == []


