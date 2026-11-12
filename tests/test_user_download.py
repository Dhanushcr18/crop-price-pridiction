"""Unit tests for the manual Agmarknet/KSAMB user download importer."""

import os
import csv
import pytest
from datetime import datetime

from src.ingest.connectors.user_download import UserDownloadImporter, UserDownloadConnector
from src.ingest.base import SchemaValidationError


@pytest.fixture
def importer(tmp_path):
    quarantine_dir = str(tmp_path / "quarantine")
    return UserDownloadImporter(
        raw_dir="tests/fixtures/user_download",
        quarantine_dir=quarantine_dir,
        today_date_str="2026-11-12"
    )


def test_user_download_importer_accepts_valid_file(importer):
    fixture_path = "tests/fixtures/user_download/valid_karnataka_agmarknet.csv"
    res = importer.import_file(fixture_path)

    assert res["status"] == "success"
    assert res["accepted_count"] == 3
    assert res["quarantined_count"] == 0

    accepted = res["accepted_rows"]
    expected_mandis = ["kolar", "chikkaballapur", "bangalore"]

    for idx, r in enumerate(accepted):
        # 1. Provenance & traceability fields
        assert r["acquisition_method"] == "user_download"
        assert r["data_provenance"] == "real"
        assert r["is_synthetic"] is False
        assert "valid_karnataka_agmarknet.csv" in r["raw_file"]
        assert r["raw_line"] == idx + 2  # header is line 1, data starts at line 2

        # 2. Field correctness
        assert r["mandi"].lower() == expected_mandis[idx]
        assert r["crop"] == "onion"
        assert r["date"] == "2026-11-04"
        assert r["min_price"] <= r["modal_price"] <= r["max_price"]
        assert r["modal_price"] > 0


def test_user_download_importer_rejects_missing_columns(importer):
    # Test missing min price
    missing_min_path = "tests/fixtures/user_download/invalid_missing_min.csv"
    with pytest.raises(SchemaValidationError) as exc_info:
        importer.import_file(missing_min_path)
    assert "missing required columns" in str(exc_info.value).lower()
    assert "min" in str(exc_info.value).lower()

    # Test missing market / mandi
    missing_mandi_path = "tests/fixtures/user_download/invalid_missing_mandi.csv"
    with pytest.raises(SchemaValidationError) as exc_info:
        importer.import_file(missing_mandi_path)
    assert "missing required columns" in str(exc_info.value).lower()
    assert "mandi" in str(exc_info.value).lower()


def test_user_download_importer_quarantines_invalid_rows(importer):
    fixture_path = "tests/fixtures/user_download/sample_with_quarantine_rows.csv"
    res = importer.import_file(fixture_path)

    assert res["status"] == "success"
    assert res["accepted_count"] == 2
    assert res["quarantined_count"] == 3

    quarantined = res["quarantined_rows"]

    # Line 3: min (3100) > modal (2500)
    q_line3 = [q for q in quarantined if q["raw_line"] == 3][0]
    assert "min_price (3100.0) > modal_price (2500.0)" in q_line3["rejection_reason"]

    # Line 4: future date (2026-11-28 > 2026-11-12)
    q_line4 = [q for q in quarantined if q["raw_line"] == 4][0]
    assert "future" in q_line4["rejection_reason"].lower()

    # Line 5: synthesized 0.9/1.1 ratio (1800, 2000, 2200)
    q_line5 = [q for q in quarantined if q["raw_line"] == 5][0]
    assert "synthesized" in q_line5["rejection_reason"].lower()

    # Check quarantine file was written to disk
    quarantine_files = os.listdir(importer.quarantine_dir)
    assert len(quarantine_files) > 0
    assert any("user_download" in f for f in quarantine_files)


def test_audit_trace_compatibility_on_user_download(importer):
    fixture_path = "tests/fixtures/user_download/valid_karnataka_agmarknet.csv"
    res = importer.import_file(fixture_path)

    # Read raw lines directly
    with open(fixture_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for r in res["accepted_rows"]:
        line_idx = r["raw_line"] - 1
        raw_text = lines[line_idx]
        assert r["mandi"].lower() in raw_text.lower()
        assert str(int(r["modal_price"])) in raw_text
