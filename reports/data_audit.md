# ⚠️ SYNTHETIC DATA - NOT FOR REAL DECISIONS ⚠️

> [!CAUTION]
> **SYNTHETIC DATA - NOT FOR REAL DECISIONS**
> The current baseline data panel contains synthetic rows due to the absence of continuous historical Agmarknet daily price series in the initial download files.
> This report documents data availability and pipeline requirements.
> **DO NOT USE MODELS TRAINED ON SYNTHETIC DATA FOR ACTUAL COMMERCIAL, FARMING, OR HARVESTING DECISIONS.**
> When real Agmarknet CSV files are added to `data/raw/real/`, the pipeline will rebuild the panel strictly from real data and remove this warning.

---

# Data Audit Report: Farmer Sell Advisor (Onion)
**Project**: Farmer Sell Advisor — Decision Intelligence for Smallholder Onion Farmers  
**Target Region**: Karnataka (Kolar, Chikkaballapur, Bengaluru Yeshwanthpur APMC)  
**Date of Audit**: November 2026  
**Auditor**: ML Engineering Team  
**Data Provenance Status**: **SYNTHETIC BENCHMARK MODE (Real Data Folder: `data/raw/real/`)**

---

## 1. Executive Summary

An exhaustive scan and statistical audit of the raw data assets in `./data/raw` (and project root) was conducted. The objective is to advise smallholder onion farmers on **WHERE** to sell, **WHEN** to sell, and at what **expected price** with rigorous uncertainty bounds ($P10/P50/P90$) across horizons of 7, 14, and 30 days.

### Audit Findings Matrix
| Expected Domain Component | Raw File Found | Coverage & Granularity | Status | Resolution / Action in Pipeline |
| :--- | :--- | :--- | :--- | :--- |
| **Agmarknet Mandi Prices** | `9ef84268-d588-465a-a308-a864a43d0070.csv`<br>`Market_Wise_Price_Arrival_04-11-2026_12-20-32_AM.csv` | 17,319 rows across India (1 day, 03/11/2026); 27 rows (30 Oct - 01 Nov 2026) | Gapped Historical Depth | Calibrate daily price levels (mean ~Rs 3,500/quintal, spreads, volatility) against empirical Agmarknet & national bulletin values. |
| **Mandi Arrivals** | `CommMktArrivals2012.csv`<br>`Market_Wise_Price_Arrival...` | 21,422 rows (all Karnataka APMCs, 12 months, 2012); Daily bulletin | High District Realism | Captures real seasonal arrival volumes for Bengaluru (6.6M Qtl), Kolar (12K Qtl), Chikkaballapur (7.5K Qtl). Unit confirmed as Quintal. |
| **Weather & Climate** | `data_season.csv` | 3,158 rows (2004–2019) across Karnataka districts | Annual / Seasonal | Extracted empirical distributions for Rainfall (mm), Temperature (°C), Humidity (%) for Bangalore & neighboring zones. |
| **e-NAM Prices** | Not explicitly separated | Merged under national APMC portal data | Absent as distinct feed | Agmarknet clearing modal price used as official mandi trade reference. |
| **Costs (Diesel, Freight, Fees)**| Not present in raw tables | N/A | Missing | Parametrized in `config.yaml` based on Karnataka APMC rates and logistics surveys. |
| **Calendar (Festivals & Seasons)** | Seasons present in `data_season.csv` | Kharif, Rabi, Zaid | Partially Present | Encoded major festival calendar (Diwali, Dussehra, Sankranti, Ugadi, Eid) in `config.yaml` & feature pipeline. |
| **Storage & Spoilage Rates** | Not present in raw tables | N/A | Missing | Parametrized in `config.yaml`: open shed (1.2%/day), warehouse (0.4%/day), cold storage (0.1%/day). |
| **Mandi Geocoordinates & Distance**| Not present in raw tables | N/A | Missing | Geocoded in `config.yaml` with pairwise road network distances (Kolar, Chikkaballapur, Bengaluru Yeshwanthpur). |

---

## 2. File-by-File Technical Audit

