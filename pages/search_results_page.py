from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By

from utils.framework_support import get_logger
from utils.wait_utils import WaitUtils


class SearchResultsPage:
    RESULTS_CONTAINER = (
        By.XPATH,
        "//*[contains(@class,'srp') or contains(@class,'tuple') or @id='srp_container' or @id='resultHolder' or contains(@class,'pageComponent')]",
    )
    RESULTS_HEADING = (
        By.XPATH,
        "//*[contains(text(),'Property in Mumbai for Sale') or contains(text(),'results')]",
    )
    LOCATION_TEXT = (
        By.XPATH,
        "//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mumbai')]",
    )
    FILTER_DROPDOWN = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[3]/div/div/div[2]/div[1]",
    )
    FILTER_OPTION = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[4]/div/div/div[2]/div[2]",
    )
    APPLIED_FILTER_CHIP = (
        By.XPATH,
        "//*[contains(text(),'Applied Filters')]/following::*[contains(text(),'Flat/Apartment')]",
    )
    SELECTED_FILTER_OPTION = (
        By.XPATH,
        "//*[contains(text(),'Residential Apartment') and (contains(@class,'selected') or contains(@class,'active') or contains(., 'Residential Apartment'))]",
    )
    LOADER = (
        By.XPATH,
        "//*[contains(@class,'loader') or contains(@class,'Loading') or contains(@class,'loading')]",
    )

    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.wait = WaitUtils(driver, timeout)
        self.logger = get_logger(__name__)

    def wait_for_results_to_load(self):
        self.logger.info("Waiting for search results page to load completely.")
        self.wait.wait_for_page_stable()
        try:
            self.wait.wait_for_presence(self.RESULTS_HEADING, 20)
        except TimeoutException:
            self.wait.wait_for_presence(self.RESULTS_CONTAINER, 20)
        self._wait_for_loader_to_clear()
        return True

    def verify_results_loaded(self):
        current_url = self.driver.current_url.lower()
        title = self.driver.title.lower()
        if "mumbai" in current_url and any(marker in current_url for marker in ("property", "search", "buy")):
            return True
        if "mumbai" in title and "property" in title:
            return True
        try:
            heading = self.wait.wait_for_visibility(self.RESULTS_HEADING, 15)
            return heading.is_displayed()
        except TimeoutException:
            try:
                return self.wait.wait_for_visibility(self.RESULTS_CONTAINER, 10).is_displayed()
            except TimeoutException:
                return False

    def verify_location_present(self, location_name):
        self.logger.info("Verifying location '%s' appears in the results.", location_name)
        page_text = self.driver.page_source.lower()
        if location_name.lower() in page_text:
            return True
        try:
            return self.wait.wait_for_visibility(self.LOCATION_TEXT, 10).is_displayed()
        except TimeoutException:
            return False

    def apply_primary_filter(self):
        self.logger.info("Applying primary search result filter.")
        self._click(self.FILTER_DROPDOWN, "first filter/dropdown", 20)
        self._click(self.FILTER_OPTION, "required filter option", 20)
        self.wait.wait_for_page_stable()
        self._wait_for_loader_to_clear()

    def verify_filter_applied(self):
        self.logger.info("Verifying filter was applied.")
        page_text = " ".join(self.driver.page_source.split()).lower()
        if "applied filters" in page_text and (
            "flat/apartment" in page_text or "residential apartment" in page_text
        ):
            return True

        try:
            if self.wait.wait_for_visibility(self.APPLIED_FILTER_CHIP, 10).is_displayed():
                return True
        except TimeoutException:
            return False

        return False

    def _click(self, locator, element_name, timeout):
        try:
            element = self.wait.wait_for_clickable(locator, timeout)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            try:
                element.click()
            except WebDriverException:
                self.driver.execute_script("arguments[0].click();", element)
        except (TimeoutException, NoSuchElementException) as exc:
            raise AssertionError(f"{element_name} was not clickable in time.") from exc

    def _wait_for_loader_to_clear(self):
        try:
            self.wait.wait_for_invisibility(self.LOADER, 10)
        except TimeoutException:
            pass
