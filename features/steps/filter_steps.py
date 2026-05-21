from behave import then, when


@when("the user applies property filters")
@then("the user applies property filters")
def step_apply_property_filters(context):
    context.login_page.apply_property_filters()
