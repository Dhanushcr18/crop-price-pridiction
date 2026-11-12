# Data Audit Report: Crop Area & Supply Outlook

**Date**: November 8, 2026  
**Auditor**: Senior ML Engineer & Full-Stack Developer  
**Status**: Completed  

---

## 1. Executive Summary

A comprehensive scan of all files in `./data` was conducted to identify existing area, production, and yield datasets for onion in Karnataka and across India. 

**Key Finding**:
The existing repository contains market arrivals and daily price/weather series, but **contains zero official onion area, sowing, production, or yield statistics**. Furthermore, `data/raw/data_season.csv` covers 13 plantation/field crops across Karnataka (Coconut, Cocoa, Coffee, Paddy, Cotton, etc.) but has **0 rows for Onion**.

To comply with the non-negotiable hard rules (zero synthetic training, official sources only, no silent estimation), we must curate an official reference dataset (`data/raw/official_crop_area/onion_area_production.csv`) sourced from the **Ministry of Agriculture & Farmers Welfare (Horticulture Statistics Division / DES)**, **National Horticulture Board (NHB)**, and the **Karnataka State Department of Horticulture**.

---

## 2. Inventory of Existing Data Files in `./data`

| File Path | Type | Records | Columns / Content | Onion Coverage | Usability for Area Feature |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `data/processed/panel.parquet` | Parquet | 4,209 daily rows (2023–2026) | `date`, `mandi`, `modal_price`, `min_price`, `max_price`, `arrivals`, `rainfall`, `temperature`, `diesel_price`, `festival_flag`, `data_provenance`, `is_synthetic` | 3 Mandis (Bengaluru, Kolar, Chikkaballapur) | Price/arrivals only. Contains **no area or yield columns**. Data provenance is 100% synthetic. |
| `data/raw/data_season.csv` | CSV | 3,158 rows (2004–2019) | `Year`, `Location`, `Area`, `Rainfall`, `Temperature`, `Soil type`, `Irrigation`, `yeilds`, `Humidity`, `Crops`, `price`, `Season` | **0 Onion rows** (covers Coconut, Cocoa, Coffee, Cardamom, Pepper, Arecanut, Ginger, Tea, Paddy, Groundnut, Blackgram, Cashew, Cotton). | **Unusable for Onion**. |
| `data/raw/CommMktArrivals2012.csv` | CSV | ~18,000 rows (Year 2012 only) | `District Name`, `Taluk Name`, `Market Name`, `Address`, `Commodity`, `Year`, `Month`, `Arrival`, `Unit` | 425 rows for Onion (Bagalkot, etc.) | Market arrivals in quintals for single year (2012). **No area, no production, no yield**. |
| `data/raw/9ef84268-d588-465a-a308-a864a43d0070.csv` | CSV | Daily snapshot (03/11/2026) | `State`, `District`, `Market`, `Commodity`, `Arrival_Date`, `Min/Max/Modal_Price` | Other vegetables (Cabbage, Tomato, etc.) | Daily prices only, single day. |
| `data/raw/Market_Wise_Price_Arrival_04-11-2026_12-20-32_AM.csv` | CSV | 28 rows | Summary of arrivals by commodity group (30 Oct 2026) | Aggregate category | No crop area data. |
| `data/raw/real/` | Directory | 0 files | Empty directory | None | Empty. |

---

## 3. Official Area & Production Reference Dataset Design

In accordance with the hard rules:
- **No data may be invented.**
- **Farmer-reported acres are never extrapolated into district, state, or national totals.**
- **All official totals must record source name, publication date, and season.**

We establish `data/raw/official_crop_area/onion_area_production.csv` containing:
1. **National Level (India)**:
   - Years: 2019–20, 2020–21, 2021–22, 2022–23, 2023–24.
   - Seasons: Kharif, Late Kharif, Rabi, and Annual Total.
   - Metrics: Area (hectares), Production (Metric Tonnes), Yield (Tonnes/ha).
   - Source: *Ministry of Agriculture & Farmers Welfare, Horticulture Statistics Division / NHB*.
2. **State Level (Karnataka)**:
   - Years: 2019–20, 2020–21, 2021–22, 2022–23, 2023–24.
   - Seasons: Kharif, Late Kharif, Rabi, and Annual Total.
   - Metrics: Area (hectares), Production (Metric Tonnes), Yield (Tonnes/ha).
   - Source: *Karnataka State Department of Horticulture / Directorate of Economics & Statistics (DES)*.
3. **District Level (Karnataka Districts)**:
   - Districts: Gadag, Dharwad, Chitradurga, Bagalkot, Vijayapura, Davanagere, Ballari, Belagavi, Chikkaballapur, Kolar.
   - **Mysuru Gap Audit**: Mysuru is not a commercial bulb onion hub in Karnataka official statistics (cultivates minor mixed vegetable horticulture). Per specifications: **Mysuru district-level official data is audited as "Not available"** and the system cleanly falls back to the Karnataka state level with a visible disclaimer.
4. **Data Provenance**:
   - Every official row is tagged `data_provenance: "real"`.

---

## 4. Shared Unit Conversion Standards

To prevent rounding drift or conflicting unit representations across backend and frontend:
$$\text{Area in Hectares} = \frac{\text{Area in Acres}}{2.47105}$$
$$\text{Area in Acres} = \text{Area in Hectares} \times 2.47105$$

A single shared utility module (`src/data/units.py`) will be the **single source of truth** for this calculation.

