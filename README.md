# ⚠️ SYNTHETIC DATA - NOT FOR REAL DECISIONS ⚠️

> [!CAUTION]
> **SYNTHETIC DATA - NOT FOR REAL DECISIONS**
> The current baseline data panel contains generated/synthetic rows due to the absence of continuous historical Agmarknet daily price series in the initial download files.
> This repository is strictly for architecture validation and MUST NOT be used for real harvesting or commercial sales decisions.
> When real Agmarknet CSV files are added to `data/raw/real/`, the pipeline will rebuild the panel strictly from real data and remove this warning.

---

# Farmer Sell Advisor (Onion) 🧅
### Production-Grade Full-Stack Decision Intelligence Web Platform

**Farmer Sell Advisor** is an end-to-end decision intelligence platform engineered to advise smallholder onion farmers in Karnataka (**Kolar**, **Chikkaballapur**, and **Bengaluru Yeshwanthpur APMC**) on:
1. **WHERE to sell**: Spatial arbitrage ranking nearby mandis by net realized return after deducting transport freight, APMC market fees, agent commissions, and transit shrinkage.
2. **WHEN to sell**: Temporal arbitrage simulating holding produce for 7, 14, or 30 days vs. selling today using a 5,000-draw Monte Carlo simulation incorporating post-harvest rot/decay rates and carrying debt interest.
3. **At what EXPECTED PRICE**: Probabilistic price forecasting stating calibrated uncertainty ranges (**P10 downside, P50 expected, P90 upside**) rather than misleading point forecasts.

> **Hard Rules Enforced in System**:
> 1. **The farmer makes the final decision**; the system only advises.
> 2. **Every forecast must state its uncertainty** ($P10 \le P50 \le P90$), never a single price as certain.
> 3. **DATA_PROVENANCE Gate**: The pipeline refuses to train if the panel contains synthetic rows unless real Agmarknet CSVs are provided in `data/raw/real/`.
> 4. **Low Confidence Flagging**: Any horizon where the ML model does not beat the Naive baseline or where coverage falls outside 70%–90% displays a prominent yellow "Low Confidence" badge.

---

## 1. System Architecture

