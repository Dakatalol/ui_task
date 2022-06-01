from Pages.login.login_page import LoginPage
from Pages.inventory.inventory_page import InventoryPage


def test_login():
    LoginPage.set_user_name("standard_user")
    LoginPage.set_password("secret_sauce")
    LoginPage.click_login_button()
    InventoryPage.get_item_by_number_and_add_to_cart(2)
    print("F")


