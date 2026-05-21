from selenium.webdriver.common.by import By


class AccountLocators:
    ACCOUNT_MENU_TRIGGERS = (
        (By.CSS_SELECTOR, "[data-label='USER_PROFILE_DROPDOWN']"),
        (By.XPATH, "//*[contains(@class,'user') or contains(@class,'profile')][self::div or self::a or self::button or self::i]"),
    )
    LOGOUT_OPTIONS = (
        (By.XPATH, "//*[normalize-space()='Logout' or normalize-space()='Log Out']"),
        (By.XPATH, "//a[contains(., 'Logout') or contains(., 'Log Out')]"),
        (By.XPATH, "//button[contains(., 'Logout') or contains(., 'Log Out')]"),
    )
    POST_LOGOUT_INDICATORS = (
        (By.XPATH, "//*[contains(text(),'LOGIN / REGISTER') or contains(text(),'Login / Register')]"),
        (By.CSS_SELECTOR, ".hmenu__loginRegister"),
    )

