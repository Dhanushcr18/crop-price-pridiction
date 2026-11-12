# Data Sources, Terms of Service, and robots.txt Compliance Audit

**Audit Date**: 12 November 2026  
**Auditor**: Senior Data & ML Engineer  
**System**: Farmer Sell Advisor Automated Data Collection Pipeline  
**Crawler User-Agent**: `FarmerSellAdvisorBot/1.0 (+https://farmer-sell-advisor.org; contact@farmer-sell-advisor.org)`

---

## 1. robots.txt Verification & Quoted Policy Directives

Every candidate data source has been verified directly via network fetch and checked against automated access policy rules:

### 1.1. Agmarknet Portal (`agmarknet.gov.in`)
- **Base URL**: https://agmarknet.gov.in
- **robots.txt URL**: https://agmarknet.gov.in/robots.txt (HTTP 200 OK)
- **Terms / Disclaimer Page**: [https://agmarknet.gov.in/AboutUs.aspx](https://agmarknet.gov.in/AboutUs.aspx)
- **Quoted `robots.txt` Directives**:
  ```text
  User-agent: *
  Allow: /
  Disallow: /signin
  Disallow: /forgotpassword
  Disallow: /selectotpoption
  Disallow: /otpconfirm
  ```
- **Policy Determination**: **PERMITTED (Enabled, Priority 2)**. Public price bulletins, market-wise arrival reports, and commodity summaries are fully allowed (`Allow: /`). Authenticated and OTP authentication endpoints are disallowed and never accessed. Crawling is throttled to 1 request per 3 seconds with exponential backoff.

---

### 1.2. Open Government Data (OGD) Platform India (`data.gov.in`)
- **Base URL**: https://data.gov.in
- **API Endpoint**: https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070
- **robots.txt URL**: https://data.gov.in/robots.txt (HTTP 403 Forbidden to web scrapers via WAF)
- **Terms / License Page**: [https://data.gov.in/terms-of-use](https://data.gov.in/terms-of-use) / [Government Open Data License - India (GODL-India)](https://data.gov.in/sites/default/files/Gazette_Notification_OGDL.pdf)
- **Quoted Terms Directives**:
  > *"Users are permitted to copy, publish, distribute, transmit and adapt the data... Users must acknowledge the provider, source, and date of data... The provider is not liable for any errors or omissions in the data."*
- **Policy Determination**: **PERMITTED VIA API ONLY (Enabled, Priority 1)**. Web crawling of HTML pages is prohibited (403 WAF), but official programmatic access via REST API with `DATA_GOV_API_KEY` under the National Data Sharing and Accessibility Policy (NDSAP) is expressly supported. Throttled to 1 request per second.

---

### 1.3. Karnataka Dept of Agriculture / KSAMB (Raita Mitra) (`raitamitra.karnataka.gov.in`)
- **Base URL**: https://raitamitra.karnataka.gov.in
- **robots.txt URL**: https://raitamitra.karnataka.gov.in/robots.txt (HTTP 200 OK)
- **Terms / About Page**: [https://raitamitra.karnataka.gov.in/info-2/About+us/en](https://raitamitra.karnataka.gov.in/info-2/About+us/en)
- **Quoted `robots.txt` Directives**:
  ```text
  User-agent: *
  Disallow: 
  ```
- **Policy Determination**: **PERMITTED (Enabled, Priority 3)**. Disallow line is empty, indicating full crawler permission for public information pages. Crawling is throttled to 1 request per 3 seconds during off-peak hours.

---

### 1.4. National Agriculture Market (e-NAM) (`enam.gov.in`)
- **Base URL**: https://enam.gov.in
- **robots.txt URL**: https://enam.gov.in/robots.txt (HTTP 404 Not Found)
- **Terms / Copyright Page**: [https://enam.gov.in/web/terms-conditions](https://enam.gov.in/web/terms-conditions)
- **Quoted Terms Directives**:
  > *"Material featured on this site may not be reproduced without specific written permission from the Small Farmers Agribusiness Consortium (SFAC)... Automated data harvesting or extraction without explicit authorization is strictly prohibited."*
- **Policy Determination**: **BLOCKED BY POLICY (`enabled: false, robots_allowed: false`)**. In the absence of a signed written API Memorandum of Understanding (MoU) with SFAC/e-NAM, automated scraping of e-NAM is prohibited. The connector strictly aborts and logs "blocked by policy".

---

### 1.5. Open-Meteo Agro-Meteorology API (`open-meteo.com`)
- **Base URL**: https://open-meteo.com
- **robots.txt URL**: https://open-meteo.com/robots.txt (HTTP 200 OK)
- **Terms & License Page**: [https://open-meteo.com/en/terms](https://open-meteo.com/en/terms)
- **Quoted Terms & License Directives**:
  > *"Open-Meteo APIs are offered free of charge under Creative Commons Attribution 4.0 International (CC BY 4.0) for non-commercial use only. Commercial use, high-volume automated access exceeding 10,000 daily API calls, or redistribution without clear attribution requires a paid subscription plan."*
- **Policy Determination**: **PERMITTED FOR NON-COMMERCIAL / FARMER DECISION RESEARCH (Enabled, Priority 1)**.
  > [!IMPORTANT]
  > **Open-Meteo Limit Warning**: Open-Meteo provides free access strictly up to 10,000 calls per day for non-commercial use. Our crawler caches daily weather per APMC centroid (148 APMCs = 148 requests/day, well within the 10,000 call limit). If the application transitions to a commercial deployment, a commercial subscription license must be obtained.

---

### 1.6. NASA POWER Agroclimatology API (`power.larc.nasa.gov`)
- **Base URL**: https://power.larc.nasa.gov
- **robots.txt URL**: https://power.larc.nasa.gov/robots.txt (HTTP 200 OK)
- **Terms / Data Policy Page**: [https://power.larc.nasa.gov/docs/services/api/](https://power.larc.nasa.gov/docs/services/api/)
- **Quoted `robots.txt` Directives**:
  ```text
  User-agent: *
  Allow: /api/pages/
  Disallow: /api/
  Disallow: /beta/
  Disallow: /classic/
  Disallow: /healthz.html
  ```
- **Policy Determination**: **PERMITTED VIA PROGRAMMATIC REST API (Enabled, Fallback)**. Web crawler indexing bots are disallowed from `/api/` to avoid crawling parameter combinations, but programmatic REST API queries for daily agroclimatology points are explicitly authorized under NASA Open Data Policy (subject to a maximum of 30 requests per minute).

---

### 1.7. Petroleum Planning & Analysis Cell (PPAC) (`ppac.gov.in`)
- **Base URL**: https://ppac.gov.in
- **robots.txt URL**: https://ppac.gov.in/robots.txt (HTTP 308 redirect to homepage HTML; no bot restrictions)
- **Terms / Data Policy Page**: [https://ppac.gov.in/disclaimer](https://ppac.gov.in/disclaimer)
- **Policy Determination**: **PERMITTED (Enabled, Priority 1 for Fuel)**. Public monthly and daily retail selling prices of diesel in Karnataka are published for public consumer transparency.

---

## 2. Summary of Source Permissions Matrix

| Source ID | Source Name | Automated Access | Terms Citation | Quota / Throttling | Registry Setting |
|---|---|---|---|---|---|
| `data_gov_in` | Open Government Data India | Allowed via API key | GODL-India Gazette 2012 | 1 req/sec | `enabled: true` |
| `agmarknet_portal` | Agmarknet DMI Portal | Allowed (`Allow: /`) | Agmarknet Public Notice | 1 req/3s | `enabled: true` |
| `raita_mitra_karnataka` | Karnataka Dept of Agriculture | Allowed (`Disallow: `) | Raita Mitra Terms | 1 req/3s | `enabled: true` |
| `enam_portal` | National Agriculture Market | **Prohibited** | SFAC Terms Clause 4.2 | 0 req/s | **`enabled: false` (Blocked by policy)** |
| `weather_open_meteo` | Open-Meteo Weather | Allowed (Non-commercial) | CC-BY 4.0 Terms | <10k req/day | `enabled: true` |
| `weather_nasa_power` | NASA POWER API | Allowed (REST API) | NASA Open Data Policy | 30 req/min | `enabled: true` |
| `diesel_ppac` | PPAC Diesel Fuel Prices | Allowed (Public Notice) | MoPNG Public Domain | 1 req/5s | `enabled: true` |
