import React from "react";

export interface SelectCardProps {
  selected?: boolean;
  disabled?: boolean;
  title: string;
  subtitle?: string;
  description?: string;
  badge?: string;
  badgeColor?: "primary" | "caution" | "risk" | "neutral";
  icon?: React.ReactNode;
  onClick?: () => void;
  className?: string;
}

export const SelectCard: React.FC<SelectCardProps> = ({
  selected = false,
  disabled = false,
  title,
  subtitle,
  description,
  badge,
  badgeColor = "neutral",
  icon,
  onClick,
  className = "",
}) => {
  const badgeStyle = {
    primary: "bg-primary-tint dark:bg-primary/20 text-primary dark:text-primary-dark",
    caution: "bg-caution-light dark:bg-caution/20 text-caution dark:text-caution-dark",
    risk: "bg-risk-light dark:bg-risk/20 text-risk dark:text-risk-dark",
    neutral: "bg-surface-high dark:bg-surface-high-dark text-ink-muted dark:text-ink-muted-dark",
  }[badgeColor];

  return (
    <div
      role="button"
      tabIndex={disabled ? -1 : 0}
      aria-disabled={disabled}
      aria-pressed={selected}
      onClick={disabled ? undefined : onClick}
      onKeyDown={(e) => {
        if (!disabled && (e.key === "Enter" || e.key === " ")) {
          e.preventDefault();
          onClick?.();
        }
      }}
      className={`relative w-full rounded-2xl p-4 sm:p-5 flex items-start justify-between gap-3.5 transition-all duration-fast select-none touch-press ${
        disabled
          ? "opacity-50 cursor-not-allowed bg-surface-low dark:bg-surface-low-dark border border-divider dark:border-divider-dark"
          : selected
          ? "cursor-pointer bg-white dark:bg-surface-dark border-2 border-primary shadow-touch ring-2 ring-primary/20"
          : "cursor-pointer bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark hover:border-ink-subtle/50"
      } ${className}`}
    >
      <div className="flex items-start gap-3.5 min-w-0 flex-1">
        {icon && (
          <div
            className={`w-12 h-12 rounded-xl flex items-center justify-center shrink-0 text-2xl transition-colors ${
              selected
                ? "bg-primary-tint dark:bg-primary/20 text-primary"
                : "bg-surface-low dark:bg-surface-low-dark text-ink-muted"
            }`}
          >
            {typeof icon === "string" && /^[a-z_]+$/.test(icon) ? (
              <span className="material-symbols-outlined text-[26px]">{icon}</span>
            ) : (
              icon
            )}
          </div>
        )}
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="font-bold text-base sm:text-lg text-ink dark:text-ink-dark leading-snug">
              {title}
            </h3>
            {badge && (
              <span
                className={`px-2 py-0.5 rounded-full text-xs font-semibold uppercase tracking-wider shrink-0 ${badgeStyle}`}
              >
                {badge}
              </span>
            )}
          </div>
          {subtitle && (
            <p className="text-sm font-semibold text-primary dark:text-primary-dark mt-0.5">
              {subtitle}
            </p>
          )}
          {description && (
            <p className="text-sm text-ink-muted dark:text-ink-muted-dark mt-1 leading-relaxed">
              {description}
            </p>
          )}
        </div>
      </div>

      {/* Radio Indicator (56px touch friendly target) */}
      <div
        className={`w-7 h-7 rounded-full flex items-center justify-center shrink-0 mt-0.5 transition-colors ${
          selected
            ? "bg-primary text-white"
            : "border-2 border-divider dark:border-divider-dark bg-transparent"
        }`}
      >
        {selected && (
          <span className="material-symbols-outlined text-[18px]">check</span>
        )}
      </div>
    </div>
  );
};

