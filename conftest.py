import pytest
import logging
from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

logging.basicConfig(level=logging.INFO, filename="selenium.log")


class MyListener(AbstractEventListener):

    def on_exception(self, exception, driver):
        driver.save_screenshot("error.png")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--selenoid", action="store", default="localhost")


@pytest.fixture
def browser(request):
    browser = request.config.getoption("--browser")
    selenoid = request.config.getoption("--selenoid")
    fixture_logger = logging.getLogger("fixture")

    executor_url = f"http://{selenoid}:4444/wd/hub"

    caps = {"browserName": browser,
            # "enableVnc": True,
            # "enableVideo": True,
            # "enableLog": True,
            # "screenResolution": "1280x720",
            "name": request.node.name}

    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities=caps)

    driver = EventFiringWebDriver(driver, MyListener())
    fixture_logger.info(f"Start session {driver.session_id}")
    request.addfinalizer(driver.quit)
    return driver
