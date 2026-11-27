import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from utils.data_factory import unique_email


@pytest.mark.ui
@pytest.mark.regression
def test_subscription_from_home_page(page):
    home = HomePage(page).open()
    home.scroll_to(home.subscription_input)
    expect(home.subscription_input).to_be_visible()

    home.subscribe(unique_email("subscriber"))

    expect(home.subscription_success).to_be_visible()
    expect(home.subscription_success).to_contain_text("You have been successfully subscribed!")
