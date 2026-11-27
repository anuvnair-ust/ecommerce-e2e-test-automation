import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.ui_flows import register_new_user


@pytest.mark.ui
@pytest.mark.regression
def test_register_new_user(page, new_user_data, signup_user_cleanup):
    login = LoginPage(page).open()
    expect(login.new_user_heading).to_be_visible()

    account = register_new_user(page, new_user_data)

    assert account.current_path() == "/account_created"


@pytest.mark.ui
@pytest.mark.regression
def test_account_created_successfully(page, api_client, new_user_data, signup_user_cleanup):
    account = register_new_user(page, new_user_data)
    expect(account.account_created).to_have_text("Account Created!", ignore_case=True)

    account.continue_after_creation()
    home = HomePage(page)
    expect(home.logged_in_as).to_contain_text(new_user_data.name)

    body = api_client.get_user_by_email(new_user_data.email).json()
    assert body["responseCode"] == 200, body
    assert body["user"]["email"] == new_user_data.email
    assert body["user"]["name"] == new_user_data.name


@pytest.mark.ui
@pytest.mark.regression
def test_signup_with_already_registered_email(page, existing_user):
    login = LoginPage(page).open()
    login.start_signup("Duplicate Person", existing_user.email)

    expect(login.signup_error).to_have_text("Email Address already exist!")
