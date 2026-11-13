# Data Readiness & Provenance Report

**Date of Report**: 13 November 2026  
**Provenance Status**: 100% REAL DATA (0 synthetic rows, 0 LLM-generated prices, 0 imputed rows)  
**Historical Continuity Status**: **1 DAY ONLY (2026-11-11)** — **ALL CROPS AND MANDIS REMAIN TIER C**  
**Training Gate**: **STRICTLY BLOCKED** — No model training can begin until Tier A data exists (requires >= 300 real days of daily observations).

---

## 1. Executive Summary & Provenance Gate

On 13 November 2026, the official KSAMB Commoditywise Daily Market Report PDF (`Crop_price_of_all_mandies_of_karnataka.pdf`) for trade date **2026-11-11** covering all 115 Karnataka APMC markets was ingested via `src/ingest/connectors/ksamb_pdf.py` and validated against golden fixture `karnataka_mandi_prices_2026-11-11.csv`:

- **Total Markets in Bulletin**: 115 markets (100% verified contiguous 1..115 with zero gaps, every market has >= 1 row, and dual table/text passes agree).
- **Total Parsed Rows**: 752 raw rows.
  - **Accepted Quintal Rows**: 653 rows (loaded into `data/processed/panel.parquet`).
  - **Non-Quintal Series**: 27 rows (Numbers, Thousands) safely isolated outside the quintal panel in `data/processed/non_quintal_prices.parquet`.
  - **Quarantined Rows**: 99 rows flagged for anomalies and stored in `data/quarantine/` with diagnostic logs.
- **National Baseline Rows**: 16,240 rows from date `2026-11-03`.
- **Total Rows in `panel.parquet`**: **16,893 rows**.
- **Audit-Trace Status**: **100% PASSED** (`make audit-trace` verified all 16,893 rows against raw file lines, PDF pages, and tables).

---

## 2. Readiness Tiers Across Karnataka Mandis

| Metric | Status | Rule / Requirement |
| :--- | :--- | :--- |
| **Karnataka Trade Dates** | **1 Day Only** (`2026-11-11`) | Tier A requires $\ge 300$ daily observations; Tier B requires $\ge 60$ days. |
| **Active Mandis with Valid Rows** | **115 APMCs** | All 115 markets present; 653 clean quintal rows across reporting markets. |
| **Distinct Commodities Covered** | **96 crops** | Field crops, vegetables, pulses, oilseeds, plantation crops, spices. |
| **Tier A Coverage** | **0.0% (0 / 444 pairs)** | **INSUFFICIENT DATA FOR FORECAST TRAINING** |
| **Tier B Coverage** | **0.0% (0 / 444 pairs)** | Insufficient history |
| **Tier C Coverage** | **100.0% (444 / 444 pairs)** | **Tier C (Observed Spot Price Today Only, No Model Forecast)** |

> [!IMPORTANT]
> **TRAINING STATUS: STRICTLY BLOCKED**  
> While we now have exact, observed, verified market prices for Karnataka mandis for today/yesterday (`2026-11-11`), **1 single day of observations is not a time series**. The provenance gate strictly prohibits model fitting, quantile regression, or LightGBM training until a multi-year historical backfill provides Tier A depth. The application UI must display actual observed prices where present and "Not Available / No Model Yet" for forward forecasts.

---

## 3. Today's Onion Market Realities: Kolar, Bengaluru, and Hubballi

- **Kolar**: **NO ONION ON THIS DATE**. Kolar APMC reported 17 commodities (Tomato, Thogarikai, Beans, etc.) on 2026-11-11, but reported **zero Onion arrivals and zero Onion price rows**.
- **Bengaluru**: **HAS ONION TODAY** (4 distinct series across grades and varieties, Local Medium modal ₹3,500/qtl, 10,823 qtl arrivals).
- **Hubballi**: **HAS ONION TODAY** (2 series: Local Average modal ₹4,500/qtl with 12,500 qtl arrivals, Puna Average modal ₹4,200/qtl with 2,160 qtl arrivals).

### All 21 Observed Onion Rows in Karnataka (2026-11-11)

