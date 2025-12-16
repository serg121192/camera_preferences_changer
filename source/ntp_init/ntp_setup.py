from datetime import datetime

from requests.exceptions import RequestException

from source.utilities.data_loader import load_data
from source.utilities.logger_setup import setup_logger
from source.utilities.template_renderer import render_template
from source.utilities.put_request import make_put


logger = setup_logger()


def setup_ntp(
        base_url: str,
        headers: dict[str, str],
        auth: tuple[str, str],
        server_ip: str,
        cam: str
) -> bool:
    path = "./config/configs/ntp_config.json"
    ntp_conf = load_data(path)

    logger.info(f" -> Setting up NTP for {cam}")

    xml_data = render_template(
        "ntp_server_sync.xml.j2",
        ID=ntp_conf["id"],
        NTP_FORMAT=ntp_conf["ntp_format"],
        SERVER_IP=server_ip,
        NTP_PORT=ntp_conf["ntp_port"],
        NTP_INTERVAL=ntp_conf["ntp_interval"]
    )

    time_data = render_template(
        "ntp_time_schema.xml.j2",
        TIME_MODE=ntp_conf["time_mode"],
        CURRENT_DATETIME=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        TIMEZONE_OFFSET=ntp_conf["timezone_offset"],
        TIME_OFFSET=ntp_conf["time_offset"],
        S_MONTH=ntp_conf["summertime_month"],
        S_WEEK=ntp_conf["summertime_week"],
        S_HOUR=ntp_conf["summertime_hour"],
        W_MONTH=ntp_conf["wintertime_month"],
        W_WEEK=ntp_conf["wintertime_week"],
        W_HOUR=ntp_conf["wintertime_hour"]
    )

    try:
        make_put(
            url=f"{base_url}{ntp_conf['url_sync']}",
            headers=headers,
            data=xml_data,
            auth=auth,
        )

        make_put(
            url=f"{base_url}{ntp_conf['url_time']}",
            headers=headers,
            data=time_data,
            auth=auth,
        )
        logger.info(f" -> NTP setup for {cam} completed: OK!")
        return True
    except RequestException as e:
        logger.error("NTP setup error: %s", e)
        return False
