"use client";

import React from "react";
import { AreaHistoryEntry } from "../../types/api";

export interface AreaBarChartProps {
  stateHistory: AreaHistoryEntry[];
  countryHistory?: AreaHistoryEntry[];
  language: string;
  title: string;
}

export const AreaBarChart: React.FC<AreaBarChartProps> = ({
  stateHistory,
  language,
  title,
}) => {
  if (!stateHistory || stateHistory.length === 0) {
    return null;
  }

  // Find max acres for scaling
  const maxAcres = Math.max(...stateHistory.map((h) => h.area_acres), 1);

  return (
    <div className="w-full bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-2xl p-4 sm:p-5 space-y-3 select-none">
      <div className="flex items-center justify-between">
        <h4 className="font-extrabold text-sm sm:text-base text-ink dark:text-ink-dark flex items-center gap-1.5">
          <span className="material-symbols-outlined text-primary text-[20px]">
            bar_chart
          </span>
          <span>{title}</span>
        </h4>
        <span className="text-[11px] font-bold text-ink-muted dark:text-ink-muted-dark">
          {language === "kn" ? "ಲಕ್ಷ ಎಕರೆಗಳಲ್ಲಿ" : language === "hi" ? "लाख एकड़ में" : "In Lakh Acres"}
        </span>
      </div>

      <div className="pt-2 flex items-end justify-between gap-2 h-[150px] w-full px-1">
        {stateHistory.map((item) => {
          const heightPct = Math.max(15, Math.round((item.area_acres / maxAcres) * 100));
          const lakhAcres = (item.area_acres / 100000.0).toFixed(1);

          return (
            <div
              key={item.year}
              className="flex-1 flex flex-col items-center justify-end h-full group"
            >
              {/* Value label */}
              <span
                className={`text-[10px] sm:text-[11px] font-extrabold mb-1 tabular-nums ${
                  item.is_current
                    ? "text-primary dark:text-primary-dark font-black"
                    : "text-ink-muted dark:text-ink-muted-dark"
                }`}
              >
                {lakhAcres}L
              </span>

              {/* Bar */}
              <div className="w-full max-w-[36px] bg-surface-low dark:bg-surface-low-dark rounded-t-lg overflow-hidden flex items-end h-[100px]">
                <div
                  style={{ height: `${heightPct}%` }}
                  className={`w-full rounded-t-lg transition-all duration-300 ${
                    item.is_current
                      ? "bg-primary dark:bg-primary-dark shadow-sm"
                      : "bg-ink-muted/30 dark:bg-ink-muted-dark/30 group-hover:bg-primary/50"
                  }`}
                />
              </div>

              {/* Year Label */}
              <span
                className={`text-[10px] sm:text-[11px] font-bold mt-1.5 truncate max-w-full text-center ${
                  item.is_current
                    ? "text-primary dark:text-primary-dark font-black"
                    : "text-ink-muted dark:text-ink-muted-dark"
                }`}
              >
                {item.year.replace("20", "'")}
              </span>
            </div>
          );
        })}
      </div>

      <div className="pt-2 border-t border-divider/60 dark:border-divider-dark flex items-center justify-between text-[11px] text-ink-muted dark:text-ink-muted-dark font-medium">
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-sm bg-primary dark:bg-primary-dark inline-block" />
          <span>{language === "kn" ? "ಪ್ರಸ್ತುತ ಋತು" : language === "hi" ? "वर्तमान मौसम" : "Current Season"}</span>
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-sm bg-ink-muted/30 dark:bg-ink-muted-dark/30 inline-block" />
          <span>{language === "kn" ? "ಹಿಂದಿನ ವರ್ಷಗಳು" : language === "hi" ? "पिछले वर्ष" : "Past 5 Years"}</span>
        </span>
      </div>
    </div>
  );
};
