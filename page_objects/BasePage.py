import selenium
import allure

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:

    def __init__(self, driver, wait=3):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait)
        self.actions = ActionChains(driver)

    def __wait_element(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except selenium.common.exceptions.TimeoutException:
            allure.attach(
                name="screenshot",
                body=self.driver.get_screenshot_as_png()
            )
            raise AssertionError(f"Element {locator} not found.")

    @allure.step
    def open(self, url):
        self.driver.get(url)

    @allure.step
    def click(self, locator):
        self.__wait_element(locator).click()

    @allure.step
    def input_and_submit(self, locator, value):
        find_field = self.__wait_element(locator)
        find_field.click()
        find_field.clear()
        find_field.send_keys(value)
        find_field.send_keys(Keys.ENTER)

    @allure.step
    def is_present(self, locator):
        self.__wait_element(locator)
