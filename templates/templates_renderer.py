import jinja2
from jinja2 import FileSystemLoader


class TemplatesRenderer:
    def __init__(self, templates_dir: str):
        self.environment = jinja2.Environment(loader=FileSystemLoader(templates_dir))

    def render(self, template_name: str, **context):
        template = self.environment.get_template(template_name)
        return template.render(**context)