from time import sleep
import pyautogui

from selenium import webdriver

from source.utilities.logger_setup import setup_logger
from source.user_init.camera_auth import cam_authentication
from source.user_init.mapping import selector_mapping
from source.user_init.page_element import search_page_element
from source.user_init.quit_connection import quit_connection


logger = setup_logger()


def activate_user(
        driver: webdriver.Chrome,
        data: dict,
        strong_password: str
) -> None:
    old_pass_selector = selector_mapping(data["old_pass"])
    strong_pass_selector = selector_mapping(data["strong_pass"])
    pass_confirm_selector = selector_mapping(data["strong_pass_confirm"])
    button_ok = selector_mapping(data["btn_ok"])

    cam_authentication(
        driver,
        (data["username"], data["init_password"]),
        data
    )
    sleep(2)

    pyautogui.moveTo(500, 550)
    old_pass = search_page_element(driver, old_pass_selector)
    old_pass.send_keys(data["init_password"])

    strong_pass = search_page_element(driver, strong_pass_selector)
    strong_pass.send_keys(strong_password)

    strong_pass_confirm = search_page_element(driver, pass_confirm_selector)
    strong_pass_confirm.send_keys(strong_password)

    btn_ok = search_page_element(driver, button_ok)
    btn_ok.click()
    logger.info(" -> User 'stream' has activated successfully!")
    sleep(3)
    quit_connection(driver)
