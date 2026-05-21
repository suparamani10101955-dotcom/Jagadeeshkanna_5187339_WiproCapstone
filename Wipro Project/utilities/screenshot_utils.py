from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings


def _safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", value).strip("_")


def build_screenshot_path(test_name: str) -> Path:
    settings.screenshot_dir.mkdir(parents=True, exist_ok=True)
    return settings.screenshot_dir / f"{_safe_name(test_name)}_{datetime.now():%Y%m%d_%H%M%S}.png"


def attach_screenshot_to_allure(image_bytes: bytes, attachment_name: str) -> None:
    allure.attach(
        image_bytes,
        name=attachment_name,
        attachment_type=allure.attachment_type.PNG,
    )


def capture_screenshot(driver: WebDriver, test_name: str) -> Path:
    file_path = build_screenshot_path(test_name)
    driver.save_screenshot(str(file_path))
    attach_screenshot_to_allure(driver.get_screenshot_as_png(), file_path.name)
    return file_path
