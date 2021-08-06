import mne
from pathlib import Path
from eegor.utils.os import DuplicateFileError, MissingFileError, load_data, find_file

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

def cut(eeg):
    eeg.crop(tmin=10)

def main():
    root = Path("/Users/pstetz/Desktop/eeg")
    fp = find_file(root / subject, "*.cnt")
    eeg = load_data(fp)
    peeg = preprocess(eeg)

if __name__ == "__main__":
    main(root)
