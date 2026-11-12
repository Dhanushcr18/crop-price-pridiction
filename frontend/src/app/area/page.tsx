"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { CropAreaView } from "../../components/CropAreaView";
import { Language } from "../../types/api";

export default function AreaPage() {
  const router = useRouter();
  const [language, setLanguage] = useState<Language>("kn");

  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedLang = localStorage.getItem("fsa_lang") as Language;
      if (savedLang && ["en", "hi", "kn"].includes(savedLang)) {
        setLanguage(savedLang);
      }
    }
  }, []);

  const handleLanguageChange = (newLang: Language) => {
    setLanguage(newLang);
    if (typeof window !== "undefined") {
      localStorage.setItem("fsa_lang", newLang);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-fsa-cream dark:bg-fsa-creamDark text-fsa-textMainLight dark:text-fsa-textMainDark">
      <CropAreaView
        language={language}
        onLanguageChange={handleLanguageChange}
        onBackToAdvisor={() => router.push("/")}
        isStandalone={true}
      />
    </div>
  );
}
