from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from source.utilities.camera_processing import camera_process
from source.utilities.logger_setup import setup_logger
from source.utilities.cameras_data import get_cameras_dict


logger = setup_logger()
failed_logs = Path("./logs/failed_cams.txt")


def main() -> None:
    cameras = get_cameras_dict()
    failed_logs.write_text("", encoding="utf-8")

    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = [
            executor.submit(camera_process, cam.strip())
            for cam in cameras
        ]

        for future in as_completed(futures):
            future.result()
