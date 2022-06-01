from eegor.utils.eeg import load_data, drop_eog
import eegor.preprocess.preprocess as preprocess
from eegor.preprocess.reject import reject
from eegor.vis.report import frequency_report, df_report
import eegor.report.qa as qa
from eegor.report.report import individual_report
from eegor.parser import setup_config
from os import path, replace
from pathlib import Path
import pandas as pd

def write_report(config, report):
    subject_folder = "sub-" + report["subject"]
    session_folder = "ses-" + report["session"]
    dst_dir = config.output_dir / subject_folder / session_folder
    dst = dst_dir / "report.html"
    dst.parent.mkdir(exist_ok=True, parents=True)
    #report["tasks"][trial]["freq_dom_df"].to_csv(dst_dir / "freq_domain.csv")
    with open(dst, "w") as f:
        f.write(individual_report(report))


def preprocess_trial(config, raw, trial, report):
    subject_folder = "sub-" + report["subject"]
    session_folder = "ses-" + report["session"]
    dst_dir = config.output_dir / subject_folder / session_folder
    poor_channels = ", ".join(qa.dead_channels(raw.copy()))
    processed = preprocess.run_filters(raw, config)
    processed = preprocess.rereference(processed)
    epochs = preprocess.epoch(processed, config)
    epochs = preprocess.gratton(epochs)

    drop_eog(epochs)  # FIXME: autoreject has a cow otherwise
    ar, log, clean = reject(epochs, config)

    num_dropped = qa.dropped_epochs(log)
    freq_dicts = []
    for epoch in clean:
        t_freq_dict = preprocess.freq_domain(epoch, clean.info['chs'], config)
        freq_dicts.append(t_freq_dict)
    freq_fig, ax = frequency_report(clean, config, "Frequency Spectrum")
        
    report["tasks"][trial] = dict()
    report["tasks"][trial]["poor_channels"] = poor_channels
    report["tasks"][trial]["num_dropped"] = num_dropped
    report["tasks"][trial]["freq_fig"] = freq_fig

    df = pd.DataFrame(freq_dicts)
    df.to_csv(dst_dir / f"{trial}_freq_domain.csv")


def _get_task(fp):
    return fp.name.split(".")[0].split("_task-")[1].split("_")[0]


def eegor(config):
    for sub in config.subjects:
        for ses in config.sessions:
            ses_dir = config.input_dir / sub
            if not ses_dir.is_dir():
                continue  # subject, session does not have available data
            report = {"subject": sub, "session": ses, "tasks": {}}
            # creating two lists, one of files in ses_dir with correct formatting, and one with every .cnt file
            # if a .cnt is not in the correct formatting file list, we can correct it
            good_list = ses_dir.glob(f"sub-{sub}_ses-{ses}_task-*.cnt")
            for fp in ses_dir.glob(f"*{sub}*{ses}*.cnt"):
                if fp not in good_list:
                    print(path.basename(fp))
                    task = "".join(path.basename(fp).split('_')[-2:])
                    print(task)
                    new_fp = str(fp).replace(path.basename(fp), f"sub-{sub}_ses-{ses}_task-{task}")
                    replace(fp, new_fp)
                    print(f"{fp} -> {new_fp}")
                    fp = new_fp
                else:
                    print(fp)
                trial = _get_task(Path(fp))
                acq = load_data(fp)
                preprocess_trial(config, acq, trial, report)
                write_report(config, report)


def main():
    config = setup_config()
    eegor(config)


if __name__ == "__main__":
    main()
