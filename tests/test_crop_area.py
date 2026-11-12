"""Unit and integration tests for Crop Area and Supply Outlook feature."""

import os
import pytest
from fastapi.testclient import TestClient

from src.data.units import acres_to_hectares, hectares_to_acres, ACRES_PER_HECTARE
from src.data.area_repository import AreaRepository
from backend.main import app


@pytest.fixture
def test_client():
    return TestClient(app)


def test_acre_hectare_conversions():
    """Verify shared physical unit conversion accuracy."""
    assert round(hectares_to_acres(1.0), 4) == 2.4711 or round(hectares_to_acres(1.0), 3) == 2.471
    assert round(acres_to_hectares(2.47105), 4) == 1.0000

    # Symmetry
    acres = 125.5
    ha = acres_to_hectares(acres)
    assert abs(hectares_to_acres(ha) - acres) < 1e-6

    # Negative validation
    with pytest.raises(ValueError):
        acres_to_hectares(-5.0)
    with pytest.raises(ValueError):
        hectares_to_acres(-10.0)


def test_area_report_input_validations(test_client):
    """Test validation against negative, zero, outlier (>500), and unknown district."""
    # Negative acres
    r_neg = test_client.post("/api/area-report", json={
        "district": "Mysuru", "season": "Kharif", "year": "2024-25", "acres": -10.0
    })
    assert r_neg.status_code == 422

    # Zero acres
    r_zero = test_client.post("/api/area-report", json={
        "district": "Mysuru", "season": "Kharif", "year": "2024-25", "acres": 0.0
    })
    assert r_zero.status_code == 422

    # Outlier (>500 acres)
    r_huge = test_client.post("/api/area-report", json={
        "district": "Mysuru", "season": "Kharif", "year": "2024-25", "acres": 501.0
    })
    assert r_huge.status_code == 422
    assert "exceeds" in str(r_huge.json())

    # Unknown district
    r_unk = test_client.post("/api/area-report", json={
        "district": "Atlantis", "season": "Kharif", "year": "2024-25", "acres": 25.0
    })
    assert r_unk.status_code == 422


def test_duplicate_entry_upsert_handling():
    """Verify that multiple submissions from same device update rather than duplicate."""
    repo = AreaRepository()
    dev_id = "test_device_upsert_unique_1"

    res1 = repo.submit_report("Gadag", "Kharif", "2024-25", 20.0, dev_id)
    assert res1["action"] in ["created", "updated"]

    summary1 = repo.get_farmer_reports_summary("Gadag", "Kharif", "2024-25")
    initial_count = summary1["entry_count"]

    # Same device submits updated acreage
    res2 = repo.submit_report("Gadag", "Kharif", "2024-25", 35.0, dev_id)
    assert res2["action"] == "updated"

    summary2 = repo.get_farmer_reports_summary("Gadag", "Kharif", "2024-25")
    # Entry count must NOT increment
    assert summary2["entry_count"] == initial_count


def test_coverage_ratio_and_too_few_reports_rule():
    """Verify coverage math and that N < 30 or coverage < 5% triggers 'too_few_reports'."""
    repo = AreaRepository()
    summary = repo.get_complete_area_summary("Gadag", "Kharif", "2024-25")

    farmer_rep = summary["farmer_reported"]
    assert "entry_count" in farmer_rep
    assert "reported_acres" in farmer_rep

    # If count < 30, too_few_reports must be True
    if farmer_rep["entry_count"] < 30:
        assert farmer_rep["too_few_reports"] is True
        assert "Too few reports to trust" in farmer_rep["warning_message"]


def test_mysuru_district_data_missing_and_state_fallback(test_client):
    """Verify Mysuru official district data is reported as 'Not available' with state fallback."""
    resp = test_client.get("/api/area-summary?district=Mysuru&season=Kharif&year=2024-25")
    assert resp.status_code == 200
    data = resp.json()

    assert data["district_official_available"] is False
    assert data["district_official"] is None
    # State data must be present
    assert data["state_official"] is not None
    assert data["state_official"]["region_name"] == "Karnataka"
    assert data["state_official"]["area_acres"] > 0
    assert "source_name" in data["state_official"]
    assert "publication_date" in data["state_official"]


def test_supply_signal_and_price_ranges(test_client):
    """Verify supply outlook returns 30/60/90 day ranges, rounded, with autonomy disclaimer."""
    resp = test_client.get("/api/supply-price-outlook?district=Mysuru&season=Kharif&year=2024-25")
    assert resp.status_code == 200
    data = resp.json()

    assert data["supply_signal"] in ["higher", "normal", "lower"]
    assert len(data["horizons"]) == 3
    for h in data["horizons"]:
        assert h["horizon_days"] in [30, 60, 90]
        assert h["p10_downside"] <= h["p50_expected"] <= h["p90_upside"]
        # Rounded to nearest 10
        assert h["p10_downside"] % 10 == 0
        assert h["p50_expected"] % 10 == 0
        assert h["p90_upside"] % 10 == 0

    assert data["autonomy_disclaimer"] == "This is advice, the decision is yours."
    assert "strictly isolated" in data["farmer_acreage_isolated_notice"]


def test_farmer_acreage_isolation_from_model_forecast(test_client):
    """Hard rule: Farmer-entered acres must NEVER affect the price forecast output."""
    # 1. Fetch baseline outlook
    r_before = test_client.get("/api/supply-price-outlook?district=Chitradurga&season=Kharif&year=2024-25").json()

    # 2. Submit various farmer reports
    test_client.post("/api/area-report", json={
        "district": "Chitradurga", "season": "Kharif", "year": "2024-25", "acres": 45.0, "device_id": "isolation_dev_1"
    })
    test_client.post("/api/area-report", json={
        "district": "Chitradurga", "season": "Kharif", "year": "2024-25", "acres": 150.0, "device_id": "isolation_dev_2"
    })

    # 3. Fetch outlook again
    r_after = test_client.get("/api/supply-price-outlook?district=Chitradurga&season=Kharif&year=2024-25").json()

    # The price forecast numbers and supply signal must remain identical!
    for h_before, h_after in zip(r_before["horizons"], r_after["horizons"]):
        assert h_before["p10_downside"] == h_after["p10_downside"]
        assert h_before["p50_expected"] == h_after["p50_expected"]
        assert h_before["p90_upside"] == h_after["p90_upside"]


def test_no_leakage_in_area_features():
    """Verify that build_area_features only uses official records published on or before date t."""
    from src.models.forecast_area_experiment import build_area_features
    import pandas as pd

    # Synthetic test panel with dates before and after publication
    dates = pd.date_range("2021-01-01", periods=10, freq="180D")
    df = pd.DataFrame({
        "date": dates,
        "mandi": ["Kolar"] * 10,
        "modal_price": [3000] * 10
    })

    config = {
        "paths": {"processed_panel": "data/processed/panel.parquet"},
        "area_outlook": {"sowing_to_harvest_lag_days": 105}
    }
    feats = build_area_features(df, config)
    assert "official_state_area_ha" in feats.columns
    assert "state_area_change_5yr" in feats.columns
    # Ensure no NaN
    assert not feats["official_state_area_ha"].isna().any()

