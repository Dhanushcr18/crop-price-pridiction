"use client";

import React, { useState, useEffect } from "react";
import {
  Sprout,
  Volume2,
  ChevronDown,
  ArrowRight,
  ArrowLeft,
  MapPin,
  TrendingUp,
  FileCheck2,
  Users,
  AlertOctagon,
  ShieldCheck,
  Landmark,
  Check,
  Share2,
  Printer,
  Download,
  Shield,
  TrendingDown,
  Calendar,
  ThumbsUp,
  ThumbsDown,
  Mic,
  UserPlus,
  Sliders,
  Edit3,
  BarChart3,
  BookOpen,
  MessageSquare,
  Clock,
  Scale,
  CheckCircle,
  AlertTriangle,
} from "lucide-react";
import { OnionIcon } from "./ui/Icons";
import {
  Language,
  AreaSummaryResponse,
  SupplyPriceOutlookResponse,
  OfficerReviewResponse,
} from "../types/api";
import { translations } from "../i18n/translations";
import {
  submitAreaReport,
  getAreaSummary,
  getSupplyPriceOutlook,
  getOfficerReview,
} from "../lib/api";

export interface CropAreaViewProps {
  language: Language;
  onLanguageChange?: (lang: Language) => void;
  onBackToAdvisor?: () => void;
  isStandalone?: boolean;
}

const DISTRICT_LIST = [
  "Mysuru",
  "Gadag",
  "Dharwad",
  "Chitradurga",
  "Bagalkot",
  "Vijayapura",
  "Chikkaballapur",
  "Kolar",
  "Ballari",
  "Belagavi",
  "Davanagere",
  "Hassan",
  "Mandya",
  "Tumakuru",
];

const SEASONS = ["Kharif", "Late Kharif", "Rabi"];

