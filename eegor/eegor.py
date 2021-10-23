from eegor.utils.eeg import load_data, drop_eog
import eegor.preprocess.preprocess as preprocess
from eegor.preprocess.reject import reject
from eegor.vis.report import frequency_vis
import eegor.report.qa as qa
from eegor.parser import setup_config


def preprocess_trial(config, raw, trial, report):
    trial_info = {}
    trial_info["poor_channels"] = ", ".join(qa.dead_channels(raw.copy()))
    trial_info["duration"] = max(raw.times) - min(raw.times)
    processed = preprocess.run_filters(raw, config)
    processed = preprocess.rereference(processed)
    epochs = preprocess.epoch(processed, config)
    drop_eog(epochs)  # NOTE: autoreject has a cow otherwise
    ar, log, clean = reject(epochs, config)

    trial_info["num_dropped"] = qa.dropped_epochs(log)
    trial_info["freq_fig"], ax = frequency_vis(clean, config)
    report["tasks"][trial] = trial_info


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
    # FIXME: this section should be part of CLI
    config = setup_config()
    if config.group:
        from eegor.group import group
        group(config)
    else:
        eegor(config)


if __name__ == "__main__":
    main()
