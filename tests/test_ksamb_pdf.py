"""Unit and integration tests for KSAMB PDF importer, golden fixture parity,
page-break carry-over, missed-row recovery, flag rules, idempotency, and unit separation.
"""

import os
import json
import pytest
import pandas as pd
import numpy as np

from src.ingest.connectors.ksamb_pdf import (
    KsambPdfImporter,
    DateGateError,
    CompletenessError,
    extract_report_date_from_title,
    validate_and_route_ksamb_data
)


@pytest.fixture
def golden_csv_path():
    path = "data/raw/user_download/karnataka_mandi_prices_2026-11-11.csv"
    assert os.path.exists(path), f"Golden fixture CSV not found at {path}"
    return path


@pytest.fixture
def pdf_path():
    path = "Crop_price_of_all_mandies_of_karnataka.pdf"
    assert os.path.exists(path), f"Raw KSAMB PDF not found at {path}"
    return path


def test_golden_fixture_match(pdf_path, golden_csv_path):
    """Task 1 & 9: Importer output for this PDF must equal golden CSV row for row."""
    importer = KsambPdfImporter()
    df_parsed = importer.parse_pdf(pdf_path)
    golden_df = pd.read_csv(golden_csv_path)

    assert len(df_parsed) == len(golden_df) == 752
    assert list(df_parsed.columns) == list(golden_df.columns)

    # Assert row-for-row equality across all columns
    pd.testing.assert_frame_equal(df_parsed, golden_df, check_dtype=False)


def test_title_date_gate(pdf_path):
    """Task 1 & 9: Report date comes from PDF's first-page title ('For DD/MM/YYYY') and refuses file without one."""
    import pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        report_date = extract_report_date_from_title(pdf, file_path=pdf_path)
        assert report_date == "2026-11-11"

    # Create dummy PDF without date title
    import reportlab.lib.pagesizes as ps
    from reportlab.pdfgen import canvas
    dummy_pdf_path = "tests/fixtures/dummy_no_date.pdf"
    os.makedirs("tests/fixtures", exist_ok=True)
    c = canvas.Canvas(dummy_pdf_path, pagesize=ps.A4)
    c.drawString(100, 750, "Random Title Without Date")
    c.save()

    with pdfplumber.open(dummy_pdf_path) as pdf:
        with pytest.raises(DateGateError) as exc_info:
            extract_report_date_from_title(pdf, file_path=dummy_pdf_path)
        assert "Missing report date in first-page title" in str(exc_info.value)

    if os.path.exists(dummy_pdf_path):
        os.remove(dummy_pdf_path)


def test_page_break_header_carryover(pdf_path):
    """Task 1 & 9: Header at bottom of page owns the first table on the next page."""
    importer = KsambPdfImporter()
    df = importer.parse_pdf(pdf_path)

    # Check Chikkamagaluru (Market 23): header on page 10, table on page 11
    chik = df[df['mandi'] == 'CHIKKAMAGALURU']
    assert not chik.empty
    assert (chik['source_page'] == 11).all()
    assert chik['market_no'].iloc[0] == 23

    # Check Doddaballapur (Market 29): header on page 13, table on page 14
    dodda = df[df['mandi'] == 'DODDABALLAPUR']
    assert not dodda.empty
    assert (dodda['source_page'] == 14).all()
    assert dodda['market_no'].iloc[0] == 29

    # Check Kollegal (Market 61): header on page 23, table continuation on page 24
    koll = df[df['mandi'] == 'KOLLEGAL']
    assert not koll.empty
    assert (koll['source_page'] == 24).all()


