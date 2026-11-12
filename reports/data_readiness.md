# Data Readiness Report: Farmer Sell Advisor

**Generated Date**: 12 November 2026  
**Audited Dataset**: `data/processed/panel.parquet` (16,240 verified rows)  
**Strict Provenance Gate Status**: **ENFORCED**  

---

## 1. Executive Summary: Model Training Gate

> [!CAUTION]
> **NO MODEL TRAINING CAN START UNTIL TIER A DATA EXISTS.**
> Under the project's strict data provenance rules, machine learning models (LightGBM quantile regressors, CQR calibration) can **only** be trained on verified **Tier A** real market history. No synthetic rows, LLM-generated values, or interpolated multi-day gaps are permitted.
>
> Currently, **0% of Karnataka market yards meet Tier A criteria**. All active models in `models/` remain archived, `models/registry.json` is empty, and the application strictly returns `"Not available"` (`"ಲಭ್ಯವಿಲ್ಲ"`) for spot prices and forecasts across all Karnataka mandis.

---

## 2. Coverage Tier Definitions

| Tier | Minimum Real Daily Rows | Minimum Time Span | Temporal Coverage | Training & App Policy |
|:---:|:---:|:---:|:---:|---|
| **Tier A** | $\ge 365$ daily observations | $\ge 1$ continuous year | $\ge 70\%$ active trading days | **Eligible for model training, conformal calibration, and live multi-horizon forecasting.** |
| **Tier B** | $90 - 364$ daily observations | $\ge 3$ continuous months | $\ge 50\%$ active trading days | Experimental heuristic benchmark only. No ML quantile training. |
| **Tier C** | $< 90$ daily observations | $< 3$ months (or snapshot) | $< 50\%$ coverage | **Strictly unready. No trained model. App shows "Not available".** |

---

## 3. Current Dataset Audit (`data/processed/panel.parquet`)

- **Total Panel Rows**: 16,240 (100% `data_provenance = "real"`, 0 synthetic rows)
- **Traceability**: 100% (16,240/16,240) verified against raw files and raw line numbers (`scripts/audit_trace.py`)
- **Acquisition Method**: 100% `user_download` from `data/raw/9ef84268-d588-465a-a308-a864a43d0070.csv`
- **Date Span**: Exactly 1 calendar date (`2026-11-03` to `2026-11-03`)
- **Total Mandis in Panel**: 1,720 mandis across 28 states
- **Karnataka Mandis in Panel**: **0** (data.gov.in snapshot on 03/11/2026 omitted Karnataka APMCs)

---

## 4. Readiness Matrix: Karnataka Focus Crops & Key Mandis

All Karnataka mandis and target crops evaluated currently have **zero historical rows** in the real panel.

| Crop | Mandi | District | Real Rows in Panel | Date Range | Coverage Tier | Readiness Status |
|---|---|---|:---:|:---:|:---:|---|
| **Onion** | Kolar APMC | Kolar | 0 | None | **Tier C** | Unready (Awaiting historical backfill) |
| **Onion** | Chikkaballapur APMC | Chikkaballapur | 0 | None | **Tier C** | Unready (Awaiting historical backfill) |
| **Onion** | Bengaluru (Yeshwanthpur) | Bengaluru Urban | 0 | None | **Tier C** | Unready (Awaiting historical backfill) |
| **Onion** | Hubballi (Amaragol) | Dharwad | 0 | None | **Tier C** | Unready (Awaiting historical backfill) |
| **Onion** | Belagavi APMC | Belagavi | 0 | None | **Tier C** | Unready (Awaiting historical backfill) |
| **Onion** | Shivamogga APMC | Shivamogga | 0 | None | **Tier C** | Unready (Awaiting historical backfill) |
| **Onion** | Hassan APMC | Hassan | 0 | None | **Tier C** | Unready (Awaiting historical backfill) |
| **Onion** | Mysuru (Bandipalya) | Mysuru | 0 | None | **Tier C** | Unready (Awaiting historical backfill) |
| **Potato** | Hassan APMC | Hassan | 0 | None | **Tier C** | Unready (Awaiting historical backfill) |
| **Potato** | Kolar APMC | Kolar | 0 | None | **Tier C** | Unready (Awaiting historical backfill) |
| **Potato** | Chikkaballapur APMC | Chikkaballapur | 0 | None | **Tier C** | Unready (Awaiting historical backfill) |
| **Potato** | Bengaluru (Yeshwanthpur) | Bengaluru Urban | 0 | None | **Tier C** | Unready (Awaiting historical backfill) |
| **Tomato** | Kolar APMC | Kolar | 0 | None | **Tier C** | Unready (Awaiting historical backfill) |
| **Tomato** | Chintamani APMC | Chikkaballapur | 0 | None | **Tier C** | Unready (Awaiting historical backfill) |
| **Tomato** | Malur APMC | Kolar | 0 | None | **Tier C** | Unready (Awaiting historical backfill) |
| **Tomato** | Bengaluru (Yeshwanthpur) | Bengaluru Urban | 0 | None | **Tier C** | Unready (Awaiting historical backfill) |

*Summary across all 444 Karnataka district-mandi candidate pairs*:
- **Tier A**: 0 (0.0%)
- **Tier B**: 0 (0.0%)
- **Tier C**: 444 (100.0%)

---

## 5. Non-Karnataka Mandis in Existing Panel (Snapshot Only)

The 16,240 rows in `panel.parquet` cover other Indian states (Tamil Nadu, Madhya Pradesh, Maharashtra, Kerala, Gujarat, etc.) for a single date (`03/11/2026`). Even for major onion markets in Maharashtra:

| Crop | Mandi | State | Real Rows | Date Range | Coverage Tier | Readiness Status |
|---|---|---|:---:|:---:|:---:|---|
| Onion | Lasalgaon APMC | Maharashtra | 1 | 2026-11-03 to 2026-11-03 | **Tier C** | Snapshot only (< 90 rows) |
| Onion | Pimpalgaon APMC | Maharashtra | 1 | 2026-11-03 to 2026-11-03 | **Tier C** | Snapshot only (< 90 rows) |
| Onion | Pune APMC | Maharashtra | 1 | 2026-11-03 to 2026-11-03 | **Tier C** | Snapshot only (< 90 rows) |
| Onion | Solapur APMC | Maharashtra | 1 | 2026-11-03 to 2026-11-03 | **Tier C** | Snapshot only (< 90 rows) |

---

## 6. Action Plan for Achieving Tier A Readiness

To transition Karnataka mandis from **Tier C** to **Tier A**:
1. **User Download Ingestion**: Place verified Agmarknet portal daily market bulletins / KSAMB CSV exports into `data/raw/user_download/`.
2. **Historical Backfill**: Collect continuous daily reports covering 2021–2026 for Karnataka market yards (minimum 365 daily rows per mandi-crop pair).
3. **Automated Verification**: Run `python scripts/audit_trace.py` and `pytest tests/test_provenance.py` on every batch.
4. **Training Authorization**: Trigger model training (`src/models/forecast.py`) **only** when `data/processed/coverage.parquet` shows target pairs achieving `tier == 'A'`.
