import os
from pathlib import Path
from requests import (
    ConnectTimeout,
    ReadTimeout,
    RequestException
)
from dotenv import load_dotenv

from source.utilities.logger_setup import setup_logger
from source.utilities.camera_activity import is_reachable
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


def camera_process(cam: str) -> None:
    with failed_logs.open("a", encoding="utf-8") as failed:
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
                failed.write(f"{cam} connection error: camera not set up\n")
                return
            except RequestException as e:
                logger.error(f"{cam} request error: {e}")
                failed.write(f"{cam} request error: camera request error\n")
                return
            except Exception as e:
                logger.error(f"{cam} Other error occurred: {e}")
                failed.write(f"{cam} Other error occurred: camera not set up\n")
                return
