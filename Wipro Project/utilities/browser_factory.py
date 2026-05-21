from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings


class BrowserFactory:
    @staticmethod
    def create_driver(browser: str | None = None, headless: bool | None = None) -> WebDriver:
        browser_name = (browser or settings.browser).strip().lower()
        if browser_name == "chrome":
            return BrowserFactory._create_chrome_driver(headless=headless)
        if browser_name == "edge":
            return BrowserFactory._create_edge_driver(headless=headless)

        raise ValueError(f"Unsupported browser '{browser_name}'. This framework currently supports Chrome and Edge.")

    @staticmethod
    def _create_chrome_driver(headless: bool | None = None) -> webdriver.Chrome:
        options = ChromeOptions()
        if settings.headless if headless is None else headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(options=options)
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
        )
        driver.implicitly_wait(settings.implicit_wait)
        driver.set_page_load_timeout(settings.page_load_timeout)
        return driver

    @staticmethod
    def _create_edge_driver(headless: bool | None = None) -> webdriver.Edge:
        options = EdgeOptions()
        if settings.headless if headless is None else headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Edge(options=options)
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
        )
        driver.implicitly_wait(settings.implicit_wait)
        driver.set_page_load_timeout(settings.page_load_timeout)
        return driver
