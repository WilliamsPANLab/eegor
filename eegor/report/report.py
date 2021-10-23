from pathlib import Path
import eegor.report as template_folder
from eegor.utils.figure import embed_html
from eegor.utils.os import save_json
from eegor.utils.objects import is_json_serializable
from eegor.report.report import individual_report


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
        info["task"] = task
        bodies.append(templates["task"].format(**info))
    if len(bodies) == 0:
        return False
    report = ([templates["head"].format(**report)] +
              bodies +
              [templates["tail"].format(**report)])
    return "\n".join(report)


def save_annotations(acq, dst):
    df = acq.annotations.to_data_frame()
    df.rename(columns={"onset": "datetime"}, inplace=True)
    df["onset"] = ((df["datetime"] - df["datetime"].min())
                   .map(lambda x: x.total_seconds()))
    df.to_csv(dst, index=False)


def write_html(report, dst):
    with open(dst, "w") as f:
        f.write(individual_report(report))


def write_json(report, dst):
    metrics = dict()
    for task, info in report["tasks"].items():
        metrics.setdefault(task, dict())
        for k, v in info.items():
            if not is_json_serializable(v):
                continue
            metrics[task][k] = v
    save_json(metrics, dst)


def write_report(acq, config, report):
    bids_sub = "sub-" + report["subject"]
    bids_ses = "ses-" + report["session"]
    dst_dir = config.output_dir / bids_sub / bids_ses
    dst_dir.mkdir(exist_ok=True, parents=True)

    fn = f"{bids_sub}_{bids_ses}"
    write_html(report, dst_dir / (fn + "_report.html"))
    write_json(report, dst_dir / (fn + "_report.json"))
    write_methods(config, dst_dir / (fn + "_methods.txt"))
    save_annotations(acq, dst_dir / (fn + "_annotations.csv"))


def write_methods(config, dst):
    filters = "Hz, ".join(config.notch) + "Hz"
    text = f"""The raw EEG was filtered with a high pass of
    {config.high_pass}Hz and a low pass of {config.low_pass}Hz.
    Then notch filters, {filters}, were applied to the EEG data.
    The data was rereferenced to the {config.ref_channel}. Epochs
    were generated with a period of {config.epoch}s. Finally Autoreject
    was run using {config.autoreject_method}"""
    with open(dst, "w") as f:
        f.write(dst, text)
