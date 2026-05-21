from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WaitUtils:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.timeout = timeout

    def wait_for_visibility(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_presence(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_page_ready(self):
        return WebDriverWait(self.driver, self.timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
