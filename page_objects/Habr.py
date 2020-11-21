from page_objects.BasePage import BasePage
from selenium.webdriver.common.by import By


class Habr(BasePage):
    URL = "https://habr.com/"
    SEARCH_BTN = (By.CSS_SELECTOR, "#search-form-btn")
    SEARCH_FILED = (By.CSS_SELECTOR, "#search-form-field")
    READ_MORE = (By.PARTIAL_LINK_TEXT, "Read more")
    FILTER_BY_RATING = (By.CSS_SELECTOR, '.tabs__level.tabs__level_bottom li:nth-child(3)')
    POST_BODY = (By.CSS_SELECTOR, ".post__body")
    TAB_HUBS_AND_COMPANIES = (By.XPATH, "//h3[contains(text(), 'Hubs')]")
    HUBS = (By.ID, "hubs")

    def open(self):
        return self._open(self.URL)

    def search(self, request):
        return self.input_and_submit(self.SEARCH_FILED, request)

    def filter_by_rating(self):
        self.click(self.FILTER_BY_RATING)

    def read_more(self):
        self.click(self.READ_MORE)

    def click_search(self):
        return self.click(self.SEARCH_BTN)

    def select_hubs_and_companies(self):
        self.click(self.TAB_HUBS_AND_COMPANIES)
