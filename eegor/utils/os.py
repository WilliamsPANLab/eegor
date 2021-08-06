import mne

class DuplicateFileError(Exception):
    pass

class MissingFileError(Exception):
    pass

def load_data(fp):
    return mne.io.cnt.read_raw_cnt(fp, preload=False)

def find_file(folder, regex: str):
    matches = folder.glob(regex)
    if len(matches) == 0:
        raise MissingFileError("Cannot find matches for", (folder / regex))
    elif len(matches) != 1:
        raise DuplicateFileError("Cannot find matches for", (folder / regex))
    else:
        return next(matches)
