import React, { useState } from "react";
import { ForecastHorizonDetail, Language } from "../../types/api";
import { formatCurrency } from "../../lib/formatter";

export interface ChartCardProps {
  horizons: ForecastHorizonDetail[];
  spotPriceToday: number;
  language: Language;
  title: string;
  subtitle: string;
  axisPriceText: string;
  axisDaysText: string;
  rangeLegendText: string;
  medianLegendText: string;
}

export const ChartCard: React.FC<ChartCardProps> = ({
  horizons,
  spotPriceToday,
  language,
  title,
  subtitle,
  axisPriceText,
  axisDaysText,
  rangeLegendText,
  medianLegendText,
}) => {
  const [selectedHorizon, setSelectedHorizon] = useState<number>(7);

  if (!horizons || horizons.length === 0) {
    return (
      <div className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-5 sm:p-6 shadow-card space-y-4">
        <div className="space-y-1">
          <h3 className="font-extrabold text-lg text-ink dark:text-ink-dark">{title}</h3>
          {subtitle && <p className="text-xs text-ink-muted dark:text-ink-muted-dark">{subtitle}</p>}
        </div>
        <div className="h-48 rounded-2xl bg-surface-low dark:bg-surface-low-dark border border-divider/60 flex flex-col items-center justify-center text-center p-4 space-y-2">
          <span className="material-symbols-outlined text-4xl text-ink-muted">query_stats</span>
          <p className="text-sm font-bold text-ink dark:text-ink-dark">
            {language === "kn" ? "ಮುನ್ಸೂಚನೆ ಲಭ್ಯವಿಲ್ಲ (ಮಾಹಿತಿ ಅಲಭ್ಯ)" : language === "hi" ? "पूर्वानुमान उपलब्ध नहीं है" : "Forecast Not Available"}
          </p>
          <p className="text-xs text-ink-muted max-w-sm">
            {language === "kn"
              ? "ಕರ್ನಾಟಕ ಮಂಡಿಗಳಿಗೆ ನೈಜ ಮಾರುಕಟ್ಟೆ ದತ್ತಾಂಶ ಬಂದ ನಂತರ ಮುನ್ಸೂಚನೆ ಲಭ್ಯವಾಗಲಿದೆ."
              : language === "hi"
              ? "सत्यापित मंडी डेटा उपलब्ध होने के बाद ही मॉडल पूर्वानुमान दिखाएगा।"
              : "Awaiting verified continuous real mandi data before model forecast is displayed."}
          </p>
        </div>
      </div>
    );
  }

  // SVG Geometry
  const width = 480;
  const height = 240;
  const padding = { top: 30, right: 30, bottom: 40, left: 65 };
  const plotWidth = width - padding.left - padding.right;
  const plotHeight = height - padding.top - padding.bottom;

  const days = [0, 7, 14, 30];
  const xCoords: Record<number, number> = {
    0: padding.left,
    7: padding.left + plotWidth * 0.28,
    14: padding.left + plotWidth * 0.58,
    30: padding.left + plotWidth,
  };

  // Find min and max for Y scaling
  let minPrice = spotPriceToday - 100;
  let maxPrice = spotPriceToday + 100;

  horizons.forEach((h) => {
    if (h.p10_downside < minPrice) minPrice = h.p10_downside;
    if (h.p90_upside > maxPrice) maxPrice = h.p90_upside;
  });

  const yMin = Math.floor((minPrice - 150) / 100) * 100;
  const yMax = Math.ceil((maxPrice + 150) / 100) * 100;

  const getY = (val: number) => {
    return padding.top + plotHeight - ((val - yMin) / (yMax - yMin)) * plotHeight;
  };

  const points: Record<number, { p10: number; p50: number; p90: number }> = {
    0: { p10: spotPriceToday, p50: spotPriceToday, p90: spotPriceToday },
  };

  horizons.forEach((h) => {
    points[h.horizon_days] = {
      p10: h.p10_downside,
      p50: h.p50_expected,
      p90: h.p90_upside,
    };
  });

  const topPath = days.map((d) => `${xCoords[d]},${getY(points[d].p90)}`).join(" L ");
  const bottomPath = [...days]
    .reverse()
    .map((d) => `${xCoords[d]},${getY(points[d].p10)}`)
    .join(" L ");
  const fanAreaD = `M ${topPath} L ${bottomPath} Z`;
  const p50LineD = "M " + days.map((d) => `${xCoords[d]},${getY(points[d].p50)}`).join(" L ");

  const yTicks = [
    yMin,
    Math.round(yMin + (yMax - yMin) * 0.33),
    Math.round(yMin + (yMax - yMin) * 0.66),
    yMax,
  ];

  const activeDetail = horizons.find((h) => h.horizon_days === selectedHorizon);

  return (
    <div className="w-full bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-2xl p-4 sm:p-5 shadow-card space-y-4 min-w-0">
      {/* Title & Subtitle */}
      <div className="space-y-1 border-b border-divider/60 dark:border-divider-dark pb-3">
        <h3 className="font-extrabold text-base sm:text-lg text-ink dark:text-ink-dark">
          {title}
        </h3>
        <p className="text-xs text-ink-muted dark:text-ink-muted-dark">
          {subtitle}
        </p>

        {/* Legend */}
        <div className="flex items-center gap-3 pt-2 text-xs font-semibold text-ink-muted dark:text-ink-muted-dark">
          <div className="flex items-center gap-1.5">
            <span className="w-3.5 h-3.5 rounded bg-primary-tint dark:bg-primary/30 border border-primary/40 inline-block" />
            <span>{rangeLegendText}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-4 h-1 bg-primary dark:bg-primary-dark inline-block rounded" />
            <span>{medianLegendText}</span>
          </div>
        </div>
      </div>

      {/* Horizon Selector Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 select-none">
        {horizons.map((h) => (
          <button
            key={h.horizon_days}
            type="button"
            onClick={() => setSelectedHorizon(h.horizon_days)}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all shrink-0 ${
              selectedHorizon === h.horizon_days
                ? "bg-primary text-white shadow-touch"
                : "bg-surface-low dark:bg-surface-low-dark text-ink dark:text-ink-dark border border-divider dark:border-divider-dark"
            }`}
          >
            {h.horizon_days}{" "}
            {language === "kn" ? "ದಿನ" : language === "hi" ? "दिन" : "Days"}
          </button>
        ))}
      </div>

      {/* SVG Container */}
      <div className="w-full overflow-hidden">
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="w-full h-auto max-h-[260px]"
          aria-label={title}
          role="img"
        >
          {/* Grid lines */}
          {yTicks.map((tickVal) => {
            const y = getY(tickVal);
            return (
              <g key={tickVal}>
                <line
                  x1={padding.left}
                  y1={y}
                  x2={width - padding.right}
                  y2={y}
                  stroke="currentColor"
                  className="text-divider dark:text-divider-dark"
                  strokeDasharray="4 4"
                  strokeWidth="1"
                />
                <text
                  x={padding.left - 8}
                  y={y + 4}
                  textAnchor="end"
                  className="text-[11px] font-semibold fill-ink-muted dark:fill-ink-muted-dark tabular-nums"
                >
                  ₹{Math.round(tickVal)}
                </text>
              </g>
            );
          })}

          {/* Shaded P10-P90 Fan Area */}
          <path
            d={fanAreaD}
            className="fill-primary/20 dark:fill-primary/30"
          />

          {/* Median P50 Line */}
          <path
            d={p50LineD}
            fill="none"
            className="stroke-primary dark:stroke-primary-dark"
            strokeWidth="3"
            strokeLinecap="round"
          />

          {/* Data Points */}
          {days.map((d) => {
            const pt = points[d];
            const isSelected = d === selectedHorizon;
            return (
              <g key={d}>
                {/* Vertical marker for selected */}
                {isSelected && (
                  <line
                    x1={xCoords[d]}
                    y1={padding.top}
                    x2={xCoords[d]}
                    y2={padding.top + plotHeight}
                    stroke="currentColor"
                    className="text-primary/40 dark:text-primary-dark/40"
                    strokeDasharray="2 2"
                    strokeWidth="1.5"
                  />
                )}
                {/* P50 Circle */}
                <circle
                  cx={xCoords[d]}
                  cy={getY(pt.p50)}
                  r={isSelected ? 6 : 4}
                  className="fill-primary dark:fill-primary-dark stroke-white dark:stroke-surface-dark"
                  strokeWidth="2"
                />
                {/* X-axis Label */}
                <text
                  x={xCoords[d]}
                  y={height - 12}
                  textAnchor="middle"
                  className={`text-[12px] tabular-nums font-bold ${
                    isSelected
                      ? "fill-primary dark:fill-primary-dark"
                      : "fill-ink-muted dark:fill-ink-muted-dark"
                  }`}
                >
                  {d === 0 ? "Today" : `${d}d`}
                </text>
              </g>
            );
          })}

          {/* Plain Axis Labels */}
          <text
            x={14}
            y={height / 2}
            textAnchor="middle"
            transform={`rotate(-90 14 ${height / 2})`}
            className="text-[11px] font-bold fill-ink-muted dark:fill-ink-muted-dark uppercase tracking-wider"
          >
            {axisPriceText}
          </text>
          <text
            x={width / 2}
            y={height - 2}
            textAnchor="middle"
            className="text-[11px] font-bold fill-ink-muted dark:fill-ink-muted-dark uppercase tracking-wider"
          >
            {axisDaysText}
          </text>
        </svg>
      </div>

      {/* Selected Horizon Callout Details */}
      {activeDetail && (
        <div className="bg-surface-low dark:bg-surface-low-dark p-3.5 rounded-xl border border-divider/60 dark:border-divider-dark flex items-center justify-between text-xs sm:text-sm font-semibold tabular-nums">
          <div className="space-y-0.5">
            <span className="text-ink-muted dark:text-ink-muted-dark block">
              {activeDetail.horizon_days}{" "}
              {language === "kn" ? "ದಿನಗಳ ನಂತರ" : language === "hi" ? "दिन बाद" : "Days ahead"}:
            </span>
            <span className="font-bold text-primary dark:text-primary-dark text-base">
              {formatCurrency(activeDetail.p10_downside, false)} – {formatCurrency(activeDetail.p90_upside, false)}
            </span>
          </div>
          <div className="text-right text-xs text-ink-muted dark:text-ink-muted-dark">
            <span>
              {language === "kn" ? "ಅಂದಾಜು" : language === "hi" ? "संभावित" : "Likely"}:{" "}
            </span>
            <span className="font-bold text-ink dark:text-ink-dark">
              {formatCurrency(activeDetail.p50_expected, false)}
            </span>
          </div>
        </div>
      )}

      {/* Accessible Screen-Reader Table (Offscreen) */}
      <div className="fixed -left-[9999px] top-0 w-1 h-1 overflow-hidden" aria-hidden="false">
        <table>
          <caption>Price Outlook Forecast Table</caption>
          <thead>
            <tr>
              <th scope="col">Horizon (Days)</th>
              <th scope="col">P10 Downside</th>
              <th scope="col">P50 Expected</th>
              <th scope="col">P90 Upside</th>
            </tr>
          </thead>
          <tbody>
            {horizons.map((h) => (
              <tr key={h.horizon_days}>
                <td>{h.horizon_days} days</td>
                <td>₹{Math.round(h.p10_downside)}</td>
                <td>₹{Math.round(h.p50_expected)}</td>
                <td>₹{Math.round(h.p90_upside)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
