from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from source.utilities.logger_setup import setup_logger


logger = setup_logger()


def search_page_element(
        driver: webdriver.Chrome,
        locator: tuple[str, str]
) -> WebElement:
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(locator)
        )
        return driver.find_element(*locator)
    except TimeoutException as e:
        logger.error("Element not found: %s", e)
        raise
