# Data Readiness & Provenance Report

**Date of Report**: 12 November 2026  
**Provenance Status**: 100% REAL DATA (0 synthetic rows, 0 LLM-generated prices, 0 imputed rows)  
**Historical Continuity Status**: **1 DAY ONLY (2026-11-11)** — **ALL CROPS AND MANDIS REMAIN TIER C**  
**Training Gate**: **BLOCKED** — No model training can begin until Tier A data exists (requires >= 300 real days of daily observations).

---

## 1. Executive Summary & Provenance Gate

On 12 November 2026, an official KSAMB Commoditywise Daily Market Report PDF (`Crop_price_of_all_mandies_of_karnataka.pdf`) for trade date **11/11/2026** covering 115 Karnataka APMC markets was ingested.

- **Total Markets in Document**: 115 markets (100% completeness verified across dual independent parsing engines).
- **Total Parsed Rows**: 752 raw rows.
  - **Accepted Quintal Rows**: 605 rows (across 99 active mandis and 96 distinct agricultural commodities).
  - **Non-Quintal Series**: 27 rows (Numbers, Thousands) safely stored outside the quintal panel in `data/processed/non_quintal_prices.parquet`.
  - **Quarantined Rows**: 120 rows flagged for anomalies and quarantined in `data/quarantine/` with diagnostic logs.
- **National Baseline Rows**: 16,240 rows from date `2026-11-03`.
- **Total Rows in `panel.parquet`**: **16,845 rows**.
- **Audit-Trace Status**: **100% PASSED** (`python scripts/audit_trace.py` verified all 16,845 rows against exact raw file lines and PDF pages).

---

## 2. Readiness Tiers Across Karnataka Mandis

| Metric | Status | Rule / Requirement |
| :--- | :--- | :--- |
| **Karnataka Trade Dates** | **1 Day Only** (`2026-11-11`) | Tier A requires $\ge 300$ daily observations; Tier B requires $\ge 60$ days. |
| **Active Mandis with Valid Rows** | **99 APMCs** | Markets reporting valid quintal trading. 16 markets had all rows quarantined or non-quintal. |
| **Distinct Commodities Covered** | **96 crops** | Field crops, vegetables, pulses, oilseeds, plantation crops, spices. |
| **Tier A Coverage** | **0.0% (0 / 444 pairs)** | **INSUFFICIENT DATA FOR FORECAST TRAINING** |
| **Tier B Coverage** | **0.0% (0 / 444 pairs)** | Insufficient history |
| **Tier C Coverage** | **100.0% (444 / 444 pairs)** | **Tier C (Observed Price Today Only, No Model Forecast)** |

> [!IMPORTANT]
> **TRAINING STATUS: STRICTLY BLOCKED**  
> While we now have exact, observed, verified market prices for Karnataka mandis for today/yesterday (`11/11/2026`), **1 single day of observations is not a time series**. The provenance gate strictly prohibits model fitting, quantile regression, or LightGBM training until a multi-year historical backfill provides Tier A depth. The application UI must display actual observed prices where present and "Not Available / No Model Yet" for forward forecasts.

---

## 3. Today's Onion Market Realities: Kolar, Chikkaballapur & Bengaluru

Inspection of the 11/11/2026 KSAMB bulletin for the core target mandis:

| Target Mandi | Status on 11/11/2026 | Reported Varieties | Modal Price (₹/qtl) | Arrivals (qtl) | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Bengaluru (Yeshwanthpur)** | **HAS ONION TODAY** | 4 distinct series (see below) | ₹1,500 – ₹4,500 | 10,823 / 3,607 | Active wholesale trading across multiple commercial grades. |
| **Kolar** | **NO ONION TODAY** | *None* | *Not available* | 0 | Kolar APMC traded other commodities (Tomato, etc.) but reported zero Onion trading on 11/11/2026. |
| **Chikkaballapur** | **NO ONION TODAY** | *None* | *Not available* | 0 | Chikkaballapur APMC reported zero Onion trading in this daily report. |

### All 17 Observed Onion Rows in Karnataka (11/11/2026)

