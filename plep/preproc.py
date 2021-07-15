import mne
from pathlib import Path

class DuplicateFileError(Exception):
    pass

class MissingFileError(Exception):
    pass

def preprocess(eeg):
    eeg = eeg.copy().filter(0.3, 100)
    eeg = eeg.notch_filter([60])
    eeg = eeg.resample(250)
    eeg = eeg.set_eeg_reference(ref_channels="average")
    return eeg

def epoch(eeg):
    epochs = mne.make_fixed_length_epochs(eeg, duration=2, preload=False)

def ica(epochs):
    ica = mne.preprocessing.ICA(n_components=64, max_iter="auto", random_state=97)
    ica.fit(epochs)
    ica.plot_sources(epochs, show_scrollbars=True)

def load_data(fp):
    return mne.io.cnt.read_raw_cnt(fp, preload=False)

def cut(eeg):
    eeg.crop(tmin=10)

def find_file(folder, regex: str):
    matches = folder.glob(regex)
    if len(matches) == 0:
        raise MissingFileError("Cannot find matches for", (folder / regex))
    elif len(matches) != 1:
        raise DuplicateFileError("Cannot find matches for", (folder / regex))
    else:
        return next(matches)

def main():
    root = Path("/Users/pstetz/Desktop/eeg")
    fp = find_file(root / subject, "*.cnt")
    eeg = load(fp)
    peeg = preprocess(eeg)


if __name__ == "__main__":
    main(root)
