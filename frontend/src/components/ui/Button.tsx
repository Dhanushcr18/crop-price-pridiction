import React from "react";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "voice";
  size?: "sm" | "md" | "lg" | "touch";
  isListening?: boolean;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = "primary",
  size = "touch",
  isListening = false,
  className = "",
  disabled,
  children,
  ...props
}) => {
  const baseStyles =
    "inline-flex items-center justify-center font-bold rounded-2xl transition-all duration-fast select-none cursor-pointer focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed touch-press";

  const sizeStyles = {
    sm: "px-3 py-1.5 text-sm min-h-[40px]",
    md: "px-4 py-2 text-base min-h-[48px]",
    lg: "px-5 py-3 text-lg min-h-[56px]",
    touch: "px-6 py-3.5 text-base sm:text-lg min-h-[56px] w-full",
  }[size];

  const variantStyles = {
    primary:
      "bg-primary hover:bg-primary-hover active:bg-primary-container text-white shadow-touch focus:ring-primary",
    secondary:
      "bg-surface-low dark:bg-surface-low-dark hover:bg-surface-high text-ink dark:text-ink-dark border border-divider dark:border-divider-dark focus:ring-primary",
    ghost:
      "bg-transparent hover:bg-black/5 dark:hover:bg-white/5 text-ink dark:text-ink-dark focus:ring-primary",
    voice: isListening
      ? "bg-risk text-white animate-pulse focus:ring-risk"
      : "bg-primary-tint dark:bg-primary/20 text-primary dark:text-primary-dark border border-primary/30 hover:bg-primary/20 focus:ring-primary",
  }[variant];

  return (
    <button
      className={`${baseStyles} ${sizeStyles} ${variantStyles} ${className}`}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};

