import os

import allure
import pytest


from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RES_DIR = os.path.join(BASE_DIR, "resources")


static_driver = None


@pytest.fixture()
def driver():
    browser_version = "100"
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=f"https://user1:1234@selenoid.autotests.cloud/wd/hub",
        options=options
    )

    global static_driver
    static_driver = driver

    yield driver

    driver.quit()


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        help="Browser for running tests",
        choices=["firefox", "chrome"],
        default="chrome"
    )
    parser.addoption(
        "--browser_version",
        help="Browser version",
        default="100.0"
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_exception_interact(node, call, report):
    web_driver = None
    for fixture_name in node.fixturenames:
        fixture = node.funcargs[fixture_name]
        if isinstance(fixture, WebDriver):
            web_driver = fixture
            break

    if not web_driver:
       yield

    global static_driver
    attach_video(static_driver)

   # web_driver.get_screenshot_as_file("/home/rattus-aristarchus/code/python/stackoverflow/generic_report/screenshots/on_failure.png")


def attach_video(driver):
    video_url = "https://selenoid.autotests.cloud/video/" + driver.session_id + ".mp4"
    html = "<html><body><video width='100%' height='100%' controls autoplay><source src='" \
           + video_url \
           + "' type='video/mp4'></video></body></html>"
    allure.attach(html, 'video_' + driver.session_id, AttachmentType.HTML, '.html')
