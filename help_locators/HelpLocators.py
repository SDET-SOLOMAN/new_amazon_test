from selenium.webdriver.common.by import By



class HelpLocators():
    #captcha locators
    IMG_CAPTCHA = (By.XPATH, "//*[@class='a-row a-text-center']/img")
    CAPTCHA_FIELD = (By.CSS_SELECTOR, "#captchacharacters")
    CAPTCHA_BUTTON = (By.XPATH, "//button[@type='submit']")