```
├── backend/                        # FastAPI REST API Backend
│   ├── main.py                     # API routes, middleware, rate-limiting, lifespan loading
│   ├── models_loader.py            # Singleton artifact loader, inference, conformal offsets
│   ├── schemas.py                  # Pydantic v2 validation models
│   ├── requirements.txt            # Python dependencies
│   └── Dockerfile                  # Container definition for backend
├── frontend/                       # Next.js 14 + TypeScript + Tailwind CSS Frontend
│   ├── src/
│   │   ├── app/                    # App Router pages
│   │   │   ├── page.tsx            # Home / Advisor Form & Results (mobile-first)
│   │   │   ├── transparency/page.tsx # Model Transparency (live /api/model-report)
│   │   │   ├── about/page.tsx      # How it Works & Farmer Field Feedback
│   │   │   ├── layout.tsx          # Root layout & metadata
│   │   │   └── globals.css         # High-contrast CSS, Devanagari & Kannada typography
│   │   ├── components/             # Reusable UI components
│   │   │   ├── Header.tsx          # Nav, i18n switcher, synthetic & stale data banners
│   │   │   ├── Footer.tsx          # Model version, data dates, farmer autonomy disclaimer
│   │   │   ├── FanChart.tsx        # Interactive SVG P10-P90 uncertainty fan chart
│   │   │   ├── MandiCard.tsx       # Top 3 mandi rank cards with net price deductions
│   │   │   ├── HoldSimulation.tsx  # Monte Carlo hold vs sell + e-NWR credit toggle
│   │   │   ├── StorageOptions.tsx  # Nearby storage facilities, rental & rot rates
│   │   │   ├── VoiceInput.tsx      # Web Speech API input with mic button
│   │   │   └── VoiceOutput.tsx     # Web Speech synthesis "Read Aloud" button
│   │   ├── i18n/
│   │   │   └── translations.ts     # Complete UI string dictionaries (en, hi, kn)
│   │   ├── lib/
│   │   │   └── api.ts              # API fetch client with localStorage offline caching
│   │   └── types/api.ts            # Full TypeScript interfaces
│   ├── Dockerfile                  # Multi-stage production container
│   ├── package.json
│   └── tailwind.config.ts
├── src/                            # Core Machine Learning & Decision Engine
│   ├── data/pipeline.py            # Data cleaning, unit checks, gap-filling, provenance tagging
│   ├── models/forecast.py          # LightGBM Quantile Regressors (P10/P50/P90) + Optuna
│   ├── decision/where_to_sell.py   # Mandi net price optimizer
│   ├── decision/when_to_sell.py    # Monte Carlo spoilage & credit simulator
│   ├── agent/advisor.py            # Multilingual LLM Agent (English, Hindi, Kannada)
│   └── evaluation/evaluate.py      # Historical out-of-sample backtest engine
├── models/                         # Serialized LightGBM models & conformal offsets
├── reports/                        # Markdown audit & backtest reports
├── tests/                          # Automated Pytest Suite (27 tests)
│   ├── test_api.py                 # API schema, net price, quantile monotonicity tests
│   ├── test_web_flow.py            # End-to-end user flows, low confidence & banner triggers
│   ├── test_provenance.py          # Data provenance and training refusal tests
│   ├── test_leakage.py             # Temporal walk-forward leakage verification
│   ├── test_optimizer.py           # Mandi ranking and freight monotonicity tests
│   ├── test_quantiles.py           # Non-crossing quantile monotonicity ($P10 \le P50 \le P90$)
│   └── test_simulator.py           # Monte Carlo decay and debt impact tests
├── docker-compose.yml              # Orchestrates Backend (port 8000) & Frontend (port 3000)
├── config.yaml                     # Central parameters & assumptions
├── Makefile / make.bat / run.py    # Standardized build commands
└── README.md
```

---

## 2. Quickstart & Deployment

