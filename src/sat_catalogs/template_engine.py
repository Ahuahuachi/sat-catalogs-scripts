"""Template engine functions"""

from jinja2 import Environment, PackageLoader, Template, select_autoescape

env = Environment(
    loader=PackageLoader("sat_catalogs"),
    autoescape=select_autoescape(),
)


def get_template(template_path: str) -> Template:
    """Returns the template as string

    Args:
        template_path (str): Path to the template file

    Returns:
        Template: Template object
    """
    return env.get_template(template_path)
