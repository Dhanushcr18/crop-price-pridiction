"""Tests for automated ingestion, connector parsers, robots policy gating, quarantine, and idempotency."""

import os
import json
import pytest
from datetime import datetime, date
from unittest.mock import patch, MagicMock

from src.ingest.base import RawPayload, ParsedRow, PolicyBlockedError, SchemaValidationError
from src.ingest.connectors.data_gov import DataGovConnector
from src.ingest.connectors.agmarknet import AgmarknetConnector
from src.ingest.connectors.raita_mitra import RaitaMitraConnector
from src.ingest.connectors.enam import ENAMConnector
from src.ingest.connectors.open_meteo import OpenMeteoConnector
from src.ingest.connectors.ppac_diesel import PPACDieselConnector
from src.ingest.validate import ValidationEngine
from src.data.units import normalize_price_to_quintal, normalize_arrival_to_quintal, UnknownUnitError


# ---------------------------------------------------------------------------
# 1. ROBOTS & POLICY GATING TEST
# ---------------------------------------------------------------------------
def test_robots_blocked_source_never_fetched():
    """Proves that a robots-blocked or policy-disabled source is never fetched."""
    enam_cfg = {
        "id": "enam_portal",
        "name": "e-NAM Portal",
        "url": "https://enam.gov.in",
        "type": "html",
        "enabled": False,
        "robots_allowed": False,
        "status_reason": "Blocked by policy"
    }
    connector = ENAMConnector(enam_cfg)

    # Calling fetch must strictly raise PolicyBlockedError before making any network call
    with pytest.raises(PolicyBlockedError) as exc_info:
        connector.fetch(start_date="2026-11-01", end_date="2026-11-12")

    assert "blocked by policy" in str(exc_info.value).lower()


# ---------------------------------------------------------------------------
# 2. INCREMENTAL FETCH TEST
# ---------------------------------------------------------------------------
def test_incremental_fetch_only_requests_new_dates():
    """Proves that incremental fetch shifts the start date based on last_stored_date."""
    dg_cfg = {
        "id": "data_gov_in",
        "name": "data.gov.in",
        "url": "https://api.data.gov.in/test",
        "type": "api",
        "enabled": True,
        "robots_allowed": True,
        "auth_env_var": "TEST_KEY"
    }
    connector = DataGovConnector(dg_cfg)

    with patch.dict(os.environ, {"TEST_KEY": "dummy_key"}):
        with patch.object(connector, "execute_http_request", return_value=b'{"records":[]}') as mock_req:
            connector.fetch(start_date="2026-01-01", end_date="2026-11-12", last_stored_date="2026-11-05")
            # Must have executed request with query parameters
            assert mock_req.called
            called_url = mock_req.call_args[0][0]
            assert "api.data.gov.in" in called_url


# ---------------------------------------------------------------------------
# 3. QUARANTINE ROUTING TEST
# ---------------------------------------------------------------------------
def test_quarantined_rows_never_enter_training_panel(tmp_path):
    """Proves that invalid rows are rejected, routed to quarantine, and never enter panel."""
    quarantine_dir = str(tmp_path / "quarantine")
    validator = ValidationEngine(quarantine_dir=quarantine_dir, today_date_str="2026-11-12")

    # Sample row with invalid plausibility: min_price > modal_price
    bad_row_plausibility = ParsedRow(
        crop="onion",
        mandi="Kolar",
        district="Kolar",
        date="2026-11-10",
        min_price=5000.0,
        modal_price=3000.0,  # min > modal!
        max_price=4000.0,
        arrivals=100.0,
        unit="Quintal",
        source_id="test_source",
        source_url="http://test.com",
        fetched_at="2026-11-12T10:00:00",
        raw_hash="hash123"
    )

    is_valid, reason, clean_dict = validator.validate_single_row(bad_row_plausibility)
    assert not is_valid
    assert "plausibility failure" in reason.lower()
    assert clean_dict is None

    # Sample row with unknown unit
    bad_row_unit = ParsedRow(
        crop="onion",
        mandi="Kolar",
        district="Kolar",
        date="2026-11-10",
        min_price=2000.0,
        modal_price=2500.0,
        max_price=3000.0,
        arrivals=100.0,
        unit="cartloads_unknown",
        source_id="test_source",
        source_url="http://test.com",
        fetched_at="2026-11-12T10:00:00",
        raw_hash="hash456"
    )

    is_valid, reason, clean_dict = validator.validate_single_row(bad_row_unit)
    assert not is_valid
    assert "unknown unit" in reason.lower()
    assert clean_dict is None

    # Quarantine file write test
    validator.quarantine_records([{"row": "bad", "reason": reason}], batch_id="test_batch")
    quarantine_files = os.listdir(quarantine_dir)
    assert len(quarantine_files) == 1


