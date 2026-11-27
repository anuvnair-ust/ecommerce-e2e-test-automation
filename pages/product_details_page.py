from pages.base_page import BasePage


class ProductDetailsPage(BasePage):
    path = "/product_details/1"

    def __init__(self, page):
        self.page = page
        self.name = page.locator(".product-information h2")
        self.category = page.locator(".product-information p", has_text="Category:")
        self.price = page.locator(".product-information span span")
        self.availability = page.locator(".product-information p", has_text="Availability:")
        self.condition = page.locator(".product-information p", has_text="Condition:")
        self.brand = page.locator(".product-information p", has_text="Brand:")
        self.quantity_input = page.locator("input#quantity")
        self.add_to_cart_button = page.locator("button.cart")

    def open_product(self, product_id):
        return self.open(f"/product_details/{product_id}")

    def set_quantity(self, quantity):
        self.quantity_input.fill(str(quantity))

    def add_to_cart(self):
        self.add_to_cart_button.click()
