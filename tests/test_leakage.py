"""Test that features strictly use historical data up to date t without data leakage."""

import pytest
import pandas as pd
import numpy as np
from src.models.forecast import build_features, load_config


def test_no_data_leakage_in_features():
    """Verify that altering future prices has ZERO impact on feature values at date t."""
    config = load_config()
    
    # Create two synthetic datasets differing ONLY in future dates
    dates = pd.date_range("2024-01-01", "2024-06-01", freq="D")
    mandis = config["project"]["target_mandis"]
    
    records1 = []
    records2 = []
    
    np.random.seed(42)
    cutoff_date = pd.to_datetime("2024-03-01")
    
    for m in mandis:
        p_base = 3500.0 + np.random.normal(0, 50, size=len(dates))
        p_future_shock = p_base.copy()
        # Shock future prices after cutoff
        future_idx = dates > cutoff_date
        p_future_shock[future_idx] += 2500.0  # Massive future spike
        
        for idx, d in enumerate(dates):
            r1 = {
                "date": d,
                "mandi": m,
                "modal_price": p_base[idx],
                "min_price": p_base[idx] - 200,
                "max_price": p_base[idx] + 200,
                "arrivals": 500.0,
                "rainfall": 5.0,
                "temperature": 25.0,
                "diesel_price": 88.0,
                "festival_flag": 0,
                "month": d.month,
                "day_of_week": d.dayofweek,
                "day_of_year": d.dayofyear,
                "week_of_year": int(d.isocalendar().week)
            }
            r2 = r1.copy()
            r2["modal_price"] = p_future_shock[idx]
            records1.append(r1)
            records2.append(r2)
            
    df1 = pd.DataFrame(records1)
    df2 = pd.DataFrame(records2)
    
    feats1 = build_features(df1, horizon=7, config=config)
    feats2 = build_features(df2, horizon=7, config=config)
    
    # Features at or before cutoff_date MUST be IDENTICAL
    past_feats1 = feats1[feats1["date"] <= cutoff_date].sort_values(["date", "mandi"]).reset_index(drop=True)
    past_feats2 = feats2[feats2["date"] <= cutoff_date].sort_values(["date", "mandi"]).reset_index(drop=True)
    
    check_cols = [
        "lag_1", "lag_7", "lag_14", "lag_30",
        "rolling_mean_7", "rolling_std_7",
        "rolling_mean_14", "rolling_mean_30"
    ]
    
    for col in check_cols:
        diff = np.abs(past_feats1[col].values - past_feats2[col].values)
        assert np.max(diff) < 1e-5, f"Data leakage detected! Feature '{col}' at date t was altered by future prices!"

