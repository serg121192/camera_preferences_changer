from selenium import webdriver

from source.utilities.logger_setup import setup_logger
from source.user_init.mapping import selector_mapping
from source.user_init.page_element import search_page_element


logger = setup_logger()


def search_system_settings(driver: webdriver.Chrome, data: dict) -> None:
    logger.info("Searching for 'System Settings' button...")
    system_button = selector_mapping(data["system_button"])
    system_settings_btn = search_page_element(driver, system_button)
    system_settings_btn.click()
