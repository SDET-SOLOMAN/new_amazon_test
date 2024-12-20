from selenium.webdriver.common.by import By
from behave import given, when, then
from time import sleep

HOME_PAGE = "https://www.amazon.com/"
SEARCH_BOX = (By.XPATH, "//input[@type='text']")
SEARCH_ICON = (By.XPATH, "//div[@class='nav-right'] // input[contains(@type, 'submit')]")