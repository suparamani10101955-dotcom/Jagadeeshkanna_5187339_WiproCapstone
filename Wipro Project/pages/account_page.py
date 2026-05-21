from __future__ import annotations

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

from locators.account_locators import AccountLocators
from pages.base_page import BasePage


class AccountPage(BasePage):
    def logout_if_available(self) -> bool:
        for trigger in AccountLocators.ACCOUNT_MENU_TRIGGERS:
            try:
                element = self.find_first_visible(trigger, timeout=5)
                ActionChains(self.driver).move_to_element(element).perform()
                self.driver.execute_script("arguments[0].click();", element)
                break
            except Exception:
                continue

        try:
            self.click_first_available(AccountLocators.LOGOUT_OPTIONS, timeout=5)
            self.wait_for_page_load(timeout=10)
            return True
        except TimeoutException:
            self.logger.info("Logout action is not available for the current session.")
            return False

    def is_logged_out(self) -> bool:
        return self.wait_utils.any_visible(AccountLocators.POST_LOGOUT_INDICATORS, timeout=10)
