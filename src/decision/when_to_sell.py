"""When-to-sell simulator: Monte Carlo simulation of holding vs selling today under post-harvest spoilage and financing."""

import yaml
from typing import Dict, List, Optional
import numpy as np


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration parameters."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def sample_from_quantiles(p10: float, p50: float, p90: float, n_draws: int = 10000, seed: int = 42) -> np.ndarray:
    """
    Sample n_draws from an asymmetric distribution defined by P10, P50, and P90 quantiles.
    Uses inverse CDF transform with piecewise linear interpolation matching exact quantiles.
    """
    np.random.seed(seed)
    u = np.random.uniform(0.001, 0.999, size=n_draws)
    samples = np.zeros(n_draws)

    # Below P10 (left tail)
    mask_left = u < 0.10
    slope_left = (p50 - p10) / 0.40
    samples[mask_left] = p10 - slope_left * (0.10 - u[mask_left])

    # Between P10 and P50
    mask_mid_left = (u >= 0.10) & (u < 0.50)
    samples[mask_mid_left] = p10 + ((u[mask_mid_left] - 0.10) / 0.40) * (p50 - p10)

    # Between P50 and P90
    mask_mid_right = (u >= 0.50) & (u <= 0.90)
    samples[mask_mid_right] = p50 + ((u[mask_mid_right] - 0.50) / 0.40) * (p90 - p50)

    # Above P90 (right tail)
    mask_right = u > 0.90
    slope_right = (p90 - p50) / 0.40
    samples[mask_right] = p90 + slope_right * (u[mask_right] - 0.90)

    return np.clip(samples, 500.0, 10000.0)


