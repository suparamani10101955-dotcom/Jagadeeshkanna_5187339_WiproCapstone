from __future__ import annotations

import allure
import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage, LoginSessionExpiredError
from pages.search_results_page import SearchResultsPage
from tests.base_test import BaseTest
from utilities.logger import get_logger
from utilities.screenshot_utils import capture_screenshot


logger = get_logger("e2e")


@allure.epic("99acres")
@allure.feature("End-to-End Login and Property Search")
@pytest.mark.e2e
class Test99AcresEndToEnd(BaseTest):
    @allure.title("Complete login, Mumbai search, and filter flow in one browser session")
    def test_login_search_and_filter_mumbai_properties(self, base_url: str, test_data: dict) -> None:
        login_data = test_data["login"]
        search_data = test_data["property_search"]
        mobile_number = login_data.get("mobile_number") or login_data.get("username")
        otp_pause_seconds = int(login_data.get("otp_pause_seconds", 17))
        before_mobile_entry_pause_seconds = int(login_data.get("before_mobile_entry_pause_seconds", 0))
        after_mobile_entry_pause_seconds = int(login_data.get("after_mobile_entry_pause_seconds", 0))
        location = search_data["filtered_location"]
        if not mobile_number:
            pytest.skip("Set login.mobile_number in test_data/test_data.xml or ACRES_USERNAME in .env.")

        home_page = HomePage(self.driver)
        login_page = LoginPage(self.driver)
        results_page = SearchResultsPage(self.driver)

        with allure.step("Open 99acres home page and handle cookies"):
            logger.info("Opening home page for end-to-end flow: %s", base_url)
            home_page.open(base_url)
            home_page.wait_for_page_load()
            self._capture_step("01_home_page_opened")

        with allure.step("Open login popup and start mobile OTP login"):
            logger.info("Opening login popup from home page.")
            home_page.open_login()
            assert login_page.is_login_dialog_displayed(), "Login dialog was not displayed."
            self._capture_step("02_login_popup_opened")

            logger.info("Entering mobile number and pausing for manual OTP entry.")
            self._start_login_with_session_retry(
                home_page,
                login_page,
                base_url,
                mobile_number,
                otp_pause_seconds,
                before_mobile_entry_pause_seconds,
                after_mobile_entry_pause_seconds,
            )
            self._capture_step("03_after_manual_otp_pause")

        with allure.step("Search Mumbai properties"):
            logger.info("Searching properties for location: %s", location)
            home_page.search_property_from_landmark_bar(location)
            home_page.wait_for_page_load()
            assert results_page.has_results_loaded(), "Search results page did not load expected result content."
            self._capture_step("04_mumbai_results_loaded")

        with allure.step("Apply budget and property filters"):
            results_page.apply_budget_range_from_requested_xpaths()
            results_page.apply_requested_property_details_filters()
            self._capture_step("05_filters_applied")

        with allure.step("Validate filtered Mumbai search results"):
            assert results_page.has_results_loaded(), "Filtered search results page did not remain loaded."
            assert results_page.page_contains_location(location), f"Filtered search results should contain '{location}'."
            self._capture_step("06_e2e_flow_completed")

    def _capture_step(self, step_name: str) -> None:
        screenshot_path = capture_screenshot(self.driver, f"e2e_{step_name}")
        logger.info("Captured E2E step screenshot: %s", screenshot_path)

    def _start_login_with_session_retry(
        self,
        home_page: HomePage,
        login_page: LoginPage,
        base_url: str,
        mobile_number: str,
        otp_pause_seconds: int,
        before_mobile_entry_pause_seconds: int,
        after_mobile_entry_pause_seconds: int,
    ) -> None:
        try:
            login_page.start_mobile_login_and_pause_for_otp(
                mobile_number,
                otp_pause_seconds,
                before_mobile_entry_pause_seconds,
                after_mobile_entry_pause_seconds,
            )
            return
        except LoginSessionExpiredError:
            logger.info("Login session expired. Reopening home page and retrying login once.")

        home_page.open(base_url)
        home_page.open_login()
        assert login_page.is_login_dialog_displayed(), "Login dialog was not displayed after session retry."
        login_page.start_mobile_login_and_pause_for_otp(
            mobile_number,
            otp_pause_seconds,
            before_mobile_entry_pause_seconds,
            after_mobile_entry_pause_seconds,
        )
