import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # 1. Start the application
            await page.goto("http://localhost:8081", wait_until="networkidle")

            # 2. Wait for the header to be visible
            header = page.locator("header")
            await header.wait_for(state="visible")

            # Give the animation a moment to start
            await page.wait_for_timeout(2000)

            # 3. Take a screenshot of the header section
            await header.screenshot(path="jules-scratch/verification/shooting_star_verification.png")
            print("Screenshot saved to jules-scratch/verification/shooting_star_verification.png")

        except Exception as e:
            await page.screenshot(path="jules-scratch/verification/error.png")
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

asyncio.run(main())