---
name: Kheti Sahayak Karnataka
colors:
  surface: '#fff8f4'
  surface-dim: '#e8d7c9'
  surface-bright: '#fff8f4'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fff1e7'
  surface-container: '#fcebdc'
  surface-container-high: '#f7e5d7'
  surface-container-highest: '#f1dfd1'
  on-surface: '#221a11'
  on-surface-variant: '#41493e'
  inverse-surface: '#382f25'
  inverse-on-surface: '#ffeee0'
  outline: '#717a6d'
  outline-variant: '#c0c9bb'
  surface-tint: '#2a6b2c'
  primary: '#00450d'
  on-primary: '#ffffff'
  primary-container: '#1b5e20'
  on-primary-container: '#90d689'
  inverse-primary: '#91d78a'
  secondary: '#7a5649'
  on-secondary: '#ffffff'
  secondary-container: '#fdcdbc'
  on-secondary-container: '#795548'
  tertiary: '#6c2200'
  on-tertiary: '#ffffff'
  tertiary-container: '#933100'
  on-tertiary-container: '#ffb498'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#acf4a4'
  primary-fixed-dim: '#91d78a'
  on-primary-fixed: '#002203'
  on-primary-fixed-variant: '#0c5216'
  secondary-fixed: '#ffdbcf'
  secondary-fixed-dim: '#ebbcac'
  on-secondary-fixed: '#2e150b'
  on-secondary-fixed-variant: '#603f33'
  tertiary-fixed: '#ffdbcf'
  tertiary-fixed-dim: '#ffb59a'
  on-tertiary-fixed: '#380d00'
  on-tertiary-fixed-variant: '#802a00'
  background: '#fff8f4'
  on-background: '#221a11'
  surface-variant: '#f1dfd1'
typography:
  display-lg:
    fontFamily: Noto Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
  display-lg-mobile:
    fontFamily: Noto Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
  headline-lg:
    fontFamily: Noto Sans
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
  headline-md:
    fontFamily: Noto Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  title-lg:
    fontFamily: Noto Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Noto Sans
    fontSize: 18px
    fontWeight: '500'
    lineHeight: 26px
  body-md:
    fontFamily: Noto Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-lg:
    fontFamily: Noto Sans
    fontSize: 16px
    fontWeight: '700'
    lineHeight: 20px
  label-md:
    fontFamily: Noto Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 18px
  numeral-lg:
    fontFamily: Noto Sans
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
  numeral-md:
    fontFamily: Noto Sans
    fontSize: 22px
    fontWeight: '700'
    lineHeight: 28px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-lg: 1.5rem
  margin: 1rem
  margin-md: 1.5rem
  margin-lg: 2.5rem
  space-xs: 0.375rem
  space-sm: 0.75rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.25rem
  space-2xl: 3rem
---

## Brand & Style

### Personality & Purpose
The visual identity is grounded, dignified, and rooted in the soil. Designed specifically for smallholder and marginal onion cultivators across Karnataka, the UI avoids slick corporate abstractions in favor of direct physical reassurance, high clarity, and field-tested legibility under intense outdoor sunlight. It conveys the authority of an agricultural research institute paired with the warmth of an experienced village elder.

### Aesthetic Direction: Tactile Agricultural Utilitarianism
The style synthesizes high-contrast utilitarian clarity with organic warmth:
- **High-contrast readability:** Built to function reliably on low-cost Android handsets, smudge-prone shared tablets, and high-glare village kiosk terminals (Raitha Samparka Kendras).
- **Physical reassurance:** Generous tap zones, distinct borders, and warm, bone-colored card substrates that mimic heavy paper ledgers rather than cold glass.
- **Visual hierarchy:** Emphasizes instant comprehension over ornamentation. Risk, market trends, and weather warnings must be distinguishable at an arm's length.

## Colors

### Palette Philosophy
The palette draws straight from agrarian life in the Deccan plateau: fertile black cotton soil, healthy onion shoots, cured turmeric, and baked brick clay. Every critical color combination meets WCAG AAA standards (7:1 contrast ratio) against the warm light background.

- **Primary (`#1B5E20` / `#2E7D32`):** Deep Forest & Leaf Green. Represents crop health, safe planting windows, and profitable market realization.
- **Secondary (`#795548` / `#5D4037`):** Khaki Soil & Silt. Grounding anchors for tab bars, inactive states, and agricultural baseline indicators.
- **Warning & Advisory (`#E65100` / `#F57F17`):** Turmeric & Deep Amber. Used for price volatility alerts, irrigation delays, and pest advisory watchlists. Paired with a pale butter-cream tint (`#FFF8E1`) for alert backgrounds.
- **Critical Risk (`#C62828`):** Terracotta Red. Reserved strictly for severe financial risk, market crashes, sudden thrips/purple blotch outbreaks, and extreme weather emergencies. Paired with soft pink-brick tint (`#FFEBEE`).
- **Base Canvas (`#FAF7F0`):** Bone/Cream. Reduces glare and eye fatigue in midday outdoor environments compared to stark pure white (`#FFFFFF`).
- **Typography (`#2A2118` / `#1C1917`):** Deep Roasted Brown-Black. Softer than pure black yet delivers near-maximum contrast over the cream canvas.

