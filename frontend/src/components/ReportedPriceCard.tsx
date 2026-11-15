"use client";

import React, { useState } from "react";
import { TodayPriceResponse, Language } from "../types/api";
import { translations } from "../i18n/translations";
import { formatCurrency } from "../lib/formatter";

interface ReportedPriceCardProps {
  priceData: TodayPriceResponse | null;
  crop: string;
  mandi: string;
  language: Language;
}

export const ReportedPriceCard: React.FC<ReportedPriceCardProps> = ({
  priceData,
  crop,
  mandi,
  language,
}) => {
  const t = translations[language];
  const [showAllGrades, setShowAllGrades] = useState(false);

  if (!priceData) return null;

  // 1. Quarantined Mandi ("Data under review")
  if (priceData.status === "Data under review") {
    return (
      <div className="bg-amber-50 dark:bg-amber-950/30 border-2 border-amber-300 dark:border-amber-700/60 rounded-3xl p-6 shadow-card space-y-3">
        <div className="flex items-center gap-2.5 text-amber-800 dark:text-amber-300">
          <span className="material-symbols-outlined text-[24px]">warning</span>
          <span className="font-black text-lg sm:text-xl uppercase tracking-wide">
            {t.dataUnderReview}
          </span>
        </div>
        <p className="text-sm text-amber-900/80 dark:text-amber-200/80 leading-relaxed font-medium">
          {priceData.message || "Prices for this market have been flagged by the data validation gate and quarantined for manual officer review. No unverified prices are shown."}
        </p>
      </div>
    );
  }

  // 2. Not Available in this Mandi
  if (priceData.status === "Not available" || !priceData.available || !priceData.headline_price) {
    return (
      <div className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-6 shadow-card space-y-3 text-center">
        <div className="w-12 h-12 rounded-2xl bg-surface-low dark:bg-surface-low-dark text-ink-muted flex items-center justify-center mx-auto">
          <span className="material-symbols-outlined text-[28px]">event_busy</span>
        </div>
        <h4 className="font-extrabold text-base text-ink dark:text-ink-dark">
          {priceData.message || `${crop} is not reported at ${mandi}`}
        </h4>
        <p className="text-xs text-ink-muted">
          {priceData.date ? t.latestReportedOn.replace("{date}", priceData.date) : "No reporting history in the KSAMB panel"}
        </p>
      </div>
    );
  }

  const hp = priceData.headline_price;
  const unitLabel = hp.unit === "Quintal" ? "₹ / Quintal" : `₹ / ${hp.unit}`;

  return (
    <div className="space-y-4">
      {/* Stale Data Banner if > 2 days old */}
      {priceData.is_stale && (
        <div className="p-3.5 rounded-2xl bg-amber-50 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-700 flex items-center gap-2.5 text-amber-900 dark:text-amber-200 text-xs sm:text-sm font-bold">
          <span className="material-symbols-outlined text-[20px] text-amber-600">history</span>
          <span>{t.latestReportedOn.replace("{date}", priceData.date || "11 Nov 2026")}</span>
        </div>
      )}

      {/* Solid Green Card for Reported Price */}
      <div className="bg-emerald-800 text-white rounded-3xl p-6 shadow-card space-y-5">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-700/80 text-emerald-100 text-xs font-black uppercase tracking-wider">
            <span className="w-2 h-2 rounded-full bg-emerald-300 animate-pulse" />
            <span>{t.reportedCardLabel}</span>
          </div>

          <div className="text-xs text-emerald-200 font-medium">
            {t.ksambSource} • {priceData.date}
          </div>
        </div>

        {/* Modal Spot Price Headline */}
        <div>
          <div className="text-xs font-bold uppercase tracking-wider text-emerald-200">
            {t.liveModalPrice} ({hp.variety} - {hp.grade})
          </div>
          <div className="flex items-baseline gap-2 mt-1">
            <span className="text-4xl sm:text-5xl font-black tracking-tight">
              {formatCurrency(hp.modal_price)}
            </span>
            <span className="text-base sm:text-lg font-bold text-emerald-200">
              {unitLabel}
            </span>
          </div>
        </div>

        {/* Metrics Grid: Min, Max, Arrivals */}
        <div className="grid grid-cols-3 gap-3 pt-2 border-t border-emerald-700/60">
          <div className="bg-emerald-900/50 rounded-2xl p-3">
            <div className="text-[11px] font-bold text-emerald-200">Min Price</div>
            <div className="text-base sm:text-lg font-extrabold mt-0.5">
              {formatCurrency(hp.min_price)}
            </div>
          </div>

          <div className="bg-emerald-900/50 rounded-2xl p-3">
            <div className="text-[11px] font-bold text-emerald-200">Max Price</div>
            <div className="text-base sm:text-lg font-extrabold mt-0.5">
              {formatCurrency(hp.max_price)}
            </div>
          </div>

          <div className="bg-emerald-900/50 rounded-2xl p-3">
            <div className="text-[11px] font-bold text-emerald-200">{t.arrivalsToday}</div>
            <div className="text-base sm:text-lg font-extrabold mt-0.5">
              {hp.arrivals.toLocaleString()} {hp.unit === "Quintal" ? "qtl" : hp.unit}
            </div>
          </div>
        </div>

        {/* Toggle to see all grades if more than 1 grade exists */}
        {priceData.all_grades && priceData.all_grades.length > 1 && (
          <div className="pt-2">
            <button
              type="button"
              onClick={() => setShowAllGrades(!showAllGrades)}
              className="w-full py-2 bg-emerald-700/60 hover:bg-emerald-700 rounded-xl text-xs font-bold text-emerald-100 flex items-center justify-center gap-1.5 transition-colors"
            >
              <span>{t.viewAllGrades} ({priceData.all_grades.length})</span>
              <span className="material-symbols-outlined text-[16px]">
                {showAllGrades ? "expand_less" : "expand_more"}
              </span>
            </button>

            {showAllGrades && (
              <div className="mt-3 overflow-x-auto rounded-2xl border border-emerald-700/80 bg-emerald-900/60">
                <table className="w-full text-xs text-left">
                  <thead className="bg-emerald-950/60 text-emerald-200 font-bold border-b border-emerald-700/80">
                    <tr>
                      <th className="p-2.5">Variety</th>
                      <th className="p-2.5">Grade</th>
                      <th className="p-2.5">Modal</th>
                      <th className="p-2.5">Min / Max</th>
                      <th className="p-2.5">Arrivals</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-emerald-800/60">
                    {priceData.all_grades.map((g, idx) => (
                      <tr key={idx} className={g.is_headline ? "bg-emerald-700/40 font-bold" : ""}>
                        <td className="p-2.5">{g.variety} {g.is_headline && "★"}</td>
                        <td className="p-2.5">{g.grade}</td>
                        <td className="p-2.5">{formatCurrency(g.modal_price)}</td>
                        <td className="p-2.5">{g.min_price} - {g.max_price}</td>
                        <td className="p-2.5">{g.arrivals.toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Honest Notice Card replacing Forecast Fan Chart */}
      <div className="bg-surface-low dark:bg-surface-low-dark border border-divider dark:border-divider-dark rounded-3xl p-5 shadow-sm space-y-2">
        <div className="flex items-center gap-2 text-ink-muted">
          <span className="material-symbols-outlined text-[20px] text-primary">info</span>
          <span className="font-extrabold text-xs uppercase tracking-wider text-ink dark:text-ink-dark">
            Tier B Policy Notice
          </span>
        </div>
        <p className="text-xs text-ink-muted dark:text-ink-muted-dark leading-relaxed font-medium">
          {t.forecastNotAvailableNotice}
        </p>
      </div>
    </div>
  );
};
