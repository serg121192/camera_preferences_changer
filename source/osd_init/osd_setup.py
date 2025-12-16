import requests
from requests.auth import HTTPDigestAuth
from requests.exceptions import RequestException

from source.utilities.data_loader import load_data
from source.utilities.logger_setup import setup_logger
from source.utilities.template_renderer import render_template
from source.utilities.put_request import make_put
from source.utilities.checker import check_success


logger = setup_logger()


def setup_osd(
        channel_name: str,
        auth: tuple[str, str],
        base_url: str,
        headers: dict[str, str],
        cam: str
) -> None:
    path = "./config/configs/osd_config.json"
    osd_conf = load_data(path)

    logger.info(f" -> Setting up OSD for {cam}")

    xml_data = render_template(
        "osd_xml_schema.xml.j2",
        DATE_X=osd_conf["DATE_X"],
        DATE_Y=osd_conf["DATE_Y"],
        DATE_FORMAT=osd_conf["DATE_FORMAT"],
        CHANNEL_X=osd_conf["CHANNEL_X"],
        CHANNEL_Y=osd_conf["CHANNEL_Y"],
        CHANNEL_NAME=channel_name
    )

    channel_data = render_template(
        "osd_channel_name_schema.xml.j2",
        CHANNEL_ID=osd_conf["CHANNEL_ID"],
        CHANNEL_NAME=channel_name
    )

    try:
        make_put(
            f"{base_url}{osd_conf['URL']}",
            headers=headers,
            data=xml_data,
            auth=auth,
        )

        make_put(
            f"{base_url}{osd_conf['channel_url']}",
            headers=headers,
            data=channel_data,
            auth=auth,
        )

        check_success(
            cam,
            requests.get(
                f"{base_url}{osd_conf['URL']}",
                headers=headers,
                auth=HTTPDigestAuth(*auth),
                timeout=(.5, 2)
            ),
            data=xml_data,
            module="OSD",
        )
    except RequestException as e:
        logger.error("OSD setup error: %s", e)
        raise
