# Karnataka Mandi Master Mapping Report

**Date**: 16 November 2026  
**Document Analyzed**: `Crop_price_of_all_mandies_of_karnataka.pdf` (115 markets)  
**Master Registry**: `data/master/mandis.csv` & `data/master/districts.csv`  

---

## 1. Summary of Mapping Status

| Total Markets in Bulletin | Resolved in Master | Coordinate Source |
| :---: | :---: | :---: |
| **115** | **115** (100%) | Official APMC: 29 \| Approximate: 85 \| Assumption: 1 |

All 115 markets in the official KSAMB bulletin now map to a known Karnataka taluk/APMC market yard with valid latitude/longitude coordinates and district associations.

---

## 2. Market Mapping Decisions & Office Confirmations

### Section A: To Confirm with the Market Office (Official Inquiry)

| Market Name in PDF | Mapped Identity | Coordinate Source | District | Justification & Note |
| :--- | :--- | :--- | :--- | :--- |
| **BENGALURU** | Bengaluru (Yeshwanthpur) | **Assumption** | Bengaluru Urban (`BLR_U`) | **User Decision**: Inferred from commodity mix (trades Onions [10,823 qtl], Grains, Pulses, Commercial crops). Mapped to Yeshwanthpur RMC Yard (13.0189° N, 77.5556° E). Tagged `Assumption`. |
| **BINNY MILL (F&V)** | Binny Mill (F&V) | **official_apmc** | Bengaluru Urban (`BLR_U`) | Maintained as an independent, distinct market yard (trades Fruits & Vegetables exclusively). Located at 12.9698° N, 77.5684° E. |

*Action Required*: During next ground audit with KSAMB Rajajinagar/Yeshwanthpur head office, confirm whether bulletin row 13 represents the Yeshwanthpur Yard exclusively or city-wide aggregate clearing.

---

## 3. Name Normalization & Variant Spellings Resolved

The following historical phonetic/government name changes have been resolved to their canonical identities:

| PDF Header Name | Canonical English | Kannada Name | District | Coordinate Source |
| :--- | :--- | :--- | :--- | :--- |
| **BALLARI** | Ballari | ಬಳ್ಳಾರಿ | Ballari | `official_apmc` |
| **BELAGAVI** | Belagavi | ಬೆಳಗಾವಿ | Belagavi | `official_apmc` |
| **CHINCOLI** | Chincholi | ಚಿಂಚೋಳಿ | Kalaburagi | `approximate` |
| **ENDI** | Indi | ಇಂಡಿ | Vijayapura | `approximate` |
| **HUBBALLI** | Hubballi | ಹುಬ್ಬಳ್ಳಿ | Dharwad | `official_apmc` |
| **KALABURAGI** | Kalaburagi | ಕಲಬುರಗಿ | Kalaburagi | `official_apmc` |
| **MYSURU** | Mysuru | ಮೈಸೂರು | Mysuru | `official_apmc` |
| **SHIVAMOGGA** | Shivamogga | ಶಿವಮೊಗ್ಗ | Shivamogga | `official_apmc` |
| **VIJAYAPURA** | Vijayapura | ವಿಜಯಪುರ | Vijayapura | `official_apmc` |
