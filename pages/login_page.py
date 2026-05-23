import os
import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils.framework_support import get_logger
from utils.wait_utils import WaitUtils


class LoginPage:
    COOKIE_OK_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Okay' or normalize-space()='OK' or normalize-space()='Got it']",
    )
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
    CONTINUE_BUTTON = (By.XPATH, "//button[normalize-space()='Continue']")
    LANDMARK_SEARCH_BAR = (By.XPATH, '//*[@id="d_landmark_inPageSearchBox"]')
    LANDMARK_SEARCH_INPUT = (By.XPATH, '//*[@id="d_landmark_inPageSearchBox"]//input')
    SEARCH_SUGGESTION_ITEM = (
        By.XPATH,
        "//*[@id='suggestions_custom']/li[@title='MUMBAI' or @title='Mumbai']",
    )
    SEARCH_ICON_BY_ID = (By.XPATH, '//*[@id="searchform_search_btn"]')
    RESULTS_CONTAINER = (
        By.XPATH,
        "//div[contains(@class,'srp') or contains(@class,'tuple') or @id='srp_container']",
    )
    LOADER = (
        By.XPATH,
        "//*[contains(@class,'loader') or contains(@class,'Loading') or contains(@class,'loading')]",
    )
    FILTER_ONE = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[2]/div/div[1]",
    )
    FILTER_ONE_OPTION = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div[2]/div/ul/li[8]",
    )
    FILTER_TWO = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[3]/div/div[2]/div/div[3]",
    )
    FILTER_TWO_OPTION = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div[2]/div/ul/li[8]",
    )
    FILTER_THREE = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[4]/div/div/div[2]/div[1]",
    )
    FILTER_FOUR = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[5]/div/div/div[2]/div[2]",
    )
    FILTER_FIVE = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[6]/div/div/div[2]/div[1]",
    )
    FILTER_SIX = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[7]/div/div/div[2]/div[1]",
    )
    FILTER_SEVEN = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[9]/div/div/div[2]/div[1]",
    )
    PROPERTY_CARD = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[3]/div[5]/section[3]/div/div/div[1]/div[2]/div[1]/div/div[1]/div[1]/div",
    )
    PROPERTY_LINKS = [
        (By.XPATH, "(//a[contains(@href,'property') or contains(@href,'project')])[1]"),
        (By.XPATH, "(//*[contains(@class,'srpTuple')]//a)[1]"),
        (By.XPATH, "(//a[contains(@href,'/buy/') or contains(@href,'/project-') or contains(@href,'/property-in-')])[1]"),
        (By.XPATH, "(//section//a[@href])[1]"),
    ]

    def __init__(self, driver, timeout=25):
        self.driver = driver
        self.wait = WaitUtils(driver, timeout)
        self.logger = get_logger(__name__)
        self.previous_url = None
        self.manual_otp_wait_seconds = int(os.getenv("MANUAL_OTP_WAIT_SECONDS", "20"))
        self.post_otp_wait_seconds = int(os.getenv("POST_OTP_WAIT_SECONDS", "10"))

    def open(self, url):
        self.logger.info("Opening 99acres website: %s", url)
        self.driver.get(url)
        self.driver.maximize_window()
        self.wait.wait_for_presence((By.TAG_NAME, "header"))
        self.wait.wait_for_page_stable()
        self._dismiss_cookie_banner_if_present()

    def click_login_icon(self):
        element = self.wait.wait_for_presence(self.LOGIN_ICON)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        ActionChains(self.driver).move_to_element(element).perform()

    def click_login_register(self):
        self.click_element(self.LOGIN_REGISTER, "Login/Register option")

    def enter_mobile_number(self, mobile_number):
        self.enter_text(self.MOBILE_NUMBER_INPUT, mobile_number, "mobile number")

    def click_continue(self):
        self.click_element(self.CONTINUE_BUTTON, "Continue button")

    def wait_for_manual_otp(self):
        self.logger.info("Waiting %s seconds for manual OTP entry and manual Continue click.", self.manual_otp_wait_seconds)
        time.sleep(self.manual_otp_wait_seconds)
        self.logger.info("Waiting %s seconds after manual OTP completion before continuing.", self.post_otp_wait_seconds)
        time.sleep(self.post_otp_wait_seconds)

    def complete_otp_login(self):
        self.wait.wait_for_page_stable()
        self._dismiss_cookie_banner_if_present()

    def search_for_city(self, city_name="MUMBAI"):
        self.logger.info("Starting property search for city: %s", city_name)
        self._dismiss_cookie_banner_if_present()
        self.wait.wait_for_presence(self.LANDMARK_SEARCH_BAR)
        search_box = self.wait.wait_for_visibility(self.LANDMARK_SEARCH_INPUT)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_box)
        self.driver.execute_script("arguments[0].focus();", search_box)
        try:
            search_box.clear()
        except WebDriverException:
            self.driver.execute_script("arguments[0].value='';", search_box)
        search_box.send_keys(city_name)
        try:
            self.click_element(self.SEARCH_SUGGESTION_ITEM, "search suggestion", 10)
        except AssertionError:
            self.logger.info("Search suggestion was not clickable. Continuing with direct search submission.")
        self.click_element(self.SEARCH_ICON_BY_ID, "search icon", 15)
        self.wait.wait_for_presence(self.RESULTS_CONTAINER)
        self._wait_for_loader_to_clear()

    def apply_requested_filters(self):
        self._click_filter_with_retry(self.FILTER_ONE, "filter 1")
        self._click_filter_with_retry(self.FILTER_ONE_OPTION, "filter 1 option")
        self._click_filter_with_retry(self.FILTER_TWO, "filter 2")
        self._click_filter_with_retry(self.FILTER_TWO_OPTION, "filter 2 option")
        self._click_filter_with_retry(self.FILTER_THREE, "filter 3")
        self._click_filter_with_retry(self.FILTER_FOUR, "filter 4")
        self._click_filter_with_retry(self.FILTER_FIVE, "filter 5")
        self._click_filter_with_retry(self.FILTER_SIX, "filter 6")
        self._click_filter_with_retry(self.FILTER_SEVEN, "filter 7")

    def open_filtered_property_card(self):
        self.previous_url = self.driver.current_url
        original_handles = list(self.driver.window_handles)
        try:
            self.click_element(self.PROPERTY_CARD, "property card", 20)
            self._wait_for_property_navigation(original_handles)
            return
        except AssertionError:
            self.logger.info("Primary property card locator failed. Trying fallback property links.")

        href = self._extract_first_property_href()
        if href:
            self.driver.get(href)
            self.wait.wait_for_page_stable()
            return

        for locator in self.PROPERTY_LINKS:
            try:
                self.click_element(locator, "property link", 15)
                self._wait_for_property_navigation(original_handles)
                return
            except AssertionError:
                continue
        raise AssertionError("Property details page did not open from any available property card or link.")

    def validate_property_details_page(self):
        self.wait.wait_for_page_stable()
        current_url = self.driver.current_url
        title = self.driver.title.strip()
        if not current_url:
            raise AssertionError("Property details page URL is empty.")
        if not title:
            raise AssertionError("Property details page title is empty.")

    def click_element(self, locator, element_name, timeout=25):
        try:
            self._dismiss_cookie_banner_if_present()
            element = self.wait.wait_for_clickable(locator, timeout)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            try:
                element.click()
            except WebDriverException:
                self.driver.execute_script("arguments[0].click();", element)
            self.wait.wait_for_page_stable()
            self._wait_for_loader_to_clear()
        except (TimeoutException, NoSuchElementException) as exc:
            raise AssertionError(f"{element_name} was not clickable in time.") from exc

    def enter_text(self, locator, value, element_name):
        try:
            element = self.wait.wait_for_visibility(locator)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            self.driver.execute_script("arguments[0].focus();", element)
            try:
                element.clear()
            except WebDriverException:
                pass
            element.send_keys(Keys.CONTROL, "a")
            element.send_keys(Keys.DELETE)
            element.send_keys(value)
            self.wait.wait_for_page_stable()
        except (TimeoutException, NoSuchElementException) as exc:
            raise AssertionError(f"{element_name} was not visible in time.") from exc

    def _click_filter_with_retry(self, locator, element_name, attempts=3):
        last_error = None
        for _ in range(attempts):
            try:
                self.click_element(locator, element_name, 20)
                time.sleep(1)
                return
            except AssertionError as exc:
                last_error = exc
                time.sleep(1)
        raise AssertionError(f"{element_name} could not be selected after {attempts} attempts.") from last_error

    def _wait_for_loader_to_clear(self):
        try:
            self.wait.wait_for_invisibility(self.LOADER, 10)
        except TimeoutException:
            pass

    def _dismiss_cookie_banner_if_present(self):
        try:
            cookie_button = self.wait.wait_for_clickable(self.COOKIE_OK_BUTTON, 3)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cookie_button)
            try:
                cookie_button.click()
            except WebDriverException:
                self.driver.execute_script("arguments[0].click();", cookie_button)
            self.wait.wait_for_page_stable(5)
            self.logger.info("Cookie banner dismissed.")
        except TimeoutException:
            return

    def _wait_for_property_navigation(self, original_handles):
        end_time = time.time() + 10
        while time.time() < end_time:
            updated_handles = self.driver.window_handles
            if len(updated_handles) > len(original_handles):
                self.driver.switch_to.window(updated_handles[-1])
                self.wait.wait_for_page_stable()
                return
            if self.driver.current_url != self.previous_url:
                return
            time.sleep(0.5)
        raise AssertionError("Property details navigation did not complete in time.")

    def _extract_first_property_href(self):
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
        return hrefs[0] if hrefs else None
