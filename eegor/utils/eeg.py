import mne
import numpy as np

def load_data(fp):
    eeg = mne.io.cnt.read_raw_cnt(fp, preload=False, eog=["EOG"])
    eeg = eeg.set_montage("standard_1020", verbose=True)
    return eeg
