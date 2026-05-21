from __future__ import annotations

from collections.abc import Iterable

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    InvalidSessionIdException,
    NoSuchWindowException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings
from utilities.logger import get_logger
from utilities.wait_utils import WaitUtils

Locator = tuple[str, str]


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.explicit_wait)
        self.wait_utils = WaitUtils(driver)
        self.logger = get_logger(self.__class__.__name__)

    def open(self, url: str) -> None:
        self.ensure_session()
        self.logger.info("Opening URL: %s", url)
        self.driver.get(url)
        self.wait_for_page_load()

    def wait_for_page_load(self, timeout: int | None = None) -> None:
        self.ensure_session()
        self.wait_utils.until_page_ready(timeout=timeout)
        self.logger.info("Page loaded completely: %s", self.driver.current_url)

    def find(self, locator: Locator) -> WebElement:
        self.ensure_session()
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_visible(self, locator: Locator) -> WebElement:
        self.ensure_session()
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_first_visible(self, locator: Locator, timeout: int | None = None) -> WebElement:
        def _visible_element(driver: WebDriver) -> WebElement | bool:
            for element in driver.find_elements(*locator):
                try:
                    if element is not None and element.is_displayed():
                        return element
                except (StaleElementReferenceException, WebDriverException):
                    continue
            return False

        return WebDriverWait(
            self.driver,
            timeout or settings.explicit_wait,
            ignored_exceptions=(StaleElementReferenceException, WebDriverException, NoSuchWindowException),
        ).until(_visible_element)

    def find_first_present(self, locators: Iterable[Locator], timeout: int | None = None) -> WebElement:
        wait_timeout = timeout or settings.explicit_wait
        last_error: TimeoutException | None = None
        for locator in locators:
            try:
                return WebDriverWait(self.driver, wait_timeout).until(EC.presence_of_element_located(locator))
            except TimeoutException as exc:
                last_error = exc
                continue
        raise TimeoutException(f"None of the locators were present: {list(locators)}") from last_error

    def find_clickable(self, locator: Locator) -> WebElement:
        self.ensure_session()
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator: Locator) -> None:
        self.logger.info("Clicking element: %s", locator)
        self.find_clickable(locator).click()

    def js_click(self, locator: Locator) -> None:
        element = self.find_first_visible(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_and_click(self, locator: Locator, timeout: int | None = None, retries: int = 3) -> None:
        wait_timeout = timeout or settings.explicit_wait
        for attempt in range(retries):
            try:
                element = self.find_first_visible(locator, timeout=wait_timeout)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                element = WebDriverWait(self.driver, wait_timeout).until(EC.element_to_be_clickable(locator))
                self.driver.execute_script("arguments[0].click();", element)
                return
            except (StaleElementReferenceException, WebDriverException):
                self.logger.info("Stale element while clicking %s. Retry %s/%s.", locator, attempt + 1, retries)
                if attempt == retries - 1:
                    raise
            except ElementClickInterceptedException:
                if attempt == retries - 1:
                    raise
                self.wait_for_page_load(timeout=wait_timeout)

    def type_text(self, locator: Locator, text: str, clear: bool = True) -> None:
        element = self.find_visible(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Locator) -> str:
        return self.find_visible(locator).text.strip()

    def is_visible(self, locator: Locator, timeout: int | None = None) -> bool:
        try:
            WebDriverWait(self.driver, timeout or settings.explicit_wait).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def click_first_available(self, locators: Iterable[Locator], timeout: int = 5, retries: int = 3) -> Locator:
        for locator in locators:
            for attempt in range(retries):
                try:
                    element = self._first_clickable(locator, timeout)
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
                    self.driver.execute_script("arguments[0].click();", element)
                    self.logger.info("Clicked available locator: %s", locator)
                    return locator
                except (StaleElementReferenceException, WebDriverException):
                    self.logger.info("Stale element while clicking %s. Retry %s/%s.", locator, attempt + 1, retries)
                    if attempt == retries - 1:
                        break
                except ElementClickInterceptedException:
                    if attempt == retries - 1:
                        break
                    self.wait_for_page_load(timeout=timeout)
                except TimeoutException:
                    break
        raise TimeoutException(f"None of the locators were clickable: {list(locators)}")

    def _first_clickable(self, locator: Locator, timeout: int) -> WebElement:
        def _clickable_element(driver: WebDriver) -> WebElement | bool:
            for element in driver.find_elements(*locator):
                try:
                    if element is not None and element.is_displayed() and element.is_enabled():
                        return element
                except (StaleElementReferenceException, WebDriverException):
                    continue
            return False

        return WebDriverWait(
            self.driver,
            timeout,
            ignored_exceptions=(StaleElementReferenceException, WebDriverException, NoSuchWindowException),
        ).until(_clickable_element)

    def switch_to_new_window(self, previous_handles: set[str], timeout: int = 10) -> str:
        new_handles = self.wait_utils.until_new_window(previous_handles, timeout=timeout)
        handle = new_handles.pop()
        self.driver.switch_to.window(handle)
        self.logger.info("Switched to new window handle: %s", handle)
        return handle

    def ensure_session(self) -> None:
        try:
            _ = self.driver.current_url
        except (InvalidSessionIdException, NoSuchWindowException, WebDriverException) as exc:
            raise RuntimeError("The browser session is no longer available for interaction.") from exc

    def visible_text_present(self, text: str, timeout: int = 10) -> bool:
        xpath = (By.XPATH, f"//*[contains(normalize-space(), {self._xpath_literal(text)})]")
        return self.is_visible(xpath, timeout=timeout)

    def find_by_xpath_js(self, xpath: str) -> WebElement | None:
        element = self.driver.execute_script(
            """
            return document.evaluate(
                arguments[0],
                document,
                null,
                XPathResult.FIRST_ORDERED_NODE_TYPE,
                null
            ).singleNodeValue;
            """,
            xpath,
        )
        return element

    @staticmethod
    def _xpath_literal(value: str) -> str:
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        parts = value.split("'")
        return "concat(" + ', "\"\'\"", '.join(f"'{part}'" for part in parts) + ")"
