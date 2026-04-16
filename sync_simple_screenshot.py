from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://google.com")

    # ASSERTY – POPRAWNIE (bez nawiasów przy url)
    assert page.title() == "Google"  # title() to metoda – nawiasy OK
    assert "Google" in page.title()  # title() to metoda – nawiasy OK
    assert page.url == "https://www.google.com/"  # url to property – BEZ NAWIASÓW!

    page.screenshot(path="test_screenshot.png")
    browser.close()