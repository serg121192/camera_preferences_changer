from selenium import webdriver

from source.utilities.logger_setup import setup_logger
from source.user_init.mapping import selector_mapping
from source.user_init.page_element import search_page_element


logger = setup_logger()


def search_settings(driver: webdriver.Chrome, data: dict) -> None:
    logger.info("Searching for 'Settings' button...")
    settings_button = selector_mapping(data["settings_button"])
    settings_btn = search_page_element(driver, settings_button)
    settings_btn.click()
