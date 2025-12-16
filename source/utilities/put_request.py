import requests
from requests.auth import HTTPDigestAuth

from source.utilities.logger_setup import setup_logger


logger = setup_logger()


def make_put(
        url: str,
        headers: dict[str, str],
        data: str,
        auth: tuple[str, str],
) -> None:
    _ = requests.put(
        url,
        headers=headers,
        data=data,
        auth=HTTPDigestAuth(*auth),
        timeout=(2.5, 2)
    )
