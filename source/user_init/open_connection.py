from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from source.utilities.logger_setup import setup_logger


logger = setup_logger()


def open_connection(driver: webdriver.Chrome, ip_addr: str) -> None:
    try:
        driver.get(ip_addr + "/doc/index.html#/portal/login")
        WebDriverWait(driver, 10).until(
            lambda drv:
            drv.current_url.startswith(ip_addr)
        )
        logger.info("Connection established successfully!")
    except TimeoutException:
        raise logger.exception(
            "Connection timeout. Check your network connection or URL."
        )
