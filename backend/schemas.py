"""Pydantic schemas for Farmer Sell Advisor API."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class HealthResponse(BaseModel):
    status: str = "healthy"
    model_version: str = "1.0.0-lgb-cqr"
    last_data_date: str
    days_since_data: int
    is_stale: bool
    provenance: str = Field(..., description="'real' or 'synthetic'")
    is_synthetic: bool
    synthetic_banner: Optional[str] = None


class MandiInfo(BaseModel):
    id: str
    name: str
    state: str
    district: str
    lat: float
    lon: float
    tier: str
    distance_km: Optional[float] = None


class ForecastHorizonDetail(BaseModel):
    horizon_days: int
    p10_downside: float
    p50_expected: float
    p90_upside: float
    uncertainty_interval: str
    interval_width: float
    coverage_pct: float
    beats_naive: bool
    is_low_confidence: bool
    confidence_reason: Optional[str] = None


class ForecastResponse(BaseModel):
    mandi: str
    crop: Optional[str] = None
    spot_price_today: Optional[float] = None
    as_of_date: Optional[str] = None
    horizons: List[ForecastHorizonDetail] = []
    status: Optional[str] = None
    message: Optional[str] = None
    provenance: str = "real"
    is_synthetic: bool = False
    synthetic_banner: Optional[str] = None
    disclaimer: str = "This is advice, the decision is yours. Prices reflect P10-P90 statistical ranges."


class WhereToSellRequest(BaseModel):
    farmer_location: str = Field(..., description="e.g., 'Kolar', 'Chikkaballapur', 'Bengaluru (Yeshwanthpur)'")
    quantity_quintals: float = Field(..., gt=0, le=10000, description="Quantity in quintals")
    horizon_days: int = Field(7, description="7, 14, or 30 days")

    @field_validator("quantity_quintals")
    @classmethod
    def validate_quantity(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Quantity must be greater than 0 quintals.")
        if v > 10000:
            raise ValueError("Quantity exceeds maximum lot capacity (10,000 quintals).")
        return v


class MandiRankCard(BaseModel):
    rank: int
    mandi: str
    distance_km: float
    gross_price_p50: float
    gross_price_p10: float
    gross_price_p90: float
    transport_cost_per_qtl: float
    fees_and_commission_per_qtl: float
    shrinkage_loss_per_qtl: float
    net_price_p50: float
    net_price_p10_downside: float
    net_price_p90_upside: float
    gain_over_local_per_qtl: float
    total_gain_rs: float
    is_local: bool


class WhereToSellResponse(BaseModel):
    farmer_location: str
    quantity_quintals: float
    horizon_days: int
    local_mandi_net_p50: Optional[float] = None
    local_mandi_net_p10: Optional[float] = None
    ranked_mandis: List[MandiRankCard]
    provenance: str
    is_synthetic: bool
    synthetic_banner: Optional[str] = None
    disclaimer: str = "This is advice, the decision is yours. Net realized price accounts for transport freight, APMC fees, commissions, and transit shrinkage."


class WhenToSellRequest(BaseModel):
    farmer_location: str = Field(..., description="Farmer's mandi or village location")
    quantity_quintals: float = Field(..., gt=0, le=10000)
    storage_type: str = Field("open", description="'open', 'warehouse', or 'cold_storage'")
    has_trader_debt: bool = Field(False, description="Whether farmer owes a commission agent / trader")
    simulate_credit_comparison: bool = True

    @field_validator("storage_type")
    @classmethod
    def validate_storage(cls, v: str) -> str:
        valid = ["open", "warehouse", "cold_storage"]
        if v not in valid:
            raise ValueError(f"storage_type must be one of {valid}")
        return v


class HoldSimulationHorizon(BaseModel):
    k_days: int
    expected_future_price: float
    spoilage_loss_pct: float
    storage_cost_per_qtl: float
    interest_cost_per_qtl: float
    expected_gain_per_qtl: float
    total_expected_gain_lot: float
    worst_case_p10_gain: float
    prob_wait_beats_today_pct: float
    recommendation: str


class StorageOption(BaseModel):
    type_key: str
    name: str
    rental_cost_per_qtl_day: float
    daily_spoilage_loss_pct: float
    max_safe_holding_days: int
    distance_km: float
    best_for: str


class WhenToSellResponse(BaseModel):
    price_today: Optional[float] = None
    storage_type: str
    has_trader_debt: bool
    best_k_days: int = 0
    max_expected_gain_per_qtl: float = 0.0
    simulation_results: List[HoldSimulationHorizon] = []
    credit_comparison: Optional[Dict[str, Any]] = None
    storage_options: List[StorageOption] = []
    provenance: str
    is_synthetic: bool
    synthetic_banner: Optional[str] = None
    disclaimer: str = "This is advice, the decision is yours. Holding simulation models daily spoilage decay and carrying interest via Monte Carlo sampling."


class AdviceRequest(BaseModel):
    farmer_location: str
    crop: Optional[str] = None
    quantity_quintals: float = Field(..., gt=0, le=10000)
    storage_type: str = Field("open", description="'open', 'warehouse', or 'cold_storage'")
    has_trader_debt: bool = False
    language: str = Field("en", description="'en', 'hi', or 'kn'")

    @field_validator("language")
    @classmethod
    def validate_lang(cls, v: str) -> str:
        v_low = v.lower()
        if v_low not in ["en", "hi", "kn", "english", "hindi", "kannada"]:
            return "en"
        return v_low


class AdviceResponse(BaseModel):
    summary_sentence: str
    full_advice_text: str
    language: str = "en"
    recommended_mandi: str = "Not available"
    best_timing_days: int = 0
    expected_net_gain_total: float = 0.0
    p10_p90_range: str = "Not available"
    has_low_confidence: bool = True
    low_confidence_notice: Optional[str] = None
    disclaimer: str = "This is advice, the decision is yours."
    provenance: str = "real"
    is_synthetic: bool = False
    synthetic_banner: Optional[str] = None


class ModelReportResponse(BaseModel):
    executive_summary: str
    metrics_table: List[Dict[str, Any]]
    coverage_audit: List[Dict[str, Any]]
    assumptions: Dict[str, Any]
    limitations: List[str]
    data_provenance: str
    data_date_range: str
    is_synthetic: bool
    synthetic_banner: Optional[str] = None


# ---------------------------------------------------------------------------
# Crop Area and Supply Outlook Schemas
# ---------------------------------------------------------------------------

class AreaReportRequest(BaseModel):
    district: str = Field(..., description="Karnataka district name, e.g. 'Mysuru', 'Gadag', 'Dharwad'")
    season: str = Field("Kharif", description="'Kharif', 'Late Kharif', 'Rabi', or 'Total'")
    year: str = Field("2024-25", description="Agricultural year e.g. '2024-25'")
    acres: float = Field(..., description="Reported onion acreage")
    device_id: str = Field("anonymous_device", description="Device ID (hashed with SHA-256 upon arrival)")

    @field_validator("acres")
    @classmethod
    def validate_acres(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Acres must be greater than zero. Please enter a valid farm size.")
        if v > 500.0:
            raise ValueError("Reported area exceeds the 500-acre limit for single-holding entries. Please verify your land size.")
        return v


class AreaReportResponse(BaseModel):
    status: str = "success"
    action: str = Field(..., description="'created' or 'updated'")
    record_id: int
    district: str
    season: str
    year: str
    reported_acres: float
    reported_hectares: float
    is_anomaly: bool
    timestamp: str


class RegionAreaMetric(BaseModel):
    level: str = Field(..., description="'country', 'state', or 'district'")
    region_name: str
    year: str
    season: str
    area_hectares: float
    area_acres: float
    production_tonnes: float
    yield_tonnes_per_ha: float
    avg_5yr_hectares: float
    avg_5yr_acres: float
    area_ratio_vs_5yr: float
    prod_ratio_vs_5yr: float
    signal_category: str = Field(..., description="'higher', 'normal', or 'lower'")
    source_name: str
    publication_date: str
    history: List[Dict[str, Any]] = Field(default_factory=list)


class FarmerReportedSummary(BaseModel):
    reported_acres: float
    reported_hectares: float
    entry_count: int
    coverage_pct: Optional[float] = None
    too_few_reports: bool
    warning_message: Optional[str] = None


class AreaSummaryResponse(BaseModel):
    district: str
    season: str
    year: str
    farmer_reported: FarmerReportedSummary
    district_official: Optional[RegionAreaMetric] = None
    district_official_available: bool
    state_official: Optional[RegionAreaMetric] = None
    country_official: Optional[RegionAreaMetric] = None
    sowing_to_harvest_lag_days: int
    assumptions: List[Dict[str, str]] = Field(default_factory=list)
    synthetic_banner: Optional[str] = None


class SupplyHorizonOutlook(BaseModel):
    horizon_days: int = Field(..., description="30, 60, or 90 days")
    p10_downside: float
    p50_expected: float
    p90_upside: float
    price_range_text: str
    confidence_badge: str


class SupplyPriceOutlookResponse(BaseModel):
    district: str
    season: str
    year: str
    supply_signal: str = Field(..., description="'higher', 'normal', or 'lower'")
    supply_summary_sentence: str
    horizons: List[SupplyHorizonOutlook]
    confidence_badge: str
    confidence_level: str
    explanation_text: str
    farmer_acreage_isolated_notice: str = "Farmer-reported acreage is strictly isolated and does not alter this price forecast."
    autonomy_disclaimer: str = "This is advice, the decision is yours."
    synthetic_banner: Optional[str] = None


# ---------------------------------------------------------------------------
# All-Crop & All-Mandi Dynamic Schemas
# ---------------------------------------------------------------------------

class CropInfo(BaseModel):
    crop_id: str
    name_en: str
    name_kn: str
    name_hi: str
    category: str
    unit: str
    perishability_class: str
    variety_count: int
    grade_count: int
    reporting_mandis_count: int
    total_records: int


class DistrictInfo(BaseModel):
    district_code: str
    name_en: str
    name_kn: str
    lat: float
    lon: float
    reporting_mandis_count: int
    status: str


class MandiItem(BaseModel):
    mandi_id: str
    raw_market_name: str
    name_en: str
    name_kn: str
    district_code: str
    district_en: str
    district_kn: str
    lat: float
    lon: float
    coord_source: str
    tier: str
    last_reported_date: Optional[str] = None
    is_stale: bool = True
    all_quarantined: bool = False
    distance_km: Optional[float] = None


class GradePriceDetail(BaseModel):
    variety: str
    grade: str
    unit: str
    min_price: float
    modal_price: float
    max_price: float
    arrivals: float


class HeadlinePrice(BaseModel):
    min_price: float
    modal_price: float
    max_price: float
    arrivals: float
    unit: str
    variety: str
    grade: str
    date: str
    source: str
    is_stale: bool
    stale_notice: str
    headline_selection_rule: str


class TodayPriceResponse(BaseModel):
    status: str
    available: bool
    crop: str
    mandi: str
    message: str
    headline_price: Optional[HeadlinePrice] = None
    all_grades: List[GradePriceDetail] = []
    notice: Optional[str] = None
    is_stale: bool = True
    date: Optional[str] = None
    source: Optional[str] = None


class WhereToSellSpatialRequest(BaseModel):
    crop: str
    farmer_location: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    quantity_quintals: float = 30.0
    radius_km: float = 100.0


class CoverageSummaryResponse(BaseModel):
    total_crops: int
    total_districts: int
    total_mandis: int
    total_pairs: int
    tier_counts: Dict[str, int]
    freshness: Dict[str, Any]
    quarantined_mandis: List[str]



