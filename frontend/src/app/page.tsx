"use client";

import React, { useState, useEffect } from "react";
import { Header } from "../components/Header";
import { BottomNav } from "../components/BottomNav";
import { Button } from "../components/ui/Button";
import { SelectCard } from "../components/ui/SelectCard";
import { QuantityStepper } from "../components/ui/QuantityStepper";
import { ProgressDots } from "../components/ui/ProgressDots";
import { ConfidenceBadge } from "../components/ui/ConfidenceBadge";
import { SourceBadge } from "../components/ui/SourceBadge";
import { MandiCard } from "../components/ui/MandiCard";
import { LocalMandiStrip } from "../components/ui/LocalMandiStrip";
import { ChartCard } from "../components/ui/ChartCard";
import { BottomSheet } from "../components/ui/BottomSheet";
import { Toast } from "../components/ui/Toast";
import { Skeleton } from "../components/ui/Skeleton";
import { ReadAloudButton } from "../components/ui/ReadAloudButton";
import { ShareButton } from "../components/ui/ShareButton";
import { CropAreaView } from "../components/CropAreaView";
import { CropPicker } from "../components/CropPicker";
import { MandiPicker } from "../components/MandiPicker";
import { ReportedPriceCard } from "../components/ReportedPriceCard";
import { KarnatakaMap } from "../components/KarnatakaMap";
import {
  OnionIcon,
  FarmerIcon,
  CropIcon,
} from "../components/ui/Icons";
import {
  Language,
  HealthResponse,
  ForecastResponse,
  WhereToSellResponse,
  WhenToSellResponse,
  AdviceResponse,
  HistoryRecord,
  TextSize,
  CropInfo,
  DistrictInfo,
  MandiDetailItem,
  TodayPriceResponse,
  WhereToSellSpatialResponse,
  CoverageSummaryResponse,
} from "../types/api";
import { translations } from "../i18n/translations";
import {
  getHealth,
  getForecast,
  getWhereToSell,
  getWhenToSell,
  getAdvice,
  getCrops,
  getDistricts,
  getMandisFiltered,
  getTodayPrice,
  postWhereToSellSpatial,
  getCoverageSummary,
} from "../lib/api";
import { formatCurrency, formatPercent } from "../lib/formatter";

