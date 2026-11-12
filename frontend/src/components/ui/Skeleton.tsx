import React from "react";

export interface SkeletonProps {
  className?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({ className = "" }) => {
  return (
    <div
      className={`animate-pulse bg-surface-high dark:bg-surface-high-dark rounded-xl ${className}`}
      aria-hidden="true"
    />
  );
};

