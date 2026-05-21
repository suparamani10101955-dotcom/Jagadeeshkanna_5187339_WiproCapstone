from pathlib import Path

import allure
from allure_commons.types import AttachmentType

from utils.driver_factory import DriverFactory
from utils.logger import get_logger
from utils.screenshot import capture_screenshot


def before_all(context):
    context.base_url = "https://www.99acres.com/"
    context.driver_factory = DriverFactory()
    context.reports_dir = Path("reports")
    (context.reports_dir / "allure-results").mkdir(parents=True, exist_ok=True)
    (context.reports_dir / "allure-report").mkdir(parents=True, exist_ok=True)
    (context.reports_dir / "screenshots").mkdir(parents=True, exist_ok=True)
    (context.reports_dir / "logs").mkdir(parents=True, exist_ok=True)
    context.logger = get_logger("behave.environment")


def before_scenario(context, scenario):
    context.logger.info("Starting scenario: %s", scenario.name)
    context.driver = context.driver_factory.create_driver()
    context.scenario_logger = get_logger(scenario.name)


def after_step(context, step):
    if step.status != "failed":
        return

    logger = getattr(context, "scenario_logger", context.logger)
    logger.error("Step failed: %s", step.name)
    driver = getattr(context, "driver", None)
    if driver is None:
        return

    screenshot_path = capture_screenshot(driver, context.scenario.name, step.name)
    if screenshot_path:
        logger.error("Failure screenshot captured: %s", screenshot_path)
        allure.attach.file(
            str(screenshot_path),
            name=f"{context.scenario.name} - {step.name}",
            attachment_type=AttachmentType.PNG,
        )


def after_scenario(context, scenario):
    logger = getattr(context, "scenario_logger", context.logger)
    driver = getattr(context, "driver", None)
    if scenario.status == "failed" and driver is not None:
        screenshot_path = capture_screenshot(driver, scenario.name, "scenario_failure")
        if screenshot_path:
            logger.error("Scenario failed: %s", scenario.name)
            logger.error("Scenario failure screenshot captured: %s", screenshot_path)
            allure.attach.file(
                str(screenshot_path),
                name=f"{scenario.name} - scenario failure",
                attachment_type=AttachmentType.PNG,
            )

    driver = getattr(context, "driver", None)
    if driver is not None:
        logger.info("Closing browser for scenario: %s", scenario.name)
        driver.quit()
