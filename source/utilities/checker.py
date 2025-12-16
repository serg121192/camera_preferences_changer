import requests
from xml.etree import ElementTree as ET
from source.utilities.logger_setup import setup_logger


logger = setup_logger()


def check_success(
        cam: str,
        response: requests.Response,
        data: str,
        module: str,
) -> bool:
    resp_root = str
    data_root = str
    ns = {"x": "http://www.hikvision.com/ver20/XMLSchema"}

    try:
        resp_root = ET.fromstring(response.text)
        data_root = ET.fromstring(data)
    except ET.ParseError as e:
        logger.error("XML parse error: %s", e)

    root_channel = resp_root.findall(".//x:channelName", namespaces=ns)
    data_channel = data_root.findall(".//x:channelName", namespaces=ns)

    if data_channel != root_channel:
        logger.error(f"Checker -> {cam} {module} setup error: XML data mismatch!")
        return False
    else:
        logger.info(f"Checker -> {module} setup for {cam} completed: OK!")
        return True
