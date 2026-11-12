import os
import re
import sys
import time
from playwright.sync_api import sync_playwright

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "artifacts", "screenshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

VIEWPORTS = {
    "mobile": {"width": 360, "height": 780},
    "tablet": {"width": 768, "height": 1024},
    "desktop": {"width": 1280, "height": 800},
}

def verify_and_capture():
    results = []
    def log(msg):
        print(f"[VERIFY] {msg}")
        results.append(msg)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for lang in ["kn", "hi", "en"]:
            log(f"\n================ Testing Language: {lang.upper()} ================")
            
            # 1. Mobile (360px)
            context = browser.new_context(
                viewport=VIEWPORTS["mobile"],
                user_agent="Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 Mobile Safari/537.36"
            )
            page = context.new_page()
            
            # Go to home page
            page.goto("http://localhost:3000")
            page.wait_for_load_state("networkidle")
            
            # Save welcome screenshot
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"welcome_{lang}_360px.png"), full_page=True)
            log(f"Saved welcome_{lang}_360px.png")
            
            # Click language card on welcome screen
            lang_btn = page.locator(f"button[data-lang='{lang}']")
            if lang_btn.count() > 0:
                lang_btn.click()
            else:
                top_lang = page.locator(f"button[data-lang='{lang}']")
                if top_lang.count() > 0:
                    top_lang.first.click()
            
            page.wait_for_timeout(500)
            
            # Check horizontal overflow on mobile
            scroll_width = page.evaluate("document.documentElement.scrollWidth")
            client_width = page.evaluate("document.documentElement.clientWidth")
            log(f"360px Step 1 Scroll Width: {scroll_width}, Client Width: {client_width}")
            assert scroll_width <= client_width + 1, f"Horizontal overflow! {scroll_width} > {client_width}"
            
            # Screenshot step 1: Crop
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"step1_crop_{lang}_360px.png"))
            log(f"Saved step1_crop_{lang}_360px.png")
            
            # Click Next to Location
            page.locator("[data-testid='next-step-btn']").click()
            page.wait_for_timeout(300)
            
            # Step 2: Mandi - select Kolar
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"step2_mandi_{lang}_360px.png"))
            kolar_card = page.locator("button:has-text('Kolar'), button:has-text('ಕೋಲಾರ'), button:has-text('कोलार')")
            if kolar_card.count() > 0:
                kolar_card.first.click()
            page.wait_for_timeout(200)
            
            # Click Next to Quantity
            page.locator("[data-testid='next-step-btn']").click()
            page.wait_for_timeout(300)
            
            # Step 3: Quantity - select 30 qtl
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"step3_quantity_{lang}_360px.png"))
            chip_30 = page.locator("button:has-text('30 qtl'), button:has-text('30 ಕ್ವಿಂಟಾಲ್'), button:has-text('30 क्विंटल')")
            if chip_30.count() > 0:
                chip_30.first.click()
            page.wait_for_timeout(200)
            
            # Click Next to Storage
            page.locator("[data-testid='next-step-btn']").click()
            page.wait_for_timeout(300)
            
            # Step 4: Storage - select None (already default)
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"step4_storage_{lang}_360px.png"))
            
            # Click Next to Loan
            page.locator("[data-testid='next-step-btn']").click()
            page.wait_for_timeout(300)
            
            # Step 5: Loan - select Yes (owes trader)
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"step5_loan_{lang}_360px.png"))
            yes_btn = page.locator("button:has-text('ಹೌದು'), button:has-text('हाँ'), button:has-text('Yes')")
            if yes_btn.count() > 0:
                yes_btn.first.click()
            page.wait_for_timeout(200)
            
            # Click Next to Review
            page.locator("[data-testid='next-step-btn']").click()
            page.wait_for_timeout(300)
            
            # Step 6: Review Screen
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"step6_review_{lang}_360px.png"))
            log(f"Saved step6_review_{lang}_360px.png")
            
            # Click "Get Advice" button
            get_advice_btn = page.locator("[data-testid='get-advice-btn']")
            get_advice_btn.click()
            
            # Wait for results to load
            page.wait_for_selector("[data-testid='results-deck']", timeout=20000)
            page.wait_for_timeout(1000)
            
            # Check horizontal overflow on Results Deck
            scroll_width = page.evaluate("document.documentElement.scrollWidth")
            client_width = page.evaluate("document.documentElement.clientWidth")
            log(f"360px Results Scroll Width: {scroll_width}, Client Width: {client_width}")
            assert scroll_width <= client_width + 1, f"Horizontal overflow in Results deck! {scroll_width} > {client_width}"
            
            # Full page screenshot of Results on 360px
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"results_{lang}_360px.png"), full_page=True)
            log(f"Saved results_{lang}_360px.png")
            
            # Run visual & content validations
            text_content = page.locator("body").inner_text()
            
            # 1. Check decimals in prices (e.g. ₹ 3,650.39 or ₹3650.39)
            decimal_matches = re.findall(r"₹\s*\d+[,\d]*\.\d{2}", text_content)
            log(f"Decimal price check: found {len(decimal_matches)} decimal occurrences ({decimal_matches})")
            assert len(decimal_matches) == 0, f"Found decimal prices: {decimal_matches}"
            
            # 2. Check headline range exists
            assert ("₹" in text_content), "No rupee symbols found in results!"
            
            # 3. Check Synthetic Banner is present
            synthetic_banner = page.locator("[data-testid='synthetic-banner']")
            log(f"Synthetic banner count: {synthetic_banner.count()}")
            assert synthetic_banner.count() > 0, "Synthetic banner missing!"
            
            # 4. Check Local Mandi Strip is separated
            local_strip = page.locator("[data-testid='local-mandi-strip']")
            log(f"Local mandi strip count: {local_strip.count()}")
            assert local_strip.count() > 0, "Local mandi comparison strip missing!"
            
            # Visit Tab 2: History
            page.locator("a[href='/history']").click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"history_{lang}_360px.png"), full_page=True)
            log(f"Saved history_{lang}_360px.png")
            
            # Visit Tab 3: Reliability
            page.locator("a[href='/transparency']").click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"reliability_{lang}_360px.png"), full_page=True)
            log(f"Saved reliability_{lang}_360px.png")
            
            # Visit Tab 4: Help
            page.locator("a[href='/help']").click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"help_{lang}_360px.png"), full_page=True)
            log(f"Saved help_{lang}_360px.png")
            
            context.close()
            
        # 2. Tablet (768px) and Desktop (1280px) in Kannada
        for device_name, vp in [("tablet", VIEWPORTS["tablet"]), ("desktop", VIEWPORTS["desktop"])]:
            log(f"\n================ Testing Device: {device_name.upper()} ({vp['width']}x{vp['height']}) ================")
            context = browser.new_context(viewport=vp)
            page = context.new_page()
            
            # Load home and go directly to results
            page.goto("http://localhost:3000")
            page.wait_for_load_state("networkidle")
            
            # Click Kannada
            lang_btn = page.locator("button[data-lang='kn']")
            if lang_btn.count() > 0:
                lang_btn.click()
                page.wait_for_timeout(300)
            
            # Step through to results
            for _ in range(5):
                next_btn = page.locator("[data-testid='next-step-btn']")
                if next_btn.count() > 0 and next_btn.is_visible():
                    next_btn.click()
                    page.wait_for_timeout(200)
            
            # Review step -> Get Advice
            adv_btn = page.locator("[data-testid='get-advice-btn']")
            if adv_btn.count() > 0 and adv_btn.is_visible():
                adv_btn.click()
                page.wait_for_selector("[data-testid='results-deck']", timeout=20000)
                page.wait_for_timeout(1000)
            
            # Check horizontal overflow
            scroll_width = page.evaluate("document.documentElement.scrollWidth")
            client_width = page.evaluate("document.documentElement.clientWidth")
            log(f"{device_name} Results Scroll Width: {scroll_width}, Client Width: {client_width}")
            assert scroll_width <= client_width + 1, f"Horizontal overflow on {device_name}! {scroll_width} > {client_width}"
            
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"results_kn_{device_name}.png"), full_page=True)
            log(f"Saved results_kn_{device_name}.png")
            
            # Also open Transparency on desktop
            if device_name == "desktop":
                page.locator("a[href='/transparency']").click()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(500)
                page.screenshot(path=os.path.join(OUTPUT_DIR, f"reliability_kn_desktop.png"), full_page=True)
                log("Saved reliability_kn_desktop.png")
            
            context.close()
            
        browser.close()
        log("\n=======================================================")
        log("ALL PLAYWRIGHT VERIFICATION CHECKS PASSED SUCCESSFULLY!")
        log("=======================================================")

if __name__ == "__main__":
    verify_and_capture()
