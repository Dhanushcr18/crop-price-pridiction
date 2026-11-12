import React from "react";

export interface ProgressDotsProps {
  currentStep: number;
  totalSteps: number;
  stepLabel?: string;
}

export const ProgressDots: React.FC<ProgressDotsProps> = ({
  currentStep,
  totalSteps,
  stepLabel,
}) => {
  return (
    <div className="w-full space-y-2 select-none">
      {stepLabel && (
        <div className="flex items-center justify-between text-sm font-bold text-ink-muted dark:text-ink-muted-dark">
          <span>{stepLabel}</span>
          <span className="tabular-nums">
            {Math.round((currentStep / totalSteps) * 100)}%
          </span>
        </div>
      )}

      {/* Progress Bars / Dots */}
      <div
        className="grid gap-1.5 h-2 w-full"
        style={{ gridTemplateColumns: `repeat(${totalSteps}, minmax(0, 1fr))` }}
      >
        {Array.from({ length: totalSteps }, (_, idx) => idx + 1).map((s) => {
          const isCompleted = s < currentStep;
          const isCurrent = s === currentStep;

          return (
            <div
              key={s}
              className={`h-full rounded-full transition-all duration-fast ${
                isCompleted || isCurrent
                  ? "bg-primary"
                  : "bg-surface-high dark:bg-surface-high-dark"
              }`}
            />
          );
        })}
      </div>
    </div>
  );
};

