import pytest

from page_objects.HabrObject import HabrObject


@pytest.mark.parametrize("query", ["Python", "Swift"])
def test_post_open(browser, query):
    page = HabrObject(browser)
    page.open("https://habr.com/en")
    page.click_search()
    page.search(query)
    page.read_more()
    page.is_present(page.POST_BODY)


@pytest.mark.parametrize("query", ["Dart", "Java"])
def test_hubs_open(browser, query):
    page = HabrObject(browser)
    page.open("https://habr.com/en")
    page.click_search()
    page.search(query)
    page.select_hubs()
    page.is_present(page.HUBS)
