import pytest
from playwright.sync_api import expect

from config import settings


@pytest.mark.ui
@pytest.mark.smoke
def test_add_product_to_cart(page, product_details_page, cart_modal, cart_page):
    product_details_page.open_product(settings.KNOWN_PRODUCT_ID)
    product_details_page.add_to_cart()

    cart_modal.wait_until_visible()
    expect(cart_modal.message).to_contain_text("added to cart")

    cart_modal.view_cart()
    assert cart_page.current_path() == "/view_cart"
    assert cart_page.is_product_in_cart(settings.KNOWN_PRODUCT_NAME), "Product missing from cart"
    assert cart_page.item_count() == 1


@pytest.mark.ui
@pytest.mark.regression
def test_cart_product_details_and_quantity(page, product_details_page, cart_modal, cart_page):
    quantity = 3
    product_details_page.open_product(settings.KNOWN_PRODUCT_ID)
    product_details_page.set_quantity(quantity)
    product_details_page.add_to_cart()

    cart_modal.wait_until_visible()
    cart_modal.view_cart()

    name = settings.KNOWN_PRODUCT_NAME
    
    expect(cart_page.product_names).to_have_text([name])
    assert cart_page.quantity_of(name) == quantity
    assert cart_page.unit_price_of(name) == settings.KNOWN_PRODUCT_PRICE
    assert cart_page.total_of(name) == settings.KNOWN_PRODUCT_PRICE * quantity


@pytest.mark.ui
@pytest.mark.regression
def test_remove_product_from_cart(page, product_in_cart, cart_page):
    name = product_in_cart
    assert cart_page.is_product_in_cart(name)

    cart_page.remove_product(name)

    assert not cart_page.is_product_in_cart(name), "Product still listed after removal"
    expect(cart_page.empty_message).to_be_visible()
    expect(cart_page.empty_message).to_contain_text("Cart is empty!")
