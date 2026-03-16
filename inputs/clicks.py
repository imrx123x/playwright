import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = await context.new_page()

        await page.goto("https://demoqa.com/buttons")

        ### generic click - dynamic selector
        button = page.locator("text=Click Me").nth(2)
        await page.screenshot(path='screenshots/dynamic_click.png')
        await button.click()

        ### assertion
       # await expect(page.locator())
asyncio.run(main())