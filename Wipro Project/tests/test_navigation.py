from __future__ import annotations

import allure
import pytest

from pages.home_page import HomePage
from tests.base_test import BaseTest


@allure.epic("99acres")
@allure.feature("Navigation")
@pytest.mark.navigation
class TestNavigation(BaseTest):
    @allure.title("Verify primary menu items are visible on home page")
    @pytest.mark.smoke
    def test_primary_menu_items_visible(self, base_url: str, test_data: dict) -> None:
        home_page = HomePage(self.driver)
        home_page.open(base_url)

        expected_items = test_data["navigation"]["primary_menu_items"]
        assert home_page.are_primary_menu_items_visible(expected_items), "One or more expected primary menu items are missing."
