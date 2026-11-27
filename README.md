# E-Commerce Website – End-to-End Test Automation

UI and REST API test automation for [automationexercise.com](https://automationexercise.com/) built with
Python, Playwright, Pytest and pytest-html. UI flows follow the Page Object Model; API scenarios use
`requests` through a small shared client.

## Project layout

```
config/            central settings (URLs, timeouts, known test data, report paths)
pages/             page objects for every screen touched by the UI suite
utils/             API client, test data factory, shared UI flow helper
tests/
  conftest.py      browser context fixture, ad blocking, screenshot-on-failure hook
  ui/              UI scenarios + UI fixtures
  api/             REST scenarios + API fixtures
.github/workflows/ GitHub Actions pipeline
reports/           generated HTML reports and failure screenshots (git-ignored)
```

## Prerequisites

- Python 3.10 or newer
- Git
- Internet access to `https://automationexercise.com`

## Installation

```bash
git clone <your-repo-url>
cd ecommerce-e2e-test-automation
python -m venv .venv
```

Activate the virtual environment (Windows / Linux-macOS):

```bash
.venv\Scripts\activate
```

```bash
source .venv/bin/activate
```

Install the dependencies and the browser used by Playwright:

```bash
pip install -r requirements.txt
```

```bash
python -m playwright install chromium
```

## Running the tests

Everything:

```bash
pytest
```

Only the API suite / only the UI suite:

```bash
pytest -m api
```

```bash
pytest -m ui
```

A single file or a single test:

```bash
pytest tests/ui/test_cart.py
```

```bash
pytest tests/api/test_account_api.py::test_delete_user_account
```

Other markers: `smoke`, `regression`, `negative`.

UI runs are headless Chromium by default. The usual pytest-playwright switches work:

```bash
pytest -m ui --headed --slowmo 300
```

```bash
pytest -m ui --browser firefox
```

## Configuration

Settings live in `config/settings.py`. Values that differ per environment can be overridden with
environment variables:

| Variable               | Default                          | Purpose                                         |
|------------------------|----------------------------------|-------------------------------------------------|
| `AE_BASE_URL`          | `https://automationexercise.com` | UI base URL                                     |
| `AE_API_BASE_URL`      | same as `AE_BASE_URL`            | API base URL                                    |
| `AE_UI_TIMEOUT_MS`     | `15000`                          | Playwright action / assertion timeout           |
| `AE_API_TIMEOUT_S`     | `20`                             | Timeout for API calls                           |
| `AE_OVERLOAD_RETRIES`  | `3`                              | Retries when the site answers "queue full"      |
| `AE_OVERLOAD_WAIT_MS`  | `3000`                           | Base wait between those retries                 |
| `AE_TEST_PASSWORD`     | `Secret@123`                     | Password for generated test accounts            |
| `AE_TEST_EMAIL_DOMAIN` | `example.com`                    | Domain for generated test emails                |

## Reports and screenshots

- Every run writes a self-contained HTML report to `reports/report.html`.
- When a UI test fails, a full-page screenshot is saved under `reports/screenshots/` and embedded in
  the HTML report together with the URL the test was on.

## What is covered

UI (`tests/ui`)

| # | Scenario                              | Test                                                              |
|---|---------------------------------------|-------------------------------------------------------------------|
| 1 | Home page loads                       | `test_home_page.py::test_home_page_loads_successfully`            |
| 2 | Register a new user                   | `test_registration.py::test_register_new_user`                    |
| 3 | Verify account creation               | `test_registration.py::test_account_created_successfully`         |
| 4 | Login with valid credentials          | `test_login.py::test_login_with_valid_credentials`                |
| 5 | Login with invalid credentials        | `test_login.py::test_login_with_invalid_credentials`              |
| 6 | Logout                                | `test_login.py::test_logout`                                      |
| 7 | Navigate to Products                  | `test_products.py::test_navigate_to_products_page`                |
| 8 | Search product and verify results     | `test_products.py::test_search_product`                           |
| 9 | View product details                  | `test_products.py::test_view_product_details`                     |
| 10| Add product to cart                   | `test_cart.py::test_add_product_to_cart`                          |
| 11| Product details and quantity in cart  | `test_cart.py::test_cart_product_details_and_quantity`            |
| 12| Remove product from cart              | `test_cart.py::test_remove_product_from_cart`                     |
| 13| Product categories                    | `test_categories_and_brands.py::test_navigate_product_categories` |
| 14| Product brands                        | `test_categories_and_brands.py::test_navigate_product_brands`     |
| 15| Subscription                          | `test_subscription.py::test_subscription_from_home_page`          |

API (`tests/api`)

| # | Scenario                  | Method | Endpoint                    | File                   |
|---|---------------------------|--------|-----------------------------|------------------------|
| 1 | Get all products          | GET    | `/api/productsList`         | `test_products_api.py` |
| 2 | Get all brands            | GET    | `/api/brandsList`           | `test_brands_api.py`   |
| 3 | Search products           | POST   | `/api/searchProduct`        | `test_products_api.py` |
| 4 | Verify login              | POST   | `/api/verifyLogin`          | `test_account_api.py`  |
| 5 | Create user account       | POST   | `/api/createAccount`        | `test_account_api.py`  |
| 6 | Update user account       | PUT    | `/api/updateAccount`        | `test_account_api.py`  |
| 7 | Delete user account       | DELETE | `/api/deleteAccount`        | `test_account_api.py`  |
| 8 | Get user details by email | GET    | `/api/getUserDetailByEmail` | `test_account_api.py`  |

Negative API checks: search without `search_product`, login with invalid credentials, login without
email and/or password, POST on `productsList`, PUT on `brandsList`, delete with a wrong password and
user lookup without an email.

## CI – GitHub Actions

`.github/workflows/tests.yml` runs on pushes to `main`/`master`, on pull requests and on manual dispatch.
It installs the requirements and Chromium, runs the API suite and the UI suite as separate steps and
uploads the `reports/` folder (HTML reports + failure screenshots) as the `test-reports` artifact.
The artifact is available from the **Artifacts** section of the workflow run.

## Notes

- The site answers HTTP 200 for API calls and puts the real status in `responseCode` inside the JSON
  body, so API tests assert on both.
- It is a shared public demo and sometimes replies with a "This website is under heavy load (queue full)"
  page. `BasePage` reloads when it sees that page and `ApiClient` retries the call; in CI the UI step
  additionally reruns a failed test once (`--reruns 1`).
- Accounts needed by tests are created through the API with unique emails and deleted in fixture
  teardown, so runs don't depend on pre-existing data.
- Google ad requests are blocked at context level because the ad overlays intercept clicks.
