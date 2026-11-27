import time

import requests
import truststore

from config import settings

truststore.inject_into_ssl()


class ApiClient:

    def __init__(self, base_url=settings.API_BASE_URL, timeout=settings.API_TIMEOUT_S):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _url(self, endpoint):
        return f"{self.base_url}/api/{endpoint.lstrip('/')}"

    def request(self, method, endpoint, **kwargs):
        url = self._url(endpoint)
        response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        attempt = 0
        while _is_overloaded(response) and attempt < settings.OVERLOAD_RETRIES:
            attempt += 1
            time.sleep(settings.OVERLOAD_WAIT_MS / 1000 * attempt)
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        return response

    def get_all_products(self):
        return self.request("GET", "productsList")

    def get_all_brands(self):
        return self.request("GET", "brandsList")

    def search_product(self, search_term=None):
        data = {} if search_term is None else {"search_product": search_term}
        return self.request("POST", "searchProduct", data=data)

    def verify_login(self, email=None, password=None):
        data = {}
        if email is not None:
            data["email"] = email
        if password is not None:
            data["password"] = password
        return self.request("POST", "verifyLogin", data=data)

    def create_account(self, user):
        return self.request("POST", "createAccount", data=user.account_payload())

    def update_account(self, user, **changes):
        payload = user.account_payload()
        payload.update(changes)
        return self.request("PUT", "updateAccount", data=payload)

    def delete_account(self, email, password):
        return self.request("DELETE", "deleteAccount", data={"email": email, "password": password})

    def get_user_by_email(self, email=None):
        params = {} if email is None else {"email": email}
        return self.request("GET", "getUserDetailByEmail", params=params)

    def remove_account_quietly(self, email, password):
        try:
            self.delete_account(email, password)
        except requests.RequestException:
            pass


def _is_overloaded(response):
    return response.status_code in (502, 503, 504) or "under heavy load" in response.text[:300]
