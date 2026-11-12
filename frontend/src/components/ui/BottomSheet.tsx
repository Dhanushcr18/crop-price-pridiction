import React, { useEffect } from "react";

export interface BottomSheetProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
}

export const BottomSheet: React.FC<BottomSheetProps> = ({
  isOpen,
  onClose,
  title,
  children,
}) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };
    if (isOpen) {
      document.body.style.overflow = "hidden";
      window.addEventListener("keydown", handleKeyDown);
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4 select-none">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/60 backdrop-blur-xs transition-opacity"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Sheet Content */}
      <div
        role="dialog"
        aria-modal="true"
        className="relative w-full max-w-lg bg-white dark:bg-surface-dark border-t sm:border border-divider dark:border-divider-dark rounded-t-3xl sm:rounded-3xl p-5 sm:p-6 shadow-elevated z-10 max-h-[85vh] overflow-y-auto animate-in slide-in-from-bottom duration-fast"
      >
        {/* Handle for mobile swipe affordance */}
        <div className="w-12 h-1.5 bg-divider dark:bg-divider-dark rounded-full mx-auto mb-4 sm:hidden" />

        <div className="flex items-center justify-between pb-3 border-b border-divider/60 dark:border-divider-dark mb-4">
          {title && (
            <h3 className="font-extrabold text-lg sm:text-xl text-ink dark:text-ink-dark">
              {title}
            </h3>
          )}
          <button
            type="button"
            aria-label="Close"
            onClick={onClose}
            className="w-10 h-10 rounded-full bg-surface-low dark:bg-surface-low-dark flex items-center justify-center text-ink-muted hover:text-ink dark:text-ink-muted-dark dark:hover:text-ink-dark transition-colors touch-press ml-auto"
          >
            <span className="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        <div>{children}</div>
      </div>
    </div>
  );
};

