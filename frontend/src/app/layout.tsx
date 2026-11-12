import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Farmer Sell Advisor | ರೈತ ಮಾರಾಟ ಸಲಹೆಗಾರ",
  description:
    "Honest market price decision intelligence for Karnataka smallholder onion farmers. Advises WHERE and WHEN to sell.",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1.0,
  maximumScale: 5.0, // Allows user pinch-zoom to 200%+ for visual accessibility
  userScalable: true,
  themeColor: "#2E7D32",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="kn" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        {/* Noto Sans Kannada, Noto Sans Devanagari, Inter for 100% native Indic script rendering */}
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;500;600;700;800&family=Noto+Sans+Kannada:wght@400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,600,0,0&display=swap"
        />
        {/* All fonts (Noto Sans Kannada, Noto Sans Devanagari, Inter) are 100% self-hosted via fonts.css */}
      </head>
      <body className="bg-cream dark:bg-cream-dark text-ink dark:text-ink-dark antialiased font-sans selection:bg-primary/20 min-h-screen flex flex-col">
        {children}
      </body>
    </html>
  );
}
