"use client";

import React, { useState, useEffect } from "react";
import { Header } from "../../components/Header";
import { BottomNav } from "../../components/BottomNav";
import { ConfidenceBadge } from "../../components/ui/ConfidenceBadge";
import { SourceBadge } from "../../components/ui/SourceBadge";
import { Language, HealthResponse, ModelReportResponse } from "../../types/api";
import { translations } from "../../i18n/translations";
import { getHealth, getModelReport } from "../../lib/api";

export default function TransparencyPage() {
  const [language, setLanguage] = useState<Language>("kn");
  const t = translations[language];

  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [report, setReport] = useState<ModelReportResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedLang = localStorage.getItem("fsa_lang") as Language;
      if (savedLang && ["en", "hi", "kn"].includes(savedLang)) {
        setLanguage(savedLang);
      }
    }

    getHealth()
      .then((h) => setHealth(h))
      .catch((e) => console.warn(e));

    getModelReport()
      .then((rep) => {
        setReport(rep);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed loading model report:", err);
        setLoading(false);
      });
  }, []);

  const handleLanguageChange = (newLang: Language) => {
    setLanguage(newLang);
    if (typeof window !== "undefined") {
      localStorage.setItem("fsa_lang", newLang);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-cream dark:bg-cream-dark text-ink dark:text-ink-dark">
      <Header
        language={language}
        onLanguageChange={handleLanguageChange}
        health={health}
      />

      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6 min-w-0">
        <div className="space-y-1 pb-2 border-b border-divider/60 dark:border-divider-dark">
          <h2 className="text-xl sm:text-2xl font-black text-ink dark:text-ink-dark">
            {t.reliabilityTitle}
          </h2>
          <p className="text-xs sm:text-sm text-ink-muted dark:text-ink-muted-dark leading-relaxed">
            {t.reliabilitySubtitle}
          </p>
        </div>

        {loading ? (
          <div className="p-8 text-center text-sm font-bold text-ink-muted animate-pulse">
            Loading validation metrics from model registry...
          </div>
        ) : report ? (
          <div className="space-y-6">
            {/* 1. TRAFFIC LIGHT STATUS PER HORIZON */}
            <section className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-5 shadow-card space-y-3">
              <h3 className="font-extrabold text-base text-ink dark:text-ink-dark">
                {t.trafficLightTitle}
              </h3>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                {[
                  { days: "7d", label: t.horizon7d, level: "low" as const, reason: "Naive baseline is sticky in 7-day spot pricing" },
                  { days: "14d", label: t.horizon14d, level: "medium" as const, reason: "Captures arrival trend shifts" },
                  { days: "30d", label: t.horizon30d, level: "high" as const, reason: "Decisively outperforms naive baseline" },
                ].map((item) => (
                  <div
                    key={item.days}
                    className="p-3 rounded-2xl bg-surface-low dark:bg-surface-low-dark border border-divider/60 dark:border-divider-dark space-y-1"
                  >
                    <span className="font-bold text-sm block text-ink dark:text-ink-dark">
                      {item.label}
                    </span>
                    <ConfidenceBadge
                      level={item.level}
                      label={
                        item.level === "high"
                          ? t.confidenceHigh
                          : item.level === "medium"
                          ? t.confidenceMedium
                          : t.confidenceLow
                      }
                      reason={item.reason}
                    />
                  </div>
                ))}
              </div>
            </section>

            {/* 2. BASELINE COMPARISON TABLE (Model vs Tomorrow = Today) */}
            <section className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-5 shadow-card space-y-3">
              <div className="space-y-0.5">
                <h3 className="font-extrabold text-base text-ink dark:text-ink-dark">
                  {t.baselineComparisonTitle}
                </h3>
                <p className="text-xs text-ink-muted dark:text-ink-muted-dark">
                  {t.baselineComparisonDesc}
                </p>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs tabular-nums">
                  <thead>
                    <tr className="border-b border-divider dark:border-divider-dark text-ink-muted dark:text-ink-muted-dark">
                      <th className="py-2 pr-2 font-bold">{t.colHorizon}</th>
                      <th className="py-2 px-2 font-bold">{t.colModelError}</th>
                      <th className="py-2 px-2 font-bold">{t.colSimpleGuessError}</th>
                      <th className="py-2 pl-2 font-bold">{t.colOutcome}</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-divider/40 dark:divide-divider-dark">
                    {report.metrics_table.map((row) => (
                      <tr key={row.horizon} className="hover:bg-surface-low">
                        <td className="py-2.5 pr-2 font-bold text-ink dark:text-ink-dark">
                          {row.horizon}
                        </td>
                        <td className="py-2.5 px-2 font-semibold">
                          ₹{Math.round(row.lgb_p50_mae)} / qtl
                        </td>
                        <td className="py-2.5 px-2 text-ink-muted">
                          ₹{Math.round(row.naive_mae)} / qtl
                        </td>
                        <td className="py-2.5 pl-2 font-bold">
                          {row.beats_naive ? (
                            <span className="text-primary dark:text-primary-dark">
                              ✓ {t.beatsSimpleGuess}
                            </span>
                          ) : (
                            <span className="text-caution">
                              ⚠️ {t.doesNotBeatSimpleGuess}
                            </span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>

            {/* 3. COVERAGE AUDIT (Target 70-90%) */}
            <section className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-5 shadow-card space-y-3">
              <div className="space-y-0.5">
                <h3 className="font-extrabold text-base text-ink dark:text-ink-dark">
                  {t.coverageTitle}
                </h3>
                <p className="text-xs text-ink-muted dark:text-ink-muted-dark">
                  {t.coverageDesc}
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs">
                {report.coverage_audit.map((aud) => (
                  <div
                    key={aud.horizon}
                    className="p-3 rounded-2xl bg-surface-low dark:bg-surface-low-dark border border-divider/60 dark:border-divider-dark space-y-1"
                  >
                    <span className="font-bold text-ink dark:text-ink-dark block">
                      {aud.horizon} {language === "kn" ? "ದಿನ" : "Days"}
                    </span>
                    <span className="text-lg font-black text-primary dark:text-primary-dark tabular-nums block">
                      {Math.round(aud.coverage_pct)}%
                    </span>
                    <span className="text-[11px] text-ink-muted dark:text-ink-muted-dark block">
                      {aud.target_band}
                    </span>
                  </div>
                ))}
              </div>
            </section>

            {/* 4. ASSUMPTIONS VS MEASURED DATA */}
            <section className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-5 shadow-card space-y-3">
              <div className="space-y-0.5">
                <h3 className="font-extrabold text-base text-ink dark:text-ink-dark">
                  {t.assumptionsTitle}
                </h3>
                <p className="text-xs text-ink-muted dark:text-ink-muted-dark leading-relaxed">
                  {t.assumptionsDesc}
                </p>
              </div>

              <div className="space-y-2 text-xs">
                <div className="p-3 rounded-xl bg-surface-low dark:bg-surface-low-dark flex items-center justify-between">
                  <span className="font-bold text-ink dark:text-ink-dark">
                    Agmarknet Modal & Arrival Prices
                  </span>
                  <SourceBadge source="measured" label={t.sourceMeasured} />
                </div>
                <div className="p-3 rounded-xl bg-surface-low dark:bg-surface-low-dark flex items-center justify-between">
                  <span className="font-bold text-ink dark:text-ink-dark">
                    District Weather & Rainfall
                  </span>
                  <SourceBadge source="measured" label={t.sourceMeasured} />
                </div>
                <div className="p-3 rounded-xl bg-surface-low dark:bg-surface-low-dark flex items-center justify-between">
                  <span className="font-bold text-ink dark:text-ink-dark">
                    Freight Rate: ₹{report.assumptions?.transport_rate_per_km_qtl || 1.6}/km/qtl
                  </span>
                  <SourceBadge source="assumption" label={t.sourceAssumption} />
                </div>
                <div className="p-3 rounded-xl bg-surface-low dark:bg-surface-low-dark flex items-center justify-between">
                  <span className="font-bold text-ink dark:text-ink-dark">
                    APMC Cess: {report.assumptions?.mandi_fee_pct || 1.5}% + Hamali: {report.assumptions?.commission_pct || 2.0}%
                  </span>
                  <SourceBadge source="assumption" label={t.sourceAssumption} />
                </div>
              </div>
            </section>

            {/* 5. KNOWN LIMITATIONS */}
            <section className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-5 shadow-card space-y-3">
              <h3 className="font-extrabold text-base text-ink dark:text-ink-dark">
                {t.limitsTitle}
              </h3>
              <ul className="list-disc pl-5 space-y-1.5 text-xs text-ink-muted dark:text-ink-muted-dark leading-relaxed">
                {report.limitations.map((lim, idx) => (
                  <li key={idx}>{lim}</li>
                ))}
              </ul>
            </section>
          </div>
        ) : (
          <div className="p-6 text-center text-xs text-risk">
            Unable to connect to model report service.
          </div>
        )}
      </main>

      <BottomNav language={language} />
    </div>
  );
}
