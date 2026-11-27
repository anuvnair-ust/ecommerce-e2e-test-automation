from pages.account_page import AccountPage
from pages.login_page import LoginPage


def register_new_user(page, user):
    LoginPage(page).open().start_signup(user.name, user.email)
    account = AccountPage(page)
    account.fill_form(user)
    account.submit()
    return account
