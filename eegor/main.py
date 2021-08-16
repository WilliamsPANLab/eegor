from pathlib import Path
from eegor.utils.os import find_file
from eegor.utils.eeg import load_data
from eegor.config import config
import eegor.preprocess.preprocess as preprocess
from eegor.vis.report import raw_report, autoreject_report

def preproc(config, acq):
    raw_report(acq, config, subject)
    eo, ec = preprocess.split_eeg(acq, config)
    for trial, raw in [("open", eo), ("closed", ec)]:
        preprocess.crop_eeg(raw, config, trial=trial)
        processed = preprocess.preprocess(raw, config)
        epochs    = preprocess.epoch(processed, config)
        ar, log, clean = preprocess.reject(epochs, config)
        autoreject_report(processed, log, epochs, subject, trial, config)

def main():
    root     = config["root"]
    subjects = config["subjects"]
    for subject in subjects:
        fp  = find_file(root / subject, "*.cnt")
        acq = load_data(fp)
        preproc(config, acq)

if __name__ == "__main__":
    main()
