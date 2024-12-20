from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from behave import given, when, then
from time import sleep

HOME_PAGE = "https://www.amazon.com/"
SEARCH_BOX = (By.XPATH, "//input[@type='text']")
SEARCH_ICON = (By.XPATH, "//div[@class='nav-right'] // input[contains(@type, 'submit')]")

@given("Open Amazon Home page")
def amazon_home_page_is_opened(context):
    context.driver.get(HOME_PAGE)


@when("Click on Search Bar")
def amazon_search_box(context):
    context.driver.find_element(*SEARCH_BOX).click()


@when("Input {text} into Amazon Search Box")
def input_text_into_amazon_search_box(context, text):
    context.driver.find_element(*SEARCH_BOX).send_keys(text)


@when("Click on Amazon search icon")
def amazon_search_icon(context):
    """
    Click on the Amazon search icon. If the search icon is not found, press Enter in the search box.
    """
    try:
        # Attempt to find and click the search icon
        context.driver.find_element(*SEARCH_ICON).click()
    except NoSuchElementException as e:
        print(f"Search icon not found, falling back to pressing Enter: {e}")
        # If search icon is not found, press Enter in the search box
        search_box = context.driver.find_element(*SEARCH_BOX)
        search_box.send_keys(Keys.RETURN)

@then("Verify that the results for {text} are shown")
def is_search_results_shown(context, text):
    SEARCH_TEXT = (By.XPATH, f"//div // span[contains(text(), '{text}')]")
    shown_result = context.driver.find_element(*SEARCH_TEXT)
    assert shown_result.is_displayed(), f"Shown result is not displayed: {shown_result}"
    print(shown_result.text)
    assert shown_result.text == f'"{text}"', f"Shown result is not '{text}'"


@then("Verify that {number} of the search result == {expected}")
def is_it_nth_element_of_search(context, number, expected):
    SEARCH_RESULTS = (By.XPATH, f"//span[@data-component-type] / div / div[contains(@class, 'sg-col')][{number}]")
    actual_text = context.driver.find_element(*SEARCH_RESULTS).text
    context.driver.find_element(*SEARCH_RESULTS).click()
    sleep(5)
    expected_list = expected.lower().split()
    assert any(item in actual_text.lower() for item in expected_list), f"Expected: {expected}, Actual: {actual_text}"
