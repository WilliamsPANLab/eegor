import mne


def run_filters(acq, config):
    """
    Applies Notch and Bandpass filters to acquisition
    """
    notch = config["notch"]
    low_pass = config["low_pass"]
    high_pass = config["high_pass"]
    assert high_pass < low_pass, ("high_pass should be less than low_pass. "
                                  f"high_pass={high_pass} low_path={low_pass}")
    return acq.copy().filter(high_pass, low_pass).notch_filter(notch)


def rereference(acq, config):
    """
    Rereference all the EEG changes to the ref_channel (usually average)
    """
    return acq.set_eeg_reference(ref_channels=config.ref_channel)


def epoch(eeg, config):
    """ Epoch a given EEG signal into fixed chunks """
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

    codes = {
            1001: "Start",
            1002: "End",
            1003: "Eyes Open",
            1004: "Eyes Closed"
            }
    """
    df = acq.annotations.to_data_frame()
    start = df[df["description"] == "0"]["onset"].min()
    half = ((df[df["description"] == "1004"]["onset"].iloc[-1] - start)
            .total_seconds())
    return half


def crop_eeg(acq, config, report):
    time = max(acq.times) - min(acq.times)
    _min, _max = config.min_acq_time, config.max_acq_time
    assert _max > _min, (f"The maximum time ({_max}s) should be greater than "
                         f"the minimum time ({_min}s)")
    assert time >= _min, (f"Acquisition is {time}s which is shorter than the "
                          f"minimum time given in the config, {_min}s")
    if time > max(acq.times):
        print("WARNING. Acquisition is {time}s which is longer than the"
              "maximum time given in the config, {_max}s")
        acq.crop(tmin=min(acq.times), tmax=min(acq.times) + _max)


'''
def split_eeg(acq, config):
    """
    Deprecated

    Before the eyes open and eyes closed data were acquired as separate
    trials, they were acquired all at once with a marker that separated
    the two
    """
    half = get_marker_timepoint(acq)
    eyes_o = acq.copy().crop(tmin=0, tmax=half)
    eyes_c = acq.copy().crop(tmin=half, tmax=None)
    crop_eeg(eyes_o, config, trial="open")
    crop_eeg(eyes_c, config, trial="closed")
    return eyes_o, eyes_c


def crop_eeg(acq, config, trial=None):
    """
    Deprecated

    The data was cut out of the worry that the transition between eyes open
    and eyes closed would be noisy.

    TODO: below is if we cared about having the durations all be the same
    eeg.crop(tmin=max(times) - trial_duration, tmax=max(times) - 15)
    """
    valid_trials = ["open", "closed"]
    assert trial in valid_trials, (f"trial={trial} is not a valid option. "
                                   f"Choose from {valid_trials}")
    epsilon = config["duration_epsilon"]
    expected_duration = config["trial_duration"]
    if f"eyes_{trial}_start_cut" in config:
        start = config[f"eyes_{trial}_start_cut"]
        acq.crop(tmin=start, tmax=None)
    if f"eyes_{trial}_end_cut" in config:
        end = config[f"eyes_{trial}_start_cut"]
        acq.crop(tmin=0, tmax=max(acq.times) - end)
    duration = max(acq.times)
    if abs(duration - expected_duration) > epsilon:
        raise Exception(f"EEG recording of duration={duration} is too short")
'''
