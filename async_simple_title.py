import pytest
from unittest.mock import AsyncMock, patch
import asyncio


# ========== prod ==========
async def get_page_title(page, url: str) -> str:
    """logic"""
    await page.goto(url)
    return await page.title()


async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        title = await get_page_title(page, "https://google.com")
        print(title)
        await browser.close()


# ========== uts ==========
@pytest.mark.asyncio
async def test_get_page_title_unit():
    """Unit test"""
    mock_page = AsyncMock()
    mock_page.goto = AsyncMock()
    mock_page.title = AsyncMock(return_value="Expected Title")

    result = await get_page_title(mock_page, "https://test.com")

    mock_page.goto.assert_called_once_with("https://test.com")
    assert result == "Expected Title"


@pytest.mark.asyncio
async def test_main_with_full_mock():
    """Unit test main() – mock evrthng"""
    with patch("your_module.async_playwright") as mock_apw:
        # Mock context manager
        mock_p = AsyncMock()
        mock_apw.return_value.__aenter__ = AsyncMock(return_value=mock_p)
        mock_apw.return_value.__aexit__ = AsyncMock()

        mock_browser = AsyncMock()
        mock_p.chromium.launch = AsyncMock(return_value=mock_browser)

        mock_page = AsyncMock()
        mock_browser.new_page = AsyncMock(return_value=mock_page)
        mock_page.title = AsyncMock(return_value="Mocked Title")

        await main()

        mock_p.chromium.launch.assert_called_once()
        mock_browser.new_page.assert_called_once()
        mock_page.goto.assert_called_once()


# ========== integration ==========
@pytest.mark.integration
@pytest.mark.asyncio
async def test_main_integration():
    """Test integracyjny – używa prawdziwego Playwright (wolny, tylko czasem)"""
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # headless dla CI
        page = await browser.new_page()
        title = await get_page_title(page, "https://google.com")
        assert "Google" in title
        await browser.close()