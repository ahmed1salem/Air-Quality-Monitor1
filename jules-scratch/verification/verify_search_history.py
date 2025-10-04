import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # 1. Start the application
            await page.goto("http://localhost:8081", wait_until="networkidle")

            # 2. Navigate to the map page
            await page.locator("#launch-map-btn").click()

            # 3. Wait for the map view to be visible and initialized
            map_view = page.locator("#map-view")
            await map_view.wait_for(state="visible", timeout=5000)

            # The geocoder is added dynamically by Leaflet, so we wait for it
            geocoder_input = page.locator('.leaflet-control-geocoder-form input')
            await geocoder_input.wait_for(state="visible", timeout=15000)

            # 4. Perform the first search (in English)
            await geocoder_input.fill('Cairo')
            await page.keyboard.press('Enter')
            await page.locator('#data-panel').wait_for(state="visible", timeout=10000)
            await page.wait_for_timeout(1000)

            # 5. Switch language to Arabic
            await page.locator("#menu-btn").click()
            await page.locator("#sidebar").wait_for(state="visible")
            await page.locator("#lang-ar-sidebar").click()
            await page.wait_for_timeout(1000)

            # Close the sidebar to ensure the map is interactive
            await page.locator("#close-sidebar-btn").click()
            await page.locator("#sidebar").wait_for(state="hidden")

            # 6. Perform the second search (in Arabic)
            await geocoder_input.fill('القاهرة')
            await page.keyboard.press('Enter')
            await page.locator('#data-panel').wait_for(state="visible", timeout=10000)
            await page.wait_for_timeout(1000)

            # 7. Open the sidebar and verify history
            await page.locator("#menu-btn").click()
            await page.locator("#sidebar").wait_for(state="visible")

            sidebar = page.locator("#sidebar")
            await sidebar.screenshot(path="jules-scratch/verification/search_history_verification.png")
            print("Screenshot saved to jules-scratch/verification/search_history_verification.png")

        except Exception as e:
            await page.screenshot(path="jules-scratch/verification/error.png")
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

asyncio.run(main())