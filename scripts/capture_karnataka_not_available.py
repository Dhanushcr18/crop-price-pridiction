import os
import time
from playwright.sync_api import sync_playwright

OUTPUT_DIR = r"C:\Users\dhadh\.gemini\antigravity\brain\96f1bef3-2c58-4faa-81e5-583c6058ad5e"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def capture():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        print("Navigating to http://localhost:3000...")
        page.goto("http://localhost:3000", wait_until="networkidle")
        time.sleep(2)

        # 1. Welcome screen: Click Start button
        start_btn = page.locator("button:has-text('ಪ್ರಾರಂಭಿಸಿ'), button:has-text('ಆರಂಭಿಸಿ'), button:has-text('Start')").first
        if start_btn.is_visible():
            start_btn.click()
            time.sleep(1)

        # 2. Step 1 (Crop): Onion is selected by default, click "ಮುಂದೆ" (Next)
        next_btn = page.locator("button:has-text('ಮುಂದೆ'), button:has-text('Next')").first
        if next_btn.is_visible():
            next_btn.click()
            time.sleep(1)

        # 3. Capture Step 2 (Mandis)
        mandi_screenshot_path = os.path.join(OUTPUT_DIR, "step2_mandi_neutral_svg.png")
        page.screenshot(path=mandi_screenshot_path, full_page=False)
        print(f"Captured Step 2: {mandi_screenshot_path}")

        # Continue through wizard:
        # Step 2 -> Next
        next_btn = page.locator("button:has-text('ಮುಂದೆ'), button:has-text('Next')").first
        if next_btn.is_visible():
            next_btn.click()
            time.sleep(0.5)

        # Step 3 (Quantity) -> Next
        next_btn = page.locator("button:has-text('ಮುಂದೆ'), button:has-text('Next')").first
        if next_btn.is_visible():
            next_btn.click()
            time.sleep(0.5)

        # Step 4 (Storage) -> Next
        next_btn = page.locator("button:has-text('ಮುಂದೆ'), button:has-text('Next')").first
        if next_btn.is_visible():
            next_btn.click()
            time.sleep(0.5)

        # Step 5 (Debt) -> Next
        next_btn = page.locator("button:has-text('ಮುಂದೆ'), button:has-text('Next')").first
        if next_btn.is_visible():
            next_btn.click()
            time.sleep(0.5)

        # Step 6 (Review) -> Click "ಸಲಹೆ ಪಡೆಯಿರಿ" / "Get Advice"
        get_advice_btn = page.locator("button:has-text('ಸಲಹೆ ಪಡೆಯಿರಿ'), button:has-text('Get Advice')").first
        if get_advice_btn.is_visible():
            get_advice_btn.click()
            print("Clicked Get Advice, waiting for results...")
            time.sleep(3)

        # 4. Capture Results page
        results_screenshot_path = os.path.join(OUTPUT_DIR, "results_karnataka_not_available.png")
        page.screenshot(path=results_screenshot_path, full_page=False)
        print(f"Captured Results: {results_screenshot_path}")

        browser.close()

if __name__ == "__main__":
    capture()
