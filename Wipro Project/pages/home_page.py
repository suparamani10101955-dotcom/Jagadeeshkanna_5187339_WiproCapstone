from __future__ import annotations

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from config.settings import settings
from locators.home_locators import HomeLocators
from pages.base_page import BasePage, Locator


class HomePage(BasePage):
    def load(self) -> None:
        self.open(settings.base_url)
        self.accept_cookies_if_present()

    def open(self, url: str) -> None:
        super().open(url)
        self.accept_cookies_if_present()

    def accept_cookies_if_present(self) -> None:
        try:
            self.click_first_available((HomeLocators.COOKIE_OK_BUTTON,), timeout=3)
        except Exception:
            self.logger.info("Cookie confirmation was not shown.")

    def open_login(self) -> None:
        icon = self.find_first_visible(HomeLocators.LOGIN_ICON, timeout=30)
        ActionChains(self.driver).move_to_element(icon).perform()
        self.logger.info("Hovered on login icon: %s", HomeLocators.LOGIN_ICON)
        try:
            self.click_first_available(HomeLocators.LOGIN_ENTRY_POINTS, timeout=8)
            return
        except TimeoutException:
            self.logger.info("Login menu entry points were not clickable after hover; trying icon click fallback.")

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", icon)
        self.driver.execute_script("arguments[0].click();", icon)
        self.wait_for_page_load(timeout=5)
        self.click_first_available(HomeLocators.LOGIN_ENTRY_POINTS, timeout=8)

    def search_property(self, location: str) -> None:
        try:
            self.search_property_from_landmark_bar(location)
            return
        except Exception as exc:
            self.logger.info("Landmark search flow was unavailable. Falling back to generic search input: %s", exc)

        search_box: WebElement | None = None
        last_error: Exception | None = None
        for locator in HomeLocators.SEARCH_INPUTS:
            try:
                candidate = self.find_first_visible(locator)
                if candidate is None:
                    continue
                tag_name = candidate.tag_name.lower()
                if tag_name not in {"input", "textarea"} and candidate.get_attribute("contenteditable") != "true":
                    continue
                search_box = candidate
                break
            except Exception as exc:
                last_error = exc
        if search_box is None:
            raise AssertionError("Search input was not available on the home page.") from last_error

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_box)
        if search_box.get_attribute("contenteditable") == "true":
            self.driver.execute_script("arguments[0].textContent = '';", search_box)
            search_box.send_keys(location)
        else:
            search_box.clear()
            search_box.send_keys(location)
        self.click_first_available(HomeLocators.SEARCH_BUTTONS)

    def search_property_from_landmark_bar(self, location: str) -> None:
        try:
            self.find_first_visible(HomeLocators.LANDMARK_SEARCH_BAR, timeout=10)
        except TimeoutException:
            current_url = self.driver.current_url.lower()
            if "search/property" in current_url and location.lower() in self.driver.page_source.lower():
                self.logger.info(
                    "Landmark search bar was not visible because current page is already a %s results page.",
                    location,
                )
                return
            raise
        search_box = self.find_first_visible(HomeLocators.LANDMARK_SEARCH_INPUT)
        search_box.clear()
        search_box.send_keys(location)
        self.click_first_available(
            ((By.XPATH, f"//*[@id='suggestions_custom']/li[@title={self._xpath_literal(location)}]"),),
            timeout=10,
        )
        self.click_first_available((HomeLocators.SEARCH_ICON_BY_ID,), timeout=10)

    def are_primary_menu_items_visible(self, expected_items: list[str] | tuple[str, ...]) -> bool:
        missing_items = [item for item in expected_items if not self.visible_text_present(item, timeout=5)]
        if missing_items:
            self.logger.error("Missing primary menu items: %s", missing_items)
        return not missing_items
