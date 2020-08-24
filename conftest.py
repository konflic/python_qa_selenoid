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
    parser.addoption("--selenoid", action="store", default="127.0.0.1")


@pytest.fixture
def browser(request):
    browser = request.config.getoption("--browser")
    selenoid = request.config.getoption("--selenoid")
    fixture_logger = logging.getLogger("fixture")

    executor_url = f"http://{selenoid}:4444/wd/hub"

    options = webdriver.ChromeOptions()
    # Передача мобильного User-Agent для хрома
    # options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')

    caps = {"browserName": browser,
            "enableVnc": True,
            "enableVideo": True,
            # "enableLog": True,
            # "screenResolution": "1280x720",
            "name": request.node.name}

    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities=caps, options=options)

    driver = EventFiringWebDriver(driver, MyListener())
    fixture_logger.info(f"Start session {driver.session_id}")
    request.addfinalizer(driver.quit)
    return driver
