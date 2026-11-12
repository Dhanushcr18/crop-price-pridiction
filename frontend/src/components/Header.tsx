import React, { useState, useEffect } from "react";
import Link from "next/link";
import { Language, HealthResponse } from "../types/api";
import { translations } from "../i18n/translations";
import { LanguageSwitcher } from "./ui/LanguageSwitcher";
import { AlertBanner } from "./ui/AlertBanner";
import { OnionIcon } from "./ui/Icons";

export interface HeaderProps {
  language: Language;
  onLanguageChange: (lang: Language) => void;
  onOpenSettings?: () => void;
  health?: HealthResponse | null;
}

export const Header: React.FC<HeaderProps> = ({
  language,
  onLanguageChange,
  onOpenSettings,
  health,
}) => {
  const t = translations[language];
  const [isOnline, setIsOnline] = useState(true);

  const isSynthetic = health?.is_synthetic ?? true;
  const isStale = health?.is_stale ?? false;
  const lastDate = health?.last_data_date ?? "2026-11-03";

  useEffect(() => {
    if (typeof window !== "undefined") {
      setIsOnline(navigator.onLine);
      const handleOnline = () => setIsOnline(true);
      const handleOffline = () => setIsOnline(false);

      window.addEventListener("online", handleOnline);
      window.addEventListener("offline", handleOffline);

      return () => {
        window.removeEventListener("online", handleOnline);
        window.removeEventListener("offline", handleOffline);
      };
    }
  }, []);

  return (
    <header className="sticky top-0 z-40 bg-white/95 dark:bg-surface-dark/95 backdrop-blur-md border-b border-divider dark:border-divider-dark select-none">
      {/* 1. SYNTHETIC DATA BANNER (Strict Hard Rule: On Every Screen, Non-Dismissible) */}
      {isSynthetic && (
        <AlertBanner type="synthetic" message={t.syntheticBanner} />
      )}

      {/* 2. STALE DATA BANNER (Yellow Warning if last data > 3 days) */}
      {isStale && (
        <AlertBanner
          type="stale"
          message={t.staleDataBanner.replace("{date}", lastDate)}
        />
      )}

      {/* 3. OFFLINE BANNER */}
      {!isOnline && <AlertBanner type="offline" message={t.offlineBanner} />}

      {/* Main Bar: Logo, Online Dot, Language Switcher, Settings */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex items-center justify-between gap-3">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-2.5 min-w-0 focus:outline-none">
          <div className="w-10 h-10 rounded-xl bg-primary text-white flex items-center justify-center shadow-touch shrink-0">
            <OnionIcon size={24} />
          </div>
          <div className="min-w-0">
            <div className="flex items-center gap-1.5">
              <h1 className="font-extrabold text-base sm:text-lg text-ink dark:text-ink-dark truncate leading-tight">
                {t.appName}
              </h1>
              {/* Online/Offline status dot */}
              <span
                className={`w-2 h-2 rounded-full shrink-0 ${
                  isOnline ? "bg-primary" : "bg-caution"
                }`}
                title={isOnline ? t.online : t.offline}
              />
            </div>
            <p className="text-xs text-ink-muted dark:text-ink-muted-dark truncate hidden sm:block">
              {t.appTagline}
            </p>
          </div>
        </Link>

        {/* Right Controls: Language Switcher & Settings */}
        <div className="flex items-center gap-2 shrink-0">
          <LanguageSwitcher
            currentLanguage={language}
            onLanguageChange={onLanguageChange}
          />

          {onOpenSettings && (
            <button
              type="button"
              aria-label={t.settings}
              onClick={onOpenSettings}
              className="w-10 h-10 rounded-xl bg-surface-low dark:bg-surface-low-dark border border-divider dark:border-divider-dark flex items-center justify-center text-ink-muted hover:text-ink dark:text-ink-muted-dark dark:hover:text-ink-dark transition-colors touch-press"
            >
              <span className="material-symbols-outlined text-[20px]">
                settings
              </span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
