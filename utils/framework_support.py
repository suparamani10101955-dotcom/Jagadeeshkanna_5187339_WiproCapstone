import logging
from datetime import datetime
from pathlib import Path


LOG_DIR = Path("reports") / "logs"
SCREENSHOT_DIR = Path("reports") / "screenshots"


def get_logger(name="framework"):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(filename)s | %(message)s")
    file_handler = logging.FileHandler(LOG_DIR / "execution.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False
    return logger


def capture_screenshot(driver, scenario_name, suffix="failure"):
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = _sanitize_name(scenario_name)
    safe_suffix = _sanitize_name(suffix)
    screenshot_path = SCREENSHOT_DIR / f"{safe_name}_{safe_suffix}_{timestamp}.png"
    if driver.save_screenshot(str(screenshot_path)):
        return screenshot_path
    return None


def _sanitize_name(value):
    sanitized = "".join(char if char.isalnum() else "_" for char in value.strip())
    return sanitized or "unnamed"
