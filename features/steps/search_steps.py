from behave import then, when


@when("the user searches for properties")
@then("the user searches for properties")
def step_search_for_properties(context):
    context.login_page.search_for_city("MUMBAI")
