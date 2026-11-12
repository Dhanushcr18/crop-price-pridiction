import React from "react";

export interface ShareButtonProps {
  onShareWhatsApp: () => void;
  onDownloadSummary: () => void;
  whatsAppLabel: string;
  downloadLabel: string;
  className?: string;
}

export const ShareButton: React.FC<ShareButtonProps> = ({
  onShareWhatsApp,
  onDownloadSummary,
  whatsAppLabel,
  downloadLabel,
  className = "",
}) => {
  return (
    <div className={`flex items-center gap-2 flex-wrap ${className}`}>
      {/* WhatsApp Share */}
      <button
        type="button"
        onClick={onShareWhatsApp}
        className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-bold bg-[#25D366]/10 text-[#128C7E] dark:text-[#25D366] border border-[#25D366]/30 hover:bg-[#25D366]/20 transition-all duration-fast select-none touch-press"
      >
        <span className="material-symbols-outlined text-[18px]">share</span>
        <span>{whatsAppLabel}</span>
      </button>

      {/* Download Summary */}
      <button
        type="button"
        onClick={onDownloadSummary}
        className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-bold bg-surface-low dark:bg-surface-low-dark text-ink dark:text-ink-dark border border-divider dark:border-divider-dark hover:bg-surface-high transition-all duration-fast select-none touch-press"
      >
        <span className="material-symbols-outlined text-[18px]">download</span>
        <span>{downloadLabel}</span>
      </button>
    </div>
  );
};

