import pytest

from utils.data_factory import build_user, unique_email


@pytest.mark.api
@pytest.mark.regression
def test_verify_login_with_valid_credentials(api_client, api_user):
    response = api_client.verify_login(api_user.email, api_user.password)

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert body["message"] == "User exists!"


@pytest.mark.api
@pytest.mark.negative
def test_verify_login_with_invalid_credentials_returns_404(api_client):
    response = api_client.verify_login(unique_email("ghost"), "NotAPassword1")

    body = response.json()
    assert body["responseCode"] == 404
    assert body["message"] == "User not found!"


@pytest.mark.api
@pytest.mark.negative
@pytest.mark.parametrize(
    "fields",
    [
        {"password": "Secret@123"},
        {"email": "someone@example.com"},
        {},
    ],
    ids=["missing_email", "missing_password", "missing_both"],
)
def test_verify_login_without_required_fields_returns_400(api_client, fields):
    response = api_client.verify_login(**fields)

    body = response.json()
    assert body["responseCode"] == 400
    assert body["message"] == "Bad request, email or password parameter is missing in POST request."


@pytest.mark.api
@pytest.mark.smoke
def test_create_user_account(api_client):
    user = build_user()

    response = api_client.create_account(user)
    try:
        assert response.status_code == 200
        body = response.json()
        assert body["responseCode"] == 201
        assert body["message"] == "User created!"
    finally:
        api_client.remove_account_quietly(user.email, user.password)


@pytest.mark.api
@pytest.mark.regression
def test_update_user_account(api_client, api_user):
    new_name = api_user.name + " Updated"

    response = api_client.update_account(api_user, name=new_name, city="Vancouver")

    body = response.json()
    assert body["responseCode"] == 200
    assert body["message"] == "User updated!"

    details = api_client.get_user_by_email(api_user.email).json()
    assert details["user"]["name"] == new_name
    assert details["user"]["city"] == "Vancouver"


@pytest.mark.api
@pytest.mark.regression
def test_delete_user_account(api_client):
    user = build_user()
    assert api_client.create_account(user).json()["responseCode"] == 201

    response = api_client.delete_account(user.email, user.password)

    body = response.json()
    assert body["responseCode"] == 200
    assert body["message"] == "Account deleted!"

    after = api_client.get_user_by_email(user.email).json()
    assert after["responseCode"] == 404


@pytest.mark.api
@pytest.mark.negative
def test_delete_account_with_wrong_password_returns_404(api_client, api_user):
    response = api_client.delete_account(api_user.email, "WrongPass#999")

    body = response.json()
    assert body["responseCode"] == 404
    assert body["message"] == "Account not found!"


@pytest.mark.api
@pytest.mark.regression
def test_get_user_detail_by_email(api_client, api_user):
    response = api_client.get_user_by_email(api_user.email)

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert body["user"]["email"] == api_user.email
    assert body["user"]["name"] == api_user.name
    assert body["user"]["first_name"] == api_user.first_name
    assert body["user"]["last_name"] == api_user.last_name


@pytest.mark.api
@pytest.mark.negative
def test_get_user_detail_without_email_returns_400(api_client):
    body = api_client.get_user_by_email().json()

    assert body["responseCode"] == 400
    assert body["message"] == "Bad request, email parameter is missing in GET request."