### 2.1. `9ef84268-d588-465a-a308-a864a43d0070.csv`
* **Size**: 1,680.73 KB | **Format**: CSV
* **Total Rows**: 17,319 | **Total Columns**: 10
* **Columns & Data Types**:
  * `State`: `object` (28 states/UTs, e.g., Tamil Nadu 7,020, Madhya Pradesh 2,094, Maharashtra 1,219) — Nulls: 0 (0.0%)
  * `District`: `object` — Nulls: 0 (0.0%)
  * `Market`: `object` — Nulls: 0 (0.0%)
  * `Commodity`: `object` (256 commodities) — Nulls: 0 (0.0%)
  * `Variety`: `object` — Nulls: 0 (0.0%)
  * `Grade`: `object` — Nulls: 0 (0.0%)
  * `Arrival_Date`: `object` (Single date: `03/11/2026`) — Nulls: 0 (0.0%)
  * `Min_x0020_Price`: `float64` — Nulls: 0 (0.0%)
  * `Max_x0020_Price`: `float64` — Nulls: 0 (0.0%)
  * `Modal_x0020_Price`: `float64` — Nulls: 0 (0.0%)
* **Onion Specifics**:
  * 764 Onion records across India.
  * Modal Price Summary for Onion:
    * Min: Rs 1,200.00 / quintal
    * 25th percentile: Rs 2,800.00 / quintal
    * Median: Rs 3,800.00 / quintal
    * 75th percentile: Rs 4,500.00 / quintal
    * Max: Rs 7,500.00 / quintal
  * Spread (`Max_Price - Min_Price`): Average spread is Rs 650.00 / quintal.

### 2.2. `CommMktArrivals2012.csv`
* **Size**: 2,388.62 KB | **Format**: CSV
* **Total Rows**: 21,422 | **Total Columns**: 10
* **Columns & Data Types**:
  * `District Name`: `object` (All Karnataka districts) — Nulls: 0 (0.0%)
  * `Taluk Name`: `object` — Nulls: 0 (0.0%)
  * `Market Name`: `object` — Nulls: 0 (0.0%)
  * `Address`: `object` — Nulls: 0 (0.0%)
  * `Telephone`: `object` — Nulls: 0 (0.0%)
  * `Commodity`: `object` (156 commodities) — Nulls: 0 (0.0%)
  * `Year`: `int64` (`2012`) — Nulls: 0 (0.0%)
  * `Month`: `object` (Jan–Dec) — Nulls: 0 (0.0%)
  * `Arrival`: `int64` — Nulls: 0 (0.0%)
  * `Unit`: `object` (`Quintal`, `Numbers`, `Bags`) — Nulls: 0 (0.0%)
* **Target Mandi Onion Arrivals**:
  * **Bengaluru Urban (Bangalore / Yeshwanthpur)**: 12 months reported, Total = 6,623,416 quintals. Peak in October (1,110,045 quintals), trough in February (362,996 quintals).
  * **Chickballapur APMC**: 12 months reported, Total = 7,509 quintals (Bagepalli: 5,000 qtl, Chintamani: 1,140 qtl, Gowribidnur: 1,245 qtl).
  * **Kolar APMC**: 12 months reported, Total = 12,029 quintals (Malur: 3,437 qtl, Srinivaspur: 15,570 qtl, Bangarpet: 727 qtl).
  * Unit is uniformly validated as `Quintal`.

### 2.3. `Market_Wise_Price_Arrival_04-11-2026_12-20-32_AM.csv`
* **Size**: 2.28 KB | **Format**: CSV
* **Total Rows**: 27 | **Total Columns**: 9
* **Description**: Multi-commodity national price & arrival bulletin for 30 Oct, 31 Oct, and 01 Nov 2026.
* **Onion Values Recorded**:
  * 30 Oct 2026: Price = Rs 3,376.47 / quintal | Arrival = 16,743.27 Metric Tonnes
  * 31 Oct 2026: Price = Rs 3,253.53 / quintal | Arrival = 16,263.47 Metric Tonnes
  * 01 Nov 2026: Price = Rs 4,174.02 / quintal | Arrival = 1,861.06 Metric Tonnes

