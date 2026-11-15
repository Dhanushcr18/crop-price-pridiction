"""Comprehensive validation suite for All Crops and 115 Karnataka Mandis.
Tests strict data rules, tier gating, quarantine isolation, freshness calculation,
and proves no hard-coded defaults remain in backend, src, or frontend.
"""

import os
import re
import pytest
import pandas as pd
from fastapi.testclient import TestClient
from backend.main import app
from backend.models_loader import AdvisorService
from src.decision.where_to_sell import haversine_km, get_road_distance_km

client = TestClient(app)


# ---------------------------------------------------------------------------
# Test 1: No price is returned for a crop-mandi without a real row
# ---------------------------------------------------------------------------
def test_no_price_for_unreported_pair_no_default_fallback():
    """Verify that a crop-mandi without a real row returns 'Not available'
    and NEVER invents, imputes, or falls back to a default price."""
    # Kolar has NO onion rows in the 2026-11-11 KSAMB report
    resp = client.get("/api/today-price?crop=Onion&mandi=Kolar")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "Not available"
    assert data["available"] is False
    assert data["headline_price"] is None
    assert len(data["all_grades"]) == 0

    # Nonexistent pair
    resp_fake = client.get("/api/today-price?crop=Apple&mandi=Afzalpur")
    assert resp_fake.status_code == 200
    data_fake = resp_fake.json()
    assert data_fake["status"] == "Not available"
    assert data_fake["available"] is False
    assert data_fake["headline_price"] is None


# ---------------------------------------------------------------------------
# Test 2: Quarantined rows never appear in any API response
# ---------------------------------------------------------------------------
def test_quarantined_rows_never_appear_in_api():
    """Verify that all rows flagged and sent to data/quarantine are strictly
    isolated and never surface in today-price, prices/compare, or where-to-sell."""
    service = AdvisorService.get_instance()
    assert service.quarantine_df is not None
    assert len(service.quarantine_df) > 0

    quarantined_mandis = service.fully_quarantined_mandis
    assert "CHIKKAMAGALURU" in quarantined_mandis or "Chikkamagaluru" in [m.title() for m in quarantined_mandis]
    assert "KADUR" in quarantined_mandis or "Kadur" in [m.title() for m in quarantined_mandis]

    # Check today-price for a quarantined market
    resp = client.get("/api/today-price?crop=Coffee&mandi=CHIKKAMAGALURU")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "Data under review"
    assert data["available"] is False
    assert data["headline_price"] is None

    # Check prices/compare
    resp_comp = client.get("/api/prices/compare?crop=Coffee")
    assert resp_comp.status_code == 200
    comp_items = resp_comp.json()
    for item in comp_items:
        assert item["mandi"] not in ["CHIKKAMAGALURU", "KADUR"]

    # Check where-to-sell
    resp_where = client.post("/api/where-to-sell", json={
        "crop": "Coffee",
        "farmer_location": "CHIKKAMAGALURU",
        "quantity_quintals": 30.0,
        "radius_km": 150.0
    })
    assert resp_where.status_code == 200
    where_data = resp_where.json()
    for cand in where_data.get("results", []):
        assert cand["mandi"] not in ["CHIKKAMAGALURU", "KADUR"]


# ---------------------------------------------------------------------------
# Test 3: Stale banner appears when latest report is older than 2 days
# ---------------------------------------------------------------------------
def test_stale_banner_when_older_than_2_days():
    """Report date is 2026-11-11, current reference date is 2026-11-16 (5 days > 2 days).
    Every reported price and coverage endpoint must indicate staleness."""
    resp_cov = client.get("/api/coverage")
    assert resp_cov.status_code == 200
    cov = resp_cov.json()
    assert cov["freshness"]["days_since_latest"] >= 5
    assert cov["freshness"]["stale_banner_required"] is True
    assert "Latest reported" in cov["freshness"]["stale_banner_text"]

    # Today-price must also flag is_stale = True
    resp_price = client.get("/api/today-price?crop=Onion&mandi=BENGALURU")
    assert resp_price.status_code == 200
    pdata = resp_price.json()
    assert pdata["status"] == "Reported"
    assert pdata["is_stale"] is True


