"""Test Monte Carlo simulation and output ranges for hold vs sell decision."""

import pytest
import numpy as np
from src.decision.when_to_sell import sample_from_quantiles, simulate_hold_vs_sell


def test_sample_from_quantiles_properties():
    """Verify Monte Carlo draws from asymmetric distribution respect quantiles."""
    p10, p50, p90 = 3000.0, 3600.0, 4400.0
    samples = sample_from_quantiles(p10, p50, p90, n_draws=10000, seed=42)

    assert len(samples) == 10000
    # 10th percentile should be close to p10
    emp_p10 = np.percentile(samples, 10.0)
    emp_p50 = np.percentile(samples, 50.0)
    emp_p90 = np.percentile(samples, 90.0)

    assert abs(emp_p10 - p10) < 60.0, f"Empirical P10 {emp_p10} deviates from target {p10}"
    assert abs(emp_p50 - p50) < 60.0, f"Empirical P50 {emp_p50} deviates from target {p50}"
    assert abs(emp_p90 - p90) < 60.0, f"Empirical P90 {emp_p90} deviates from target {p90}"


def test_simulator_bounds_and_decay():
    """Verify simulation probability bounded in [0, 100%] and higher spoilage reduces gains."""
    forecasts = {
        7: {"p10": 3400.0, "p50": 3700.0, "p90": 4000.0},
        14: {"p10": 3450.0, "p50": 3800.0, "p90": 4200.0},
        30: {"p10": 3500.0, "p50": 4100.0, "p90": 4600.0}
    }

    # Open storage (1.2% decay/day) vs Cold storage (0.1% decay/day)
    sim_open = simulate_hold_vs_sell(3600.0, forecasts, storage_type="open", credit_mode="none")
    sim_cold = simulate_hold_vs_sell(3600.0, forecasts, storage_type="cold_storage", credit_mode="none")

    # Spoilage in open storage for 30d must be strictly higher than in cold storage
    assert sim_open["horizons"][30]["spoilage_loss_pct"] > sim_cold["horizons"][30]["spoilage_loss_pct"]

    # Probabilities must be bounded in [0, 100]
    for k in [7, 14, 30]:
        prob = sim_open["horizons"][k]["prob_wait_beats_today_pct"]
        assert 0.0 <= prob <= 100.0, f"Probability {prob} out of bounds!"


def test_trader_debt_reduces_holding_incentive():
    """Verify that high trader debt interest pushes recommendation towards selling today."""
    forecasts = {
        7: {"p10": 3500.0, "p50": 3650.0, "p90": 3800.0},
        14: {"p10": 3550.0, "p50": 3720.0, "p90": 3900.0},
        30: {"p10": 3600.0, "p50": 3850.0, "p90": 4100.0}
    }
    # With 24% trader debt interest, holding gains must be significantly lower than with 0% debt
    sim_debt = simulate_hold_vs_sell(3600.0, forecasts, storage_type="warehouse", credit_mode="trader_debt")
    sim_nodebt = simulate_hold_vs_sell(3600.0, forecasts, storage_type="warehouse", credit_mode="none")

    gain_debt_30 = sim_debt["horizons"][30]["expected_gain_per_qtl"]
    gain_nodebt_30 = sim_nodebt["horizons"][30]["expected_gain_per_qtl"]

    assert gain_debt_30 < gain_nodebt_30

