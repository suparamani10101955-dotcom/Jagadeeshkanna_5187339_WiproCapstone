from __future__ import annotations

import allure
import pytest

from tests.base_test import BaseTest


@allure.epic("99acres")
@allure.feature("Individual Functional Test Cases")
class Test99AcresIndividualCase(BaseTest):
    @allure.title("Verify the login dialog opens from the home page")
    @pytest.mark.login
    @pytest.mark.smoke
    def test_login_dialog_opens(self, base_url: str) -> None:
        with allure.step("Open the home page and login dialog"):
            self.home_page.open(base_url)
            self.home_page.open_login()
            self.capture_step_screenshot("individual_login_dialog_opened")

        assert self.login_page.is_login_dialog_displayed(), "Login dialog should be visible after clicking login."

    @allure.title("Verify the user can submit a valid mobile number in the login flow")
    @pytest.mark.login
    def test_login_with_mobile_number(self, base_url: str, test_data: dict) -> None:
        with allure.step("Start login flow with mobile number"):
            mobile_number = self.start_login_flow(base_url, test_data)
            self.capture_step_screenshot("individual_login_completed")

        assert mobile_number, "A mobile number should be available for the login test."
        assert "99acres" in self.driver.title.lower(), "The 99acres page title should remain available after login."

    @allure.title("Verify Mumbai property search loads results")
    @pytest.mark.search
    @pytest.mark.smoke
    def test_property_search_by_location(self, base_url: str, test_data: dict) -> None:
        location = test_data["property_search"]["default_location"]

        with allure.step("Search properties by location"):
            self.home_page.open(base_url)
            self.home_page.search_property(location)
            self.capture_step_screenshot("individual_property_search_results")

        assert self.results_page.has_results_loaded(), "Search results should be displayed after a valid search."
        assert self.results_page.page_contains_location(location), f"Search results should contain '{location}'."

    @allure.title("Verify budget and property filters can be applied on Mumbai search results")
    @pytest.mark.filters
    def test_apply_filters_on_mumbai_properties(self, base_url: str, test_data: dict) -> None:
        location = test_data["property_search"]["filtered_location"]

        with allure.step("Open Mumbai search results"):
            self.home_page.open(base_url)
            self.home_page.search_property_from_landmark_bar(location)
            self.capture_step_screenshot("individual_filter_results_loaded")
        assert self.results_page.has_results_loaded(), "Results page should load before applying filters."

        with allure.step("Apply requested property filters"):
            self.results_page.apply_budget_range_from_requested_xpaths()
            self.results_page.apply_requested_property_details_filters()
            self.capture_step_screenshot("individual_filters_applied")

        assert self.results_page.has_results_loaded(), "Results should remain visible after filter application."
        assert self.results_page.has_applied_filters_visible(), "Applied filters should be visible in the results page."
        assert self.results_page.page_contains_location(location), f"Filtered results should still contain '{location}'."

    @allure.title("Verify a property details page opens from search results")
    @pytest.mark.details
    def test_property_details_validation(self, base_url: str, test_data: dict) -> None:
        location = test_data["property_search"]["filtered_location"]

        with allure.step("Search properties before opening details"):
            self.home_page.open(base_url)
            self.home_page.search_property(location)
            self.capture_step_screenshot("individual_property_search_before_details")
        assert self.results_page.has_results_loaded(), "Results page should load before opening property details."

        with allure.step("Open first property details page"):
            self.results_page.open_first_property()
            self.capture_step_screenshot("individual_property_details_opened")

        assert self.property_details_page.is_property_details_page_opened(), "Property details page should open."
        assert self.property_details_page.has_property_title(), "Property details page should show a title."
        assert self.property_details_page.has_price_information(), "Property details page should show price data."
        assert self.property_details_page.contains_location(location), (
            f"Property details page should reference the searched location '{location}'."
        )

    @allure.title("Verify a logged-in user can log out")
    @pytest.mark.logout
    def test_logout_flow(self, base_url: str, test_data: dict) -> None:
        with allure.step("Login before logout"):
            self.start_login_flow(base_url, test_data)
            self.capture_step_screenshot("individual_logout_precondition_login")

        with allure.step("Log out from the current session"):
            assert self.account_page.logout_if_available(), "Logout option should be available for a logged-in session."
            self.capture_step_screenshot("individual_logout_completed")

        assert self.account_page.is_logged_out(), "Login/Register entry should be visible after logout."
