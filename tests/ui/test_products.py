import pytest
from playwright.sync_api import expect

from config import settings
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage


@pytest.mark.ui
@pytest.mark.smoke
def test_navigate_to_products_page(page, home_page):
    home_page.go_to_products()

    products = ProductsPage(page)
    assert products.current_path() == "/products"
    expect(products.page_heading).to_have_text("All Products", ignore_case=True)
    assert products.product_cards.count() > 0, "No products rendered on the products page"


@pytest.mark.ui
@pytest.mark.regression
def test_search_product(page, products_page):
    term = settings.SEARCH_TERM
    products_page.search(term)

    expect(products_page.page_heading).to_have_text("Searched Products", ignore_case=True)
    names = products_page.product_name_list()
    assert names, f"No results returned for search term '{term}'"
    assert any(term in name.lower() for name in names), names


@pytest.mark.ui
@pytest.mark.smoke
def test_view_product_details(page, products_page):
    products_page.open_product(settings.KNOWN_PRODUCT_ID)

    details = ProductDetailsPage(page)
    assert details.current_path() == f"/product_details/{settings.KNOWN_PRODUCT_ID}"
    expect(details.name).to_have_text(settings.KNOWN_PRODUCT_NAME)
    expect(details.category).to_contain_text(settings.KNOWN_PRODUCT_CATEGORY)
    expect(details.price).to_contain_text(f"Rs. {settings.KNOWN_PRODUCT_PRICE}")
    expect(details.availability).to_be_visible()
    expect(details.condition).to_be_visible()
    expect(details.brand).to_contain_text(settings.KNOWN_PRODUCT_BRAND)
