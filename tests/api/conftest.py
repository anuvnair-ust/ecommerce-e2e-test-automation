import pytest

from utils.data_factory import build_user


@pytest.fixture
def api_user(api_client):
    user = build_user()
    created = api_client.create_account(user)
    assert created.json().get("responseCode") == 201, created.text
    yield user
    api_client.remove_account_quietly(user.email, user.password)
