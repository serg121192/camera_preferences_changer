from time import sleep
import pyautogui

from selenium import webdriver

from source.utilities.logger_setup import setup_logger
from source.user_init.mapping import selector_mapping
from source.user_init.page_element import search_page_element


logger = setup_logger()


def init_new_user(
        driver: webdriver.Chrome,
        data: dict,
        admin_password: str
) -> None:
    user_login = selector_mapping(data["user_login"])
    admin_pass = selector_mapping(data["admin_pass"])
    init_pass = selector_mapping(data["init_pass"])
    confirm_pass = selector_mapping(data["confirm_pass"])
    btn_ok = selector_mapping(data["btn_ok"])
    checkbox = selector_mapping(data["checkbox"])

    try:
        logger.info("Inserting new user's username...")
        user_login_el = search_page_element(driver, user_login)
        user_login_el.clear()
        user_login_el.send_keys(data["username"])

        logger.info("Inserting admin password...")
        admin_pass_el = search_page_element(driver, admin_pass)
        admin_pass_el.clear()
        admin_pass_el.send_keys(admin_password)

        logger.info("Inserting initial password...")
        pyautogui.moveTo(380, 520)
        init_pass_el = search_page_element(driver, init_pass)
        init_pass_el.clear()
        init_pass_el.send_keys(data["init_password"])

        logger.info("Confirming initial password...")
        confirm_pass_el = search_page_element(driver, confirm_pass)
        confirm_pass_el.clear()
        confirm_pass_el.send_keys(data["init_password"])

        logger.info("Applying 'Send to Center' checkbox...")
        check_box = search_page_element(driver, checkbox)
        check_box.click()

        logger.info("Clicking OK button to finish user creation...")
        btn_ok_el = search_page_element(driver, btn_ok)
        btn_ok_el.click()
        sleep(2)
        logger.info(f"New user '{data['username']}' successfully created!")
    except Exception as e:
        logger.exception("Failed to initialize new user: %s", e)
        raise
