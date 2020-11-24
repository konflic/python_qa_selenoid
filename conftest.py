import pytest
import time

from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--bversion", action="store", required=True)
    parser.addoption("--vnc", action="store_true", default=False)
    parser.addoption("--logs", action="store_true", default=False)
    parser.addoption("--videos", action="store_true", default=False)
    parser.addoption("--executor", action="store", default="localhost")
    parser.addoption("--mobile", action="store_true")


@pytest.fixture
def browser(request):
    browser = request.config.getoption("--browser")
    version = request.config.getoption("--bversion")
    executor = request.config.getoption("--executor")
    vnc = request.config.getoption("--vnc")
    logs = request.config.getoption("--logs")
    videos = request.config.getoption("--videos")
    executor_url = f"http://{executor}:4444/wd/hub"
    mobile = request.config.getoption("--mobile")

    caps = {
        "browserName": browser,
        "browserVersion": version,
        "screenResolution": "1280x720",
        "name": "Mikhail.C",
        "selenoid:options": {
            "enableVNC": vnc,
            "enableVideo": videos,
            "enableLog": logs,
        },
        'acceptSslCerts': True,
        'acceptInsecureCerts': True,
        'timeZone': 'Europe/Moscow',
        'goog:chromeOptions': {
            'args': []
        }
    }

    if browser == "chrome" and mobile:
        caps["goog:chromeOptions"]["mobileEmulation"] = {"deviceName": "iPhone 5/SE"}

    driver = webdriver.Remote(
        command_executor=executor_url,
        desired_capabilities=caps
    )

    if not mobile:
        driver.maximize_window()

    def fin():
        time.sleep(1)
        driver.quit()

    request.addfinalizer(fin)
    return driver
