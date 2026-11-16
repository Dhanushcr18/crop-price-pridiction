"use client";

import React, { useState, useMemo } from "react";
import { CropInfo, Language } from "../types/api";
import { getCropIconComponent } from "./ui/Icons";
import { translations } from "../i18n/translations";

interface CropPickerProps {
  crops: CropInfo[];
  selectedCrop: string;
  onSelectCrop: (cropName: string) => void;
  language: Language;
}

export const CropPicker: React.FC<CropPickerProps> = ({
  crops,
  selectedCrop,
  onSelectCrop,
  language,
}) => {
  const t = translations[language];
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [displayCount, setDisplayCount] = useState<number>(24);

  const categories = useMemo(() => [
    { id: "all", label: t.allCategories },
    { id: "vegetable", label: t.catVegetable },
    { id: "fruit", label: t.catFruit },
    { id: "cereal", label: t.catCereal },
    { id: "pulse", label: t.catPulse },
    { id: "spice", label: t.catSpice },
    { id: "oilseed", label: t.catOilseed },
    { id: "plantation", label: t.catPlantation },
    { id: "other", label: t.catOther },
  ], [t]);

  const filteredCrops = useMemo(() => {
    return crops.filter((c) => {
      const matchesCategory =
        selectedCategory === "all" ||
        (c.category && c.category.toLowerCase() === selectedCategory.toLowerCase());
      if (!matchesCategory) return false;

      const cropName = c.name || c.name_en || c.crop_id;
      const cropKn = c.kannada_name || c.name_kn || "";
      const cropHi = c.hindi_name || c.name_hi || "";

      if (!searchTerm.trim()) return true;
      const q = searchTerm.toLowerCase();
      return (
        cropName.toLowerCase().includes(q) ||
        cropKn.toLowerCase().includes(q) ||
        cropHi.toLowerCase().includes(q)
      );
    });
  }, [crops, selectedCategory, searchTerm]);

  const visibleCrops = useMemo(() => {
    return filteredCrops.slice(0, displayCount);
  }, [filteredCrops, displayCount]);

  return (
    <div className="space-y-4">
      {/* Quick Dropdown: All 102 Karnataka Crops */}
      <div className="space-y-1.5">
        <label className="text-xs font-extrabold uppercase tracking-wider text-ink-muted flex items-center justify-between">
          <span>{language === "kn" ? "ಕರ್ನಾಟಕದ ಎಲ್ಲಾ ಬೆಳೆಗಳು (102)" : language === "hi" ? "कर्नाटक की सभी फसलें (102)" : "All Karnataka Crops (102)"}</span>
          <span className="text-[11px] font-normal text-primary">Direct Dropdown</span>
        </label>
        <select
          value={selectedCrop}
          onChange={(e) => onSelectCrop(e.target.value)}
          className="w-full p-3 bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-2xl text-sm font-bold text-ink dark:text-ink-dark focus:outline-none focus:ring-2 focus:ring-primary/30 shadow-sm"
        >
          {crops.map((c) => {
            const cropName = c.name || c.name_en || c.crop_id;
            const cropKn = c.kannada_name || c.name_kn || cropName;
            const cropHi = c.hindi_name || c.name_hi || cropName;
            const label =
              language === "kn"
                ? `${cropKn} (${cropName})`
                : language === "hi"
                ? `${cropHi} (${cropName})`
                : cropName;
            return (
              <option key={cropName} value={cropName}>
                {label} — {c.category} ({c.unit})
              </option>
            );
          })}
        </select>
      </div>

      {/* Search Input */}
      <div className="relative">
        <span className="material-symbols-outlined absolute left-3.5 top-1/2 -translate-y-1/2 text-ink-muted text-[20px]">
          search
        </span>
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => {
            setSearchTerm(e.target.value);
            setDisplayCount(24);
          }}
          placeholder={t.searchCrop}
          className="w-full pl-10 pr-4 py-3 bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-2xl text-sm font-bold text-ink dark:text-ink-dark focus:outline-none focus:ring-2 focus:ring-primary/30"
        />
        {searchTerm && (
          <button
            type="button"
            onClick={() => setSearchTerm("")}
            className="absolute right-3.5 top-1/2 -translate-y-1/2 text-ink-muted hover:text-ink"
          >
            ✕
          </button>
        )}
      </div>

      {/* Category Pills */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none select-none">
        {categories.map((cat) => {
          const isActive = selectedCategory === cat.id;
          return (
            <button
              key={cat.id}
              type="button"
              onClick={() => {
                setSelectedCategory(cat.id);
                setDisplayCount(24);
              }}
              className={`px-3 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition-all ${
                isActive
                  ? "bg-primary text-white shadow-sm"
                  : "bg-surface-low dark:bg-surface-low-dark text-ink-muted hover:text-ink border border-divider/60"
              }`}
            >
              {cat.label}
            </button>
          );
        })}
      </div>

      {/* Crop Cards Grid */}
      {filteredCrops.length === 0 ? (
        <div className="text-center py-8 text-ink-muted text-sm font-medium">
          {t.noMarketData}
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5 max-h-[360px] overflow-y-auto pr-1">
          {visibleCrops.map((c) => {
            const cropName = c.name || c.name_en || c.crop_id;
            const cropKn = c.kannada_name || c.name_kn || cropName;
            const cropHi = c.hindi_name || c.name_hi || cropName;
            const reportingCount = c.reporting_mandis_count ?? c.reporting_markets_count ?? 0;

            const isSelected = selectedCrop.toLowerCase() === cropName.toLowerCase();
            const IconComp = getCropIconComponent(cropName, c.category);
            const localizedName =
              language === "kn"
                ? cropKn
                : language === "hi"
                ? cropHi
                : cropName;

            return (
              <button
                key={cropName}
                type="button"
                onClick={() => onSelectCrop(cropName)}
                className={`p-3 rounded-2xl border text-left flex flex-col justify-between gap-2 transition-all touch-press ${
                  isSelected
                    ? "bg-primary-tint/30 dark:bg-primary/20 border-2 border-primary ring-2 ring-primary/20 shadow-sm"
                    : "bg-white dark:bg-surface-dark border-divider dark:border-divider-dark hover:border-primary/40"
                }`}
              >
                <div className="flex items-start justify-between w-full">
                  <div className="w-10 h-10 rounded-xl bg-surface-low dark:bg-surface-low-dark flex items-center justify-center shrink-0">
                    <IconComp size={22} className={isSelected ? "text-primary" : "text-ink"} />
                  </div>
                  {reportingCount > 0 && (
                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-md bg-surface-low dark:bg-surface-low-dark text-ink-muted">
                      {reportingCount} mkt
                    </span>
                  )}
                </div>

                <div>
                  <div className="font-extrabold text-sm text-ink dark:text-ink-dark line-clamp-1">
                    {localizedName}
                  </div>
                  {language !== "en" && (
                    <div className="text-[11px] text-ink-muted dark:text-ink-muted-dark line-clamp-1">
                      {cropName}
                    </div>
                  )}
                </div>

                <div className="text-[10px] text-ink-muted flex items-center justify-between">
                  <span>{c.unit}</span>
                  {c.category && (
                    <span className="capitalize">{c.category}</span>
                  )}
                </div>
              </button>
            );
          })}
        </div>
      )}

      {/* Show more button if filtered count exceeds displayCount */}
      {filteredCrops.length > displayCount && (
        <button
          type="button"
          onClick={() => setDisplayCount((prev) => prev + 24)}
          className="w-full py-2 bg-surface-low hover:bg-surface-high border border-divider/60 rounded-xl text-xs font-bold text-ink transition-colors"
        >
          +{filteredCrops.length - displayCount} more crops
        </button>
      )}
    </div>
  );
};
