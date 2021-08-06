import mne
import numpy as np

def load_data(fp):
    eeg = mne.io.cnt.read_raw_cnt(fp, preload=False, eog=["EOG"])
    fix_channel_locations(eeg)

def fix_channel_locations(eeg):
    chs = mne.channels.make_standard_montage("standard_1020")
    pos = chs.get_positions()["ch_pos"]
    for ch in eeg.info["chs"]:
        name = ch["ch_name"]
        if name == "EOG": continue
        loc = np.zeros(12)
        loc[:3] = pos[name]
        ch["loc"] = loc