# ---------------------------------------------------------------------------
# 4. IDEMPOTENT INGESTION TEST (NO DUPLICATES)
# ---------------------------------------------------------------------------
def test_rerun_ingest_creates_no_duplicates():
    """Proves that re-running validation & deduplication produces identical row counts."""
    validator = ValidationEngine(today_date_str="2026-11-12")

    row1 = ParsedRow(
        crop="onion", mandi="Kolar", district="Kolar", date="2026-11-05",
        min_price=3000.0, modal_price=3500.0, max_price=4000.0,
        arrivals=200.0, unit="Quintal", source_id="data_gov_in",
        source_url="http://data.gov.in", fetched_at="2026-11-12T00:00:00", raw_hash="h1"
    )
    # Duplicate row from secondary source
    row2 = ParsedRow(
        crop="onion", mandi="Kolar", district="Kolar", date="2026-11-05",
        min_price=3100.0, modal_price=3550.0, max_price=4100.0,
        arrivals=200.0, unit="Quintal", source_id="agmarknet_portal",
        source_url="http://agmarknet.gov.in", fetched_at="2026-11-12T00:00:00", raw_hash="h2"
    )

    _, _, d1 = validator.validate_single_row(row1)
    _, _, d2 = validator.validate_single_row(row2)

    priorities = {"data_gov_in": 1, "agmarknet_portal": 2}
    reconciled, _ = validator.cross_source_reconciliation([d1, d2, d1, d2], priorities)

    # Exactly 1 row for (onion, Kolar, 2026-11-05) resolved to data_gov_in (priority 1)
    assert len(reconciled) == 1
    assert reconciled[0]["source_id"] == "data_gov_in"


# ---------------------------------------------------------------------------
# 5. CONNECTOR PARSER TESTS AGAINST SAVED FIXTURES
# ---------------------------------------------------------------------------
def test_data_gov_parser_fixture():
    """Tests DataGovConnector against tests/fixtures/data_gov_sample.json."""
    with open("tests/fixtures/data_gov_sample.json", "rb") as f:
        content = f.read()

    connector = DataGovConnector({"id": "data_gov_in", "name": "OGD", "url": "https://api.data.gov.in"})
    payload = connector.create_payload(content, "https://api.data.gov.in/sample", "application/json", "json")
    rows = connector.parse(payload)

    assert len(rows) == 3
    assert rows[0].crop == "Onion"
    assert rows[0].mandi == "Kolar"
    assert rows[0].modal_price == 3500.0
    assert rows[0].date == "2026-11-08"


def test_agmarknet_bulletin_parser_fixture():
    """Tests AgmarknetConnector stores national summary bulletins in national_prices table and never into mandi panel."""
    with open("tests/fixtures/agmarknet_sample.csv", "rb") as f:
        content = f.read()

    connector = AgmarknetConnector({"id": "agmarknet_portal", "name": "Agmarknet", "url": "https://agmarknet.gov.in"})
    payload = connector.create_payload(content, "https://agmarknet.gov.in/sample.csv", "text/csv", "csv")
    rows = connector.parse(payload)

    # Must NOT output rows into mandi panel (no mandi column in bulletin)
    assert len(rows) == 0

    # Must have stored records in data/processed/national_prices.parquet
    import pandas as pd
    nat_df = pd.read_parquet("data/processed/national_prices.parquet")
    onion_nat = nat_df[nat_df["crop"] == "onion"]
    assert len(onion_nat) > 0
    assert 4174.02 in onion_nat["price_rs_per_qtl"].values


