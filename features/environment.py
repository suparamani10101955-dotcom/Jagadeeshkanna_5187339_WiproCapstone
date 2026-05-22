from pathlib import Path

import allure
from allure_commons.types import AttachmentType

from utils.driver_factory import DriverFactory
from utils.framework_support import capture_screenshot, get_logger


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
    context.scenario_logger.info("Scenario started: %s", scenario.name)


def before_step(context, step):
    logger = getattr(context, "scenario_logger", context.logger)
    logger.info("Starting step: %s", step.name)


def after_step(context, step):
    logger = getattr(context, "scenario_logger", context.logger)
    logger.info("Completed step: %s | status=%s", step.name, step.status)
    driver = getattr(context, "driver", None)
    if driver is None:
        return

    screenshot_path = capture_screenshot(driver, context.scenario.name, step.name)
    if screenshot_path:
        allure.attach.file(
            str(screenshot_path),
            name=f"{context.scenario.name} - {step.name} - screenshot",
            attachment_type=AttachmentType.PNG,
        )

    if step.status == "failed":
        logger.error("Step failed: %s", step.name)

    log_file_path = Path("reports") / "logs" / "execution.log"
    if log_file_path.exists():
        allure.attach(
            log_file_path.read_text(encoding="utf-8", errors="replace"),
            name=f"{context.scenario.name} - {step.name} - execution log",
            attachment_type=AttachmentType.TEXT,
        )


def after_scenario(context, scenario):
    logger = getattr(context, "scenario_logger", context.logger)
    log_file_path = Path("reports") / "logs" / "execution.log"
    driver = getattr(context, "driver", None)

    if driver is not None:
        screenshot_path = capture_screenshot(driver, scenario.name, f"scenario_{scenario.status}")
        if screenshot_path:
            allure.attach.file(
                str(screenshot_path),
                name=f"{scenario.name} - scenario {scenario.status} screenshot",
                attachment_type=AttachmentType.PNG,
            )

    if scenario.status == "failed" and driver is not None:
        screenshot_path = capture_screenshot(driver, scenario.name, "scenario_failure")
        if screenshot_path:
            logger.error("Scenario failed: %s", scenario.name)
            allure.attach.file(
                str(screenshot_path),
                name=f"{scenario.name} - scenario failure",
                attachment_type=AttachmentType.PNG,
            )

    if log_file_path.exists():
        allure.attach(
            log_file_path.read_text(encoding="utf-8", errors="replace"),
            name=f"{scenario.name} - scenario execution log",
            attachment_type=AttachmentType.TEXT,
        )

    if driver is not None:
        logger.info("Closing browser for scenario: %s", scenario.name)
        driver.quit()
