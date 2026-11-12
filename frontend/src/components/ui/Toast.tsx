import React from "react";

export interface ToastProps {
  message: string;
  icon?: string;
  visible: boolean;
}

export const Toast: React.FC<ToastProps> = ({
  message,
  icon = "check_circle",
  visible,
}) => {
  if (!visible) return null;

  return (
    <div className="fixed bottom-20 left-1/2 -translate-x-1/2 z-50 bg-ink text-white dark:bg-white dark:text-ink px-4 py-2.5 rounded-2xl shadow-elevated flex items-center gap-2 text-sm font-bold animate-in fade-in slide-in-from-bottom-2 duration-fast select-none">
      <span className="material-symbols-outlined text-[18px] text-primary dark:text-primary-dark">
        {icon}
      </span>
      <span>{message}</span>
    </div>
  );
};

