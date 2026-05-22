from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WaitUtils:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.timeout = timeout

    def wait_for_visibility(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_presence(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_invisibility(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def wait_for_page_stable(self, timeout=None):
        wait_timeout = timeout or self.timeout
        WebDriverWait(self.driver, wait_timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        try:
            WebDriverWait(self.driver, wait_timeout).until(
                lambda driver: driver.execute_script("return window.jQuery ? jQuery.active === 0 : true")
            )
        except Exception:
            pass
        return True
