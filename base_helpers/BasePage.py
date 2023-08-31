from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedTagNameException
from selenium.webdriver.support.events import AbstractEventListener
from selenium.webdriver.remote.webelement import WebElement
from typing import List
import logging


class BasePage(AbstractEventListener):
    def __init__(self, browser):
        self.browser = browser
        self.actions = ActionChains(driver=browser)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel("INFO")
        file_handler = logging.FileHandler(f"autotest_avito/logs/{__name__}.log")
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)

    def open_page(self, url):
        self.logger.info("Opening url: {}".format(url))
        self.browser.get(url)

    def check_element_clickable(self, locator: tuple, timeout: int = 10, raise_error: bool = True):
        self.logger.info(msg=f"Check if element with locator {locator} is clickable")
        try:
            return WebDriverWait(driver=self.browser, timeout=timeout).until(
                method=ec.element_to_be_clickable(mark=locator))
        except TimeoutException:
            if raise_error:
                self.logger.error(msg=f"Assertion Error: Can't find clickable element with locator {locator}")
                raise AssertionError(f"Can't find clickable element with locator {locator}")
            else:
                self.logger.info(msg=f"Timeout {timeout}s has expired while checking if element with locator {locator}"
                                     f" is clickable")
                raise NoSuchElementException

    def check_element_visible(self, locator: tuple, visibility: bool = True, timeout: int = 10,
                               raise_error: bool = True):
        self.logger.info(msg=f"Check if element with locator {locator} has required visibility")
        try:
            if visibility:
                method = ec.visibility_of_element_located
            else:
                method = ec.invisibility_of_element_located
            return WebDriverWait(driver=self.browser, timeout=timeout).until(method=method(locator=locator))
        except TimeoutException:
            state = "visible" if visibility else "absent or invisible"
            if raise_error:
                self.logger.error(msg=f"Assertion Error: Can't find {state} element with locator {locator}")
                raise AssertionError(f"Can't find {state} element with locator {locator}")
            else:
                self.logger.info(msg=f"Timeout {timeout}s has expired while checking if element with locator {locator}"
                                      f" is {state}")
                raise NoSuchElementException

    def click_element(self, locator: tuple, timeout: int = 10):
        element = self.check_element_clickable(locator=locator, timeout=timeout)
        self.actions.move_to_element(to_element=element).click(on_element=element).perform()
        self.logger.info(msg=f"Click element with locator {locator}")
        return element

    def find_elements_visible(self, locator: tuple, timeout: int = 10):
        self.logger.info(msg=f"Find visible elements with locator {locator}")
        try:
            return WebDriverWait(driver=self.browser, timeout=timeout).until(
                method=ec.visibility_of_all_elements_located(locator=locator))
        except TimeoutException:
            self.logger.error(msg=f"Assertion Error: Can't find elements with locator {locator} or some of them"
                                   f" are not visible")
            raise AssertionError(f"Can't find elements with locator {locator} or some of them are not visible")

    def get_element_by_text(self, elements: List[WebElement], text: str, strict_mode: bool = False):
        self.logger.info(msg=f"Get element with text \'{text}\' from given list of WebElements")
        if strict_mode:
            result = list(filter(lambda item: text == item.text, elements))
        else:
            result = list(filter(lambda item: text in item.text, elements))
        if len(result) > 0:
            return result[0]
        else:
            self.logger.error(msg=f"Assertion Error: Can't find element with text \'{text}\' in given list"
                                   f" of WebElements")
            raise AssertionError(f"Can't find element with text \'{text}\' in given list of WebElements")