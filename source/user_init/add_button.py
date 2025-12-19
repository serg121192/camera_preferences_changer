import pyautogui as pag
from time import sleep

from source.user_init.mapping import selector_mapping
from source.user_init.page_element import search_page_element


pag.PAUSE = 0.2


def find_add_button(driver, data: dict) -> None:
    btn_list = selector_mapping(data["btn_list"])
    add_button = search_page_element(driver, btn_list)
    coords = add_button.location
    pag.moveTo(coords["x"] + 80, coords["y"] + 155, duration=0.05)
    sleep(.02)
    pag.moveRel(10, 0, duration=0.05)

    if coords:
        pag.click()
