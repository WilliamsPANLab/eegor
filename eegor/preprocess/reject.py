import mne
from autoreject import AutoReject


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
