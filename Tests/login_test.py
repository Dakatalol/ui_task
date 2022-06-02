from Pages.login.login_page import LoginPage
from Pages.inventory.inventory_page import InventoryPage


def test_login():
    LoginPage.set_user_name("standard_user")
    LoginPage.set_password("secret_sauce")
    LoginPage.click_login_button()
    InventoryPage.add_first_and_last_item_to_cart()
    check = InventoryPage.is_item_in_cart("Sauce Labs Backpack")
    print("F")


