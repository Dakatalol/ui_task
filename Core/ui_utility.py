import json
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from Core.webdriver_utility import WebdriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

BASE_TIMEOUT = 10


class ElementInteractions(WebdriverManager):
    """Helper utility for common UI commands"""

    @classmethod
    def enter_characters(cls, element: str, characters: str, index: int = 0,
                         timeout: int = BASE_TIMEOUT):
        """
        Enter characters into an element

        Args:
            element: CSS selector or XPath
            characters: Characters to enter
            timeout: Number of seconds to wait for the element

        Returns:
            None
        """
        ElementWait.wait_for_element_to_be_clickable(element, timeout, continue_on_timeout=True)
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
        ElementWait.wait_for_element_to_be_clickable(element, timeout, continue_on_timeout=True)
        ele = cls.__get_desired_elements(element=element)
        ele.click()

    @classmethod
    def enter_characters_at_coordinate_offset(cls, characters: str, x_offset: float = 0, y_offset: float = 0,
                                              reset_actions: bool = True):
        """
        Enter character string at coordinate offset

        Args:
            characters: Character string to be sent to coordinate offset
            x_offset: Override to provide X offset to move to. Can be positive or negative
            y_offset: Override to provide Y offset to move to. Can be positive or negative
            reset_actions: Override to disable action reset

        Returns:
            None
        """
        actions = ActionChains(cls.driver)
        actions.move_by_offset(x_offset, y_offset)
        actions.send_keys(characters)
        actions.perform()
        if reset_actions:
            actions.reset_actions()

    @classmethod
    def execute_script(cls, script: str, element: str = None, timeout: int = BASE_TIMEOUT, index: int = 0,
                       scroll_options: {} = None):
        """
        Execute a JavaScript command

        Args:
            script: JavaScript command to execute
            element: Override to target a CSS selector or XPath
            timeout: Number of seconds to wait for the element
            index: in case your CSS selector or XPath returns multiple WebElements, you can choose which one to use
            scroll_options: options to use for scrolling (see scroll_into_view method for examples)

        Returns:
            The return value of the JavaScript command
        """
        if element is not None:
            ElementWait.wait_for_element_to_be_clickable(element, timeout, continue_on_timeout=True)
            ele = cls.__get_desired_elements(element=element, index=index)
            return cls.driver.execute_script(script, ele)
        else:
            return cls.driver.execute_script(script)

    @classmethod
    def get_attribute(cls, element: str, attribute: str, get_all: bool = False, index: int = 0,
                      timeout: int = BASE_TIMEOUT, scroll_options: {} = None):
        """
        Get the value of attribute(s)

        Args:
            element: CSS selector or XPath
            attribute: Name of the targeted attribute
            get_all: Override to get all occurrences of the element
            index: Override to select a specific occurrence of the element
            timeout: Number of seconds to wait for the element
            scroll_options: options to use for scrolling (see scroll_into_view method for examples)

        Returns:
            Value(s) of the targeted attribute(s)
        """
        ElementWait.wait_for_element_to_appear(element, timeout, continue_on_timeout=True)
        ele = cls.__get_desired_elements(element=element, index=index, get_all=get_all)
        if get_all:
            all_elements = []
            for el in ele:
                all_elements.append(el.get_attribute(attribute))
            return all_elements
        else:
            return ele.get_attribute(attribute)

    @classmethod
    def get_canvas_location(cls, element: str, scroll_to_element: bool = True, scroll_options: {} = None):
        """
        Get the coordinates of the canvas

        Args:
            element: CSS selector or XPath for the canvas
            scroll_to_element: Override to prevent scrolling to the element
            scroll_options: options to use for scrolling (see scroll_into_view method for examples)

        Returns:
            dict - contains x and y coordinates
        """
        ele = cls.__get_desired_elements(element, scroll_to_element=scroll_to_element, scroll_options=scroll_options)
        return ele.location

    @classmethod
    def get_css_value(cls, element: str, css_value: str, get_all: bool = False, index: int = 0,
                      timeout: int = BASE_TIMEOUT):
        """
        Get the value of CSS selector(s) or XPath(s)

        Args:
            element: CSS selector or XPath
            css_value: Name of the targeted CSS selector
            get_all: Override to get all occurrences of the element
            index: Override to select a specific occurrence of the element
            timeout: Number of seconds to wait for the element

        Returns:
            Value(s) of the targeted CSS selector(s)
        """
        ElementWait.wait_for_element_to_appear(element, timeout, continue_on_timeout=True)
        ele = cls.__get_desired_elements(element=element, index=index, get_all=get_all)
        if get_all:
            all_elements = []
            for el in ele:
                all_elements.append(el.value_of_css_property(css_value))
            return all_elements
        else:
            return ele.value_of_css_property(css_value)

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
    def get_multi_select_dropdown_selections(cls, element: str, get_all: bool = False, index: int = 0,
                                             timeout: int = BASE_TIMEOUT, scroll_options: {} = None):
        """
        Get all the selected values from multi-select dropdown(s)

        Args:
            element: CSS selector or XPath
            get_all: Override to get all occurrences of the element
            index: Override to select a specific occurrence of the element
            timeout: Number of seconds to wait for the element
            scroll_options: options to use for scrolling (see scroll_into_view method for examples)

        Returns:
            Selected values of the multi-select dropdown(s)
        """
        ElementWait.wait_for_element_to_appear(element, timeout, continue_on_timeout=True)
        elements = cls.__get_desired_elements(element=element, index=index, get_all=get_all,
                                              scroll_options=scroll_options)

        def get_selected_items(ele):
            all_elements = Select(ele).all_selected_options
            all_values = []
            for selected_element in all_elements:
                all_values.append(selected_element.text)
            return all_elements

        if get_all:
            all_dropdown_multi_values = []
            for el in elements:
                all_dropdown_multi_values.append(get_selected_items(el))
            return all_dropdown_multi_values
        else:
            return get_selected_items(elements)

    @classmethod
    def get_selected_dropdown_text(cls, element: str, get_all: bool = False, index: int = 0,
                                   timeout: int = BASE_TIMEOUT, scroll_options: {} = None):
        """
        Get the selected value of dropdown(s)

        Args:
            element: CSS selector or XPath
            get_all: Override to get all occurrences of the element
            index: Override to select a specific occurrence of the element
            timeout: Number of seconds to wait for the element
            scroll_options: options to use for scrolling (see scroll_into_view method for examples)

        Returns:
            Selected value of the dropdown(s)
        """
        ElementWait.wait_for_element_to_appear(element, timeout, continue_on_timeout=True)
        ele = cls.__get_desired_elements(element=element, index=index, get_all=get_all, scroll_options=scroll_options)
        if get_all:
            all_values = []
            for el in ele:
                all_values.append(Select(el).first_selected_option.text)
            return all_values
        else:
            return Select(ele).first_selected_option.text

    @classmethod
    def get_text(cls, element: str, get_all: bool = False, index: int = 0, timeout: int = BASE_TIMEOUT,
                 scroll_options: {} = None):
        """
        Get the text of element(s)

        Args:
            element: CSS selector or XPath
            get_all: Override to get all occurrences of the element
            index: Override to select a specific occurrence of the element
            timeout: Number of seconds to wait for the element
            scroll_options: options to use for scrolling (see scroll_into_view method for examples)

        Returns:
            Text value(s) of the element(s)
        """
        ElementWait.wait_for_element_to_appear(element, timeout, continue_on_timeout=True)
        ele = cls.__get_desired_elements(element=element, index=index, get_all=get_all, scroll_options=scroll_options)
        if get_all:
            all_elements = []
            for el in ele:
                all_elements.append(el.text)
            return all_elements
        else:
            return ele.text

    @classmethod
    def is_class_present(cls, element: str, element_class: str, index: int = 0, scroll_options: {} = None):
        """
        Check if a class is present on an element

        Args:
            element: CSS selector or XPath
            element_class: Class to check the presence of
            index: Override to select a specific occurrence of the element
            scroll_options: options to use for scrolling (see scroll_into_view method for examples)

        Returns:
            bool: Class is/is not present on the element
        """
        try:
            ele = cls.__get_desired_elements(element=element, index=index, scroll_options=scroll_options)
            classes = ele.get_attribute('class')
            return classes.split(' ').indexOf(element_class) != -1
        except IndexError:
            return False

    @classmethod
    def is_displayed(cls, element: str, index: int = 0, scroll_options: {} = None):
        """
        Check if an element is displayed on the page

        Args:
            element: CSS selector or XPath
            index: Override to select a specific occurrence of the element
            scroll_options: options to use for scrolling (see scroll_into_view method for examples)

        Returns:
            bool: Element is/is not displayed on the page
        """
        try:
            ele = cls.__get_desired_elements(element=element, index=index, scroll_options=scroll_options)
            return ele.is_displayed()
        except IndexError:
            return False

    @classmethod
    def is_link_displayed(cls, text: str):
        """
        Check if a link is displayed on the page

        Args:
            text: Text used to find the link

        Returns:
            bool: Link is/is not displayed on the page
        """
        try:
            ele = cls.driver.find_element(by=By.PARTIAL_LINK_TEXT, value=text)
            return ele.is_displayed()
        except NoSuchElementException:
            print('Link is not found')
            return False

    @classmethod
    def is_selected(cls, element: str, index: int = 0, scroll_options: {} = None):
        """
        Check if an element is selected

        Args:
            element: CSS selector or XPath
            index: Override to select a specific occurrence of the element
            scroll_options: options to use for scrolling (see scroll_into_view method for examples)

        Returns:
            bool: Element is/is not selected
        """
        ele = cls.__get_desired_elements(element=element, index=index, scroll_options=scroll_options)
        return ele.is_selected()

    @classmethod
    def move_cursor(cls, element: str = None, x_offset: float = None, y_offset: float = None,
                    reset_actions: bool = True):
        """
        Move the cursor to the middle of an element, offset from the top-left corner of an element or an offset from the
         last cursor position.

        Args:
            element: Override to provide a CSS Selector or XPath
            x_offset: Override to provide X offset to move to. Can be positive or negative
            y_offset: Override to provide Y offset to move to. Can be positive or negative
            reset_actions: Override to disable action reset

        Examples:
            >>> move_cursor(element='.my_account')
            Moves the cursor to middle of the element

            >>> move_cursor(element='.my_account', xoffset=10, yoffset=-5)
            Moves the cursor down 10 pixels and 5 pixels to the right from the top left corner of the element

            >>> move_cursor(xoffset=-130, yoffset=20)
            Moves the cursor up 130 pixels and 20 pixels to the left of the current cursor position

        Notes:
            If just an element is provided, cursor will move to middle of the element. If element and offsets are
            provided, offsets are relative to top-left corner of the element. If only offsets are provided, offset will
            be based on last cursor position. If using offsets, X and Y are required. Pixel distance will vary based on
            browser size and screen resolution.

        Returns:
            None
        """
        if element and x_offset:
            ele = cls.__get_desired_elements(element, scroll_to_element=False)
            ActionChains(cls.driver).move_to_element_with_offset(ele, x_offset, y_offset).perform()
        elif element:
            ele = cls.__get_desired_elements(element, scroll_to_element=False)
            ActionChains(cls.driver).move_to_element(ele).perform()
        else:
            ActionChains(cls.driver).move_by_offset(x_offset, y_offset).perform()

        if reset_actions:
            ActionChains(cls.driver).reset_actions()

    @classmethod
    def perform_control_hotkey(cls, key: str):
        """
        Execute Ctrl + KEY hotkey action

        Args:
            key: Specify key to combine with CONTROL

        Examples:
            $ perform_control_hotkey('c') --> Copy
            $ perform_control_hotkey('v') --> Paste

        Returns:
            None
        """
        actions = ActionChains(cls.driver)
        actions.key_down(Keys.CONTROL).send_keys(key.lower())
        actions.key_up(Keys.CONTROL)
        actions.perform()
        actions.reset_actions()

    @classmethod
    def scroll_into_view(cls, element: str, index: int = 0, scroll_options: {} = None):
        """
        Helper method to scroll the element into view

        Args:
            element: CSS selector or XPath
            index: The index of elements to use if more then one is found with the CSS selector or XPath
            scroll_options: Set of dictionary values you can use in order to do the type of scroll you need"
                {
                  "behaviour": "",
                  "block": "",
                  "inline": ""
                }

                behavior - It defines the transition animation. It takes auto or smooth values. Defaults to auto
                block - It defines vertical alignment. It takes start, center, end, or nearest. Defaults to start.
                inline - It defines horizontal alignment. It takes start, center, end, or nearest. Defaults to nearest.

        Examples:
            >>> scroll_into_view(element='.my_account', index=1,
                    scroll_options={behavior: "smooth", block: "center", inline: "nearest"})
            Selects the second instance of element and does smooth transition, horizontally aligns in center and
                vertically sets to nearest.

            >>> scroll_into_view(element='.my_account', scroll_options={block: "center"})
            Selects the first instance of element and does horizontally aligns in center. Other two values use default

        Returns:
            None
        """
        ele = cls.__get_desired_elements(element, scroll_to_element=False, index=index)
        if scroll_options is None:
            cls.driver.execute_script("arguments[0].scrollIntoView();", ele)
        else:
            cls.driver.execute_script("arguments[0].scrollIntoView(" + json.dumps(scroll_options) + ");", ele)

    @classmethod
    def select_dropdown_item(cls, element: str, dropdown_item: str, index: int = 0, timeout: int = BASE_TIMEOUT,
                             scroll_options: {} = None):
        """
        Select an item from a dropdown element

        Args:
            element: CSS selector or XPath
            dropdown_item: Value to select
            index: Override to select a specific occurrence of the element
            timeout: Number of seconds to wait for the element
            scroll_options: options to use for scrolling (see scroll_into_view method for examples)

        Examples:
            >>> select_dropdown_item(element='.states', dropdown_item='Minnesota')
            Selects 'Minnesota' from the 'states' class

        Returns:
            None
        """
        ElementWait.wait_for_element_to_appear(element, timeout, continue_on_timeout=True)
        ele = cls.__get_desired_elements(element=element, index=index, scroll_options=scroll_options)
        Select(ele).select_by_visible_text(dropdown_item)

    @classmethod
    def select_dropdown_item_matching_text(cls, element: str, combinator_element: str, text: str, index: int = 0,
                                           click_dropdown: bool = True, timeout: int = BASE_TIMEOUT,
                                           scroll_options: {} = None):
        """
        Select a dropdown item that matches a specified text value

        Args:
            element: CSS selector or XPath for the dropdown
            combinator_element: CSS selector for the dropdown items with combinator (space, >, +, ~)
                NOTE: Pass empty string for cominator_element when using XPath
            text: Value to select
            index: Override to select a specific occurrence of the element
            click_dropdown: Override to disable clicking the dropdown before selection
            timeout: Number of seconds to wait for the element
            scroll_options: options to use for scrolling (see scroll_into_view method for examples)

        Examples:
            >>> select_dropdown_item_matching_text(element='.states', combinator_element=' option', text='Iowa')
            Clicks the dropdown and searches for a descendant selector with text that matches 'Iowa' and clicks on it.

            >>> select_dropdown_item_matching_text(element='.template-type', combinator_element='+li', text='Barcode',
            click_dropdown=False)
            Does not click the dropdown and searches for an adjacent sibling selector with text that matches 'Barcode'
            and clicks on it.

        Notes:
            To simplify the page file, you can set the selection_element once in your page. For example, if you have a
            state dropdown, you can have two elements: state_dropdown for the dropdown element, like '.states', and
            dropdown_options for the child element with your combinator baked in, like '+li' or ' option'. The method
            will combine these together during execution.

        Raises:
            ValueError: If item isn't found

        Returns:
            None
        """
        if click_dropdown:
            ElementWait.wait_for_element_to_appear(element, timeout, continue_on_timeout=True)
            ele = cls.__get_desired_elements(element=element, index=index, scroll_options=scroll_options)
            ele.click()

        elements = cls.__get_desired_elements(element=f'{element}{combinator_element}', get_all=True)
        for e in elements:
            if e.text == text:
                e.click()
                return
        raise ValueError(f'{text} was not found')

    @classmethod
    def select_item_matching_text(cls, element: str, combinator_element: str, text: str):
        """
        Select an item that matches a specified text value

        Args:
            element: CSS selector or XPath for the parent element
            combinator_element: CSS selector for the child element with combinator (space, >, +, ~)
                NOTE: Pass empty string for cominator_element when using XPath
            text: Value to select

        Examples:
            >>> select_item_matching_text(element='.template-type', combinator_element='+li', text='Barcode')
            Searches for an adjacent sibling selector with text that matches 'Barcode' and clicks on it.

        Notes:
            To simplify the page file, you can set the selection_element once in your page. For example, if you have a
            grid of products, you can have two elements: product_container for each item in the grid, '.prod-tile-wrap'
            and one for the child element with your combinator baked in, ' .prod-label > a'. The method will combine
            these together during execution.

        Raises:
            ValueError: If item isn't found

        Returns:
            None
        """
        elements = cls.__get_desired_elements(element=f'{element}{combinator_element}', get_all=True)
        for e in elements:
            if e.text == text:
                e.click()
                return
        raise ValueError(f'{text} was not found')

    @classmethod
    def is_enabled(cls, element: str, index: int = 0, scroll_options: {} = None):
        """
        Check if an element is enabled on the page

        Args:
            element: CSS selector or XPath
            index: Override to select a specific occurrence of the element
            scroll_options: options to use for scrolling (see scroll_into_view method for examples)

        Returns:
            bool: Element is/is not enabled on the page
        """
        try:
            ele = cls.__get_desired_elements(element=element, index=index, scroll_options=scroll_options)
            return ele.is_enabled()
        except IndexError:
            return False

    @classmethod
    def is_focused(cls, element: str, index: int = 0, scroll_options: {} = None):
        """
        Check if an element is focused on the page

        Args:
            element: CSS selector or XPath
            index: Override to select a specific occurrence of the element
            scroll_options: options to use for scrolling (see scroll_into_view method for examples)

        Returns:
            bool: Element is/is not focused on the page
        """
        try:
            ele = cls.__get_desired_elements(element=element, index=index, scroll_options=scroll_options)
            return ele == cls.driver.switch_to.active_element
        except IndexError:
            return False

    @classmethod
    def drag_and_drop_script_for_html5(cls, initial_element: str, final_element: str):
        """
        Page implements an HTML5 drag and drop which is not supported by the Selenium dragAndDrop action.
        This is to simulate the action by injecting the dragenter, dragover, drop, dragend events with executeScript:
        https://stackoverflow.com/questions/40607833/how-to-simulate-a-drag-and-drop-action-in-protractor-in-angular2

        Args:
            initial_element: CSS selector or XPath of initial element
            final_element: CSS selector or XPath of final element

        Returns:
            The return value of the JavaScript command
        """

        JS_HTML5_DND = "function e(e,t,n,i){" \
                       'var r=a.createEvent("DragEvent");' \
                       "r.initMouseEvent(t,!0,!0,o,0,0,0,c,g,!1,!1,!1,!1,0,null)," \
                       'Object.defineProperty(r,"dataTransfer",{get:function(){return d}}),' \
                       "e.dispatchEvent(r),o.setTimeout(i,n)}" \
                       "var t=arguments[0],n=arguments[1],i=arguments[2]||0,r=arguments[3]||0;" \
                       'if(!t.draggable)throw new Error("Source element is not draggable");' \
                       "var a=t.ownerDocument,o=a.defaultView,l=t.getBoundingClientRect()," \
                       "u=n?n.getBoundingClientRect():l,c=l.left+(l.width>>1),g=l.top+(l.height>>1)," \
                       "s=u.left+(u.width>>1)+i,f=u.top+(u.height>>1)+r," \
                       'd=Object.create(Object.prototype,{_items:{value:{}},effectAllowed:{value:"all",writable:!0},' \
                       'dropEffect:{value:"move",writable:!0},files:{get:function(){return this._items.Files}},' \
                       "types:{get:function(){return Object.keys(this._items)}}," \
                       "setData:{value:function(e,t){this._items[e]=t}}," \
                       "getData:{value:function(e){return this._items[e]}}," \
                       "clearData:{value:function(e){delete this._items[e]}}," \
                       "setDragImage:{value:function(e){}}});" \
                       'if(n=a.elementFromPoint(s,f),!n)throw new Error("Target element is not interactable ' \
                       'and needs to be scrolled into view");' \
                       "u=n.getBoundingClientRect()," \
                       'e(t,"dragstart",101,function(){var i=n.getBoundingClientRect();' \
                       'c=i.left+s-u.left,g=i.top+f-u.top,e(n,"dragenter",1,function()' \
                       '{e(n,"dragover",101,function(){n=a.elementFromPoint(c,g),e(n,"drop",1,function()' \
                       '{e(t,"dragend",1,callback)})})})})'

        element_1 = cls.__get_desired_elements(initial_element, scroll_to_element=False)
        element_2 = cls.__get_desired_elements(final_element, scroll_to_element=False)

        return cls.driver.execute_script(JS_HTML5_DND, element_1, element_2)


