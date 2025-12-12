import json

from source.utilities.logger_setup import setup_logger


logger = setup_logger()


def load_data(path: str) -> dict[str, str]:
    try:
        with open(path, "r", encoding="utf-8") as config:
            return json.load(config)
    except FileNotFoundError as e:
        logger.error("Config file error: %s", e)
        raise