| # | Market No | Mandi | District | Variety | Grade | Min (₹) | Max (₹) | Modal (₹) | Arrivals (qtl) | Source Page & Table Row | Flags |
| :-: | :-: | :--- | :--- | :--- | :--- | :-: | :-: | :-: | :-: | :-: | :--- |
| 1 | 8 | **BANGARPET** | Kolar | Onion | Average | 4,000 | 5,000 | **4,500** | 6 | Page 2, Row 16 | *None (Accepted)* |
| 2 | 11 | **BELAGAVI** | Belagavi | Pusa-Red | Large | 2,000 | 5,000 | **4,000** | 5,176 | Page 4, Row 12 | *None (Accepted)* |
| 3 | 12 | **BELUR** | Hassan | Bombay (U.P.) | Medium | 4,500 | 4,500 | **4,500** | 15 | Page 5, Row 5 | *None (Accepted)* |
| 4 | 13 | **BENGALURU** | Bengaluru Urban | Bangalore Small | Small | 1,000 | 2,500 | **1,500** | 10,823 | Page 6, Row 13 | *None (Accepted)* |
| 5 | 13 | **BENGALURU** | Bengaluru Urban | Local | Medium | 3,000 | 4,000 | **3,500** | 10,823 | Page 6, Row 14 | *None (Accepted)* |
| 6 | 13 | **BENGALURU** | Bengaluru Urban | Onion | Large | 4,000 | 5,500 | **4,500** | 10,823 | Page 6, Row 15 | *None (Accepted)* |
| 7 | 13 | **BENGALURU** | Bengaluru Urban | Puna | Average | 3,000 | 5,400 | **4,500** | 3,607 | Page 6, Row 16 | *None (Accepted)* |
| 8 | 23 | **CHIKKAMAGALURU** | Chikkamagaluru | Other | Average | 4,200 | 4,200 | **4,200** | 8 | Page 11, Row 6 | `min_eq_max_eq_modal_most_rows` |
| 9 | 28 | **DAVANAGERE** | Davanagere | Onion | Average | 3,000 | 4,800 | **4,400** | 975 | Page 12, Row 12 | *None (Accepted)* |
| 10 | 29 | **DODDABALLAPUR** | Bengaluru Rural | Onion | Medium | 4,000 | 5,000 | **4,600** | 35 | Page 14, Row 5 | *None (Accepted)* |
| 11 | 31 | **GADAG** | Gadag | Onion | Medium | 950 | 4,500 | **3,000** | 1,368 | Page 14, Row 32 | *None (Accepted)* |
| 12 | 34 | **GOWRIBIDNUR** | Chikkaballapur | Onion | Average | 3,800 | 4,500 | **4,300** | 4 | Page 16, Row 13 | *None (Accepted)* |
| 13 | 42 | **HASSAN** | Hassan | Other | Average | 1,000 | 3,000 | **1,712** | 1,091 | Page 17, Row 22 | *None (Accepted)* |
| 14 | 51 | **HUBBALLI** | Dharwad | Local | Average | 500 | 4,900 | **4,500** | 12,500 | Page 19, Row 13 | *None (Accepted)* |
| 15 | 51 | **HUBBALLI** | Dharwad | Puna | Average | 1,000 | 4,700 | **4,200** | 2,160 | Page 19, Row 14 | *None (Accepted)* |
| 16 | 57 | **K.R.PET** | Mandya | Onion | Average | 3,000 | 3,000 | **3,000** | 15 | Page 21, Row 12 | *None (Accepted)* |
| 17 | 58 | **KADUR** | Chikkamagaluru | Onion | Medium | 2,776 | 2,776 | **2,776** | 3 | Page 21, Row 25 | `same_price_triple_3plus_crops;min_eq_max_eq_modal_most_rows` |
| 18 | 59 | **KALABURAGI** | Kalaburagi | Onion | Average | 300 | 4,500 | **2,400** | 725 | Page 22, Row 2 | *None (Accepted)* |
| 19 | 90 | **RAMANAGARA** | Ramanagara | Onion | Average | 4,400 | 5,600 | **5,000** | 105 | Page 29, Row 21 | *None (Accepted)* |
| 20 | 101 | **SHIVAMOGGA** | Shivamogga | Onion | Average | 3,000 | 6,000 | **4,500** | 50 | Page 32, *Text Line* | `recovered_from_text_line` |
| 21 | 113 | **UDIPI** | Udupi | Onion | Average | 3,500 | 4,000 | **3,800** | 331 | Page 35, Row 12 | *None (Accepted)* |

---

## 4. Multi-Variety Handling & Headline Price Rule (Assumption)

- **Independent Series**: Varieties and grades are preserved as distinct rows. Arrivals are **never summed or averaged** across varieties (in Bengaluru, arrival `10,823` is repeated on three varieties; summing them would falsely record 32,469 quintals).
- **Headline Selection Rule (`config.yaml`)**:
  - `rule_name`: `highest_arrivals_representative_variety`
  - `is_assumption`: `True`
  - `default_rule`: `"the row with the highest arrivals for that variety, and show every grade in the UI detail"`
  - **Headline Selection for Bengaluru**: The standard `Local (Medium)` series with modal price **₹3,500/quintal** and 10,823 quintals arrival is designated as the primary benchmark.

---

## 5. Summary of Quarantined Anomalies (99 Rows)

The 99 flagged rows were excluded from `panel.parquet` and stored in `data/quarantine/` with diagnostic tags:
1. **Flag `same_price_triple_3plus_crops`** (50 rows): Identical min/max/modal triple shared across $\ge 3$ distinct crops in a single market.
2. **Flag `min_eq_max_eq_modal_most_rows`** (25 rows): Flat market pricing (>50% of rows flat) in markets with $\ge 8$ rows (CHIKKAMAGALURU and KADUR).
3. **Flag `price_below_100_per_qtl`** (1 row): Kalaburagi Radish reported at `min=10, max=20, modal=15` (unit error).
4. **Flag `non_quintal_unit`** (27 rows): Numbers/Thousands (safely preserved in `non_quintal_prices.parquet`).
5. **Flag `recovered_from_text_line`** (1 row): Shivamogga Onion on page 32 recovered from text lines pass.