### Option A: Run via `make web` (Recommended for Local Dev)
```bash
# Start backend (FastAPI :8000) and frontend (Next.js :3000) simultaneously
make web
# or on Windows:
.\make.bat web
# or directly:
python run.py web
```
- Open Frontend: [http://localhost:3000](http://localhost:3000)
- Open Interactive API Docs (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)

### Option B: Run via Docker Compose
```bash
# Build and start all containers
docker-compose up --build
```
Both services will boot with automatic healthchecks.

---

## 3. Environment Variables

Create a `.env` file (copied from `.env.example`):
```ini
# Server-side Anthropic LLM API Key (NEVER exposed to the browser)
ANTHROPIC_API_KEY=your_key_here

# Frontend API Endpoint
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 4. API Endpoints Specification

All endpoints validate with Pydantic v2, enforce rate limits, and provide structured OpenAPI documentation at `http://localhost:8000/docs`:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | System health, model version, last data date, and provenance tag (`real` vs `synthetic`). |
| `GET` | `/api/mandis` | List of target APMC mandis with lat/lon coordinates, APMC tier, and road distances. |
| `GET` | `/api/forecast?mandi=Kolar` | Multi-horizon P10, P50, and P90 price forecasts for 7, 14, and 30 days ahead with confidence status. |
| `POST` | `/api/where-to-sell` | Ranks nearby mandis by net realized price deducting freight, fees, and shrinkage. |
| `POST` | `/api/when-to-sell` | 5,000-draw Monte Carlo simulation of holding vs selling today under post-harvest decay and interest. |
| `POST` | `/api/advice` | Plain-language recommendation in English, Hindi, or Kannada with farmer autonomy disclaimers. |
| `GET` | `/api/model-report` | Live transparency report pulling benchmark baseline metrics, horizon coverage audits, and assumptions. |

---

## 5. Mobile-First Page Guide (Works on 360px Viewports)

### 1. Home / Sell Advisor (`/`)
- **Large Input Controls**: High-contrast, touch-friendly dropdowns and inputs for Crop (Onion), Mandi (Kolar, Chikkaballapur, Bengaluru), Quantity in quintals, Storage type, and Trader debt status.
- **Voice Speech Input**: Tap-to-speak button powered by the Web Speech Recognition API (`kn-IN`, `hi-IN`, `en-IN`).
- **Results Rendered in Strict Required Order**:
  1. *One-Sentence Plain-Language Answer*: Clear bottom-line recommendation with a **"Read Aloud"** voice synthesis button.
  2. *Price Forecast Fan Chart*: Interactive SVG fan chart displaying the $P10–P90$ shaded uncertainty band and $P50$ expected modal trajectory.
  3. *Top 3 Mandis as Cards*: Net price realized after deducting freight, APMC statutory fee (1.5%), commission (2.0%), and transit shrinkage (0.25%/100km), alongside gain over local mandi and total rupee value for harvest lot.
  4. *Hold-vs-Sell Simulation*: Probability that waiting beats selling today, best day to sell, and $P10$ worst-case downside outcome.
  5. *Produce Borrowing Comparison*: "What if I could borrow against stored produce?" toggle comparing 9% e-NWR warehouse loans vs 24% informal trader debt.
  6. *Nearby Storage Options*: Storage facilities with daily costs, decay rates, and safe capacities.
- **Farmer Autonomy Banner**: Prominent notice stating: *"This is advice, the decision is yours."*
- **Offline Resilient**: Uses `localStorage` caching to surface the last generated advisory if connection drops.

### 2. Model Transparency Page (`/transparency`)
- Pulls live data dynamically from `/api/model-report`.
- **Benchmark Comparison Table**: Compares LightGBM Quantile Regressors against Naive (`tomorrow = today`), Seasonal Naive (same day last year), and 7-Day Moving Average.
- **Horizon Coverage Audit**: Audits $P10–P90$ interval coverage against the strict 70%–90% target band, displaying warning badges for any under-covered horizon.
- **Explicit Assumptions vs Measured Data**: Full disclosure of parametrized freight rates, APMC deductions, decay rates, and interest rates.
- **Known Real-World Boundaries & Limitations**: Clear disclosure of market random walks, lack of bulb grade distinction, and moneylender contracts.

### 3. About / How it Works (`/about`)
- Educational breakdown of why small farmers lose ₹5,000–₹20,000 per cycle and 20–30% in post-harvest decay.
- Technical explanation of the optimization formulas, Monte Carlo decay modeling, and conformalized quantile regression.
- **Farmer Field Feedback Form**: Interactive form allowing farmers and extension officers to submit real-time mandi rate observations or transport discrepancy reports.

---

## 6. Automated Test Suite (27 Tests)

Run the full automated test suite:
```bash
pytest -v
# or: make test
```

### Verified Test Categories:
- **API Tests (`tests/test_api.py`)**: Validates health, mandis, quantile monotonicity ($P10 \le P50 \le P90$), net price math, Monte Carlo probability bounds in $[0, 100]\%$, multilingual advice, and Pydantic input validation.
- **Web Flow Tests (`tests/test_web_flow.py`)**: Tests the sample farmer flow across English, Hindi, and Kannada, low-confidence badge triggering, synthetic banner triggering, stale data warning logic, and report fidelity.
- **Provenance Gate Tests (`tests/test_provenance.py`)**: Tests strict refusal to train on synthetic rows when real data is missing.
- **Model Integrity Tests (`tests/test_quantiles.py`, `tests/test_leakage.py`, `tests/test_optimizer.py`, `tests/test_simulator.py`)**: Tests non-crossing quantiles, absence of feature leakage, freight monotonicity with distance, and spoilage decay bounds.
