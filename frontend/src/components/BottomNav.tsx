import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Language } from "../types/api";
import { translations } from "../i18n/translations";

export interface BottomNavProps {
  language: Language;
}

export const BottomNav: React.FC<BottomNavProps> = ({ language }) => {
  const pathname = usePathname();
  const t = translations[language];

  const navItems = [
    {
      href: "/",
      label: t.tabAdvice,
      icon: "insights",
      isActive: pathname === "/",
    },
    {
      href: "/history",
      label: t.tabHistory,
      icon: "history",
      isActive: pathname === "/history",
    },
    {
      href: "/transparency",
      label: t.tabReliability,
      icon: "verified",
      isActive: pathname === "/transparency",
    },
    {
      href: "/help",
      label: t.tabHelp,
      icon: "help_outline",
      isActive: pathname === "/help",
    },
  ];

  return (
    <nav
      aria-label="Main Navigation"
      className="sticky bottom-0 z-40 w-full bg-white/95 dark:bg-surface-dark/95 backdrop-blur-md border-t border-divider dark:border-divider-dark select-none shadow-elevated"
    >
      <div className="max-w-md mx-auto grid grid-cols-4 h-16 px-2">
        {navItems.map((item) => {
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex flex-col items-center justify-center min-h-[56px] transition-colors duration-fast rounded-xl py-1 ${
                item.isActive
                  ? "text-primary dark:text-primary-dark font-black"
                  : "text-ink-muted hover:text-ink dark:text-ink-muted-dark dark:hover:text-ink-dark font-semibold"
              }`}
            >
              <span
                className={`material-symbols-outlined text-[24px] ${
                  item.isActive ? "font-bold scale-110" : ""
                }`}
              >
                {item.icon}
              </span>
              <span className="text-[11px] leading-tight mt-0.5 truncate max-w-full px-1">
                {item.label}
              </span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
};

