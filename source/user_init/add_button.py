import pyautogui

from source.user_init.mapping import selector_mapping
from source.user_init.page_element import search_page_element


def find_add_button(driver, data: dict) -> None:
    btn_list_selector = selector_mapping(data["btn_list"])
    _ = search_page_element(driver, btn_list_selector)
    pyautogui.moveTo(380, 280)
    pyautogui.click()
