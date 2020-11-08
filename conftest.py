import pytest
import logging
from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

logging.basicConfig(level=logging.INFO, filename="results/selenium.log")


class MyListener(AbstractEventListener):

    def on_exception(self, exception, driver):
        driver.save_screenshot("results/error.png")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--browser_version", action="store", default="")
    parser.addoption("--executor", action="store", default="127.0.0.1")


@pytest.fixture
def browser(request):
    browser = request.config.getoption("--browser")
    version = request.config.getoption("--browser_version")
    executor = request.config.getoption("--executor")

    fixture_logger = logging.getLogger("fixture")

    executor_url = f"http://{executor}:4444/wd/hub"

    options = {}
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        # Передача мобильного User-Agent для хрома
        # options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')

    caps = {
        "browserName": "chrome",
        "browserVersion": "50.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": False
        }
    }

    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities=caps)
    driver.maximize_window()

    driver = EventFiringWebDriver(driver, MyListener())
    fixture_logger.info(f"Start session {driver.session_id}")

    request.addfinalizer(driver.quit)
    return driver
