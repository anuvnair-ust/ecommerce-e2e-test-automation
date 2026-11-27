from pages.base_page import BasePage


class HomePage(BasePage):
    path = "/"

    def __init__(self, page):
        self.page = page
        self.featured_items = page.locator(".features_items")
        self.signup_login_link = page.locator('a[href="/login"]')
        self.products_link = page.locator('a[href="/products"]')
        self.cart_link = page.locator('a[href="/view_cart"]').first
        self.logout_link = page.locator('a[href="/logout"]')
        
        self.logged_in_as = page.locator("li", has_text="Logged in as")
        
        self.subscription_input = page.locator("#susbscribe_email")
        self.subscription_button = page.locator("#subscribe")
        self.subscription_success = page.locator("#success-subscribe")

    def go_to_login(self):
        self.click_and_wait(self.signup_login_link)

    def go_to_products(self):
        self.click_and_wait(self.products_link)

    def go_to_cart(self):
        self.click_and_wait(self.cart_link)

    def logout(self):
        self.click_and_wait(self.logout_link)

    def subscribe(self, email):
        self.scroll_to(self.subscription_input)
        self.subscription_input.fill(email)
        self.subscription_button.click()
