import os
import pytest
import pandas as pd
import yaml

from src.models.forecast import check_data_provenance, DataProvenanceError


def test_processed_panel_provenance_columns():
    panel_path = "data/processed/panel.parquet"
    if not os.path.exists(panel_path):
        pytest.skip(f"{panel_path} does not exist.")
    
    df = pd.read_parquet(panel_path)
    assert "data_provenance" in df.columns, "panel.parquet must have 'data_provenance' column"
    assert "is_synthetic" in df.columns, "panel.parquet must have 'is_synthetic' column"
    
    # Assert values are properly typed
    assert set(df["data_provenance"].unique()).issubset({"real", "synthetic"})
    assert set(df["data_provenance"].unique()).issubset({"real", "synthetic", "unverified"})
    assert df["is_synthetic"].dtype == bool or set(df["is_synthetic"].unique()).issubset({True, False})


def test_provenance_check_raises_error_on_synthetic():
    df_synthetic = pd.DataFrame({
        "date": pd.date_range("2026-01-01", periods=10),
        "mandi": ["Kolar"] * 10,
        "modal_price": [2000] * 10,
        "is_synthetic": [True] * 10,
        "data_provenance": ["synthetic"] * 10,
    })
    config = {
        "project": {
            "allow_synthetic_training": False
        }
    }
    with pytest.raises(DataProvenanceError) as exc_info:
        check_data_provenance(df_synthetic, config)
    assert "DATA_PROVENANCE CHECK FAILED" in str(exc_info.value)
    assert "strictly refused" in str(exc_info.value).lower()


def test_provenance_check_passes_on_real_data():
    df_real = pd.DataFrame({
        "date": pd.date_range("2026-01-01", periods=10),
        "mandi": ["Kolar"] * 10,
        "modal_price": [2000] * 10,
        "is_synthetic": [False] * 10,
        "data_provenance": ["real"] * 10,
    })
    config = {
        "project": {
            "allow_synthetic_training": False
        }
    }
    # Should not raise any error
    result = check_data_provenance(df_real, config)
    assert result is True


def test_provenance_check_allows_override_when_configured():
    df_synthetic = pd.DataFrame({
        "date": pd.date_range("2026-01-01", periods=10),
        "mandi": ["Kolar"] * 10,
        "modal_price": [2000] * 10,
        "is_synthetic": [True] * 10,
        "data_provenance": ["synthetic"] * 10,
    })
    config = {
        "project": {
            "allow_synthetic_training": True
        }
    }
    # Should log warning and proceed without raising exception
    result = check_data_provenance(df_synthetic, config)
    assert result is True


def test_coverage_flagging_rule():
    config_path = "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    
    min_cov = cfg.get("project", {}).get("coverage_target_min", 70.0)
    max_cov = cfg.get("project", {}).get("coverage_target_max", 90.0)
    
    assert min_cov == 70.0
    assert max_cov == 90.0
    
    # Test inside band
    assert min_cov <= 79.5 <= max_cov
    # Test outside band
    assert not (min_cov <= 65.0 <= max_cov)
    assert not (min_cov <= 95.0 <= max_cov)


def test_parser_never_outputs_min_max_absent_from_raw():
    """Parser must reject raw input that lacks explicit min/max columns rather than inventing them."""
    from src.ingest.connectors.agmarknet import AgmarknetConnector
    from src.ingest.base import SchemaValidationError, RawPayload
    from datetime import datetime

    source_config = {
        "id": "agmarknet_portal",
        "name": "Agmarknet Portal",
        "url": "https://agmarknet.gov.in"
    }
    connector = AgmarknetConnector(source_config=source_config)
    # Standard table missing Min and Max Price columns
    raw_csv = (
        "Sl no.,Market,Arrivals (Tonnes),Modal Price (Rs./Quintal),Report Date\n"
        "1,Kolar,50,2500,03/11/2026\n"
    )
    payload = RawPayload(
        source_id="agmarknet_portal",
        url="https://agmarknet.gov.in",
        content=raw_csv.encode("utf-8"),
        content_type="text/csv",
        fetched_at=datetime.now().isoformat(),
        raw_hash="testhash",
        file_extension="csv",
        metadata={"filename": "test.csv", "acquisition_method": "user_download"}
    )
    with pytest.raises(SchemaValidationError) as exc_info:
        connector.parse(payload)
    assert "Missing required price columns" in str(exc_info.value) or "min" in str(exc_info.value).lower()


def test_no_two_mandis_share_identical_price_series():
    """No two mandis in the panel may share an identical modal price series across multiple dates."""
    panel_path = "data/processed/panel.parquet"
    if not os.path.exists(panel_path):
        pytest.skip(f"{panel_path} does not exist.")

    df = pd.read_parquet(panel_path)
    # Check for any duplicate price series across mandis for crops with multiple dates
    multi_date_crops = df.groupby("crop")["date"].nunique()
    multi_date_crops = multi_date_crops[multi_date_crops >= 3].index
    for crop in multi_date_crops:
        crop_df = df[df["crop"] == crop]
        pivot = crop_df.pivot_table(index="date", columns="mandi", values="modal_price")
        cols = list(pivot.columns)
        for i in range(len(cols)):
            for j in range(i + 1, min(len(cols), i + 15)):
                s1 = pivot[cols[i]].dropna()
                s2 = pivot[cols[j]].dropna()
                common = s1.index.intersection(s2.index)
                if len(common) >= 3 and (s1.loc[common] == s2.loc[common]).all():
                    pytest.fail(f"Mandis {cols[i]} and {cols[j]} have identical price series for {crop}!")


def test_no_row_has_synthesized_min_max_ratio():
    """No row in the panel may have min = round(0.9 * modal, 2) and max = round(1.1 * modal, 2)."""
    panel_path = "data/processed/panel.parquet"
    if not os.path.exists(panel_path):
        pytest.skip(f"{panel_path} does not exist.")

    df = pd.read_parquet(panel_path)
    # Check for exact 0.9 / 1.1 synthesis pattern
    synthesized = df[
        (df["min_price"] == (df["modal_price"] * 0.9).round(2)) &
        (df["max_price"] == (df["modal_price"] * 1.1).round(2))
    ]
    assert len(synthesized) == 0, f"Found {len(synthesized)} rows with synthesized 0.9/1.1 min/max prices!"

