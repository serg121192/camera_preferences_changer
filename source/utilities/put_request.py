import requests
from requests.auth import HTTPDigestAuth

from source.utilities.logger_setup import setup_logger


logger = setup_logger()


def make_put(
        url: str,
        headers: dict[str, str],
        data: str,
        auth: tuple[str, str],
        log_description: str
) -> None:
    response = requests.put(
        url,
        headers=headers,
        data=data,
        auth=HTTPDigestAuth(*auth),
        timeout=(2.5, 2)
    )

    if response.status_code in [200, 201]:
        logger.info(
            "%s %s OK",
            log_description,
            response.status_code
        )
    else:
        logger.error(
            "%s ERROR: %s",
            log_description,
            response.status_code
        )