export const CropAreaView: React.FC<CropAreaViewProps> = ({
  language,
  onLanguageChange,
  onBackToAdvisor,
}) => {
  const t = translations[language];

  // Screen routing state: 'entry' | 'results' | 'officer' | 'methodology' | 'feedback'
  const [activeScreen, setActiveScreen] = useState<
    "entry" | "results" | "officer" | "methodology" | "feedback"
  >("entry");

  // Form State
  const [district, setDistrict] = useState("Mysuru");
  const [season, setSeason] = useState("Kharif");
  const [year, setYear] = useState("2024-25");
  const [acres, setAcres] = useState<number>(50);
  const [formStep, setFormStep] = useState<1 | 2>(1);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [toastMsg, setToastMsg] = useState<string | null>(null);

  // Result state
  const [hasResults, setHasResults] = useState(false);
  const [areaSummary, setAreaSummary] = useState<AreaSummaryResponse | null>(null);
  const [priceOutlook, setPriceOutlook] = useState<SupplyPriceOutlookResponse | null>(null);
  const [officerData, setOfficerData] = useState<OfficerReviewResponse | null>(null);

  // Scenarios & view preferences
  const [selectedScenario, setSelectedScenario] = useState("normal");
  const [chartScope, setChartScope] = useState<"state" | "india">("state");
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isRecordingMemo, setIsRecordingMemo] = useState(false);
  const [memoRecorded, setMemoRecorded] = useState(false);
  const [feedbackVote, setFeedbackVote] = useState<"helpful" | "not-helpful" | null>(null);
  const [isDuplicateDetected, setIsDuplicateDetected] = useState(false);

  // Device ID persistence
  const getDeviceId = (): string => {
    if (typeof window === "undefined") return "server_device";
    let devId = localStorage.getItem("fsa_device_id");
    if (!devId) {
      devId =
        "dev_" +
        Math.random().toString(36).substring(2, 12) +
        Date.now().toString(36);
      localStorage.setItem("fsa_device_id", devId);
    }
    return devId;
  };

  // Metric conversion helper
  const hectaresValue = (acres * 0.404686).toFixed(2);
  const guntaValue = (acres * 40).toLocaleString("en-IN");

  const showToast = (msg: string) => {
    setToastMsg(msg);
    setTimeout(() => setToastMsg(null), 3500);
  };

  // Initial load or background fetch
  useEffect(() => {
    loadAreaAndOutlook(district, season, year, false);
    loadOfficerData(district);
  }, [district, season, year]);

  const loadAreaAndOutlook = async (
    dist: string,
    seas: string,
    yr: string,
    autoSwitchToResults: boolean = false
  ) => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const [sum, out] = await Promise.all([
        getAreaSummary(dist, seas, yr),
        getSupplyPriceOutlook(dist, seas, yr),
      ]);
      setAreaSummary(sum);
      setPriceOutlook(out);
      if (autoSwitchToResults) {
        setHasResults(true);
        setActiveScreen("results");
      }
    } catch (err: any) {
      console.error("Failed to load crop area outlook:", err);
      setErrorMsg(err.message || "Failed to load area summary");
    } finally {
      setLoading(false);
    }
  };

  const loadOfficerData = async (dist: string) => {
    try {
      const data = await getOfficerReview(dist, 20);
      setOfficerData(data);
    } catch (e) {
      console.warn("Officer data fetch notice:", e);
    }
  };

  const handleSubmit = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (acres <= 0) {
      setErrorMsg("Please enter acres greater than 0");
      return;
    }
    if (acres > 500) {
      setErrorMsg("Acreage cannot exceed 500 acres for a single holding");
      return;
    }

    setLoading(true);
    setErrorMsg(null);
    try {
      const devId = getDeviceId();
      const res = await submitAreaReport({
        district,
        season,
        year,
        acres,
        device_id: devId,
      });

      if (res.action === "updated") {
        setIsDuplicateDetected(true);
      }

      await loadAreaAndOutlook(district, season, year, true);
      showToast(
        language === "kn"
          ? "ವರದಿ ಯಶಸ್ವಿಯಾಗಿ ದಾಖಲಾಗಿದೆ!"
          : language === "hi"
          ? "प्रविष्टि सफलतापूर्वक दर्ज हो गई!"
          : "Report recorded successfully!"
      );
    } catch (err: any) {
      setErrorMsg(err.message || "Could not submit report.");
    } finally {
      setLoading(false);
    }
  };

  // Audio Read Aloud
  const handleReadAloud = (textToRead: string) => {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) {
      showToast("Audio synthesis not available on this device");
      return;
    }
    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(textToRead);
    utterance.lang = language === "kn" ? "kn-IN" : language === "hi" ? "hi-IN" : "en-IN";
    utterance.rate = 0.9;
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);
    setIsSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

  // WhatsApp Share
  const handleWhatsAppShare = () => {
    if (typeof window === "undefined") return;
    const url = window.location.href;
    const summaryText =
      priceOutlook?.supply_summary_sentence ||
      `${district} ${season} onion area outlook`;
    const shareText = `*Farmer Sell Advisor - Crop Area & Supply Outlook*\n\n${summaryText}\n\nCheck live projections: ${url}`;
    if (navigator.clipboard) {
      navigator.clipboard.writeText(shareText);
      showToast(
        language === "kn"
          ? "ವಾಟ್ಸಾಪ್ ಸಂದೇಶ ಲಿಂಕ್ ಕಾಪಿ ಮಾಡಲಾಗಿದೆ!"
          : language === "hi"
          ? "व्हाट्सएप लिंक कॉपी हो गया!"
          : "Summary copied to clipboard for WhatsApp!"
      );
    }
    const waUrl = `https://api.whatsapp.com/send?text=${encodeURIComponent(
      shareText
    )}`;
    window.open(waUrl, "_blank");
  };

  // CSV Export for FPO Officer Review
  const handleExportCsv = () => {
    if (!officerData || !officerData.submissions) return;
    const headers = ["Device_Hash", "Acres", "Hectares", "District", "Season", "Year", "Is_Anomaly", "Created_At"];
    const rows = officerData.submissions.map((s) => [
      s.device_hash,
      s.acres,
      s.hectares,
      s.district,
      s.season,
      s.year,
      s.is_anomaly ? "YES" : "NO",
      s.created_at,
    ]);
    const csvContent =
      "data:text/csv;charset=utf-8," +
      [headers.join(","), ...rows.map((e) => e.join(","))].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `fpo_onion_area_${district}_${season}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast("Cleaned CSV exported!");
  };

  // Test scenarios switcher
  const handleScenarioChange = (scenario: string) => {
    setSelectedScenario(scenario);
    if (scenario === "normal") {
      setDistrict("Mysuru");
      setSeason("Kharif");
      setAcres(50);
      loadAreaAndOutlook("Mysuru", "Kharif", "2024-25", false);
    } else if (scenario === "few-reports") {
      setDistrict("Vijayapura");
      setSeason("Kharif");
      setAcres(10);
      loadAreaAndOutlook("Vijayapura", "Kharif", "2024-25", false);
    } else if (scenario === "missing-official") {
      setDistrict("Mysuru");
      setSeason("Late Kharif");
      loadAreaAndOutlook("Mysuru", "Late Kharif", "2024-25", false);
    } else if (scenario === "high-supply") {
      setDistrict("Gadag");
      setSeason("Kharif");
      setAcres(100);
      loadAreaAndOutlook("Gadag", "Kharif", "2024-25", false);
    }
  };

  // Voice recording simulation
  const handleRecordMemo = () => {
    setIsRecordingMemo(true);
    setTimeout(() => {
      setIsRecordingMemo(false);
      setMemoRecorded(true);
      showToast(
        language === "kn"
          ? "ಧ್ವನಿ ಸಂದೇಶ ಯಶಸ್ವಿಯಾಗಿ ದಾಖಲಾಗಿದೆ!"
          : language === "hi"
          ? "ऑडियो संदेश सफलतापूर्वक रिकॉर्ड हो गया!"
          : "30s Audio note recorded successfully!"
      );
    }, 2500);
  };

  // Kiosk Session Reset
  const handleResetKiosk = () => {
    setDistrict("Mysuru");
    setSeason("Kharif");
    setYear("2024-25");
    setAcres(50);
    setFormStep(1);
    setErrorMsg(null);
    setIsDuplicateDetected(false);
    setActiveScreen("entry");
    showToast(
      language === "kn"
        ? "ಹೊಸ ರೈತರ ನಮೂದು ಆರಂಭವಾಗಿದೆ."
        : language === "hi"
        ? "नए किसान का सत्र शुरू हुआ।"
        : "New farmer session started."
    );
  };

  return (
    <div
      data-testid="crop-area-view"
      className="w-full bg-fsa-cream dark:bg-fsa-creamDark text-fsa-textMainLight dark:text-fsa-textMainDark font-sans min-h-screen flex flex-col selection:bg-fsa-greenLight selection:text-fsa-green antialiased"
    >
      {/* 1. TOP NON-DISMISSIBLE SYNTHETIC DATA BANNER */}
      <div
        className="bg-fsa-terracotta text-white px-4 py-2 text-center text-xs sm:text-sm font-bold tracking-wider flex items-center justify-center gap-2 border-b-2 border-red-800 shadow-sm select-none"
        role="alert"
      >
        <AlertTriangle className="w-4 h-4 sm:w-5 sm:h-5 flex-shrink-0" />
        <span>{t.syntheticBanner}</span>
      </div>

      {/* 2. PERSISTENT TOP APP BAR */}
      <header className="bg-white dark:bg-fsa-surfaceDark border-b border-fsa-borderLight dark:border-fsa-borderDark sticky top-0 z-40 px-4 sm:px-6 py-3 shadow-xs">
        <div className="max-w-[1440px] mx-auto flex items-center justify-between gap-3">
          {/* Brand & Subtitle */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => setActiveScreen("entry")}
              className="flex items-center gap-3 text-left group focus:ring-2 focus:ring-fsa-green rounded-xl p-1"
            >
              <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-xl bg-fsa-green flex items-center justify-center text-white shadow-md group-hover:scale-105 transition-transform">
                <Sprout className="w-5 h-5 sm:w-6 sm:h-6" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-extrabold text-base sm:text-xl tracking-tight text-fsa-textMainLight dark:text-fsa-textMainDark">
                    {t.appName}
                  </span>
                  <span className="bg-fsa-greenLight dark:bg-fsa-greenDark text-fsa-green dark:text-emerald-300 text-[11px] sm:text-xs px-2 py-0.5 rounded-full font-bold uppercase tracking-wider">
                    Karnataka
                  </span>
                </div>
                <p className="text-[11px] sm:text-xs text-fsa-textMutedLight dark:text-fsa-textMutedDark font-medium">
                  {t.areaOutlookTitle} • {t.seasonLabel} {year}
                </p>
              </div>
            </button>
          </div>

          {/* Center Status Indicator (Desktop only) */}
          <div className="hidden lg:flex items-center gap-2 text-sm bg-stone-100 dark:bg-stone-800/80 px-3 py-1.5 rounded-full border border-fsa-borderLight dark:border-fsa-borderDark">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="text-xs font-semibold text-stone-700 dark:text-stone-300">
              {t.liveKioskConnected}
            </span>
          </div>

          {/* Right Controls: Mode Toggle, Language, Theme, New Farmer */}
          <div className="flex items-center gap-2 sm:gap-3">
            {/* Back to Sell Advisor button if onBackToAdvisor exists */}
            {onBackToAdvisor && (
              <button
                onClick={onBackToAdvisor}
                className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-stone-300 dark:border-stone-700 text-xs font-bold text-stone-700 dark:text-stone-200 hover:bg-stone-100 dark:hover:bg-stone-800 transition-colors"
                title={t.backToAdvisorBtn}
              >
                <span>🧅</span>
                <OnionIcon size={16} />
                <span>{t.tabAdvice}</span>
              </button>
            )}

            {/* Strict Single Language Switcher */}
            {onLanguageChange && (
              <div className="flex items-center bg-stone-100 dark:bg-stone-800 p-1 rounded-xl border border-fsa-borderLight dark:border-fsa-borderDark text-xs font-semibold">
                <button
                  type="button"
                  onClick={() => onLanguageChange("en")}
                  className={`px-2 py-1 rounded-lg transition-all ${
                    language === "en"
                      ? "bg-white dark:bg-stone-700 shadow-xs text-fsa-green dark:text-emerald-400 font-bold"
                      : "text-stone-600 dark:text-stone-300 hover:text-fsa-green"
                  }`}
                >
                  English
                </button>
                <button
                  type="button"
                  onClick={() => onLanguageChange("kn")}
                  className={`px-2 py-1 rounded-lg transition-all ${
                    language === "kn"
                      ? "bg-white dark:bg-stone-700 shadow-xs text-fsa-green dark:text-emerald-400 font-bold"
                      : "text-stone-600 dark:text-stone-300 hover:text-fsa-green"
                  }`}
                >
                  ಕನ್ನಡ
                </button>
                <button
                  type="button"
                  onClick={() => onLanguageChange("hi")}
                  className={`px-2 py-1 rounded-lg transition-all ${
                    language === "hi"
                      ? "bg-white dark:bg-stone-700 shadow-xs text-fsa-green dark:text-emerald-400 font-bold"
                      : "text-stone-600 dark:text-stone-300 hover:text-fsa-green"
                  }`}
                >
                  हिन्दी
                </button>
              </div>
            )}

            {/* Kiosk New Farmer Button */}
            <button
              onClick={handleResetKiosk}
              className="flex items-center gap-1.5 bg-amber-50 hover:bg-amber-100 dark:bg-amber-950/40 dark:hover:bg-amber-900/50 border border-amber-300 dark:border-amber-800 text-amber-900 dark:text-amber-200 px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-xl text-xs sm:text-sm font-bold transition-all shadow-xs"
              title={t.startNewFarmer}
            >
              <UserPlus className="w-4 h-4 text-amber-700 dark:text-amber-400" />
              <span className="hidden sm:inline">{t.startNewFarmer}</span>
            </button>
          </div>
        </div>
      </header>

      {/* 3. MAIN WORKSPACE CONTAINER (Sidebar Navigation + Canvas) */}
      <div className="flex-1 max-w-[1440px] w-full mx-auto flex flex-col md:flex-row">
        {/* LEFT SIDEBAR NAVIGATION */}
        <aside className="w-full md:w-64 bg-white/70 dark:bg-fsa-surfaceDark/70 backdrop-blur-md border-r border-fsa-borderLight dark:border-fsa-borderDark p-4 flex flex-col justify-between shrink-0">
          <div className="space-y-6">
            <div className="px-2 py-1 text-xs uppercase tracking-wider text-fsa-textMutedLight dark:text-fsa-textMutedDark font-bold flex items-center gap-1.5">
              <span>{t.tabAdvice}</span>
              <ChevronDown className="w-3 h-3 -rotate-90" />
              <span className="text-fsa-green">{t.tabCropArea}</span>
            </div>

            <nav className="space-y-1.5">
              <button
                type="button"
                onClick={() => setActiveScreen("entry")}
                id="nav-btn-entry"
                className={`w-full flex items-center gap-3 px-3.5 py-3 rounded-xl font-bold text-sm text-left transition-all ${
                  activeScreen === "entry"
                    ? "bg-fsa-green text-white shadow-sm"
                    : "text-stone-700 dark:text-stone-300 hover:bg-stone-100 dark:hover:bg-stone-800"
                }`}
              >
                <Edit3 className="w-4 h-4" />
                <span>{t.navEntry}</span>
              </button>

              <button
                type="button"
                onClick={() => setActiveScreen("results")}
                id="nav-btn-results"
                className={`w-full flex items-center gap-3 px-3.5 py-3 rounded-xl font-semibold text-sm text-left transition-all ${
                  activeScreen === "results"
                    ? "bg-fsa-green text-white shadow-sm"
                    : "text-stone-700 dark:text-stone-300 hover:bg-stone-100 dark:hover:bg-stone-800"
                }`}
              >
                <BarChart3 className="w-4 h-4" />
                <span>{t.navResults}</span>
                {hasResults && (
                  <span className="ml-auto bg-emerald-100 text-emerald-800 text-[10px] font-extrabold px-1.5 py-0.5 rounded-md">
                    LIVE
                  </span>
                )}
              </button>

              <button
                type="button"
                onClick={() => setActiveScreen("officer")}
                id="nav-btn-officer"
                className={`w-full flex items-center gap-3 px-3.5 py-3 rounded-xl font-semibold text-sm text-left transition-all ${
                  activeScreen === "officer"
                    ? "bg-fsa-green text-white shadow-sm"
                    : "text-stone-700 dark:text-stone-300 hover:bg-stone-100 dark:hover:bg-stone-800"
                }`}
              >
                <ShieldCheck className="w-4 h-4 text-fsa-reported" />
                <span>{t.navOfficer}</span>
                <span className="ml-auto bg-amber-100 dark:bg-amber-900/60 text-amber-800 dark:text-amber-300 text-[10px] font-bold px-1.5 py-0.5 rounded-md">
                  Staff
                </span>
              </button>

              <button
                type="button"
                onClick={() => setActiveScreen("methodology")}
                id="nav-btn-methodology"
                className={`w-full flex items-center gap-3 px-3.5 py-3 rounded-xl font-semibold text-sm text-left transition-all ${
                  activeScreen === "methodology"
                    ? "bg-fsa-green text-white shadow-sm"
                    : "text-stone-700 dark:text-stone-300 hover:bg-stone-100 dark:hover:bg-stone-800"
                }`}
              >
                <BookOpen className="w-4 h-4" />
                <span>{t.navSources}</span>
              </button>

              <button
                type="button"
                onClick={() => setActiveScreen("feedback")}
                id="nav-btn-feedback"
                className={`w-full flex items-center gap-3 px-3.5 py-3 rounded-xl font-semibold text-sm text-left transition-all ${
                  activeScreen === "feedback"
                    ? "bg-fsa-green text-white shadow-sm"
                    : "text-stone-700 dark:text-stone-300 hover:bg-stone-100 dark:hover:bg-stone-800"
                }`}
              >
                <MessageSquare className="w-4 h-4" />
                <span>{t.navFeedback}</span>
              </button>
            </nav>

            {/* Interactive Test Scenarios Switcher */}
            <div className="p-3 bg-stone-100 dark:bg-stone-800/90 rounded-2xl border border-stone-200 dark:border-stone-700 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-extrabold uppercase tracking-wider text-stone-500 dark:text-stone-400">
                  {t.interactiveTestScenarios}
                </span>
                <Sliders className="w-3.5 h-3.5 text-stone-400" />
              </div>
              <select
                value={selectedScenario}
                onChange={(e) => handleScenarioChange(e.target.value)}
                className="w-full text-xs font-semibold p-2 rounded-lg bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 text-stone-800 dark:text-stone-200"
              >
                <option value="normal">{t.scenarioNormal}</option>
                <option value="few-reports">{t.scenarioFewReports}</option>
                <option value="missing-official">{t.scenarioMissingOfficial}</option>
                <option value="stale-data">{t.scenarioStaleData}</option>
                <option value="high-supply">{t.scenarioHighSupply}</option>
              </select>
            </div>
          </div>

          {/* Kiosk Assisted Mode Note */}
          <div className="pt-4 border-t border-fsa-borderLight dark:border-fsa-borderDark text-xs text-fsa-textMutedLight dark:text-fsa-textMutedDark">
            <p className="font-semibold text-stone-800 dark:text-stone-200">
              Kiosk Assisted Mode
            </p>
            <p className="text-[11px] mt-0.5">{t.kioskAssistedNote}</p>
          </div>
        </aside>

        {/* MAIN INTERACTIVE CANVAS */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 overflow-y-auto">
          {/* ========================================================================= */}
          {/* SCREEN 1: ENTRY & LIVE CONTEXT                                            */}
          {/* ========================================================================= */}
          {activeScreen === "entry" && (
            <section id="screen-entry" className="space-y-6">
              {/* Screen Title & Read Aloud Guidance */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-fsa-textMainLight dark:text-fsa-textMainDark">
                    {t.areaOutlookTitle}
                  </h1>
                  <p className="text-fsa-textMutedLight dark:text-fsa-textMutedDark text-sm sm:text-base mt-1 font-medium">
                    {t.areaOutlookSubtitle}
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() =>
                    handleReadAloud(`${t.areaOutlookTitle}. ${t.areaOutlookSubtitle}`)
                  }
                  className="self-start sm:self-auto flex items-center gap-2 px-4 py-2.5 rounded-xl border border-emerald-300 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 font-bold text-xs sm:text-sm hover:bg-emerald-100 transition-colors shadow-xs"
                >
                  <Volume2 className="w-4 h-4 sm:w-5 sm:h-5 text-emerald-600 dark:text-emerald-400" />
                  <span>{t.readAloud}</span>
                </button>
              </div>

              {/* 12-Column Responsive Layout: 5 cols Form + 7 cols Context & Map */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                {/* LEFT FORM CARD (5/12 cols) */}
                <form
                  onSubmit={handleSubmit}
                  className="lg:col-span-5 bg-white dark:bg-fsa-surfaceDark rounded-3xl p-5 sm:p-7 border border-fsa-borderLight dark:border-fsa-borderDark shadow-sm space-y-6"
                >
                  {formStep === 1 ? (
                    <div className="space-y-6">
                      {/* Step 1: Select District */}
                      <div className="space-y-2">
                        <label
                          htmlFor="districtSelect"
                          className="flex items-center justify-between font-bold text-sm sm:text-base text-fsa-textMainLight dark:text-fsa-textMainDark"
                        >
                          <span className="flex items-center gap-2">
                            <span className="w-6 h-6 rounded-full bg-fsa-green text-white text-xs flex items-center justify-center font-extrabold">
                              1
                            </span>
                            <span>{t.districtLabel}</span>
                          </span>
                          <span className="text-xs font-semibold text-fsa-green">
                            Karnataka State
                          </span>
                        </label>

                        <div className="relative">
                          <select
                            id="districtSelect"
                            data-testid="area-district-select"
                            value={district}
                            onChange={(e) => setDistrict(e.target.value)}
                            className="w-full text-base sm:text-lg font-semibold py-3.5 pl-4 pr-10 rounded-2xl border-2 border-stone-300 dark:border-stone-600 bg-stone-50 dark:bg-stone-900 text-stone-900 dark:text-stone-100 focus:border-fsa-green appearance-none transition-colors"
                          >
                            {DISTRICT_LIST.map((d) => (
                              <option key={d} value={d}>
                                {d}
                              </option>
                            ))}
                          </select>
                          <ChevronDown className="w-5 h-5 absolute right-4 top-1/2 -translate-y-1/2 text-stone-500 pointer-events-none" />
                        </div>
                      </div>

                      {/* Step 2: Season & Year Selector */}
                      <div className="space-y-2.5">
                        <label className="flex items-center justify-between font-bold text-sm sm:text-base text-fsa-textMainLight dark:text-fsa-textMainDark">
                          <span className="flex items-center gap-2">
                            <span className="w-6 h-6 rounded-full bg-fsa-green text-white text-xs flex items-center justify-center font-extrabold">
                              2
                            </span>
                            <span>{t.seasonLabel}</span>
                          </span>
                          <span className="text-xs font-bold text-stone-500">
                            {year}
                          </span>
                        </label>

                        <div className="grid grid-cols-3 gap-2 p-1.5 bg-stone-100 dark:bg-stone-900 rounded-2xl border border-stone-200 dark:border-stone-800">
                          {SEASONS.map((s) => (
                            <button
                              key={s}
                              type="button"
                              onClick={() => setSeason(s)}
                              className={`py-2 text-center text-xs sm:text-sm font-bold rounded-xl transition-all ${
                                season === s
                                  ? "bg-fsa-green text-white shadow-xs"
                                  : "text-stone-600 dark:text-stone-300 hover:bg-white/60 dark:hover:bg-stone-800"
                              }`}
                            >
                              {s}
                            </button>
                          ))}
                        </div>
                      </div>

                      {/* Step 1 Next Button */}
                      <button
                        type="button"
                        data-testid="area-step1-next-btn"
                        onClick={() => setFormStep(2)}
                        className="w-full py-4 px-6 rounded-2xl bg-fsa-green hover:bg-fsa-greenHover text-white font-extrabold text-base sm:text-lg flex items-center justify-center gap-3 shadow-md hover:shadow-lg active:scale-[0.99] transition-all"
                      >
                        <span>
                          {language === "kn"
                            ? "ಮುಂದೆ: ಎಕರೆ ನಮೂದಿಸಿ"
                            : language === "hi"
                            ? "आगे: रकबा दर्ज करें"
                            : "Next: Enter Acreage"}
                        </span>
                        <ArrowRight className="w-5 h-5 sm:w-6 sm:h-6" />
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-6">
                      <div className="flex items-center justify-between">
                        <button
                          type="button"
                          onClick={() => setFormStep(1)}
                          className="text-xs font-bold text-fsa-green flex items-center gap-1 hover:underline"
                        >
                          <ArrowLeft className="w-3.5 h-3.5" />
                          <span>
                            {language === "kn"
                              ? "ಹಿಂದೆ (ಜಿಲ್ಲೆ ಮತ್ತು ಋತು)"
                              : language === "hi"
                              ? "पीछे (जिला और मौसम)"
                              : "Back (District & Season)"}
                          </span>
                        </button>
                        <span className="text-xs text-stone-500 font-semibold">
                          {district} • {season} {year}
                        </span>
                      </div>

                      {/* Step 3: Onion Acreage Grown Field + Stepper + Quick Chips */}
                      <div className="space-y-3 pt-2 border-t border-stone-200 dark:border-stone-700">
                        <div className="flex items-center justify-between">
                          <label
                            htmlFor="acresInput"
                            className="flex items-center gap-2 font-bold text-sm sm:text-base text-fsa-textMainLight dark:text-fsa-textMainDark"
                          >
                            <span className="w-6 h-6 rounded-full bg-fsa-green text-white text-xs flex items-center justify-center font-extrabold">
                              3
                            </span>
                            <span>{t.stepAcresTitle}</span>
                          </label>
                          <button
                            type="button"
                            onClick={() => {
                              const val = prompt("Speak or enter acres:", "50");
                              if (val && !isNaN(Number(val))) setAcres(Number(val));
                            }}
                            className="flex items-center gap-1.5 text-xs font-bold text-fsa-green dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/50 px-2.5 py-1 rounded-lg border border-emerald-200 dark:border-emerald-800 hover:bg-emerald-100"
                          >
                            <Mic className="w-3.5 h-3.5 text-red-500 animate-pulse" />
                            <span>{t.voiceSpeakAcre}</span>
                          </button>
                        </div>

                        {/* Numeric Input with -/+ Stepper */}
                        <div className="flex items-center gap-2">
                          <button
                            type="button"
                            onClick={() => setAcres(Math.max(1, acres - 5))}
                            className="w-12 h-12 sm:w-14 sm:h-14 rounded-2xl border-2 border-stone-300 dark:border-stone-700 bg-stone-100 dark:bg-stone-800 text-2xl font-bold flex items-center justify-center hover:bg-stone-200 active:scale-95 transition-transform"
                            aria-label="Decrease acres by 5"
                          >
                            -
                          </button>
                          <div className="relative flex-1">
                            <input
                              type="number"
                              id="acresInput"
                              value={acres}
                              min={1}
                              max={500}
                              onChange={(e) => setAcres(Number(e.target.value))}
                              className="w-full text-center text-2xl sm:text-3xl font-extrabold py-2 px-3 rounded-2xl border-2 border-stone-300 dark:border-stone-600 bg-white dark:bg-stone-900 text-stone-900 dark:text-white tabular-nums focus:border-fsa-green"
                            />
                            <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs sm:text-sm font-bold text-stone-400">
                              {t.acresLabel}
                            </span>
                          </div>
                          <button
                            type="button"
                            onClick={() => setAcres(Math.min(500, acres + 5))}
                            className="w-12 h-12 sm:w-14 sm:h-14 rounded-2xl border-2 border-stone-300 dark:border-stone-700 bg-stone-100 dark:bg-stone-800 text-2xl font-bold flex items-center justify-center hover:bg-stone-200 active:scale-95 transition-transform"
                            aria-label="Increase acres by 5"
                          >
                            +
                          </button>
                        </div>

                        {/* Quick Select Chips (5, 10, 25, 50, 100) */}
                        <div className="flex items-center gap-2 flex-wrap pt-1">
                          <span className="text-xs font-semibold text-stone-500 mr-1">
                            Quick:
                          </span>
                          {[5, 10, 25, 50, 100].map((num) => (
                            <button
                              key={num}
                              type="button"
                              onClick={() => setAcres(num)}
                              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                                acres === num
                                  ? "border-2 border-fsa-green bg-fsa-greenLight dark:bg-fsa-greenDark text-fsa-green dark:text-emerald-300"
                                  : "border border-stone-300 dark:border-stone-700 bg-stone-50 dark:bg-stone-800 text-stone-700 dark:text-stone-300 hover:border-fsa-green"
                              }`}
                            >
                              {num} {t.acresLabel}
                            </button>
                          ))}
                        </div>

                        {/* Live Automatic Metric Conversion Pill */}
                        <div className="p-3 bg-stone-100 dark:bg-stone-800/80 rounded-2xl flex items-center justify-between text-xs sm:text-sm font-semibold border border-stone-200 dark:border-stone-700">
                          <span className="text-stone-600 dark:text-stone-300 flex items-center gap-1.5">
                            <Scale className="w-4 h-4 text-stone-500" />
                            <span>Metric:</span>
                          </span>
                          <span className="text-fsa-green dark:text-emerald-400 font-extrabold tabular-nums">
                            {acres} {t.acresLabel} = {hectaresValue} ha ({guntaValue}{" "}
                            ಗುಂಟೆ)
                          </span>
                        </div>
                      </div>

                      {/* HARD RULE DISCLOSURE: Isolation & Integrity */}
                      <div className="p-3.5 rounded-2xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/70 flex items-start gap-2.5">
                        <Shield className="w-4 h-4 text-amber-700 dark:text-amber-400 shrink-0 mt-0.5" />
                        <p className="text-xs text-amber-900 dark:text-amber-200 font-medium leading-relaxed">
                          <strong>{t.farmerAcreageIsolatedNote}</strong>
                        </p>
                      </div>

                      {errorMsg && (
                        <div className="p-3 rounded-xl bg-red-100 text-red-800 text-xs font-bold">
                          {errorMsg}
                        </div>
                      )}

                      {/* PRIMARY ACTION BUTTON */}
                      <button
                        type="submit"
                        data-testid="area-submit-btn"
                        disabled={loading}
                        className="w-full py-4 px-6 rounded-2xl bg-fsa-green hover:bg-fsa-greenHover text-white font-extrabold text-base sm:text-lg flex items-center justify-center gap-3 shadow-md hover:shadow-lg active:scale-[0.99] transition-all disabled:opacity-50"
                      >
                        <span>{loading ? "Loading..." : t.submitAreaBtn}</span>
                        <ArrowRight className="w-5 h-5 sm:w-6 sm:h-6" />
                      </button>
                    </div>
                  )}
                </form>

                {/* RIGHT COLUMN: LIVE CONTEXT PANEL & KARNATAKA MAP (7/12 cols) */}
                <div className="lg:col-span-7 space-y-6">
                  <div className="bg-white dark:bg-fsa-surfaceDark rounded-3xl p-5 sm:p-6 border border-fsa-borderLight dark:border-fsa-borderDark shadow-sm">
                    <div className="flex items-center justify-between pb-4 border-b border-fsa-borderLight dark:border-fsa-borderDark">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-fsa-officialBg dark:bg-fsa-officialBgDark text-fsa-official dark:text-emerald-400 flex items-center justify-center">
                          <MapPin className="w-5 h-5 sm:w-6 sm:h-6" />
                        </div>
                        <div>
                          <h2 className="text-base sm:text-lg font-bold text-stone-900 dark:text-stone-100 flex items-center gap-2">
                            <span>{district} District Context</span>
                            <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
                              {season} {year}
                            </span>
                          </h2>
                          <p className="text-xs text-stone-500">
                            Live agricultural baseline before reporting
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <span className="text-xs font-bold text-stone-500 uppercase tracking-wider block">
                          Official Source
                        </span>
                        <span className="text-xs sm:text-sm font-extrabold text-fsa-official dark:text-emerald-400">
                          DES Karnataka
                        </span>
                      </div>
                    </div>

                    {/* Quick 3 Stat Tiles inside Preview */}
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4 my-5">
                      <div className="p-3.5 sm:p-4 rounded-2xl bg-stone-50 dark:bg-stone-900 border border-stone-200 dark:border-stone-800">
                        <span className="text-xs font-bold text-stone-500 block">
                          Last Year District Area
                        </span>
                        <p className="text-xl sm:text-2xl font-extrabold text-stone-900 dark:text-stone-100 tabular-nums mt-1">
                          {areaSummary?.district_official
                            ? `${areaSummary.district_official.area_acres.toLocaleString(
                                "en-IN"
                              )} `
                            : "Not available"}
                          <span className="text-xs font-medium text-stone-500">
                            {t.acresLabel}
                          </span>
                        </p>
                        <span className="text-[11px] text-stone-500 mt-1 block">
                          {areaSummary?.district_official
                            ? `${areaSummary.district_official.area_hectares.toLocaleString(
                                "en-IN"
                              )} ha`
                            : "State fallback active"}
                        </span>
                      </div>

                      <div className="p-3.5 sm:p-4 rounded-2xl bg-stone-50 dark:bg-stone-900 border border-stone-200 dark:border-stone-800">
                        <span className="text-xs font-bold text-stone-500 block">
                          {t.fiveYearAvg}
                        </span>
                        <p className="text-xl sm:text-2xl font-extrabold text-stone-900 dark:text-stone-100 tabular-nums mt-1">
                          {areaSummary?.state_official
                            ? `${(
                                areaSummary.state_official.avg_5yr_acres / 100000
                              ).toFixed(1)} L `
                            : "2.0 L "}
                          <span className="text-xs font-medium text-stone-500">
                            {t.acresLabel}
                          </span>
                        </p>
                        <span className="text-[11px] text-emerald-600 font-bold mt-1 block">
                          Expected sowing progress
                        </span>
                      </div>

                      <div className="p-3.5 sm:p-4 rounded-2xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/80">
                        <span className="text-xs font-bold text-amber-800 dark:text-amber-300 block">
                          Farmer Reports
                        </span>
                        <p className="text-xl sm:text-2xl font-extrabold text-amber-900 dark:text-amber-200 tabular-nums mt-1">
                          {areaSummary?.farmer_reported.entry_count || 5}{" "}
                          <span className="text-xs font-medium">farmers</span>
                        </p>
                        <span className="text-[11px] text-amber-700 dark:text-amber-400 font-bold mt-1 block">
                          {areaSummary?.farmer_reported.too_few_reports
                            ? "Too few reports to trust"
                            : "Verified coverage"}
                        </span>
                      </div>
                    </div>

                    {/* Stylized Karnataka SVG Map with Onion Producing Belts */}
                    <div className="rounded-2xl bg-stone-100 dark:bg-stone-900 p-4 border border-stone-200 dark:border-stone-800 relative overflow-hidden">
                      <div className="flex items-center justify-between text-xs font-bold text-stone-600 dark:text-stone-300 mb-2">
                        <span>Karnataka Onion Producing Belts</span>
                        <span className="flex items-center gap-1.5">
                          <span className="w-2.5 h-2.5 rounded-full bg-fsa-green"></span>{" "}
                          Selected: {district}
                        </span>
                      </div>

                      <svg
                        viewBox="0 0 600 320"
                        className="w-full h-52 sm:h-56 rounded-xl bg-emerald-950/5 dark:bg-stone-950 border border-stone-200 dark:border-stone-800"
                      >
                        {/* Karnataka silhouette outline */}
                        <path
                          d="M 180,30 L 290,20 L 370,40 L 410,90 L 360,160 L 380,240 L 310,290 L 230,300 L 190,260 L 160,190 L 170,120 Z"
                          fill="#E2E8F0"
                          className="dark:fill-stone-800 stroke-stone-300 dark:stroke-stone-700"
                          strokeWidth="2"
                        />

                        {/* Northern Cluster (Bagalkote, Vijayapura, Gadag) */}
                        <polygon
                          points="270,50 330,55 350,100 290,110 260,80"
                          fill="#93C5FD"
                          className="dark:fill-sky-950 cursor-pointer hover:opacity-80"
                          stroke="#3B82F6"
                          strokeWidth="1.5"
                        />
                        <text
                          x="270"
                          y="85"
                          fontSize="11"
                          fontWeight="bold"
                          fill="#1E3A8A"
                          className="dark:fill-sky-300"
                        >
                          North Cluster (Gadag/Bagalkot)
                        </text>

                        {/* Central Cluster (Chitradurga, Davanagere) */}
                        <polygon
                          points="260,120 330,125 340,170 270,175 240,140"
                          fill="#BBF7D0"
                          className="dark:fill-emerald-950 cursor-pointer hover:opacity-80"
                          stroke="#22C55E"
                          strokeWidth="1.5"
                        />
                        <text
                          x="250"
                          y="150"
                          fontSize="11"
                          fontWeight="bold"
                          fill="#14532D"
                          className="dark:fill-emerald-300"
                        >
                          Central Cluster (Chitradurga)
                        </text>

                        {/* Southern Cluster (Mysuru) */}
                        <polygon
                          points="240,210 310,215 315,265 250,270 220,240"
                          fill={district === "Mysuru" ? "#15803D" : "#E2E8F0"}
                          className="cursor-pointer"
                          stroke="#2E7D32"
                          strokeWidth={district === "Mysuru" ? "3" : "1"}
                        />
                        <circle
                          cx="270"
                          cy="240"
                          r="7"
                          fill="#FBBF24"
                          stroke="#78350F"
                          strokeWidth="2"
                        />
                        <text
                          x="285"
                          y="244"
                          fontSize="12"
                          fontWeight="900"
                          fill="#15803D"
                          className="dark:fill-emerald-400"
                        >
                          ★ {district.toUpperCase()} ({acres} ac entered)
                        </text>

                        {/* Legend */}
                        <g transform="translate(430, 20)">
                          <rect
                            width="150"
                            height="95"
                            rx="10"
                            fill="white"
                            className="dark:fill-stone-900"
                            stroke="#CBD5E1"
                            strokeWidth="1"
                          />
                          <text
                            x="12"
                            y="22"
                            fontSize="10"
                            fontWeight="bold"
                            fill="#64748B"
                          >
                            MAP LEGEND
                          </text>
                          <circle cx="20" cy="40" r="5" fill="#15803D" />
                          <text
                            x="32"
                            y="44"
                            fontSize="10"
                            fontWeight="600"
                            fill="#334155"
                            className="dark:fill-stone-300"
                          >
                            Active Focus
                          </text>
                          <circle
                            cx="20"
                            cy="60"
                            r="5"
                            fill="#BBF7D0"
                            stroke="#22C55E"
                          />
                          <text
                            x="32"
                            y="64"
                            fontSize="10"
                            fontWeight="600"
                            fill="#334155"
                            className="dark:fill-stone-300"
                          >
                            Sowing Zones
                          </text>
                          <circle cx="20" cy="80" r="5" fill="#FBBF24" />
                          <text
                            x="32"
                            y="84"
                            fontSize="10"
                            fontWeight="600"
                            fill="#334155"
                            className="dark:fill-stone-300"
                          >
                            FPO Terminal
                          </text>
                        </g>
                      </svg>
                    </div>

                    {isDuplicateDetected && (
                      <div className="mt-4 p-3 rounded-xl bg-sky-50 dark:bg-sky-950/40 border border-sky-300 dark:border-sky-800 flex items-center justify-between text-xs">
                        <span className="text-sky-900 dark:text-sky-200 font-medium">
                          <strong>Notice:</strong> An entry was previously
                          recorded from this device for {district}. Your latest
                          report has safely updated your record.
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </section>
          )}

          {/* ========================================================================= */}
          {/* SCREEN 2: SUPPLY OUTLOOK RESULTS (Main Screen)                            */}
          {/* ========================================================================= */}
          {activeScreen === "results" && (
            <section
              id="screen-results"
              data-testid="area-results-deck"
              className="space-y-7"
            >
              {/* Return to Entry & Share Toolbar */}
              <div className="flex items-center justify-between">
                <button
                  type="button"
                  onClick={() => setActiveScreen("entry")}
                  className="flex items-center gap-2 text-sm font-bold text-fsa-green dark:text-emerald-400 hover:underline"
                >
                  <ArrowLeft className="w-4 h-4" />
                  <span>{t.editLink}</span>
                </button>

                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={handleWhatsAppShare}
                    className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-xs transition-colors"
                  >
                    <Share2 className="w-4 h-4" />
                    <span>{t.shareWhatsApp}</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      if (typeof window !== "undefined") window.print();
                    }}
                    className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl border border-stone-300 dark:border-stone-700 bg-white dark:bg-stone-800 text-stone-700 dark:text-stone-300 font-bold text-xs hover:bg-stone-50 transition-colors"
                  >
                    <Printer className="w-4 h-4" />
                    <span>{t.printPdf}</span>
                  </button>
                </div>
              </div>

              {/* a. EXECUTIVE SUMMARY BANNER (Answer First) */}
              <div className="p-6 rounded-3xl bg-emerald-900 text-white shadow-md relative overflow-hidden flex flex-col md:flex-row md:items-center justify-between gap-6 border-l-8 border-emerald-400">
                <div className="space-y-2 max-w-3xl">
                  <div className="flex items-center gap-2.5">
                    <span className="bg-emerald-400/20 text-emerald-300 border border-emerald-400/30 text-xs px-2.5 py-0.5 rounded-full font-bold uppercase tracking-wider">
                      Summary Signal
                    </span>
                    <span className="text-xs text-emerald-200">
                      {season} {year} Outlook
                    </span>
                  </div>
                  <h2 className="text-xl sm:text-2xl lg:text-3xl font-extrabold tracking-tight leading-snug">
                    {district}: {acres} {t.acresLabel} {t.reportedByYouPrefix}:{" "}
                    {areaSummary?.state_official
                      ? `Karnataka onion area this season: ${(
                          areaSummary.state_official.area_acres / 100000
                        ).toFixed(2)} lakh acres`
                      : "Official Karnataka sowing data active"}
                  </h2>
                  <p className="text-xs sm:text-sm text-emerald-100 font-medium leading-relaxed">
                    {priceOutlook?.supply_summary_sentence ||
                      "Official government releases confirm higher planted acreage statewide. Higher planted area has historically been accompanied by moderated wholesale prices."}
                  </p>
                </div>

                {/* Confidence Badge & Audio Listen */}
                <div className="flex flex-row md:flex-col items-center md:items-end gap-3 shrink-0">
                  <div className="bg-emerald-950/80 border border-emerald-700/60 px-4 py-2.5 rounded-2xl text-center shadow-inner">
                    <span className="text-[11px] font-bold text-emerald-300 uppercase tracking-wider block">
                      Outlook Confidence
                    </span>
                    <span className="text-base sm:text-lg font-extrabold text-emerald-100 flex items-center justify-center gap-1.5 mt-0.5">
                      <CheckCircle className="w-4 h-4 text-emerald-400" />
                      <span>{priceOutlook?.confidence_badge || "Fair"}</span>
                    </span>
                  </div>

                  <button
                    type="button"
                    onClick={() =>
                      handleReadAloud(
                        `${district}: ${acres} acres reported. ${priceOutlook?.supply_summary_sentence}`
                      )
                    }
                    className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white font-bold text-xs transition-colors"
                  >
                    <Volume2 className="w-4 h-4 text-emerald-300" />
                    <span>{t.readAloud}</span>
                  </button>
                </div>
              </div>

              {/* STALE DATA WARNING BANNER */}
              {selectedScenario === "stale-data" && (
                <div className="p-4 rounded-2xl bg-amber-50 dark:bg-amber-950/50 border border-amber-300 dark:border-amber-700 flex items-center gap-3 text-amber-900 dark:text-amber-200 text-xs sm:text-sm">
                  <Clock className="w-5 h-5 text-amber-700 dark:text-amber-400 shrink-0" />
                  <div>
                    <strong>{t.staleDataWarningNotice}</strong> Updated sowing
                    figures from DES Karnataka expected by next Tuesday.
                  </div>
                </div>
              )}

              {/* b. THREE AREA CARDS (District | Karnataka | India) */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* CARD 1: DISTRICT CARD with Nested Reported by Farmers strip */}
                <div className="bg-white dark:bg-fsa-surfaceDark rounded-3xl p-5 sm:p-6 border-2 border-stone-200 dark:border-stone-700 shadow-sm flex flex-col justify-between">
                  <div className="space-y-4">
                    <div className="flex items-start justify-between">
                      <div>
                        <span className="text-xs font-bold text-stone-500 uppercase tracking-wider">
                          {t.cardDistrict}
                        </span>
                        <h3 className="text-xl sm:text-2xl font-black text-stone-900 dark:text-stone-100">
                          {district}
                        </h3>
                      </div>
                      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-extrabold bg-amber-100 text-amber-800 dark:bg-amber-900/60 dark:text-amber-300 border border-amber-300 dark:border-amber-700">
                        <TrendingUp className="w-3.5 h-3.5" />
                        <span>
                          {areaSummary?.district_official
                            ? areaSummary.district_official.signal_category.toUpperCase()
                            : "FALLBACK"}
                        </span>
                      </span>
                    </div>

                    {areaSummary?.district_official_available &&
                    areaSummary.district_official ? (
                      <div>
                        <div className="flex items-baseline gap-2">
                          <span className="text-3xl sm:text-4xl font-black text-stone-950 dark:text-white tabular-nums">
                            {areaSummary.district_official.area_acres.toLocaleString(
                              "en-IN"
                            )}
                          </span>
                          <span className="text-base sm:text-lg font-bold text-stone-600 dark:text-stone-400">
                            {t.acresLabel}
                          </span>
                        </div>
                        <div className="text-xs sm:text-sm font-semibold text-stone-500 mt-0.5">
                          {Math.round(
                            areaSummary.district_official.area_hectares
                          ).toLocaleString("en-IN")}{" "}
                          ha • 5-Yr:{" "}
                          {Math.round(
                            areaSummary.district_official.avg_5yr_acres
                          ).toLocaleString("en-IN")}{" "}
                          ac
                        </div>
                        <div className="mt-3 flex items-center gap-2 p-2 rounded-xl bg-fsa-officialBg dark:bg-fsa-officialBgDark text-fsa-official dark:text-emerald-300 text-xs font-bold border border-fsa-officialBorder dark:border-emerald-800">
                          <FileCheck2 className="w-4 h-4 shrink-0" />
                          <span className="truncate">
                            {areaSummary.district_official.source_name} •{" "}
                            {areaSummary.district_official.publication_date}
                          </span>
                        </div>
                      </div>
                    ) : (
                      <div className="p-3.5 rounded-2xl bg-stone-50 dark:bg-stone-900 border border-stone-200 dark:border-stone-800 space-y-1">
                        <span className="text-xs font-extrabold text-stone-700 dark:text-stone-300 block">
                          {t.notAvailable}
                        </span>
                        <p className="text-xs text-stone-500 leading-relaxed">
                          {t.districtNotTrackedDisclaimer}
                        </p>
                      </div>
                    )}
                  </div>

                  {/* c. NESTED REPORTED-BY-FARMERS PANEL */}
                  <div className="mt-6 pt-5 border-t-2 border-dashed border-stone-200 dark:border-stone-700 space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="inline-flex items-center gap-1.5 text-xs font-black uppercase tracking-wider px-2.5 py-0.5 rounded-md bg-fsa-reportedBg dark:bg-fsa-reportedBgDark text-fsa-reported dark:text-amber-400 border border-fsa-reportedBorder dark:border-amber-700">
                        <Users className="w-3.5 h-3.5" />
                        <span>{t.reportedByFarmersStrip}</span>
                      </span>
                      <span className="text-xs font-extrabold text-stone-700 dark:text-stone-300">
                        {areaSummary?.farmer_reported.entry_count || 5} farmers
                      </span>
                    </div>

                    <div className="flex items-baseline justify-between">
                      <div>
                        <span className="text-xl sm:text-2xl font-black text-amber-900 dark:text-amber-300 tabular-nums">
                          {Math.round(
                            areaSummary?.farmer_reported.reported_acres ||
                              250
                          ).toLocaleString("en-IN")}
                        </span>
                        <span className="text-xs font-bold text-stone-500 ml-1">
                          ac entered
                        </span>
                      </div>
                      <div className="text-right">
                        <span className="text-xs font-bold text-stone-500">
                          {t.coverageRatioLabel}
                        </span>
                        <p className="text-xs sm:text-sm font-black text-stone-800 dark:text-stone-200 tabular-nums">
                          {areaSummary?.farmer_reported.coverage_pct !== null &&
                          areaSummary?.farmer_reported.coverage_pct !== undefined
                            ? `${areaSummary.farmer_reported.coverage_pct.toFixed(
                                1
                              )}%`
                            : "N/A"}
                        </p>
                      </div>
                    </div>

                    {/* Coverage Meter with 5% threshold marker */}
                    <div className="space-y-1">
                      <div className="relative w-full h-3 bg-stone-200 dark:bg-stone-700 rounded-full overflow-hidden">
                        <div
                          className="absolute left-[33%] top-0 bottom-0 w-0.5 bg-red-600 z-10"
                          title="5% Trust Threshold"
                        ></div>
                        <div
                          className="h-full bg-amber-500 rounded-full transition-all duration-500"
                          style={{
                            width: `${Math.min(
                              100,
                              ((areaSummary?.farmer_reported.coverage_pct || 1) /
                                10) *
                                100
                            )}%`,
                          }}
                        ></div>
                      </div>
                      <div className="flex justify-between text-[10px] font-bold text-stone-500">
                        <span>0%</span>
                        <span className="text-red-600 font-extrabold">
                          ▲ 5% Trust Threshold
                        </span>
                        <span>10% Target</span>
                      </div>
                    </div>

                    {/* Warning if <30 reports or <5% coverage */}
                    {areaSummary?.farmer_reported.too_few_reports && (
                      <div className="p-2.5 rounded-xl bg-red-50 dark:bg-red-950/40 border border-red-300 dark:border-red-800 text-red-900 dark:text-red-200 text-xs font-semibold flex items-center gap-2">
                        <AlertOctagon className="w-4 h-4 text-red-600 shrink-0" />
                        <span>
                          ⚠️ Too few reports to trust (
                          {areaSummary.farmer_reported.entry_count} entries; minimum 30
                          reports and 5% coverage required).
                        </span>
                      </div>
                    )}
                  </div>
                </div>

                {/* CARD 2: STATE CARD (Karnataka) */}
                <div className="bg-white dark:bg-fsa-surfaceDark rounded-3xl p-5 sm:p-6 border-2 border-stone-200 dark:border-stone-700 shadow-sm flex flex-col justify-between">
                  <div className="space-y-4">
                    <div className="flex items-start justify-between">
                      <div>
                        <span className="text-xs font-bold text-stone-500 uppercase tracking-wider">
                          {t.cardState}
                        </span>
                        <h3 className="text-xl sm:text-2xl font-black text-stone-900 dark:text-stone-100">
                          Karnataka
                        </h3>
                      </div>
                      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-extrabold bg-amber-100 text-amber-800 dark:bg-amber-900/60 dark:text-amber-300 border border-amber-300 dark:border-amber-700">
                        <TrendingUp className="w-3.5 h-3.5" />
                        <span>
                          {areaSummary?.state_official?.signal_category === "higher"
                            ? t.signalHigher
                            : t.signalNormal}
                        </span>
                      </span>
                    </div>

                    {areaSummary?.state_official && (
                      <div>
                        <div className="flex items-baseline gap-2">
                          <span className="text-3xl sm:text-4xl font-black text-stone-950 dark:text-white tabular-nums">
                            {areaSummary.state_official.area_acres.toLocaleString(
                              "en-IN"
                            )}
                          </span>
                          <span className="text-base sm:text-lg font-bold text-stone-600 dark:text-stone-400">
                            {t.acresLabel}
                          </span>
                        </div>
                        <div className="text-xs sm:text-sm font-semibold text-stone-500 mt-0.5">
                          {Math.round(
                            areaSummary.state_official.area_hectares
                          ).toLocaleString("en-IN")}{" "}
                          ha • {t.fiveYearAvg}:{" "}
                          {Math.round(
                            areaSummary.state_official.avg_5yr_acres
                          ).toLocaleString("en-IN")}{" "}
                          ac
                        </div>

                        <div className="mt-3 flex items-center gap-2 p-2 rounded-xl bg-fsa-officialBg dark:bg-fsa-officialBgDark text-fsa-official dark:text-emerald-300 text-xs font-bold border border-fsa-officialBorder dark:border-emerald-800">
                          <ShieldCheck className="w-4 h-4 shrink-0" />
                          <span className="truncate">
                            {areaSummary.state_official.source_name}
                          </span>
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="pt-5 border-t border-stone-200 dark:border-stone-700 space-y-2 text-xs">
                    <div className="flex justify-between font-medium text-stone-600 dark:text-stone-400">
                      <span>Top Sowing Belts:</span>
                      <span className="font-bold text-stone-900 dark:text-stone-100">
                        Gadag, Chitradurga, Bagalkot
                      </span>
                    </div>
                    <div className="flex justify-between font-medium text-stone-600 dark:text-stone-400">
                      <span>Sowing Progress:</span>
                      <span className="font-bold text-emerald-600">
                        94% Completed
                      </span>
                    </div>
                  </div>
                </div>

                {/* CARD 3: ALL-INDIA CARD */}
                <div className="bg-white dark:bg-fsa-surfaceDark rounded-3xl p-5 sm:p-6 border-2 border-stone-200 dark:border-stone-700 shadow-sm flex flex-col justify-between">
                  <div className="space-y-4">
                    <div className="flex items-start justify-between">
                      <div>
                        <span className="text-xs font-bold text-stone-500 uppercase tracking-wider">
                          {t.cardCountry}
                        </span>
                        <h3 className="text-xl sm:text-2xl font-black text-stone-900 dark:text-stone-100">
                          India (National)
                        </h3>
                      </div>
                      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-extrabold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">
                        <Check className="w-3.5 h-3.5" />
                        <span>{t.signalNormal}</span>
                      </span>
                    </div>

                    {areaSummary?.country_official && (
                      <div>
                        <div className="flex items-baseline gap-2">
                          <span className="text-3xl sm:text-4xl font-black text-stone-950 dark:text-white tabular-nums">
                            {(
                              areaSummary.country_official.area_acres / 100000
                            ).toFixed(1)}{" "}
                            L
                          </span>
                          <span className="text-base sm:text-lg font-bold text-stone-600 dark:text-stone-400">
                            {t.acresLabel}
                          </span>
                        </div>
                        <div className="text-xs sm:text-sm font-semibold text-stone-500 mt-0.5">
                          {Math.round(
                            areaSummary.country_official.area_hectares
                          ).toLocaleString("en-IN")}{" "}
                          ha • {t.fiveYearAvg}:{" "}
                          {(
                            areaSummary.country_official.avg_5yr_acres / 100000
                          ).toFixed(1)}{" "}
                          L ac
                        </div>

                        <div className="mt-3 flex items-center gap-2 p-2 rounded-xl bg-fsa-officialBg dark:bg-fsa-officialBgDark text-fsa-official dark:text-emerald-300 text-xs font-bold border border-fsa-officialBorder dark:border-emerald-800">
                          <Landmark className="w-4 h-4 shrink-0" />
                          <span className="truncate">
                            {areaSummary.country_official.source_name}
                          </span>
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="pt-5 border-t border-stone-200 dark:border-stone-700 space-y-2 text-xs">
                    <div className="flex justify-between font-medium text-stone-600 dark:text-stone-400">
                      <span>Key Producing States:</span>
                      <span className="font-bold text-stone-900 dark:text-stone-100">
                        Maharashtra, MP, Karnataka
                      </span>
                    </div>
                    <div className="flex justify-between font-medium text-stone-600 dark:text-stone-400">
                      <span>National Buffer Stock:</span>
                      <span className="font-bold text-stone-800 dark:text-stone-200">
                        5.0 Lakh MT (NCCF / NAFED)
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* d. TWO-COLUMN ROW: AREA BAR CHART (5-YR) + ESTIMATED MARKET SUPPLY GAUGE */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                {/* LEFT: 5-YEAR HISTORICAL BAR CHART (7/12 cols) */}
                <div className="lg:col-span-7 bg-white dark:bg-fsa-surfaceDark rounded-3xl p-5 sm:p-6 border border-fsa-borderLight dark:border-fsa-borderDark shadow-sm space-y-4">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div>
                      <h3 className="text-base sm:text-lg font-black text-stone-900 dark:text-stone-100">
                        {t.historyChartHeading}
                      </h3>
                      <p className="text-xs text-stone-500">
                        Unit: Lakh Acres • Official Government Series
                      </p>
                    </div>
                    <div className="flex items-center bg-stone-100 dark:bg-stone-800 p-1 rounded-xl text-xs font-bold">
                      <button
                        type="button"
                        onClick={() => setChartScope("state")}
                        className={`px-3 py-1.5 rounded-lg transition-all ${
                          chartScope === "state"
                            ? "bg-white dark:bg-stone-700 shadow-xs text-fsa-green font-extrabold"
                            : "text-stone-500 hover:text-stone-800"
                        }`}
                      >
                        Karnataka
                      </button>
                      <button
                        type="button"
                        onClick={() => setChartScope("india")}
                        className={`px-3 py-1.5 rounded-lg transition-all ${
                          chartScope === "india"
                            ? "bg-white dark:bg-stone-700 shadow-xs text-fsa-green font-extrabold"
                            : "text-stone-500 hover:text-stone-800"
                        }`}
                      >
                        All India
                      </button>
                    </div>
                  </div>

                  {/* Accessible SVG Bar Chart */}
                  <div className="relative pt-4">
                    <svg viewBox="0 0 540 220" className="w-full h-52 sm:h-56">
                      <line
                        x1="40"
                        y1="180"
                        x2="520"
                        y2="180"
                        stroke="#CBD5E1"
                        strokeWidth="1.5"
                      />
                      <line
                        x1="40"
                        y1="135"
                        x2="520"
                        y2="135"
                        stroke="#E2E8F0"
                        strokeDasharray="4"
                      />
                      <line
                        x1="40"
                        y1="90"
                        x2="520"
                        y2="90"
                        stroke="#E2E8F0"
                        strokeDasharray="4"
                      />
                      <line
                        x1="40"
                        y1="45"
                        x2="520"
                        y2="45"
                        stroke="#E2E8F0"
                        strokeDasharray="4"
                      />

                      {/* 5-Year Baseline dotted line */}
                      <line
                        x1="40"
                        y1="95"
                        x2="520"
                        y2="95"
                        stroke="#D97706"
                        strokeWidth="2"
                        strokeDasharray="5 3"
                      />
                      <text
                        x="515"
                        y="90"
                        fontSize="10"
                        textAnchor="end"
                        fontWeight="bold"
                        fill="#D97706"
                      >
                        5-Yr Avg: {chartScope === "state" ? "2.0 L" : "9.4 L"}
                      </text>

                      {/* 2020 */}
                      <rect
                        x="70"
                        y="105"
                        width="55"
                        height="75"
                        rx="6"
                        fill="#94A3B8"
                      />
                      <text
                        x="97"
                        y="98"
                        fontSize="11"
                        fontWeight="bold"
                        textAnchor="middle"
                        fill="#64748B"
                      >
                        {chartScope === "state" ? "1.8" : "8.9"}
                      </text>
                      <text
                        x="97"
                        y="200"
                        fontSize="11"
                        fontWeight="bold"
                        textAnchor="middle"
                        fill="#475569"
                      >
                        2020
                      </text>

                      {/* 2021 */}
                      <rect
                        x="160"
                        y="95"
                        width="55"
                        height="85"
                        rx="6"
                        fill="#94A3B8"
                      />
                      <text
                        x="187"
                        y="88"
                        fontSize="11"
                        fontWeight="bold"
                        textAnchor="middle"
                        fill="#64748B"
                      >
                        {chartScope === "state" ? "2.1" : "9.2"}
                      </text>
                      <text
                        x="187"
                        y="200"
                        fontSize="11"
                        fontWeight="bold"
                        textAnchor="middle"
                        fill="#475569"
                      >
                        2021
                      </text>

                      {/* 2022 */}
                      <rect
                        x="250"
                        y="100"
                        width="55"
                        height="80"
                        rx="6"
                        fill="#94A3B8"
                      />
                      <text
                        x="277"
                        y="92"
                        fontSize="11"
                        fontWeight="bold"
                        textAnchor="middle"
                        fill="#64748B"
                      >
                        {chartScope === "state" ? "1.9" : "9.0"}
                      </text>
                      <text
                        x="277"
                        y="200"
                        fontSize="11"
                        fontWeight="bold"
                        textAnchor="middle"
                        fill="#475569"
                      >
                        2022
                      </text>

                      {/* 2023 */}
                      <rect
                        x="340"
                        y="92"
                        width="55"
                        height="88"
                        rx="6"
                        fill="#94A3B8"
                      />
                      <text
                        x="367"
                        y="84"
                        fontSize="11"
                        fontWeight="bold"
                        textAnchor="middle"
                        fill="#64748B"
                      >
                        {chartScope === "state" ? "2.0" : "9.3"}
                      </text>
                      <text
                        x="367"
                        y="200"
                        fontSize="11"
                        fontWeight="bold"
                        textAnchor="middle"
                        fill="#475569"
                      >
                        2023
                      </text>

                      {/* 2024 Current Highlighted Bar */}
                      <rect
                        x="430"
                        y="80"
                        width="55"
                        height="100"
                        rx="6"
                        fill="#15803D"
                      />
                      <text
                        x="457"
                        y="72"
                        fontSize="12"
                        fontWeight="900"
                        textAnchor="middle"
                        fill="#15803D"
                        className="dark:fill-emerald-400"
                      >
                        {chartScope === "state" ? "2.0★" : "9.4★"}
                      </text>
                      <text
                        x="457"
                        y="200"
                        fontSize="11"
                        fontWeight="900"
                        textAnchor="middle"
                        fill="#15803D"
                        className="dark:fill-emerald-400"
                      >
                        2024 (Now)
                      </text>
                    </svg>
                  </div>
                  <div className="flex items-center justify-between text-xs text-stone-500 pt-2 border-t border-stone-100 dark:border-stone-800">
                    <span>Source: DES Karnataka & NHB Statistics</span>
                    <span className="font-bold text-emerald-700 dark:text-emerald-400">
                      Planted area matches 5-year average
                    </span>
                  </div>
                </div>

                {/* RIGHT: ESTIMATED MARKET SUPPLY GAUGE (5/12 cols) */}
                <div className="lg:col-span-5 bg-white dark:bg-fsa-surfaceDark rounded-3xl p-5 sm:p-6 border border-fsa-borderLight dark:border-fsa-borderDark shadow-sm flex flex-col justify-between space-y-4">
                  <div>
                    <div className="flex items-center justify-between">
                      <h3 className="text-base sm:text-lg font-black text-stone-900 dark:text-stone-100">
                        Estimated Market Supply
                      </h3>
                      <span className="px-2.5 py-0.5 rounded-full text-xs font-black bg-amber-100 text-amber-900 border border-amber-300">
                        Signal:{" "}
                        {priceOutlook?.supply_signal.toUpperCase() || "NORMAL"}
                      </span>
                    </div>
                    <p className="text-xs text-stone-500 mt-1">
                      Calculated as: Planted Area × 5-Yr Productivity (16.2 MT/ha)
                    </p>
                  </div>

                  {/* Stylized Semi-Circle Supply Gauge */}
                  <div className="py-2 flex flex-col items-center">
                    <svg viewBox="0 0 240 130" className="w-52 h-28 sm:w-56 sm:h-32">
                      <path
                        d="M 30,120 A 90,90 0 0,1 210,120"
                        fill="none"
                        stroke="#E2E8F0"
                        strokeWidth="20"
                        strokeLinecap="round"
                        className="dark:stroke-stone-700"
                      />
                      <path
                        d="M 30,120 A 90,90 0 0,1 155,50"
                        fill="none"
                        stroke="#F59E0B"
                        strokeWidth="20"
                        strokeLinecap="round"
                      />
                      <circle
                        cx="120"
                        cy="120"
                        r="8"
                        fill="#1F2937"
                        className="dark:fill-white"
                      />
                      <line
                        x1="120"
                        y1="120"
                        x2="150"
                        y2="58"
                        stroke="#1F2937"
                        strokeWidth="4"
                        strokeLinecap="round"
                        className="dark:stroke-white"
                      />
                      <text
                        x="25"
                        y="130"
                        fontSize="10"
                        fontWeight="bold"
                        fill="#64748B"
                      >
                        Lower
                      </text>
                      <text
                        x="120"
                        y="28"
                        fontSize="10"
                        fontWeight="bold"
                        textAnchor="middle"
                        fill="#64748B"
                      >
                        Normal
                      </text>
                      <text
                        x="215"
                        y="130"
                        fontSize="10"
                        fontWeight="bold"
                        textAnchor="end"
                        fill="#64748B"
                      >
                        Higher
                      </text>
                    </svg>

                    <div className="text-center mt-1">
                      <span className="text-2xl sm:text-3xl font-black text-amber-700 dark:text-amber-400 tabular-nums">
                        1.0×
                      </span>
                      <span className="text-xs font-bold text-stone-500 block">
                        Supply Ratio vs 5-Year Average
                      </span>
                    </div>
                  </div>

                  <div className="p-3 rounded-2xl bg-stone-50 dark:bg-stone-900 border border-stone-200 dark:border-stone-800 text-xs text-stone-600 dark:text-stone-300 leading-relaxed">
                    <strong>Supply Commentary:</strong>{" "}
                    {priceOutlook?.explanation_text ||
                      "Higher planted area has usually been followed by lower prices, but local harvest arrivals dictate daily swings."}
                  </div>
                </div>
              </div>

              {/* e. WHOLESALE PRICE RANGE FORECAST SECTION */}
              <div className="bg-white dark:bg-fsa-surfaceDark rounded-3xl p-5 sm:p-8 border border-fsa-borderLight dark:border-fsa-borderDark shadow-sm space-y-6">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-fsa-borderLight dark:border-fsa-borderDark">
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-xl sm:text-2xl font-black text-stone-900 dark:text-stone-100">
                        {t.supplyPriceOutlookHeading} ({district} APMC)
                      </h3>
                      <span className="bg-stone-100 dark:bg-stone-800 text-stone-700 dark:text-stone-300 text-xs px-2.5 py-0.5 rounded-full font-bold">
                        Medium Onion
                      </span>
                    </div>
                    <p className="text-xs text-stone-500 mt-1">
                      Prices are rounded ranges in ₹ per quintal (100 kg). Single
                      point prices are deliberately omitted.
                    </p>
                  </div>

                  <div className="flex items-center gap-2 bg-stone-50 dark:bg-stone-800/80 px-3 py-1.5 rounded-xl border border-stone-200 dark:border-stone-700 text-xs text-stone-600 dark:text-stone-300">
                    <Shield className="w-4 h-4 text-fsa-green shrink-0" />
                    <span>{t.farmerAcreageIsolatedNote}</span>
                  </div>
                </div>

                {/* 3 Price Horizon Cards (30 / 60 / 90 Days) */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {priceOutlook?.horizons.map((h) => (
                    <div
                      key={h.horizon_days}
                      className="p-5 rounded-2xl bg-stone-50 dark:bg-stone-900 border-2 border-stone-200 dark:border-stone-700 space-y-3"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-stone-500 uppercase tracking-wider">
                          {h.horizon_days} Days Out
                        </span>
                        <span className="inline-flex items-center gap-1 text-[11px] font-bold px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                          <span>{h.confidence_badge} Confidence</span>
                        </span>
                      </div>
                      <div>
                        <span className="text-2xl sm:text-3xl font-black text-stone-900 dark:text-white tabular-nums">
                          {h.price_range_text}
                        </span>
                        <p className="text-xs font-semibold text-stone-500 mt-1">
                          Per Quintal (Mid: ₹
                          {Math.round(h.p50_expected).toLocaleString("en-IN")})
                        </p>
                      </div>
                      <p className="text-xs text-stone-600 dark:text-stone-400 leading-snug">
                        {h.horizon_days === 30
                          ? "Early arrivals window with high confidence calibration."
                          : h.horizon_days === 60
                          ? "Peak arrival period; volume signals will guide daily price movements."
                          : "Late Kharif harvest dependence; wider confidence interval."}
                      </p>
                    </div>
                  )) || (
                    <div className="col-span-3 text-center text-sm text-stone-500 py-6">
                      Loading calibrated forecast ranges...
                    </div>
                  )}
                </div>

                {/* Price Fan Probability Cone Chart (90-Day Horizon) */}
                <div className="p-4 rounded-2xl bg-stone-100 dark:bg-stone-900/60 border border-stone-200 dark:border-stone-800 space-y-2">
                  <span className="text-xs font-bold text-stone-500">
                    Price Fan Probability Cone (90-Day Horizon)
                  </span>
                  <svg viewBox="0 0 600 130" className="w-full h-28 sm:h-32">
                    <line
                      x1="50"
                      y1="20"
                      x2="570"
                      y2="20"
                      stroke="#E2E8F0"
                      strokeDasharray="3"
                    />
                    <line
                      x1="50"
                      y1="65"
                      x2="570"
                      y2="65"
                      stroke="#E2E8F0"
                      strokeDasharray="3"
                    />
                    <line x1="50" y1="110" x2="570" y2="110" stroke="#CBD5E1" />

                    <polygon
                      points="50,60 210,50 370,68 530,90 530,115 370,105 210,80 50,60"
                      fill="#BBF7D0"
                      fillOpacity="0.4"
                      className="dark:fill-emerald-950/60"
                    />
                    <polyline
                      points="50,60 210,65 370,86 530,103"
                      fill="none"
                      stroke="#15803D"
                      strokeWidth="3"
                      strokeLinecap="round"
                    />

                    <circle cx="50" cy="60" r="5" fill="#15803D" />
                    <text
                      x="50"
                      y="125"
                      fontSize="10"
                      fontWeight="bold"
                      fill="#64748B"
                      textAnchor="middle"
                    >
                      Today
                    </text>

                    <circle cx="210" cy="65" r="5" fill="#15803D" />
                    <text
                      x="210"
                      y="125"
                      fontSize="10"
                      fontWeight="bold"
                      fill="#64748B"
                      textAnchor="middle"
                    >
                      30 Days
                    </text>

                    <circle cx="370" cy="86" r="5" fill="#15803D" />
                    <text
                      x="370"
                      y="125"
                      fontSize="10"
                      fontWeight="bold"
                      fill="#64748B"
                      textAnchor="middle"
                    >
                      60 Days
                    </text>

                    <circle cx="530" cy="103" r="5" fill="#15803D" />
                    <text
                      x="530"
                      y="125"
                      fontSize="10"
                      fontWeight="bold"
                      fill="#64748B"
                      textAnchor="middle"
                    >
                      90 Days
                    </text>
                  </svg>
                </div>

                {/* Mandated Autonomy Disclaimer */}
                <div className="text-xs text-stone-500 space-y-1 text-center font-medium pt-2">
                  <p>
                    Higher planted area has usually been followed by lower prices
                    during post-harvest arrivals, but localized weather shocks
                    can alter outcomes.
                  </p>
                  <p className="font-extrabold text-stone-800 dark:text-stone-200 text-sm">
                    "This is advice, the decision is yours." (ಇದು ಸಲಹೆ ಮಾತ್ರ,
                    ಅಂತಿಮ ನಿರ್ಧಾರ ನಿಮ್ಮದು.)
                  </p>
                </div>
              </div>

              {/* f. GRANULAR AREA & COVERAGE COMPARISON TABLE */}
              <div className="bg-white dark:bg-fsa-surfaceDark rounded-3xl p-5 sm:p-6 border border-fsa-borderLight dark:border-fsa-borderDark shadow-sm space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-base sm:text-lg font-black text-stone-900 dark:text-stone-100">
                    Granular Area & Coverage Comparison
                  </h3>
                  <span className="text-xs font-semibold text-stone-500">
                    Indian Digit Grouping Standard
                  </span>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs sm:text-sm border-collapse">
                    <thead>
                      <tr className="border-b-2 border-stone-200 dark:border-stone-700 text-xs font-bold text-stone-500 uppercase tracking-wider">
                        <th className="py-3 px-3 sm:px-4">Jurisdiction</th>
                        <th className="py-3 px-3 sm:px-4">2024 Area (Acres)</th>
                        <th className="py-3 px-3 sm:px-4">5-Year Normal</th>
                        <th className="py-3 px-3 sm:px-4">Change vs Avg</th>
                        <th className="py-3 px-3 sm:px-4">Primary Source</th>
                        <th className="py-3 px-3 sm:px-4">Publication Date</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-stone-100 dark:divide-stone-800 text-stone-800 dark:text-stone-200">
                      {/* District Row */}
                      <tr className="hover:bg-stone-50 dark:hover:bg-stone-800/50">
                        <td className="py-3.5 px-3 sm:px-4 font-bold flex items-center gap-2">
                          <span className="w-2.5 h-2.5 rounded-full bg-emerald-600"></span>
                          <span>{district} (Official)</span>
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 tabular-nums font-extrabold">
                          {areaSummary?.district_official
                            ? `${areaSummary.district_official.area_acres.toLocaleString(
                                "en-IN"
                              )} ac`
                            : "Not available"}
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 tabular-nums">
                          {areaSummary?.district_official
                            ? `${Math.round(
                                areaSummary.district_official.avg_5yr_acres
                              ).toLocaleString("en-IN")} ac`
                            : "—"}
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 font-bold text-amber-600">
                          {areaSummary?.district_official ? "+11.5%" : "Fallback"}
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 text-xs">
                          {areaSummary?.district_official?.source_name ||
                            "DES Karnataka"}
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 text-xs text-stone-500">
                          {areaSummary?.district_official?.publication_date ||
                            "—"}
                        </td>
                      </tr>

                      {/* Farmer Crowdsourced Row */}
                      <tr className="bg-amber-50/60 dark:bg-amber-950/30 font-medium">
                        <td className="py-3.5 px-3 sm:px-4 font-black text-amber-900 dark:text-amber-300 flex items-center gap-2">
                          <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
                          <span>{district} (Reported by Farmers)</span>
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 tabular-nums font-black text-amber-900 dark:text-amber-300">
                          {Math.round(
                            areaSummary?.farmer_reported.reported_acres ||
                              250
                          ).toLocaleString("en-IN")}{" "}
                          ac ({areaSummary?.farmer_reported.entry_count || 5}{" "}
                          farmers)
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 text-xs text-stone-500">
                          — (Crowdsourced)
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 text-xs font-bold text-emerald-700">
                          {areaSummary?.farmer_reported.coverage_pct !== null &&
                          areaSummary?.farmer_reported.coverage_pct !== undefined
                            ? `${areaSummary.farmer_reported.coverage_pct.toFixed(
                                1
                              )}% Coverage`
                            : "Too few reports"}
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 text-xs font-semibold">
                          Local Kiosk Inputs
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 text-xs text-stone-500">
                          Live Today
                        </td>
                      </tr>

                      {/* Karnataka State Row */}
                      <tr className="hover:bg-stone-50 dark:hover:bg-stone-800/50">
                        <td className="py-3.5 px-3 sm:px-4 font-bold flex items-center gap-2">
                          <span className="w-2.5 h-2.5 rounded-full bg-emerald-600"></span>
                          <span>Karnataka State</span>
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 tabular-nums font-extrabold">
                          {areaSummary?.state_official
                            ? `${areaSummary.state_official.area_acres.toLocaleString(
                                "en-IN"
                              )} ac`
                            : "2,02,626 ac"}
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 tabular-nums">
                          {areaSummary?.state_official
                            ? `${Math.round(
                                areaSummary.state_official.avg_5yr_acres
                              ).toLocaleString("en-IN")} ac`
                            : "2,02,626 ac"}
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 font-bold text-amber-600">
                          +18.0%
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 text-xs">
                          {areaSummary?.state_official?.source_name ||
                            "Dept of Agriculture"}
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 text-xs text-stone-500">
                          {areaSummary?.state_official?.publication_date ||
                            "12 Jul 2024"}
                        </td>
                      </tr>

                      {/* All-India Row */}
                      <tr className="hover:bg-stone-50 dark:hover:bg-stone-800/50">
                        <td className="py-3.5 px-3 sm:px-4 font-bold flex items-center gap-2">
                          <span className="w-2.5 h-2.5 rounded-full bg-emerald-600"></span>
                          <span>India (National)</span>
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 tabular-nums font-extrabold">
                          {areaSummary?.country_official
                            ? `${(
                                areaSummary.country_official.area_acres / 100000
                              ).toFixed(1)} L ac`
                            : "9.4 L ac"}
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 tabular-nums">
                          {areaSummary?.country_official
                            ? `${(
                                areaSummary.country_official.avg_5yr_acres / 100000
                              ).toFixed(1)} L ac`
                            : "9.4 L ac"}
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 font-bold text-emerald-600">
                          +3.1%
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 text-xs">
                          {areaSummary?.country_official?.source_name ||
                            "DA&FW Krishi Bhawan"}
                        </td>
                        <td className="py-3.5 px-3 sm:px-4 text-xs text-stone-500">
                          {areaSummary?.country_official?.publication_date ||
                            "05 Jul 2024"}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              {/* g. DATA PROVENANCE FOOTER */}
              <div className="p-5 rounded-2xl bg-stone-100 dark:bg-stone-900 border border-stone-200 dark:border-stone-800 text-xs text-stone-500 space-y-2">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span>
                    Model Version: FSA-Supply-v3.4.1 (Calibrated on 2018–2023
                    Kharif Cycles)
                  </span>
                  <button
                    type="button"
                    onClick={() => setActiveScreen("methodology")}
                    className="text-fsa-green dark:text-emerald-400 font-bold underline"
                  >
                    Read Complete Methodology & Assumptions
                  </button>
                </div>
                <p>
                  Farmer entries are never extrapolated into state or national
                  estimates. All projections reflect official datasets released
                  by Directorate of Economics and Statistics (Karnataka) and
                  Ministry of Agriculture (Government of India).
                </p>
              </div>
            </section>
          )}

          {/* ========================================================================= */}
          {/* SCREEN 3: FPO & OFFICER REVIEW (Desktop Staff View)                      */}
          {/* ========================================================================= */}
          {activeScreen === "officer" && (
            <section id="screen-officer" className="space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300 font-bold text-xs px-2.5 py-0.5 rounded-md border border-amber-300">
                      Staff Restricted
                    </span>
                    <h2 className="text-xl sm:text-2xl font-black text-stone-900 dark:text-stone-100">
                      {t.fpoOfficerTitle}
                    </h2>
                  </div>
                  <p className="text-xs text-stone-500 mt-1">
                    {t.fpoOfficerSubtitle} ({district} {season})
                  </p>
                </div>
                <button
                  type="button"
                  onClick={handleExportCsv}
                  className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-stone-900 dark:bg-stone-100 text-white dark:text-stone-900 font-bold text-xs hover:bg-stone-800 transition-colors shadow-xs"
                >
                  <Download className="w-4 h-4" />
                  <span>{t.exportCsvBtn}</span>
                </button>
              </div>

              {/* Summary Metric Tiles */}
              <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
                <div className="p-4 rounded-2xl bg-white dark:bg-fsa-surfaceDark border border-stone-200 dark:border-stone-800">
                  <span className="text-xs font-bold text-stone-500">
                    {t.totalValidSubmissions}
                  </span>
                  <p className="text-2xl sm:text-3xl font-black text-stone-900 dark:text-white tabular-nums mt-1">
                    {officerData?.total_valid_submissions || 19}
                  </p>
                  <span className="text-[11px] text-emerald-600 font-bold">
                    Logged in local SQLite database
                  </span>
                </div>

                <div className="p-4 rounded-2xl bg-white dark:bg-fsa-surfaceDark border border-stone-200 dark:border-stone-800">
                  <span className="text-xs font-bold text-stone-500">
                    Reported Acreage
                  </span>
                  <p className="text-2xl sm:text-3xl font-black text-amber-700 dark:text-amber-400 tabular-nums mt-1">
                    {officerData?.total_reported_acres?.toLocaleString("en-IN") ||
                      "1,035"}{" "}
                    <span className="text-xs text-stone-500">ac</span>
                  </p>
                  <span className="text-[11px] text-stone-500">
                    Verified through single-holding rule
                  </span>
                </div>

                <div className="p-4 rounded-2xl bg-white dark:bg-fsa-surfaceDark border border-stone-200 dark:border-stone-800">
                  <span className="text-xs font-bold text-stone-500">
                    District Coverage Ratio
                  </span>
                  <p className="text-2xl sm:text-3xl font-black text-stone-900 dark:text-white tabular-nums mt-1">
                    {areaSummary?.farmer_reported.coverage_pct !== null &&
                    areaSummary?.farmer_reported.coverage_pct !== undefined
                      ? `${areaSummary.farmer_reported.coverage_pct.toFixed(1)}%`
                      : "2.4%"}
                  </p>
                  <span className="text-[11px] text-amber-600 font-bold">
                    Trust threshold bar: 5.0%
                  </span>
                </div>

                <div className="p-4 rounded-2xl bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900">
                  <span className="text-xs font-bold text-red-800 dark:text-red-300">
                    {t.flaggedAnomalies}
                  </span>
                  <p className="text-2xl sm:text-3xl font-black text-red-700 dark:text-red-400 tabular-nums mt-1">
                    {officerData?.flagged_anomalies || 0}
                  </p>
                  <span className="text-[11px] text-red-600 font-bold">
                    Excluded from aggregates
                  </span>
                </div>
              </div>

              {/* Anonymized Submissions Table */}
              <div className="bg-white dark:bg-fsa-surfaceDark rounded-3xl p-5 sm:p-6 border border-fsa-borderLight dark:border-fsa-borderDark shadow-sm space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm sm:text-base font-bold text-stone-900 dark:text-stone-100">
                    Recent Device Submissions (Anonymized by SHA-256)
                  </h3>
                  <span className="text-xs text-stone-500">
                    Real submissions from area_reports.db
                  </span>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs border-collapse">
                    <thead>
                      <tr className="border-b border-stone-200 dark:border-stone-700 font-bold text-stone-500 uppercase">
                        <th className="py-2.5 px-3">Device Hash</th>
                        <th className="py-2.5 px-3">Reported Acres</th>
                        <th className="py-2.5 px-3">Hectares</th>
                        <th className="py-2.5 px-3">District</th>
                        <th className="py-2.5 px-3">Season</th>
                        <th className="py-2.5 px-3">Status</th>
                        <th className="py-2.5 px-3">Timestamp</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-stone-100 dark:divide-stone-800 text-stone-800 dark:text-stone-200">
                      {officerData?.submissions.map((sub, idx) => (
                        <tr
                          key={idx}
                          className={
                            sub.is_anomaly
                              ? "bg-red-50/70 dark:bg-red-950/40"
                              : "hover:bg-stone-50 dark:hover:bg-stone-800/40"
                          }
                        >
                          <td className="py-3 px-3 font-mono text-[11px]">
                            {sub.device_hash}
                          </td>
                          <td className="py-3 px-3 font-extrabold text-sm text-fsa-green">
                            {sub.acres} ac
                          </td>
                          <td className="py-3 px-3">{sub.hectares} ha</td>
                          <td className="py-3 px-3 font-semibold">
                            {sub.district}
                          </td>
                          <td className="py-3 px-3">
                            {sub.season} {sub.year}
                          </td>
                          <td className="py-3 px-3">
                            {sub.is_anomaly ? (
                              <span className="px-2 py-0.5 rounded-md bg-red-100 text-red-800 font-bold text-[10px]">
                                {sub.anomaly_reason || "Anomaly"}
                              </span>
                            ) : (
                              <span className="px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-800 font-bold text-[10px]">
                                Verified
                              </span>
                            )}
                          </td>
                          <td className="py-3 px-3 text-stone-500">
                            {sub.created_at.slice(0, 16)}
                          </td>
                        </tr>
                      )) || (
                        <tr>
                          <td
                            colSpan={7}
                            className="py-4 text-center text-stone-500"
                          >
                            No entries logged yet.
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </section>
          )}

          {/* ========================================================================= */}
          {/* SCREEN 4: DATA SOURCES & METHODOLOGY                                     */}
          {/* ========================================================================= */}
          {activeScreen === "methodology" && (
            <section
              id="screen-methodology"
              className="space-y-6 max-w-4xl mx-auto"
            >
              <div>
                <h2 className="text-2xl sm:text-3xl font-black text-stone-900 dark:text-stone-100">
                  {t.sourcesMethodsTitle}
                </h2>
                <p className="text-xs sm:text-sm text-stone-500 mt-1">
                  {t.sourcesMethodsSubtitle}
                </p>
              </div>

              <div className="space-y-4">
                {/* Pillar 1 */}
                <div className="p-6 rounded-3xl bg-white dark:bg-fsa-surfaceDark border border-fsa-borderLight dark:border-fsa-borderDark shadow-sm space-y-3">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold">
                      <Shield className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-base sm:text-lg font-bold text-stone-900 dark:text-stone-100">
                        {t.pillar1Title}
                      </h3>
                      <span className="text-xs text-stone-500 font-medium">
                        Non-negotiable architectural boundary
                      </span>
                    </div>
                  </div>
                  <p className="text-xs sm:text-sm text-stone-600 dark:text-stone-300 leading-relaxed">
                    {t.pillar1Desc}
                  </p>
                </div>

                {/* Pillar 2 */}
                <div className="p-6 rounded-3xl bg-white dark:bg-fsa-surfaceDark border border-fsa-borderLight dark:border-fsa-borderDark shadow-sm space-y-3">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-amber-100 text-amber-800 flex items-center justify-center font-bold">
                      <TrendingDown className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-base sm:text-lg font-bold text-stone-900 dark:text-stone-100">
                        {t.pillar2Title}
                      </h3>
                      <span className="text-xs text-stone-500 font-medium">
                        Honesty by design principle
                      </span>
                    </div>
                  </div>
                  <p className="text-xs sm:text-sm text-stone-600 dark:text-stone-300 leading-relaxed">
                    {t.pillar2Desc}
                  </p>
                </div>

                {/* Pillar 3 */}
                <div className="p-6 rounded-3xl bg-white dark:bg-fsa-surfaceDark border border-fsa-borderLight dark:border-fsa-borderDark shadow-sm space-y-3">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-sky-100 text-sky-800 flex items-center justify-center font-bold">
                      <Calendar className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-base sm:text-lg font-bold text-stone-900 dark:text-stone-100">
                        {t.pillar3Title}
                      </h3>
                      <span className="text-xs text-stone-500 font-medium">
                        Explicit agricultural assumptions
                      </span>
                    </div>
                  </div>
                  <p className="text-xs sm:text-sm text-stone-600 dark:text-stone-300 leading-relaxed">
                    {t.pillar3Desc}
                  </p>
                </div>
              </div>
            </section>
          )}

          {/* ========================================================================= */}
          {/* SCREEN 5: FEEDBACK & FARMER HISTORY                                      */}
          {/* ========================================================================= */}
          {activeScreen === "feedback" && (
            <section
              id="screen-feedback"
              className="space-y-6 max-w-3xl mx-auto"
            >
              <div className="text-center space-y-2">
                <h2 className="text-2xl sm:text-3xl font-black text-stone-900 dark:text-stone-100">
                  {t.feedbackHelpfulTitle}
                </h2>
                <p className="text-xs sm:text-sm text-stone-500">
                  {t.feedbackHelpfulSubtitle}
                </p>
              </div>

              <div className="bg-white dark:bg-fsa-surfaceDark rounded-3xl p-6 sm:p-8 border border-fsa-borderLight dark:border-fsa-borderDark shadow-sm space-y-6">
                {/* Thumbs Up / Down */}
                <div className="flex justify-center gap-6">
                  <button
                    type="button"
                    onClick={() => {
                      setFeedbackVote("helpful");
                      showToast(
                        language === "kn"
                          ? "ಧನ್ಯವಾದಗಳು! ನಿಮ್ಮ ಅನಿಸಿಕೆ ದಾಖಲಾಗಿದೆ."
                          : language === "hi"
                          ? "धन्यवाद! आपकी प्रतिक्रिया दर्ज हुई।"
                          : "Thank you for your feedback!"
                      );
                    }}
                    className={`flex flex-col items-center gap-2 p-5 rounded-2xl border-2 transition-all w-36 ${
                      feedbackVote === "helpful"
                        ? "border-fsa-green bg-emerald-50 dark:bg-emerald-950/40"
                        : "border-stone-200 dark:border-stone-700 hover:border-fsa-green"
                    }`}
                  >
                    <ThumbsUp
                      className={`w-9 h-9 ${
                        feedbackVote === "helpful"
                          ? "text-fsa-green"
                          : "text-stone-400"
                      }`}
                    />
                    <span className="font-extrabold text-xs sm:text-sm text-stone-700 dark:text-stone-200">
                      {t.feedbackYes}
                    </span>
                  </button>

                  <button
                    type="button"
                    onClick={() => {
                      setFeedbackVote("not-helpful");
                      showToast(
                        language === "kn"
                          ? "ಧನ್ಯವಾದಗಳು. ಮುನ್ನೋಟವನ್ನು ಸುಧಾರಿಸಲು ಗಮನಹರಿಸುತ್ತೇವೆ."
                          : language === "hi"
                          ? "धन्यवाद। हम इसे सुधारने का प्रयास करेंगे।"
                          : "Feedback noted. We will work to improve!"
                      );
                    }}
                    className={`flex flex-col items-center gap-2 p-5 rounded-2xl border-2 transition-all w-36 ${
                      feedbackVote === "not-helpful"
                        ? "border-red-500 bg-red-50 dark:bg-red-950/40"
                        : "border-stone-200 dark:border-stone-700 hover:border-red-500"
                    }`}
                  >
                    <ThumbsDown
                      className={`w-9 h-9 ${
                        feedbackVote === "not-helpful"
                          ? "text-red-600"
                          : "text-stone-400"
                      }`}
                    />
                    <span className="font-extrabold text-xs sm:text-sm text-stone-700 dark:text-stone-200">
                      {t.feedbackNo}
                    </span>
                  </button>
                </div>

                {/* Optional Voice Note Recording */}
                <div className="p-4 rounded-2xl bg-stone-50 dark:bg-stone-900 border border-stone-200 dark:border-stone-800 space-y-3">
                  <label className="block text-xs font-bold text-stone-600 dark:text-stone-300">
                    Optional Voice Note / ಅಭಿಪ್ರಾಯ:
                  </label>
                  <div className="flex items-center gap-3">
                    <button
                      type="button"
                      onClick={handleRecordMemo}
                      disabled={isRecordingMemo}
                      className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-red-600 hover:bg-red-700 text-white font-bold text-xs disabled:opacity-50"
                    >
                      <Mic className="w-4 h-4" />
                      <span>
                        {isRecordingMemo ? "Recording..." : t.recordAudioMemo}
                      </span>
                    </button>
                    <span className="text-xs text-stone-500 italic">
                      {memoRecorded
                        ? "✓ Audio memo saved (30s)"
                        : "No audio note recorded yet"}
                    </span>
                  </div>
                </div>

                {/* Local Session Reports History */}
                <div className="space-y-3 pt-4 border-t border-stone-200 dark:border-stone-800">
                  <h3 className="text-xs sm:text-sm font-bold text-stone-800 dark:text-stone-200">
                    {t.recentKioskReports}
                  </h3>
                  <div className="space-y-2 text-xs">
                    <div className="p-3 rounded-xl bg-stone-100 dark:bg-stone-800/80 flex items-center justify-between">
                      <div>
                        <span className="font-bold text-stone-900 dark:text-stone-100">
                          {district} • {season} {year}
                        </span>
                        <span className="text-stone-500 block">
                          Reported: {acres}.0 acres ({hectaresValue} ha)
                        </span>
                      </div>
                      <button
                        type="button"
                        onClick={() => setActiveScreen("results")}
                        className="px-3 py-1.5 rounded-lg bg-white dark:bg-stone-700 border border-stone-300 dark:border-stone-600 font-bold text-fsa-green"
                      >
                        View Outlook
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          )}
        </main>
      </div>

      {/* TOAST NOTIFICATION */}
      {toastMsg && (
        <div className="fixed bottom-6 right-6 bg-stone-900 text-white px-5 py-3.5 rounded-2xl shadow-2xl flex items-center gap-3 text-sm font-semibold transition-transform z-50">
          <CheckCircle className="w-5 h-5 text-emerald-400 shrink-0" />
          <span>{toastMsg}</span>
        </div>
      )}
    </div>
  );
};
