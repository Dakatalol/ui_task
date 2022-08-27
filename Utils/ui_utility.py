import time

from selenium.webdriver.common.by import By
from Utils.webdriver_utility import WebdriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select

BASE_TIMEOUT = 10


class ElementInteractions(WebdriverManager):
    """Helper utility for common UI commands"""

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
    def enter_text(cls, element: str, characters: str, index: int = 0, timeout: int = BASE_TIMEOUT):
        """
        Enter text into an element

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
    def click(cls, element: str, index: int = 0, timeout: int = BASE_TIMEOUT):
        """
        Click on an element

        Args:
            element: CSS selector or XPath
            index: Override to select a specific occurrence of the element
            timeout: Number of seconds to wait for the element
        Returns:
            None
        """
        ElementWait.wait_for_element_to_be_clickable(element, timeout)
        ele = cls.__get_desired_elements(element=element, index=index)
        ele.click()

    @classmethod
    def get_number_of_elements(cls, element: str):
        """
        Get the number of elements found for a CSS selector or XPath

        Args:
            element: CSS selector or XPath

        Returns:
            Integer - The number of elements found with that CSS selector or XPath
        """
        return len(cls.__get_desired_elements(element, get_all=True))

    @classmethod
    def get_text(cls, element: str, get_all: bool = False, index: int = 0, timeout: int = BASE_TIMEOUT):
        """
        Get the text of element(s)

        Args:
            element: CSS selector or XPath
            get_all: Override to get all occurrences of the element
            index: Override to select a specific occurrence of the element
            timeout: Number of seconds to wait for the element
        Returns:
            Text value(s) of the element(s)
        """
        ElementWait.wait_for_element_to_appear(element, timeout)
        ele = cls.__get_desired_elements(element=element, index=index, get_all=get_all)
        if get_all:
            all_elements = []
            for el in ele:
                all_elements.append(el.text)
            return all_elements
        else:
            return ele.text

    @classmethod
    def is_displayed(cls, element: str, index: int = 0):
        """
        Check if an element is displayed on the page

        Args:
            element: CSS selector or Xpath
            index: select specific occurrence of the element
        Returns:
             none
        """
        try:
            ele = cls.__get_desired_elements(element=element, index=index)
            return ele.is_displayed()
        except IndexError:
            return False

    @classmethod
    def select_dropdown_item(cls, element: str, dropdown_item: str, index: int = 0, timeout: int = BASE_TIMEOUT):
        """
        Select an item from a dropdown element

        Args:
            element: CSS selector or XPath
            dropdown_item: Value to select
            index: Override to select a specific occurrence of the element
            timeout: Number of seconds to wait for the element
        Returns:
            None
        """
        ElementWait.wait_for_element_to_appear(element, timeout)
        ele = cls.__get_desired_elements(element=element, index=index)
        Select(ele).select_by_visible_text(dropdown_item)


class ElementWait(WebdriverManager):
    """Helper utility that waits for certain conditions to be met"""

    @classmethod
    def wait_for_element_to_be_clickable(cls, element: str, timeout: int = BASE_TIMEOUT):
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

    @classmethod
    def wait_for_element_to_appear(cls, element: str, timeout: int = BASE_TIMEOUT):
        """
        Wait for an element to appear on the page

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

        WebDriverWait(cls.driver, timeout).until(ec.visibility_of_element_located((locator_type, element)))
