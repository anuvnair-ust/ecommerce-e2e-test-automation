import pytest


@pytest.mark.api
@pytest.mark.smoke
def test_get_all_brands_returns_brand_list(api_client):
    response = api_client.get_all_brands()

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert body["brands"], "brands list is empty"
    assert all("id" in brand and "brand" in brand for brand in body["brands"])


@pytest.mark.api
@pytest.mark.negative
def test_put_to_brands_list_is_not_supported(api_client):
    response = api_client.request("PUT", "brandsList")

    body = response.json()
    assert body["responseCode"] == 405
    assert body["message"] == "This request method is not supported."
