from datetime import datetime
from pathlib import Path


SCREENSHOT_DIR = Path("reports") / "screenshots"


def capture_screenshot(driver, scenario_name, suffix="failure"):
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_scenario_name = _sanitize_name(scenario_name)
    safe_suffix = _sanitize_name(suffix)
    screenshot_path = SCREENSHOT_DIR / f"{safe_scenario_name}_{safe_suffix}_{timestamp}.png"

    if driver.save_screenshot(str(screenshot_path)):
        return screenshot_path
    return None


def _sanitize_name(value):
    sanitized = "".join(char if char.isalnum() else "_" for char in value.strip())
    return sanitized or "unnamed"
