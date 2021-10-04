import argparse
import importlib.util
from pathlib import PosixPath
from eegor.utils.os import find_file
from eegor.utils.eeg import load_data
import eegor.preprocess.preprocess as preprocess
from eegor.preprocess.reject import reject
from eegor.vis.report import raw_report, autoreject_report, frequency_report


def preprocess(config, acq, subject):
    root = config["root"]
    dst = root / "reports" / subject / "raw.html"
    raw_report(acq.copy(), config, dst)
    eo, ec = preprocess.split_eeg(acq, config)

    freq_open_fig = preprocess_trial(eo, "open")
    freq_closed_fig = preprocess_trial()
    return freq_open_fig, freq_closed_fig
    for trial, raw in [("open", eo), ("closed", ec)]:
        preprocess_trial()
        pass


def preprocess_trial():
    preprocess.crop_eeg(raw, config, trial=trial)
    processed = preprocess.run_filters(raw, config)
    processed = preprocess.rereference(processed)
    epochs = preprocess.epoch(processed, config)
    drop_eog(epochs)  # FIXME: autoreject has a cow otherwise
    ar, log, clean = reject(epochs, config)

    dst = root / "reports" / subject / f"{trial}_rejected.html"
    autoreject_report(processed.copy(), log, clean, dst, config)
    dst = root / "reports" / subject / f"{trial}_freq.png"
    return frequency_report(clean, config, f"Eyes {trial}", dst)


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
        preprocess(config, acq, subject)


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
