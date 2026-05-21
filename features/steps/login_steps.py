from behave import given, then, when

from pages.login_page import LoginPage


@given("the user launches the 99acres website")
def step_launch_website(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.open(context.base_url)


@when("the user opens the login panel")
def step_open_login_panel(context):
    context.login_page.click_login_icon()


@when("the user selects the Login/Register option")
def step_select_login_register(context):
    context.login_page.click_login_register()


@when('the user enters mobile number "{mobile_number}"')
def step_enter_mobile_number(context, mobile_number):
    context.login_page.enter_mobile_number(mobile_number)


@when("the user clicks the Continue button")
def step_click_continue(context):
    context.login_page.click_continue()


@when("the system waits for manual OTP entry")
@then("the system waits for manual OTP entry")
def step_wait_for_otp(context):
    context.login_page.wait_for_manual_otp()
