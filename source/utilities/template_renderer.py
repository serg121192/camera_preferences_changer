from jinja2 import Environment, FileSystemLoader

from source.utilities.logger_setup import setup_logger


logger = setup_logger()
environment = Environment(
    loader=FileSystemLoader("./config/templates/")
)


def render_template(template_name: str, **kwargs) -> str:
    try:
        template = environment.get_template(template_name)
        return template.render(**kwargs)
    except FileNotFoundError as e:
        raise logger.error("Template file error: %s", e)
