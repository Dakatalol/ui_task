from Core.ui_utility import ElementInteractions


class LoginPage:
    """Xpath selectors and methods for the main login page"""

    # Xpath Selectors
    # Text boxes
    username_text_box = "//input[@id='user-name']"
    password_text_box = "//input[@id='password'] "

    # Buttons
    login_button = "//input[@id='login-button']"

    # Setters
    @classmethod
    def set_user_name(cls, value):
        ElementInteractions.enter_characters(cls.username_text_box, value)

    @classmethod
    def set_password(cls, value):
        ElementInteractions.enter_characters(cls.password_text_box, value)

    # Clicks
    @classmethod
    def click_login_button(cls):
        ElementInteractions.click(cls.login_button)
