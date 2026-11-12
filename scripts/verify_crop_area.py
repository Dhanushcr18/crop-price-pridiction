import os
import re
import sys
import time
from playwright.sync_api import sync_playwright

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "artifacts", "screenshots", "area")
os.makedirs(OUTPUT_DIR, exist_ok=True)

VIEWPORTS = {
    "mobile": {"width": 360, "height": 780},
    "tablet": {"width": 768, "height": 1024},
    "desktop": {"width": 1280, "height": 800},
}


def verify_crop_area():
    results = []

    def log(msg):
        print(f"[AREA-VERIFY] {msg}")
        results.append(msg)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for lang in ["kn", "hi", "en"]:
            log(f"\n================ Testing Language: {lang.upper()} (360px) ================")
            context = browser.new_context(
                viewport=VIEWPORTS["mobile"],
                user_agent="Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 Mobile Safari/537.36",
            )
            page = context.new_page()

            page.goto("http://localhost:3000")
            page.wait_for_load_state("networkidle")

            # Click language card on welcome screen
            lang_btn = page.locator(f"button[data-lang='{lang}']")
            if lang_btn.count() > 0:
                lang_btn.click()
                page.wait_for_timeout(400)

            # Switch to Crop Area tab
            crop_area_tab = page.locator("[data-testid='switch-to-crop-area-btn']")
            assert crop_area_tab.count() > 0, "Switch to Crop Area button not found!"
            crop_area_tab.click()
            page.wait_for_timeout(500)

            # Check 360px Step 1 scroll width
            sw = page.evaluate("document.documentElement.scrollWidth")
            cw = page.evaluate("document.documentElement.clientWidth")
            log(f"360px Step 1 Scroll Width: {sw}, Client Width: {cw}")
            assert sw <= cw + 1, f"Horizontal overflow at Step 1! {sw} > {cw}"

            # Screenshot Step 1
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"step1_district_{lang}_360px.png"))
            log(f"Saved step1_district_{lang}_360px.png")

            # Verify Mysuru is default
            select = page.locator("[data-testid='area-district-select']")
            assert select.count() > 0
            val = select.input_value()
            assert val == "Mysuru", f"Default district should be Mysuru, got {val}"

            # Click Step 1 Next
            page.locator("[data-testid='area-step1-next-btn']").click()
            page.wait_for_timeout(400)

            # Step 2: Acres Stepper
            sw = page.evaluate("document.documentElement.scrollWidth")
            cw = page.evaluate("document.documentElement.clientWidth")
            log(f"360px Step 2 Scroll Width: {sw}, Client Width: {cw}")
            assert sw <= cw + 1, f"Horizontal overflow at Step 2! {sw} > {cw}"

            # Click chip 50
            chip_50 = page.locator("button:has-text('50')")
            if chip_50.count() > 0:
                chip_50.first.click()
                page.wait_for_timeout(200)

            # Screenshot Step 2
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"step2_acres_{lang}_360px.png"))
            log(f"Saved step2_acres_{lang}_360px.png")

            # Click Submit & View Outlook
            submit_btn = page.locator("[data-testid='area-submit-btn']")
            assert submit_btn.count() > 0
            submit_btn.click()

            # Wait for results deck
            page.wait_for_selector("[data-testid='area-results-deck']", timeout=20000)
            page.wait_for_timeout(800)

            # Check 360px Results scroll width
            sw = page.evaluate("document.documentElement.scrollWidth")
            cw = page.evaluate("document.documentElement.clientWidth")
            log(f"360px Results Scroll Width: {sw}, Client Width: {cw}")
            assert sw <= cw + 1, f"Horizontal overflow in Crop Area Results! {sw} > {cw}"

            # Capture Full Results Deck Screenshot
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"results_mysuru_{lang}_360px.png"), full_page=True)
            log(f"Saved results_mysuru_{lang}_360px.png")

            # Text content assertions
            text = page.locator("body").inner_text()

            # 1. Decimal price check (must be 0)
            decimals = re.findall(r"₹\s*\d+[,\d]*\.\d{2}", text)
            log(f"Decimal price check: found {len(decimals)} occurrences ({decimals})")
            assert len(decimals) == 0, f"Found decimal prices: {decimals}"

            # 2. Check Mysuru "Not available" / fallback
            assert ("Mysuru" in text)
            assert ("Karnataka" in text)
            assert ("INDIA" in text.upper() or "ಭಾರತ" in text or "भारत" in text)

            # 3. Check "Too few reports to trust" warning
            assert ("Too few reports to trust" in text or "ವಿಶ್ವಾಸಾರ್ಹತೆಗೆ ತುಂಬಾ ಕಡಿಮೆ" in text or "भरोसे के लिए बहुत कम" in text)

            # 4. Check Synthetic Banner
            assert ("SYNTHETIC DATA" in text or "ಕೃತಕ ಡೇಟಾ" in text or "सिंथेटिक डेटा" in text or "काल्पनिक डेटा" in text)

            # 5. Check Autonomy disclaimer
            assert ("This is advice, the decision is yours." in text or "ತೀರ್ಮಾನ ನಿಮ್ಮದು" in text or "निर्णय आपका है" in text)

            context.close()

        # ================= Testing Gadag (Official District Available) =================
        log("\n================ Testing District with Official Data Available: GADAG ================")
        context = browser.new_context(viewport=VIEWPORTS["mobile"])
        page = context.new_page()

        page.goto("http://localhost:3000/area")
        page.wait_for_load_state("networkidle")

        # Select Gadag
        page.locator("[data-testid='area-district-select']").select_option("Gadag")
        page.locator("[data-testid='area-step1-next-btn']").click()
        page.wait_for_timeout(300)

        # Select 25 acres
        page.locator("button:has-text('25')").first.click()
        page.locator("[data-testid='area-submit-btn']").click()

        page.wait_for_selector("[data-testid='area-results-deck']", timeout=20000)
        page.wait_for_timeout(800)

        # Check scroll width
        sw = page.evaluate("document.documentElement.scrollWidth")
        cw = page.evaluate("document.documentElement.clientWidth")
        log(f"Gadag 360px Results Scroll Width: {sw}, Client Width: {cw}")
        assert sw <= cw + 1

        gadag_text = page.locator("body").inner_text()
        assert ("Gadag" in gadag_text)
        # Should have official district acreage (51,892 acres)
        assert ("51,892" in gadag_text or "51892" in gadag_text)

        page.screenshot(path=os.path.join(OUTPUT_DIR, "results_gadag_en_360px.png"), full_page=True)
        log("Saved results_gadag_en_360px.png")
        context.close()

        # ================= Desktop 1280px Viewport Verification =================
        log("\n================ Testing Desktop 1280px Viewport ================")
        context = browser.new_context(viewport=VIEWPORTS["desktop"])
        page = context.new_page()

        page.goto("http://localhost:3000/area")
        page.wait_for_load_state("networkidle")

        page.locator("[data-testid='area-step1-next-btn']").click()
        page.wait_for_timeout(300)
        page.locator("[data-testid='area-submit-btn']").click()
        page.wait_for_selector("[data-testid='area-results-deck']", timeout=20000)
        page.wait_for_timeout(800)

        sw = page.evaluate("document.documentElement.scrollWidth")
        cw = page.evaluate("document.documentElement.clientWidth")
        log(f"Desktop Results Scroll Width: {sw}, Client Width: {cw}")
        assert sw <= cw + 1

        page.screenshot(path=os.path.join(OUTPUT_DIR, "results_desktop_1280px.png"), full_page=True)
        log("Saved results_desktop_1280px.png")
        context.close()

        browser.close()
        log("\n==================================================================")
        log("ALL PLAYWRIGHT CROP AREA VERIFICATION TESTS PASSED SUCCESSFULLY!")
        log("==================================================================")


if __name__ == "__main__":
    verify_crop_area()
