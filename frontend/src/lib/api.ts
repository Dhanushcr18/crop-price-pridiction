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
  SupplyPriceOutlookResponse
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

export async function getForecast(mandi: string): Promise<ForecastResponse> {
  return fetchWithCache<ForecastResponse>(
    `${API_BASE}/api/forecast?mandi=${encodeURIComponent(mandi)}`,
    `forecast_${mandi}`
  );
}

export async function getWhereToSell(
  farmerLocation: string,
  quantityQuintals: number,
  horizonDays: number = 7
): Promise<WhereToSellResponse> {
  return fetchWithCache<WhereToSellResponse>(
    `${API_BASE}/api/where-to-sell`,
    `where_${farmerLocation}_${quantityQuintals}_${horizonDays}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
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
  language: string = "en"
): Promise<AdviceResponse> {
  return fetchWithCache<AdviceResponse>(
    `${API_BASE}/api/advice`,
    `advice_${farmerLocation}_${quantityQuintals}_${storageType}_${hasTraderDebt}_${language}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
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
