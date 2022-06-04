from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


class WebdriverManager:
    """Configurations for all browsers. Add your selection after --browser in the command line"""
    BROWSER_OPTIONS = {'chrome', 'firefox'}
    CHROME_OPTIONS = None
    DESIRED_CAPABILITIES = None
    driver = None

    @classmethod
    def __configure_browser(cls, browser: str = 'chrome'):
        """
        Set the Desired Capabilities and Chrome Options for the driver

        Args:
            browser: Name of the targeted browser
        Returns:
            None
        """

        if browser not in cls.BROWSER_OPTIONS:
            raise ValueError('Invalid browser, expected one of the following: %s' % cls.BROWSER_OPTIONS)

        elif browser == 'chrome':
            cls.CHROME_OPTIONS = webdriver.ChromeOptions()
            cls.DESIRED_CAPABILITIES = {'browserName': 'chrome', 'platform': 'WINDOWS'}
            cls.CHROME_OPTIONS.add_argument("--disable-popup-blocking")
            cls.CHROME_OPTIONS.add_experimental_option('prefs', {'credentials_enable_service': False})
            cls.CHROME_OPTIONS.add_experimental_option('excludeSwitches', ['enable-automation'])
            cls.CHROME_OPTIONS.add_experimental_option('useAutomationExtension', False)

        elif browser == 'firefox':
            cls.DESIRED_CAPABILITIES = {'browserName': 'firefox', 'platform': 'WINDOWS'}

    @classmethod
    def create_driver(cls, browser: str = 'chrome'):
        """

        Args:
            browser: Name of the targeted browser

        Returns:
            None
        """
        cls.__configure_browser(browser)

        if browser == 'chrome':
            cls.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=cls.CHROME_OPTIONS)

        elif browser == 'firefox':
            cls.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    @classmethod
    def get_driver(cls):
        """
        Get the class level webdriver

        Returns:
            Class level webdriver, if configured
        """
        return cls.driver
