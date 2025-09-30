"""Common step definitions for BDD tests."""

from behave import given, when, then, step
import re


# Navigation steps

@given('I open the application')
@given('I navigate to the application')
def step_open_application(context):
    """Open the application base URL."""
    base_url = context.config_manager.get('framework', 'base_url')
    context.actions.navigate(base_url)


@given('I navigate to "{url}"')
@when('I navigate to "{url}"')
def step_navigate_to_url(context, url):
    """Navigate to specific URL."""
    context.actions.navigate(url)


@when('I reload the page')
def step_reload_page(context):
    """Reload current page."""
    context.actions.reload()


@when('I go back')
def step_go_back(context):
    """Navigate back."""
    context.actions.go_back()


@when('I go forward')
def step_go_forward(context):
    """Navigate forward."""
    context.actions.go_forward()


# Click steps

@when('I click "{selector}"')
@when('I click on "{selector}"')
@when('I click the "{selector}"')
def step_click_element(context, selector):
    """Click element."""
    context.actions.click(selector)


@when('I double click "{selector}"')
@when('I double click on "{selector}"')
def step_double_click_element(context, selector):
    """Double click element."""
    context.actions.double_click(selector)


@when('I right click "{selector}"')
@when('I right click on "{selector}"')
def step_right_click_element(context, selector):
    """Right click element."""
    context.actions.right_click(selector)


@when('I click at coordinates ({x:d}, {y:d})')
def step_click_coordinates(context, x, y):
    """Click at specific coordinates."""
    context.actions.click_by_coordinates(x, y)


# Input steps

@when('I enter "{text}" in "{selector}"')
@when('I enter "{text}" into "{selector}"')
@when('I type "{text}" in "{selector}"')
@when('I type "{text}" into "{selector}"')
def step_enter_text(context, text, selector):
    """Enter text into element."""
    context.actions.type_text(selector, text)


@when('I fill "{selector}" with "{text}"')
def step_fill_element(context, selector, text):
    """Fill element with text."""
    context.actions.fill(selector, text)


@when('I clear "{selector}"')
def step_clear_element(context, selector):
    """Clear input field."""
    context.actions.clear(selector)


@when('I press "{key}" on "{selector}"')
@when('I press {key} key on "{selector}"')
def step_press_key(context, key, selector):
    """Press keyboard key on element."""
    context.actions.press_key(selector, key)


# Checkbox and radio steps

@when('I check "{selector}"')
def step_check_element(context, selector):
    """Check checkbox or radio button."""
    context.actions.check(selector)


@when('I uncheck "{selector}"')
def step_uncheck_element(context, selector):
    """Uncheck checkbox."""
    context.actions.uncheck(selector)


# Select steps

@when('I select "{option}" from "{selector}"')
def step_select_by_label(context, option, selector):
    """Select dropdown option by label."""
    context.actions.select_option(selector, label=option)


@when('I select option with value "{value}" from "{selector}"')
def step_select_by_value(context, value, selector):
    """Select dropdown option by value."""
    context.actions.select_option(selector, value=value)


# Hover steps

@when('I hover over "{selector}"')
@when('I hover on "{selector}"')
def step_hover_element(context, selector):
    """Hover over element."""
    context.actions.hover(selector)


# Drag and drop steps

@when('I drag "{source}" to "{target}"')
def step_drag_and_drop(context, source, target):
    """Drag and drop element."""
    context.actions.drag_and_drop(source, target)


# Upload steps

@when('I upload "{file_path}" to "{selector}"')
@when('I upload file "{file_path}" to "{selector}"')
def step_upload_file(context, file_path, selector):
    """Upload file."""
    context.actions.upload_file(selector, file_path)


# Wait steps

@when('I wait for "{selector}" to be visible')
@then('I wait for "{selector}" to be visible')
def step_wait_for_visible(context, selector):
    """Wait for element to be visible."""
    context.actions.wait_for_selector(selector, state='visible')


@when('I wait for "{selector}" to be hidden')
@then('I wait for "{selector}" to be hidden')
def step_wait_for_hidden(context, selector):
    """Wait for element to be hidden."""
    context.actions.wait_for_selector(selector, state='hidden')


@when('I wait for {seconds:d} seconds')
@then('I wait for {seconds:d} seconds')
def step_wait_seconds(context, seconds):
    """Wait for specified seconds."""
    context.actions.wait_for_timeout(seconds * 1000)


@when('I wait for page to load')
def step_wait_for_load(context):
    """Wait for page to load."""
    context.actions.wait_for_load_state('networkidle')


# Assertion steps

@then('I should see "{selector}"')
@then('"{selector}" should be visible')
def step_should_see_element(context, selector):
    """Assert element is visible."""
    context.actions.assert_visible(selector)


@then('I should not see "{selector}"')
@then('"{selector}" should be hidden')
@then('"{selector}" should not be visible')
def step_should_not_see_element(context, selector):
    """Assert element is not visible."""
    context.actions.assert_hidden(selector)