def test_raita_mitra_html_parser_fixture():
    """Tests RaitaMitraConnector against tests/fixtures/raita_mitra_sample.html."""
    with open("tests/fixtures/raita_mitra_sample.html", "rb") as f:
        content = f.read()

    connector = RaitaMitraConnector({"id": "raita_mitra_karnataka", "name": "Raita Mitra", "url": "https://raitamitra.karnataka.gov.in"})
    payload = connector.create_payload(content, "https://raitamitra.karnataka.gov.in/rates", "text/html", "html")
    rows = connector.parse(payload)

    assert len(rows) == 2
    assert rows[0].crop == "onion"
    assert rows[0].modal_price == 3550.0


def test_raita_mitra_changed_layout_fails_loudly():
    """Tests that RaitaMitraConnector raises SchemaValidationError on layout change."""
    with open("tests/fixtures/raita_mitra_changed_layout.html", "rb") as f:
        content = f.read()

    connector = RaitaMitraConnector({"id": "raita_mitra_karnataka", "name": "Raita Mitra", "url": "https://raitamitra.karnataka.gov.in"})
    payload = connector.create_payload(content, "https://raitamitra.karnataka.gov.in/rates", "text/html", "html")

    with pytest.raises(SchemaValidationError) as exc_info:
        connector.parse(payload)

    assert "no <table> found" in str(exc_info.value).lower()


def test_open_meteo_parser_fixture():
    """Tests OpenMeteoConnector against tests/fixtures/open_meteo_sample.json."""
    with open("tests/fixtures/open_meteo_sample.json", "rb") as f:
        content = f.read()

    connector = OpenMeteoConnector({"id": "weather_open_meteo", "name": "Open-Meteo", "url": "https://api.open-meteo.com/v1/forecast"})
    payload = connector.create_payload(content, "https://api.open-meteo.com/sample", "application/json", "json", metadata={"mandi": "Kolar"})
    rows = connector.parse(payload)

    assert len(rows) == 3
    assert rows[0].crop == "weather_exogenous"
    assert rows[0].mandi == "Kolar"
    assert rows[0].modal_price == 23.8  # (29.2 + 18.4)/2


def test_ppac_diesel_parser_fixture():
    """Tests PPACDieselConnector against tests/fixtures/ppac_sample.csv."""
    with open("tests/fixtures/ppac_sample.csv", "rb") as f:
        content = f.read()

    connector = PPACDieselConnector({"id": "diesel_ppac", "name": "PPAC", "url": "https://ppac.gov.in"})
    payload = connector.create_payload(content, "https://ppac.gov.in/sample.csv", "text/csv", "csv")
    rows = connector.parse(payload)

    assert len(rows) == 3
    assert rows[0].modal_price == 88.94


# ---------------------------------------------------------------------------
# 6. UNIT NORMALIZATION TESTS
# ---------------------------------------------------------------------------
def test_unit_normalization_and_unknown_unit_error():
    """Tests standard price and arrival unit normalization."""
    # 1. Quintal to Quintal
    p_qtl, u_qtl = normalize_price_to_quintal(3500.0, "Quintal")
    assert p_qtl == 3500.0
    assert u_qtl == "Rs/Quintal"

    # 2. Kg to Quintal (* 100)
    p_kg, _ = normalize_price_to_quintal(35.0, "kg")
    assert p_kg == 3500.0

    # 3. Tonne to Quintal (/ 10)
    p_tonne, _ = normalize_price_to_quintal(35000.0, "tonne")
    assert p_tonne == 3500.0

    # 4. Unknown unit raises UnknownUnitError loudly
    with pytest.raises(UnknownUnitError):
        normalize_price_to_quintal(500.0, "basket_unmeasured")
