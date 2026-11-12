"use client";

import React, { useState, useEffect } from "react";
import { Header } from "../../components/Header";
import { BottomNav } from "../../components/BottomNav";
import { Button } from "../../components/ui/Button";
import { Toast } from "../../components/ui/Toast";
import { Language, HealthResponse } from "../../types/api";
import { translations } from "../../i18n/translations";
import { getHealth } from "../../lib/api";

export default function HelpPage() {
  const [language, setLanguage] = useState<Language>("kn");
  const t = translations[language];

  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [name, setName] = useState("");
  const [village, setVillage] = useState("");
  const [feedback, setFeedback] = useState("");
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [toastMessage, setToastMessage] = useState("");
  const [toastVisible, setToastVisible] = useState(false);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedLang = localStorage.getItem("fsa_lang") as Language;
      if (savedLang && ["en", "hi", "kn"].includes(savedLang)) {
        setLanguage(savedLang);
      }
    }

    getHealth()
      .then((h) => setHealth(h))
      .catch((e) => console.warn(e));
  }, []);

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
  };

  const handleSubmitFeedback = (e: React.FormEvent) => {
    e.preventDefault();
    if (!feedback.trim()) return;

    if (typeof window !== "undefined") {
      const existing = JSON.parse(
        localStorage.getItem("fsa_feedback_log") || "[]"
      );
      existing.push({
        name,
        village,
        feedback,
        date: new Date().toISOString(),
      });
      localStorage.setItem("fsa_feedback_log", JSON.stringify(existing));
    }

    setIsSubmitted(true);
    setName("");
    setVillage("");
    setFeedback("");
    showToast(t.feedbackThankYou);
  };

  return (
    <div className="min-h-screen flex flex-col bg-cream dark:bg-cream-dark text-ink dark:text-ink-dark">
      <Header
        language={language}
        onLanguageChange={handleLanguageChange}
        health={health}
      />

      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6 min-w-0">
        <div className="space-y-1 pb-2 border-b border-divider/60 dark:border-divider-dark">
          <h2 className="text-xl sm:text-2xl font-black text-ink dark:text-ink-dark">
            {t.helpTitle}
          </h2>
          <p className="text-xs sm:text-sm text-ink-muted dark:text-ink-muted-dark">
            {t.helpSubtitle}
          </p>
        </div>

        {/* 1. 3-STEP EXPLAINER */}
        <section className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-5 shadow-card space-y-3">
          <h3 className="font-extrabold text-base text-ink dark:text-ink-dark">
            {t.howItWorksHeading}
          </h3>

          <div className="space-y-2.5 text-xs sm:text-sm text-ink-muted dark:text-ink-muted-dark leading-relaxed">
            <div className="p-3 rounded-2xl bg-surface-low dark:bg-surface-low-dark border border-divider/60 dark:border-divider-dark flex items-start gap-2.5">
              <span className="w-6 h-6 rounded-full bg-primary text-white flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">
                1
              </span>
              <p className="text-ink dark:text-ink-dark font-medium">{t.step1Text}</p>
            </div>

            <div className="p-3 rounded-2xl bg-surface-low dark:bg-surface-low-dark border border-divider/60 dark:border-divider-dark flex items-start gap-2.5">
              <span className="w-6 h-6 rounded-full bg-primary text-white flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">
                2
              </span>
              <p className="text-ink dark:text-ink-dark font-medium">{t.step2Text}</p>
            </div>

            <div className="p-3 rounded-2xl bg-surface-low dark:bg-surface-low-dark border border-divider/60 dark:border-divider-dark flex items-start gap-2.5">
              <span className="w-6 h-6 rounded-full bg-primary text-white flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">
                3
              </span>
              <p className="text-ink dark:text-ink-dark font-medium">{t.step3Text}</p>
            </div>
          </div>
        </section>

        {/* 2. BOUNDARIES & FARMER SOVEREIGNTY */}
        <section className="bg-primary-tint dark:bg-primary/10 border border-primary/20 rounded-3xl p-5 space-y-2">
          <h3 className="font-extrabold text-base text-primary dark:text-primary-dark flex items-center gap-2">
            <span className="material-symbols-outlined text-[20px]">
              verified_user
            </span>
            <span>{t.boundariesHeading}</span>
          </h3>
          <p className="text-xs sm:text-sm text-ink dark:text-ink-dark leading-relaxed font-medium">
            {t.boundariesBody}
          </p>
        </section>

        {/* 3. FREQUENTLY ASKED QUESTIONS */}
        <section className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-5 shadow-card space-y-3">
          <h3 className="font-extrabold text-base text-ink dark:text-ink-dark">
            {t.faqHeading}
          </h3>

          <div className="space-y-3 text-xs sm:text-sm divide-y divide-divider/60 dark:divide-divider-dark">
            <div className="pt-2 space-y-1">
              <h4 className="font-bold text-ink dark:text-ink-dark">{t.faq1Q}</h4>
              <p className="text-ink-muted dark:text-ink-muted-dark leading-relaxed">
                {t.faq1A}
              </p>
            </div>

            <div className="pt-3 space-y-1">
              <h4 className="font-bold text-ink dark:text-ink-dark">{t.faq2Q}</h4>
              <p className="text-ink-muted dark:text-ink-muted-dark leading-relaxed">
                {t.faq2A}
              </p>
            </div>
          </div>

          {/* Call a helper button (56px) */}
          <div className="pt-3">
            <a
              href="tel:18001801551"
              className="w-full min-h-[56px] rounded-2xl bg-surface-low dark:bg-surface-low-dark border border-divider dark:border-divider-dark text-ink dark:text-ink-dark font-bold text-sm flex items-center justify-center gap-2 hover:bg-surface-high transition-colors select-none touch-press"
            >
              <span className="material-symbols-outlined text-primary text-[22px]">
                support_agent
              </span>
              <span>{t.callHelperBtn} (1800-180-1551)</span>
            </a>
          </div>
        </section>

        {/* 4. FIELD FEEDBACK FORM */}
        <section className="bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-3xl p-5 shadow-card space-y-3">
          <h3 className="font-extrabold text-base text-ink dark:text-ink-dark">
            {t.fieldFeedbackHeading}
          </h3>

          <form onSubmit={handleSubmitFeedback} className="space-y-3">
            <input
              type="text"
              placeholder={t.farmerNamePlaceholder}
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full h-12 px-4 rounded-xl bg-surface-low dark:bg-surface-low-dark border border-divider text-sm font-semibold text-ink dark:text-ink-dark focus:outline-none focus:ring-2 focus:ring-primary"
            />

            <input
              type="text"
              placeholder={t.villagePlaceholder}
              value={village}
              onChange={(e) => setVillage(e.target.value)}
              className="w-full h-12 px-4 rounded-xl bg-surface-low dark:bg-surface-low-dark border border-divider text-sm font-semibold text-ink dark:text-ink-dark focus:outline-none focus:ring-2 focus:ring-primary"
            />

            <textarea
              rows={3}
              placeholder={t.notesPlaceholder}
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              className="w-full p-4 rounded-xl bg-surface-low dark:bg-surface-low-dark border border-divider text-sm font-semibold text-ink dark:text-ink-dark focus:outline-none focus:ring-2 focus:ring-primary"
            />

            <Button variant="primary" size="touch" type="submit">
              <span>{t.sendFeedbackBtn}</span>
              <span className="material-symbols-outlined ml-1.5 text-[20px]">
                send
              </span>
            </Button>

            {isSubmitted && (
              <p className="text-xs font-bold text-primary dark:text-primary-dark text-center pt-1">
                ✓ {t.feedbackThankYou}
              </p>
            )}
          </form>
        </section>
      </main>

      <BottomNav language={language} />
      <Toast message={toastMessage} visible={toastVisible} />
    </div>
  );
}

