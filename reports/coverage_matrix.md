# Karnataka Coverage Matrix & Tier Audit Report

**Date of Analysis**: 2026-11-16  
**Data Provenance**: 100% Real APMC Daily Clearing Records (KSAMB Bulletin: 2026-11-11)  
**Total Monitored Markets**: 115 Karnataka APMC Markets  
**Total Monitored Commodities**: 102 Crops across 8 Categories  
**Total Universe of Pairs**: 11,730 (`crop` × `mandi`)  

---

## 1. Executive Summary & Tier Distribution

> [!IMPORTANT]
> **Strict Provenance & Honesty Gate**:
> As of **2026-11-16**, only **1 day** of verified Karnataka mandi clearing history (`2026-11-11`) exists in the panel.
> In accordance with project integrity rules:
> - **Zero pairs qualify for Tier A** (requires at least 2.0 continuous years of real daily reporting).
> - **All ML forecasting, quantile interval models, and time-series projections are strictly disabled** across all crops and mandis.
> - Exactly **591 pairs** qualify for **Tier B** ("Latest price only", displaying verified reported prices with date and source).
> - Exactly **11,139 pairs** remain in **Tier C** ("No recent report", showing "Not available").
> - **No synthetic row, LLM hallucination, or forward fill has been or will ever be used to promote any pair to Tier A.**

| Tier Classification | Requirement | Count | Share (%) | User-Facing Action |
| :--- | :--- | :---: | :---: | :--- |
| **Tier A (Forecast Available)** | $\ge 2$ years real history, $\ge 60\%$ reporting days, last report $\le 7$ days | **0** | **0.0%** | ML Forecast & Uncertainty Fan Chart active |
| **Tier B (Latest Price Only)** | $\ge 1$ verified real report in panel | **591** | **5.04%** | Display today's/latest reported price card; forecasts disabled |
| **Tier C (No Recent Report)** | 0 reports in panel or stale beyond freshness gate | **11,139** | **94.96%** | Display "Not available", no price returned |

---

## 2. Crop-Level Coverage Summary (Top Commodities by Market Breadth)

The table below outlines reporting market breadth for the leading commodities in the 2026-11-11 KSAMB bulletin:

| Commodity | Category | Native Unit | Reporting Markets | Total Real Rows | Days Since Latest | Tier Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **maize** | crop | Quintal | 46 mandis | 47 | 5 days | **Tier B** (46 markets) / **Tier C** (remainder) |
| **paddy** | crop | Quintal | 21 mandis | 31 | 5 days | **Tier B** (21 markets) / **Tier C** (remainder) |
| **tomato** | crop | Quintal | 18 mandis | 18 | 5 days | **Tier B** (18 markets) / **Tier C** (remainder) |
| **arecanut** | crop | Quintal | 18 mandis | 45 | 5 days | **Tier B** (18 markets) / **Tier C** (remainder) |
| **rice** | crop | Quintal | 16 mandis | 23 | 5 days | **Tier B** (16 markets) / **Tier C** (remainder) |
| **bengalgram** | crop | Quintal | 14 mandis | 14 | 5 days | **Tier B** (14 markets) / **Tier C** (remainder) |
| **beans** | crop | Quintal | 14 mandis | 14 | 5 days | **Tier B** (14 markets) / **Tier C** (remainder) |
| **green chilly** | crop | Quintal | 14 mandis | 14 | 5 days | **Tier B** (14 markets) / **Tier C** (remainder) |
| **ragi** | crop | Quintal | 14 mandis | 14 | 5 days | **Tier B** (14 markets) / **Tier C** (remainder) |
| **onion** | crop | Quintal | 14 mandis | 18 | 5 days | **Tier B** (14 markets) / **Tier C** (remainder) |
| **green ginger** | crop | Quintal | 13 mandis | 13 | 5 days | **Tier B** (13 markets) / **Tier C** (remainder) |
| **carrot** | crop | Quintal | 13 mandis | 13 | 5 days | **Tier B** (13 markets) / **Tier C** (remainder) |
| **brinjal** | crop | Quintal | 13 mandis | 15 | 5 days | **Tier B** (13 markets) / **Tier C** (remainder) |
| **cotton** | crop | Quintal | 13 mandis | 13 | 5 days | **Tier B** (13 markets) / **Tier C** (remainder) |
| **greengram** | crop | Quintal | 12 mandis | 12 | 5 days | **Tier B** (12 markets) / **Tier C** (remainder) |
| **jowar** | crop | Quintal | 12 mandis | 12 | 5 days | **Tier B** (12 markets) / **Tier C** (remainder) |
| **potato** | crop | Quintal | 11 mandis | 12 | 5 days | **Tier B** (11 markets) / **Tier C** (remainder) |
| **tur** | crop | Quintal | 11 mandis | 11 | 5 days | **Tier B** (11 markets) / **Tier C** (remainder) |
| **cabbage** | crop | Quintal | 10 mandis | 10 | 5 days | **Tier B** (10 markets) / **Tier C** (remainder) |
| **cucumbar** | crop | Quintal | 10 mandis | 10 | 5 days | **Tier B** (10 markets) / **Tier C** (remainder) |
| **groundnut** | crop | Quintal | 10 mandis | 10 | 5 days | **Tier B** (10 markets) / **Tier C** (remainder) |
| **bajra** | crop | Quintal | 9 mandis | 9 | 5 days | **Tier B** (9 markets) / **Tier C** (remainder) |
| **ladies finger** | crop | Quintal | 9 mandis | 9 | 5 days | **Tier B** (9 markets) / **Tier C** (remainder) |
| **ridgeguard** | crop | Quintal | 9 mandis | 9 | 5 days | **Tier B** (9 markets) / **Tier C** (remainder) |
| **beetroot** | crop | Quintal | 9 mandis | 9 | 5 days | **Tier B** (9 markets) / **Tier C** (remainder) |
| **soyabeen** | crop | Quintal | 8 mandis | 8 | 5 days | **Tier B** (8 markets) / **Tier C** (remainder) |
| **bitter gourd** | crop | Quintal | 8 mandis | 8 | 5 days | **Tier B** (8 markets) / **Tier C** (remainder) |
| **copra** | crop | Quintal | 8 mandis | 10 | 5 days | **Tier B** (8 markets) / **Tier C** (remainder) |
| **cauliflower** | crop | Quintal | 8 mandis | 8 | 5 days | **Tier B** (8 markets) / **Tier C** (remainder) |
| **wheat** | crop | Quintal | 8 mandis | 8 | 5 days | **Tier B** (8 markets) / **Tier C** (remainder) |

---

## 3. Freshness Status & Banner Gate

- **Reference Evaluation Date**: `2026-11-16`
- **Bulletin Date**: `2026-11-11`
- **Elapsed Age**: **5 days** (exceeds the 2-day freshness threshold)
- **UI Behavior**: Every Tier B card displays the prominent yellow banner:
  > **"Latest reported: 11 Nov 2026"**
  > Under no circumstance is an old report presented as today's live cleared price.

---

## 4. Path to Unlock Tier A Forecasts

To advance any Karnataka crop-mandi pair from Tier B to Tier A:
1. **Multi-Year Backfill**: Agmarknet daily historical records from **November 2024 through November 2026** (minimum 730 calendar days).
2. **Reporting Consistency**: Daily reporting on at least 60% of operating trading days (excluding Sundays and APMC notified holidays).
3. **Data Provenance**: Sourced strictly via official Agmarknet CSV downloads with raw file, page/line provenance and verifiable hashes.
