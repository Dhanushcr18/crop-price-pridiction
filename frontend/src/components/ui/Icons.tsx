import React from "react";

export interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number | string;
  className?: string;
}

/** APMC Market Yard / Mandi Building Icon */
export const MandiIcon: React.FC<IconProps> = ({ size = 24, className = "", ...props }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
    {...props}
  >
    {/* Market Yard Building Structure */}
    <path d="M3 21h18" />
    <path d="M4 10h16" />
    <path d="M12 3L2 10h20L12 3z" />
    <path d="M6 10v11" />
    <path d="M10 10v11" />
    <path d="M14 10v11" />
    <path d="M18 10v11" />
  </svg>
);

/** Commercial Mandi / Large APMC Terminal Icon */
export const TerminalMandiIcon: React.FC<IconProps> = ({ size = 24, className = "", ...props }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
    {...props}
  >
    <path d="M4 22h16" />
    <path d="M5 22V7l7-4 7 4v15" />
    <path d="M9 11h2" />
    <path d="M13 11h2" />
    <path d="M9 15h2" />
    <path d="M13 15h2" />
    <path d="M10 22v-4h4v4" />
  </svg>
);

/** Local Rural / Sub-market Mandi Icon */
export const LocalMandiIcon: React.FC<IconProps> = ({ size = 24, className = "", ...props }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
    {...props}
  >
    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
    <polyline points="9 22 9 12 15 12 15 22" />
  </svg>
);

/** Onion Commodity Icon */
export const OnionIcon: React.FC<IconProps> = ({ size = 24, className = "", ...props }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 32 32"
    fill="none"
    className={className}
    {...props}
  >
    {/* Onion Stem / Shoot */}
    <path
      d="M16 2v6M16 8c-1.5-2.5-4-3.5-5-4M16 8c1.5-2.5 4-3.5 5-4"
      stroke="#2E7D32"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    {/* Bulb Body */}
    <path
      d="M16 8c-7 2-10 8-10 14 0 5 4.5 8 10 8s10-3 10-8c0-6-3-12-10-14z"
      fill="#C2410C"
      fillOpacity="0.18"
      stroke="#9A3412"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    {/* Skin Striations */}
    <path
      d="M13 12c-2.5 2-4 5.5-4 10 0 2.5 1 4.5 3 6M19 12c2.5 2 4 5.5 4 10 0 2.5-1 4.5-3 6M16 9v21"
      stroke="#9A3412"
      strokeWidth="1.5"
      strokeLinecap="round"
    />
  </svg>
);

/** Potato Commodity Icon */
export const PotatoIcon: React.FC<IconProps> = ({ size = 24, className = "", ...props }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 32 32"
    fill="none"
    className={className}
    {...props}
  >
    <path
      d="M8 12c1-6 8-8 15-5 5 2 6 7 5 12-1 6-6 10-12 9-7-1-9-10-8-16z"
      fill="#D97706"
      fillOpacity="0.18"
      stroke="#B45309"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <circle cx="12" cy="14" r="1" fill="#B45309" />
    <circle cx="19" cy="13" r="1.2" fill="#B45309" />
    <circle cx="15" cy="21" r="1.2" fill="#B45309" />
    <circle cx="21" cy="20" r="1" fill="#B45309" />
  </svg>
);

/** Tomato Commodity Icon */
export const TomatoIcon: React.FC<IconProps> = ({ size = 24, className = "", ...props }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 32 32"
    fill="none"
    className={className}
    {...props}
  >
    {/* Stem & Calyx Leaves */}
    <path
      d="M16 4v4M16 8l-4-2M16 8l4-2M16 8l-3 4M16 8l3 4"
      stroke="#15803D"
      strokeWidth="2"
      strokeLinecap="round"
    />
    {/* Tomato Body */}
    <path
      d="M16 10c-6.5 0-11 4-11 11 0 6 5 9 11 9s11-3 11-9c0-7-4.5-11-11-11z"
      fill="#DC2626"
      fillOpacity="0.18"
      stroke="#B91C1C"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

/** Sprout / Crop Outline Icon */
export const CropIcon: React.FC<IconProps> = ({ size = 24, className = "", ...props }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
    {...props}
  >
    <path d="M7 20h10" />
    <path d="M12 20v-8" />
    <path d="M12 12c-3-3-4-7 0-9 4 2 3 6 0 9z" />
    <path d="M12 15c-3-1-5-4-3-7 3 0 4 3 3 7z" />
  </svg>
);

/** Farmer / Producer Icon */
export const FarmerIcon: React.FC<IconProps> = ({ size = 24, className = "", ...props }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
    {...props}
  >
    {/* Hat Brim */}
    <path d="M2 10h20" />
    {/* Hat Top */}
    <path d="M6 10c0-3 2.5-5 6-5s6 2 6 5" />
    {/* Head & Face */}
    <path d="M7 10v3a5 5 0 0 0 10 0v-3" />
    {/* Shoulders */}
    <path d="M4 21v-2a4 4 0 0 1 4-4h8a4 4 0 0 1 4 4v2" />
  </svg>
);