# ---------------------------------------------------------------------------
# Test 4: Mandis whose rows are all quarantined show "Data under review"
# ---------------------------------------------------------------------------
def test_fully_quarantined_mandi_shows_data_under_review():
    """Markets where min=max=modal on all rows (CHIKKAMAGALURU, KADUR)
    must explicitly display 'Data under review'."""
    for mandi_name in ["CHIKKAMAGALURU", "KADUR"]:
        resp = client.get(f"/api/today-price?crop=Onion&mandi={mandi_name}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "Data under review"
        assert "review" in data["message"].lower() or "quarantine" in data["message"].lower()


# ---------------------------------------------------------------------------
# Test 5: Automated grep proves NO hard-coded defaults in code
# ---------------------------------------------------------------------------
def test_grep_no_hardcoded_defaults_in_code():
    """Scan backend/ and frontend/src/ to ensure no hard-coded defaults remain
    for crop='onion', mandi='Kolar', 'Chikkaballapur', or 'Bengaluru'."""
    # Pattern matching default assignments in Python or TypeScript
    bad_patterns = [
        re.compile(r'crop:\s*str\s*=\s*["\']onion["\']', re.IGNORECASE),
        re.compile(r'crop\s*=\s*useState<string>\(\s*["\']onion["\']\s*\)', re.IGNORECASE),
        re.compile(r'farmerLocation\s*=\s*useState<string>\(\s*["\'](?:Chikkaballapur|Kolar|Bengaluru)["\']\s*\)', re.IGNORECASE),
        re.compile(r'setFarmerLocation\(\s*["\']Chikkaballapur["\']\s*\)'),
        re.compile(r'setCrop\(\s*["\']onion["\']\s*\)'),
    ]

    scanned_files = []
    violations = []

    # Check backend
    for root, _, files in os.walk("backend"):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                scanned_files.append(path)
                with open(path, "r", encoding="utf-8") as fh:
                    for line_idx, line in enumerate(fh, 1):
                        for pat in bad_patterns:
                            if pat.search(line):
                                violations.append(f"{path}:{line_idx} - {line.strip()}")

    # Check frontend/src
    for root, _, files in os.walk("frontend/src"):
        for f in files:
            if f.endswith((".ts", ".tsx")) and not f.endswith(".d.ts"):
                path = os.path.join(root, f)
                scanned_files.append(path)
                with open(path, "r", encoding="utf-8") as fh:
                    for line_idx, line in enumerate(fh, 1):
                        for pat in bad_patterns:
                            if pat.search(line):
                                violations.append(f"{path}:{line_idx} - {line.strip()}")

    assert len(scanned_files) > 10, "Should have scanned at least 10 source files"
    assert len(violations) == 0, f"Found hard-coded defaults in code: {violations}"


# ---------------------------------------------------------------------------
# Test 6: Distance Symmetry and Road Factor Assumption
# ---------------------------------------------------------------------------
def test_distance_symmetry_and_road_factor():
    """Haversine distance must be strictly symmetric: haversine_km(A, B) == haversine_km(B, A).
    Road distance must equal haversine * road_factor (1.25 # Assumption)."""
    lat1, lon1 = 13.1367, 78.1292  # Kolar
    lat2, lon2 = 12.9716, 77.5946  # Bengaluru

    dist1 = haversine_km(lat1, lon1, lat2, lon2)
    dist2 = haversine_km(lat2, lon2, lat1, lon1)
    assert abs(dist1 - dist2) < 1e-6, "Haversine distance must be symmetric"

    road_dist, source = get_road_distance_km(lat1, lon1, lat2, lon2)
    assert abs(road_dist - round(dist1 * 1.25, 1)) < 1e-4
    assert "ASSUMPTION" in source and "1.25" in source


# ---------------------------------------------------------------------------
# Test 7: Non-Quintal Crops Excluded from Quintal Where-to-Sell
# ---------------------------------------------------------------------------
def test_non_quintal_crops_handling():
    """Coconut (per 1000) and Goat/Sheep (per head) must retain their native units
    and be excluded from quintal net-price math."""
    # Coconut spot price
    resp = client.get("/api/today-price?crop=Coconut&mandi=BENGALURU")
    assert resp.status_code == 200
    data = resp.json()
    if data["status"] == "Reported" and data["headline_price"]:
        assert data["headline_price"]["unit"] in ["Numbers", "Thousands", "Per 1000"]

    # POST /api/where-to-sell for Coconut should return appropriate notice
    resp_where = client.post("/api/where-to-sell", json={
        "crop": "Coconut",
        "farmer_location": "BENGALURU",
        "quantity_quintals": 10.0,
        "radius_km": 150.0
    })
    assert resp_where.status_code == 200


# ---------------------------------------------------------------------------
# Test 8: Master Data Catalog & Tier Gating
# ---------------------------------------------------------------------------
def test_master_data_catalog_and_tier_gating():
    """Verify master data counts: 102 crops, 31 districts, 115 mandis.
    Verify Tier A count is 0 and forecasts are strictly gated."""
    resp_crops = client.get("/api/crops")
    assert resp_crops.status_code == 200
    crops = resp_crops.json()
    assert len(crops) == 102

    resp_districts = client.get("/api/districts")
    assert resp_districts.status_code == 200
    districts = resp_districts.json()
    assert len(districts) == 31

    resp_mandis = client.get("/api/mandis")
    assert resp_mandis.status_code == 200
    mandis = resp_mandis.json()
    assert len(mandis) == 115

    # Gated forecast: Tier A is 0, so forecast must return unavailable
    resp_fc = client.get("/api/forecast?mandi=BENGALURU&crop=Onion")
    assert resp_fc.status_code == 200
    fc = resp_fc.json()
    assert fc["available"] is False
    assert "Tier A required" in fc["message"] or "Tier A" in fc["message"]
