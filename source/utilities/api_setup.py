from dotenv import load_dotenv

from source.utilities.logger_setup import setup_logger
from source.osd_init.osd_setup import setup_osd
from source.ntp_init.ntp_setup import setup_ntp


load_dotenv()
logger = setup_logger()


def run_api_setup(
        cam: str,
        auth: tuple[str, str],
        headers: dict
) -> None:
    octets = cam.split(".")
    channel_name = ".".join(octets[2:])
    server_ip = ".".join(octets[:3]) + ".128"
    base_url = f"http://{cam}"

    logger.info(f" -> Setting up camera {cam}")
    setup_osd(channel_name, auth, base_url, headers, cam)
    setup_ntp(base_url, headers, auth, server_ip, cam)
