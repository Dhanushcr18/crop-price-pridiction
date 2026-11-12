import React, { useState } from "react";
import { MandiRankCard, Language } from "../../types/api";
import { formatCurrency, formatDistance, formatPriceRange } from "../../lib/formatter";
import { SourceBadge } from "./SourceBadge";

export interface MandiCardProps {
  card: MandiRankCard;
  language: Language;
  quantityQuintals: number;
  isBest?: boolean;
  bestOptionBadgeText: string;
  priceYouMayGetText: string;
  worstCaseText: string;
  gainVsLocalText: string;
  gainTotalLotText: string;
  costsTakenOffText: string;
  transportCostText: string;
  mandiFeesText: string;
  shrinkageText: string;
  sourceAssumptionText: string;
  sourceMeasuredText: string;
}

export const MandiCard: React.FC<MandiCardProps> = ({
  card,
  language,
  quantityQuintals,
  isBest = false,
  bestOptionBadgeText,
  priceYouMayGetText,
  worstCaseText,
  gainVsLocalText,
  gainTotalLotText,
  costsTakenOffText,
  transportCostText,
  mandiFeesText,
  shrinkageText,
  sourceAssumptionText,
  sourceMeasuredText,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  // Guarantee headline range
  const priceRange = formatPriceRange(
    card.net_price_p10_downside,
    card.net_price_p90_upside || card.net_price_p50 * 1.1,
    card.net_price_p50,
    language
  );

  const gainPerQtl = Math.round(card.gain_over_local_per_qtl);
  const totalGain = Math.round(card.total_gain_rs || gainPerQtl * quantityQuintals);
  const hasGain = gainPerQtl > 0;

  return (
    <div
      className={`rounded-2xl border transition-all duration-fast p-4 sm:p-5 relative select-none w-full min-w-0 ${
        isBest
          ? "bg-white dark:bg-surface-dark border-2 border-primary shadow-touch ring-2 ring-primary/20"
          : "bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark shadow-card"
      }`}
    >
      {/* Top Bar: Rank, Name, Distance (nowrap!), Best Badge */}
      <div className="flex items-start justify-between gap-2.5 pb-3 border-b border-divider/60 dark:border-divider-dark min-w-0">
        <div className="flex items-center gap-2.5 min-w-0 flex-1">
          <span
            className={`w-8 h-8 rounded-xl flex items-center justify-center text-sm font-extrabold shrink-0 ${
              isBest
                ? "bg-primary text-white"
                : "bg-surface-low dark:bg-surface-low-dark text-ink dark:text-ink-dark border border-divider dark:border-divider-dark"
            }`}
          >
            #{card.rank}
          </span>
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2 flex-wrap">
              <h3 className="font-extrabold text-base sm:text-lg text-ink dark:text-ink-dark truncate">
                {card.mandi}
              </h3>
              {isBest && (
                <span className="px-2 py-0.5 rounded-full text-xs font-bold bg-primary-tint dark:bg-primary/20 text-primary dark:text-primary-dark border border-primary/20 shrink-0">
                  {bestOptionBadgeText}
                </span>
              )}
            </div>
            {/* Non-breaking distance string */}
            <span className="text-xs font-semibold text-ink-muted dark:text-ink-muted-dark whitespace-nowrap block mt-0.5">
              {formatDistance(card.distance_km, language)}
            </span>
          </div>
        </div>

        <SourceBadge source="measured" label={sourceMeasuredText} />
      </div>

      {/* Main Section: Price You May Get (Headline Range) - Stacks cleanly on 360px */}
      <div className="pt-3.5 pb-3 space-y-2 min-w-0">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-ink-muted dark:text-ink-muted-dark block">
            {priceYouMayGetText}
          </span>
          {/* Prominent Range */}
          <div className="text-2xl sm:text-3xl font-black text-primary dark:text-primary-dark tabular-nums tracking-tight leading-tight mt-0.5">
            {priceRange.minFormatted} – {priceRange.maxFormatted}
          </div>
          <span className="text-xs font-semibold text-ink-muted dark:text-ink-muted-dark tabular-nums block mt-0.5">
            {priceRange.mostLikely}
          </span>
        </div>

        {/* Worst Case line */}
        <div className="flex items-center gap-1.5 text-xs font-semibold text-ink-muted dark:text-ink-muted-dark pt-1">
          <span className="material-symbols-outlined text-caution text-[16px] shrink-0">
            warning
          </span>
          <span>{worstCaseText}:</span>
          <span className="font-bold text-ink dark:text-ink-dark tabular-nums">
            {formatCurrency(card.net_price_p10_downside, false)}
          </span>
        </div>
      </div>

      {/* Extra Gain vs Local Mandi Callout Strip */}
      {hasGain && (
        <div className="my-2.5 p-3 rounded-xl bg-primary-tint dark:bg-primary/10 border border-primary/20 flex flex-col sm:flex-row sm:items-center justify-between gap-1.5 min-w-0">
          <div className="flex items-center gap-1.5 text-xs font-bold text-primary dark:text-primary-dark min-w-0">
            <span className="material-symbols-outlined text-[18px] shrink-0">
              trending_up
            </span>
            <span className="truncate">{gainVsLocalText}:</span>
            <span className="tabular-nums whitespace-nowrap">
              +{formatCurrency(gainPerQtl, false)} / qtl
            </span>
          </div>
          <div className="text-xs font-black text-primary dark:text-primary-dark tabular-nums sm:text-right">
            +{formatCurrency(totalGain, true)} ({gainTotalLotText})
          </div>
        </div>
      )}

      {/* Expandable Deductions Accordion */}
      <div className="pt-2 border-t border-divider/60 dark:border-divider-dark">
        <button
          type="button"
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-full flex items-center justify-between text-xs font-bold text-ink-muted hover:text-ink dark:text-ink-muted-dark dark:hover:text-ink-dark py-1.5 focus:outline-none"
        >
          <span className="flex items-center gap-1.5 truncate">
            <span className="material-symbols-outlined text-[18px]">
              receipt_long
            </span>
            <span>{costsTakenOffText}</span>
          </span>
          <span className="material-symbols-outlined text-[18px] shrink-0">
            {isExpanded ? "expand_less" : "expand_more"}
          </span>
        </button>

        {isExpanded && (
          <div className="pt-2.5 pb-1 space-y-2 text-xs text-ink-muted dark:text-ink-muted-dark">
            <div className="flex items-center justify-between gap-2">
              <span className="flex items-center gap-1 truncate">
                <span className="material-symbols-outlined text-[15px]">
                  local_shipping
                </span>
                <span>{transportCostText}</span>
                <span className="whitespace-nowrap">
                  ({formatDistance(card.distance_km, language)})
                </span>
              </span>
              <span className="font-bold text-risk tabular-nums whitespace-nowrap">
                -{formatCurrency(card.transport_cost_per_qtl, false)}
              </span>
            </div>

            <div className="flex items-center justify-between gap-2">
              <span className="flex items-center gap-1 truncate">
                <span className="material-symbols-outlined text-[15px]">
                  store
                </span>
                <span>{mandiFeesText}</span>
              </span>
              <span className="font-bold text-risk tabular-nums whitespace-nowrap">
                -{formatCurrency(card.fees_and_commission_per_qtl, false)}
              </span>
            </div>

            <div className="flex items-center justify-between gap-2">
              <span className="flex items-center gap-1 truncate">
                <span className="material-symbols-outlined text-[15px]">
                  scale
                </span>
                <span>{shrinkageText}</span>
              </span>
              <span className="font-bold text-risk tabular-nums whitespace-nowrap">
                -{formatCurrency(card.shrinkage_loss_per_qtl, false)}
              </span>
            </div>

            <div className="pt-1 flex items-center justify-end">
              <SourceBadge source="assumption" label={sourceAssumptionText} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
