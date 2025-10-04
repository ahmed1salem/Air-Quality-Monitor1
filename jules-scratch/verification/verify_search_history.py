from playwright.sync_api import sync_playwright, expect
import time

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # 1. Load the page and go to the map view
            page.goto("http://localhost:8000/index.html#map")

            # 2. Explicitly wait for the geocoder control container to be ready
            geocoder_container = page.locator(".leaflet-control-geocoder")
            expect(geocoder_container).to_be_visible(timeout=15000)

            # 3. Now find and click the geocoder icon within the container
            geocoder_icon = geocoder_container.locator("a.leaflet-control-geocoder-icon")
            expect(geocoder_icon).to_be_visible()
            geocoder_icon.click()

            # 4. Search for a location in English
            geocoder_input = page.locator(".leaflet-control-geocoder-form input")
            expect(geocoder_input).to_be_visible()
            geocoder_input.fill("Cairo")
            geocoder_input.press("Enter")

            # Wait for the geocoder result to appear and click it
            page.locator(".leaflet-control-geocoder-alternatives a").first.click()

            # 5. Verify map moved and data panel is updated
            expect(page.locator("#city-name")).to_contain_text("Cairo", timeout=15000)

            # 6. Open sidebar and verify history
            page.locator("#menu-btn").click()
            expect(page.locator("#history-list a").first).to_contain_text("Cairo")

            # 7. Switch to Arabic
            page.locator("#lang-ar-sidebar").click()
            expect(page.locator("h3[data-lang-key='historyTitle']")).to_contain_text("سجل البحث")

            # 8. Search for a location in Arabic
            page.locator("#close-sidebar-btn").click()
            geocoder_icon.click() # Re-expand the search bar
            geocoder_input_ar = page.locator(".leaflet-control-geocoder-form input")
            expect(geocoder_input_ar).to_have_attribute("placeholder", "ابحث عن مدينة أو مكان...")
            geocoder_input_ar.fill("Riyadh")
            geocoder_input_ar.press("Enter")
            page.locator(".leaflet-control-geocoder-alternatives a").first.click()

            # 9. Verify map moved and data panel is updated
            expect(page.locator("#city-name")).to_contain_text("Riyadh", timeout=15000)

            # 10. Re-open sidebar and verify new history item
            page.locator("#menu-btn").click()
            expect(page.locator("#history-list a").first).to_contain_text("Riyadh")

            # 11. Click the first history item (Cairo)
            page.locator("#history-list a").last.click()

            # 12. Verify map moved back to Cairo
            expect(page.locator("#city-name")).to_contain_text("Cairo", timeout=15000)

            # 13. Take final screenshot
            page.screenshot(path="jules-scratch/verification/verification_search.png")

            print("Verification script completed successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            page.screenshot(path="jules-scratch/verification/verification_error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()