class ElementWait(WebdriverManager):
    """Helper utility that waits for certain conditions to be met"""

    @classmethod
    def wait_for_alert_to_appear(cls, timeout: int = BASE_TIMEOUT, continue_on_timeout: bool = False):
        """
        Wait for an alert to appear

        Args:
            timeout: Number of seconds to wait for the element
            continue_on_timeout: Override to prevent failure on timeout

        Returns:
            None
        """
        if continue_on_timeout:
            try:
                WebDriverWait(cls.driver, timeout).until(ec.alert_is_present())
            except TimeoutException:
                print('Alert did not appear')
        else:
            WebDriverWait(cls.driver, timeout).until(ec.alert_is_present())

    @classmethod
    def wait_for_element_to_appear(cls, element: str, timeout: int = BASE_TIMEOUT, continue_on_timeout: bool = False):
        """
        Wait for an element to appear on the page

        Args:
            element: CSS selector or XPath
            timeout: Number of seconds to wait for the element
            continue_on_timeout: Override to prevent failure on timeout

        Returns:
            None
        """
        if element.startswith('/'):
            locator_type = By.XPATH
        else:
            locator_type = By.CSS_SELECTOR

        WebDriverWait(cls.driver, timeout).until(ec.presence_of_element_located((locator_type, element)))

        if continue_on_timeout:
            try:
                WebDriverWait(cls.driver, timeout).until(ec.visibility_of_element_located((locator_type, element)))
            except TimeoutException:
                print(f'{element} did not appear')
        else:
            WebDriverWait(cls.driver, timeout).until(ec.visibility_of_element_located((locator_type, element)))

    @classmethod
    def wait_for_element_to_refresh(cls, element: str, timeout: int = BASE_TIMEOUT, continue_on_timeout: bool = False):
        """
        Wait for an element to become stale and refresh on the page

        Args:
            element: CSS selector or XPath
            timeout: Number of seconds to wait for the element
            continue_on_timeout: Override to prevent failure on timeout

        Returns:
            None
        """
        if element.startswith('/'):
            try:
                WebDriverWait(cls.driver, timeout).until(
                    ec.staleness_of(cls.driver.find_element(by=By.XPATH, value=element)))
            except TimeoutException:
                print(f"Element did not go stale after {timeout} seconds, proceeding without refresh.")
        else:
            try:
                WebDriverWait(cls.driver, timeout).until(
                    ec.staleness_of(cls.driver.find_element(by=By.CSS_SELECTOR, value=element)))
            except TimeoutException:
                print(f"Element did not go stale after {timeout} seconds, proceeding without refresh.")

        cls.wait_for_element_to_appear(element=element, continue_on_timeout=continue_on_timeout)

    @classmethod
    def wait_for_element_to_be_clickable(cls, element: str, timeout: int = BASE_TIMEOUT,
                                         continue_on_timeout: bool = False):
        """
        Wait for an element to be clickable

        Args:
            element: CSS selector or XPath
            timeout: Number of seconds to wait for the element
            continue_on_timeout: Override to prevent failure on timeout

        Returns:
            None
        """
        if element.startswith('/'):
            locator_type = By.XPATH
        else:
            locator_type = By.CSS_SELECTOR

        WebDriverWait(cls.driver, timeout).until(ec.presence_of_element_located((locator_type, element)))

        if continue_on_timeout:
            try:
                WebDriverWait(cls.driver, timeout).until(ec.element_to_be_clickable((locator_type, element)))
            except TimeoutException:
                print(f'{element} is not clickable')
        else:
            WebDriverWait(cls.driver, timeout).until(ec.element_to_be_clickable((locator_type, element)))

    @classmethod
    def wait_for_element_to_disappear(cls, element: str, timeout: int = BASE_TIMEOUT):
        """
        Wait for an element to disappear from the page

        Args:
            element: CSS selector or XPath
            timeout: Number of seconds to wait for the element

        Returns:
            None
        """
        if element.startswith('/'):
            try:
                WebDriverWait(cls.driver, timeout).until(
                    ec.staleness_of(cls.driver.find_element(by=By.XPATH, value=element)))
            except (NoSuchElementException, AttributeError):
                print(element + " Element isn't on page so no waiting")

        else:
            try:
                WebDriverWait(cls.driver, timeout).until(
                    ec.staleness_of(cls.driver.find_element(by=By.CSS_SELECTOR, value=element)))
            except (NoSuchElementException, AttributeError):
                print(element + " Element isn't on page so no waiting")

    @classmethod
    def wait_for_element_to_be_invisible(cls, element: str, timeout: int = BASE_TIMEOUT):
        """
        Wait for an element to not be visible on the page. Useful for situations where an element doesn't become stale
        and remains in the DOM but is no longer visible.

        Args:
            element: CSS selector or XPath
            timeout: Number of seconds to wait for the element

        Returns:
            None
        """
        if element.startswith('/'):
            try:
                WebDriverWait(cls.driver, timeout).until(
                    ec.invisibility_of_element(cls.driver.find_element(by=By.XPATH, value=element)))
            except (NoSuchElementException, AttributeError):
                print(element + " Element isn't on page so no waiting")
        else:
            try:
                WebDriverWait(cls.driver, timeout).until(
                    ec.invisibility_of_element(cls.driver.find_element(by=By.CSS_SELECTOR, value=element)))
            except (NoSuchElementException, AttributeError):
                print(element + " Element isn't on page so no waiting")

    @classmethod
    def wait_for_element_to_have_text(cls, element: str, text: str, timeout: int = BASE_TIMEOUT,
                                      continue_on_timeout: bool = False):
        """
        Wait for specific text to be present on an element

        Args:
            element: CSS selector or XPath
            text: Text to wait for
            timeout: Number of seconds to wait for the element
            continue_on_timeout: Override to prevent failure on timeout

        Returns:
            None
        """
        if element.startswith('/'):
            locator_type = By.XPATH
        else:
            locator_type = By.CSS_SELECTOR

        WebDriverWait(cls.driver, timeout).until(ec.presence_of_element_located((locator_type, element)))

        if continue_on_timeout:
            try:
                WebDriverWait(cls.driver, timeout).until(
                    ec.text_to_be_present_in_element((locator_type, element), text))
            except TimeoutException:
                print(f'{element} does not have {text}')
        else:
            WebDriverWait(cls.driver, timeout).until(ec.text_to_be_present_in_element((locator_type, element), text))

    @classmethod
    def wait_for_element_to_have_text_attribute_value(cls, element: str, text: str, timeout: int = BASE_TIMEOUT,
                                                      continue_on_timeout: bool = False):
        """
        Wait for specific text value to be present on attribute of an element
        Args:
            element: CSS selector or XPath
            text: Text to wait for
            timeout: Number of seconds to wait for the element
            continue_on_timeout: Override to prevent failure on timeout
        Returns:
            None
        """
        if element.startswith('/'):
            locator_type = By.XPATH
        else:
            locator_type = By.CSS_SELECTOR

        WebDriverWait(cls.driver, timeout).until(ec.presence_of_element_located((locator_type, element)))

        if continue_on_timeout:
            try:
                WebDriverWait(cls.driver, timeout).until(
                    ec.text_to_be_present_in_element_value((locator_type, element), text))
            except TimeoutException:
                print(f'{element} does not have {text}')
        else:
            WebDriverWait(cls.driver, timeout).until(
                ec.text_to_be_present_in_element_value((locator_type, element), text))


