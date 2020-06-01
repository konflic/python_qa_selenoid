from page_objects.HabrObject import HabrObject


def test_post_open(browser):
    page = HabrObject(browser) \
        .open() \
        .click_search() \
        .search('Python')
    page.filter_by_rating()
    page.read_more()
    page.is_present(page.POST_BODY)


def test_hubs_open(browser):
    page = HabrObject(browser) \
        .open() \
        .click_search() \
        .search('Python')
    page.select_hubs_and_companies()
    page.is_present(page.HUBS)


def test_post_open_2(browser):
    page = HabrObject(browser) \
        .open() \
        .click_search() \
        .search('Python')
    page.filter_by_rating()
    page.read_more()
    page.is_present(page.POST_BODY)


def test_hubs_open_2(browser):
    page = HabrObject(browser) \
        .open() \
        .click_search() \
        .search('Python')
    page.select_hubs_and_companies()
    page.is_present(page.HUBS)
