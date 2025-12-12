from selenium import webdriver

from source.user_init.add_button import find_add_button
from source.user_init.camera_auth import cam_authentication
from source.user_init.new_user_init import init_new_user
from source.user_init.quit_connection import quit_connection
from source.user_init.search_settings import search_settings
from source.user_init.system_settings import search_system_settings
from source.user_init.user_menu import search_users_menu


def create_user(
        driver: webdriver.Chrome,
        data: dict,
        auth: tuple[str, str]
) -> None:
    cam_authentication(driver, auth, data)
    search_settings(driver, data)
    search_system_settings(driver, data)
    search_users_menu(driver, data)
    find_add_button(driver, data)
    init_new_user(driver, data, auth[1])
    quit_connection(driver)
