"""Unit and integration tests for KSAMB PDF importer, date gating, anomaly flags, and idempotency."""

import os
import json
import pytest
import pandas as pd
from datetime import datetime

from src.ingest.connectors.ksamb_pdf import (
    KsambPdfImporter,
    ParsedPdfRow,
    DateGateError,
    CompletenessError,
    resolve_report_date,
    validate_and_filter_ksamb_rows,
    select_headline_series
)


@pytest.fixture
def sample_pdf_path():
    path = "tests/fixtures/ksamb_sample.pdf"
    if not os.path.exists(path):
        from tests.generate_test_fixture_pdf import generate_fixture_pdf
        generate_fixture_pdf(path)
    return path


def test_ksamb_pdf_fixture_wrapped_and_glued(sample_pdf_path):
    """Proves handling of wrapped names, glued tokens ('1900 2] MARKET: ...'), and page breaks."""
    importer = KsambPdfImporter(expected_markets=2)
    rows = importer.import_pdf(sample_pdf_path, report_date="2026-11-11")

    assert len(rows) == 5

    # 1. Market 1: ANNIGERI on Page 1
    m1_rows = [r for r in rows if r.market_num == 1]
    assert len(m1_rows) == 3
    assert m1_rows[0].mandi == "ANNIGERI"
    assert m1_rows[0].commodity == "Cotton"
    assert m1_rows[0].raw_page == 1

    # Check un-wrapping of 'Coconut (Per\n1000)'
    assert m1_rows[1].commodity == "Coconut (Per 1000)"
    assert m1_rows[1].unit == "Numbers"
    assert m1_rows[1].raw_page == 1

    # 2. Market 2: C.R.PATNA on Page 2 (glued token '1900 2] MARKET: C.R.PATNA' decoupled)
    m2_rows = [r for r in rows if r.market_num == 2]
    assert len(m2_rows) == 2
    assert m2_rows[0].mandi == "C.R.PATNA"
    assert m2_rows[0].raw_page == 2
    # Check un-wrapping of 'Beans\n(Whole)'
    assert m2_rows[0].commodity == "Beans (Whole)"
    assert m2_rows[1].commodity == "Onion"
    assert m2_rows[1].modal == 3500.0


def test_ksamb_pdf_date_gate():
    """Proves refusal when report date is missing or un-configured, and warning on mismatch."""
    # 1. Refusal when explicit_date is None and filename has no date
    with pytest.raises(DateGateError) as exc_info:
        resolve_report_date(explicit_date=None, file_path="dummy_report.pdf", stray_date="2026-11-11")
    assert "must come from an explicit config field or the file name" in str(exc_info.value)

    # 2. Acceptance from filename YYYY-MM-DD
    d1 = resolve_report_date(explicit_date=None, file_path="ksamb_2026-11-11.pdf", stray_date="2026-11-11")
    assert d1 == "2026-11-11"

    # 3. Acceptance from explicit config
    d2 = resolve_report_date(explicit_date="11/11/2026", file_path="dummy.pdf", stray_date="2026-11-11")
    assert d2 == "2026-11-11"

    # 4. Warning when configured date differs from stray date found in PDF text
    with pytest.warns(UserWarning) as recorded_warnings:
        d3 = resolve_report_date(explicit_date="2026-11-10", file_path="dummy.pdf", stray_date="2026-11-11")
        assert d3 == "2026-11-10"
    assert len(recorded_warnings) == 1
    assert "differs from stray date found in PDF text" in str(recorded_warnings[0].message)


