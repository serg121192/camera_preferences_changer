from pathlib import Path

from source.utilities.camera_processing import camera_process
from source.utilities.logger_setup import setup_logger
from source.utilities.cameras_data import get_cameras_list


logger = setup_logger()
failed_logs = Path("./logs/failed_cams.txt")


def main() -> None:
    cameras = get_cameras_list()
    failed_logs.write_text("", encoding="utf-8")

    camera_process(cameras)
