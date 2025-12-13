from threading import Lock
from pathlib import Path


failed_lock = Lock()
failed_log = Path("./logs/failed_log.txt")


def get_loch(message: str) -> None:
    with failed_lock:
        with failed_log.open("a", encoding="utf-8") as failed:
            failed.write(message + "\n")
