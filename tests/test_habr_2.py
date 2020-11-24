import pytest

from page_objects import Habr


@pytest.mark.parametrize("query", ["Python", "Swift"])
def test_post_open1(browser, query):
    page = Habr(browser) \
        .open() \
        .click_search() \
        .search(query)
    page.filter_by_rating()
    page.read_more()
    page.is_present(page.POST_BODY)


def test_hubs_open1(browser):
    page = Habr(browser) \
        .open() \
        .click_search() \
        .search('Dart')
    page.select_hubs_and_companies()
    page.is_present(page.HUBS)


def test_hubs_open_21(browser):
    page = Habr(browser) \
        .open() \
        .click_search() \
        .search('Java')
    page.select_hubs_and_companies()
    page.is_present(page.HUBS)
