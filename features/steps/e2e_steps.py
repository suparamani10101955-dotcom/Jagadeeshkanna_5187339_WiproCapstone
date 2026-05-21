from behave import when


@when("the user completes the full 99acres journey")
def step_complete_full_journey(context):
    context.login_page.navigate_to_property_search()
    context.login_page.apply_property_filters()
    context.login_page.open_filtered_property_card()
    context.login_page.validate_property_details_page()
