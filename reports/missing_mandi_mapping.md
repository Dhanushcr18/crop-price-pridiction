# Karnataka Mandi Master Mapping Report

**Date**: 13 November 2026  
**Document Analyzed**: `Crop_price_of_all_mandies_of_karnataka.pdf` (115 markets)  
**Master Registry**: `data/master/mandis.csv` & `data/master/districts.csv`  

---

## 1. Summary of Mapping Status

| Total Markets in PDF | Matched in Master | Unresolved / Variant Names |
| :---: | :---: | :---: |
| **115** | **101** (87.8%) | **14** (12.2%) |

All 101 matched markets have verified `district_en`, `lat`, `lon`, and `coord_source` (`official_apmc` or `approximate`).

---

## 2. Unresolved / Variant Mandi Names (14 Markets)

The following 14 markets appearing in the KSAMB bulletin require confirmation or canonical alias aliasing against `mandis.csv`:

| # | PDF Market Name | Likely Taluk / District | Suspected Canonical Match in Master | Candidate Coordinates | Status |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | **BENGALURU** | Bengaluru Urban | `bengaluru_yeshwanthpur` or `BANGALORE` | 13.0285° N, 77.5450° E | **Pending User Clarification (See Question Below)** |
| 2 | **BINNY MILL (F&V)** | Bengaluru Urban | `bengaluru_binny_mill` | 12.9698° N, 77.5684° E | Matched in master by raw name `BINNY MILL (F&V)` |
| 3 | **MYSURU** | Mysuru | `mysuru_bandipalya` (Listed as `MYSORE` in master) | 12.2850° N, 76.6710° E | Spelling alias (`MYSURU` vs `MYSORE`) |
| 4 | **CHIKKAMAGALURU** | Chikkamagaluru | Chikkamagaluru APMC Yard | 13.3161° N, 75.7720° E | Missing in `mandis.csv` |
| 5 | **ARAKALGUD** | Hassan | Arakalgud APMC Yard | 12.7667° N, 76.0500° E | Missing in `mandis.csv` |
| 6 | **CHINCOLI** | Kalaburagi | Chincholi APMC Yard | 17.4667° N, 77.4167° E | Missing in `mandis.csv` |
| 7 | **ENDI** | Vijayapura | Indi APMC Sub-market Yard | 17.1833° N, 75.9667° E | Phonetic spelling (`ENDI` for `Indi`) |
| 8 | **HANUR** | Chamarajanagar | Hanur APMC Sub-market Yard | 12.0833° N, 77.3000° E | Missing in `mandis.csv` |
| 9 | **JEVARGI** | Kalaburagi | Jevargi APMC Yard | 17.0167° N, 76.7667° E | Missing in `mandis.csv` |
| 10 | **KAMPLI** | Ballari / Vijayanagara | Kampli APMC Yard | 15.4000° N, 76.6167° E | Missing in `mandis.csv` |
| 11 | **KANAKAGIRI** | Koppal | Kanakagiri APMC Yard | 15.5667° N, 76.4167° E | Missing in `mandis.csv` |
| 12 | **KUDLIGI** | Vijayanagara / Ballari | Kudligi APMC Yard | 14.9000° N, 76.3833° E | Missing in `mandis.csv` |
| 13 | **MALAVALLI** | Mandya | Malavalli APMC Yard | 12.3833° N, 77.0500° E | Missing in `mandis.csv` |
| 14 | **SHIGGAON** | Haveri | Shiggaon APMC Yard | 14.9833° N, 75.2333° E | Missing in `mandis.csv` |
| 15 | **YARAHALLI** | Mysuru | Yarahalli Sub-market Yard | 12.3000° N, 76.6500° E | Missing in `mandis.csv` |

---

## 3. Explicit User Question: "Yeshwanthpur"

> [!IMPORTANT]
> **Clarification Required from User**:
> In the official KSAMB 115-market report, Bengaluru city has two distinct market headers:
> 1. `13] MARKET: BENGALURU` (trades Grains, Commercial crops, Oilseeds, and Onions with 10,823 qtl arrivals)
> 2. `16] MARKET: BINNY MILL (F&V)` (trades Fruits & Vegetables)
>
> In agricultural trade and Agmarknet records, Yeshwanthpur is the main Bangalore APMC regulated market yard (RMC Yard, Yeshwanthpur).  
> **Which market should be mapped to "Yeshwanthpur" in the advisor model?**
> - Option A: `BENGALURU` is the Yeshwanthpur main APMC yard.
> - Option B: `BINNY MILL (F&V)` is Yeshwanthpur.
>
> Per instructions, we do not guess and await your confirmation.
