import os
from pathlib import Path
from requests import (
    ConnectTimeout,
    ReadTimeout,
    RequestException
)
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

from source.utilities.logger_setup import setup_logger
from source.utilities.camera_activity import is_reachable
from source.utilities.api_setup import run_api_setup
from source.user_init.user_existency import check_user_exists
from source.user_init.user_setup import user_setup


logger = setup_logger()
load_dotenv()
AUTH = (os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD"))
USER_STRONG_PASS = os.getenv("USER_STRONG_PASS")
HEADERS = {"Content-Type": "application/xml; charset=utf-8"}
failed_logs = Path("./logs/failed_cams.txt")


def camera_process(cameras: list) -> None:
    with failed_logs.open("a", encoding="utf-8") as failed:
        online_cams = []
        for cam in cameras:
            if not is_reachable(cam.strip()):
                failed.write(f"Camera offline -> {cam}\n")
            else:
                online_cams.append(cam.strip())
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [
                executor.submit(
                    run_api_setup,
                    cam,
                    AUTH,
                    HEADERS
                )
                for cam in online_cams
            ]

            for future in as_completed(futures):
                future.result()

        for cam in online_cams:
            base_url = f"http://{cam}"
            try:
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
