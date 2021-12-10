

def test_open_local_url(browser):
    browser.get("http://192.168.1.88:8081/")
    assert browser.title == "Your Store"
