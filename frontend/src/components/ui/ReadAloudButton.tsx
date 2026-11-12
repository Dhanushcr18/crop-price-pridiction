import React, { useState, useEffect } from "react";
import { Language } from "../../types/api";

export interface ReadAloudButtonProps {
  text: string;
  language: Language;
  playLabel: string;
  stopLabel: string;
  className?: string;
}

export const ReadAloudButton: React.FC<ReadAloudButtonProps> = ({
  text,
  language,
  playLabel,
  stopLabel,
  className = "",
}) => {
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    return () => {
      if (typeof window !== "undefined" && "speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const handleToggle = () => {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) {
      alert("Voice speech is not supported in this browser.");
      return;
    }

    if (isPlaying) {
      window.speechSynthesis.cancel();
      setIsPlaying(false);
      return;
    }

    window.speechSynthesis.cancel();
    const cleanText = text.replace(/₹/g, " ರೂಪಾಯಿ ").replace(/\*/g, "");
    const utterance = new SpeechSynthesisUtterance(cleanText);

    utterance.lang =
      language === "kn" ? "kn-IN" : language === "hi" ? "hi-IN" : "en-IN";
    utterance.rate = 0.95; // slightly slower for rural legibility

    utterance.onend = () => setIsPlaying(false);
    utterance.onerror = () => setIsPlaying(false);

    setIsPlaying(true);
    window.speechSynthesis.speak(utterance);
  };

  return (
    <button
      type="button"
      onClick={handleToggle}
      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all duration-fast select-none touch-press ${
        isPlaying
          ? "bg-risk text-white animate-pulse"
          : "bg-surface-low dark:bg-surface-low-dark text-ink dark:text-ink-dark border border-divider dark:border-divider-dark hover:bg-surface-high"
      } ${className}`}
    >
      <span className="material-symbols-outlined text-[18px]">
        {isPlaying ? "stop" : "volume_up"}
      </span>
      <span>{isPlaying ? stopLabel : playLabel}</span>
    </button>
  );
};

