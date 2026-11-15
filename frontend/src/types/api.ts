export type Language = "en" | "hi" | "kn";

export interface HealthResponse {
  status: string;
  model_version: string;
  last_data_date: string;
  days_since_data: number;
  is_stale: boolean;
  provenance: "real" | "synthetic";
  is_synthetic: boolean;
  synthetic_banner?: string | null;
  notice?: string | null;
}

export interface MandiInfo {
  id: string;
  name: string;
  state: string;
  district: string;
  lat: number;
  lon: number;
  tier: string;
  distance_km?: number;
}

export interface ForecastHorizonDetail {
  horizon_days: number;
  p10_downside: number;
  p50_expected: number;
  p90_upside: number;
  uncertainty_interval: string;
  interval_width: number;
  coverage_pct: number;
  beats_naive: boolean;
  is_low_confidence: boolean;
  confidence_reason?: string | null;
}

export interface ForecastResponse {
  mandi: string;
  crop: string;
  spot_price_today: number;
  as_of_date: string;
  horizons: ForecastHorizonDetail[];
  provenance: string;
  is_synthetic: boolean;
  synthetic_banner?: string | null;
  notice?: string | null;
  disclaimer: string;
}

export interface MandiRankCard {
  rank: number;
  mandi: string;
  distance_km: number;
  gross_price_p50: number;
  gross_price_p10: number;
  gross_price_p90: number;
  transport_cost_per_qtl: number;
  fees_and_commission_per_qtl: number;
  shrinkage_loss_per_qtl: number;
  net_price_p50: number;
  net_price_p10_downside: number;
  net_price_p90_upside: number;
  gain_over_local_per_qtl: number;
  total_gain_rs: number;
  is_local: boolean;
}

export interface WhereToSellResponse {
  farmer_location: string;
  quantity_quintals: number;
  horizon_days: number;
  local_mandi_net_p50: number;
  local_mandi_net_p10: number;
  ranked_mandis: MandiRankCard[];
  provenance: string;
  is_synthetic: boolean;
  synthetic_banner?: string | null;
  notice?: string | null;
  disclaimer: string;
}

export interface HoldSimulationHorizon {
  k_days: number;
  expected_future_price: number;
  spoilage_loss_pct: number;
  storage_cost_per_qtl: number;
  interest_cost_per_qtl: number;
  expected_gain_per_qtl: number;
  total_expected_gain_lot: number;
  worst_case_p10_gain: number;
  prob_wait_beats_today_pct: number;
  recommendation: string;
}

export interface StorageOption {
  type_key: string;
  name: string;
  rental_cost_per_qtl_day: number;
  daily_spoilage_loss_pct: number;
  max_safe_holding_days: number;
  distance_km: number;
  best_for: string;
}

export interface CreditComparison {
  enwr_best_k_days: number;
  enwr_max_gain_per_qtl: number;
  interest_rate_annual_pct: number;
  trader_debt_rate_annual_pct: number;
  explanation: string;
}

export interface WhenToSellResponse {
  price_today: number;
  storage_type: string;
  has_trader_debt: boolean;
  best_k_days: number;
  max_expected_gain_per_qtl: number;
  simulation_results: HoldSimulationHorizon[];
  credit_comparison?: CreditComparison | null;
  storage_options: StorageOption[];
  provenance: string;
  is_synthetic: boolean;
  synthetic_banner?: string | null;
  notice?: string | null;
  disclaimer: string;
}

export interface AdviceResponse {
  summary_sentence: string;
  full_advice_text: string;
  language: string;
  recommended_mandi: string;
  best_timing_days: number;
  expected_net_gain_total: number;
  p10_p90_range: string;
  has_low_confidence: boolean;
  low_confidence_notice?: string | null;
  disclaimer: string;
  provenance: string;
  is_synthetic: boolean;
  synthetic_banner?: string | null;
  notice?: string | null;
}

export interface MetricRow {
  horizon: string;
  naive_mae: number;
  naive_mape: number;
  seasonal_naive_mae: number;
  moving_avg_mae: number;
  lgb_p50_mae: number;
  lgb_p50_mape: number;
  pinball_loss: number;
  coverage_pct: number;
  coverage_status: string;
  beats_naive: boolean;
  interval_width_rs: number;
}

