from selenium.webdriver.common.by import By


class PropertyDetailsLocators:
    DETAIL_PAGE_ANCHORS = (
        (By.XPATH, "//*[contains(@class,'pdp') or contains(@class,'propertyHeading') or contains(@class,'overview')]"),
        (By.XPATH, "//*[contains(., 'Property Details') or contains(., 'Overview') or contains(., 'Description')]"),
    )
    PRICE_SECTION = (
        By.XPATH,
        "//*[contains(@class,'price') or contains(., 'Price') or contains(., 'Lac') or contains(., 'Cr')]",
    )
    TITLE_SECTION = (
        By.XPATH,
        "//*[self::h1 or self::h2][normalize-space()]",
    )
    LOCATION_SECTION = (
        By.XPATH,
        "//*[contains(@class,'location') or contains(@class,'address') or contains(., 'Mumbai')]",
    )

