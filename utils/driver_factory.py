from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DriverFactory:
    def create_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        service = Service(self._resolve_chromedriver_path())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            },
        )
        driver.implicitly_wait(0)
        return driver

    def _resolve_chromedriver_path(self):
        driver_path = Path(ChromeDriverManager().install())
        if driver_path.suffix.lower() == ".exe":
            return str(driver_path)

        candidates = sorted(driver_path.parent.rglob("chromedriver.exe"))
        if not candidates:
            raise FileNotFoundError(
                f"ChromeDriver executable was not found near: {driver_path}"
            )
        return str(candidates[0])
