from eegor.utils.os import find_file
from eegor.utils.eeg import load_data
from eegor.config import config
import eegor.preprocess.preprocess as preprocess
from eegor.vis.report import raw_report, autoreject_report, frequency_report


def preproc(config, acq, subject):
    root = config["root"]
    dst = root / "reports" / subject / "raw.html"
    raw_report(acq.copy(), config, dst)
    eo, ec = preprocess.split_eeg(acq, config)
    for trial, raw in [("open", eo), ("closed", ec)]:
        preprocess.crop_eeg(raw, config, trial=trial)
        processed = preprocess.preprocess(raw, config)
        epochs = preprocess.epoch(processed, config)
        ar, log, clean = preprocess.reject(epochs, config)

        dst = root / "reports" / subject / f"{trial}_rejected.html"
        autoreject_report(processed.copy(), log, epochs, dst, config)
        dst = root / "reports" / subject / f"{trial}_freq.png"
        frequency_report(clean, config, f"Eyes {trial}", dst)


def main():
    root = config["root"]
    subjects = config["subjects"]
    for subject in subjects:
        fp = find_file(root / subject, "*.cnt")
        acq = load_data(fp)
        preproc(config, acq, subject)


if __name__ == "__main__":
    main()
