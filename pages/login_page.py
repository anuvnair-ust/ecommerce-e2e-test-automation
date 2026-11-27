from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/login"

    def __init__(self, page):
        self.page = page
        self.login_email = page.locator('[data-qa="login-email"]')
        self.login_password = page.locator('[data-qa="login-password"]')
        self.login_button = page.locator('[data-qa="login-button"]')
        self.login_error = page.locator('form:has([data-qa="login-button"]) p')
        self.signup_name = page.locator('[data-qa="signup-name"]')
        self.signup_email = page.locator('[data-qa="signup-email"]')
        self.signup_button = page.locator('[data-qa="signup-button"]')
        self.signup_error = page.locator('form:has([data-qa="signup-button"]) p')
        self.new_user_heading = page.locator("h2", has_text="New User Signup!")
        self.login_heading = page.locator("h2", has_text="Login to your account")

    def login(self, email, password):
        self.login_email.fill(email)
        self.login_password.fill(password)
        self.click_and_wait(self.login_button)

    def start_signup(self, name, email):
        self.signup_name.fill(name)
        self.signup_email.fill(email)
        self.click_and_wait(self.signup_button)
