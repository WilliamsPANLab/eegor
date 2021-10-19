from eegor.utils.eeg import load_data, drop_eog
import eegor.preprocess.preprocess as preprocess
from eegor.preprocess.reject import reject
from eegor.vis.report import frequency_report
import eegor.report.qa as qa
from eegor.report.report import individual_report
from eegor.parser import setup_config
from eegor.utils.objects import is_json_serializable
from eegor.utils.os import save_json


def write_report(config, report):
    bids_sub = "sub-" + report["subject"]
    bids_ses = "ses-" + report["session"]
    dst_dir = config.output_dir / bids_sub / bids_ses
    dst_dir.mkdir(exist_ok=True, parents=True)

    fn = f"{bids_sub}_{bids_ses}_report"
    write_html(report, dst_dir / (fn + ".html"))
    write_json(report, dst_dir / (fn + ".json"))
    write_methods(config, dst_dir / f"{bids_sub}_{bids_ses}_methods.txt")


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


def preprocess_trial(config, raw, trial, report):
    poor_channels = ", ".join(qa.dead_channels(raw.copy()))
    processed = preprocess.run_filters(raw, config)
    processed = preprocess.rereference(processed)
    epochs = preprocess.epoch(processed, config)
    drop_eog(epochs)  # NOTE: autoreject has a cow otherwise
    ar, log, clean = reject(epochs, config)

    num_dropped = qa.dropped_epochs(log)
    freq_fig, ax = frequency_report(clean, config, "Frequency Spectrum")

    report["tasks"][trial] = dict()
    report["tasks"][trial]["poor_channels"] = poor_channels
    report["tasks"][trial]["num_dropped"] = num_dropped
    report["tasks"][trial]["freq_fig"] = freq_fig


def _get_task(fp):
    return fp.name.split(".")[0].split("_task-")[1].split("_")[0]


def eegor(config):
    for sub in config.subjects:
        for ses in config.sessions:
            ses_dir = config.input_dir / f"sub-{sub}" / f"ses-{ses}"
            if not ses_dir.is_dir():
                continue  # subject, session does not have available data
            report = {"subject": sub, "session": ses, "tasks": {}}
            for fp in ses_dir.glob(f"sub-{sub}_ses-{ses}_task-*.cnt"):
                print(fp)
                trial = _get_task(fp)
                acq = load_data(fp)
                preprocess_trial(config, acq, trial, report)
            write_report(config, report)


def main():
    config = setup_config()
    eegor(config)


if __name__ == "__main__":
    main()
