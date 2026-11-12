import React from "react";
import { formatNumber } from "../../lib/formatter";

export interface QuantityStepperProps {
  value: number;
  onChange: (val: number) => void;
  unitLabel: string;
  bagEstimateLabel: string; // e.g. "about {bags} bags (50 kg gunny bags)"
  min?: number;
  max?: number;
  step?: number;
}

export const QuantityStepper: React.FC<QuantityStepperProps> = ({
  value,
  onChange,
  unitLabel,
  bagEstimateLabel,
  min = 1,
  max = 1000,
  step = 5,
}) => {
  const chips = [10, 20, 30, 50];
  const bagCount = Math.round(value * 2);
  const bagText = bagEstimateLabel.replace("{bags}", formatNumber(bagCount));

  const handleDecrement = () => {
    onChange(Math.max(min, value - step));
  };

  const handleIncrement = () => {
    onChange(Math.min(max, value + step));
  };

  return (
    <div className="w-full bg-white dark:bg-surface-dark border border-divider dark:border-divider-dark rounded-2xl p-5 sm:p-6 shadow-card flex flex-col items-center text-center gap-4">
      {/* Big Counter Deck */}
      <div className="flex items-center justify-between w-full max-w-[320px] gap-3">
        {/* Decrement Button (56px) */}
        <button
          type="button"
          aria-label="Decrease quantity"
          onClick={handleDecrement}
          disabled={value <= min}
          className="w-14 h-14 rounded-2xl bg-surface-low dark:bg-surface-low-dark border border-divider dark:border-divider-dark text-ink dark:text-ink-dark flex items-center justify-center active:bg-surface-high transition-colors touch-press disabled:opacity-40 disabled:cursor-not-allowed select-none"
        >
          <span className="material-symbols-outlined text-[32px]">remove</span>
        </button>

        {/* Central Display */}
        <div className="flex flex-col items-center min-w-0">
          <div className="flex items-baseline gap-1.5">
            <span className="text-3xl sm:text-4xl font-extrabold text-primary dark:text-primary-dark tabular-nums tracking-tight">
              {formatNumber(value)}
            </span>
            <span className="text-base sm:text-lg font-bold text-ink-muted dark:text-ink-muted-dark">
              {unitLabel}
            </span>
          </div>
        </div>

        {/* Increment Button (56px) */}
        <button
          type="button"
          aria-label="Increase quantity"
          onClick={handleIncrement}
          disabled={value >= max}
          className="w-14 h-14 rounded-2xl bg-primary text-white flex items-center justify-center hover:bg-primary-hover active:bg-primary-container transition-colors touch-press shadow-touch disabled:opacity-40 disabled:cursor-not-allowed select-none"
        >
          <span className="material-symbols-outlined text-[32px]">add</span>
        </button>
      </div>

      {/* Quick Tap Chips */}
      <div className="w-full flex items-center justify-center gap-2 flex-wrap pt-1">
        {chips.map((chipVal) => {
          const isActive = value === chipVal;
          return (
            <button
              key={chipVal}
              type="button"
              onClick={() => onChange(chipVal)}
              className={`h-11 px-4 rounded-xl font-bold text-sm transition-all duration-fast select-none touch-press ${
                isActive
                  ? "bg-primary text-white shadow-touch"
                  : "bg-surface-low dark:bg-surface-low-dark text-ink dark:text-ink-dark border border-divider dark:border-divider-dark hover:bg-surface-high"
              }`}
            >
              {chipVal} {unitLabel}
            </button>
          );
        })}
      </div>

      {/* Live 50kg Bag Conversion Strip */}
      <div className="w-full rounded-xl bg-surface-low dark:bg-surface-low-dark border border-divider/60 dark:border-divider-dark p-3 flex items-center justify-center gap-2 text-ink dark:text-ink-dark text-sm sm:text-base font-semibold">
        <span className="material-symbols-outlined text-primary text-[20px]">
          inventory_2
        </span>
        <span className="tabular-nums">{bagText}</span>
      </div>
    </div>
  );
};

