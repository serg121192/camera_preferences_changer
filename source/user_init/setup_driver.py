from selenium import webdriver
from selenium.common import WebDriverException

from source.utilities.logger_setup import setup_logger
from source.user_init.driver_options import set_driver_options


logger = setup_logger()


def drivers_setup() -> webdriver.Chrome:
    try:
        logger.info("Setting Up new driver...")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        driver = webdriver.Chrome(
            options=set_driver_options()
        )
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        return driver
    except WebDriverException as e:
        raise logger.exception("Driver setup error: %s", e)
