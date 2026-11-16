import {
  HealthResponse,
  MandiInfo,
  ForecastResponse,
  WhereToSellResponse,
  WhenToSellResponse,
  AdviceResponse,
  ModelReportResponse,
  AreaReportRequest,
  AreaReportResponse,
  AreaSummaryResponse,
  SupplyPriceOutlookResponse,
  CropInfo,
  DistrictInfo,
  MandiDetailItem,
  TodayPriceResponse,
  PriceComparisonItem,
  WhereToSellSpatialResponse,
  CoverageSummaryResponse
} from "../types/api";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchWithCache<T>(url: string, cacheKey: string, options?: RequestInit): Promise<T> {
  try {
    const res = await fetch(url, options);
    if (!res.ok) {
      throw new Error(`API error: ${res.status} ${res.statusText}`);
    }
    const data = await res.json();
    if (typeof window !== "undefined") {
      try {
        localStorage.setItem(`fsa_cache_${cacheKey}`, JSON.stringify(data));
      } catch {
        // quota exceeded or private mode
      }
    }
    return data;
  } catch (err) {
    if (typeof window !== "undefined") {
      const cached = localStorage.getItem(`fsa_cache_${cacheKey}`);
      if (cached) {
        console.warn(`Network unavailable, returning cached offline response for ${cacheKey}`);
        return JSON.parse(cached);
      }
    }
    throw err;
  }
}

export async function getHealth(): Promise<HealthResponse> {
  return fetchWithCache<HealthResponse>(`${API_BASE}/api/health`, "health");
}

export async function getMandis(userLocation?: string): Promise<MandiInfo[]> {
  const query = userLocation ? `?user_location=${encodeURIComponent(userLocation)}` : "";
  return fetchWithCache<MandiInfo[]>(`${API_BASE}/api/mandis${query}`, `mandis_${userLocation || "all"}`);
}

export async function getForecast(mandi: string, crop?: string): Promise<ForecastResponse> {
  const cropParam = crop ? `&crop=${encodeURIComponent(crop)}` : "";
  return fetchWithCache<ForecastResponse>(
    `${API_BASE}/api/forecast?mandi=${encodeURIComponent(mandi)}${cropParam}`,
    `forecast_${mandi}_${crop || "all"}`
  );
}

export async function getWhereToSell(
  farmerLocation: string,
  quantityQuintals: number,
  horizonDays: number = 7,
  crop: string = "Onion"
): Promise<WhereToSellResponse> {
  return fetchWithCache<WhereToSellResponse>(
    `${API_BASE}/api/where-to-sell`,
    `where_${farmerLocation}_${quantityQuintals}_${horizonDays}_${crop}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        crop: crop || "Onion",
        farmer_location: farmerLocation,
        quantity_quintals: quantityQuintals,
        horizon_days: horizonDays,
      }),
    }
  );
}

export async function getWhenToSell(
  farmerLocation: string,
  quantityQuintals: number,
  storageType: string = "open",
  hasTraderDebt: boolean = false
): Promise<WhenToSellResponse> {
  return fetchWithCache<WhenToSellResponse>(
    `${API_BASE}/api/when-to-sell`,
    `when_${farmerLocation}_${quantityQuintals}_${storageType}_${hasTraderDebt}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        farmer_location: farmerLocation,
        quantity_quintals: quantityQuintals,
        storage_type: storageType,
        has_trader_debt: hasTraderDebt,
        simulate_credit_comparison: true,
      }),
    }
  );
}

