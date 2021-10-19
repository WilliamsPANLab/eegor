from eegor.utils.eeg import load_data, drop_eog
import eegor.preprocess.preprocess as preprocess
from eegor.preprocess.reject import reject
from eegor.vis.report import frequency_report
import eegor.report.qa as qa
from eegor.report.report import individual_report
from eegor.parser import setup_config


def write_report(config, report):
    subject_folder = "sub-" + report["subject"]
    session_folder = "ses-" + report["session"]
    dst_dir = config.output_dir / subject_folder / session_folder
    dst = dst_dir / "report.html"
    dst.parent.mkdir(exist_ok=True, parents=True)
    with open(dst, "w") as f:
        f.write(individual_report(report))


def preprocess_trial(config, raw, trial, report):
    poor_channels = ", ".join(qa.dead_channels(raw.copy()))
    processed = preprocess.run_filters(raw, config)
    processed = preprocess.rereference(processed)
    epochs = preprocess.epoch(processed, config)
    drop_eog(epochs)  # FIXME: autoreject has a cow otherwise
    ar, log, clean = reject(epochs, config)

    num_dropped = qa.dropped_epochs(log)
    freq_fig, ax = frequency_report(clean, config, "Frequenct Spectrum")

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
