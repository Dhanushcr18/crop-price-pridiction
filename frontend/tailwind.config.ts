import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        fsa: {
          cream: '#FAF7F0',
          creamDark: '#141412',
          surfaceLight: '#FFFFFF',
          surfaceDark: '#21211E',
          borderLight: '#E8E3D7',
          borderDark: '#33322E',
          textMainLight: '#211C18',
          textMainDark: '#F7F4EE',
          textMutedLight: '#6B6258',
          textMutedDark: '#A39B91',
          green: '#2E7D32',
          greenHover: '#236327',
          greenLight: '#E8F5E9',
          greenDark: '#123D15',
          official: '#1B4D3E',
          officialBg: '#EAF3EF',
          officialBgDark: '#0D2921',
          officialBorder: '#A3C9BC',
          reported: '#B25E00',
          reportedBg: '#FFF7EB',
          reportedBgDark: '#3A1E02',
          reportedBorder: '#F2D099',
          turmeric: '#E65100',
          turmericBg: '#FFF3E0',
          terracotta: '#C62828',
          terracottaBg: '#FFEBEE',
          amberBadge: '#F59E0B',
        },
        // Core design system tokens for Farmer Sell Advisor
        primary: {
          DEFAULT: "#2E7D32", // Primary accessible harvest green
          dark: "#4CAF50",
          hover: "#236526",
          tint: "#E8F5E9",
          container: "#1B5E20",
        },
        caution: {
          DEFAULT: "#ED6C02", // Amber warning
          light: "#FFF3E0",
          dark: "#FFA726",
        },
        risk: {
          DEFAULT: "#D32F2F", // Terracotta risk
          dark: "#EF5350",
          light: "#FFEBEE",
        },
        cream: {
          DEFAULT: "#FAF7F0", // Outdoor sunlight-tested warm background
          dark: "#141210",
        },
        surface: {
          DEFAULT: "#FFFFFF",
          dark: "#201C19",
          low: "#F5F2EB",
          "low-dark": "#28231F",
          high: "#EAE5DB",
          "high-dark": "#342E28",
        },
        ink: {
          DEFAULT: "#1C1917", // Deep brown-black for high contrast readability
          muted: "#57534E",
          subtle: "#78716C",
          dark: "#FAF7F0",
          "muted-dark": "#A8A29E",
        },
        divider: {
          DEFAULT: "#E2DDD3",
          dark: "#3A332C",
        },
      },
      fontFamily: {
        sans: [
          '"Noto Sans Kannada"',
          '"Noto Sans Devanagari"',
          "Inter",
          "system-ui",
          "-apple-system",
          "sans-serif",
        ],
      },
      fontSize: {
        xs: ["13px", { lineHeight: "18px" }],
        sm: ["15px", { lineHeight: "22px" }],
        base: ["18px", { lineHeight: "26px" }], // Base 18px per design spec
        lg: ["20px", { lineHeight: "28px" }],
        xl: ["24px", { lineHeight: "32px" }],
        "2xl": ["28px", { lineHeight: "36px" }],
        "3xl": ["32px", { lineHeight: "40px" }],
        range: ["32px", { lineHeight: "38px", letterSpacing: "-0.02em" }],
      },
      minHeight: {
        touch: "56px", // Minimum 56px touch target for one-handed outdoor use
      },
      minWidth: {
        touch: "56px",
      },
      boxShadow: {
        touch: "0 2px 4px rgba(28, 25, 23, 0.06)",
        card: "0 1px 3px rgba(28, 25, 23, 0.08), 0 1px 2px rgba(28, 25, 23, 0.04)",
        elevated: "0 4px 12px rgba(28, 25, 23, 0.12)",
      },
      transitionDuration: {
        fast: "150ms", // Motion under 200ms per design spec
      },
    },
  },
  plugins: [],
};

export default config;
