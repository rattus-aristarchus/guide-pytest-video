import logging
import os
import allure
import pytest


from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RES_DIR = os.path.join(BASE_DIR, "resources")

SELENOID_URL = "https://your.selenoid.URL"

@pytest.fixture()
def driver():
    """
    The fixture that our tests call to get access to a driver.
    """

    # This is needed to tell selenoid that we want it to
    # record videos
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "125",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }

    options = Options()
    options.capabilities.update(selenoid_capabilities)

    # Here, we create a driver that is going to use selenoid instead of
    # a local browser
    driver = webdriver.Remote(
        command_executor=f"{SELENOID_URL}/wd/hub",
        options=options
    )

  #  driver = webdriver.Chrome()

    yield driver

    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_exception_interact(node, call, report):
    web_driver = None
    for fixture_name in node.fixturenames:
        if fixture_name in node.funcargs.keys():
            fixture = node.funcargs[fixture_name]
            if isinstance(fixture, webdriver.Remote):
                web_driver = fixture
                break

    if web_driver:
        attach_video(web_driver)

    yield


def attach_video(driver):
    video_url = f"{SELENOID_URL}/video/" + driver.session_id + ".mp4"
    html = "<html><body><video width='100%' height='100%' controls autoplay><source src='" \
           + video_url \
           + "' type='video/mp4'></video></body></html>"
    allure.attach(html, 'video_' + driver.session_id, AttachmentType.HTML, '.html')
