/**
 * Unified Number, Currency, and Text Formatter for Farmer Sell Advisor.
 * Enforces strict honesty, zero false precision (no decimals), Indian numbering grouping,
 * range headlines, and grade-6 language conventions.
 */

import { Language } from "../types/api";

export interface PriceRangeFormatted {
  headline: string; // e.g., "₹3,340 to ₹3,650 per quintal"
  minFormatted: string; // e.g., "₹3,340"
  maxFormatted: string; // e.g., "₹3,650"
  mostLikely: string; // e.g., "most likely about ₹3,500"
  p10: number; // rounded integer
  p50: number; // rounded integer
  p90: number; // rounded integer
}

/**
 * Format Indian currency with comma grouping (e.g. 1,23,456).
 * Prices per quintal are rounded to nearest ₹10.
 * Lot totals are rounded to nearest ₹100.
 * Strictly NO DECIMALS allowed anywhere.
 */
export function formatCurrency(
  amount: number,
  isTotal: boolean = false
): string {
  if (isNaN(amount) || amount === null || amount === undefined) {
    return "₹0";
  }

  // Round according to specification
  const rounded = isTotal
    ? Math.round(amount / 100) * 100
    : Math.round(amount / 10) * 10;

  // Format with Indian grouping
  const formatted = new Intl.NumberFormat("en-IN", {
    maximumFractionDigits: 0,
    minimumFractionDigits: 0,
  }).format(Math.abs(rounded));

  const sign = rounded < 0 ? "-" : "";
  return `${sign}₹${formatted}`;
}

/**
 * Format raw number with Indian grouping and no decimals.
 */
export function formatNumber(val: number): string {
  if (isNaN(val) || val === null || val === undefined) return "0";
  return new Intl.NumberFormat("en-IN", {
    maximumFractionDigits: 0,
    minimumFractionDigits: 0,
  }).format(Math.round(val));
}

/**
 * Formats a price range ensuring P10 <= P50 <= P90.
 * Returns a primary headline RANGE (never a single certain price)
 * and a secondary "most likely" estimate.
 */
export function formatPriceRange(
  p10: number,
  p90: number,
  p50?: number,
  lang: Language = "en"
): PriceRangeFormatted {
  const cleanP10 = Math.round((p10 || 0) / 10) * 10;
  const cleanP90 = Math.round((p90 || 0) / 10) * 10;
  const mid = p50 !== undefined ? p50 : (cleanP10 + cleanP90) / 2;
  const cleanP50 = Math.round(mid / 10) * 10;

  // Guarantee monotonic bounds
  const low = Math.min(cleanP10, cleanP50, cleanP90);
  const high = Math.max(cleanP10, cleanP50, cleanP90);
  const median = Math.max(low, Math.min(cleanP50, high));

  const lowStr = formatCurrency(low, false);
  const highStr = formatCurrency(high, false);
  const midStr = formatCurrency(median, false);

  let headline = "";
  let mostLikely = "";

  if (lang === "kn") {
    headline = `${lowStr} ರಿಂದ ${highStr} ಪ್ರತಿ ಕ್ವಿಂಟಾಲ್‌ಗೆ`;
    mostLikely = `ಸಾಧ್ಯವಾದ ಸರಾಸರಿ ದರ ಸುಮಾರು ${midStr}`;
  } else if (lang === "hi") {
    headline = `${lowStr} से ${highStr} प्रति क्विंटल`;
    mostLikely = `सबसे संभावित दर लगभग ${midStr}`;
  } else {
    headline = `${lowStr} to ${highStr} per quintal`;
    mostLikely = `most likely about ${midStr}`;
  }

  return {
    headline,
    minFormatted: lowStr,
    maxFormatted: highStr,
    mostLikely,
    p10: low,
    p50: median,
    p90: high,
  };
}

/**
 * Format distance without wrapping text across lines.
 * Uses non-breaking space (U+00A0) and return string.
 */
export function formatDistance(km: number, lang: Language = "en"): string {
  const rounded = Math.round(km);
  const unit = lang === "kn" ? "ಕಿಮೀ" : lang === "hi" ? "किमी" : "km";
  // non-breaking space between number and unit
  return `${rounded}\u00A0${unit}`;
}

/**
 * Format probabilities as clean whole percents.
 */
export function formatPercent(val: number): string {
  const pct = val <= 1 ? val * 100 : val;
  return `${Math.round(pct)}%`;
}
