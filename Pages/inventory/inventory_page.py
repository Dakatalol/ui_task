from Core.ui_utility import ElementInteractions


class InventoryPage:
    """Xpath selectors and methods for the main inventory page"""

    # Xpath Selectors
    # Buttons
    backpack_button = "//button[@id='add-to-cart-sauce-labs-backpack']"
    bike_light_button = "//input[@id='login-button']"
    bolt_t_shirt_button = ""
    fleece_jacket_button = ""
    labs_onesie_button = ""
    red_t_shirt_button = ""

    inventory_list = "//div[@class='inventory_list']"

    all_inventory_buttons = "//button[@class='btn btn_primary btn_small btn_inventory']"
    test_button = "//button[contains(text(),'Add')][2]"

    # Getters
    @classmethod
    def get_specific_item(cls, number):
        return ElementInteractions.get_attribute(cls.inventory_list, attribute='innerHTML', index=number)

    @classmethod
    def get_item_by_number_and_add_to_cart(cls, number):
        desired_item_button = cls.all_inventory_buttons + "[{number}]".format(number=number)
        ElementInteractions.click(cls.test_button)