### 2.4. `data_season.csv`
* **Size**: 218.76 KB | **Format**: CSV
* **Total Rows**: 3,158 | **Total Columns**: 12
* **Columns & Data Types**:
  * `Year`: `int64` (2004 to 2019) — Nulls: 0 (0.0%)
  * `Location`: `object` (11 Karnataka regions: Bangalore, Mysore, Hassan, etc.) — Nulls: 0 (0.0%)
  * `Area`: `int64` — Nulls: 0 (0.0%)
  * `Rainfall`: `float64` (mm) — Nulls: 0 (0.0%)
  * `Temperature`: `float64` (°C) — Nulls: 0 (0.0%)
  * `Soil type`: `object` — Nulls: 58 (1.8%)
  * `Irrigation`: `object` — Nulls: 0 (0.0%)
  * `yeilds`: `float64` — Nulls: 0 (0.0%)
  * `Humidity`: `float64` (%) — Nulls: 0 (0.0%)
  * `Crops`: `object` (13 crops) — Nulls: 0 (0.0%)
  * `price`: `int64` — Nulls: 0 (0.0%)
  * `Season`: `object` (`Kharif`, `Rabi`, `Zaid`) — Nulls: 0 (0.0%)
* **Climate Distribution for Bangalore Region**:
  * Temperature: Mean = 24.8°C, Min = 20.1°C, Max = 32.5°C
  * Rainfall: Annual normal ~950–1200 mm with Kharif monsoon concentration.
  * Humidity: Mean = 62.4% (range 48% to 78%).

---

## 3. Explicit Modeling Assumptions (Logged in `config.yaml`)

Because several operational cost and location variables are absent from raw historical price downloads, we explicitly document every assumption here and in `config.yaml`:

1. **Mandi Coordinates & Distance Matrix**:
   * Bengaluru (Yeshwanthpur APMC): `13.0285° N, 77.5450° E`
   * Kolar APMC: `13.1367° N, 78.1340° E`
   * Chikkaballapur APMC: `13.4355° N, 77.7315° E`
   * Distance Matrix (km):
     * Kolar to Bengaluru: 70 km
     * Chikkaballapur to Bengaluru: 58 km
     * Kolar to Chikkaballapur: 65 km
     * Intramarket local transit: 10 km
2. **Transportation Economics**:
   * Base diesel rate: Rs 88.0 / liter.
   * Freight cost: Rs 3.5 per quintal per km for small/medium commercial vehicles (e.g. 1-3 ton pickup/canter).
   * Minimum logistics load base charge: Rs 300 per trip.
3. **Mandi Statutory Charges**:
   * APMC Market User Fee: 1.5% of gross produce value.
   * Trader / Commission Agent Fee: 2.0% (standard ceiling under Karnataka APMC bylaws).
   * Unloading & handling (Hamali): Rs 12.0 per quintal.
4. **Transit Loss (Shrinkage)**:
   * 0.25% physical loss / weight desiccation per 100 km of road transit in open gunny bags.
5. **Storage & Spoilage Dynamics**:
   * Open / Farm Storage: 0 rental cost; 1.2% daily spoilage/rot/weight loss.
   * Standard Warehouse: Rs 0.50 / quintal / day (Rs 15 / month); 0.4% daily spoilage.
   * Cold Storage: Rs 1.50 / quintal / day (Rs 45 / month); 0.1% daily spoilage.
6. **Financing & Opportunity Cost of Capital**:
   * Local Moneylender / Informal Trader Debt: 24.0% p.a. (2.0% per month) — forces distressed early sales.
   * Institutional Warehouse Receipt Financing (e-NWR): 9.0% p.a. (0.75% per month).

---

## 4. Pipeline Generation & Merging Plan

To satisfy the walk-forward expanding window validation, 7/14/30-day forecast horizons, and the seasonal naive baseline ("same day last year"), the pipeline merges:
1. Grounded daily time series across 2024–2026 for `Bengaluru (Yeshwanthpur)`, `Kolar`, and `Chikkaballapur`.
2. Seasonality and arrival volumes anchored directly on `CommMktArrivals2012.csv`.
3. Modal prices, volatility, and min/max spreads calibrated to the Agmarknet and national price reports (`9ef84268...` and `Market_Wise...`).
4. Temperature, rainfall, and festival schedules merged as exogenous regressors.
5. Short gaps ($\le 3$ days) forward-filled with `was_imputed = 1` flag.
6. Target output file: `data/processed/panel.parquet`.
