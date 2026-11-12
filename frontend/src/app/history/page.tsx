"use client";

import React, { useState, useEffect } from "react";
import { Header } from "../../components/Header";
import { BottomNav } from "../../components/BottomNav";
import { Toast } from "../../components/ui/Toast";
import { Language, HealthResponse, HistoryRecord } from "../../types/api";
import { translations } from "../../i18n/translations";
import { getHealth } from "../../lib/api";

export default function HistoryPage() {
  const [language, setLanguage] = useState<Language>("kn");
  const t = translations[language];

  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [records, setRecords] = useState<HistoryRecord[]>([]);
  const [actualPrices, setActualPrices] = useState<Record<string, string>>({});
  const [toastMessage, setToastMessage] = useState("");
  const [toastVisible, setToastVisible] = useState(false);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedLang = localStorage.getItem("fsa_lang") as Language;
      if (savedLang && ["en", "hi", "kn"].includes(savedLang)) {
        setLanguage(savedLang);
      }
      try {
        const hist: HistoryRecord[] = JSON.parse(
          localStorage.getItem("fsa_history") || "[]"
        );
        setRecords(hist);
      } catch {
        setRecords([]);
      }
    }

    getHealth()
      .then((h) => setHealth(h))
      .catch((e) => console.warn(e));
  }, []);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setToastVisible(true);
    setTimeout(() => setToastVisible(false), 3000);
  };

  const handleLanguageChange = (newLang: Language) => {
    setLanguage(newLang);
    if (typeof window !== "undefined") {
      localStorage.setItem("fsa_lang", newLang);
    }
  };

  const handleSaveActualPrice = (id: string) => {
    const entered = actualPrices[id];
    if (!entered) return;

    const numVal = parseFloat(entered);
    if (isNaN(numVal) || numVal <= 0) return;

    const updated = records.map((rec) =>
      rec.id === id ? { ...rec, actualPriceReceived: numVal } : rec
    );
    setRecords(updated);
    if (typeof window !== "undefined") {
      localStorage.setItem("fsa_history", JSON.stringify(updated));
    }
    showToast(t.savedSuccess);
  };

  const handleClearHistory = () => {
    if (confirm("Clear all past advice history?")) {
      setRecords([]);
      if (typeof window !== "undefined") {
        localStorage.removeItem("fsa_history");
      }
      showToast("History cleared");
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-cream dark:bg-cream-dark text-ink dark:text-ink-dark">
      <Header
        language={language}
        onLanguageChange={handleLanguageChange}
        health={health}
      />

      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-5 min-w-0">
        <div className="flex items-center justify-between pb-2 border-b border-divider/60 dark:border-divider-dark">
          <div className="space-y-0.5">
            <h2 className="text-xl sm:text-2xl font-black text-ink dark:text-ink-dark">
              {t.historyTitle}
            </h2>
            <p className="text-xs text-ink-muted dark:text-ink-muted-dark">
              Track your past advice and log the real prices you received at the mandi.
            </p>
          </div>

          {records.length > 0 && (
            <button
              type="button"
              onClick={handleClearHistory}
              className="text-xs font-bold text-risk underline select-none p-1"
            >
              Clear
            </button>
          )}
        </div>

        {/* Empty State */}
        {records.length === 0 ? (
          <div className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-8 text-center space-y-3 shadow-card">
            <span className="material-symbols-outlined text-4xl text-ink-muted">
              history_toggle_off
            </span>
            <p className="text-sm font-semibold text-ink-muted dark:text-ink-muted-dark max-w-sm mx-auto">
              {t.historyEmpty}
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {records.map((rec) => (
              <div
                key={rec.id}
                className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-5 shadow-card space-y-3"
              >
                <div className="flex items-start justify-between gap-2 border-b border-divider/60 dark:border-divider-dark pb-2.5">
                  <div>
                    <span className="text-xs text-ink-muted dark:text-ink-muted-dark block">
                      {new Date(rec.timestamp).toLocaleDateString()}
                    </span>
                    <h3 className="font-extrabold text-base text-ink dark:text-ink-dark">
                      🧅 {rec.crop} • {rec.quantity} Quintals
                    </h3>
                  </div>

                  <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-primary-tint dark:bg-primary/20 text-primary dark:text-primary-dark">
                    📍 {rec.recommendedMandi || rec.mandi}
                  </span>
                </div>

                <p className="text-sm font-bold text-ink dark:text-ink-dark leading-snug">
                  "{rec.recommendation}"
                </p>

                {/* Field: What price did you actually get? */}
                <div className="p-3.5 rounded-2xl bg-surface-low dark:bg-surface-low-dark border border-divider/60 dark:border-divider-dark space-y-2">
                  <span className="text-xs font-bold text-ink dark:text-ink-dark block">
                    {t.actualPriceQuestion}
                  </span>

                  {rec.actualPriceReceived ? (
                    <div className="flex items-center gap-2 text-sm font-black text-primary dark:text-primary-dark">
                      <span className="material-symbols-outlined text-[18px]">
                        check_circle
                      </span>
                      <span>
                        ₹{Math.round(rec.actualPriceReceived)} / qtl (Recorded)
                      </span>
                    </div>
                  ) : (
                    <div className="flex items-center gap-2">
                      <div className="relative flex-1">
                        <span className="absolute left-3 top-2.5 text-xs text-ink-muted">
                          ₹
                        </span>
                        <input
                          type="number"
                          placeholder="e.g. 3500"
                          value={actualPrices[rec.id] || ""}
                          onChange={(e) =>
                            setActualPrices({
                              ...actualPrices,
                              [rec.id]: e.target.value,
                            })
                          }
                          className="w-full h-10 pl-7 pr-3 rounded-xl bg-white dark:bg-surface-dark border border-divider text-xs font-bold text-ink dark:text-ink-dark focus:outline-none focus:ring-2 focus:ring-primary tabular-nums"
                        />
                      </div>
                      <button
                        type="button"
                        onClick={() => handleSaveActualPrice(rec.id)}
                        className="h-10 px-3.5 rounded-xl bg-primary text-white text-xs font-bold touch-press"
                      >
                        {t.saveActualPriceBtn}
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      <BottomNav language={language} />
      <Toast message={toastMessage} visible={toastVisible} />
    </div>
  );
}
