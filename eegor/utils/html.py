"""
Utilities: Jinja2 templates.

Copied from here
https://github.com/nipreps/mriqc/blob/af3562c63873d17089cb322f59c2924982caa8d6/mriqc/data/config.py
"""

from io import open

import jinja2
from pkg_resources import resource_filename as pkgrf


class Template(object):
    """
    Utility class for generating a config file from a jinja template.
    """

    def __init__(self, template_str):
        self.template_str = template_str
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath="/"),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def compile(self, configs):
        """Generates a string with the replacements"""
        template = self.env.get_template(self.template_str)
        return template.render(configs)

    def generate_conf(self, configs, path):
        """Saves the oucome after replacement on the template to file"""
        output = self.compile(configs)
        with open(path, "w+") as output_file:
            output_file.write(output)


class IndividualTemplate(Template):
    """Specific template for the individual report"""

    def __init__(self):
        super(IndividualTemplate, self).__init__(
            pkgrf("eegor", "data/reports/individual.html")
        )


class GroupTemplate(Template):
    """Specific template for the individual report"""

    def __init__(self):
        super(GroupTemplate, self).__init__(pkgrf("eegor", "data/reports/group.html"))
