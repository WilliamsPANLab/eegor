from pathlib import Path

class DuplicateFileError(Exception):
    pass

class MissingFileError(Exception):
    pass

def find_file(folder, regex: str):
    matches = Path(folder).glob(regex)
    if len(matches) == 0:
        raise MissingFileError("Cannot find matches for", (folder / regex))
    elif len(matches) != 1:
        raise DuplicateFileError("Cannot find matches for", (folder / regex))
    else:
        return next(matches)
