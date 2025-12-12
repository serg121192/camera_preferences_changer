from selenium import webdriver

from source.utilities.logger_setup import setup_logger


logger = setup_logger()


def quit_connection(driver: webdriver.Chrome) -> None:
    logger.info("Closing connection...")
    driver.quit()
