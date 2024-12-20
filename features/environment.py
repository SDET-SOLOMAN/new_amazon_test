from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.by import By

# Define CAPTCHA locators
IMG_CAPTCHA = (By.XPATH, "//*[@class='a-row a-text-center']/img")
CAPTCHA_FIELD = (By.CSS_SELECTOR, "#captchacharacters")
CAPTCHA_BUTTON = (By.XPATH, "//button[@type='submit']")


def browser_init(context):
    """
    Initialize the browser for the Behave context.
    """
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    context.driver = webdriver.Chrome(service=service)

    context.driver.maximize_window()
    context.driver.implicitly_wait(15)  # Reduced timeout for faster feedback


def is_captcha_present(driver):
    """
    Check if CAPTCHA is present on the page.
    """
    try:
        captcha = driver.find_element(*IMG_CAPTCHA)
        return captcha.is_displayed()
    except Exception:
        return False


def handle_captcha(driver):
    """
    Handle Amazon CAPTCHA if present.
    """
    try:
        link = driver.find_element(*IMG_CAPTCHA).get_attribute("src")
        print("CAPTCHA image link:", link)
        if link:
            image = AmazonCaptcha.fromlink(link)
            captcha_value = AmazonCaptcha.solve(image)
            print("CAPTCHA solved value:", captcha_value)
            driver.find_element(*CAPTCHA_FIELD).send_keys(captcha_value)
            driver.find_element(*CAPTCHA_BUTTON).click()
    except Exception as e:
        print("CAPTCHA handling failed:", e)


def before_scenario(context, scenario):
    """
    Actions to perform before each scenario.
    """
    print('\nStarted scenario:', scenario.name)
    browser_init(context)
    context.driver.get('https://www.amazon.com/')

    # Check for CAPTCHA and handle if present
    if is_captcha_present(context.driver):
        print("CAPTCHA detected, solving...")
        handle_captcha(context.driver)
    else:
        print("No CAPTCHA detected.")


def before_step(context, step):
    """
    Actions to perform before each step.
    """
    try:
        print(f"\nStarted step: {step.name}")
    except Exception as e:
        print(f"Error in before_step: {e}")


def after_step(context, step):
    """
    Actions to perform after each step.
    """
    if step.status == 'failed':
        print(f"\nStep failed: {step.name}")


def after_scenario(context, scenario):
    """
    Actions to perform after each scenario.
    """
    try:
        context.driver.quit()
    except Exception as e:
        print(f"Error during browser teardown: {e}")