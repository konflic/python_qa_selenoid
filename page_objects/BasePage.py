import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC


class BasePage:

    def __init__(self, driver, wait=3):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait)
        self.logger = logging.getLogger(type(self).__name__)

    def _open(self, url):
        self.logger.info("Opening url: {}".format(url))
        self.driver.get(url)
        return self

    def click(self, locator):
        self.logger.info("Clicking element: {}".format(locator))
        try:
            self.wait.until(EC.visibility_of_element_located(locator)).click()
            return self
        except TimeoutException:
            self.logger.exception("Element {} not found on page".format(locator))
            raise TimeoutException

    def input_and_submit(self, locator, value):
        self.logger.info("Input {} in input {}".format(value, locator))
        find_field = self.driver.find_element(*locator)
        find_field.send_keys(value)
        find_field.send_keys(Keys.ENTER)
        return self

    def is_present(self, locator):
        self.logger.info("Check if element {} is present".format(locator))
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            self.logger.exception("Element {} not found on page".format(locator))
            raise TimeoutException
