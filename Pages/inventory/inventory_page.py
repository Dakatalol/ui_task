from Core.ui_utility import ElementInteractions


class InventoryPage:
    """Xpath selectors and methods for the main inventory page"""

    # Xpath Selectors
    # Buttons
    list_of_buttons = "//button[@class='btn btn_primary btn_small btn_inventory']"
    items_names_in_cart = "//div[@class='inventory_item_name']"

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
    def is_item_in_cart(cls, item):
        return item in ElementInteractions.get_text(cls.items_names_in_cart, get_all=True)
