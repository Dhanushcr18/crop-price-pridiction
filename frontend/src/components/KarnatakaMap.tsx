"use client";

import React, { useState } from "react";
import { MandiDetailItem, Language } from "../types/api";
import { translations } from "../i18n/translations";

interface KarnatakaMapProps {
  mandis: MandiDetailItem[];
  selectedMandi: string;
  onSelectMandi: (mandiName: string, district: string) => void;
  language: Language;
}

export const KarnatakaMap: React.FC<KarnatakaMapProps> = ({
  mandis,
  selectedMandi,
  onSelectMandi,
  language,
}) => {
  const t = translations[language];
  const [hoveredMandi, setHoveredMandi] = useState<MandiDetailItem | null>(null);

  // Geographic bounds for Karnataka
  // Min Lon: 74.0, Max Lon: 78.6
  // Min Lat: 11.5, Max Lat: 18.5
  const minLon = 74.0;
  const maxLon = 78.6;
  const minLat = 11.5;
  const maxLat = 18.5;

  const width = 360;
  const height = 440;

  const project = (lat?: number | null, lon?: number | null) => {
    if (!lat || !lon) return null;
    const x = ((lon - minLon) / (maxLon - minLon)) * (width - 40) + 20;
    const y = ((maxLat - lat) / (maxLat - minLat)) * (height - 40) + 20;
    return { x, y };
  };

  return (
    <div className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-5 shadow-card space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h4 className="font-extrabold text-sm sm:text-base text-ink dark:text-ink-dark">
            {t.karnatakaMapTitle}
          </h4>
          <p className="text-xs text-ink-muted">
            {t.karnatakaMapSubtitle}
          </p>
        </div>

        {/* Legend */}
        <div className="flex items-center gap-3 text-[11px] font-bold">
          <div className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-600" />
            <span className="text-ink-muted">{t.legendTierB}</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
            <span className="text-ink-muted">{t.legendUnderReview}</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-slate-400" />
            <span className="text-ink-muted">{t.legendTierC}</span>
          </div>
        </div>
      </div>

      {/* SVG Canvas */}
      <div className="relative flex justify-center items-center bg-surface-low/40 dark:bg-surface-low-dark/40 rounded-2xl p-2 border border-divider/40 overflow-hidden">
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="w-full max-w-[340px] h-auto select-none"
        >
          {/* Karnataka Outline Silhouette (Stylized Boundary) */}
          <path
            d="M120 40 L210 25 L250 70 L280 130 L230 180 L250 250 L270 320 L240 390 L180 415 L140 370 L100 320 L70 240 L80 160 L120 110 Z"
            fill="currentColor"
            className="text-divider/30 dark:text-divider-dark/40 stroke-divider dark:stroke-divider-dark"
            strokeWidth="1.5"
            strokeDasharray="4 4"
          />

          {/* Mandi Dots */}
          {mandis.map((m) => {
            const pt = project(m.lat, m.lon);
            if (!pt) return null;

            const mName = m.name || m.name_en || m.mandi_id || "";
            const mDistrict = m.district || m.district_en || "";
            const isSelected =
              selectedMandi.toLowerCase() === mName.toLowerCase() ||
              (m.id && selectedMandi.toLowerCase() === m.id.toLowerCase()) ||
              (m.mandi_id && selectedMandi.toLowerCase() === m.mandi_id.toLowerCase());

            let dotColor = "#94A3B8"; // Tier C
            if (m.is_quarantined || m.all_quarantined) {
              dotColor = "#D97706"; // Under review
            } else if (m.tier === "Tier B") {
              dotColor = "#15803D"; // Tier B
            }

            return (
              <g
                key={m.id || m.mandi_id || mName}
                className="cursor-pointer"
                onClick={() => onSelectMandi(mName, mDistrict)}
                onMouseEnter={() => setHoveredMandi(m)}
                onMouseLeave={() => setHoveredMandi(null)}
              >
                {/* Ping circle if selected */}
                {isSelected && (
                  <circle
                    cx={pt.x}
                    cy={pt.y}
                    r={8}
                    fill="none"
                    stroke="#2E7D32"
                    strokeWidth="2"
                    className="animate-ping origin-center"
                  />
                )}
                <circle
                  cx={pt.x}
                  cy={pt.y}
                  r={isSelected ? 6 : 4}
                  fill={dotColor}
                  stroke={isSelected ? "#FFFFFF" : "none"}
                  strokeWidth={isSelected ? 2 : 0}
                  className="transition-all hover:scale-150 origin-center"
                />
              </g>
            );
          })}
        </svg>

        {/* Hover Tooltip */}
        {hoveredMandi && (
          <div className="absolute bottom-3 left-1/2 -translate-x-1/2 bg-ink/90 text-white text-xs font-bold px-3 py-1.5 rounded-xl shadow-lg pointer-events-none whitespace-nowrap">
            {(hoveredMandi.name || hoveredMandi.name_en)} ({(hoveredMandi.district || hoveredMandi.district_en)}) •{" "}
            {hoveredMandi.is_quarantined || hoveredMandi.all_quarantined
              ? t.dataUnderReview
              : hoveredMandi.tier === "Tier B"
              ? t.legendTierB
              : t.legendTierC}
          </div>
        )}
      </div>
    </div>
  );
};
