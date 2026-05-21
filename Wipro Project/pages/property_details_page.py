from __future__ import annotations

from locators.property_details_locators import PropertyDetailsLocators
from pages.base_page import BasePage


class PropertyDetailsPage(BasePage):
    def is_property_details_page_opened(self) -> bool:
        return self.wait_utils.any_visible(PropertyDetailsLocators.DETAIL_PAGE_ANCHORS, timeout=15)

    def has_property_title(self) -> bool:
        return self.is_visible(PropertyDetailsLocators.TITLE_SECTION, timeout=10)

    def has_price_information(self) -> bool:
        return self.is_visible(PropertyDetailsLocators.PRICE_SECTION, timeout=10)

    def contains_location(self, location: str) -> bool:
        return location.lower() in self.driver.page_source.lower() or self.is_visible(
            PropertyDetailsLocators.LOCATION_SECTION,
            timeout=5,
        )

