import pyautogui as pag

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from source.utilities.logger_setup import setup_logger
from source.user_init.check_success import check_success
from source.user_init.mapping import selector_mapping
from source.user_init.page_element import search_page_element
from source.user_init.quit_connection import quit_connection


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
        admin_coords = admin_pass_el.location
        admin_pass_el.send_keys(admin_password)

        logger.info("Inserting initial password...")
        pag.moveTo(
            admin_coords["x"] + 150,
            admin_coords["y"] + 230
        )
        pag.click()
        init_pass_el = search_page_element(driver, init_pass)
        try:
            init_pass_el.clear()
            init_pass_el.send_keys(data["init_password"])
        except TimeoutError:
            pag.typewrite(data["init_password"], interval=0.02)

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
        WebDriverWait(driver, 15).until(
            lambda drv: drv.find_element(
                *(By.XPATH, "//div[@class='el-message']")
            )
        )
        check_success(driver)
        logger.info(f"New user '{data['username']}' successfully created!")
        quit_connection(driver)
    except Exception as e:
        logger.error("Failed to initialize new user: %s", e)
        quit_connection(driver)
