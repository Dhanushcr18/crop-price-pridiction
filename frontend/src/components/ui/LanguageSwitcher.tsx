import React from "react";
import { Language } from "../../types/api";

export interface LanguageSwitcherProps {
  currentLanguage: Language;
  onLanguageChange: (lang: Language) => void;
  className?: string;
}

export const LanguageSwitcher: React.FC<LanguageSwitcherProps> = ({
  currentLanguage,
  onLanguageChange,
  className = "",
}) => {
  const languages: { code: Language; nativeLabel: string }[] = [
    { code: "kn", nativeLabel: "ಕನ್ನಡ" },
    { code: "hi", nativeLabel: "हिन्दी" },
    { code: "en", nativeLabel: "English" },
  ];

  return (
    <div
      role="radiogroup"
      aria-label="Select language"
      className={`inline-flex items-center p-1 bg-surface-low dark:bg-surface-low-dark border border-divider dark:border-divider-dark rounded-xl select-none ${className}`}
    >
      {languages.map((item) => {
        const isSelected = currentLanguage === item.code;
        return (
          <button
            key={item.code}
            type="button"
            role="radio"
            aria-checked={isSelected}
            onClick={() => onLanguageChange(item.code)}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all duration-fast select-none touch-press ${
              isSelected
                ? "bg-primary text-white shadow-touch"
                : "text-ink-muted hover:text-ink dark:text-ink-muted-dark dark:hover:text-ink-dark"
            }`}
          >
            {item.nativeLabel}
          </button>
        );
      })}
    </div>
  );
};

