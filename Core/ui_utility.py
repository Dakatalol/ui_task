from selenium.webdriver.common.by import By
from Core.webdriver_utility import WebdriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

BASE_TIMEOUT = 10


class ElementInteractions(WebdriverManager):
    """Helper utility for common UI commands"""

    @classmethod
    def enter_characters(cls, element: str, characters: str, index: int = 0, timeout: int = BASE_TIMEOUT):
        """
        Enter characters into an element

        Args:
            element: CSS selector or XPath
            characters: Characters to enter
            index: Index of the element
            timeout: Number of seconds to wait for the element

        Returns:
            None
        """
        ElementWait.wait_for_element_to_be_clickable(element, timeout)
        ele = cls.__get_desired_elements(element=element, index=index)
        ele.send_keys(characters)

    @classmethod
    def __get_desired_elements(cls, element: str, get_all: bool = False, index: int = 0):
        """
        Helper method to get css or xpath element back

        Args:
            element: CSS selector or XPath

        Returns:
            Element(s)
        """
        if element.startswith('/'):
            elements = cls.driver.find_elements(by=By.XPATH, value=element)
        else:
            elements = cls.driver.find_elements(by=By.CSS_SELECTOR, value=element)

        if get_all:
            return elements
        else:
            return elements[index]

    @classmethod
    def click(cls, element: str, timeout: int = BASE_TIMEOUT):
        """
        Click on an element

        Args:
            element: CSS selector or XPath
            timeout: Number of seconds to wait for the element

        Returns:
            None
        """
        ElementWait.wait_for_element_to_be_clickable(element, timeout)
        ele = cls.__get_desired_elements(element=element)
        ele.click()


class ElementWait(WebdriverManager):
    """Helper utility that waits for certain conditions to be met"""

    @classmethod
    def wait_for_element_to_be_clickable(cls, element: str, timeout: int = BASE_TIMEOUT, ):
        """
        Wait for an element to be clickable

        Args:
            element: CSS selector or XPath
            timeout: Number of seconds to wait for the element

        Returns:
            None
        """
        if element.startswith('/'):
            locator_type = By.XPATH
        else:
            locator_type = By.CSS_SELECTOR

        WebDriverWait(cls.driver, timeout).until(ec.presence_of_element_located((locator_type, element)))
