import requests
from xml.etree import ElementTree as ET
from source.utilities.logger_setup import setup_logger


logger = setup_logger()


def check_success(
        response: requests.Response,
        data: str,
        module: str
) -> bool:
    resp_root = str
    data_root = str

    try:
        resp_root = ET.fromstring(response.text)
        data_root = ET.fromstring(data)
    except ET.ParseError as e:
        logger.error("XML parse error: %s", e)

    if ET.tostring(data_root) in ET.tostring(resp_root):
        logger.error(f"Checker -> {module} setup error: XML data mismatch!")
        return False
    else:
        logger.info(f"Checker -> {module} setup completed: OK!")
        return True
