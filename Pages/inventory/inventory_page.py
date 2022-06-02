from Core.ui_utility import ElementInteractions, ElementWait
from Pages.login.login_page import LoginPage


class InventoryPage:
    """Xpath selectors and methods for the main inventory page"""

    # Xpath Selectors
    # Text boxes
    first_name_text_box = "//input[@id='first-name']"
    last_name_text_box = "//input[@id='last-name']"
    postal_code_text_box = "//input[@id='postal-code']"
    completed_order_header = "//h2[@class='complete-header']"
    shopping_cart_badge = "//span[@class='shopping_cart_badge']"

    # Buttons
    list_of_buttons = "//button[@class='btn btn_primary btn_small btn_inventory']"
    items_names_in_cart = "//div[@class='inventory_item_name']"
    shopping_cart_button = "//a[@class='shopping_cart_link']"
    remove_buttons_in_cart = "//button[@class='btn btn_secondary btn_small cart_button']"
    continue_shopping_button = "//button[@id='continue-shopping']"
    checkout_button = "//button[@id='checkout']"
    continue_checkout_button = "//input[@id='continue']"
    finish_order_button = "//button[@id='finish']"
    hamburger_menu_button = "//button[@id='react-burger-menu-btn']"
    logout_button = "//a[@id='logout_sidebar_link']"

    # Getters
    @classmethod
    def get_number_of_items(cls):
        return ElementInteractions.get_number_of_elements(cls.list_of_buttons)

    @classmethod
    def get_item_by_number_and_add_to_cart(cls, number):
        ElementInteractions.click(cls.list_of_buttons, index=number)

    # Actions
    @classmethod
    def add_first_and_last_item_to_cart(cls):
        # adding the first item from the inventory
        cls.get_item_by_number_and_add_to_cart(0)
        # adding the last item from the inventory
        cls.get_item_by_number_and_add_to_cart(cls.get_number_of_items() - 1)

    @classmethod
    def go_to_cart(cls):
        ElementInteractions.click(cls.shopping_cart_button)

    @classmethod
    def is_item_in_cart(cls, item):
        return item in ElementInteractions.get_text(cls.items_names_in_cart, get_all=True)

    @classmethod
    def remove_first_item_from_cart(cls):
        ElementInteractions.click(cls.remove_buttons_in_cart, index=0)

    @classmethod
    def return_to_shopping_inventory(cls):
        ElementInteractions.click(cls.continue_shopping_button)

    @classmethod
    def add_previous_to_the_last_item(cls):
        cls.get_item_by_number_and_add_to_cart(cls.get_number_of_items() - 1)

    @classmethod
    def go_to_checkout(cls):
        ElementInteractions.click(cls.checkout_button)

    @classmethod
    def fill_shipment_info(cls):
        ElementInteractions.enter_text(cls.first_name_text_box, "Peshko")
        ElementInteractions.enter_text(cls.last_name_text_box, "Peshkov")
        ElementInteractions.enter_text(cls.postal_code_text_box, "7000")

    @classmethod
    def continue_to_checkout_and_finish_order(cls):
        ElementInteractions.click(cls.continue_checkout_button)
        ElementInteractions.click(cls.finish_order_button)

    @classmethod
    def is_order_placed(cls):
        return "THANK YOU FOR YOUR ORDER" in ElementInteractions.get_text(cls.completed_order_header)

    @classmethod
    def is_shopping_cart_empty(cls):
        return ElementInteractions.is_displayed(cls.shopping_cart_badge)

    @classmethod
    def logout_from_inventory(cls):
        ElementInteractions.click(cls.hamburger_menu_button)
        ElementWait.wait_for_element_to_appear(cls.logout_button)
        ElementInteractions.click(cls.logout_button)

    @classmethod
    def is_user_logged_out(cls):
        return ElementInteractions.is_displayed(LoginPage.login_button)
