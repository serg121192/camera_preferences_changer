import pyautogui

from source.utilities.data_loader import load_data
from source.utilities.logger_setup import setup_logger
from source.user_init.activate_user import activate_user
from source.user_init.create_user import create_user
from source.user_init.open_connection import open_connection
from source.user_init.setup_driver import drivers_setup


logger = setup_logger()


def user_setup(
        ip_addr: str,
        auth: tuple[str, str],
        strong_pass: str
) -> None:
    pyautogui.moveTo(500, 500)
    driver = drivers_setup()
    open_connection(driver, ip_addr)
    path = "./config/configs/user_config.json"
    dataset = load_data(path)

    logger.info(" -> Starting setup a new camera user")
    create_user(driver, dataset, auth)

    logger.info(" -> Activating new user...")
    driver = drivers_setup()
    open_connection(driver, ip_addr)
    activate_user(driver, dataset, strong_pass)
