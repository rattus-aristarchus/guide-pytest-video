import allure
from allure_commons.types import Severity
from selenium.webdriver.common.by import By
from test import conftest


@allure.severity(severity_level=Severity.CRITICAL)
@allure.label("owner", 'lankinma')
@allure.feature("Software testing wiki page")
@allure.title("Page should have a word in the title")
def test_main_page_title_should_have_word_in_title(driver):
    with allure.step("Open the main page"):
        driver.get("https://en.wikipedia.org/wiki/Software_testing")

    with allure.step("Look for a phrase in the title"):
        conftest.attach_video(conftest.static_driver)
        assert "Software testing" in driver.title


@allure.severity(severity_level=Severity.CRITICAL)
@allure.label("owner", 'lankinma')
@allure.feature("Software testing wiki page")
@allure.title("Page should have a text entry element")
def test_main_page_should_have_text_entry(driver):
    with allure.step("Open the main page"):
        driver.get("https://en.wikipedia.org/wiki/Software_testing")

    with allure.step("Find an element on the page"):
        elem = driver.find_element(By.ID, "searchInput")
        assert elem is not None
