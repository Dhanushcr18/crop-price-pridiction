import React from "react";

export interface ConfidenceBadgeProps {
  level: "high" | "medium" | "low" | "fair" | string;
  label: string;
  reason?: string | null;
  className?: string;
}

export const ConfidenceBadge: React.FC<ConfidenceBadgeProps> = ({
  level,
  label,
  reason,
  className = "",
}) => {
  const normalized = (level || "medium").toLowerCase();
  const key = normalized === "fair" ? "medium" : (["high", "medium", "low"].includes(normalized) ? normalized : "medium");

  const configMap: Record<string, { bg: string; text: string; border: string; icon: string }> = {
    high: {
      bg: "bg-primary-tint dark:bg-primary/20",
      text: "text-primary dark:text-primary-dark",
      border: "border-primary/30",
      icon: "verified",
    },
    medium: {
      bg: "bg-caution-light dark:bg-caution/20",
      text: "text-caution dark:text-caution-dark",
      border: "border-caution/30",
      icon: "info",
    },
    low: {
      bg: "bg-caution-light dark:bg-caution/20",
      text: "text-caution dark:text-caution-dark",
      border: "border-caution/40",
      icon: "warning",
    },
  };

  const config = configMap[key] || configMap.medium;

  return (
    <div className={`inline-flex flex-col gap-1 ${className}`}>
      <div
        className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold border ${config.bg} ${config.text} ${config.border} select-none shrink-0`}
      >
        <span className="material-symbols-outlined text-[16px] shrink-0">
          {config.icon}
        </span>
        <span className="truncate">{label}</span>
      </div>
      {reason && (key === "low" || normalized === "low") && (
        <span className="text-[12px] text-caution dark:text-caution-dark leading-tight block">
          {reason}
        </span>
      )}
    </div>
  );
};

