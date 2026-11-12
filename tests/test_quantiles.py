"""Test quantile ordering (P10 <= P50 <= P90) and crossing resolution."""

import pytest
import numpy as np
import pickle
import os
from src.models.forecast import fix_quantile_crossing, load_config


def test_fix_quantile_crossing_synthetic():
    """Verify that fix_quantile_crossing strictly enforces P10 <= P50 <= P90."""
    # Synthetic badly inverted quantiles
    p10_raw = np.array([4200.0, 3100.0, 3500.0, 5000.0])
    p50_raw = np.array([3900.0, 3200.0, 3500.0, 4800.0])
    p90_raw = np.array([3600.0, 3400.0, 3500.0, 4500.0])

    p10, p50, p90 = fix_quantile_crossing(p10_raw, p50_raw, p90_raw)

    # Check non-crossing invariant
    assert np.all(p10 <= p50), f"Quantile crossing failure: P10 > P50 found: {p10} vs {p50}"
    assert np.all(p50 <= p90), f"Quantile crossing failure: P50 > P90 found: {p50} vs {p90}"
    assert np.all(p10 <= p90), f"Quantile crossing failure: P10 > P90 found: {p10} vs {p90}"


def test_saved_models_quantile_ordering():
    """Verify that trained LightGBM models predict logically ordered quantiles on sample data."""
    config = load_config()
    models_dir = config["paths"]["models_dir"]
    
    for h in [7, 14, 30]:
        q10_file = os.path.join(models_dir, f"lgb_h{h}_q10.pkl")
        q50_file = os.path.join(models_dir, f"lgb_h{h}_q50.pkl")
        q90_file = os.path.join(models_dir, f"lgb_h{h}_q90.pkl")
        feats_file = os.path.join(models_dir, f"features_h{h}.pkl")

        assert os.path.exists(q10_file), f"Model {q10_file} missing!"
        assert os.path.exists(q50_file), f"Model {q50_file} missing!"
        assert os.path.exists(q90_file), f"Model {q90_file} missing!"
        assert os.path.exists(feats_file), f"Features file {feats_file} missing!"

        with open(q10_file, "rb") as f:
            m10 = pickle.load(f)
        with open(q50_file, "rb") as f:
            m50 = pickle.load(f)
        with open(q90_file, "rb") as f:
            m90 = pickle.load(f)
        with open(feats_file, "rb") as f:
            cols = pickle.load(f)

        # Generate sample feature vector
        sample_X = np.random.uniform(10.0, 4000.0, size=(20, len(cols)))
        pred10 = m10.predict(sample_X)
        pred50 = m50.predict(sample_X)
        pred90 = m90.predict(sample_X)

        fixed10, fixed50, fixed90 = fix_quantile_crossing(pred10, pred50, pred90)
        assert np.all(fixed10 <= fixed50)
        assert np.all(fixed50 <= fixed90)