class BrowserInteractions(WebdriverManager):
    """Helper utility that performs browser commands"""

    @classmethod
    def accept_alert(cls):
        """
        Accept the alert on the page

        Returns:
            None
        """
        cls.driver.switch_to.alert.accept()

    @classmethod
    def get_alert_text(cls):
        """
        Gets the text within an alert and sends it back

        Returns:
            Text of the alert
        """
        return cls.driver.switch_to.alert.text

    @classmethod
    def close_current_window(cls):
        """
        Close the active window

        Returns:
            None
        """
        cls.driver.close()

    @classmethod
    def dismiss_alert(cls):
        """
        Decline the alert on the page

        Returns:
            None
        """
        cls.driver.switch_to.alert.dismiss()

    @classmethod
    def enter_iframe(cls, element: str):
        """
        Switch to a specified iframe

        Args:
            element: CSS selector or XPath

        Returns:
            None
        """
        if element.startswith('/'):
            cls.driver.switch_to.frame(cls.driver.find_element(by=By.XPATH, value=element))
        else:
            cls.driver.switch_to.frame(cls.driver.find_element(by=By.CSS_SELECTOR, value=element))

    @classmethod
    def exit_iframe(cls):
        """
        Exit the current iframe

        Returns:
            None
        """
        cls.driver.switch_to.default_content()

    @classmethod
    def get_all_cookies(cls):
        """
        Get all browser cookies

        Returns:
            list: All browser cookies
        """
        return cls.driver.get_cookies()

    @classmethod
    def get_cookie(cls, name: str):
        """
        Get a specific browser cookie

        Args:
            name: Name of the cookie

        Raises:
            ValueError: If the cookie is not found

        Returns:
            str: The value of the cookie, if found
        """
        cookies = cls.driver.get_cookies()
        for cookie in cookies:
            if cookie['name'] == name:
                return cookie
        raise ValueError(name + " cookie not found")

    @classmethod
    def get_url(cls):
        """
        Get the current URL

        Returns:
            str: Current URL
        """
        return cls.driver.current_url

    @classmethod
    def get_window_handles(cls):
        """
        Get all of the window handles

        Notes:
            Useful when you need the total amount of windows or when switching windows/tabs

        Returns:
            list: Identifiers for each window handle
        """
        return cls.driver.window_handles

    @classmethod
    def go_to_url(cls, url: str):
        """
        Go to a URL

        Args:
            url: Targeted URL

        Returns:
            None
        """
        cls.driver.get(url)

    @classmethod
    def is_alert_displayed(cls, timeout: int = BASE_TIMEOUT):
        """
        Check if an alert is displayed on the page

        Args:
            timeout: Number of seconds to wait for the element

        Returns:
            bool: Alert is/is not displayed
        """
        try:
            WebDriverWait(cls.driver, timeout).until(ec.alert_is_present())
            return True
        except TimeoutException:
            return False

    @classmethod
    def refresh(cls):
        """
        Refresh the page

        Returns:
            None
        """
        cls.driver.refresh()

    @classmethod
    def resize_browser(cls, width: int, height: int):
        """
        Resize the browser to a specified width and height

        Args:
            width: Desired width in pixels
            height: Desired height in pixels

        Examples:
            >>> resize_browser(1280, 720)
            Browser window is resized to 1280x720 pixels

        Returns:
            None
        """
        cls.driver.set_window_size(width, height)

    @classmethod
    def save_screenshot(cls, path: str, name: str, extension: str = 'png'):
        """
        Save a screenshot

        Args:
            path: Path to save the screenshot
            name: Name of the screenshot
            extension: Screenshot extension.
                Options: 'png', 'jpeg'

        Examples:
            >>> save_screenshot('./././', 'test_login_link', 'jpeg')
            Screenshot saved to ./././test_login_link.jpeg

        Raises:
            ValueError: If extension is not 'png' or 'jpeg'

        Returns:
            None
        """
        if extension not in EXTENSION_OPTIONS:
            raise ValueError("Invalid extension type. Expected one of the following: %s" % EXTENSION_OPTIONS)
        else:
            cls.driver.save_screenshot(f'' + path + name + '.' + extension)

    @classmethod
    def switch_to_window(cls, window_index: int):
        """
        Change focus to a different window

        Args:
            window_index: Window to switch to, 0 returns to initial window

        Example:
            >>> switch_to_window(1)
            Change focus to second window

            >>> switch_to_window(0)
            Change focus to initial window

        Returns:
            None
        """
        cls.driver.switch_to.window(cls.driver.window_handles[window_index])

    @classmethod
    def back(cls):
        """
        Go back to previous page

        Returns:
            None
        """
        cls.driver.execute_script("window.history.go(-1)")

    @classmethod
    def forward(cls):
        """
        Go forward to next page

        Returns:
            None
        """
        cls.driver.execute_script("window.history.go(1)")