export interface CoverageAuditRow {
  horizon: number;
  coverage_pct: number;
  target_band: string;
  is_flagged: boolean;
  reason: string;
}

export interface ModelReportResponse {
  executive_summary: string;
  metrics_table: MetricRow[];
  coverage_audit: CoverageAuditRow[];
  assumptions: Record<string, number>;
  limitations: string[];
  data_provenance: string;
  data_date_range: string;
  is_synthetic: boolean;
  synthetic_banner?: string | null;
  notice?: string | null;
}



export interface HistoryRecord {
  id: string;
  timestamp: string;
  crop: string;
  mandi: string;
  quantity: number;
  storage: string;
  hasTraderDebt: boolean;
  recommendation: string;
  recommendedMandi: string;
  priceRange: string;
  actualPriceReceived?: number | null;
  notes?: string;
}

export type TextSize = "normal" | "large" | "xlarge";

export interface AppSettings {
  language: Language;
  textSize: TextSize;
  darkMode: boolean;
  voiceEnabled: boolean;
}

// ---------------------------------------------------------------------------
// Crop Area and Supply Outlook Types
// ---------------------------------------------------------------------------

export interface AreaReportRequest {
  district: string;
  season: string;
  year: string;
  acres: number;
  device_id: string;
}

export interface AreaReportResponse {
  status: string;
  action: string;
  record_id: number;
  district: string;
  season: string;
  year: string;
  reported_acres: number;
  reported_hectares: number;
  is_anomaly: boolean;
  timestamp: string;
}

export interface AreaHistoryEntry {
  year: string;
  season: string;
  area_hectares: number;
  area_acres: number;
  production_tonnes: number;
  is_current: boolean;
}

export interface RegionAreaMetric {
  level: string;
  region_name: string;
  year: string;
  season: string;
  area_hectares: number;
  area_acres: number;
  production_tonnes: number;
  yield_tonnes_per_ha: number;
  avg_5yr_hectares: number;
  avg_5yr_acres: number;
  area_ratio_vs_5yr: number;
  prod_ratio_vs_5yr: number;
  signal_category: "higher" | "normal" | "lower";
  source_name: string;
  publication_date: string;
  history: AreaHistoryEntry[];
}

export interface FarmerReportedSummary {
  reported_acres: number;
  reported_hectares: number;
  entry_count: number;
  coverage_pct: number | null;
  too_few_reports: boolean;
  warning_message: string | null;
}

export interface AreaSummaryResponse {
  district: string;
  season: string;
  year: string;
  farmer_reported: FarmerReportedSummary;
  district_official: RegionAreaMetric | null;
  district_official_available: boolean;
  state_official: RegionAreaMetric | null;
  country_official: RegionAreaMetric | null;
  sowing_to_harvest_lag_days: number;
  assumptions: Array<{ item: string; value: string; status: string }>;
  synthetic_banner?: string | null;
  notice?: string | null;
}

export interface SupplyHorizonOutlook {
  horizon_days: number;
  p10_downside: number;
  p50_expected: number;
  p90_upside: number;
  price_range_text: string;
  confidence_badge: string;
}

export interface SupplyPriceOutlookResponse {
  district: string;
  season: string;
  year: string;
  supply_signal: "higher" | "normal" | "lower";
  supply_summary_sentence: string;
  horizons: SupplyHorizonOutlook[];
  confidence_badge: string;
  confidence_level: string;
  explanation_text: string;
  farmer_acreage_isolated_notice: string;
  autonomy_disclaimer: string;
  synthetic_banner?: string | null;
  notice?: string | null;
}

export interface OfficerSubmissionRow {
  device_hash: string;
  acres: number;
  hectares: number;
  district: string;
  season: string;
  year: string;
  is_anomaly: boolean;
  anomaly_reason?: string | null;
  created_at: string;
}

export interface OfficerReviewResponse {
  total_valid_submissions: number;
  total_reported_acres: number;
  flagged_anomalies: number;
  submissions: OfficerSubmissionRow[];
}

