"""
First and foremost, the formats for EEG are a hot mess express; it's all over
the place. There is no real NIFTI eqivalent and it gets even harder since EEG is
lumped together with MEG, sEEG, ECoG. Below are some notes I've picked up

--- FIF
MNE tends to treat the fif format as one of it's first class citizen.
For more details on why [read here](https://github.com/mne-tools/mne-python/issues/5302)
This format is mostly used for MEG, but it's required by MNE. Their only writer works for the
FIF format. See https://mne.tools/stable/generated/mne.io.Raw.html#mne.io.Raw.save
NOTE: converting from CNT to fif adds differences to the data on the order of 1e-10

--- EDF
The BIDS standard highly recommends using either the European data format (EDF) or the
BrainVision Core Data Format. If I had more of a choice, I'd use the EDF+ format.
However my hope is in the format the raw data will be BIDS and the EDF+ reader will work
or MNE will add a EDF+ writer so that we can convert the CNT neuroscan inputs we have to EDF as
well as the intermediate steps.
https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/03-electroencephalography.html#eeg-recording-data

NOTE: Hopefully the above discussion on file format doesn't come across as persnickety, there
are differences introduced albeit on the order of 1e-10. However these discrepencies might
grow downstream if any segment acts chaotically (what I've noticed in MRI).
"""
import mne
import numpy as np
import eegor.utils.os as eos

def create_raw_eeg(fp):
    """
    To be consistent the raw EEG data will be converted to .fif format
    before analysis
    """
    dst = eos.replace_ext(fp, "_raw.fif")
    if Path(dst).is_file():
        return
    eeg = load_data(fp)
    eeg.save(dst)

def load_data(fp, preload=True, eog=["EOG"], montage="standard_1020"):
    """
    Loads the filepath as an MNE raw object.
    NOTE: In the VA multisite EEG TMS study, one channel of EOG is also recorded
    """
    if str(fp).endswith(".edf"):
        # mne.io.edf.edf.RawEDF
        eeg = mne.io.read_raw_edf(fp, preload=preload, eog=eog)
    elif str(fp).endswith(".fif"):
        # mne.io.fiff.raw.Raw
        eeg = mne.io.read_raw_fif(fp, preload=preload)
    elif str(fp).endswith(".cnt"):
        # mne.io.cnt.cnt.RawCNT
        eeg = mne.io.read_raw_cnt(fp, preload=preload, eog=eog)
    else:
        msg = f"Cannot read {fp}. Can only read data from the following extensions: ['.cnt', '.edf', '.fif']"
        raise NotImplementedError(msg)
    if montage:
        eeg = eeg.set_montage(montage, verbose=True)
    return eeg
