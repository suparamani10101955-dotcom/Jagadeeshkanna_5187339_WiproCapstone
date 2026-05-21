from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from pages.account_page import AccountPage
from pages.home_page import HomePage
from pages.login_page import LoginPage, LoginSessionExpiredError
from pages.property_details_page import PropertyDetailsPage
from pages.search_results_page import SearchResultsPage
from utilities.logger import get_logger
from utilities.screenshot_utils import capture_screenshot


class BaseTest:
    driver: WebDriver
    logger = get_logger("tests")

    @property
    def home_page(self) -> HomePage:
        return HomePage(self.driver)

    @property
    def login_page(self) -> LoginPage:
        return LoginPage(self.driver)

    @property
    def results_page(self) -> SearchResultsPage:
        return SearchResultsPage(self.driver)

    @property
    def property_details_page(self) -> PropertyDetailsPage:
        return PropertyDetailsPage(self.driver)

    @property
    def account_page(self) -> AccountPage:
        return AccountPage(self.driver)

    def capture_step_screenshot(self, step_name: str) -> None:
        screenshot_path = capture_screenshot(self.driver, step_name)
        self.logger.info("Captured step screenshot: %s", screenshot_path)

    def start_login_flow(self, base_url: str, test_data: dict) -> str:
        login_data = test_data["login"]
        mobile_number = login_data.get("mobile_number") or login_data.get("username")
        if not mobile_number:
            raise AssertionError("Login test data is missing 'mobile_number' or 'username'.")

        self.home_page.open(base_url)
        self.home_page.open_login()
        assert self.login_page.is_login_dialog_displayed(), "Login dialog should be visible before login starts."
        try:
            self.login_page.start_mobile_login_and_pause_for_otp(
                mobile_number=mobile_number,
                otp_pause_seconds=int(login_data.get("otp_pause_seconds", 60)),
                before_mobile_entry_pause_seconds=int(login_data.get("before_mobile_entry_pause_seconds", 0)),
                after_mobile_entry_pause_seconds=int(login_data.get("after_mobile_entry_pause_seconds", 0)),
            )
        except LoginSessionExpiredError:
            self.home_page.open(base_url)
            self.home_page.open_login()
            assert self.login_page.is_login_dialog_displayed(), "Login dialog should reopen after session retry."
            self.login_page.start_mobile_login_and_pause_for_otp(
                mobile_number=mobile_number,
                otp_pause_seconds=int(login_data.get("otp_pause_seconds", 60)),
                before_mobile_entry_pause_seconds=0,
                after_mobile_entry_pause_seconds=0,
            )
        return mobile_number
