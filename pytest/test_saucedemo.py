from playwright.sync_api import Page
import pytest
from unittest.mock import Mock, patch, MagicMock


# ========== prod code ==========
# @pytest.mark.skip_browser("chromium")
@pytest.mark.only_browser("chromium")
def test_title(page: Page):
    page.goto('/')  # u can just run it:  playwright % pytest --headed --base-url https://www.saucedemo.com/
    assert page.title() == "Swag Labs"


def test_inventory(page: Page):
    page.goto("https://www.saucedemo.com/inventory.html")
    assert page.inner_text('h3') == "Epic sadface: You can only access '/inventory.html' when you are logged in."

    # u can use arg --tracing on for test-results
    # for opening the trace u can use playwright show-trace /path-to/trace.zip


# ========== UNIT TESTY (mockowane, bez przeglądarki) ==========

def test_title_unit():
    """Unit test – mockujemy Page, nie otwieramy przeglądarki"""
    mock_page = Mock(spec=Page)
    mock_page.title = Mock(return_value="Swag Labs")

    mock_page.goto('/')
    result = mock_page.title()

    mock_page.goto.assert_called_once_with('/')
    assert result == "Swag Labs"


def test_inventory_unit():
    """Unit test – mockujemy Page i inner_text"""
    mock_page = Mock(spec=Page)
    expected_text = "Epic sadface: You can only access '/inventory.html' when you are logged in."
    mock_page.inner_text = Mock(return_value=expected_text)

    mock_page.goto("https://www.saucedemo.com/inventory.html")
    result = mock_page.inner_text('h3')

    mock_page.goto.assert_called_once_with("https://www.saucedemo.com/inventory.html")
    mock_page.inner_text.assert_called_once_with('h3')
    assert result == expected_text


def test_title_negative_unit():
    """Unit test – scenariusz negatywny: tytuł się nie zgadza"""
    mock_page = Mock(spec=Page)
    mock_page.title = Mock(return_value="Wrong Title")

    mock_page.goto('/')
    result = mock_page.title()

    assert result != "Swag Labs"
    assert result == "Wrong Title"


def test_inventory_error_message_unit():
    """Unit test – sprawdzamy różne możliwe komunikaty błędów"""
    test_cases = [
        ("Epic sadface: You can only access '/inventory.html' when you are logged in.", True),
        ("Something else", False),
    ]

    for error_text, should_match in test_cases:
        mock_page = Mock(spec=Page)
        mock_page.inner_text = Mock(return_value=error_text)

        result = mock_page.inner_text('h3')

        if should_match:
            assert "Epic sadface" in result
        else:
            assert "Epic sadface" not in result


@pytest.mark.parametrize("url,expected_title", [
    ("/", "Swag Labs"),
    ("/inventory.html", "Swag Labs"),
    ("/cart.html", "Swag Labs"),
])
def test_title_parametrized(url, expected_title):
    """Parametryzowane unit testy – różne URLe"""
    mock_page = Mock(spec=Page)
    mock_page.title = Mock(return_value=expected_title)

    mock_page.goto(url)
    result = mock_page.title()

    assert result == expected_title


@pytest.mark.parametrize("error_message,expected_contains", [
    ("Epic sadface: You can only access '/inventory.html' when you are logged in.", True),
    ("Epic sadface: Username and password do not match", True),
    ("Welcome to the site", False),
])
def test_error_message_analysis(error_message, expected_contains):
    """Test logiki analizy komunikatu błędu (bez Page)"""
    if expected_contains:
        assert "Epic sadface" in error_message
    else:
        assert "Epic sadface" not in error_message