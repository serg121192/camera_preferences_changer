import os
import socket
from pathlib import Path

from dotenv import load_dotenv
from requests import (
    ConnectTimeout,
    ReadTimeout,
    RequestException
)

from source.utilities.logger_setup import setup_logger
from source.osd_init.osd_setup import setup_osd
from source.ntp_init.ntp_setup import setup_ntp
from source.user_init.user_existency import check_user_exists
from source.user_init.user_setup import user_setup


logger = setup_logger()

load_dotenv()
AUTH = (os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD"))
USER_STRONG_PASS = os.getenv("USER_STRONG_PASS")
HEADERS = {"Content-Type": "application/xml; charset=utf-8"}
failed_logs = Path("./logs/failed_cams.txt")


def get_cameras_dict() -> list:
    try:
        with open("./config/cameras.txt", "r", encoding="utf-8") as cameras:
            return list(cameras.readlines())
    except FileNotFoundError as e:
        logger.error("Cameras config file error: %s", e)
        raise


def is_reachable(
        ip_addr: str,
        port: int = 80,
        timeout: float = 2.5
) -> bool:
    try:
        with socket.create_connection((ip_addr, port), timeout):
            return True
    except OSError:
        return False


def main() -> None:
    cameras = get_cameras_dict()
    failed_logs.write_text("", encoding="utf-8")
    with failed_logs.open("a", encoding="utf-8") as failed:
        for cam in cameras:
            cam = cam.strip()
            if not is_reachable(cam):
                failed.write(f"Camera offline -> {cam}\n")
            else:
                logger.info(
                    f" \n{"-" * 40} Setting up camera: {cam} {"-" * 40} "
                )
                try:
                    logger.info(f" -> Setting up OSD for current camera")
                    octets = cam.split(".")
                    channel_name = ".".join(octets[2:])
                    base_url = f"http://{cam}"
                    flag_osd = setup_osd(
                        channel_name,
                        AUTH,
                        base_url,
                        HEADERS
                    )
                    if flag_osd:
                        logger.info(f" -> OSD for {cam} successfully set up!")
                    else:
                        failed.write(f" -> OSD for {cam} not set up\n")

                    logger.info(f" -> Setting up NTP for current camera")
                    server_ip = ".".join(octets[:3]) + ".128"
                    flag_ntp = setup_ntp(base_url, HEADERS, AUTH, server_ip)
                    if flag_ntp:
                        logger.info(f" -> NTP for {cam} successfully set up!")
                    else:
                        failed.write(f" -> NTP for {cam} not set up\n")

                    if check_user_exists(base_url, AUTH, HEADERS):
                        logger.info(
                            f" -> User 'stream' for {cam} already set up!"
                        )
                    else:
                        logger.info(f" -> User 'stream' for {cam} not found!")
                        logger.info(f" -> Deploying a new user to camera")
                        user_setup(base_url, AUTH, USER_STRONG_PASS)
                        if check_user_exists(base_url, AUTH, HEADERS):
                            logger.info(
                                f" -> User 'stream' for "
                                f"{cam} was set up successfully!"
                            )
                        else:
                            logger.info(
                                f" -> User 'stream' for {cam} not found!"
                            )
                            failed.write(
                                f" -> User 'stream' for "
                                f"{cam} still not set up!!!\n"
                            )

                except (ConnectTimeout, ReadTimeout) as e:
                    logger.error(f"{cam} connection timeout: {e}")
                    continue
                except RequestException as e:
                    logger.error(f"{cam} request error: {e}")
                    continue
