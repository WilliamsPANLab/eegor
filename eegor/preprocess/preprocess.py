import mne
import logging
from autoreject import AutoReject


def run_filters(acq, config):
    notch = config["notch"]
    low_pass = config["low_pass"]
    high_pass = config["high_pass"]
    assert high_pass < low_pass, ("high_pass should be less than low_pass. "
                                  f"{high_pass=} {low_pass=}")
    return acq.copy().filter(high_pass, low_pass).notch_filter(notch)


def rereference(acq):
    return acq.set_eeg_reference(ref_channels="average")


def epoch(eeg, config):
    duration = config["epoch"]
    epochs = mne.make_fixed_length_epochs(eeg,
                                          duration=duration,
                                          preload=True,
                                          reject_by_annotation=False)
    return epochs


def get_marker_timepoint(acq):
    """
    start: EEG recording has started
    half: transition period from eyes open to eyes closed
    end: EEG recording has ended
    """
    df = acq.annotations.to_data_frame()
    start = df[df["description"] == "0"]["onset"].min()
    half = ((df[df["description"] == "1004"]["onset"].iloc[0] - start)
            .total_seconds())
    return half


def split_eeg(acq, config):
    half = get_marker_timepoint(eeg)
    eyes_o = acq.copy().crop(tmin=0, tmax=half)
    eyes_c = acq.copy().crop(tmin=half, tmax=None)
    crop_eeg(eyes_o, config, trial="open")
    crop_eeg(eyes_c, config, trial="closed")
    return eyes_o, eyes_c


def crop_eeg(acq, config, trial=None):
    """
    TODO: below is if we cared about having the durations all be the same
    eeg.crop(tmin=max(times) - trial_duration, tmax=max(times) - 15)
    """
    valid_trials = ["open", "closed"]
    assert trial in valid_trials, (f"{trial=} is not a valid option. "
                                   f"Choose from {valid_trials}")
    epsilon = config["duration_epsilon"]
    expected_duration = config["trial_duration"]
    if f"eyes_{trial}_start_cut" in config:
        start = config[f"eyes_{trial}_start_cut"]
        acq.crop(tmin=start, tmax=None)
    if f"eyes_{trial}_end_cut" in config:
        end = config[f"eyes_{trial}_start_cut"]
        acq.crop(tmin=0, tmax=max(eeg.times) - end)
    duration = max(acq.times)
    if duration + epsilon - expected_duration < 0:
        print(f"EEG recording of {duration=} is too short")


def reject(epochs, config, verbose="tqdm"):
    """
    We will denote by κ the maximum number of bad sensors in a non-rejected
    trial and by ρ the maximum number of sensors that can be interpolated
    i.e. ρ are n_interpolates and κ are consensus_percs


    Please cite Autoreject! The 2nd paper has more info if you can how to
    choose the n_interpolates and consensus_percs variables
    [1] Mainak Jas, Denis Engemann, Federico Raimondo, Yousra Bekhti, and
    Alexandre Gramfort, "Automated rejection and repair of bad trials in
    MEG/EEG." In 6th International Workshop on Pattern Recognition in
    Neuroimaging (PRNI), 2016.
    [2] Mainak Jas, Denis Engemann, Yousra Bekhti, Federico Raimondo, and
    Alexandre Gramfort. 2017. "Autoreject: Automated artifact rejection for
    MEG and EEG data". NeuroImage, 159, 417-429.
    """
    seed = config["seed"]
    picks = mne.pick_types(epochs.info, meg=False, eeg=True, stim=False,
                           eog=True, ecg=False)
    # Bayesian Optimization is preferred over random_search
    # https://github.com/autoreject/autoreject/issues/84#issuecomment-341049798
    ar = AutoReject(thresh_method="bayesian_optimization", random_state=seed,
                    verbose=verbose, picks=picks)
    clean, return_log = ar.fit_transform(epochs, return_log=True)
    return ar, return_log, clean
