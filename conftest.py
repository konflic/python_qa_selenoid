import pytest
import time

from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--bversion", action="store", default="latest")
    parser.addoption("--vnc", action="store_true", default=False)
    parser.addoption("--logs", action="store_true", default=False)
    parser.addoption("--videos", action="store_true", default=False)
    parser.addoption("--executor", action="store", default="127.0.0.1")


@pytest.fixture
def browser(request):
    browser = request.config.getoption("--browser")
    version = request.config.getoption("--bversion")
    executor = request.config.getoption("--executor")
    vnc = request.config.getoption("--vnc")
    logs = request.config.getoption("--logs")
    videos = request.config.getoption("--videos")
    executor_url = f"http://{executor}:4444/wd/hub"

    options = {}
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        # Передача мобильного User-Agent для хрома
        # options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')

    caps = {
        "browserName": browser,
        "browserVersion": version,
        "selenoid:options": {
            "enableVNC": vnc,
            "enableVideo": videos,
            "enableLog": logs
        }
    }

    driver = webdriver.Remote(
        command_executor=executor_url,
        desired_capabilities=caps
    )
    driver.maximize_window()

    def fin():
        time.sleep(1)
        driver.quit()

    request.addfinalizer(fin)
    return driver
