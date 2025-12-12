import os
import logging
from logging.handlers import RotatingFileHandler


def setup_logger() -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    open("./logs/cam.log", "w").close()

    logger = logging.getLogger("cam")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    fh = RotatingFileHandler(
        "./logs/cam.log",
        maxBytes=2_000_000,
        backupCount=3,
        encoding="utf-8"
    )
    fmt = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s")
    sh = logging.StreamHandler()

    sh.setFormatter(fmt)
    fh.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger
