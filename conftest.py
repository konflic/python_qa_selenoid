import time

import allure
import pytest
import requests
from selenium import webdriver


# Оперу удалили
# from selenium.webdriver.opera.options import Options

@allure.step("Waiting for availability {url}")
def wait_url_data(url, timeout=10):
    """Метод ожидания доступности урла"""
    while timeout:
        response = requests.get(url)
        if not response.ok:
            time.sleep(1)
            timeout -= 1
        else:
            if 'video' in url:
                return response.content
            else:
                return response.text
    return None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
# https://github.com/pytest-dev/pytest/issues/230#issuecomment-402580536
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.outcome != 'passed':
        item.status = 'failed'
    else:
        item.status = 'passed'


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--executor", action="store", default="192.168.0.108")
    parser.addoption("--mobile", action="store_true")
    parser.addoption("--vnc", action="store_true")
    parser.addoption("--logs", action="store_true")
    parser.addoption("--video", action="store_true")
    parser.addoption("--bv")


@pytest.fixture
def browser(request):
    browser = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    version = request.config.getoption("--bv")
    vnc = request.config.getoption("--vnc")
    logs = request.config.getoption("--logs")
    video = request.config.getoption("--video")
    mobile = request.config.getoption("--mobile")

    if executor == "local":
        caps = {'goog:chromeOptions': {}}

        if mobile:
            caps["goog:chromeOptions"]["mobileEmulation"] = {"deviceName": "iPhone 5/SE"}

        driver = webdriver.Chrome(desired_capabilities=caps)

    else:
        executor_url = f"http://{executor}:4444/wd/hub"

        caps = {
            "browserName": browser,
            # "browserVersion": version,
            # "screenResolution": "1280x720",
            # "name": "Mikhail",
            "selenoid:options": {
                "enableVNC": vnc,
                "enableVideo": video,
                "enableLog": logs
            },
            # 'acceptSslCerts': True,
            # 'acceptInsecureCerts': True,
            # 'timeZone': 'Europe/Moscow',
            # 'goog:chromeOptions': {}
        }

        # Мобильная эмуляция
        # if browser == "chrome" and mobile:
        #     caps["goog:chromeOptions"]["mobileEmulation"] = {"deviceName": "iPhone 5/SE"}

        # options = Options()
        # if browser == "opera":
        #     options.add_experimental_option('w3c', True)

        driver = webdriver.Remote(
            command_executor=executor_url,
            desired_capabilities=caps,
            # options=options
        )

        if not mobile:
            driver.maximize_window()

    def finalizer():
        log_url = f"{executor}/logs/{driver.session_id}.log"
        video_url = f"http://{executor}:8080/video/{driver.session_id}.mp4"
        driver.quit()

        if request.node.status != 'passed':
            if logs:
                allure.attach(
                    name="selenoid_log_" + driver.session_id,
                    body=wait_url_data(log_url),
                    attachment_type=allure.attachment_type.TEXT)
            if video:
                allure.attach(
                    body=wait_url_data(video_url),
                    name="video_for_" + driver.session_id,
                    attachment_type=allure.attachment_type.MP4)

        if video and wait_url_data(video_url):
            requests.delete(url=video_url)

        if logs and wait_url_data(log_url):
            requests.delete(url=log_url)

        # with open("allure-results/environment.xml", "w+") as file:
        #     file.write(f"""<environment>
        #         <parameter>
        #             <key>Browser</key>
        #             <value>{browser}</value>
        #         </parameter>
        #         <parameter>
        #             <key>Browser.Version</key>
        #             <value>{version}</value>
        #         </parameter>
        #         <parameter>
        #             <key>Executor</key>
        #             <value>{executor_url}</value>
        #         </parameter>
        #     </environment>
        #     """)

    request.addfinalizer(finalizer)
    return driver
