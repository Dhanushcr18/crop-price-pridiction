"""Integration and user-flow tests for Farmer Sell Advisor web platform."""

import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from backend.main import app
from backend.models_loader import AdvisorService

client = TestClient(app)


def test_sample_farmer_user_flow_all_three_languages():
    """
    Acceptance Criterion 2:
    A sample farmer (onion, 30 quintal, Kolar, no storage, owes trader)
    gets the full results page with real model output, in all three languages.
    """
    farmer_location = "Kolar"
    quantity_quintals = 30.0
    storage_type = "open"
    has_trader_debt = True

    # 1. Fetch Forecast
    fc_res = client.get(f"/api/forecast?mandi={farmer_location}")
    assert fc_res.status_code == 200
    fc = fc_res.json()
    assert fc["crop"] == "onion"
    assert fc["mandi"] == farmer_location
    assert len(fc["horizons"]) == 3
    for h in fc["horizons"]:
        assert h["p10_downside"] <= h["p50_expected"] <= h["p90_upside"]

    # 2. Fetch Where-to-Sell
    where_res = client.post("/api/where-to-sell", json={
        "farmer_location": farmer_location,
        "quantity_quintals": quantity_quintals,
        "horizon_days": 7
    })
    assert where_res.status_code == 200
    where = where_res.json()
    assert len(where["ranked_mandis"]) >= 1
    top_mandi = where["ranked_mandis"][0]
    assert top_mandi["net_price_p10_downside"] <= top_mandi["net_price_p50"] <= top_mandi["net_price_p90_upside"]

    # 3. Fetch When-to-Sell
    when_res = client.post("/api/when-to-sell", json={
        "farmer_location": farmer_location,
        "quantity_quintals": quantity_quintals,
        "storage_type": storage_type,
        "has_trader_debt": has_trader_debt,
        "simulate_credit_comparison": True
    })
    assert when_res.status_code == 200
    when = when_res.json()
    assert len(when["simulation_results"]) >= 4
    for r in when["simulation_results"]:
        assert 0.0 <= r["prob_wait_beats_today_pct"] <= 100.0

    # 4. Fetch Advice in all 3 languages (English, Hindi, Kannada)
    for lang in ["en", "hi", "kn"]:
        adv_res = client.post("/api/advice", json={
            "farmer_location": farmer_location,
            "quantity_quintals": quantity_quintals,
            "storage_type": storage_type,
            "has_trader_debt": has_trader_debt,
            "language": lang
        })
        assert adv_res.status_code == 200
        adv = adv_res.json()
        assert len(adv["summary_sentence"]) > 0
        assert "disclaimer" in adv
        assert "This is advice, the decision is yours" in adv["disclaimer"]
        assert len(adv["p10_p90_range"]) > 0
        # Ensure never states a single price as certain
        assert "to" in adv["p10_p90_range"] or "-" in adv["p10_p90_range"] or "से" in adv["full_advice_text"] or "ರಿಂದ" in adv["full_advice_text"]


def test_low_confidence_badges_trigger_logic():
    """
    Acceptance Criterion 3:
    The low-confidence badges appear correctly when conditions are triggered
    (coverage outside 70-90% or model does not beat naive baseline).
    """
    fc_res = client.get("/api/forecast?mandi=Kolar")
    assert fc_res.status_code == 200
    fc = fc_res.json()

    for h in fc["horizons"]:
        # Verify rule: if coverage < 70% or > 90% or does not beat naive, is_low_confidence must be True
        if h["coverage_pct"] < 70.0 or h["coverage_pct"] > 90.0 or not h["beats_naive"]:
            assert h["is_low_confidence"] is True
            assert h["confidence_reason"] is not None
            assert len(h["confidence_reason"]) > 5
        else:
            assert h["is_low_confidence"] is False


def test_synthetic_banner_trigger_logic():
    """
    Acceptance Criterion 3:
    Synthetic banner appears whenever synthetic rows are present in the panel.
    """
    health_res = client.get("/api/health")
    assert health_res.status_code == 200
    health = health_res.json()

    if health["is_synthetic"]:
        assert health["synthetic_banner"] == "SYNTHETIC DATA - NOT FOR REAL DECISIONS"
        assert health["provenance"] == "synthetic"


def test_stale_data_warning_trigger_logic():
    """
    Acceptance Criterion 3:
    Stale data warning triggers when days_since_data > 3.
    """
    service = AdvisorService.get_instance()
    # Save original
    orig_date = service.last_data_date

    try:
        # Mock date older than 3 days
        service.last_data_date = datetime.now() - timedelta(days=5)
        stale_status = service.get_health_status()
        assert stale_status["is_stale"] is True
        assert stale_status["days_since_data"] == 5

        # Mock fresh date (< 3 days)
        service.last_data_date = datetime.now() - timedelta(days=1)
        fresh_status = service.get_health_status()
        assert fresh_status["is_stale"] is False
        assert fresh_status["days_since_data"] == 1
    finally:
        service.last_data_date = orig_date


def test_model_transparency_page_data_fidelity():
    """
    Acceptance Criterion 4:
    The Model Transparency page shows the real metrics from reports/.
    """
    rep_res = client.get("/api/model-report")
    assert rep_res.status_code == 200
    rep = rep_res.json()

    # Verify metrics table
    assert len(rep["metrics_table"]) == 3
    horizons = [r["horizon"] for r in rep["metrics_table"]]
    assert "7 Days" in horizons
    assert "14 Days" in horizons
    assert "30 Days" in horizons

    # 30-day horizon LightGBM must beat naive baseline
    h30 = next(r for r in rep["metrics_table"] if "30" in r["horizon"])
    assert h30["beats_naive"] is True
    assert h30["lgb_p50_mae"] < h30["naive_mae"]

    # Coverage audit must flag under-covered horizons
    assert len(rep["coverage_audit"]) == 3
    for aud in rep["coverage_audit"]:
        assert aud["is_flagged"] is True
        assert "Under-covered" in aud["reason"]

    # Assumptions must match config.yaml
    assert rep["assumptions"]["transport_rate_per_km_quintal"] == 3.5
    assert rep["assumptions"]["min_trip_freight_base"] == 300.0
    assert rep["assumptions"]["mandi_user_fee_pct"] == 1.5
    assert rep["assumptions"]["commission_agent_fee_pct"] == 2.0

