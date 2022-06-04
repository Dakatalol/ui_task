import pytest

from Pages.login.login_page import LoginPage
from Pages.inventory.inventory_page import InventoryPage


@pytest.mark.smoke
def test_variant_one():
    # Log in with the standard user
    LoginPage.user_login("standard")

    # Add the first and the last item in the cart, verify the correct items are added
    InventoryPage.add_first_and_last_item_to_cart()
    InventoryPage.go_to_cart()
    assert InventoryPage.is_item_in_cart("Sauce Labs Backpack") and \
           InventoryPage.is_item_in_cart("Test.allTheThings() T-Shirt (Red)")

    # Remove the first item and add previous to the last item to the cart, verify the content again
    InventoryPage.remove_first_item_from_cart()
    InventoryPage.return_to_shopping_inventory()
    InventoryPage.add_previous_to_the_last_item()
    InventoryPage.go_to_cart()
    assert InventoryPage.is_item_in_cart("Sauce Labs Onesie") and \
           InventoryPage.is_item_in_cart("Test.allTheThings() T-Shirt (Red)")

    # Go to checkout
    InventoryPage.go_to_checkout()

    # Finish the order
    InventoryPage.fill_shipment_info()
    InventoryPage.continue_to_checkout_and_finish_order()

    # Verify order is placed
    assert InventoryPage.is_order_placed()

    # Verify cart is empty
    InventoryPage.go_to_cart()
    assert not InventoryPage.is_shopping_cart_empty()

    # Logout from the system
    InventoryPage.logout_from_inventory()
    assert LoginPage.is_user_logged_out()


@pytest.mark.regression
def test_variant_two():
    # Log in with the standard user
    LoginPage.user_login("standard")

    # Verify when for sorting it is selected "Price (high to low)"
    InventoryPage.select_descending_price_ordering()
    # Then the items are sorted in the correct manner
    assert InventoryPage.is_prices_listed_descending()

    # Logout from the system
    InventoryPage.logout_from_inventory()
    assert LoginPage.is_user_logged_out()
