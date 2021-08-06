import mne
from pathlib import Path
from autoreject import AutoReject
from eegor.utils.os import DuplicateFileError, MissingFileError, find_file
from eegor.utils.eeg import load_data

def preprocess(eeg):
    tmp = eeg.copy().filter(2, 100)
    tmp = tmp.notch_filter([60])
    tmp = tmp.set_eeg_reference(ref_channels="average")
    return tmp

def epoch(eeg):
    epochs = mne.make_fixed_length_epochs(eeg, duration=2, preload=False)

def ica(epochs):
    ica = mne.preprocessing.ICA(n_components=64, max_iter="auto", random_state=97)
    ica.fit(epochs)
    ica.plot_sources(epochs, show_scrollbars=True)

def split_eeg(eeg):
    df = eeg.annotations.to_data_frame()
    start = df[df["description"] == "1003"]["onset"].iloc[0]
    half  = (df[df["description"] == "1004"]["onset"].iloc[0] - start).total_seconds()
    end   = (df[df["description"] == "1002"]["onset"].iloc[0] - start).total_seconds()
    start = 0
    eyes_o = eeg.copy().crop(tmin=start, tmax=half)
    eyes_c = eeg.copy().crop(tmin=half, tmax=end)
    #FIXME: raise warnings if the length is too short
    eyes_o.crop(tmin=max(eyes_o.times) - 285, tmax=max(eyes_o.times) - 15)
    eyes_c.crop(tmin=15, tmax=285)
    return eyes_o, eyes_c

def reject(eeg):
    n_interpolates = np.array([1, 4, 32])
    consensus_percs = np.linspace(0, 1.0, 11)
    picks = mne.pick_types(eeg.info, meg=False, eeg=True, stim=False, eog=False, ecg=False)
    ar = AutoReject(thresh_method="random_search", random_state=42)
    ar.fit(eeg)
    clean = ar.transform(eeg)
    return clean

def main():
    root = Path("/Users/pstetz/Desktop/eeg")
    fp = find_file(root / subject, "*.cnt")
    eeg = load_data(fp)
    eo, ec = split_eeg(eeg)
    pec = preprocess(ec)
    peo = preprocess(eo)

if __name__ == "__main__":
    main(root)
