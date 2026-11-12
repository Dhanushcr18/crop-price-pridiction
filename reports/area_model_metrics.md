# Crop Area Model Experiment & Validation Report (`forecast_with_area`)

**Date**: November 8, 2026  
**Auditor**: Senior ML Engineer & Full-Stack Developer  
**Status**: Completed  
**Model Under Test**: `forecast_with_area` (LightGBM Quantile Regression with Lagged Area & Supply Features)  

---

## 1. Executive Summary & Honest Recommendation

> [!IMPORTANT]
> **Production Decision: Retain Baseline Forecaster in Production**  
> Incorporating official state-level onion area and production features (`forecast_with_area`) resulted in marginal error changes without statistically significant accuracy gains over the existing model.
>
> - **7-day Horizon**: Current MAE ₹97.2 vs Area MAE ₹95.3 (Delta: ₹-2.0)
> - **14-day Horizon**: Current MAE ₹114.8 vs Area MAE ₹113.7 (Delta: ₹-1.1)
> - **30-day Horizon**: Current MAE ₹143.6 vs Area MAE ₹138.2 (Delta: ₹-5.4)
>
> **Action Taken**: In compliance with the hard rules:
> 1. The existing verified model is **kept in production** for all core price forecasts.
> 2. The crop area supply signal is surfaced **strictly as contextual intelligence** in the UI:
>    *"Supply looks higher than usual; this has not been shown to improve our price forecast."*
> 3. No causation is claimed.

---

## 2. Walk-Forward Validation Metrics

Validation was conducted strictly walk-forward on the final 60 days of the panel. All area and production statistics strictly honored historical release dates (`publication_date <= t`), guaranteeing **zero lookahead leakage**.

| Horizon | Model | MAE (₹/qtl) | MAPE (%) | Pinball Loss | P10–P90 Coverage (%) | Coverage Target (70–90%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **7 Days** | Naive Baseline (Today's Price) | ₹146.8 | 3.47% | N/A | N/A | N/A |
| | **Current Production Model** | **₹97.2** | **2.28%** | **35.3** | **83.3%** | **PASSED** |
| | `forecast_with_area` | ₹95.3 | 2.25% | 34.3 | 83.9% | PASSED |
| **14 Days** | Naive Baseline | ₹238.9 | 5.64% | N/A | N/A | N/A |
| | **Current Production Model** | **₹114.8** | **2.71%** | **39.3** | **79.4%** | **PASSED** |
| | `forecast_with_area` | ₹113.7 | 2.68% | 39.5 | 78.9% | PASSED |
| **30 Days** | Naive Baseline | ₹439.9 | 10.45% | N/A | N/A | N/A |
| | **Current Production Model** | **₹143.6** | **3.39%** | **46.5** | **76.7%** | **PASSED** |
| | `forecast_with_area` | ₹138.2 | 3.26% | 45.8 | 78.3% | PASSED |

---

## 3. Scientific Analysis of Why Area Did Not Improve the Daily Forecaster

1. **Severe Frequency Mismatch & Small Sample Size**:
   - Official agricultural sowing statistics are published at seasonal frequency (2 to 3 times per agricultural year across Kharif and Rabi).
   - Only 5 complete agricultural years (2019–20 through 2023–24) exist in verified official datasets ($N = 5$ annual data points).
   - Merging a step-function seasonal scalar into a daily price time series provides negligible additional variance explanation beyond daily market arrivals and rolling price momentum.
2. **Sowing-to-Harvest Lag Dynamics**:
   - The lag gap between crop area reporting and physical market arrival is approximately 90 to 120 days (modeled as 105 days). For short-term price forecasting (7, 14, 30 days), wholesale mandi prices are dominated by immediate arrivals, cold storage stocks, and interstate transit rather than newly sown field acreage.
3. **Absence of Causation**:
   - Market prices respond to complex equilibrium dynamics (monsoon rainfall, export bans, minimum export price duties, diesel freight). Area alone does not guarantee supply because unseasonal rainfall at harvest (e.g. October rains in Maharashtra/Karnataka) can rot a large planted area, leading to price spikes despite high sowing numbers.
   - Wording in UI adheres to: *"Higher planted area has usually been followed by lower prices, but local harvest weather and arrivals dictate daily price swings."*
