"""Farmer Sell Advisor - FastAPI Backend Application."""

import os
import sys
import time
import logging
from collections import defaultdict
from contextlib import asynccontextmanager
from typing import Dict, List, Optional

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, HTTPException, Request, Response, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from backend.schemas import (
    HealthResponse,
    MandiInfo,
    ForecastResponse,
    WhereToSellRequest,
    WhereToSellResponse,
    WhenToSellRequest,
    WhenToSellResponse,
    AdviceRequest,
    AdviceResponse,
    ModelReportResponse,
    AreaReportRequest,
    AreaReportResponse,
    AreaSummaryResponse,
    SupplyPriceOutlookResponse
)
from backend.models_loader import AdvisorService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s"
)
logger = logging.getLogger("farmer_advisor.api")

# Rate limiting settings (in-memory token bucket/counter)
RATE_LIMIT_REQUESTS = 120
RATE_LIMIT_WINDOW_SECONDS = 60
client_request_history: Dict[str, List[float]] = defaultdict(list)


def check_rate_limit(client_ip: str) -> bool:
    """Returns True if within rate limit, False if rate exceeded."""
    now = time.time()
    cutoff = now - RATE_LIMIT_WINDOW_SECONDS
    # Clean old requests
    client_request_history[client_ip] = [t for t in client_request_history[client_ip] if t > cutoff]
    if len(client_request_history[client_ip]) >= RATE_LIMIT_REQUESTS:
        return False
    client_request_history[client_ip].append(now)
    return True


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler: loads models and panel artifacts once at application startup."""
    logger.info("Starting Farmer Sell Advisor API...")
    try:
        AdvisorService.get_instance()
        logger.info("Advisor models and services initialized successfully.")
    except Exception as e:
        logger.error(f"Error during service initialization: {e}", exc_info=True)
    yield
    logger.info("Shutting down Farmer Sell Advisor API...")


app = FastAPI(
    title="Farmer Sell Advisor API",
    description=(
        "Production API powering the Farmer Sell Advisor website. "
        "Provides probabilistic price forecasts (P10/P50/P90), spatial mandi routing, "
        "temporal Monte Carlo holding simulations, and multilingual plain-language advice."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def rate_limit_and_logging_middleware(request: Request, call_next):
    """Rate limits incoming requests and logs execution time."""
    client_ip = request.client.host if request.client else "unknown"
    
    # Don't rate limit health checks
    if request.url.path not in ["/api/health", "/docs", "/openapi.json"]:
        if not check_rate_limit(client_ip):
            logger.warning(f"Rate limit exceeded for client: {client_ip}")
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Too many requests. Please slow down and try again shortly."}
            )

    start_time = time.time()
    try:
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms:.1f}ms)")
        return response
    except Exception as exc:
        duration_ms = (time.time() - start_time) * 1000
        logger.error(f"Unhandled server error on {request.method} {request.url.path} ({duration_ms:.1f}ms): {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An internal server error occurred. Please verify inputs and try again."}
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Returns farmer-friendly validation error messages."""
    errors = []
    for err in exc.errors():
        field = " -> ".join([str(x) for x in err.get("loc", []) if x != "body"])
        msg = err.get("msg", "Invalid value")
        errors.append(f"{field}: {msg}" if field else msg)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Input validation error",
            "errors": errors,
            "friendly_message": "Please check your inputs (e.g. quantity must be positive, mandi must be valid)."
        }
    )


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

@app.get("/api/health", response_model=HealthResponse, tags=["System"])
def get_health():
    """Health, model version, data freshness, and synthetic provenance status."""
    service = AdvisorService.get_instance()
    return service.get_health_status()


@app.get("/api/mandis", response_model=List[MandiInfo], tags=["Market Data"])
def get_mandis(user_location: Optional[str] = Query(None, description="Optional user location for distance calculation")):
    """List of candidate Karnataka mandis with coordinates, APMC tier, and road distances."""
    service = AdvisorService.get_instance()
    return service.get_mandis(user_location)


@app.get("/api/forecast", response_model=ForecastResponse, tags=["Forecasting"])
def get_forecast(mandi: str = Query("Kolar", description="Name of the APMC mandi")):
    """P10/P50/P90 price forecast across 7, 14, and 30 days for a specific mandi."""
    service = AdvisorService.get_instance()
    # Normalize mandi check
    mandis_cfg = service.config.get("mandis", {})
    match = None
    for name in mandis_cfg:
        if mandi.lower() in name.lower() or name.lower() in mandi.lower():
            match = name
            break
    target_mandi = match or mandi
    return service.get_forecast_for_mandi(target_mandi)


