def dead_channels(acq, thresh=1e-15):
    """
    Given raw EEG data, determines which channels were dead

    Parameters
    ----------
    acq : mne.io.cnt.cnt.RawCNT
        The raw EEG acquisition
    thresh : float, optional
        Channels with standard deviations below this threshold are determined
        to be dead

    Returns
    -------
    The names of the channels that were determined to be dead
    """
    data = acq.get_data()
    chs = acq.info["chs"]
    dead = list()
    for i, ch in enumerate(chs):
        std = data[i].std()
        if std < thresh:
            dead.append(ch["ch_name"])
    return dead


def dropped_epochs(return_log):
    """
    Given an Autoreject return_log, returns the number of epochs dropped.

    Parameters
    ----------
    return_log : autoreject.autoreject.RejectLog
        The return_log given from AutoReject.fit_transform(...)

    Returns
    -------
    The number of bads epochs
    """
    return sum(return_log.bad_epochs)
