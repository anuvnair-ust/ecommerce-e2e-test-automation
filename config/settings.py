import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

BASE_URL = os.getenv("AE_BASE_URL", "https://automationexercise.com").rstrip("/")
API_BASE_URL = os.getenv("AE_API_BASE_URL", BASE_URL).rstrip("/")

RUNNING_IN_CI = os.getenv("CI", "").lower() == "true"
HEADLESS = os.getenv("AE_HEADLESS", str(RUNNING_IN_CI)).lower() == "true"

UI_TIMEOUT_MS = int(os.getenv("AE_UI_TIMEOUT_MS", "15000"))
NAVIGATION_TIMEOUT_MS = int(os.getenv("AE_NAVIGATION_TIMEOUT_MS", "45000"))
API_TIMEOUT_S = int(os.getenv("AE_API_TIMEOUT_S", "20"))
OVERLOAD_RETRIES = int(os.getenv("AE_OVERLOAD_RETRIES", "3"))
OVERLOAD_WAIT_MS = int(os.getenv("AE_OVERLOAD_WAIT_MS", "3000"))

TEST_PASSWORD = os.getenv("AE_TEST_PASSWORD", "Secret@123")
TEST_EMAIL_DOMAIN = os.getenv("AE_TEST_EMAIL_DOMAIN", "example.com")

KNOWN_PRODUCT_ID = 1
KNOWN_PRODUCT_NAME = "Blue Top"
KNOWN_PRODUCT_PRICE = 500
KNOWN_PRODUCT_CATEGORY = "Women > Tops"
KNOWN_PRODUCT_BRAND = "Polo"
SEARCH_TERM = "top"
KNOWN_CATEGORY = "Women"
KNOWN_SUBCATEGORY = "Dress"
KNOWN_BRAND = "Polo"

REPORTS_DIR = ROOT_DIR / "reports"
SCREENSHOT_DIR = REPORTS_DIR / "screenshots"
HTML_REPORT_PATH = REPORTS_DIR / "report.html"
