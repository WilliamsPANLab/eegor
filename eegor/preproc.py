import mne
from pathlib import Path
from autoreject import AutoReject
from eegor.utils.os import DuplicateFileError, MissingFileError, find_file
from eegor.utils.eeg import load_data

def preprocess(eeg, config):
    notch = config["notch"]
    low_pass = config["low_pass"]
    high_pass = config["high_pass"]
    assert low_pass < high_pass, "low_pass should be less than high_pass. {low_pass=} {high_pass=}"
    tmp = eeg.copy().filter(high_pass, low_pass)
    tmp = tmp.notch_filter(notch)
    tmp = tmp.set_eeg_reference(ref_channels="average")
    return tmp

def epoch(eeg, config):
    duration = config["epoch"]
    epochs = mne.make_fixed_length_epochs(eeg,
            duration=duration,
            preload=True,
            reject_by_annotation=False)
    return epochs

def ica(epochs, config):
    seed = config["seed"]
    N = config["num_ica_components"]
    ica = mne.preprocessing.ICA(n_components=N, max_iter="auto", random_state=seed)
    ica.fit(epochs)
    ica.plot_sources(epochs, show_scrollbars=True)

def get_marker_timepoints(eeg):
    """
    start: EEG recording has started
    half: transition period from eyes open to eyes closed
    end: EEG recording has ended
    """
    df = eeg.annotations.to_data_frame()
    start = df[df["description"] == "1003"]["onset"].iloc[0]
    half  = (df[df["description"] == "1004"]["onset"].iloc[0] - start).total_seconds()
    end   = (df[df["description"] == "1002"]["onset"].iloc[0] - start).total_seconds()
    return 0, half, end

def split_eeg(eeg, config):
    start, half, end = get_marker_timepoints(eeg)
    eyes_o = eeg.copy().crop(tmin=start, tmax=half)
    eyes_c = eeg.copy().crop(tmin=half, tmax=end)
    crop_eeg(eyes_o, config, trial="open")
    crop_eeg(eyes_c, config, trial="closed")
    eyes_c.crop(tmin=15, tmax=trial_duration)
    return eyes_o, eyes_c

def crop_eeg(eeg, config, trial=None):
    """
    TODO: below is if we cared about having the durations all be the same
    eeg.crop(tmin=max(times) - trial_duration, tmax=max(times) - 15)
    """
    valid_trials = ["open", "closed"]
    assert trial in valid_trials, f"{trial=} is not a valid option. Choose from {valid_trials}"
    epsilon = config["duration_epsilon"]
    expected_duration = config["trial_duration"]
    if f"eyes_{trial}_start_cut" in config:
        start = config[f"eyes_{trial}_start_cut"]
        eeg.crop(tmin=start, tmax=None)
    if f"eyes_{trial_end_cut}" in config
        end = config[f"eyes_{trial}_start_cut"]
        eeg.crop(tmin=0, tmax=max(eeg.times) - end)
    duration = max(eeg.times)
    assert duration + epsilon - expected_duration > 0, f"EEG recording of {duration=} is too short"

def reject(eeg, config):
    seed = config["seed"]
    n_interpolates = np.array([1, 4, 32])
    consensus_percs = np.linspace(0, 1.0, 11)
    picks = mne.pick_types(eeg.info, meg=False, eeg=True, stim=False, eog=False, ecg=False)
    ar = AutoReject(thresh_method="random_search", random_state=seed)
    ar.fit(eeg)
    clean = ar.transform(eeg)
    return clean

def preproc(config):
    root = Path(config["root"])
    fp = find_file(root / subject, "*.cnt")
    eeg = load_data(fp)
    eo, ec = split_eeg(eeg, config)
    pec = preprocess(ec, config)
    peo = preprocess(eoconfig)

if __name__ == "__main__":
    preproc(root)
