import React from "react";
import { formatPriceRange } from "../../lib/formatter";
import { Language } from "../../types/api";

export interface RangeDisplayProps {
  p10: number;
  p90: number;
  p50?: number;
  language: Language;
  isSynthetic?: boolean;
  demoBadgeText?: string;
  size?: "sm" | "md" | "lg";
  className?: string;
}

export const RangeDisplay: React.FC<RangeDisplayProps> = ({
  p10,
  p90,
  p50,
  language,
  isSynthetic = false,
  demoBadgeText = "Demo numbers",
  size = "lg",
  className = "",
}) => {
  const formatted = formatPriceRange(p10, p90, p50, language);

  const headlineSize = {
    sm: "text-lg sm:text-xl",
    md: "text-xl sm:text-2xl",
    lg: "text-2xl sm:text-3xl",
  }[size];

  return (
    <div className={`space-y-1 min-w-0 ${className}`}>
      {/* Primary Headline: Range strictly required */}
      <div className="flex items-center gap-2 flex-wrap">
        <span
          className={`font-black text-primary dark:text-primary-dark tabular-nums tracking-tight leading-tight ${headlineSize}`}
        >
          {formatted.headline}
        </span>
        {isSynthetic && (
          <span className="px-2 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider bg-risk-light dark:bg-risk/20 text-risk dark:text-risk-dark border border-risk/30 shrink-0">
            {demoBadgeText}
          </span>
        )}
      </div>

      {/* Secondary Middle Estimate */}
      <p className="text-sm font-semibold text-ink-muted dark:text-ink-muted-dark tabular-nums">
        {formatted.mostLikely}
      </p>
    </div>
  );
};

