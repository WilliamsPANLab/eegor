from pathlib import Path
import eegor.report as template_folder
from eegor.utils.figure import embed_html


template_folder = Path(template_folder.__file__).parent


def open_templates():
    """
    Opens a template HTML file and returns it as one string (\n included to
    indicate newlines).
    """
    templates = dict()
    for name in ["head", "task", "tail"]:
        with open(template_folder / f"{name}.html", "r") as f:
            templates[name] = "".join(f.readlines())
    return templates


def individual_report(report):
    templates = open_templates()
    bodies = list()
    for task, info in report["tasks"].items():
        info["freq_png"] = embed_html(info["freq_fig"])
        #info["freq_dom_df"] = embed_html(info["freq_dom_df"])
        #info["table"] = embed_html(info["table"])
        info["task"] = task
        bodies.append(templates["task"].format(**info))
    if len(bodies) == 0:
        return False
    report = ([templates["head"].format(**report)] +
              bodies +
              [templates["tail"].format(**report)])
    return "\n".join(report)