// ---------------------------------------------------------------------------
// Dynamic All-Crop & All-Mandi Interfaces
// ---------------------------------------------------------------------------

export interface CropInfo {
  crop_id: string;
  name_en: string;
  name_kn?: string;
  name_hi?: string;
  name?: string;
  kannada_name?: string;
  hindi_name?: string;
  category: string;
  unit: string;
  perishability_class?: string;
  variety_count?: number;
  grade_count?: number;
  reporting_mandis_count: number;
  reporting_markets_count?: number;
  total_records?: number;
}

export interface DistrictInfo {
  district_code?: string;
  name_en: string;
  name_kn?: string;
  name?: string;
  kannada_name?: string;
  lat?: number;
  lon?: number;
  reporting_mandis_count: number;
  mandi_count?: number;
  status: string;
}

export interface MandiDetailItem {
  id?: string;
  mandi_id?: string;
  raw_market_name?: string;
  name?: string;
  name_en?: string;
  name_kn?: string;
  kannada_name?: string;
  district?: string;
  district_code?: string;
  district_en?: string;
  district_kn?: string;
  lat?: number | null;
  lon?: number | null;
  coord_source?: string;
  tier?: string;
  last_reported_date?: string | null;
  latest_date?: string | null;
  is_stale?: boolean;
  all_quarantined?: boolean;
  is_quarantined?: boolean;
  distance_km?: number | null;
}

export interface GradePriceDetail {
  variety: string;
  grade: string;
  unit: string;
  min_price: number;
  modal_price: number;
  max_price: number;
  arrivals: number;
  is_headline?: boolean;
}

export interface HeadlinePrice {
  min_price: number;
  modal_price: number;
  max_price: number;
  arrivals: number;
  unit: string;
  variety: string;
  grade: string;
  date: string;
  source: string;
  is_stale: boolean;
  stale_notice: string;
  headline_selection_rule: string;
}

export interface TodayPriceResponse {
  status: "Reported" | "Not available" | "Data under review";
  available: boolean;
  crop: string;
  mandi: string;
  message: string;
  headline_price?: HeadlinePrice | null;
  all_grades: GradePriceDetail[];
  notice?: string | null;
  is_stale: boolean;
  date?: string | null;
  source?: string | null;
}

export interface PriceComparisonItem {
  mandi: string;
  district: string;
  modal_price: number;
  min_price: number;
  max_price: number;
  arrivals: number;
  unit: string;
  variety: string;
  grade: string;
  date: string;
  tier: string;
  distance_km?: number | null;
}

export interface WhereToSellCandidate {
  mandi: string;
  raw_mandi: string;
  district: string;
  distance_km: number;
  is_local: boolean;
  reported_date: string;
  variety: string;
  grade: string;
  arrivals_quintal: number;
  reported_min_price: number;
  reported_modal_price: number;
  reported_max_price: number;
  transport_cost_per_qtl: number;
  fees_and_commission_per_qtl: number;
  transit_shrinkage_per_qtl: number;
  net_price_modal: number;
  net_price_min: number;
  net_price_max: number;
  net_price_range: string;
  gain_over_local_per_qtl: number;
  total_gain_rs: number;
}

export interface WhereToSellSpatialResponse {
  status: string;
  crop: string;
  quantity_quintals: number;
  radius_km: number;
  results: WhereToSellCandidate[];
  reporting_mandis_in_range: number;
  excluded_mandis_no_report: number;
  excluded_mandis_out_of_radius: number;
  excluded_notice: string;
  disclaimer: string;
  assumption_label: string;
}

export interface CoverageSummaryResponse {
  total_crops: number;
  total_districts: number;
  total_mandis: number;
  total_pairs: number;
  tier_counts: {
    tier_a: number;
    tier_b: number;
    tier_c: number;
  };
  freshness: {
    latest_report_date: string;
    current_date: string;
    days_since_latest: number;
    stale_banner_required: boolean;
    stale_banner_text: string;
  };
  quarantined_mandis: string[];
}


