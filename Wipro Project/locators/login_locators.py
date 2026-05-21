from selenium.webdriver.common.by import By


class LoginLocators:
    SESSION_EXPIRED_MESSAGE = (
        By.XPATH,
        "//*[contains(normalize-space(), 'Your session has been expired') or contains(normalize-space(), 'session has been expired')]",
    )
    MOBILE_NUMBER_INPUTS = (
        (By.XPATH, "//input[@data-for='phnNumber']"),
        (By.XPATH, "//input[@placeholder='Phone Number']"),
        (By.XPATH, "//input[@title='Phone Number']"),
        (By.XPATH, "//input[@type='tel' or contains(@placeholder, 'Phone')]"),
    )
    CONTINUE_BUTTONS = (
        (By.XPATH, "//button[normalize-space()='Continue']"),
        (By.XPATH, "//*[@id='app']/div/div[7]/div[2]/div[1]/div/div/form/div[2]/button"),
    )
    USERNAME_FIELDS = (
        (By.XPATH, "//input[@type='tel' or @type='email' or contains(@placeholder, 'Mobile') or contains(@placeholder, 'Email')]"),
        (By.CSS_SELECTOR, "input[type='text']"),
    )
    PASSWORD_FIELDS = ((By.XPATH, "//input[@type='password']"),)
    LOGIN_DIALOG = (
        By.XPATH,
        "//*[contains(., 'Login') or contains(., 'LOGIN / REGISTER') or contains(., 'Mobile') or contains(., 'Email')][self::div or self::section or self::form]",
    )
    OTP_SUCCESS_INDICATORS = (
        (By.CSS_SELECTOR, "[data-label='USER_PROFILE_DROPDOWN']"),
        (By.XPATH, "//*[contains(., 'My99acres') or contains(., 'My Account') or contains(., 'Logout')]"),
    )

