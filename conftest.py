import os
import random
import time

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--executor", action="store", default="192.168.170.47")
    parser.addoption("--mobile", action="store_true")
    parser.addoption("--vnc", action="store_true")
    parser.addoption("--logs", action="store_true")
    parser.addoption("--video", action="store_true")
    parser.addoption("--bv")


@pytest.fixture
def browser(request):
    browser = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    # vnc = request.config.getoption("--vnc")
    # version = request.config.getoption("--bv")
    # logs = request.config.getoption("--logs")
    # video = request.config.getoption("--video")
    mobile = request.config.getoption("--mobile")

    if browser == "chrome":
        options = ChromeOptions()
        # if mobile:
        #     mobile_emulation = { "deviceName": "iPhone XR" }
        #     options.add_experimental_option("mobileEmulation", mobile_emulation)
    elif browser == "firefox":
        options = FirefoxOptions()

    caps = {
        "browserName": browser,
        # "browserVersion": version,
        "selenoid:options": {
            "enableVNC": True,
            # "name": request.node.name,
            # "screenResolution": "1280x2000",
            # "enableVideo": video,
            # "enableLog": logs,
            # "timeZone": "Europe/Moscow",
            # "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru:en", "LC_ALL=ru_RU.UTF-8"]
        },
        "acceptInsecureCerts": True,
    }

    for k, v in caps.items():
        options.set_capability(k, v)

    driver = webdriver.Remote(
        command_executor=f"http://{executor}:4444/wd/hub",
        options=options
    )

    if not mobile:
        driver.maximize_window()

    def finalizer():
        driver.quit()

    request.addfinalizer(finalizer)
    return driver