## Typography

### Font Stack & Indic Script Parity
The typographic engine relies on **Noto Sans** with runtime glyph resolution across **Noto Sans Kannada**, **Noto Sans Devanagari**, and **Noto Sans** (Latin/Numeral).
- Line heights are tuned generously (1.45–1.5x) to accommodate conjuncts, vowel matras, and ottu characters in Kannada script without clipping ascenders or descenders.
- The base reading size is elevated to **18px** (`body-lg`) to ensure farmers with varying degrees of visual acuity can read comfortably without squinting.
- All numbers, mandi market prices (₹/Quintal), moisture percentages, and crop yield forecasts must enforce OpenType tabular figures (`font-variant-numeric: tabular-nums`) to preserve strict column alignment across comparison matrices.

## Layout & Spacing

### Ergonomic Standards
Layout rules prioritize rough, dust-covered hands, one-handed field smartphone usage, and shared kiosk touch interfaces.
- **Minimum Interactive Bound:** Every interactive target (action buttons, chips, radio cards) must provide a bounding box of at least **48×48px**, with 56px preferred on primary workflows.
- **Rhythm & Grid:** A responsive 4-column layout on mobile (<600px), transitioning to an 8-column layout on tablet/handheld terminals (600–1024px), and a structured 12-column system on desktop and fixed kiosks (>1024px).
- **Sticky Decision Trays:** Critical advisory actions (e.g., "Sell Now at APMC Hubli", "Apply Fungicide") pin to the bottom edge on mobile viewports with full 16px lateral padding and safe-area insets.

## Elevation & Depth

### Tonal Stratification with Crisp Grounding
To maintain contrast in extreme daylight, this system rejects soft diffused blurs and low-opacity multi-layered drop shadows. Depth is achieved via **structural surface tones** and **firm boundary lines**:

- **Ground (Canvas):** Tone `#FAF7F0`.
- **Level 1 (Cards & Data Surfaces):** `#FFFFFF` with a crisp 1.5px solid border in `#E6DFD5`.
- **Level 2 (Active Sheets & Focus Items):** Elevated with a single directional offset shadow: `0 3px 0 0 #D7CCC8`, grounding the element physically to the surface like a physical ledger tab.
- **Alert Overlays & Modals:** Crisp 2px perimeter border in the respective status hue (Terracotta Red `#C62828` or Leaf Green `#1B5E20`) accompanied by a 40% dark amber scrim (`rgba(42, 33, 24, 0.45)`).

## Shapes

### Sturdy Architectural Radii
- All standard containers, data tiles, and kiosk cards use a disciplined, soft **0.25rem (4px)** corner radius (`roundedness: 1`), keeping elements looking sturdy and deliberate.
- Interactive buttons and badges scale to a maximum radius of **0.5rem (8px)** (`rounded-lg`).
- Overly round or pill-shaped containers are avoided; square-adjacent profiles maximize internal display area for high-density Kannada character strings and wide tabular numeral grids.

## Components

### 1. Action Buttons
- **Primary Action:** Solid Leaf Green (`#1B5E20`) fill with White (`#FFFFFF`) bold text. Height: minimum 52px. Internal padding: `space-md` (16px) left/right.
- **Secondary Action:** Bone/White fill with `#1B5E20` 2px border and text.
- **Risk Action:** Terracotta Red (`#C62828`) fill for immediate harvest/dump or loss-prevention decisions.

### 2. Kiosk & Field Cards
- Constructed with `#FFFFFF` background, 1.5px border (`#E6DFD5`), and padding of `space-lg` (24px).
- Cards display an explicit color-coded indicator stripe (4px thick) along the left edge: Leaf Green for positive yield/price indicators, Turmeric for caution, Terracotta for danger.

### 3. Structured Comparison Strips
- Used for side-by-side APMC Mandi pricing (e.g., Hubli vs. Bengaluru vs. Solapur).
- Horizontal rows divided by 1px solid `#E6DFD5` dividers.
- Tabular numerals (`numeral-md`) right-aligned, market name left-aligned with localized script labels above.

### 4. Alert & Advisory Banners
- **Turmeric Warning:** `#FFF8E1` background, `#E65100` bold heading, 2px `#F57F17` border. Accompanied by high-legibility caution iconography.
- **Critical Red Warning:** `#FFEBEE` background, `#C62828` body copy and border.

### 5. Form Elements (Radio Tiles & Inputs)
- Checkboxes and radio buttons are contained inside full-width tap-target cards (minimum height 56px) rather than naked inputs.
- Selected state: 2px solid `#1B5E20` boundary with a subtle green tint background (`#E8F5E9`).