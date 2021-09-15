import imp
import argparse
from pathlib import PosixPath
from eegor.utils.os import find_file
from eegor.utils.eeg import load_data
import eegor.preprocess.preprocess as preprocess
from eegor.preprocess.reject import reject
from eegor.vis.report import raw_report, autoreject_report, frequency_report


def preproc(config, acq, subject):
    root = config["root"]
    dst = root / "reports" / subject / "raw.html"
    raw_report(acq.copy(), config, dst)
    eo, ec = preprocess.split_eeg(acq, config)
    for trial, raw in [("open", eo), ("closed", ec)]:
        preprocess.crop_eeg(raw, config, trial=trial)
        processed = preprocess.run_filters(raw, config)
        processed = preprocess.rereference(processed)
        epochs = preprocess.epoch(processed, config)
        ar, log, clean = reject(epochs, config)

        dst = root / "reports" / subject / f"{trial}_rejected.html"
        autoreject_report(processed.copy(), log, epochs, dst, config)
        dst = root / "reports" / subject / f"{trial}_freq.png"
        frequency_report(epochs, config, f"Eyes {trial}", dst)


def main(config):
    root = config["root"]
    subjects = config["subjects"]
    for subject in subjects:
        fp = find_file(root / subject, "*.cnt")
        acq = load_data(fp)
        preproc(config, acq, subject)


def parse_args():
    parser = argparse.ArgumentParser(description="EEGOR config parser")
    parser.add_argument("config_path", type=PosixPath,
                        help="Path to the config file")
    args = parser.parse_args()
    config = imp.load_source(args.config_path.name, str(args.config_path))
    return config.config


if __name__ == "__main__":
    config = parse_args()
    main(config)
