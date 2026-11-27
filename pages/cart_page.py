import re

from pages.base_page import BasePage


def _digits_to_int(text):
    return int(re.sub(r"[^\d]", "", text))


class CartPage(BasePage):
    path = "/view_cart"

    def __init__(self, page):
        self.page = page
        self.item_rows = page.locator("#cart_info_table tbody tr")
        self.product_names = page.locator(".cart_description h4 a")
        self.empty_message = page.locator("#empty_cart")

    def row_for(self, product_name):
        return self.item_rows.filter(has_text=product_name)
    

    def is_product_in_cart(self, product_name):
        return self.row_for(product_name).count() > 0

    def quantity_of(self, product_name):
        return int(self.row_for(product_name).locator(".cart_quantity button").inner_text().strip())

    def unit_price_of(self, product_name):
        return _digits_to_int(self.row_for(product_name).locator("td.cart_price p").inner_text())

    def total_of(self, product_name):
        return _digits_to_int(self.row_for(product_name).locator("td.cart_total p").inner_text())

    def remove_product(self, product_name):
        self.row_for(product_name).locator("a.cart_quantity_delete").click()
        self.row_for(product_name).first.wait_for(state="detached", timeout=10000)

    def item_count(self):
        return self.item_rows.count()
