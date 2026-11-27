from urllib.parse import urlparse

from config import settings


class SiteOverloadedError(Exception):
    pass


class BasePage:
    path = "/"

    def open(self, path=None):
        target = self.path if path is None else path
        self.page.goto(f"{settings.BASE_URL}{target}", wait_until="domcontentloaded")
        self._reload_while_overloaded()
        return self

    def click_and_wait(self, locator):
        with self.page.expect_navigation(wait_until="domcontentloaded"):
            locator.click()
            
        self._reload_while_overloaded()

    def current_path(self):
        return urlparse(self.page.url).path

    def page_title(self):
        return self.page.title()

    def scroll_to(self, locator):
        locator.scroll_into_view_if_needed()

    def _is_overloaded(self):
        return self.page.locator("h2", has_text="under heavy load").count() > 0

    def _reload_while_overloaded(self):

        for attempt in range(1, settings.OVERLOAD_RETRIES + 1):
            if not self._is_overloaded():
                return
            self.page.wait_for_timeout(settings.OVERLOAD_WAIT_MS * attempt)
            self.page.reload(wait_until="domcontentloaded")


        if self._is_overloaded():
            raise SiteOverloadedError(
                f"{self.page.url} still answers 'queue full' after {settings.OVERLOAD_RETRIES} reloads"
            )
