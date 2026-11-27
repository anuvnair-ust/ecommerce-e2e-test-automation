import re

from pages.base_page import BasePage


class ProductsPage(BasePage):
    path = "/products"

    def __init__(self, page):
        self.page = page
        self.page_heading = page.locator("h2.title").first
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")
        self.product_cards = page.locator(".features_items .product-image-wrapper")
        self.product_names = page.locator(".features_items .productinfo p")
        self.product_prices = page.locator(".features_items .productinfo h2")
        self.category_panel = page.locator("#accordian")
        self.category_headers = page.locator("#accordian .panel-title a")
        self.brand_links = page.locator(".brands_products a")

    def search(self, term):
        self.search_input.fill(term)
        self.click_and_wait(self.search_button)

    def heading_text(self):
        return self.page_heading.inner_text().strip()

    def product_name_list(self):
        return [name.strip() for name in self.product_names.all_inner_texts()]

    def open_product(self, product_id):
        self.click_and_wait(self.page.locator(f'a[href="/product_details/{product_id}"]').first)

    def expand_category(self, category):
        self.category_panel.locator(f'a[href="#{category}"]').click()

    def open_subcategory(self, category, subcategory):
        self.expand_category(category)
        link = self.page.locator(f"#{category} a", has_text=re.compile(subcategory, re.IGNORECASE))
        self.click_and_wait(link.first)

    def open_brand(self, brand):
        link = self.brand_links.filter(has_text=re.compile(re.escape(brand), re.IGNORECASE))
        self.click_and_wait(link.first)