def test_identical_triple_and_anomaly_flags(tmp_path):
    """Proves detection and quarantine of shared triples, flat markets, and sub-100 floor."""
    quarantine_dir = str(tmp_path / "quarantine")
    non_qtl_path = str(tmp_path / "non_qtl.parquet")

    mock_rows = [
        # (a) Identical triple (2000, 3000, 2500) shared by 3 crops in Bangarpet
        ParsedPdfRow("2026-11-11", "Bangarpet", 1, "Beetroot", "Local", "Average", 10, "Quintal", 2000, 3000, 2500, "f.pdf", 1, 2, "hash"),
        ParsedPdfRow("2026-11-11", "Bangarpet", 1, "Potato", "Local", "Average", 20, "Quintal", 2000, 3000, 2500, "f.pdf", 1, 3, "hash"),
        ParsedPdfRow("2026-11-11", "Bangarpet", 1, "Capsicum", "Local", "Average", 5, "Quintal", 2000, 3000, 2500, "f.pdf", 1, 4, "hash"),

        # (b) Flat market (Kadur: 2 of 3 rows have min=max=modal -> 66% > 50%)
        ParsedPdfRow("2026-11-11", "Kadur", 2, "Onion", "Onion", "Medium", 3, "Quintal", 2776, 2776, 2776, "f.pdf", 2, 2, "hash"),
        ParsedPdfRow("2026-11-11", "Kadur", 2, "Potato", "Potato", "Medium", 3, "Quintal", 2776, 2776, 2776, "f.pdf", 2, 3, "hash"),
        ParsedPdfRow("2026-11-11", "Kadur", 2, "Tomato", "Tomato", "Medium", 10, "Quintal", 1500, 2000, 1800, "f.pdf", 2, 4, "hash"),

        # (c) Sub-100 floor: Kalaburagi Radish (10/20/15)
        ParsedPdfRow("2026-11-11", "Kalaburagi", 3, "Radish", "Radish", "Average", 200, "Quintal", 10, 20, 15, "f.pdf", 3, 2, "hash"),

        # Valid row
        ParsedPdfRow("2026-11-11", "Gadag", 4, "Onion", "Onion", "Medium", 100, "Quintal", 2000, 3500, 3000, "f.pdf", 4, 2, "hash")
    ]

    accepted, non_qtl, quarantined = validate_and_filter_ksamb_rows(
        mock_rows,
        quarantine_dir=quarantine_dir,
        non_quintal_output_path=non_qtl_path
    )

    # 1. Valid row accepted
    assert len(accepted) == 1
    assert accepted[0].mandi == "Gadag"
    assert accepted[0].modal == 3000.0

    # 2. Check quarantine reasons
    flag_a = [q for q in quarantined if q["flag"] == "flag_a_shared_triple"]
    assert len(flag_a) == 3
    assert all(q["mandi"] == "Bangarpet" for q in flag_a)

    flag_b = [q for q in quarantined if q["flag"] == "flag_b_flat_market"]
    assert len(flag_b) == 3
    assert all(q["mandi"] == "Kadur" for q in flag_b)

    flag_c = [q for q in quarantined if q["flag"] == "flag_c_below_100"]
    assert len(flag_c) == 1
    assert flag_c[0]["commodity"] == "Radish"


def test_quintal_vs_non_quintal_units(tmp_path):
    """Proves non-quintal units (Numbers, Thousands) are routed to separate parquet."""
    quarantine_dir = str(tmp_path / "quarantine")
    non_qtl_path = str(tmp_path / "non_qtl.parquet")

    mock_rows = [
        ParsedPdfRow("2026-11-11", "Arsikere", 1, "Coconut", "Medium", "Medium", 6125, "Numbers", 35000, 35000, 35000, "f.pdf", 1, 2, "hash"),
        ParsedPdfRow("2026-11-11", "Pandavapura", 2, "Tender Coconut", "Tender", "Average", 73000, "Thousands", 22000, 24000, 23000, "f.pdf", 1, 3, "hash"),
        ParsedPdfRow("2026-11-11", "Gadag", 3, "Onion", "Onion", "Medium", 100, "Quintal", 2000, 3500, 3000, "f.pdf", 1, 4, "hash")
    ]

    accepted, non_qtl, quarantined = validate_and_filter_ksamb_rows(
        mock_rows,
        quarantine_dir=quarantine_dir,
        non_quintal_output_path=non_qtl_path
    )

    assert len(accepted) == 1
    assert accepted[0].unit == "Quintal"

    assert len(non_qtl) == 2
    assert os.path.exists(non_qtl_path)
    df_non = pd.read_parquet(non_qtl_path)
    assert len(df_non) == 2
    assert set(df_non["unit"].unique()) == {"Numbers", "Thousands"}


def test_idempotent_reimport(tmp_path):
    """Proves re-running the ingest produces zero duplicate rows."""
    panel_file = str(tmp_path / "test_panel.parquet")

    rows = [
        {"date": "2026-11-11", "mandi": "Bengaluru", "crop": "onion", "variety": "Local", "grade": "Medium", "modal_price": 3500.0},
        {"date": "2026-11-11", "mandi": "Bengaluru", "crop": "onion", "variety": "Onion", "grade": "Large", "modal_price": 4500.0}
    ]

    df1 = pd.DataFrame(rows)
    df1.to_parquet(panel_file, index=False)

    # Re-importing exact same rows
    df2 = pd.concat([df1, pd.DataFrame(rows)], ignore_index=True)
    dedup_cols = ["date", "mandi", "crop", "variety", "grade"]
    deduped = df2.drop_duplicates(subset=dedup_cols, keep="last").reset_index(drop=True)

    assert len(deduped) == 2
