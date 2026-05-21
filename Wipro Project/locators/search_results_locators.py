from selenium.webdriver.common.by import By


class SearchResultsLocators:
    RESULTS_CONTAINER = (
        By.XPATH,
        "//*[contains(@class, 'srp') or contains(@class, 'result') or contains(., 'Properties') or contains(., 'results')]",
    )
    RESULTS_CARDS = (
        By.XPATH,
        "//div[contains(@class,'srpTuple') or contains(@class,'tupleCard') or contains(@class,'propertyTuple')]",
    )
    BUDGET_MIN_DROPDOWN = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[2]/div/div[1]",
    )
    BUDGET_MIN_OPTION = (By.XPATH, '//*[@id="lf_budget_min_list"]/li[5]')
    BUDGET_MAX_DROPDOWN = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[2]/div/div[3]",
    )
    BUDGET_MAX_DROPDOWN_FALLBACK = (
        By.XPATH,
        "//*[contains(@class, 'bdf__maxValue') and normalize-space()='No max']",
    )
    BUDGET_MAX_OPTION = (By.XPATH, '//*[@id="lf_budget_max_list"]/li[11]')
    PROPERTY_TYPE_SECTION = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[4]/div/div/div[2]/div[2]",
    )
    PROPERTY_TYPE_SECTION_FALLBACK = (
        By.XPATH,
        "(//*[@id='property_type' and self::div]/following-sibling::div//*[contains(@data-label, 'PROPTYPE') or @datalabel='PROPTYPE_CLUSTER'])[2]",
    )
    FINAL_ACTION_BUTTON = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[3]/div[3]/div[2]/section[2]/div/div/div[2]/div[2]/button[1]",
    )
    FINAL_ACTION_BUTTON_FALLBACKS = (
        FINAL_ACTION_BUTTON,
        (
            By.XPATH,
            "/html/body/div[1]/div/div/div[4]/div[3]/div[2]/section[2]/div/div/div[2]/div[2]/button[1]",
        ),
        (By.XPATH, "//section[2]//div[2]/div[2]/button[1]"),
        (By.XPATH, "(//section[2]//button)[1]"),
    )
    RESIDENTIAL_APARTMENT_OPTION = (
        By.XPATH,
        "//*[@id='property_type' and self::div]/following-sibling::div//*[@datalabel='PROPTYPE_CLUSTER' and @id='1']",
    )
    OWNER_OPTION = (By.XPATH, '//*[@id="__Owner__"]')
    BHK_FILTER_OPTION_ONE = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[7]/div/div[2]/div/div[1]",
    )
    BHK_FILTER_OPTION_ONE_FALLBACK = (
        By.XPATH,
        "//*[@id='bedroom_num' and self::div]/following-sibling::div//*[@datalabel='BEDROOM_CLUSTER' and @id='1']",
    )
    BHK_FILTER_OPTION_TWO = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[7]/div/div[2]/div/div[3]",
    )
    BHK_FILTER_OPTION_TWO_FALLBACK = (
        By.XPATH,
        "//*[@id='bedroom_num' and self::div]/following-sibling::div//*[@datalabel='BEDROOM_CLUSTER' and @id='3']",
    )
    FURNISHING_OPTION = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[8]/div/div/div[2]/div[1]/div/label",
    )
    FURNISHING_SECTION = (By.XPATH, "//*[@id='furnish' and self::div]")
    FURNISHING_OPTION_FALLBACK = (
        By.XPATH,
        "//*[@id='furnish' and self::div]/following-sibling::div//*[self::div or self::label][normalize-space()][1]",
    )
    ADDITIONAL_FILTER_OPTION_ONE = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[11]/div/div/div[2]/div[3]",
    )
    ADDITIONAL_FILTER_OPTION_ONE_FALLBACK = (
        By.XPATH,
        "//*[@id='amenities' and self::div]/following-sibling::div//*[@datalabel='AMENITIES_CLUSTER'][3]",
    )
    ADDITIONAL_FILTER_OPTION_TWO = (
        By.XPATH,
        "/html/body/div[1]/div/div/div[4]/div[2]/div/div[11]/div/div/div[2]/div[2]",
    )
    ADDITIONAL_FILTER_OPTION_TWO_FALLBACK = (
        By.XPATH,
        "//*[@id='amenities' and self::div]/following-sibling::div//*[@datalabel='AMENITIES_CLUSTER'][2]",
    )
    ACTIVE_FILTER_BADGES = (
        By.XPATH,
        "//*[contains(@class,'appliedFilter') or contains(@class,'filterChip') or contains(@class,'selectedFilters')]",
    )
    SORT_OR_FILTER_PANEL = (
        By.XPATH,
        "//*[contains(@class,'filters') or contains(@class,'filter') or contains(., 'Budget')]",
    )
    FIRST_PROPERTY_LINKS = (
        (By.XPATH, "(//a[contains(@href,'property') or contains(@href,'project')])[1]"),
        (By.XPATH, "(//*[contains(@class,'srpTuple')]//a)[1]"),
        (By.XPATH, "(//a[contains(@href,'/buy/') or contains(@href,'/project-') or contains(@href,'/property-in-')])[1]"),
        (By.XPATH, "(//section//a[@href])[1]"),
    )
