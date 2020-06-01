import time
from page_objects import Habr


def test_post_open(browser):
    page = Habr(browser) \
        .open() \
        .click_search() \
        .search('Swift')
    page.filter_by_rating()
    page.read_more()
    page.is_present(page.POST_BODY)
    time.sleep(2)


def test_hubs_open(browser):
    page = Habr(browser) \
        .open() \
        .click_search() \
        .search('Dart')
    page.select_hubs_and_companies()
    page.is_present(page.HUBS)
    time.sleep(2)


def test_post_open_2(browser):
    page = Habr(browser) \
        .open() \
        .click_search() \
        .search('Python')
    page.filter_by_rating()
    page.read_more()
    page.is_present(page.POST_BODY)
    time.sleep(2)


def test_hubs_open_2(browser):
    page = Habr(browser) \
        .open() \
        .click_search() \
        .search('Java')
    page.select_hubs_and_companies()
    page.is_present(page.HUBS)
    time.sleep(2)
