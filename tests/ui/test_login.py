import pytest
from playwright.sync_api import expect

from config import settings
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.data_factory import unique_email


@pytest.mark.ui
@pytest.mark.smoke
def test_login_with_valid_credentials(page, existing_user):
    login = LoginPage(page).open()
    expect(login.login_heading).to_be_visible()

    login.login(existing_user.email, existing_user.password)

    home = HomePage(page)
    expect(home.logged_in_as).to_contain_text(existing_user.name)
    expect(home.logout_link).to_be_visible()


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize(
    "email_kind, password",
    [
        ("unregistered", settings.TEST_PASSWORD),
        ("registered", "WrongPass#999"),
    ],
    ids=["unknown_email", "wrong_password"],
)
def test_login_with_invalid_credentials(page, existing_user, email_kind, password):
    email = unique_email("nobody") if email_kind == "unregistered" else existing_user.email

    login = LoginPage(page).open()
    login.login(email, password)

    expect(login.login_error).to_have_text("Your email or password is incorrect!")
    assert login.current_path() == "/login"
    expect(HomePage(page).logged_in_as).to_have_count(0)


@pytest.mark.ui
@pytest.mark.regression
def test_logout(page, logged_in_user):
    home = HomePage(page)
    home.logout()

    login = LoginPage(page)
    assert login.current_path() == "/login"
    expect(login.login_heading).to_be_visible()
    expect(home.logout_link).to_have_count(0)
    expect(home.signup_login_link).to_be_visible()
