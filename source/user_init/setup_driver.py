import pygetwindow as gw
from time import sleep
from selenium import webdriver
from selenium.common import WebDriverException

from source.utilities.logger_setup import setup_logger
from source.user_init.driver_options import set_driver_options


logger = setup_logger()


def drivers_setup() -> webdriver.Chrome:
    try:
        logger.info("Setting Up new driver...")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        driver = webdriver.Chrome(
            options=set_driver_options()
        )
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd(
            "Network.setBlockedURLs",
            {"urls": ["*rtsp*", "*stream*", "*.m3u8", "*.ts"]}
        )
        try:
            driver.set_window_position(0, 0)
            driver.set_window_size(1280, 900)
        except WebDriverException:
            pass

        wins = [w for w in gw.getAllTitles() if 'Chrome' in w]
        if wins:
            gw.getWindowsWithTitle(wins[0])[0].activate()
            sleep(0.2)
        return driver
    except WebDriverException as e:
        raise logger.exception("Driver setup error: %s", e)
