import pytest

from config import settings


@pytest.mark.api
@pytest.mark.smoke
def test_get_all_products_returns_product_list(api_client):
    response = api_client.get_all_products()

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert isinstance(body["products"], list) and body["products"], "products list is empty"
    for product in body["products"]:
        for key in ("id", "name", "price", "brand", "category"):
            assert key in product, f"product {product.get('id')} is missing '{key}'"


@pytest.mark.api
@pytest.mark.regression
def test_search_product_returns_matching_products(api_client):
    response = api_client.search_product(settings.SEARCH_TERM)

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    products = body["products"]
    assert products, f"no products returned for '{settings.SEARCH_TERM}'"
    assert any(settings.SEARCH_TERM in product["name"].lower() for product in products)


@pytest.mark.api
@pytest.mark.negative
def test_search_product_without_search_parameter_returns_400(api_client):
    response = api_client.search_product()

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 400
    assert body["message"] == "Bad request, search_product parameter is missing in POST request."


@pytest.mark.api
@pytest.mark.negative
def test_post_to_products_list_is_not_supported(api_client):
    response = api_client.request("POST", "productsList")

    body = response.json()
    assert body["responseCode"] == 405
    assert body["message"] == "This request method is not supported."
