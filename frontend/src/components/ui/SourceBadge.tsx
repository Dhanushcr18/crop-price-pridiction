import React from "react";

export interface SourceBadgeProps {
  source: "measured" | "assumption";
  label: string;
  className?: string;
}

export const SourceBadge: React.FC<SourceBadgeProps> = ({
  source,
  label,
  className = "",
}) => {
  const isMeasured = source === "measured";

  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold tracking-wide uppercase select-none shrink-0 ${
        isMeasured
          ? "bg-primary-tint dark:bg-primary/20 text-primary dark:text-primary-dark border border-primary/20"
          : "bg-surface-high dark:bg-surface-high-dark text-ink-muted dark:text-ink-muted-dark border border-divider dark:border-divider-dark"
      } ${className}`}
    >
      <span className="material-symbols-outlined text-[13px]">
        {isMeasured ? "analytics" : "tune"}
      </span>
      <span>{label}</span>
    </span>
  );
};

