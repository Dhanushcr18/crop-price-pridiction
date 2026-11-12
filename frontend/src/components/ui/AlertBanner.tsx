import React from "react";

export interface AlertBannerProps {
  type: "synthetic" | "stale" | "offline";
  message: string;
  className?: string;
}

export const AlertBanner: React.FC<AlertBannerProps> = ({
  type,
  message,
  className = "",
}) => {
  const config = {
    synthetic: {
      bg: "bg-risk text-white",
      icon: "shield_with_heart",
      role: "alert" as const,
    },
    stale: {
      bg: "bg-caution text-white",
      icon: "schedule",
      role: "status" as const,
    },
    offline: {
      bg: "bg-ink text-white dark:bg-surface-high-dark",
      icon: "wifi_off",
      role: "status" as const,
    },
  }[type];

  return (
    <div
      data-testid={type === "synthetic" ? "synthetic-banner" : undefined}
      role={config.role}
      className={`w-full py-2 px-3 sm:px-4 text-xs sm:text-sm font-bold flex items-center justify-center gap-2 text-center select-none shadow-sm ${config.bg} ${className}`}
    >
      <span className="material-symbols-outlined text-[18px] shrink-0">
        {config.icon}
      </span>
      <span className="leading-snug">{message}</span>
    </div>
  );
};