@then('"{selector}" should have text "{text}"')
@then('"{selector}" should contain text "{text}"')
@then('I should see "{text}" in "{selector}"')
def step_should_have_text(context, selector, text):
    """Assert element contains text."""
    context.actions.assert_contains_text(selector, text)


@then('"{selector}" should have exact text "{text}"')
def step_should_have_exact_text(context, selector, text):
    """Assert element has exact text."""
    context.actions.assert_text(selector, text)


@then('"{selector}" should have value "{value}"')
@then('the value of "{selector}" should be "{value}"')
def step_should_have_value(context, selector, value):
    """Assert input has value."""
    context.actions.assert_value(selector, value)


@then('the page URL should be "{url}"')
@then('I should be on "{url}"')
def step_should_be_on_url(context, url):
    """Assert current URL."""
    context.actions.assert_url(url)


@then('the page URL should contain "{url}"')
def step_url_should_contain(context, url):
    """Assert URL contains text."""
    context.actions.assert_url(re.compile(url))


@then('the page title should be "{title}"')
def step_should_have_title(context, title):
    """Assert page title."""
    context.actions.assert_title(title)


@then('the page title should contain "{title}"')
def step_title_should_contain(context, title):
    """Assert title contains text."""
    context.actions.assert_title(re.compile(title))


@then('"{selector}" should be enabled')
def step_should_be_enabled(context, selector):
    """Assert element is enabled."""
    assert context.actions.is_enabled(selector), f"Element {selector} is not enabled"


@then('"{selector}" should be disabled')
def step_should_be_disabled(context, selector):
    """Assert element is disabled."""
    assert context.actions.is_disabled(selector), f"Element {selector} is not disabled"


@then('"{selector}" should be checked')
def step_should_be_checked(context, selector):
    """Assert checkbox is checked."""
    assert context.actions.is_checked(selector), f"Element {selector} is not checked"


@then('"{selector}" should not be checked')
@then('"{selector}" should be unchecked')
def step_should_not_be_checked(context, selector):
    """Assert checkbox is not checked."""
    assert not context.actions.is_checked(selector), f"Element {selector} is checked"


# Screenshot steps

@when('I take a screenshot')
@when('I take a screenshot named "{name}"')
def step_take_screenshot(context, name='screenshot'):
    """Take screenshot."""
    from datetime import datetime
    from pathlib import Path
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_name = f"{name}_{timestamp}.png"
    screenshot_path = Path('screenshots') / screenshot_name
    
    context.actions.take_screenshot(str(screenshot_path), full_page=True)
    context.logger.info(f"Screenshot saved: {screenshot_path}")


@when('I take a screenshot of "{selector}"')
@when('I take a screenshot of "{selector}" named "{name}"')
def step_take_element_screenshot(context, selector, name='element'):
    """Take screenshot of element."""
    from datetime import datetime
    from pathlib import Path
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_name = f"{name}_{timestamp}.png"
    screenshot_path = Path('screenshots') / screenshot_name
    
    context.actions.take_element_screenshot(selector, str(screenshot_path))
    context.logger.info(f"Element screenshot saved: {screenshot_path}")


# Scroll steps

@when('I scroll to "{selector}"')
def step_scroll_to_element(context, selector):
    """Scroll to element."""
    context.actions.scroll_to_element(selector)


@when('I scroll to the bottom')
@when('I scroll to bottom of page')
def step_scroll_to_bottom(context):
    """Scroll to bottom of page."""
    context.actions.scroll_to_bottom()


@when('I scroll to the top')
@when('I scroll to top of page')
def step_scroll_to_top(context):
    """Scroll to top of page."""
    context.actions.scroll_to_top()


# JavaScript execution steps

@when('I execute JavaScript "{script}"')
def step_execute_javascript(context, script):
    """Execute JavaScript."""
    context.actions.execute_script(script)


# Focus steps

@when('I focus on "{selector}"')
def step_focus_element(context, selector):
    """Focus on element."""
    context.actions.focus(selector)


# Generic get steps (for data extraction)

@when('I get the text from "{selector}" and store it as "{var_name}"')
@then('I get the text from "{selector}" and store it as "{var_name}"')
def step_get_and_store_text(context, selector, var_name):
    """Get text from element and store in context."""
    text = context.actions.get_text(selector)
    setattr(context, var_name, text)
    context.logger.info(f"Stored text '{text}' as {var_name}")


@when('I get the value from "{selector}" and store it as "{var_name}"')
@then('I get the value from "{selector}" and store it as "{var_name}"')
def step_get_and_store_value(context, selector, var_name):
    """Get value from element and store in context."""
    value = context.actions.get_value(selector)
    setattr(context, var_name, value)
    context.logger.info(f"Stored value '{value}' as {var_name}")