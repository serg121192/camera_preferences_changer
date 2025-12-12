from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.keys import Keys

from source.utilities.logger_setup import setup_logger
from source.user_init.mapping import selector_mapping
from source.user_init.page_element import search_page_element


logger = setup_logger()


def cam_authentication(
        driver: webdriver.Chrome,
        auth: tuple[str, str],
        data: dict,
) -> None:
    login = auth[0]
    password = auth[1]
    login_selector = selector_mapping(data["login_creds"])
    password_selector = selector_mapping(data["pass_creds"])

    try:
        login_el = search_page_element(driver, login_selector)
        login_el.clear()
        login_el.send_keys(login)

        password_el = search_page_element(driver, password_selector)
        password_el.clear()
        password_el.send_keys(password + Keys.ENTER)

        logger.info("Authentication successful!")
    except TimeoutException as e:
        logger.exception("Authentication error: %s", e)
        raise
