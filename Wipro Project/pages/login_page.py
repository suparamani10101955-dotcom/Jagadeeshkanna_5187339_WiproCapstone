from __future__ import annotations

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings
from locators.login_locators import LoginLocators
from pages.base_page import BasePage, Locator


class LoginSessionExpiredError(RuntimeError):
    pass


class LoginPage(BasePage):
    def is_login_dialog_displayed(self) -> bool:
        return self.is_visible(LoginLocators.LOGIN_DIALOG, timeout=10)

    def is_session_expired_message_displayed(self) -> bool:
        return self.is_visible(LoginLocators.SESSION_EXPIRED_MESSAGE, timeout=3)

    def submit_username(self, username: str) -> None:
        if not username:
            raise ValueError("Username is required for login.")
        self._type_into_first_available(LoginLocators.USERNAME_FIELDS, username)
        self.click_first_available(LoginLocators.CONTINUE_BUTTONS)

    def start_mobile_login_and_pause_for_otp(
        self,
        mobile_number: str,
        otp_pause_seconds: int = 30,
        before_mobile_entry_pause_seconds: int = 0,
        after_mobile_entry_pause_seconds: int = 0,
    ) -> None:
        if not mobile_number:
            raise ValueError("Mobile number is required for login.")

        self.enter_mobile_number(mobile_number)
        if before_mobile_entry_pause_seconds or after_mobile_entry_pause_seconds:
            self.logger.info("Ignoring manual pause settings in favor of explicit waits.")
        if self.is_session_expired_message_displayed():
            raise LoginSessionExpiredError("99acres login session expired before Continue was clicked.")
        self.click_first_available(LoginLocators.CONTINUE_BUTTONS, timeout=10)
        if self.is_session_expired_message_displayed():
            raise LoginSessionExpiredError("99acres login session expired after Continue was clicked.")
        self.logger.info(
            "Mobile number submitted. Pausing for %s seconds to allow manual OTP entry. "
            "No further actions will run during this wait.",
            otp_pause_seconds,
        )
        time.sleep(otp_pause_seconds)

        self.logger.info("Manual OTP wait completed. Verifying whether login has completed successfully.")
        if not self.wait_utils.any_visible(LoginLocators.OTP_SUCCESS_INDICATORS, timeout=30):
            raise AssertionError("Login was not completed successfully after the manual OTP wait.")

        self.logger.info("Login success confirmed. Waiting 40 seconds for the post-login page to stabilize.")
        time.sleep(40)
        self.wait_for_page_load(timeout=40)
        self.logger.info("Post-login stabilization wait completed. E2E flow can continue.")

    def submit_password_if_present(self, password: str) -> None:
        for locator in LoginLocators.PASSWORD_FIELDS:
            if self.is_visible(locator, timeout=5):
                self.type_text(locator, password)
                self.click_first_available(LoginLocators.CONTINUE_BUTTONS)
                return
        self.logger.info("Password field was not shown. Site may require OTP-based login.")

    def enter_mobile_number(self, mobile_number: str) -> None:
        locator = self._first_visible_locator(LoginLocators.MOBILE_NUMBER_INPUTS, timeout=10)
        self.logger.info("Entering mobile number using locator: %s", locator)
        element = self.find_first_visible(locator, timeout=10)
        WebDriverWait(self.driver, settings.explicit_wait).until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        self.driver.execute_script("arguments[0].focus();", element)
        self.driver.execute_script("arguments[0].value='';", element)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", element)
        element.send_keys(mobile_number)

    def _first_visible_locator(self, locators: tuple[Locator, ...], timeout: int = 5) -> Locator:
        for locator in locators:
            if self.is_visible(locator, timeout=timeout):
                return locator
        raise AssertionError(f"No visible element was available for locators: {locators}")

    def _type_into_first_available(self, locators: tuple[Locator, ...], text: str) -> None:
        for locator in locators:
            if self.is_visible(locator, timeout=5):
                self.type_text(locator, text)
                return
        raise AssertionError(f"No input field was available for locators: {locators}")
