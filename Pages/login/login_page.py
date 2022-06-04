from Utility.ui_utility import ElementInteractions


class LoginPage:
    """Xpath selectors and methods for the main login page"""

    # Xpath Selectors
    # Text boxes
    username_text_box = "//input[@id='user-name']"
    password_text_box = "//input[@id='password'] "

    # Buttons
    login_button = "//input[@id='login-button']"

    # Headers
    username_list = "//div[@id='login_credentials']"
    password_list = "//div[@class='login_password']"

    # Setters
    @classmethod
    def set_user_name(cls, value):
        ElementInteractions.enter_text(cls.username_text_box, value)

    @classmethod
    def set_password(cls, value):
        ElementInteractions.enter_text(cls.password_text_box, value)

    # Clicks
    @classmethod
    def click_login_button(cls):
        ElementInteractions.click(cls.login_button)

    # Actions
    @classmethod
    def user_login(cls, desired_user):
        raw_user_list = ElementInteractions.get_text(cls.username_list)
        raw_password = ElementInteractions.get_text(cls.password_list)

        # Splitting users into list of strings based on new lines(\n)
        list_of_users = raw_user_list.split('\n')
        # Removing the first item that is not user
        list_of_users.pop(0)
        # Getting the password
        password = raw_password.split('\n')
        password.pop(0)

        cls.set_user_name([v for v in list_of_users if desired_user in v])
        cls.set_password(password)
        cls.click_login_button()

    @classmethod
    def is_user_logged_out(cls):
        return ElementInteractions.is_displayed(LoginPage.login_button)
