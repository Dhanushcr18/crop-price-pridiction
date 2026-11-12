# Karnataka APMC Data Coverage Matrix (Strict Real Data Audit)

**Audit Date**: 2026-11-12 20:03:38  
**Target Region**: Karnataka (31 Districts, 148 APMC Mandis)  
**Total Pairs Evaluated**: 444  

---

## 1. Executive Summary & Tier Distribution

| Coverage Tier | Definition | Pairs | Share (%) | Model Deployment Rule |
|---|---|---|---|---|
| **Tier A** | >=730 days continuous real history, >=60% reporting, latest <=10d | **0** | 0.0% | Full Multi-Horizon Conformal LightGBM (Allowed) |
| **Tier B** | >=365 days real history, >=40% reporting, latest <=30d | **0** | 0.0% | Conservative Baseline / Cautious (Allowed) |
| **Tier C** | <365 days real history or missing active prices | **444** | **100.0%** | **No Model / Baseline / Uncovered (Model Disabled)** |

> [!IMPORTANT]
> **Strict Tier C Classification**: In strict compliance with the provenance gate, zero synthetic rows or unverified cross-mandi mappings are permitted. Because live Karnataka APMC reporting is currently missing in the primary OGD snapshot, **100% of Karnataka mandi pairs are designated as Tier C**.
> 
> The application will display **"Not available"** and **"No trained model yet"** until verified multi-year Karnataka history is backfilled.

---

## 2. Sample Karnataka APMC Pair Status (All Tier C)

| District | APMC Mandi | Crop | Verified Price Rows | Latest Price Date | Coverage Tier | Status / Action Required |
|---|---|---|---|---|---|---|
| Bagalakote | Badami | Onion | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Badami | Potato | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Badami | Tomato | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Bagalkot | Onion | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Bagalkot | Potato | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Bagalkot | Tomato | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Bilagi | Onion | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Bilagi | Potato | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Bilagi | Tomato | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Hungund | Onion | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Hungund | Potato | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Hungund | Tomato | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Jamkandi | Onion | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Jamkandi | Potato | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Jamkandi | Tomato | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Mahalingapura | Onion | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Mahalingapura | Potato | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bagalakote | Mahalingapura | Tomato | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bengaluru Rural | Doddaballapur | Onion | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bengaluru Rural | Doddaballapur | Potato | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bengaluru Rural | Doddaballapur | Tomato | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bengaluru Urban | Bengaluru (Yeshwanthpur) | Onion | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bengaluru Urban | Bengaluru (Yeshwanthpur) | Potato | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bengaluru Urban | Bengaluru (Yeshwanthpur) | Tomato | 0 | Not available | **Tier C** | Model Blocked (Tier C) |
| Bengaluru Urban | Bengaluru (Binny Mill) | Onion | 0 | Not available | **Tier C** | Model Blocked (Tier C) |

---

## 3. Backfill Remediation Roadmap
To upgrade Karnataka APMC pairs from **Tier C** to **Tier A**:
1. Download 2021–2026 Karnataka APMC price archives from Agmarknet portal (`SA_Pri_Month.aspx`).
2. Run `python scripts/backfill_karnataka.py`.
3. Ingestion will verify raw source signatures and update tiers objectively without synthetic interpolation.
