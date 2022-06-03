import pytest

from Pages.login.login_page import LoginPage
from Pages.inventory.inventory_page import InventoryPage


@pytest.mark.smoke
def test_variant_one():
    LoginPage.login_standard_user()
    InventoryPage.add_first_and_last_item_to_cart()
    InventoryPage.go_to_cart()
    assert InventoryPage.is_item_in_cart("Sauce Labs Backpack") and \
           InventoryPage.is_item_in_cart("Test.allTheThings() T-Shirt (Red)")
    InventoryPage.remove_first_item_from_cart()
    InventoryPage.return_to_shopping_inventory()
    InventoryPage.add_previous_to_the_last_item()
    InventoryPage.go_to_cart()
    assert InventoryPage.is_item_in_cart("Sauce Labs Onesie") and \
           InventoryPage.is_item_in_cart("Test.allTheThings() T-Shirt (Red)")
    InventoryPage.go_to_checkout()
    InventoryPage.fill_shipment_info()
    InventoryPage.continue_to_checkout_and_finish_order()
    assert InventoryPage.is_order_placed()
    InventoryPage.go_to_cart()
    assert not InventoryPage.is_shopping_cart_empty()
    InventoryPage.logout_from_inventory()
    assert LoginPage.is_user_logged_out()


@pytest.mark.regression
def test_variant_two():
    LoginPage.set_user_name("standard_user")
    LoginPage.set_password("secret_sauce")
    LoginPage.click_login_button()
    InventoryPage.select_descending_price_ordering()
    assert InventoryPage.is_prices_listed_descending()
    InventoryPage.logout_from_inventory()
    assert LoginPage.is_user_logged_out()