export async function getAdvice(
  farmerLocation: string,
  quantityQuintals: number,
  storageType: string = "open",
  hasTraderDebt: boolean = false,
  language: string = "en",
  crop: string = "Onion"
): Promise<AdviceResponse> {
  return fetchWithCache<AdviceResponse>(
    `${API_BASE}/api/advice`,
    `advice_${farmerLocation}_${quantityQuintals}_${storageType}_${hasTraderDebt}_${language}_${crop}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        crop: crop || "Onion",
        farmer_location: farmerLocation,
        quantity_quintals: quantityQuintals,
        storage_type: storageType,
        has_trader_debt: hasTraderDebt,
        language: language,
      }),
    }
  );
}

export async function getModelReport(): Promise<ModelReportResponse> {
  return fetchWithCache<ModelReportResponse>(`${API_BASE}/api/model-report`, "model_report");
}

export async function submitAreaReport(req: AreaReportRequest): Promise<AreaReportResponse> {
  const res = await fetch(`${API_BASE}/api/area-report`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!res.ok) {
    const errorBody = await res.json().catch(() => ({}));
    throw new Error(errorBody.detail || `Failed to submit area report (${res.status})`);
  }
  return res.json();
}

export async function getAreaSummary(
  district: string = "Mysuru",
  season: string = "Kharif",
  year: string = "2024-25"
): Promise<AreaSummaryResponse> {
  const query = `district=${encodeURIComponent(district)}&season=${encodeURIComponent(season)}&year=${encodeURIComponent(year)}`;
  return fetchWithCache<AreaSummaryResponse>(
    `${API_BASE}/api/area-summary?${query}`,
    `area_summary_${district}_${season}_${year}`
  );
}

export async function getSupplyPriceOutlook(
  district: string = "Mysuru",
  season: string = "Kharif",
  year: string = "2024-25"
): Promise<SupplyPriceOutlookResponse> {
  const query = `district=${encodeURIComponent(district)}&season=${encodeURIComponent(season)}&year=${encodeURIComponent(year)}`;
  return fetchWithCache<SupplyPriceOutlookResponse>(
    `${API_BASE}/api/supply-price-outlook?${query}`,
    `supply_outlook_${district}_${season}_${year}`
  );
}

export async function getOfficerReview(
  district: string = "Mysuru",
  limit: number = 20
): Promise<any> {
  const res = await fetch(`${API_BASE}/api/area-reports/officer-review?district=${encodeURIComponent(district)}&limit=${limit}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch officer review: ${res.statusText}`);
  }
  return res.json();
}

// ---------------------------------------------------------------------------
// All-Crop & All-Mandi Dynamic Endpoints
// ---------------------------------------------------------------------------

export async function getCrops(): Promise<CropInfo[]> {
  return fetchWithCache<CropInfo[]>(`${API_BASE}/api/crops`, "all_crops");
}

export async function getDistricts(): Promise<DistrictInfo[]> {
  return fetchWithCache<DistrictInfo[]>(`${API_BASE}/api/districts`, "all_districts");
}

export async function getMandisFiltered(params?: {
  district?: string;
  crop?: string;
  lat?: number;
  lon?: number;
}): Promise<MandiDetailItem[]> {
  const searchParams = new URLSearchParams();
  if (params?.district) searchParams.set("district", params.district);
  if (params?.crop) searchParams.set("crop", params.crop);
  if (params?.lat !== undefined) searchParams.set("lat", params.lat.toString());
  if (params?.lon !== undefined) searchParams.set("lon", params.lon.toString());
  const qs = searchParams.toString();
  return fetchWithCache<MandiDetailItem[]>(
    `${API_BASE}/api/mandis${qs ? `?${qs}` : ""}`,
    `mandis_filtered_${qs}`
  );
}

export async function getTodayPrice(crop: string, mandi: string): Promise<TodayPriceResponse> {
  return fetchWithCache<TodayPriceResponse>(
    `${API_BASE}/api/today-price?crop=${encodeURIComponent(crop)}&mandi=${encodeURIComponent(mandi)}`,
    `today_price_${crop}_${mandi}`
  );
}

export async function getPricesCompare(params: {
  crop: string;
  district?: string;
  radiusKm?: number;
  lat?: number;
  lon?: number;
}): Promise<PriceComparisonItem[]> {
  const searchParams = new URLSearchParams();
  searchParams.set("crop", params.crop);
  if (params.district) searchParams.set("district", params.district);
  if (params.radiusKm) searchParams.set("radius_km", params.radiusKm.toString());
  if (params.lat !== undefined) searchParams.set("lat", params.lat.toString());
  if (params.lon !== undefined) searchParams.set("lon", params.lon.toString());
  const qs = searchParams.toString();
  return fetchWithCache<PriceComparisonItem[]>(
    `${API_BASE}/api/prices/compare?${qs}`,
    `compare_${qs}`
  );
}

export async function postWhereToSellSpatial(params: {
  crop: string;
  farmerLocation?: string;
  lat?: number;
  lon?: number;
  quantityQuintals?: number;
  radiusKm?: number;
}): Promise<WhereToSellSpatialResponse> {
  return fetchWithCache<WhereToSellSpatialResponse>(
    `${API_BASE}/api/where-to-sell`,
    `spatial_where_${params.crop}_${params.farmerLocation}_${params.radiusKm}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        crop: params.crop,
        farmer_location: params.farmerLocation,
        lat: params.lat,
        lon: params.lon,
        quantity_quintals: params.quantityQuintals || 30.0,
        radius_km: params.radiusKm || 100.0
      })
    }
  );
}

export async function getCoverageSummary(): Promise<CoverageSummaryResponse> {
  return fetchWithCache<CoverageSummaryResponse>(`${API_BASE}/api/coverage`, "coverage_summary");
}

