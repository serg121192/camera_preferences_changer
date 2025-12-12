import requests
from requests.auth import HTTPDigestAuth
from xml.etree import ElementTree as ET

from source.utilities.logger_setup import setup_logger


logger = setup_logger()


def check_user_exists(
        base_url: str,
        auth: tuple[str, str],
        headers: dict[str, str],
        username: str = "stream"
) -> bool:
    response = requests.get(
        f"{base_url}/ISAPI/Security/users",
        auth=HTTPDigestAuth(*auth),
        headers=headers
    )
    if response.status_code != 200:
        return False
    page_content = ET.fromstring(response.text)
    ns = {"x": "http://www.std-cgi.com/ver20/XMLSchema"}
    for user in page_content.findall(".//x:User", namespaces=ns):
        page_user = user.findtext("x:userName", namespaces=ns)
        if page_user == username:
            logger.info(f" -> User '{page_user}' Found!")
            return True
    return False