@app.post("/api/where-to-sell", response_model=WhereToSellResponse, tags=["Decision Support"])
def post_where_to_sell(body: WhereToSellRequest):
    """Ranks nearby mandis by net price deducting transport freight, statutory fees, and transit shrinkage."""
    service = AdvisorService.get_instance()
    return service.evaluate_where_to_sell(
        farmer_location=body.farmer_location,
        quantity_quintals=body.quantity_quintals,
        horizon_days=body.horizon_days
    )


@app.post("/api/when-to-sell", response_model=WhenToSellResponse, tags=["Decision Support"])
def post_when_to_sell(body: WhenToSellRequest):
    """Monte Carlo simulation of holding vs selling today under decay rates and debt interest."""
    service = AdvisorService.get_instance()
    return service.evaluate_when_to_sell(
        farmer_location=body.farmer_location,
        quantity_quintals=body.quantity_quintals,
        storage_type=body.storage_type,
        has_trader_debt=body.has_trader_debt,
        simulate_credit_comparison=body.simulate_credit_comparison
    )


@app.post("/api/advice", response_model=AdviceResponse, tags=["Agent Advice"])
def post_advice(body: AdviceRequest):
    """Plain-language multilingual advice (English, Hindi, Kannada) with uncertainty bands and farmer autonomy notice."""
    service = AdvisorService.get_instance()
    return service.generate_plain_language_advice(
        farmer_location=body.farmer_location,
        quantity_quintals=body.quantity_quintals,
        storage_type=body.storage_type,
        has_trader_debt=body.has_trader_debt,
        language=body.language
    )


@app.get("/api/model-report", response_model=ModelReportResponse, tags=["Model Transparency"])
def get_model_report():
    """Full transparency report: metrics vs baselines, horizon coverage audit, config assumptions, and limitations."""
    service = AdvisorService.get_instance()
    return service.get_model_report()


# ---------------------------------------------------------------------------
# Crop Area & Supply Outlook Endpoints
# ---------------------------------------------------------------------------

@app.post("/api/area-report", response_model=AreaReportResponse, tags=["Crop Area"])
def post_area_report(body: AreaReportRequest):
    """Submit farmer-reported acreage. Validates single-holding limits, checks anomalies, and hashes device ID."""
    service = AdvisorService.get_instance()
    try:
        return service.record_area_report(
            district=body.district,
            season=body.season,
            year=body.year,
            acres=body.acres,
            device_id=body.device_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@app.get("/api/area-summary", response_model=AreaSummaryResponse, tags=["Crop Area"])
def get_area_summary(
    district: str = Query("Mysuru", description="Karnataka district name"),
    season: str = Query("Kharif", description="Season e.g. 'Kharif', 'Rabi'"),
    year: str = Query("2024-25", description="Agricultural year e.g. '2024-25'")
):
    """Aggregates farmer-reported acreage vs official district, state, and country statistics with coverage ratio."""
    service = AdvisorService.get_instance()
    return service.get_area_summary(district=district, season=season, year=year)


@app.get("/api/supply-price-outlook", response_model=SupplyPriceOutlookResponse, tags=["Crop Area"])
def get_supply_price_outlook(
    district: str = Query("Mysuru", description="Karnataka district name"),
    season: str = Query("Kharif", description="Season e.g. 'Kharif', 'Rabi'"),
    year: str = Query("2024-25", description="Agricultural year e.g. '2024-25'")
):
    """Provides 30/60/90-day price outlook linked to official supply signals with farmer autonomy notice."""
    service = AdvisorService.get_instance()
    return service.get_supply_price_outlook(district=district, season=season, year=year)


@app.get("/api/area-reports/officer-review", tags=["Crop Area"])
def get_officer_review(
    district: str = Query("Mysuru", description="Karnataka district name"),
    limit: int = Query(20, description="Max submissions to return")
):
    """Returns anonymized device submissions and quality validation flags for FPO officer review."""
    service = AdvisorService.get_instance()
    return service.get_officer_review_data(district=district, limit=limit)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

