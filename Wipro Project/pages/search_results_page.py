from __future__ import annotations

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings
from locators.search_results_locators import SearchResultsLocators
from pages.base_page import BasePage, Locator


class SearchResultsPage(BasePage):
    def has_results_loaded(self) -> bool:
        return self.is_visible(SearchResultsLocators.RESULTS_CONTAINER, timeout=20)

    def page_contains_location(self, location: str) -> bool:
        return location.lower() in self.driver.page_source.lower()

    def apply_budget_range_from_requested_xpaths(self) -> None:
        self.wait_for_page_load()
        self.click_first_available((SearchResultsLocators.BUDGET_MIN_DROPDOWN,), timeout=20)
        self.click_first_available((SearchResultsLocators.BUDGET_MIN_OPTION,), timeout=10)
        try:
            self.click_first_available((SearchResultsLocators.BUDGET_MAX_DROPDOWN,), timeout=10)
        except TimeoutException:
            self.logger.info("Requested max-budget dropdown XPath was unavailable; using visible max-budget control.")
            self.click_first_available((SearchResultsLocators.BUDGET_MAX_DROPDOWN_FALLBACK,), timeout=10)
        self.click_first_available((SearchResultsLocators.BUDGET_MAX_OPTION,), timeout=10)
        self.wait_for_page_load()
        if not self.has_results_loaded():
            raise AssertionError("Results were not visible after applying the budget range.")

    def apply_requested_property_details_filters(self) -> None:
        self.wait_for_page_load()
        self._scroll_click_first_available(
            (SearchResultsLocators.PROPERTY_TYPE_SECTION, SearchResultsLocators.PROPERTY_TYPE_SECTION_FALLBACK)
        )
        self._wait_for_dynamic_filters()
        self._scroll_click_first_available((SearchResultsLocators.OWNER_OPTION,))
        self._wait_for_dynamic_filters()

        self._ensure_bedroom_filters_available()
        self._wait_for_first_visible(
            (SearchResultsLocators.BHK_FILTER_OPTION_ONE, SearchResultsLocators.BHK_FILTER_OPTION_ONE_FALLBACK),
            timeout=10,
        )
        self._scroll_click_first_available(
            (SearchResultsLocators.BHK_FILTER_OPTION_ONE, SearchResultsLocators.BHK_FILTER_OPTION_ONE_FALLBACK)
        )
        self._wait_for_dynamic_filters()
        self._wait_for_first_visible(
            (SearchResultsLocators.BHK_FILTER_OPTION_TWO, SearchResultsLocators.BHK_FILTER_OPTION_TWO_FALLBACK),
            timeout=10,
        )
        self._scroll_click_first_available(
            (SearchResultsLocators.BHK_FILTER_OPTION_TWO, SearchResultsLocators.BHK_FILTER_OPTION_TWO_FALLBACK)
        )
        self._wait_for_dynamic_filters()
        self._scroll_click_first_available((SearchResultsLocators.FURNISHING_OPTION, SearchResultsLocators.FURNISHING_SECTION))
        self._scroll_click_optional((SearchResultsLocators.FURNISHING_OPTION_FALLBACK,))
        self._scroll_click_first_available(
            (SearchResultsLocators.ADDITIONAL_FILTER_OPTION_ONE, SearchResultsLocators.ADDITIONAL_FILTER_OPTION_ONE_FALLBACK)
        )
        self._scroll_click_first_available(
            (SearchResultsLocators.ADDITIONAL_FILTER_OPTION_TWO, SearchResultsLocators.ADDITIONAL_FILTER_OPTION_TWO_FALLBACK)
        )
        self.wait_for_page_load()
        self._click_final_action_button()
        self._wait_for_dynamic_filters(timeout=20)
        if not self.has_results_loaded():
            raise AssertionError("Results were not visible after applying property detail filters.")

    def has_applied_filters_visible(self) -> bool:
        return self.is_visible(SearchResultsLocators.ACTIVE_FILTER_BADGES, timeout=10) or self.is_visible(
            SearchResultsLocators.SORT_OR_FILTER_PANEL, timeout=10
        )

    def open_first_property(self) -> None:
        href = self._extract_first_property_href()
        if href:
            self.logger.info("Opening first property by direct navigation: %s", href)
            self.driver.get(href)
            self.wait_for_page_load()
            return

        original_window = self.driver.current_window_handle
        original_handles = set(self.driver.window_handles)
        for locator in SearchResultsLocators.FIRST_PROPERTY_LINKS:
            try:
                element = self.find_first_visible(locator, timeout=8)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                self.driver.execute_script("arguments[0].removeAttribute('target');", element)
                self.driver.execute_script("arguments[0].click();", element)
                WebDriverWait(self.driver, 10).until(lambda driver: driver.current_url != "")
                new_handles = set(self.driver.window_handles) - original_handles
                if new_handles:
                    self.switch_to_new_window(original_handles, timeout=10)
                self.wait_for_page_load()
                return
            except Exception as exc:
                self.logger.info("Failed to open property with locator %s: %s", locator, exc)
                continue

        raise TimeoutException("Unable to open any property details link from the search results page.")

    def _extract_first_property_href(self) -> str | None:
        hrefs = self.driver.execute_script(
            """
            const selectors = [
              "a[href*='/property-in-']",
              "a[href*='/buy/']",
              "a[href*='/project-']",
              "a[href*='property']",
              "a[href*='project']"
            ];
            const results = [];
            for (const selector of selectors) {
              const elements = document.querySelectorAll(selector);
              for (const element of elements) {
                if (!element || !element.href) continue;
                const rect = element.getBoundingClientRect();
                const visible = rect.width > 0 && rect.height > 0;
                if (visible) results.push(element.href);
              }
              if (results.length) break;
            }
            return results;
            """
        )
        if hrefs:
            return hrefs[0]
        return None

    def _ensure_bedroom_filters_available(self) -> None:
        if self.is_visible(SearchResultsLocators.BHK_FILTER_OPTION_ONE_FALLBACK, timeout=3):
            return
        self.logger.info("Bedroom filters are unavailable after property-type click; selecting Residential Apartment.")
        self._scroll_click_first_available((SearchResultsLocators.RESIDENTIAL_APARTMENT_OPTION,), timeout=10)
        self._wait_for_dynamic_filters()
        self._wait_for_first_visible(
            (SearchResultsLocators.BHK_FILTER_OPTION_ONE, SearchResultsLocators.BHK_FILTER_OPTION_ONE_FALLBACK),
            timeout=10,
        )

    def _scroll_click_first_available(self, locators: tuple[Locator, ...], timeout: int = 8) -> None:
        for locator in locators:
            try:
                self.scroll_and_click(locator, timeout=timeout)
                self.logger.info("Clicked requested filter locator: %s", locator)
                return
            except (StaleElementReferenceException, TimeoutException):
                self.logger.info("Filter locator was unavailable or stale, trying fallback: %s", locator)
                continue
        raise TimeoutException(f"None of the requested filter locators were clickable: {locators}")

    def _scroll_click_optional(self, locators: tuple[Locator, ...], timeout: int = 5) -> None:
        try:
            self._scroll_click_first_available(locators, timeout=timeout)
        except TimeoutException:
            self.logger.info("Optional filter locator was unavailable or already selected: %s", locators)

    def _wait_for_dynamic_filters(self, timeout: int | None = None) -> None:
        wait_timeout = timeout or settings.explicit_wait
        WebDriverWait(self.driver, wait_timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def _wait_for_first_visible(self, locators: tuple[Locator, ...], timeout: int = 10) -> Locator:
        last_error: TimeoutException | None = None
        for locator in locators:
            try:
                WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
                return locator
            except TimeoutException as exc:
                last_error = exc
                continue
        raise TimeoutException(f"None of the dynamic filter locators became visible: {locators}") from last_error

    def _click_final_action_button(self, timeout: int = 15) -> None:
        self._wait_for_dynamic_filters(timeout=timeout)
        last_error: TimeoutException | None = None
        for locator in SearchResultsLocators.FINAL_ACTION_BUTTON_FALLBACKS:
            try:
                element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                try:
                    element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(locator))
                    self.driver.execute_script("arguments[0].click();", element)
                except TimeoutException:
                    self.logger.info("Final action locator was present but not clickable; using JavaScript click: %s", locator)
                    self.driver.execute_script("arguments[0].click();", element)
                self.logger.info("Clicked final action button after filters were applied: %s", locator)
                return
            except TimeoutException as exc:
                last_error = exc
                self.logger.info("Final action locator was not present, trying fallback: %s", locator)

        js_element = None
        for locator in SearchResultsLocators.FINAL_ACTION_BUTTON_FALLBACKS:
            if locator[0] != By.XPATH:
                continue
            js_element = self.find_by_xpath_js(locator[1])
            if js_element is not None:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", js_element)
                self.driver.execute_script("arguments[0].click();", js_element)
                self.logger.info("Clicked final action button through JavaScript XPath evaluation: %s", locator)
                return

        raise TimeoutException(
            f"None of the final action button locators were present after filters: {SearchResultsLocators.FINAL_ACTION_BUTTON_FALLBACKS}"
        ) from last_error