| # | Mandi | District | Variety | Grade | Min (₹) | Max (₹) | Modal (₹) | Arrivals (qtl) | PDF Page & Line |
| :-: | :--- | :--- | :--- | :--- | :-: | :-: | :-: | :-: | :-: |
| 1 | **Bangarpet** | Kolar | Onion | Average | 4,000 | 5,000 | **4,500** | 6.0 | Page 2, Line 16 |
| 2 | **Belagavi** | Belagavi | Pusa-Red | Large | 2,000 | 5,000 | **4,000** | 5,176.0 | Page 4, Line 12 |
| 3 | **Bengaluru (Yeshwanthpur)** | Bengaluru Urban | Bangalore Small | Small | 1,000 | 2,500 | **1,500** | 10,823.0 | Page 6, Line 13 |
| 4 | **Bengaluru (Yeshwanthpur)** | Bengaluru Urban | Local | Medium | 3,000 | 4,000 | **3,500** | 10,823.0 | Page 6, Line 14 |
| 5 | **Bengaluru (Yeshwanthpur)** | Bengaluru Urban | Onion | Large | 4,000 | 5,500 | **4,500** | 10,823.0 | Page 6, Line 15 |
| 6 | **Bengaluru (Yeshwanthpur)** | Bengaluru Urban | Puna | Average | 3,000 | 5,400 | **4,500** | 3,607.0 | Page 6, Line 16 |
| 7 | **Davanagere** | Davanagere | Onion | Average | 3,000 | 4,800 | **4,400** | 975.0 | Page 12, Line 12 |
| 8 | **Doddaballapur** | Bengaluru Rural | Onion | Medium | 4,000 | 5,000 | **4,600** | 35.0 | Page 14, Line 5 |
| 9 | **Gadag** | Gadag | Onion | Medium | 950 | 4,500 | **3,000** | 1,368.0 | Page 14, Line 32 |
| 10 | **Gowribidnur** | Chikkaballapur | Onion | Average | 3,800 | 4,500 | **4,300** | 4.0 | Page 16, Line 13 |
| 11 | **Hassan** | Hassan | Other | Average | 1,000 | 3,000 | **1,712** | 1,091.0 | Page 17, Line 22 |
| 12 | **Hubballi** | Dharwad | Local | Average | 500 | 4,900 | **4,500** | 12,500.0 | Page 19, Line 13 |
| 13 | **Hubballi** | Dharwad | Puna | Average | 1,000 | 4,700 | **4,200** | 2,160.0 | Page 19, Line 14 |
| 14 | **Kalaburagi** | Kalaburagi | Onion | Average | 300 | 4,500 | **2,400** | 725.0 | Page 22, Line 2 |
| 15 | **Ramanagara** | Ramanagara | Onion | Average | 4,400 | 5,600 | **5,000** | 105.0 | Page 29, Line 21 |
| 16 | **Shivamogga** | Shivamogga | Onion | Average | 3,000 | 6,000 | **4,500** | 50.0 | Page 32, Line 27 |
| 17 | **Udupi** | Udupi | Onion | Average | 3,500 | 4,000 | **3,800** | 331.0 | Page 35, Line 12 |

---

## 4. Multi-Variety Handling & Headline Price Rule (Assumption)

In accordance with Step 5 instructions:
- **No Summing/Averaging of Arrivals**: In Bengaluru, the arrival count `10,823` is repeated on three separate lines (`Bangalore Small`, `Local`, `Onion`). Summing them would falsely inflate market volume to $32,469$ quintals. Each variety and grade is preserved as an independent series.
- **Headline Series Rule (`config.yaml`)**:
  - `rule_name`: `representative_commercial_variety`
  - `is_assumption`: `True`
  - **Headline Selection for Bengaluru**: The standard `Local (Medium)` series with modal price **₹3,500/quintal** and 10,823 quintals arrival is designated as the primary benchmark for farmer advisory, representing standard table onion.

---

## 5. Summary of Quarantined Anomalies (120 Rows)

The 120 flagged rows were excluded from `panel.parquet` and stored in `data/quarantine/` with diagnostic tags:
1. **Flag (a) Shared Identical Triples across $\ge 3$ crops** (44 rows):
   - Examples: Nanjangud (`min=3700, max=4666, modal=4166` shared by Radish, Potato, Tomato); Gowribidnur (`1500/2500/2000` shared by Bottle Gourd, Tomato, Potato, Cauliflower).
2. **Flag (b) Flat Price Markets** (72 rows):
   - Examples: Kadur (9 of 15 rows reported `min == max == modal`, such as `2776/2776/2776` across Ladies Finger, Potato, Onion); Belur (6 of 7 rows flat); Yarahalli (100% of rows flat).
3. **Flag (c) Sub-₹100 Floor Violation** (1 row):
   - Kalaburagi: Radish reported at `min=10, max=20, modal=15` (likely per-bunch/kg reported as quintal).
4. **Flag (d) Coincidental / Synthesized 0.9 / 1.1 Min/Max Ratio** (3 rows):
   - Binny Mill: Cabbage (`900/1000/1100`), Green Avare (`3600/4000/4400`), Tomato (`1350/1500/1650`).
