from selenium import webdriver

from source.utilities.logger_setup import setup_logger
from source.user_init.mapping import selector_mapping
from source.user_init.page_element import search_page_element


logger = setup_logger()


def search_users_menu(driver: webdriver.Chrome, data: dict) -> None:
    logger.info("Searching for 'Users' menu...")
    users_menu = selector_mapping(data["users_menu"])
    users_btn = search_page_element(driver, users_menu)
    users_btn.click()