def simulate_hold_vs_sell(
    price_today: float,
    forecast_by_horizon: Dict[int, Dict[str, float]],
    storage_type: str = "open",
    credit_mode: str = "none",  # "none", "trader_debt", "warehouse_receipt"
    quantity_quintals: float = 50.0,
    config_path: str = "config.yaml",
    n_draws: int = 10000
) -> Dict:
    """
    Simulates expected financial gains and downside risks of holding onions for k days.

    Parameters:
    - price_today: Net spot price if sold today (Rs/quintal)
    - forecast_by_horizon: {7: {'p10': x, 'p50': y, 'p90': z}, 14: ..., 30: ...}
    - storage_type: "open", "warehouse", or "cold_storage"
    - credit_mode: "none" (0%), "trader_debt" (24% p.a.), or "warehouse_receipt" (9% p.a.)
    """
    config = load_config(config_path)
    storage_cfg = config["storage"]["types"].get(storage_type, config["storage"]["types"]["open"])

    daily_spoilage = storage_cfg.get("daily_spoilage_rate", 0.012)
    daily_storage_cost = storage_cfg.get("cost_per_quintal_day", 0.0)

    # Credit interest rate
    if credit_mode == "trader_debt":
        annual_rate = config["credit"].get("trader_debt_annual_interest_pct", 24.0) / 100.0
    elif credit_mode == "warehouse_receipt":
        annual_rate = config["credit"].get("warehouse_receipt_loan_annual_interest_pct", 9.0) / 100.0
    else:
        annual_rate = 0.0

    # Horizon 0: Sell today
    if price_today is None or price_today <= 0:
        return {
            "price_today": None,
            "best_k_days": 0,
            "max_expected_gain_per_qtl": 0.0,
            "horizon_results": {
                0: {
                    "k_days": 0,
                    "expected_gain_per_qtl": 0.0,
                    "p10_gain_per_qtl": 0.0,
                    "p90_gain_per_qtl": 0.0,
                    "total_expected_gain": 0.0,
                    "prob_wait_beats_today_pct": 0.0
                }
            }
        }

    daily_interest_cost = price_today * (annual_rate / 365.0)

    horizon_results = {}
    best_k = 0
    max_expected_gain = 0.0

    # Horizon 0: Sell today
    horizon_results[0] = {
        "k_days": 0,
        "expected_gain_per_qtl": 0.0,
        "worst_case_p10_gain": 0.0,
        "prob_wait_beats_today_pct": 0.0,
        "expected_future_price": price_today,
        "spoilage_loss_pct": 0.0,
        "storage_cost_per_qtl": 0.0,
        "interest_cost_per_qtl": 0.0,
        "recommendation": "Sell Today"
    }

    horizons = sorted(forecast_by_horizon.keys())
    spoilage_loss_pct = round(daily_spoilage * 7 * 100, 2)

    for k in horizons:
        q = forecast_by_horizon[k]
        p10, p50, p90 = q["p10"], q["p50"], q["p90"]

        # Monte Carlo draws of future price
        sampled_prices = sample_from_quantiles(p10, p50, p90, n_draws=n_draws, seed=42 + k)

        # Spoilage decay: compound retention factor
        retention = (1.0 - daily_spoilage) ** k
        spoilage_loss_pct = round((1.0 - retention) * 100, 2)

        storage_cost = daily_storage_cost * k
        interest_cost = daily_interest_cost * k

        # Net gain per quintal for each Monte Carlo realization
        # gain = Price(k) * (1 - spoilage(k)) - storage_cost - interest_cost - Price_today
        draws_gain = (sampled_prices * retention) - storage_cost - interest_cost - price_today

        mean_gain = float(np.mean(draws_gain))
        p10_gain = float(np.percentile(draws_gain, 10.0))
        p90_gain = float(np.percentile(draws_gain, 90.0))
        prob_positive = float(np.mean(draws_gain > 0.0) * 100.0)

        horizon_results[k] = {
            "k_days": k,
            "expected_gain_per_qtl": round(mean_gain, 2),
            "worst_case_p10_gain": round(p10_gain, 2),
            "p90_upside_gain": round(p90_gain, 2),
            "prob_wait_beats_today_pct": round(prob_positive, 1),
            "expected_future_price": round(float(p50), 2),
            "spoilage_loss_pct": spoilage_loss_pct,
            "storage_cost_per_qtl": round(storage_cost, 2),
            "interest_cost_per_qtl": round(interest_cost, 2),
            "total_expected_gain_lot": round(mean_gain * quantity_quintals, 2)
        }

        if mean_gain > max_expected_gain and prob_positive >= 50.0:
            max_expected_gain = mean_gain
            best_k = k

    # Overall recommendation synthesis
    if best_k > 0:
        advice_summary = (
            f"Advisable to HOLD for {best_k} days in {storage_cfg['name']}. "
            f"Expected gain: +Rs {horizon_results[best_k]['expected_gain_per_qtl']:.2f}/quintal "
            f"(Total: +Rs {horizon_results[best_k]['total_expected_gain_lot']:,}) "
            f"with {horizon_results[best_k]['prob_wait_beats_today_pct']}% probability of beating today's price. "
            f"Downside risk (P10): Rs {horizon_results[best_k]['worst_case_p10_gain']:.2f}/quintal."
        )
    else:
        advice_summary = (
            f"Advisable to SELL TODAY at Rs {price_today:.2f}/quintal. "
            f"Holding in {storage_cfg['name']} risks higher spoilage ({spoilage_loss_pct}%) "
            f"and carrying costs than anticipated price increases."
        )

    return {
        "best_k_days": best_k,
        "max_expected_gain_per_qtl": round(max_expected_gain, 2),
        "total_expected_gain_lot": round(max_expected_gain * quantity_quintals, 2),
        "storage_type_used": storage_type,
        "credit_mode_used": credit_mode,
        "advice_summary": advice_summary,
        "horizons": horizon_results
    }


if __name__ == "__main__":
    sample_price_today = 3500.0
    sample_forecasts = {
        7: {"p10": 3400.0, "p50": 3700.0, "p90": 4000.0},
        14: {"p10": 3450.0, "p50": 3850.0, "p90": 4200.0},
        30: {"p10": 3600.0, "p50": 4250.0, "p90": 4800.0}
    }

    print("--- 1. Farm Open Storage with Trader Debt (24% p.a.) ---")
    sim1 = simulate_hold_vs_sell(
        sample_price_today, sample_forecasts, storage_type="open", credit_mode="trader_debt"
    )
    print("Recommendation:", sim1["advice_summary"])

    print("\n--- 2. Warehouse with Warehouse Receipt Credit (9% p.a.) ---")
    sim2 = simulate_hold_vs_sell(
        sample_price_today, sample_forecasts, storage_type="warehouse", credit_mode="warehouse_receipt"
    )
    print("Recommendation:", sim2["advice_summary"])
    for k, v in sim2["horizons"].items():
        if k > 0:
            print(f"  Wait {k}d: Expected Gain = Rs {v['expected_gain_per_qtl']}/qtl | P(Beat) = {v['prob_wait_beats_today_pct']}% | Worst (P10) = Rs {v['worst_case_p10_gain']}/qtl")