def test_missed_row_recovery(pdf_path):
    """Task 1 & 9: Missed row without bounding box on page 32 is recovered from text pass and flagged."""
    importer = KsambPdfImporter()
    df = importer.parse_pdf(pdf_path)

    rec_rows = df[df['flags'].fillna('').str.contains('recovered_from_text_line')]
    assert len(rec_rows) == 1
    rec = rec_rows.iloc[0]

    assert rec['mandi'] == 'SHIVAMOGGA'
    assert rec['commodity'] == 'Onion'
    assert rec['modal_price'] == 4500
    assert rec['arrivals'] == 50
    assert rec['source_page'] == 32
    assert pd.isna(rec['table_row'])


def test_flag_rules(golden_csv_path):
    """Task 2 & 9: Proves validation and flagging rules match expected anomaly flags."""
    df = pd.read_csv(golden_csv_path)

    # 1. same_price_triple_3plus_crops: exactly 50 rows
    flag_triple = df[df['flags'].fillna('').str.contains('same_price_triple_3plus_crops')]
    assert len(flag_triple) == 50

    # 2. min_eq_max_eq_modal_most_rows: exactly 25 rows (CHIKKAMAGALURU and KADUR)
    flag_flat = df[df['flags'].fillna('').str.contains('min_eq_max_eq_modal_most_rows')]
    assert len(flag_flat) == 25
    assert set(flag_flat['mandi'].unique()) == {'CHIKKAMAGALURU', 'KADUR'}

    # 3. price_below_100_per_qtl: exactly 1 row (Kalaburagi Radish)
    flag_100 = df[df['flags'].fillna('').str.contains('price_below_100_per_qtl')]
    assert len(flag_100) == 1
    assert flag_100.iloc[0]['mandi'] == 'KALABURAGI'
    assert flag_100.iloc[0]['commodity'] == 'Raddish'

    # 4. non_quintal_unit: exactly 27 rows
    flag_non_q = df[df['flags'].fillna('').str.contains('non_quintal_unit')]
    assert len(flag_non_q) == 27
    assert set(flag_non_q['unit'].unique()) == {'Numbers', 'Thousands'}


def test_unit_separation_and_quarantine(golden_csv_path, tmp_path):
    """Task 2 & 9: Non-quintal units separated to parquet; flagged rows to quarantine."""
    df = pd.read_csv(golden_csv_path)
    q_dir = str(tmp_path / "quarantine")
    non_q_file = str(tmp_path / "non_quintal.parquet")

    accepted, non_q, quar = validate_and_route_ksamb_data(
        df,
        quarantine_dir=q_dir,
        non_quintal_output_path=non_q_file
    )

    assert len(accepted) == 653
    assert len(non_q) == 27
    assert len(quar) == 99

    assert os.path.exists(non_q_file)
    non_q_df = pd.read_parquet(non_q_file)
    assert len(non_q_df) == 27
    assert (non_q_df['unit'] != 'Quintal').all()

    # Verify quarantine file
    q_files = [f for f in os.listdir(q_dir) if f.endswith('.json')]
    assert len(q_files) == 1
    with open(os.path.join(q_dir, q_files[0]), 'r') as f:
        q_data = json.load(f)
    assert len(q_data) == 99
    assert all('rejection_reason' in item for item in q_data)


def test_idempotent_reimport(tmp_path):
    """Task 3 & 9: Re-running ingest produces zero duplicate rows using idempotent key."""
    from scripts.ingest_ksamb_panel import ingest_ksamb_to_panel

    panel_path = str(tmp_path / "panel.parquet")
    csv_path = "data/raw/user_download/karnataka_mandi_prices_2026-11-11.csv"

    # Ingest pass 1
    p1 = ingest_ksamb_to_panel(csv_path, panel_path=panel_path)
    assert len(p1) == 653

    # Ingest pass 2 (re-import exact same data)
    p2 = ingest_ksamb_to_panel(csv_path, panel_path=panel_path)
    assert len(p2) == 653

    # Verify zero duplicates on idempotent key (date, mandi, crop, variety, grade)
    idemp_cols = ['date', 'mandi', 'crop', 'variety', 'grade']
    dups = p2.duplicated(subset=idemp_cols).sum()
    assert dups == 0
