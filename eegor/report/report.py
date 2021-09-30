import eegor.report.data as template_folder
template_folder = Path(template_folder.__file__).parent


def open_template():
    with open(template_folder / "template.html", "r") as f:
        return "".join(f.readlines())
