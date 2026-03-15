from playwright.sync_api import Page
import pytest

#@pytest.mark.skip_browser("chromium")
@pytest.mark.only_browser("chromium")
def test_title(page: Page):
    page.goto('/')                          # u can just run it:  playwright % pytest --headed --base-url https://www.saucedemo.com/
    assert page.title() == "Swag Labs"

def test_inventory(page: Page):
    page.goto("https://www.saucedemo.com/inventory.html")
    assert page.inner_text('h3') == "Epic sadface: You can only access '/inventory.html' when you are logged in."

    # u can use arg --tracing on for test-results
    # for opening the trace u can use playwright show-trace /path-to/trace.zip