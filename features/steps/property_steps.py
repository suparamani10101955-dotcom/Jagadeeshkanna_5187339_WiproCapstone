from behave import then, when


@when("the user opens the property details page")
def step_open_property_details_page(context):
    context.login_page.open_filtered_property_card()


@then("the property details page should load successfully")
def step_validate_property_details_page(context):
    context.login_page.validate_property_details_page()