export default function HomePage() {
  const [language, setLanguage] = useState<Language>("kn");
  const t = translations[language];

  // App & System state
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [hasStarted, setHasStarted] = useState<boolean>(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState<boolean>(false);
  const [textSize, setTextSize] = useState<TextSize>("normal");
  const [darkMode, setDarkMode] = useState<boolean>(false);
  const [toastMessage, setToastMessage] = useState<string>("");
  const [toastVisible, setToastVisible] = useState<boolean>(false);

  // Stepper state: 1 to 6 (1: Crop, 2: Loc, 3: Qty, 4: Storage, 5: Debt, 6: Review)
  const [currentStep, setCurrentStep] = useState<number>(1);
  const totalSteps = 6;
  const [activeMode, setActiveMode] = useState<"advisor" | "crop_area">("advisor");

  // Dynamic Master Data
  const [crops, setCrops] = useState<CropInfo[]>([]);
  const [districts, setDistricts] = useState<DistrictInfo[]>([]);
  const [mandis, setMandis] = useState<MandiDetailItem[]>([]);
  const [previewPrice, setPreviewPrice] = useState<TodayPriceResponse | null>(null);
  const [spatialWhereData, setSpatialWhereData] = useState<WhereToSellSpatialResponse | null>(null);
  const [coverageSummary, setCoverageSummary] = useState<CoverageSummaryResponse | null>(null);

  // Form Inputs (dynamic default from data)
  const [crop, setCrop] = useState<string>("");
  const [farmerLocation, setFarmerLocation] = useState<string>("");
  const [quantity, setQuantity] = useState<number>(30);
  const [storageType, setStorageType] = useState<string>("warehouse");
  const [hasTraderDebt, setHasTraderDebt] = useState<boolean>(false);
  const [debtChoice, setDebtChoice] = useState<"no" | "yes" | "private">("no");

  // Results & Loading
  const [loading, setLoading] = useState<boolean>(false);
  const [hasResults, setHasResults] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const [adviceData, setAdviceData] = useState<AdviceResponse | null>(null);
  const [forecastData, setForecastData] = useState<ForecastResponse | null>(null);
  const [whereData, setWhereData] = useState<WhereToSellResponse | null>(null);
  const [whenData, setWhenData] = useState<WhenToSellResponse | null>(null);

  // Simulation Toggle: What if borrow against stored produce?
  const [borrowToggle, setBorrowToggle] = useState<boolean>(false);

  // Feedback state
  const [feedbackGiven, setFeedbackGiven] = useState<boolean>(false);

  // Voice Search Listening State
  const [isListeningMic, setIsListeningMic] = useState<boolean>(false);

  // Initialize preferences and master data on mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedLang = localStorage.getItem("fsa_lang") as Language;
      if (savedLang && ["en", "hi", "kn"].includes(savedLang)) {
        setLanguage(savedLang);
      }

      const welcomed = localStorage.getItem("fsa_welcomed");
      if (welcomed === "true") {
        setHasStarted(true);
      }

      const savedTextSize = localStorage.getItem("fsa_text_size") as TextSize;
      if (savedTextSize) {
        setTextSize(savedTextSize);
        applyTextSize(savedTextSize);
      }

      const savedDark = localStorage.getItem("fsa_dark_mode") === "true";
      setDarkMode(savedDark);
      if (savedDark) {
        document.documentElement.classList.add("dark");
      }
    }

    getHealth()
      .then((h) => setHealth(h))
      .catch((err) => console.warn("Health check error:", err));

    // Load master crops, districts, and mandis dynamically
    Promise.all([
      getCrops(),
      getDistricts(),
      getMandisFiltered(),
      getCoverageSummary()
    ]).then(([cropsRes, distsRes, mandisRes, covRes]) => {
      setCrops(cropsRes);
      setDistricts(distsRes);
      setMandis(mandisRes);
      setCoverageSummary(covRes);

      // Default crop: first crop in list, preferably one with active reports
      if (cropsRes.length > 0) {
        const defaultCrop = cropsRes.find((c) => (c.reporting_mandis_count || c.reporting_markets_count || 0) > 0) || cropsRes[0];
        setCrop(defaultCrop.name || defaultCrop.name_en || defaultCrop.crop_id);
      }
      // Default mandi: first reporting mandi in list
      if (mandisRes.length > 0) {
        const defaultMandi = mandisRes.find((m) => m.tier === "Tier B" && !m.all_quarantined && !m.is_quarantined) || mandisRes[0];
        setFarmerLocation(defaultMandi.name || defaultMandi.name_en || defaultMandi.mandi_id || "");
      }
    }).catch((err) => {
      console.warn("Failed to load master data:", err);
    });
  }, []);

  // Update preview price whenever crop or location changes
  useEffect(() => {
    if (crop && farmerLocation) {
      getTodayPrice(crop, farmerLocation)
        .then((p) => setPreviewPrice(p))
        .catch((err) => console.warn("Preview price error:", err));
    }
  }, [crop, farmerLocation]);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setToastVisible(true);
    setTimeout(() => setToastVisible(false), 3000);
  };

  const handleLanguageChange = (newLang: Language) => {
    setLanguage(newLang);
    if (typeof window !== "undefined") {
      localStorage.setItem("fsa_lang", newLang);
    }
    // If advice already calculated, refresh plain language advice
    if (hasResults) {
      getAdvice(farmerLocation, quantity, storageType, hasTraderDebt, newLang)
        .then((res) => setAdviceData(res))
        .catch((e) => console.warn(e));
    }
  };

  const applyTextSize = (size: TextSize) => {
    if (typeof document === "undefined") return;
    const root = document.documentElement;
    if (size === "large") {
      root.style.setProperty("--font-base-size", "20px");
    } else if (size === "xlarge") {
      root.style.setProperty("--font-base-size", "22px");
    } else {
      root.style.setProperty("--font-base-size", "18px");
    }
  };

  const handleTextSizeChange = (size: TextSize) => {
    setTextSize(size);
    applyTextSize(size);
    if (typeof window !== "undefined") {
      localStorage.setItem("fsa_text_size", size);
    }
  };

  const handleDarkModeToggle = () => {
    const nextDark = !darkMode;
    setDarkMode(nextDark);
    if (typeof document !== "undefined") {
      if (nextDark) {
        document.documentElement.classList.add("dark");
      } else {
        document.documentElement.classList.remove("dark");
      }
    }
    if (typeof window !== "undefined") {
      localStorage.setItem("fsa_dark_mode", String(nextDark));
    }
  };

  const handleStartWelcome = (chosenLang?: Language) => {
    if (chosenLang) {
      handleLanguageChange(chosenLang);
    }
    setHasStarted(true);
    if (typeof window !== "undefined") {
      localStorage.setItem("fsa_welcomed", "true");
    }
  };

  const handleNewFarmerSession = () => {
    setQuantity(30);
    if (crops.length > 0) {
      const defaultCrop =
        crops.find((c) => (c.reporting_mandis_count || c.reporting_markets_count || 0) > 0) ||
        crops[0];
      setCrop(defaultCrop.name || defaultCrop.name_en || defaultCrop.crop_id);
    }
    if (mandis.length > 0) {
      const defaultMandi =
        mandis.find((m) => m.tier === "Tier B" && !m.all_quarantined && !m.is_quarantined) ||
        mandis[0];
      setFarmerLocation(defaultMandi.name || defaultMandi.name_en || defaultMandi.mandi_id || "");
    }
    setStorageType("warehouse");
    setHasTraderDebt(false);
    setDebtChoice("no");
    setCurrentStep(1);
    setHasResults(false);
    setAdviceData(null);
    setWhereData(null);
    setWhenData(null);
    setForecastData(null);
    setSpatialWhereData(null);
    setIsSettingsOpen(false);
    showToast(t.startNewFarmerBtn);
  };

  const fetchAdvice = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const debtParam = debtChoice === "yes";

      const [todayPriceRes, spatialRes, adviceRes, forecastRes, whereRes, whenRes] = await Promise.all([
        getTodayPrice(crop, farmerLocation).catch(() => null),
        postWhereToSellSpatial({
          crop: crop,
          farmerLocation: farmerLocation,
          quantityQuintals: quantity,
          radiusKm: 150
        }).catch(() => null),
        getAdvice(farmerLocation, quantity, storageType, debtParam, language).catch(() => null),
        getForecast(farmerLocation, crop).catch(() => null),
        getWhereToSell(farmerLocation, quantity, 7).catch(() => null),
        getWhenToSell(farmerLocation, quantity, storageType, debtParam).catch(() => null),
      ]);

      if (todayPriceRes) {
        setPreviewPrice(todayPriceRes);
      }
      if (spatialRes) {
        setSpatialWhereData(spatialRes);
      }
      setAdviceData(adviceRes);
      setForecastData(forecastRes);
      setWhereData(whereRes);
      setWhenData(whenRes);
      setHasResults(true);

      // Auto-save to farmer history
      if (typeof window !== "undefined") {
        try {
          const historyList: HistoryRecord[] = JSON.parse(
            localStorage.getItem("fsa_history") || "[]"
          );
          const newRecord: HistoryRecord = {
            id: `rec_${Date.now()}`,
            timestamp: new Date().toISOString(),
            crop: crop || "Crop",
            mandi: farmerLocation,
            quantity: quantity,
            storage: storageType,
            hasTraderDebt: debtParam,
            recommendation: adviceRes?.summary_sentence || `Reported price: ₹${todayPriceRes?.headline_price?.modal_price || 0}`,
            recommendedMandi: farmerLocation,
            priceRange: todayPriceRes?.headline_price ? `₹${todayPriceRes.headline_price.min_price} - ₹${todayPriceRes.headline_price.max_price}` : "Spot Only",
          };
          historyList.unshift(newRecord);
          localStorage.setItem("fsa_history", JSON.stringify(historyList.slice(0, 20)));
        } catch {
          // ignore storage error
        }
      }

      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err: any) {
      console.error("Advice query failed:", err);
      setErrorMsg(
        err.message || "Network error. Please make sure the service is online."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceSearch = () => {
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Voice search is not supported in this browser.");
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.lang =
        language === "kn" ? "kn-IN" : language === "hi" ? "hi-IN" : "en-IN";
      recognition.onstart = () => setIsListeningMic(true);
      recognition.onresult = (event: any) => {
        const text = (event.results[0][0].transcript || "").toLowerCase();
        // Dynamically find matching mandi from loaded master data
        const matchedMandi = mandis.find((m) => {
          const mName = m.name || m.name_en || "";
          const mKn = m.kannada_name || m.name_kn || "";
          const mDist = m.district || m.district_en || "";
          return (
            (mName && text.includes(mName.toLowerCase())) ||
            (mKn && text.includes(mKn.toLowerCase())) ||
            (mDist && text.includes(mDist.toLowerCase()))
          );
        });
        if (matchedMandi) {
          setFarmerLocation(matchedMandi.name || matchedMandi.name_en || "");
        }
        setIsListeningMic(false);
      };
      recognition.onerror = () => setIsListeningMic(false);
      recognition.onend = () => setIsListeningMic(false);
      recognition.start();
    } catch {
      setIsListeningMic(false);
    }
  };

  const handleShareWhatsApp = () => {
    if (!adviceData || !whereData) return;
    const bestMandi = whereData.ranked_mandis[0];
    const text = encodeURIComponent(
      `🌾 *${t.appName}*\n\n` +
      `📢 *${t.resultsTitle}:*\n"${adviceData.summary_sentence}"\n\n` +
      `📍 *${t.whereToSellTitle}:* ${bestMandi ? bestMandi.mandi : farmerLocation}\n` +
      `💰 *${t.priceYouMayGet}:* ${adviceData.p10_p90_range}\n\n` +
      `⚠️ _${t.disclaimer}_`
    );
    window.open(`https://api.whatsapp.com/send?text=${text}`, "_blank");
  };

  const handleDownloadSummary = () => {
    if (!adviceData || !whereData || !whenData) return;
    const summary =
      `=======================================================\n` +
      `${t.appName.toUpperCase()} - SUMMARY REPORT\n` +
      `=======================================================\n` +
      `Crop: ${crop || "Crop"}\n` +
      `Location: ${farmerLocation}\n` +
      `Quantity: ${quantity} Quintals (${quantity * 2} Bags)\n` +
      `Storage: ${storageType}\n` +
      `Trader Debt: ${hasTraderDebt ? "Yes" : "No"}\n` +
      `Date: ${new Date().toLocaleDateString()}\n\n` +
      `1. RECOMMENDATION:\n"${adviceData.summary_sentence}"\n\n` +
      `2. DETAILS:\n${adviceData.full_advice_text}\n\n` +
      `3. WHERE TO SELL:\n` +
      whereData.ranked_mandis
        .map(
          (m, idx) =>
            `   #${idx + 1} ${m.mandi} (${m.distance_km} km): Net ₹${m.net_price_p10_downside} - ₹${m.net_price_p50}/qtl (Gain: +₹${m.gain_over_local_per_qtl}/qtl)`
        )
        .join("\n") +
      `\n\n4. WHEN TO SELL:\n` +
      `   Optimal Timing: ${whenData.best_k_days === 0 ? t.sellTodayOption : `${t.waitDaysOption.replace("{days}", String(whenData.best_k_days))}`}\n` +
      `   Extra Gain: ₹${Math.round(whenData.max_expected_gain_per_qtl)}/qtl\n\n` +
      `DISCLAIMER:\n` +
      `${t.disclaimer} All prices reflect statistical ranges.\n` +
      `=======================================================\n`;

    const blob = new Blob([summary], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `Farmer_Advice_${farmerLocation}_${quantity}qtl.txt`;
    link.click();
    URL.revokeObjectURL(url);
    showToast(t.downloadSummaryBtn);
  };

  return (
    <div className="min-h-screen flex flex-col bg-cream dark:bg-cream-dark text-ink dark:text-ink-dark">
      {/* Top Bar with Logo, Language Switcher, Online Dot */}
      <Header
        language={language}
        onLanguageChange={handleLanguageChange}
        onOpenSettings={() => setIsSettingsOpen(true)}
        health={health}
      />

      <main
        className={`flex-1 w-full mx-auto flex flex-col min-w-0 ${
          activeMode === "crop_area"
            ? "max-w-[1440px] px-2 sm:px-4 lg:px-6 py-2"
            : "max-w-7xl px-4 sm:px-6 lg:px-8 py-4 sm:py-6"
        }`}
      >
        {/* ================= 1. WELCOME SCREEN (Kiosk Language Selection) ================= */}
        {!hasStarted && (
          <div className="flex-1 flex flex-col justify-center items-center text-center py-6 sm:py-12 space-y-8 animate-in fade-in duration-fast max-w-4xl mx-auto w-full">
            {/* Kiosk Station Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary-tint dark:bg-primary/20 text-primary dark:text-primary-dark font-bold text-xs sm:text-sm border border-primary/20">
              <span className="material-symbols-outlined text-[18px]">agriculture</span>
              <span>{t.stationDepartment}</span>
            </div>

            <div className="w-24 h-24 rounded-3xl bg-primary text-white flex items-center justify-center shadow-touch">
              <OnionIcon size={48} />
            </div>

            <div className="space-y-2 max-w-2xl">
              <h1 className="text-3xl sm:text-4xl font-black text-ink dark:text-ink-dark leading-tight tracking-tight">
                {t.welcomeTitle}
              </h1>
              <p className="text-base sm:text-lg text-ink-muted dark:text-ink-muted-dark leading-relaxed">
                {t.welcomeSubtitle}
              </p>
            </div>

            {/* Language Selector: 3 Large Cards shown only in their native script */}
            <div className="w-full max-w-xl space-y-3 pt-2 text-left">
              <span className="text-xs font-bold uppercase tracking-wider text-ink-muted dark:text-ink-muted-dark block text-center">
                {t.chooseLanguage}
              </span>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {[
                  { code: "kn" as Language, label: "ಕನ್ನಡ", sub: "ಕರ್ನಾಟಕದ ರೈತರಿಗೆ" },
                  { code: "hi" as Language, label: "हिन्दी", sub: "सटीक मंडी भाव" },
                  { code: "en" as Language, label: "English", sub: "Decision Intelligence" },
                ].map((langChoice) => {
                  const isSelected = language === langChoice.code;
                  return (
                    <button
                      key={langChoice.code}
                      data-lang={langChoice.code}
                      type="button"
                      onClick={() => handleStartWelcome(langChoice.code)}
                      className={`w-full min-h-[96px] p-4 rounded-2xl border flex flex-col justify-between transition-all duration-fast select-none touch-press text-left ${
                        isSelected
                          ? "bg-white dark:bg-surface-dark border-2 border-primary shadow-touch ring-2 ring-primary/20"
                          : "bg-white dark:bg-surface-dark border-divider dark:border-divider-dark hover:border-ink-subtle"
                      }`}
                    >
                      <div className="flex items-center justify-between w-full">
                        <span className="font-extrabold text-xl text-ink dark:text-ink-dark">
                          {langChoice.label}
                        </span>
                        <span className="w-7 h-7 rounded-full bg-surface-low dark:bg-surface-low-dark flex items-center justify-center text-primary text-sm font-bold">
                          🔊
                        </span>
                      </div>
                      <span className="text-xs text-ink-muted dark:text-ink-muted-dark font-medium mt-2">
                        {langChoice.sub}
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="w-full max-w-sm pt-2">
              <Button
                variant="primary"
                size="touch"
                onClick={() => handleStartWelcome()}
              >
                <span>{t.startBtn}</span>
                <span className="material-symbols-outlined ml-2 text-[20px]">
                  arrow_forward
                </span>
              </Button>
            </div>

            <p className="text-xs sm:text-sm text-primary dark:text-primary-dark font-bold">
              ✓ {t.welcomePromise}
            </p>
          </div>
        )}

        {/* Feature Mode Switcher: Sell Advisor vs Crop Area & Supply Outlook */}
        {hasStarted && (
          <div className="flex items-center gap-2 p-1.5 bg-surface-low dark:bg-surface-low-dark rounded-2xl border border-divider/60 mb-6 select-none max-w-md mx-auto sm:mx-0">
            <button
              type="button"
              data-testid="switch-to-advisor-btn"
              onClick={() => setActiveMode("advisor")}
              className={`flex-1 min-h-[44px] py-2 rounded-xl text-xs sm:text-sm font-extrabold flex items-center justify-center gap-1.5 transition-all touch-press ${
                activeMode === "advisor"
                  ? "bg-white dark:bg-surface-dark text-ink dark:text-ink-dark shadow-sm border border-divider/60"
                  : "text-ink-muted hover:text-ink"
              }`}
            >
              <span>🧅</span>
              <OnionIcon size={18} />
              <span>{t.tabAdvice}</span>
            </button>
            <button
              type="button"
              data-testid="switch-to-crop-area-btn"
              onClick={() => setActiveMode("crop_area")}
              className={`flex-1 min-h-[44px] py-2 rounded-xl text-xs sm:text-sm font-extrabold flex items-center justify-center gap-1.5 transition-all touch-press ${
                activeMode === "crop_area"
                  ? "bg-white dark:bg-surface-dark text-primary dark:text-primary-dark shadow-sm border border-primary/40"
                  : "text-ink-muted hover:text-ink"
              }`}
            >
              <span>🌾</span>
              <CropIcon size={18} />
              <span>{t.tabCropArea}</span>
            </button>
          </div>
        )}

        {/* RENDER CROP AREA & SUPPLY OUTLOOK WHEN ACTIVE */}
        {hasStarted && activeMode === "crop_area" && (
          <CropAreaView
            language={language}
            onBackToAdvisor={() => setActiveMode("advisor")}
          />
        )}

        {/* ================= 2. ADVICE INTAKE (Stitch 12-Column Desktop Grid) ================= */}
        {hasStarted && activeMode === "advisor" && !hasResults && !loading && (
          <div className="flex flex-col gap-6 animate-in fade-in duration-fast">
            {/* Top Consultation & Kiosk Node Bar */}
            <div className="w-full bg-white dark:bg-surface-dark rounded-2xl p-4 sm:p-5 border border-divider dark:border-divider-dark shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div className="flex items-center gap-3.5">
                <div className="w-12 h-12 rounded-2xl bg-primary text-white flex items-center justify-center shrink-0 shadow-sm">
                  <FarmerIcon size={26} className="text-white" />
                </div>
                <div>
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="px-2.5 py-0.5 rounded-full bg-primary-tint dark:bg-primary/20 text-primary dark:text-primary-dark font-extrabold text-xs tracking-wider uppercase">
                      {t.jointAssistedMode}
                    </span>
                    <span className="text-xs text-ink-muted dark:text-ink-muted-dark">
                      • {t.jointAssistedSub}
                    </span>
                  </div>
                  <h2 className="text-lg sm:text-xl font-black text-ink dark:text-ink-dark mt-0.5">
                    {t.stepLocationDesc}
                  </h2>
                </div>
              </div>

              <div className="flex items-center gap-3 w-full md:w-auto justify-between md:justify-end flex-wrap">
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-surface-low dark:bg-surface-low-dark border border-divider/60 text-xs font-bold text-ink-muted">
                  <span className="w-2.5 h-2.5 rounded-full bg-primary animate-pulse" />
                  <span>
                    {previewPrice?.headline_price
                      ? `${farmerLocation} (${previewPrice.headline_price.variety}): ₹${previewPrice.headline_price.modal_price} / ${previewPrice.headline_price.unit}`
                      : `${farmerLocation || "Mandi"}: ${previewPrice?.status || "Live APMC"}`}
                  </span>
                </div>
                <button
                  type="button"
                  onClick={handleNewFarmerSession}
                  className="px-3.5 py-1.5 rounded-xl bg-surface-low dark:bg-surface-low-dark hover:bg-surface-high border border-divider/60 text-xs font-bold text-ink flex items-center gap-1.5 transition-colors"
                >
                  <span className="material-symbols-outlined text-[16px]">restart_alt</span>
                  <span>{t.startNewFarmerBtn}</span>
                </button>
              </div>
            </div>

            {/* Main 12-Column Grid: 5 Cols Form | 7 Cols Spatial Live Mandi Map */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
              {/* LEFT COLUMN: 5 COLS (Stepper Form Card) */}
              <div className="lg:col-span-5 bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-5 sm:p-6 shadow-card flex flex-col justify-between gap-6">
                {/* Stepper Progress Indicator */}
                <ProgressDots
                  currentStep={currentStep}
                  totalSteps={totalSteps}
                  stepLabel={
                    currentStep <= 5
                      ? t.stepCounter
                          .replace("{current}", String(currentStep))
                          .replace("{total}", "5")
                      : t.stepReviewTitle
                  }
                />

                {/* Error Notification */}
                {errorMsg && (
                  <div className="p-4 rounded-2xl bg-risk-light dark:bg-risk/20 border border-risk text-risk dark:text-risk-dark text-sm font-bold flex items-center gap-2">
                    <span className="material-symbols-outlined text-[20px]">error</span>
                    <span>{errorMsg}</span>
                  </div>
                )}

                {/* STEP 1: CROP SELECTION */}
                {currentStep === 1 && (
                  <section className="space-y-4 flex-1">
                    <div className="space-y-1">
                      <h3 className="text-xl sm:text-2xl font-black text-ink dark:text-ink-dark">
                        {t.stepCropTitle}
                      </h3>
                      <p className="text-sm text-ink-muted dark:text-ink-muted-dark">
                        {t.stepCropDesc}
                      </p>
                    </div>

                    <CropPicker
                      crops={crops}
                      selectedCrop={crop}
                      onSelectCrop={(c) => setCrop(c)}
                      language={language}
                    />
                  </section>
                )}

                {/* STEP 2: LOCATION INTAKE */}
                {currentStep === 2 && (
                  <section className="space-y-4 flex-1">
                    <div className="space-y-1">
                      <h3 className="text-xl sm:text-2xl font-black text-ink dark:text-ink-dark">
                        {t.stepLocationTitle}
                      </h3>
                      <p className="text-sm text-ink-muted dark:text-ink-muted-dark">
                        {t.stepLocationDesc}
                      </p>
                    </div>

                    <MandiPicker
                      districts={districts}
                      mandis={mandis}
                      selectedMandi={farmerLocation}
                      onSelectMandi={(m) => setFarmerLocation(m)}
                      language={language}
                    />

                    <div className="pt-2">
                      <Button
                        variant="voice"
                        size="touch"
                        isListening={isListeningMic}
                        onClick={handleVoiceSearch}
                        type="button"
                      >
                        <span className="material-symbols-outlined text-[24px] mr-2">
                          mic
                        </span>
                        <span>{isListeningMic ? t.listening : t.speakVillage}</span>
                      </Button>
                    </div>
                  </section>
                )}

                {/* STEP 3: QUANTITY INTAKE */}
                {currentStep === 3 && (
                  <section className="space-y-4 flex-1">
                    <div className="space-y-1">
                      <h3 className="text-xl sm:text-2xl font-black text-ink dark:text-ink-dark">
                        {t.stepQuantityTitle}
                      </h3>
                      <p className="text-sm text-ink-muted dark:text-ink-muted-dark">
                        {t.stepQuantityDesc}
                      </p>
                    </div>

                    <QuantityStepper
                      value={quantity}
                      onChange={(val) => setQuantity(val)}
                      unitLabel={t.quintalsUnit}
                      bagEstimateLabel={t.bagConversion}
                      min={1}
                      max={500}
                      step={5}
                    />
                  </section>
                )}

                {/* STEP 4: STORAGE CONDITIONS */}
                {currentStep === 4 && (
                  <section className="space-y-4 flex-1">
                    <div className="space-y-1">
                      <h3 className="text-xl sm:text-2xl font-black text-ink dark:text-ink-dark">
                        {t.stepStorageTitle}
                      </h3>
                      <p className="text-sm text-ink-muted dark:text-ink-muted-dark">
                        {t.stepStorageDesc}
                      </p>
                    </div>

                    <div className="space-y-3 pt-1">
                      <SelectCard
                        selected={storageType === "open"}
                        title={t.storageNoneTitle}
                        description={t.storageNoneDesc}
                        badge={t.rotRiskHigh}
                        badgeColor="risk"
                        icon="🌱"
                        onClick={() => setStorageType("open")}
                      />
                      <SelectCard
                        selected={storageType === "warehouse"}
                        title={t.storageWarehouseTitle}
                        description={t.storageWarehouseDesc}
                        badge={t.rotRiskMedium}
                        badgeColor="caution"
                        icon="🏠"
                        onClick={() => setStorageType("warehouse")}
                      />
                      <SelectCard
                        selected={storageType === "cold_storage"}
                        title={t.storageColdTitle}
                        description={t.storageColdDesc}
                        badge={t.rotRiskLow}
                        badgeColor="primary"
                        icon="❄️"
                        onClick={() => setStorageType("cold_storage")}
                      />
                    </div>
                  </section>
                )}

                {/* STEP 5: TRADER ADVANCE / DEBT */}
                {currentStep === 5 && (
                  <section className="space-y-4 flex-1">
                    <div className="space-y-1">
                      <h3 className="text-xl sm:text-2xl font-black text-ink dark:text-ink-dark">
                        {t.stepDebtTitle}
                      </h3>
                      <p className="text-sm text-ink-muted dark:text-ink-muted-dark">
                        {t.stepDebtDesc}
                      </p>
                    </div>

                    <div className="space-y-3 pt-1">
                      <SelectCard
                        selected={debtChoice === "no"}
                        title={t.debtNo}
                        description={t.debtNoDesc}
                        badgeColor="primary"
                        icon="✅"
                        onClick={() => {
                          setDebtChoice("no");
                          setHasTraderDebt(false);
                        }}
                      />
                      <SelectCard
                        selected={debtChoice === "yes"}
                        title={t.debtYes}
                        description={t.debtYesDesc}
                        badgeColor="caution"
                        icon="💳"
                        onClick={() => {
                          setDebtChoice("yes");
                          setHasTraderDebt(true);
                        }}
                      />
                      <SelectCard
                        selected={debtChoice === "private"}
                        title={t.debtPrivate}
                        description={t.debtPrivateDesc}
                        badgeColor="neutral"
                        icon="🔒"
                        onClick={() => {
                          setDebtChoice("private");
                          setHasTraderDebt(false);
                        }}
                      />
                    </div>

                    <div className="p-4 rounded-2xl bg-surface-low dark:bg-surface-low-dark border border-divider dark:border-divider-dark text-xs sm:text-sm text-ink-muted dark:text-ink-muted-dark space-y-1">
                      <span className="font-bold text-ink dark:text-ink-dark block">
                        💡 {t.whyWeAskTitle}
                      </span>
                      <p className="leading-relaxed">{t.whyWeAskDesc}</p>
                    </div>
                  </section>
                )}

                {/* STEP 6: REVIEW SCREEN */}
                {currentStep === 6 && (
                  <section className="space-y-4 flex-1">
                    <div className="space-y-1">
                      <h3 className="text-xl sm:text-2xl font-black text-ink dark:text-ink-dark">
                        {t.reviewSummaryHeading}
                      </h3>
                    </div>

                    <div className="bg-surface-low dark:bg-surface-low-dark border border-divider dark:border-divider-dark rounded-2xl p-4 sm:p-5 space-y-3 divide-y divide-divider/60 dark:divide-divider-dark text-sm">
                      <div className="flex items-center justify-between pt-1">
                        <div>
                          <span className="text-xs text-ink-muted dark:text-ink-muted-dark block">
                            {t.reviewCropLabel}
                          </span>
                          <span className="font-bold text-ink dark:text-ink-dark flex items-center gap-1.5">
                            <CropIcon size={18} /> {crop || "Crop"}
                          </span>
                        </div>
                        <button
                          type="button"
                          onClick={() => setCurrentStep(1)}
                          className="text-xs font-bold text-primary dark:text-primary-dark underline p-1"
                        >
                          {t.editLink}
                        </button>
                      </div>

                      <div className="flex items-center justify-between pt-3">
                        <div>
                          <span className="text-xs text-ink-muted dark:text-ink-muted-dark block">
                            {t.reviewLocationLabel}
                          </span>
                          <span className="font-bold text-ink dark:text-ink-dark">
                            📍 {farmerLocation}
                          </span>
                        </div>
                        <button
                          type="button"
                          onClick={() => setCurrentStep(2)}
                          className="text-xs font-bold text-primary dark:text-primary-dark underline p-1"
                        >
                          {t.editLink}
                        </button>
                      </div>

                      <div className="flex items-center justify-between pt-3">
                        <div>
                          <span className="text-xs text-ink-muted dark:text-ink-muted-dark block">
                            {t.reviewQuantityLabel}
                          </span>
                          <span className="font-bold text-ink dark:text-ink-dark tabular-nums">
                            ⚖️ {quantity} {t.quintalsUnit} ({quantity * 2} bags)
                          </span>
                        </div>
                        <button
                          type="button"
                          onClick={() => setCurrentStep(3)}
                          className="text-xs font-bold text-primary dark:text-primary-dark underline p-1"
                        >
                          {t.editLink}
                        </button>
                      </div>

                      <div className="flex items-center justify-between pt-3">
                        <div>
                          <span className="text-xs text-ink-muted dark:text-ink-muted-dark block">
                            {t.reviewStorageLabel}
                          </span>
                          <span className="font-bold text-ink dark:text-ink-dark">
                            🏠 {storageType === "cold_storage" ? t.storageColdTitle : storageType === "warehouse" ? t.storageWarehouseTitle : t.storageNoneTitle}
                          </span>
                        </div>
                        <button
                          type="button"
                          onClick={() => setCurrentStep(4)}
                          className="text-xs font-bold text-primary dark:text-primary-dark underline p-1"
                        >
                          {t.editLink}
                        </button>
                      </div>

                      <div className="flex items-center justify-between pt-3">
                        <div>
                          <span className="text-xs text-ink-muted dark:text-ink-muted-dark block">
                            {t.reviewDebtLabel}
                          </span>
                          <span className="font-bold text-ink dark:text-ink-dark">
                            💳 {debtChoice === "yes" ? t.debtYes : debtChoice === "no" ? t.debtNo : t.debtPrivate}
                          </span>
                        </div>
                        <button
                          type="button"
                          onClick={() => setCurrentStep(5)}
                          className="text-xs font-bold text-primary dark:text-primary-dark underline p-1"
                        >
                          {t.editLink}
                        </button>
                      </div>
                    </div>
                  </section>
                )}

                {/* STEPPER NAVIGATION BUTTONS */}
                <div className="pt-4 flex items-center gap-3 w-full">
                  {currentStep > 1 && (
                    <Button
                      data-testid="back-step-btn"
                      variant="secondary"
                      size="touch"
                      className="w-1/3"
                      onClick={() => setCurrentStep((prev) => prev - 1)}
                      type="button"
                    >
                      <span className="material-symbols-outlined text-[20px] mr-1">
                        arrow_back
                      </span>
                      <span>{t.backBtn}</span>
                    </Button>
                  )}

                  {currentStep < totalSteps ? (
                    <Button
                      data-testid="next-step-btn"
                      variant="primary"
                      size="touch"
                      className={currentStep === 1 ? "w-full" : "w-2/3"}
                      onClick={() => setCurrentStep((prev) => prev + 1)}
                      type="button"
                    >
                      <span>{t.nextBtn}</span>
                      <span className="material-symbols-outlined text-[20px] ml-1">
                        arrow_forward
                      </span>
                    </Button>
                  ) : (
                    <Button
                      data-testid="get-advice-btn"
                      variant="primary"
                      size="touch"
                      className="w-2/3"
                      onClick={fetchAdvice}
                      type="button"
                    >
                      <span>{t.getAdviceBtn}</span>
                      <span className="material-symbols-outlined text-[20px] ml-1">
                        insights
                      </span>
                    </Button>
                  )}
                </div>
              </div>

              {/* RIGHT COLUMN: 7 COLS (Reported Spot Price & Karnataka Tier Map) */}
              <div className="lg:col-span-7 flex flex-col gap-6">
                <ReportedPriceCard
                  priceData={previewPrice}
                  crop={crop}
                  mandi={farmerLocation}
                  language={language}
                />

                <KarnatakaMap
                  mandis={mandis}
                  selectedMandi={farmerLocation}
                  onSelectMandi={(m) => setFarmerLocation(m)}
                  language={language}
                />
              </div>
            </div>
          </div>
        )}

        {/* ================= 3. LOADING SKELETONS ================= */}
        {loading && (
          <div className="flex-1 flex flex-col items-center justify-center py-12 space-y-6 text-center animate-in fade-in duration-fast">
            <span className="material-symbols-outlined text-5xl text-primary animate-spin">
              refresh
            </span>
            <div className="space-y-2 max-w-sm">
              <h3 className="text-xl font-bold text-ink dark:text-ink-dark">
                {t.calculatingAdvice}
              </h3>
              <p className="text-xs text-ink-muted dark:text-ink-muted-dark">
                Checking reporting Karnataka APMCs...
              </p>
            </div>

            <div className="w-full space-y-3 pt-4 max-w-3xl">
              <Skeleton className="h-32 w-full" />
              <Skeleton className="h-44 w-full" />
              <Skeleton className="h-44 w-full" />
            </div>
          </div>
        )}

        {/* ================= 4. RESULTS SECTION (Full 12-Column Desktop Grid) ================= */}
        {activeMode === "advisor" && hasResults && adviceData && whereData && whenData && !loading && (
          <div data-testid="results-deck" className="space-y-8 py-2 sm:py-6 animate-in fade-in duration-fast">
            {/* Top Bar for Resetting / Modifying Inputs */}
            <div className="flex items-center justify-between pb-3 border-b border-divider dark:border-divider-dark">
              <div className="flex items-center gap-2 text-xs sm:text-sm text-ink-muted dark:text-ink-muted-dark font-bold flex-wrap">
                <span className="px-3 py-1 rounded-full bg-surface-low dark:bg-surface-low-dark border border-divider/60">
                  📍 {farmerLocation}
                </span>
                <span className="px-3 py-1 rounded-full bg-surface-low dark:bg-surface-low-dark border border-divider/60 tabular-nums">
                  ⚖️ {quantity} {t.quintalsUnit} ({quantity * 2} bags)
                </span>
                <span className="px-3 py-1 rounded-full bg-surface-low dark:bg-surface-low-dark border border-divider/60 flex items-center gap-1.5">
                  <CropIcon size={16} /> {crop || "Crop"}
                </span>
              </div>
              <button
                type="button"
                onClick={() => {
                  setHasResults(false);
                  setCurrentStep(6);
                }}
                className="text-xs sm:text-sm font-extrabold text-primary dark:text-primary-dark underline select-none p-1"
              >
                {t.editLink}
              </button>
            </div>

            {/* Reported Spot Price Card */}
            <ReportedPriceCard
              priceData={previewPrice}
              crop={crop}
              mandi={farmerLocation}
              language={language}
            />

            {/* NOTICE: No real price history yet, forecasts disabled */}
            {(!forecastData?.horizons?.length || adviceData?.notice) && (
              <div className="bg-amber-100 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-800 text-amber-900 dark:text-amber-200 px-5 py-4 rounded-2xl flex items-center gap-3.5 shadow-sm">
                <span className="text-2xl">⚠️</span>
                <div className="text-sm sm:text-base font-bold">
                  {t.forecastsDisabledNotice}
                </div>
              </div>
            )}

            {/* a. PRIMARY ANSWER BANNER (Deep Forest Green with Large Range & Impact Cards) */}
            <section
              aria-label="Recommendation Summary"
              className="bg-primary-container text-white rounded-3xl p-6 sm:p-8 shadow-elevated space-y-6 relative overflow-hidden"
            >
              <div className="flex items-center justify-between gap-3 flex-wrap">
                <div className="flex items-center gap-2.5">
                  <span className="text-3xl">📢</span>
                  <span className="text-xs font-black tracking-wider uppercase bg-white/20 px-3 py-1 rounded-full">
                    {t.resultsTitle}
                  </span>
                </div>

                <div className="flex items-center gap-2.5 flex-wrap">
                  <ConfidenceBadge
                    level={adviceData.has_low_confidence ? "low" : "high"}
                    label={
                      adviceData.has_low_confidence
                        ? t.lowConfidenceBadge
                        : t.confidenceHigh
                    }
                    reason={adviceData.low_confidence_notice}
                    className="text-white"
                  />
                  <ReadAloudButton
                    text={adviceData.summary_sentence}
                    language={language}
                    playLabel={t.readAloud}
                    stopLabel={t.stopVoice}
                  />
                  <button
                    type="button"
                    onClick={() => window.print()}
                    className="h-10 px-3.5 rounded-xl bg-white/15 hover:bg-white/25 text-white font-bold text-xs flex items-center gap-1.5 transition-colors"
                  >
                    <span className="material-symbols-outlined text-[18px]">print</span>
                    <span>{t.printSlipBtn}</span>
                  </button>
                </div>
              </div>

              {/* Plain Sentence with Range */}
              <div className="space-y-2">
                <h2 className="text-2xl sm:text-4xl font-black leading-tight tracking-tight text-white">
                  "{adviceData.summary_sentence}"
                </h2>
                <p className="text-sm sm:text-base text-white/80 leading-relaxed max-w-3xl">
                  {adviceData.full_advice_text}
                </p>
              </div>

              {/* 3 Financial Impact Callout Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
                <div className="bg-white/15 backdrop-blur-md rounded-2xl p-4 flex flex-col justify-between">
                  <span className="text-xs uppercase font-extrabold text-white/80">
                    {t.todayRealization}
                  </span>
                  <div className="flex items-baseline gap-2 mt-2">
                    <span className="text-2xl sm:text-3xl font-black text-white tabular-nums">
                      {forecastData?.spot_price_today ? `₹${(quantity * forecastData.spot_price_today).toLocaleString("en-IN")}` : t.notAvailable}
                    </span>
                    <span className="text-xs text-white/70">
                      ({quantity} Qtl)
                    </span>
                  </div>
                </div>

                <div className="bg-white text-ink rounded-2xl p-4 shadow-md flex flex-col justify-between">
                  <div className="flex items-center justify-between">
                    <span className="text-xs uppercase font-extrabold text-primary">
                      {t.expectedRealizationWait}
                    </span>
                    <span className="material-symbols-outlined text-primary text-[20px]">
                      trending_up
                    </span>
                  </div>
                  <div className="flex items-baseline gap-2 mt-2">
                    <span className="text-2xl sm:text-3xl font-black text-primary tabular-nums">
                      {whenData?.price_today && whenData?.max_expected_gain_per_qtl
                        ? `₹${(quantity * (whenData.price_today + whenData.max_expected_gain_per_qtl)).toLocaleString("en-IN")}`
                        : t.notAvailable}
                    </span>
                    {whenData?.price_today && whenData?.max_expected_gain_per_qtl ? (
                      <span className="text-xs font-bold text-primary">
                        (+₹{(quantity * whenData.max_expected_gain_per_qtl).toLocaleString("en-IN")})
                      </span>
                    ) : null}
                  </div>
                </div>

                <div className="bg-white/15 backdrop-blur-md rounded-2xl p-4 flex flex-col justify-between">
                  <span className="text-xs uppercase font-extrabold text-white/80">
                    {t.storageRotAllowance}
                  </span>
                  <div className="flex items-baseline gap-2 mt-2">
                    <span className="text-xl sm:text-2xl font-black text-white tabular-nums">
                      ~2.5% Loss
                    </span>
                    <span className="text-xs text-white/70">
                      {t.rotAllowanceDeducted}
                    </span>
                  </div>
                </div>
              </div>

              {/* Action Buttons: WhatsApp Share & Download */}
              <div className="pt-2 border-t border-white/20 flex items-center justify-between gap-3 flex-wrap">
                <ShareButton
                  onShareWhatsApp={handleShareWhatsApp}
                  onDownloadSummary={handleDownloadSummary}
                  whatsAppLabel={t.shareWhatsAppBtn}
                  downloadLabel={t.downloadSummaryBtn}
                />
              </div>
            </section>

            {/* b. WHERE TO SELL: TOP 3 MANDIS & SEPARATE LOCAL MANDI STRIP */}
            <section aria-label="Where to Sell" className="space-y-5">
              <div className="space-y-1">
                <h3 className="text-xl sm:text-3xl font-black text-ink dark:text-ink-dark">
                  {t.whereToSellTitle}
                </h3>
                <p className="text-sm text-ink-muted dark:text-ink-muted-dark">
                  {t.whereToSellSubtitle} {spatialWhereData ? `(${spatialWhereData.reporting_mandis_in_range} mandis reporting in range)` : ""}
                </p>
              </div>

              {/* Separate Local Mandi Comparison Strip */}
              <LocalMandiStrip
                mandiName={farmerLocation}
                netP10={whereData.local_mandi_net_p10}
                netP50={whereData.local_mandi_net_p50}
                language={language}
                title={t.localMandiComparisonTitle}
                desc={t.localMandiComparisonDesc}
                sourceMeasuredLabel={t.sourceMeasured}
              />

              {/* 3 Top Mandi Cards in 3-Column Desktop Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
                {whereData.ranked_mandis
                  .filter((m) => !m.is_local || whereData.ranked_mandis.length <= 1)
                  .slice(0, 3)
                  .map((mandiCard, idx) => (
                    <MandiCard
                      key={mandiCard.mandi}
                      card={mandiCard}
                      language={language}
                      quantityQuintals={quantity}
                      isBest={idx === 0}
                      bestOptionBadgeText={t.bestOptionBadge}
                      priceYouMayGetText={t.priceYouMayGet}
                      worstCaseText={t.worstCasePrice}
                      gainVsLocalText={t.gainVsLocal}
                      gainTotalLotText={t.gainTotalLot}
                      costsTakenOffText={t.costsTakenOffTitle}
                      transportCostText={t.transportCost}
                      mandiFeesText={t.mandiFeesCommission}
                      shrinkageText={t.transitShrinkage}
                      sourceAssumptionText={t.sourceAssumption}
                      sourceMeasuredText={t.sourceMeasured}
                    />
                  ))}
              </div>
            </section>

            {/* c. WHEN TO SELL: HOLD VS SELL TODAY */}
            <section
              aria-label="When to Sell Simulation"
              className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-6 sm:p-8 shadow-card space-y-6"
            >
              <div className="space-y-1">
                <h3 className="text-xl sm:text-2xl font-black text-ink dark:text-ink-dark">
                  {t.whenToSellTitle}
                </h3>
                <p className="text-sm text-ink-muted dark:text-ink-muted-dark">
                  {t.whenToSellSubtitle}
                </p>
              </div>

              {/* Hold Decision Ring & Callout */}
              <div className="bg-surface-low dark:bg-surface-low-dark p-5 rounded-2xl border border-divider/60 dark:border-divider-dark flex flex-col sm:flex-row items-center justify-between gap-6">
                <div className="flex items-center gap-4">
                  <div className="relative w-16 h-16 rounded-full border-4 border-primary flex items-center justify-center shrink-0">
                    <span className="text-sm font-black text-primary dark:text-primary-dark tabular-nums">
                      {whenData.simulation_results[0]
                        ? formatPercent(whenData.simulation_results[0].prob_wait_beats_today_pct)
                        : t.notAvailable}
                    </span>
                  </div>
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-ink-muted dark:text-ink-muted-dark block">
                      {t.chanceWaitingPays}
                    </span>
                    <span className="text-xl font-black text-ink dark:text-ink-dark">
                      {!whenData.price_today
                        ? t.notAvailable
                        : whenData.best_k_days === 0
                        ? t.sellTodayOption
                        : t.waitDaysOption.replace("{days}", String(whenData.best_k_days))}
                    </span>
                  </div>
                </div>

                <div className="text-right">
                  <span className="text-xs text-ink-muted dark:text-ink-muted-dark block">
                    {t.expectedGainWait}
                  </span>
                  <span className="text-2xl font-black text-primary dark:text-primary-dark tabular-nums">
                    {whenData.price_today
                      ? `+${formatCurrency(whenData.max_expected_gain_per_qtl, false)} / qtl`
                      : t.notAvailable}
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-1.5 text-xs text-ink-muted dark:text-ink-muted-dark">
                <span className="material-symbols-outlined text-caution text-[16px]">
                  warning
                </span>
                <span>{t.worstCaseWait}:</span>
                <span className="font-bold text-ink dark:text-ink-dark tabular-nums">
                  {whenData.simulation_results[0]
                    ? `${formatCurrency(whenData.simulation_results[0].worst_case_p10_gain, false)} / qtl`
                    : t.notAvailable}
                </span>
              </div>
            </section>

            {/* d. PRICE OUTLOOK FAN CHART (7, 14, 30 DAYS) or TIER B NOTICE */}
            <section aria-label="Price Outlook Forecast">
              {forecastData?.horizons && forecastData.horizons.length > 0 ? (
                <ChartCard
                  horizons={forecastData.horizons}
                  spotPriceToday={forecastData.spot_price_today}
                  language={language}
                  title={t.chartTitle}
                  subtitle={t.chartSubtitle}
                  axisPriceText={t.axisPrice}
                  axisDaysText={t.axisDays}
                  rangeLegendText={t.rangeLegend}
                  medianLegendText={t.medianLegend}
                />
              ) : (
                <div className="bg-surface-low dark:bg-surface-low-dark border border-divider dark:border-divider-dark rounded-3xl p-6 shadow-sm space-y-3">
                  <div className="flex items-center gap-2.5">
                    <span className="material-symbols-outlined text-[24px] text-primary">schedule</span>
                    <h4 className="font-extrabold text-base text-ink dark:text-ink-dark">
                      {t.tierBBadge}
                    </h4>
                  </div>
                  <p className="text-sm text-ink-muted dark:text-ink-muted-dark leading-relaxed font-medium">
                    {t.forecastNotAvailableNotice}
                  </p>
                </div>
              )}
            </section>

            {/* e. BORROW TOGGLE: E-NWR PLEDGE LOAN VS TRADER ADVANCE */}
            <section
              aria-label="Pledge Credit Comparison"
              className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-6 sm:p-8 shadow-card space-y-4"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="space-y-1">
                  <h4 className="font-bold text-base sm:text-lg text-ink dark:text-ink-dark">
                    {t.borrowToggleTitle}
                  </h4>
                  <p className="text-xs sm:text-sm text-ink-muted dark:text-ink-muted-dark">
                    {t.borrowToggleDesc}
                  </p>
                </div>

                <button
                  type="button"
                  role="switch"
                  aria-checked={borrowToggle}
                  onClick={() => setBorrowToggle(!borrowToggle)}
                  className={`w-14 h-8 rounded-full transition-colors p-1 flex items-center select-none touch-press ${
                    borrowToggle ? "bg-primary justify-end" : "bg-surface-high dark:bg-surface-high-dark justify-start"
                  }`}
                >
                  <span className="w-6 h-6 rounded-full bg-white shadow-sm block" />
                </button>
              </div>

              {borrowToggle && (
                <div className="p-4 rounded-2xl bg-primary-tint dark:bg-primary/10 border border-primary/20 space-y-2 text-xs sm:text-sm animate-in fade-in duration-fast">
                  <span className="font-bold text-primary dark:text-primary-dark block">
                    ✓ {t.borrowActiveStatus}
                  </span>
                  <p className="text-ink-muted dark:text-ink-muted-dark leading-relaxed">
                    Pledge credit at 7% p.a. reduces emergency distress selling. If you hold produce in accredited cold storage, bank pledge loans can finance your operational needs while waiting for higher mandi prices.
                  </p>
                  <p className="text-caution font-semibold">
                    ⚠️ {t.borrowWarning}
                  </p>
                </div>
              )}
            </section>

            {/* f. NEARBY STORAGE OPTIONS */}
            <section
              aria-label="Nearby Storage Facilities"
              className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-6 sm:p-8 shadow-card space-y-4"
            >
              <div className="space-y-1">
                <h3 className="text-xl sm:text-2xl font-black text-ink dark:text-ink-dark">
                  {t.storageNearbyTitle}
                </h3>
                <p className="text-sm text-ink-muted dark:text-ink-muted-dark">
                  {t.storageNearbySubtitle}
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {whenData.storage_options.map((opt) => (
                  <div
                    key={opt.type_key}
                    className="p-4 rounded-2xl bg-surface-low dark:bg-surface-low-dark border border-divider/60 dark:border-divider-dark flex flex-col justify-between space-y-3"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="font-extrabold text-sm text-ink dark:text-ink-dark">
                          {opt.name}
                        </span>
                        <SourceBadge source="assumption" label={t.sourceAssumption} />
                      </div>
                      <span className="text-xs text-ink-muted dark:text-ink-muted-dark block">
                        {opt.distance_km} km away
                      </span>
                      <div className="text-xs text-ink dark:text-ink-dark font-bold tabular-nums pt-1">
                        {t.costPerDay}: ₹{opt.rental_cost_per_qtl_day}/qtl
                      </div>
                    </div>

                    <a
                      href="tel:18001801551"
                      className="w-full h-10 rounded-xl bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark text-xs font-bold text-ink dark:text-ink-dark flex items-center justify-center gap-1 hover:bg-surface-high transition-colors"
                    >
                      <span className="material-symbols-outlined text-[16px]">call</span>
                      <span>{t.callBtn}</span>
                    </a>
                  </div>
                ))}
              </div>
            </section>

            {/* g. FIELD FEEDBACK PROMPT */}
            <div className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-6 text-center space-y-3 shadow-card">
              <span className="text-sm sm:text-base font-bold text-ink dark:text-ink-dark block">
                {t.feedbackPrompt}
              </span>
              {!feedbackGiven ? (
                <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-center gap-3">
                  <button
                    type="button"
                    onClick={() => {
                      setFeedbackGiven(true);
                      showToast(t.feedbackThankYou);
                    }}
                    className="w-full sm:w-auto px-6 py-3 rounded-2xl bg-primary-tint dark:bg-primary/20 text-primary dark:text-primary-dark font-bold text-sm flex items-center justify-center gap-1.5 touch-press min-h-[48px]"
                  >
                    <span>👍</span>
                    <span>{t.feedbackHelpful}</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setFeedbackGiven(true);
                      showToast(t.feedbackThankYou);
                    }}
                    className="w-full sm:w-auto px-6 py-3 rounded-2xl bg-surface-low dark:bg-surface-low-dark text-ink-muted font-bold text-sm flex items-center justify-center gap-1.5 touch-press min-h-[48px]"
                  >
                    <span>👎</span>
                    <span>{t.feedbackNotHelpful}</span>
                  </button>
                </div>
              ) : (
                <p className="text-sm font-bold text-primary dark:text-primary-dark">
                  ✓ {t.feedbackThankYou}
                </p>
              )}
            </div>

            {/* h. FOOTER & HARD RULE: FARMER SOVEREIGNTY */}
            <div className="text-center space-y-2 py-4">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-2xl bg-primary-tint dark:bg-primary/20 text-primary dark:text-primary-dark font-bold text-xs sm:text-sm">
                <span className="material-symbols-outlined text-[18px]">verified</span>
                <span>{t.disclaimer}</span>
              </div>
              <p className="text-xs text-ink-muted dark:text-ink-muted-dark">
                Karnataka APMC Panel: {coverageSummary?.total_mandis || 115} markets • {coverageSummary?.total_crops || 102} crops • Latest: {coverageSummary?.freshness?.latest_report_date || "2026-11-11"}
              </p>
            </div>
          </div>
        )}
      </main>

      {/* Persistent Bottom 4-Tab Navigation */}
      <BottomNav language={language} />

      {/* Settings BottomSheet Modal */}
      <BottomSheet
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        title={t.settingsTitle}
      >
        <div className="space-y-5 text-sm">
          {/* Text Size Control */}
          <div className="space-y-2">
            <span className="font-bold text-ink dark:text-ink-dark block">
              {t.textSizeLabel}
            </span>
            <div className="grid grid-cols-3 gap-2">
              {[
                { size: "normal" as TextSize, label: t.textSizeNormal },
                { size: "large" as TextSize, label: t.textSizeLarge },
                { size: "xlarge" as TextSize, label: t.textSizeXLarge },
              ].map((item) => (
                <button
                  key={item.size}
                  type="button"
                  onClick={() => handleTextSizeChange(item.size)}
                  className={`py-2 px-3 rounded-xl font-bold text-xs transition-colors ${
                    textSize === item.size
                      ? "bg-primary text-white"
                      : "bg-surface-low dark:bg-surface-low-dark text-ink dark:text-ink-dark border border-divider"
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>

          {/* Dark Mode Toggle */}
          <div className="flex items-center justify-between pt-2 border-t border-divider/60 dark:border-divider-dark">
            <span className="font-bold text-ink dark:text-ink-dark">
              {t.darkModeLabel}
            </span>
            <button
              type="button"
              role="switch"
              aria-checked={darkMode}
              onClick={handleDarkModeToggle}
              className={`w-14 h-8 rounded-full transition-colors p-1 flex items-center select-none ${
                darkMode ? "bg-primary justify-end" : "bg-surface-high justify-start"
              }`}
            >
              <span className="w-6 h-6 rounded-full bg-white shadow-sm block" />
            </button>
          </div>

          {/* Start New Farmer Session Button */}
          <div className="pt-3 border-t border-divider/60 dark:border-divider-dark space-y-1">
            <button
              type="button"
              onClick={handleNewFarmerSession}
              className="w-full min-h-[56px] rounded-2xl bg-surface-low dark:bg-surface-low-dark border border-divider dark:border-divider-dark text-ink dark:text-ink-dark font-bold text-sm flex items-center justify-center gap-2 hover:bg-surface-high transition-colors"
            >
              <span className="material-symbols-outlined text-[20px]">person_add</span>
              <span>{t.startNewFarmerBtn}</span>
            </button>
            <span className="text-[11px] text-ink-muted dark:text-ink-muted-dark block text-center">
              {t.startNewFarmerDesc}
            </span>
          </div>
        </div>
      </BottomSheet>

      {/* Floating Action Toast */}
      <Toast message={toastMessage} visible={toastVisible} />
    </div>
  );
}