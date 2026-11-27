import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.smoke
def test_home_page_loads_successfully(page):
    home = HomePage(page).open()

    assert home.current_path() == "/"
    assert "Automation Exercise" in home.page_title()
    expect(home.featured_items.first).to_be_visible()
    expect(home.signup_login_link).to_be_visible()
    expect(home.products_link).to_be_visible()
    expect(home.cart_link).to_be_visible()
