import pyautogui

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from source.utilities.logger_setup import setup_logger
from source.user_init.camera_auth import cam_authentication
from source.user_init.check_success import check_success
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

    try:
        cam_authentication(
            driver,
            (data["username"], data["init_password"]),
            data
        )

        old_pass = search_page_element(driver, old_pass_selector)
        pyautogui.moveTo(**old_pass.location)
        old_pass.send_keys(data["init_password"])

        strong_pass = search_page_element(driver, strong_pass_selector)
        strong_pass.send_keys(strong_password)

        strong_pass_confirm = search_page_element(driver, pass_confirm_selector)
        strong_pass_confirm.send_keys(strong_password)

        btn_ok = search_page_element(driver, button_ok)
        btn_ok.click()
        WebDriverWait(driver, 25).until(
            lambda drv: drv.find_element(*(By.XPATH, "//div[@class='el-message']"))
        )
        check_success(driver)
        logger.info(" -> User 'stream' has activated successfully!")
        check_success(driver)
    except Exception as e:
        logger.exception("Failed to activate user: %s", e)
        raise
    finally:
        quit_connection(driver)
