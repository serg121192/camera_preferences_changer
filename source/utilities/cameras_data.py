from source.utilities.logger_setup import setup_logger


logger = setup_logger()


def get_cameras_dict() -> list:
    try:
        with open("./config/cameras.txt", "r", encoding="utf-8") as cameras:
            return list(cameras.readlines())
    except FileNotFoundError as e:
        logger.error("Cameras config file error: %s", e)
        raise
