---
name: AgroScan Advisor
colors:
  surface: '#fff8f5'
  surface-dim: '#e3d8d1'
  surface-bright: '#fff8f5'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fdf1eb'
  surface-container: '#f7ece5'
  surface-container-high: '#f1e6df'
  surface-container-highest: '#ebe0da'
  on-surface: '#201b17'
  on-surface-variant: '#40493d'
  inverse-surface: '#352f2b'
  inverse-on-surface: '#faefe8'
  outline: '#707a6c'
  outline-variant: '#bfcaba'
  surface-tint: '#1b6d24'
  primary: '#0d631b'
  on-primary: '#ffffff'
  primary-container: '#2e7d32'
  on-primary-container: '#cbffc2'
  inverse-primary: '#88d982'
  secondary: '#376757'
  on-secondary: '#ffffff'
  secondary-container: '#baeed9'
  on-secondary-container: '#3d6d5d'
  tertiary: '#854500'
  on-tertiary: '#ffffff'
  tertiary-container: '#a95900'
  on-tertiary-container: '#ffefe5'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#a3f69c'
  primary-fixed-dim: '#88d982'
  on-primary-fixed: '#002204'
  on-primary-fixed-variant: '#005312'
  secondary-fixed: '#baeed9'
  secondary-fixed-dim: '#9ed1bd'
  on-secondary-fixed: '#002117'
  on-secondary-fixed-variant: '#1d4f40'
  tertiary-fixed: '#ffdcc4'
  tertiary-fixed-dim: '#ffb780'
  on-tertiary-fixed: '#2f1400'
  on-tertiary-fixed-variant: '#6f3800'
  background: '#fff8f5'
  on-background: '#201b17'
  surface-variant: '#ebe0da'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 3rem
    fontWeight: '700'
    lineHeight: 3.5rem
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 2rem
    fontWeight: '700'
    lineHeight: 2.5rem
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 1.5rem
    fontWeight: '600'
    lineHeight: 2rem
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 1.25rem
    fontWeight: '600'
    lineHeight: 1.75rem
  body-lg:
    fontFamily: Inter
    fontSize: 1.125rem
    fontWeight: '400'
    lineHeight: 1.75rem
  body-md:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: 1.5rem
  body-sm:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: 1.25rem
  label-lg:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '600'
    lineHeight: 1.25rem
    letterSpacing: 0.02em
  label-md:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: '600'
    lineHeight: 1rem
    letterSpacing: 0.04em
  tabular-metric:
    fontFamily: Inter
    fontSize: 1.75rem
    fontWeight: '700'
    lineHeight: 2rem
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-sm: 1rem
  margin: 2rem
  margin-sm: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system delivers an authoritative, high-clarity agricultural decision-support interface tailored for agricultural advisors, regional crop planners, and enterprise producers. It harmonizes institutional agronomic data with crowdsourced ground truth to provide clear supply outlooks and optimal crop selling windows.

The aesthetic blends **Modern Institutional Clarity** with grounded agricultural warmth:
- **Tone:** Grounded, rigorously objective, reassuring, and alert without inducing panic.
- **Visual Identity:** Crisp tabular layouts, tactile high-contrast data cards, clear data provenance distinctions, and a clean cream foundation replacing sterile tech-white.
- **Accessibility Baseline:** Meets WCAG 2.1 AAA for core readouts and contrast ratios; optimized for bright-sunlight field tablet viewports and high-density multi-pane desktop monitors.

## Colors

The color palette reinforces data origin, trust levels, and urgency:

- **Surface Base (`#FAF7F0`):** Soft, non-glare cream canvas that reduces visual fatigue in direct sunlight and indoor workstations alike.
- **Forest Green Primary (`#2E7D32`):** Primary interactive touchpoints, positive market signals, confirmed actions, and primary metrics.
- **Deep Pine (`#1B4D3E`):** Official institutional data (e.g., government crop census, satellite remote sensing, verified APMC arrivals).
- **Turmeric Amber (`#B25E00`):** Ground-reported and crowdsourced field submissions (local mandi spot rates, community sowing reports).
- **Terracotta Risk Red (`#C62828`):** Crop pest hazards, supply glut risks, extreme weather warnings, and market arbitrage anomalies.
- **Dark Charcoal Neutral (`#211C18`):** Primary text and structural outlines, ensuring stark, accessible readability across all cream backgrounds.
- **Subtle Surface Containers:** Surface alt (`#F2EEE4`), border subtle (`#E3DEC3`), border firm (`#211C18`).

## Typography

The typography system relies on **Inter** with native font fallbacks for regional languages (**Noto Sans Kannada**, **Noto Sans Devanagari**), ensuring identical vertical metrics and clear glyph separation for localized agricultural terminology.

