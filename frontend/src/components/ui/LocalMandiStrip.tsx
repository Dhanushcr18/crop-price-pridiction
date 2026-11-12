import React from "react";
import { formatDistance, formatPriceRange } from "../../lib/formatter";
import { Language } from "../../types/api";
import { SourceBadge } from "./SourceBadge";

export interface LocalMandiStripProps {
  mandiName: string;
  netP10: number;
  netP50: number;
  netP90?: number;
  language: Language;
  title: string;
  desc: string;
  sourceMeasuredLabel: string;
}

export const LocalMandiStrip: React.FC<LocalMandiStripProps> = ({
  mandiName,
  netP10,
  netP50,
  netP90 = netP50 * 1.1,
  language,
  title,
  desc,
  sourceMeasuredLabel,
}) => {
  const range = formatPriceRange(netP10, netP90, netP50, language);

  return (
    <div data-testid="local-mandi-strip" className="w-full rounded-2xl bg-surface-low dark:bg-surface-low-dark border border-divider dark:border-divider-dark p-4 sm:p-5 space-y-2.5">
      <div className="flex items-start justify-between gap-2 flex-wrap">
        <div className="flex items-center gap-2">
          <span className="w-8 h-8 rounded-xl bg-surface-high dark:bg-surface-high-dark flex items-center justify-center text-ink-muted shrink-0">
            <span className="material-symbols-outlined text-[20px]">
              home_pin
            </span>
          </span>
          <div>
            <h4 className="font-bold text-base sm:text-lg text-ink dark:text-ink-dark">
              {mandiName}
            </h4>
            <span className="text-xs text-ink-muted dark:text-ink-muted-dark font-medium">
              {title}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-bold text-ink-muted whitespace-nowrap">
            {formatDistance(0, language)}
          </span>
          <SourceBadge source="measured" label={sourceMeasuredLabel} />
        </div>
      </div>

      {/* Net Price Range at Local Mandi */}
      <div className="bg-white dark:bg-surface-dark p-3 rounded-xl border border-divider/60 dark:border-divider-dark flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <span className="text-xs text-ink-muted dark:text-ink-muted-dark font-semibold block">
            {language === "kn"
              ? "ಸ್ಥಳೀಯ ಮಂಡಿ ನಿವ್ವಳ ಬೆಲೆ"
              : language === "hi"
              ? "स्थानीय मंडी शुद्ध भाव"
              : "Local mandi net price"}
          </span>
          <span className="text-xl sm:text-2xl font-black text-ink dark:text-ink-dark tabular-nums">
            {range.minFormatted} – {range.maxFormatted}
          </span>
        </div>
        <p className="text-xs text-ink-muted dark:text-ink-muted-dark max-w-xs leading-relaxed">
          {desc}
        </p>
      </div>
    </div>
  );
};
