import allure
from behave import given, then, when

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.framework_support import capture_screenshot


def _attach_failure_screenshot(context, label):
    screenshot_path = capture_screenshot(context.driver, context.scenario.name, label)
    if screenshot_path:
        allure.attach.file(
            str(screenshot_path),
            name=f"{context.scenario.name} - {label}",
            attachment_type=allure.attachment_type.PNG,
        )


@given("the user launches the 99acres homepage for positive search")
def step_launch_positive_homepage(context):
    with allure.step("Launch 99acres homepage for positive search"):
        try:
            context.scenario_logger.info("Launching homepage for positive property search validation.")
            context.home_page = HomePage(context.driver)
            context.search_results_page = SearchResultsPage(context.driver)
            context.home_page.open(context.base_url)
        except Exception:
            _attach_failure_screenshot(context, "positive_launch_homepage_failure")
            raise


@when("the user clicks the property search field")
def step_click_property_search_field(context):
    with allure.step("Click property search field"):
        try:
            context.scenario_logger.info("Clicking property search field.")
            context.home_page.click_search_field()
        except Exception:
            _attach_failure_screenshot(context, "positive_click_search_field_failure")
            raise


@when('the user enters "{location_name}" in the property search field')
def step_enter_location_in_search_field(context, location_name):
    with allure.step(f"Enter {location_name} in property search field"):
        try:
            context.scenario_logger.info("Entering %s in the property search field.", location_name)
            context.home_page.enter_search_text(location_name)
        except Exception:
            _attach_failure_screenshot(context, "positive_enter_search_text_failure")
            raise


@when('the user selects the "{location_name}" search suggestion')
def step_select_search_suggestion(context, location_name):
    with allure.step(f"Select {location_name} search suggestion"):
        try:
            context.scenario_logger.info("Selecting %s from search suggestions.", location_name)
            context.home_page.select_search_suggestion(location_name)
        except Exception:
            _attach_failure_screenshot(context, "positive_select_suggestion_failure")
            raise


@when("the user clicks the property search button")
def step_click_property_search_button(context):
    with allure.step("Click property search button"):
        try:
            context.scenario_logger.info("Clicking property search button.")
            context.home_page.click_search_button()
        except Exception:
            _attach_failure_screenshot(context, "positive_click_search_button_failure")
            raise


@then("the Mumbai property search results should load successfully")
def step_validate_search_results(context):
    with allure.step("Validate Mumbai property search results"):
        try:
            context.scenario_logger.info("Validating that Mumbai search results are loaded.")
            assert context.search_results_page.wait_for_results_to_load(), "Search results did not load."
            assert context.search_results_page.verify_results_loaded(), "Search results did not load."
            assert context.search_results_page.verify_location_present("Mumbai"), (
                "Mumbai location did not appear in search results."
            )
        except Exception:
            _attach_failure_screenshot(context, "positive_results_validation_failure")
            raise


@when("the user applies the primary property filter")
def step_apply_primary_property_filter(context):
    with allure.step("Apply primary property filter"):
        try:
            context.scenario_logger.info("Applying primary property filter.")
            context.search_results_page.apply_primary_filter()
        except Exception:
            _attach_failure_screenshot(context, "positive_apply_filter_failure")
            raise


@then("the property filter should be applied successfully")
def step_verify_property_filter(context):
    with allure.step("Verify primary property filter"):
        try:
            context.scenario_logger.info("Verifying that the property filter was applied.")
            assert context.search_results_page.verify_filter_applied(), "Filter was not applied successfully."
        except Exception:
            _attach_failure_screenshot(context, "positive_verify_filter_failure")
            raise
