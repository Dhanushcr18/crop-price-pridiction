"use client";

import React, { useState, useMemo } from "react";
import { DistrictInfo, MandiDetailItem, Language } from "../types/api";
import { MandiIcon } from "./ui/Icons";
import { translations } from "../i18n/translations";

interface MandiPickerProps {
  districts: DistrictInfo[];
  mandis: MandiDetailItem[];
  selectedMandi: string;
  onSelectMandi: (mandiName: string, districtName?: string) => void;
  language: Language;
}

function haversineDistKm(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const R = 6371.0;
  const dLat = ((lat2 - lat1) * Math.PI) / 180.0;
  const dLon = ((lon2 - lon1) * Math.PI) / 180.0;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180.0) *
      Math.cos((lat2 * Math.PI) / 180.0) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return Math.round(R * c);
}

export const MandiPicker: React.FC<MandiPickerProps> = ({
  districts,
  mandis,
  selectedMandi,
  onSelectMandi,
  language,
}) => {
  const t = translations[language];
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedDistrict, setSelectedDistrict] = useState<string>("all");
  const [isLocating, setIsLocating] = useState<boolean>(false);
  const [geoNotice, setGeoNotice] = useState<string | null>(null);

  const handleUseMyLocation = () => {
    if (!navigator.geolocation) {
      setGeoNotice("Geolocation is not supported by your browser");
      return;
    }
    setIsLocating(true);
    setGeoNotice(null);

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setIsLocating(false);
        const { latitude, longitude } = pos.coords;
        let closestMandi: MandiDetailItem | null = null;
        let minDistance = Infinity;

        for (const m of mandis) {
          if (m.lat && m.lon) {
            const dist = haversineDistKm(latitude, longitude, m.lat, m.lon);
            if (dist < minDistance) {
              minDistance = dist;
              closestMandi = m;
            }
          }
        }

        if (closestMandi) {
          const mDist = closestMandi.district || closestMandi.district_en || "all";
          const mName = closestMandi.name || closestMandi.name_en || "";
          setSelectedDistrict(mDist);
          onSelectMandi(mName, mDist);
          setGeoNotice(`Nearest APMC: ${mName} (~${minDistance} km)`);
        }
      },
      (err) => {
        setIsLocating(false);
        setGeoNotice(`Location access denied or unavailable: ${err.message}`);
      },
      { timeout: 10000 }
    );
  };

  const filteredMandis = useMemo(() => {
    return mandis.filter((m) => {
      const mandiDistrict = m.district || m.district_en || "";
      const matchesDistrict =
        selectedDistrict === "all" ||
        mandiDistrict.toLowerCase() === selectedDistrict.toLowerCase();
      if (!matchesDistrict) return false;

      const mandiName = m.name || m.name_en || m.mandi_id || "";
      const mandiKn = m.kannada_name || m.name_kn || "";

      if (!searchTerm.trim()) return true;
      const q = searchTerm.toLowerCase();
      return (
        mandiName.toLowerCase().includes(q) ||
        mandiKn.toLowerCase().includes(q) ||
        mandiDistrict.toLowerCase().includes(q)
      );
    });
  }, [mandis, selectedDistrict, searchTerm]);

  return (
    <div className="space-y-4">
      {/* Quick Dropdown: All 115 Karnataka Mandis */}
      <div className="space-y-1.5">
        <label className="text-xs font-extrabold uppercase tracking-wider text-ink-muted flex items-center justify-between">
          <span>{language === "kn" ? "ಕರ್ನಾಟಕದ ಎಲ್ಲಾ ಮಾರುಕಟ್ಟೆಗಳು (115)" : language === "hi" ? "कर्नाटक की सभी 115 मंडियां" : "All Karnataka Markets (115 Mandis)"}</span>
          <span className="text-[11px] font-normal text-primary">Direct Dropdown</span>
        </label>
        <select
          value={selectedMandi}
          onChange={(e) => {
            const chosen = mandis.find(
              (m) =>
                (m.name || m.name_en || m.mandi_id) === e.target.value ||
                m.id === e.target.value
            );
            onSelectMandi(e.target.value, chosen?.district || chosen?.district_en);
          }}
          className="w-full p-3 bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-2xl text-sm font-bold text-ink dark:text-ink-dark focus:outline-none focus:ring-2 focus:ring-primary/30 shadow-sm"
        >
          {mandis.map((m) => {
            const mName = m.name || m.name_en || m.mandi_id || "";
            const mDist = m.district || m.district_en || "";
            const mKn = m.kannada_name || m.name_kn || mName;
            const label = language === "kn" ? `${mKn} (${mName})` : mName;
            const statusTag =
              m.is_quarantined || m.all_quarantined
                ? "Data under review"
                : m.tier || "APMC";
            return (
              <option key={m.id || m.mandi_id || mName} value={mName}>
                {label} — {mDist} ({statusTag})
              </option>
            );
          })}
        </select>
      </div>

      {/* Search and Geolocation Row */}
      <div className="flex flex-col sm:flex-row gap-2.5">
        <div className="relative flex-1">
          <span className="material-symbols-outlined absolute left-3.5 top-1/2 -translate-y-1/2 text-ink-muted text-[20px]">
            search
          </span>
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder={t.searchMandi}
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

        <button
          type="button"
          onClick={handleUseMyLocation}
          disabled={isLocating}
          className="px-4 py-3 bg-primary-tint/50 dark:bg-primary/20 hover:bg-primary-tint border border-primary/30 text-primary dark:text-primary-dark rounded-2xl text-xs sm:text-sm font-extrabold flex items-center justify-center gap-2 transition-colors shrink-0 touch-press"
        >
          <span className="material-symbols-outlined text-[18px]">
            {isLocating ? "autorenew" : "my_location"}
          </span>
          <span>{isLocating ? "Locating..." : t.useMyLocation}</span>
        </button>
      </div>

      {geoNotice && (
        <div className="text-xs font-bold px-3 py-2 rounded-xl bg-primary-tint/30 text-primary border border-primary/20">
          {geoNotice}
        </div>
      )}

      {/* Two-Level Hierarchy: District Selector */}
      <div className="space-y-1.5">
        <label className="text-xs font-extrabold uppercase tracking-wider text-ink-muted">
          {t.selectDistrict}
        </label>
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none select-none">
          <button
            type="button"
            onClick={() => setSelectedDistrict("all")}
            className={`px-3 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition-all ${
              selectedDistrict === "all"
                ? "bg-primary text-white shadow-sm"
                : "bg-surface-low dark:bg-surface-low-dark text-ink-muted hover:text-ink border border-divider/60"
            }`}
          >
            {t.allCategories} ({mandis.length})
          </button>
          {districts.map((d) => {
            const distName = d.name || d.name_en || "";
            const isSelected = selectedDistrict.toLowerCase() === distName.toLowerCase();
            const count = d.mandi_count ?? d.reporting_mandis_count ?? 0;
            const hasNoData = count === 0;
            return (
              <button
                key={distName}
                type="button"
                onClick={() => setSelectedDistrict(distName)}
                className={`px-3 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition-all flex items-center gap-1.5 ${
                  isSelected
                    ? "bg-primary text-white shadow-sm"
                    : hasNoData
                    ? "bg-surface-low/50 text-ink-muted/50 border border-divider/30 cursor-not-allowed"
                    : "bg-surface-low dark:bg-surface-low-dark text-ink-muted hover:text-ink border border-divider/60"
                }`}
              >
                <span>{language === "kn" ? d.kannada_name || d.name_kn || distName : distName}</span>
                <span className="text-[10px] opacity-75">
                  {hasNoData ? t.noMarketData : count}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Mandi Cards List */}
      {filteredMandis.length === 0 ? (
        <div className="text-center py-8 text-ink-muted text-sm font-medium">
          {t.noMarketData}
        </div>
      ) : (
        <div className="space-y-2 max-h-[320px] overflow-y-auto pr-1">
          {filteredMandis.map((m) => {
            const mName = m.name || m.name_en || m.mandi_id || "";
            const mDistrict = m.district || m.district_en || "";
            const isSelected =
              selectedMandi.toLowerCase() === mName.toLowerCase() ||
              (m.id && selectedMandi.toLowerCase() === m.id.toLowerCase()) ||
              (m.mandi_id && selectedMandi.toLowerCase() === m.mandi_id.toLowerCase());
            const localizedName =
              language === "kn" ? m.kannada_name || m.name_kn || mName : mName;

            const isQuarantined = m.is_quarantined || m.all_quarantined || false;

            // Tier & Quarantine Badges
            let badgeClass = "bg-surface-low text-ink-muted border-divider/60";
            let badgeText = m.tier === "Tier B" ? t.tierBBadge : t.tierCBadge;

            if (isQuarantined) {
              badgeClass = "bg-amber-100 text-amber-900 border-amber-300 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800";
              badgeText = t.dataUnderReview;
            } else if (m.tier === "Tier B") {
              badgeClass = "bg-emerald-100 text-emerald-800 border-emerald-300 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800";
              badgeText = t.tierBBadge;
            }

            return (
              <button
                key={m.id || m.mandi_id || mName}
                type="button"
                onClick={() => onSelectMandi(mName, mDistrict)}
                className={`w-full p-3.5 rounded-2xl border text-left flex items-center justify-between gap-3 transition-all touch-press ${
                  isSelected
                    ? "bg-primary-tint/30 dark:bg-primary/20 border-2 border-primary ring-2 ring-primary/20 shadow-sm"
                    : "bg-white dark:bg-surface-dark border-divider dark:border-divider-dark hover:border-primary/40"
                }`}
              >
                <div className="flex items-center gap-3 min-w-0">
                  <div className="w-10 h-10 rounded-xl bg-surface-low dark:bg-surface-low-dark flex items-center justify-center shrink-0">
                    <MandiIcon size={22} className={isSelected ? "text-primary" : "text-ink"} />
                  </div>
                  <div className="min-w-0">
                    <div className="font-extrabold text-sm sm:text-base text-ink dark:text-ink-dark truncate">
                      {localizedName}
                    </div>
                    <div className="text-xs text-ink-muted dark:text-ink-muted-dark flex items-center gap-2">
                      <span>{mDistrict}</span>
                      {m.coord_source === "unresolved" && (
                        <span className="text-[10px] text-amber-700 bg-amber-50 px-1 rounded">
                          {t.locationUnknown}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                <div className="shrink-0 text-right">
                  <span
                    className={`inline-block px-2.5 py-1 rounded-full text-[11px] font-bold border ${badgeClass}`}
                  >
                    {badgeText}
                  </span>
                </div>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};
