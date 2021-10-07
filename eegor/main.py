import argparse
import importlib.util
from pathlib import PosixPath
from eegor.utils.os import find_file
from eegor.utils.eeg import load_data
import eegor.preprocess.preprocess as preprocess
from eegor.preprocess.reject import reject
from eegor.vis.report import frequency_report
import eegor.report.qa as qa
from eegor.report.report import individual_report


def preprocess_subject(config, acq, subject):
    root = config["root"]
    dst = root / "reports" / f"{subject}.html"
    poor_channels = ", ".join(qa.dead_channels(acq.copy()))
    eo, ec = preprocess.split_eeg(acq, config)

    num_dropped_open, freq_open_fig = preprocess_trial(eo, "open", config)
    num_dropped_closed, freq_closed_fig = preprocess_trial(ec, "closed", config)  # noqa: E501
    report = individual_report(subject, poor_channels,
                               num_dropped_open, num_dropped_closed,
                               freq_open_fig, freq_closed_fig)
    dst.parent.mkdir(exist_ok=True, parents=True)
    with open(dst, "w") as f:
        f.write(report)


def preprocess_trial(raw, trial, config):
    preprocess.crop_eeg(raw, config, trial=trial)
    processed = preprocess.run_filters(raw, config)
    processed = preprocess.rereference(processed)
    epochs = preprocess.epoch(processed, config)
    drop_eog(epochs)  # FIXME: autoreject has a cow otherwise
    ar, log, clean = reject(epochs, config)

    num_dropped = qa.dropped_epochs(log)
    freq_fig, ax = frequency_report(clean, config, f"Eyes {trial}")
    return num_dropped, freq_fig


def drop_eog(epochs):
    if any(["EOG" == ch["ch_name"] for ch in epochs.info["chs"]]):
        epochs.drop_channels("EOG")


def main(config):
    root = config["root"]
    subjects = config["subjects"]
    for subject in subjects:
        fp = find_file(root / subject, "*.cnt")
        print(fp)
        acq = load_data(fp)
        preprocess_subject(config, acq, subject)


def parse_args():
    parser = argparse.ArgumentParser(description="EEGOR config parser")
    parser.add_argument("config_path", type=PosixPath,
                        help="Path to the config file")
    args = parser.parse_args()
    config_path = args.config_path
    loader = importlib.util.spec_from_file_location(config_path.name,
                                                    str(config_path))
    module = importlib.util.module_from_spec(loader)
    loader.loader.exec_module(module)
    return module.config


if __name__ == "__main__":
    config = parse_args()
    main(config)
