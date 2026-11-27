import pytest

from config import settings
from pages.cart_modal import CartModal
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.product_details_page import ProductDetailsPage
from pages.account_page import AccountPage
from utils.data_factory import build_user


@pytest.fixture
def home_page(page):
    return HomePage(page).open()


@pytest.fixture
def login_page(page):
    return LoginPage(page).open()


@pytest.fixture
def products_page(page):
    return ProductsPage(page).open()


@pytest.fixture
def product_details_page(page):
    return ProductDetailsPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def cart_modal(page):
    return CartModal(page)


@pytest.fixture
def account_page(page):
    return AccountPage(page)


@pytest.fixture
def existing_user(api_client):
    user = build_user()
    response = api_client.create_account(user)
    assert response.json().get("responseCode") == 201, f"Setup failed to create user: {response.text}"
    yield user
    api_client.remove_account_quietly(user.email, user.password)


@pytest.fixture
def new_user_data():
    return build_user()


@pytest.fixture
def signup_user_cleanup(api_client, new_user_data):
    yield new_user_data
    api_client.remove_account_quietly(new_user_data.email, new_user_data.password)


@pytest.fixture
def logged_in_user(page, existing_user):
    login = LoginPage(page).open()
    login.login(existing_user.email, existing_user.password)
    HomePage(page).logged_in_as.wait_for(state="visible")
    return existing_user


@pytest.fixture
def product_in_cart(product_details_page, cart_modal):
    product_details_page.open_product(settings.KNOWN_PRODUCT_ID)
    product_details_page.add_to_cart()
    cart_modal.wait_until_visible()
    cart_modal.view_cart()
    return settings.KNOWN_PRODUCT_NAME
