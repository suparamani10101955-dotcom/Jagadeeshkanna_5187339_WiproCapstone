from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils.framework_support import get_logger
from utils.wait_utils import WaitUtils


class HomePage:
    COOKIE_OK_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Okay' or normalize-space()='OK' or normalize-space()='Got it']",
    )
    SEARCH_FIELD = (
        By.XPATH,
        "/html/body/div[1]/div/div[1]/div[4]/form/div/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div/div/input",
    )
    SEARCH_BUTTON = (
        By.XPATH,
        "/html/body/div[1]/div/div[1]/div[4]/form/div[1]/div[1]/div[2]/div/div/div[1]/div[4]/button",
    )
    VALIDATION_MESSAGE = (
        By.XPATH,
        "//*[contains(@class,'error') or contains(@class,'validation') or contains(@class,'toast') or "
        "contains(text(),'Enter') or contains(text(),'enter') or contains(text(),'valid') or contains(text(),'search')]",
    )

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WaitUtils(driver, timeout)
        self.logger = get_logger(__name__)

    def open(self, url):
        try:
            self.logger.info("Opening 99acres homepage: %s", url)
            self.driver.get(url)
            self.driver.maximize_window()
            self.wait.wait_for_presence((By.TAG_NAME, "header"))
            self.wait.wait_for_page_stable()
            self._dismiss_cookie_banner_if_present()
        except WebDriverException as exc:
            raise AssertionError(f"Unable to open homepage: {url}") from exc

    def enter_search_text(self, value):
        try:
            self.logger.info("Entering search text: '%s'", value)
            self._dismiss_cookie_banner_if_present()
            element = self.wait.wait_for_visibility(self.SEARCH_FIELD)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            self.driver.execute_script("arguments[0].focus();", element)
            try:
                element.clear()
            except WebDriverException:
                pass
            element.send_keys(Keys.CONTROL, "a")
            element.send_keys(Keys.DELETE)
            if value:
                element.send_keys(value)
            self.wait.wait_for_page_stable()
        except (TimeoutException, NoSuchElementException) as exc:
            raise AssertionError("Search field was not available.") from exc
        except WebDriverException as exc:
            raise AssertionError("Failed to enter text in the search field.") from exc

    def click_search_button(self):
        try:
            self.logger.info("Clicking search button.")
            self._dismiss_cookie_banner_if_present()
            button = self.wait.wait_for_clickable(self.SEARCH_BUTTON, 15)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            try:
                button.click()
            except WebDriverException:
                self.driver.execute_script("arguments[0].click();", button)
            self.wait.wait_for_page_stable()
        except (TimeoutException, NoSuchElementException) as exc:
            raise AssertionError("Search button was not clickable in time.") from exc
        except WebDriverException as exc:
            raise AssertionError("Failed to click search button.") from exc

    def get_validation_message(self):
        try:
            element = self.wait.wait_for_visibility(self.VALIDATION_MESSAGE, 5)
            message = element.text.strip()
            self.logger.info("Validation message detected: %s", message)
            return message
        except TimeoutException:
            self.logger.info("Validation message was not displayed.")
            return ""
        except WebDriverException as exc:
            raise AssertionError("Unable to read validation message.") from exc

    def is_search_blocked(self, previous_url):
        current_url = self.driver.current_url
        blocked = current_url == previous_url
        self.logger.info("Search blocked check. previous_url=%s current_url=%s blocked=%s", previous_url, current_url, blocked)
        return blocked

    def _dismiss_cookie_banner_if_present(self):
        try:
            button = self.wait.wait_for_clickable(self.COOKIE_OK_BUTTON, 3)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            try:
                button.click()
            except WebDriverException:
                self.driver.execute_script("arguments[0].click();", button)
            self.wait.wait_for_page_stable(5)
            self.logger.info("Cookie banner dismissed.")
        except TimeoutException:
            return
