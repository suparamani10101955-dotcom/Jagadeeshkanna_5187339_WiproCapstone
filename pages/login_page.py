import logging
import time

from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from utils.wait_utils import WaitUtils


class LoginPage:
    logger = logging.getLogger(__name__)

    LOGIN_ICON = (
        By.XPATH,
        "//i[contains(@class,'icon_userWhite') and contains(@class,'theader__dot')]",
    )
    LOGIN_REGISTER = (
        By.XPATH,
        "//*[contains(text(),'LOGIN / REGISTER') or "
        "contains(text(),'Login / Register') or "
        "contains(text(),'LOGIN/REGISTER') or "
        "contains(text(),'Login/Register')]",
    )
    MOBILE_NUMBER_INPUT = (
        By.XPATH,
        "//input[@data-for='phnNumber'] | //input[@placeholder='Phone Number']",
    )
    CONTINUE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Continue']",
    )
    POST_LOGIN_NAVIGATION_LINK = (
        By.XPATH,
        '//*[@id="app"]/div/div/div[4]/div[3]/div[3]/div[3]/a[8]',
    )
    FIRST_FILTER_TILE = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[5]/div/div/div[2]/div[2]",
    )
    OWNER_CHECKBOX = (By.XPATH, '//*[@id="__Owner__"]')
    FIRST_DROPDOWN = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[8]/div/div[2]/div/div[1]",
    )
    FIRST_DROPDOWN_OPTION = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[8]/div/div[2]/div/div[1]/div[2]/div/div[2]/div/ul/li[11]",
    )
    SECOND_DROPDOWN = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[8]/div/div[2]/div/div[3]",
    )
    SECOND_DROPDOWN_OPTION = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[8]/div/div[2]/div/div[3]/div[2]/div/div[2]/div/ul/li[16]",
    )
    FINAL_CHECKBOX = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[9]/div/div/div[2]/div[1]",
    )
    PROPERTY_CARD = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[3]/div[5]/section[2]/div/div/div[1]/div[2]/div[1]/div/div[1]/div[1]/d",
    )

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WaitUtils(driver, timeout)

    def open(self, url):
        try:
            self.logger.info("Opening 99acres website.")
            self.driver.get(url)
            self.driver.maximize_window()
            self.wait.wait_for_presence((By.TAG_NAME, "header"))
            time.sleep(2)
        except WebDriverException as exc:
            raise AssertionError(f"Unable to open website: {url}") from exc

    def click_login_icon(self):
        try:
            self.logger.info("Hovering over login icon.")
            element = self.wait.wait_for_presence(self.LOGIN_ICON)
            self._scroll_into_view(element)
            ActionChains(self.driver).move_to_element(element).perform()
            time.sleep(2)
        except (TimeoutException, NoSuchElementException) as exc:
            raise AssertionError("Login icon was not available for hover.") from exc
        except WebDriverException as exc:
            raise AssertionError("Failed to hover over the login icon.") from exc

    def click_login_register(self):
        self._safe_click(self.LOGIN_REGISTER, "Login/Register option")
        time.sleep(2)

    def enter_mobile_number(self, mobile_number):
        try:
            self.logger.info("Entering mobile number.")
            element = self.wait.wait_for_visibility(self.MOBILE_NUMBER_INPUT)
            self._scroll_into_view(element)
            self.driver.execute_script("arguments[0].focus();", element)
            self.driver.execute_script("arguments[0].value='';", element)
            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('input', {bubbles:true}));",
                element,
            )
            element.send_keys(mobile_number)
        except (TimeoutException, NoSuchElementException) as exc:
            raise AssertionError("Mobile number input box was not visible in time.") from exc
        except WebDriverException as exc:
            raise AssertionError("Failed to enter the mobile number.") from exc

    def click_continue(self):
        self._safe_click(self.CONTINUE_BUTTON, "Continue button")

    def wait_for_manual_otp(self):
        self.logger.info("Waiting for manual OTP entry.")
        try:
            input("Enter OTP manually and press Enter to continue...")
        except EOFError:
            time.sleep(30)
        time.sleep(3)

    def navigate_to_property_search(self):
        self.logger.info("Navigating to property search results.")
        self._safe_click(self.POST_LOGIN_NAVIGATION_LINK, "post-login navigation link")
        time.sleep(2)
        self._safe_click(self.FIRST_FILTER_TILE, "first filter tile")
        time.sleep(2)

    def apply_property_filters(self):
        self.logger.info("Applying property filters.")
        self._safe_checkbox_click(self.OWNER_CHECKBOX, "Owner checkbox")
        self._safe_click(self.FIRST_DROPDOWN, "first dropdown")
        self._safe_click(self.FIRST_DROPDOWN_OPTION, "first dropdown option")
        time.sleep(1)
        self._safe_click(self.SECOND_DROPDOWN, "second dropdown")
        self._safe_click(self.SECOND_DROPDOWN_OPTION, "second dropdown option")
        time.sleep(1)
        self._safe_checkbox_click(self.FINAL_CHECKBOX, "final checkbox")
        time.sleep(2)

    def open_filtered_property_card(self):
        self.logger.info("Opening filtered property card.")
        self.previous_url = self.driver.current_url
        self._safe_click(self.PROPERTY_CARD, "filtered property card")
        time.sleep(3)

    def validate_property_details_page(self):
        self.logger.info("Validating property details page load.")
        self.wait_for_page_ready()
        current_url = self.driver.current_url
        title = self.driver.title.strip()
        if not current_url:
            raise AssertionError("Property details page URL is empty.")
        if not title:
            raise AssertionError("Property details page title is empty.")
        if getattr(self, "previous_url", None) == current_url and len(self.driver.window_handles) == 1:
            self.logger.warning("Property details page URL did not change after clicking the card.")

    def wait_for_page_ready(self):
        self.wait.wait_for_page_ready()

    def _safe_click(self, locator, element_name):
        try:
            self.logger.info("Clicking %s.", element_name)
            element = self.wait.wait_for_clickable(locator)
            self._fast_click(element)
        except (TimeoutException, NoSuchElementException) as exc:
            raise AssertionError(f"{element_name} was not clickable in time.") from exc
        except WebDriverException as exc:
            raise AssertionError(f"Failed to click the {element_name}.") from exc

    def _safe_checkbox_click(self, locator, element_name):
        try:
            self.logger.info("Selecting %s.", element_name)
            element = self.wait.wait_for_presence(locator)
            self._scroll_into_view(element)
            if not element.is_selected():
                try:
                    self.wait.wait_for_clickable(locator).click()
                except WebDriverException:
                    self.logger.info(
                        "Standard checkbox click failed for %s. Falling back to JavaScript click.",
                        element_name,
                    )
                    self._js_click(element)
        except (TimeoutException, NoSuchElementException) as exc:
            raise AssertionError(f"{element_name} was not available in time.") from exc
        except WebDriverException as exc:
            raise AssertionError(f"Failed to select the {element_name}.") from exc

    def _scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )

    def _fast_click(self, element):
        self._scroll_into_view(element)
        try:
            element.click()
        except WebDriverException:
            self.logger.info("Standard click failed. Falling back to JavaScript click.")
            self._js_click(element)

    def _js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)
