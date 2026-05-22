import allure
from behave import given, then, when

from pages.home_page import HomePage
from utils.framework_support import capture_screenshot


def _attach_failure_screenshot(context, label):
    screenshot_path = capture_screenshot(context.driver, context.scenario.name, label)
    if screenshot_path:
        allure.attach.file(
            str(screenshot_path),
            name=f"{context.scenario.name} - {label}",
            attachment_type=allure.attachment_type.PNG,
        )


@given("the user launches the 99acres homepage for negative search")
def step_launch_negative_homepage(context):
    with allure.step("Launch 99acres homepage for negative search"):
        try:
            context.scenario_logger.info("Launching homepage for negative search validation.")
            context.home_page = HomePage(context.driver)
            context.home_page.open(context.base_url)
        except Exception:
            _attach_failure_screenshot(context, "launch_homepage_failure")
            raise


@when("the user keeps the search box empty")
def step_keep_search_empty(context):
    with allure.step("Keep search box empty"):
        try:
            context.scenario_logger.info("Keeping search box empty.")
            context.home_page.enter_search_text("")
        except Exception:
            _attach_failure_screenshot(context, "empty_search_failure")
            raise


@when("the user enters only spaces in the search field")
def step_enter_only_spaces(context):
    with allure.step("Enter only spaces in the search field"):
        try:
            context.scenario_logger.info("Entering only spaces in search field.")
            context.home_page.enter_search_text("   ")
        except Exception:
            _attach_failure_screenshot(context, "spaces_search_failure")
            raise


@when("the user clicks the negative search button")
def step_click_negative_search_button(context):
    with allure.step("Click negative search button"):
        try:
            context.scenario_logger.info("Clicking negative search button.")
            context.pre_search_url = context.driver.current_url
            context.home_page.click_search_button()
        except Exception:
            _attach_failure_screenshot(context, "click_search_failure")
            raise


@then("a validation message should appear or the search should not be performed")
@then("a validation message should appear or the search should be blocked")
def step_validate_negative_search(context):
    with allure.step("Validate negative search behavior"):
        try:
            context.scenario_logger.info("Validating negative search behavior.")
            validation_message = context.home_page.get_validation_message()
            search_blocked = context.home_page.is_search_blocked(context.pre_search_url)
            assert validation_message or search_blocked, (
                "Expected a validation message or blocked search for invalid input."
            )
            context.scenario_logger.info(
                "Negative search validation passed. validation_message=%s, search_blocked=%s",
                validation_message or "<none>",
                search_blocked,
            )
        except Exception:
            _attach_failure_screenshot(context, "negative_search_assertion_failure")
            raise
