from selenium.webdriver.common.by import By


class HomeLocators:
    COOKIE_OK_BUTTON = (By.XPATH, "//button[normalize-space()='Okay' or normalize-space()='OK']")
    LOGIN_ICON = (By.XPATH, "//i[contains(@class,'icon_userWhite') and contains(@class,'theader__dot')]")
    LOGIN_OPTION = (
        By.XPATH,
        "//*[contains(text(),'LOGIN / REGISTER') or contains(text(),'Login / Register') or "
        "contains(text(),'LOGIN/REGISTER') or contains(text(),'Login/Register')]",
    )
    LOGIN_ENTRY_POINTS = (
        LOGIN_OPTION,
        (By.CSS_SELECTOR, "[data-label='USER_PROFILE_DROPDOWN']"),
        (By.CSS_SELECTOR, "[data-label='LR.INITIATE']"),
        (By.CSS_SELECTOR, ".hmenu__loginRegister"),
        (By.XPATH, "//a[contains(., 'Login') or contains(., 'login')]"),
        (By.XPATH, "//button[contains(., 'Login') or contains(., 'login')]"),
        (By.XPATH, "//*[contains(@class, 'login') or contains(@id, 'login')]"),
    )
    LANDMARK_SEARCH_BAR = (By.XPATH, '//*[@id="d_landmark_inPageSearchBox"]')
    LANDMARK_SEARCH_INPUT = (By.XPATH, '//*[@id="d_landmark_inPageSearchBox"]//input')
    SEARCH_ICON_BY_ID = (By.XPATH, '//*[@id="searchform_search_btn"]')
    SEARCH_INPUTS = (
        (By.ID, "keyword2"),
        (By.CSS_SELECTOR, "#d_landmark_inPageSearchBox input[name='keyword']"),
        (By.CSS_SELECTOR, ".inPageSearchBox__searchFieldInput input"),
        (By.XPATH, "//input[contains(@placeholder, 'Search') or contains(@placeholder, 'City') or contains(@placeholder, 'Locality')]"),
        (By.CSS_SELECTOR, "input[type='text']"),
        (By.XPATH, "//*[@contenteditable='true']"),
    )
    SEARCH_BUTTONS = (
        (By.ID, "searchform_search_btn"),
        (By.XPATH, "//button[contains(., 'Search')]"),
        (By.XPATH, "//*[self::button or self::a][contains(@class, 'search') or contains(@id, 'search')]"),
    )

