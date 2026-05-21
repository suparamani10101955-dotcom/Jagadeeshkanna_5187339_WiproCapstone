from __future__ import annotations

from collections.abc import Iterable

from selenium.common.exceptions import NoSuchWindowException, StaleElementReferenceException, TimeoutException, WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings


class WaitUtils:
    def __init__(self, driver: WebDriver, timeout: int | None = None) -> None:
        self.driver = driver
        self.timeout = timeout or settings.explicit_wait

    def until_visible(self, locator: tuple[str, str], timeout: int | None = None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(EC.visibility_of_element_located(locator))

    def until_clickable(self, locator: tuple[str, str], timeout: int | None = None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(EC.element_to_be_clickable(locator))

    def until_present(self, locator: tuple[str, str], timeout: int | None = None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(EC.presence_of_element_located(locator))

    def until_url_contains(self, value: str, timeout: int | None = None) -> bool:
        return WebDriverWait(self.driver, timeout or self.timeout).until(EC.url_contains(value))

    def until_page_ready(self, timeout: int | None = None) -> None:
        wait_timeout = timeout or settings.page_load_timeout
        WebDriverWait(
            self.driver,
            wait_timeout,
            ignored_exceptions=(StaleElementReferenceException, WebDriverException, NoSuchWindowException),
        ).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        WebDriverWait(
            self.driver,
            wait_timeout,
            ignored_exceptions=(StaleElementReferenceException, WebDriverException, NoSuchWindowException),
        ).until(lambda driver: driver.execute_script("return !!document.body"))

    def any_visible(self, locators: tuple[tuple[str, str], ...], timeout: int | None = None) -> bool:
        for locator in locators:
            try:
                self.until_visible(locator, timeout=timeout)
                return True
            except TimeoutException:
                continue
        return False

    def first_visible(self, locators: Iterable[tuple[str, str]], timeout: int | None = None) -> WebElement:
        last_error: TimeoutException | None = None
        for locator in locators:
            try:
                return self.until_visible(locator, timeout=timeout)
            except TimeoutException as exc:
                last_error = exc
                continue
        raise TimeoutException(f"No locator became visible: {list(locators)}") from last_error

    def until_new_window(self, previous_handles: set[str], timeout: int | None = None) -> set[str]:
        wait_timeout = timeout or self.timeout
        return WebDriverWait(self.driver, wait_timeout).until(
            lambda driver: set(driver.window_handles) - previous_handles
        )