### Key Rules
- **Tabular Numerics:** Enable `font-feature-settings: "tnum" 1, "cv05" 1` across all tables, ticker readouts, and supply forecasts to maintain vertical column alignment.
- **Multilingual Consistency:** Regional script fallbacks must maintain a minimum body size of 16px (`1rem`) to preserve readability of complex conjuncts and diacritics.
- **Data Scannability:** Use `label-md` uppercase with slight tracking (`0.04em`) exclusively for status pills, source indicators, and table header labels.

## Layout & Spacing

The layout is built for high-density agricultural dashboard monitoring with a **desktop-first 12-column fluid grid**:

- **Desktop (1280px+):** 12-column layout, 24px (`1.5rem`) gutters, 32px (`2rem`) outer margins. Supports split panels (e.g., 4-col advisory rail alongside an 8-col crop acreage map/matrix).
- **Tablet / Rugged Field Slate (768px - 1279px):** 8-column layout, 16px (`1rem`) gutters, 24px (`1.5rem`) margins.
- **Mobile (Below 768px):** 4-column layout, 16px gutters, 16px margins with horizontal scroll overflow for data grids.
- **Touch Target Enclosure:** Interactive items (filters, action triggers, toggle chips) reserve an absolute minimum hitbox of 48×48px to accommodate one-handed or gloved field operation.

## Elevation & Depth

To maximize outdoor readability and maintain a reliable, tactile interface, depth is conveyed through **firm, clean borders and layered tonal surfaces** rather than diffuse shadows.

- **Level 0 (Canvas):** Ground base `#FAF7F0`.
- **Level 1 (Default Card):** `#FFFFFF` background with a crisp 1px solid `#E3DEC3` perimeter. Zero ambient drop shadow.
- **Level 2 (Active / Critical Cards & Overlays):** `#FFFFFF` background with a 1.5px solid `#211C18` border and a solid directional offset shadow (`2px 2px 0px rgba(33, 28, 24, 0.15)`).
- **Level 3 (Modal / Flyout Advisory Sheets):** `#FFFFFF` framed with a 2px `#211C18` stroke and a sharp drop shadow (`0 8px 24px rgba(33, 28, 24, 0.12)`).

## Shapes

The design system adopts a **soft geometric precision** (`roundedness: 1`):
- Base radius: 4px (`0.25rem`) for buttons, inputs, segmented tabs, and chips.
- Container radius (`rounded-lg`): 8px (`0.5rem`) for metric containers, data tables, and map overlay cards.
- Modal / Panel radius (`rounded-xl`): 12px (`0.75rem`) for floating diagnostic sheets.
- Maintains a utilitarian, non-distracting silhouette that feels structured and durable.

## Components

### Buttons
- **Primary:** Forest green `#2E7D32` background, white `#FFFFFF` text, 4px border radius, min-height 48px, horizontal padding `1.5rem`.
- **Secondary (Official Actions):** Deep pine `#1B4D3E` outline (1.5px), cream background, `#1B4D3E` text.
- **Crowdsource Action:** Warm turmeric `#B25E00` tint background (`#FFF8F0`), 1.5px `#B25E00` border, `#B25E00` text.
- **Touch Targets:** Always enforce `min-width: 48px; min-height: 48px` with centered icon/text alignments.

### Chips & Provenance Tags
- **Official Data Tag:** `#1B4D3E` background, `#FFFFFF` text, `label-md`, solid 4px radius with an institutional building or satellite icon prefix.
- **Crowdsourced Tag:** `#B25E00` text, `#FAF0E6` background, 1px solid `#B25E00`.
- **Risk / Anomaly Tag:** `#C62828` text, `#FFEBEE` background, 1px solid `#C62828`.

### Input Fields & Selectors
- Background: `#FFFFFF`. Border: 1.5px solid `#E3DEC3`. Focused: 2px solid `#2E7D32`.
- Minimum field height: 48px. Text is `body-md` in `#211C18` with 12px horizontal padding.
- Dropdown menus use high-contrast item list separators (1px `#F2EEE4`).

### Cards & Data Containers
- White `#FFFFFF` surface on cream canvas with 1px `#E3DEC3` border.
- Segmented header zone with a distinct subtle surface (`#F2EEE4`) containing the crop name, area classification, and provenance badge.
- Inner data tables use alternating rows (`#FFFFFF` and `#FAF7F0`) with monospaced tabular figures.

### Checkboxes & Radio Controls
- Dimensions: 22×22px visual box positioned inside a 48×48px transparent touch wrapper.
- 2px border `#211C18`. Checked fill `#2E7D32` with a solid white indicator.

### Specialized Agricultural Components
- **Supply Outlook Gauge:** Dual-tone progress bar contrasting official projected supply (`#1B4D3E`) with crowdsourced actuals (`#B25E00`).
- **Harvest Window Timeline:** Horizontal segmented chart detailing optimal sell timing, marked with terracotta alert borders when storage saturation risks exceed thresholds.