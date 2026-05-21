from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


def _as_bool(value: str | bool | None, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _as_int(value: str | int | None, default: int) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://www.99acres.com/")
    browser: str = os.getenv("BROWSER", "chrome")
    headless: bool = _as_bool(os.getenv("HEADLESS"), False)
    implicit_wait: int = _as_int(os.getenv("IMPLICIT_WAIT"), 2)
    explicit_wait: int = _as_int(os.getenv("EXPLICIT_WAIT"), 20)
    page_load_timeout: int = _as_int(os.getenv("PAGE_LOAD_TIMEOUT"), 45)
    post_click_wait_seconds: int = _as_int(os.getenv("POST_CLICK_WAIT_SECONDS"), 2)
    screenshot_dir: Path = ROOT_DIR / os.getenv("SCREENSHOT_DIR", "screenshots")
    log_dir: Path = ROOT_DIR / os.getenv("LOG_DIR", "logs")
    allure_results_dir: Path = ROOT_DIR / "allure-results"
    username: str = os.getenv("ACRES_USERNAME", "")
    password: str = os.getenv("ACRES_PASSWORD", "")


settings = Settings()
