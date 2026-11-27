import base64
import re

import pytest
from playwright.sync_api import Error as PlaywrightError, expect
from pytest_html import extras

from config import settings
from utils.api_client import ApiClient


BLOCKED_HOSTS = ("doubleclick.net", "googlesyndication.com", "googleadservices.com")


def pytest_configure(config):
    settings.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    expect.set_options(timeout=settings.UI_TIMEOUT_MS)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1366, "height": 850},
        "ignore_https_errors": True,
    }


@pytest.fixture
def context(browser, browser_context_args):
    context = browser.new_context(**browser_context_args)
    context.set_default_timeout(settings.UI_TIMEOUT_MS)
    context.route("**/*", _filter_ad_requests)
    yield context
    context.close()


@pytest.fixture(scope="session")
def api_client():
    return ApiClient()


def _filter_ad_requests(route):
    if any(host in route.request.url for host in BLOCKED_HOSTS):
        route.abort()
    else:
        route.continue_()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return
    page = item.funcargs.get("page")
    if page is None:
        return

    file_name = re.sub(r"[^\w.-]+", "_", item.nodeid).strip("_") + ".png"
    try:
        image = page.screenshot(path=str(settings.SCREENSHOT_DIR / file_name), full_page=True)
    except PlaywrightError:
        return

    report.extras = getattr(report, "extras", []) + [
        extras.png(base64.b64encode(image).decode("ascii"), name="Screenshot"),
        extras.url(page.url, name="Failing URL"),
    ]
