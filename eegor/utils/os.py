from pathlib import Path, PosixPath

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

def remove_ext(filepath):
    filepath = Path(filepath)
    filename = filepath.name
    if "." not in filename:
        return filepath
    return filepath.parent / filename.split(".")[0]

def replace_ext(filepath, ext):
    orig_type = type(filepath)
    filepath_wo_ext = remove_ext(filepath)
    if orig_type == str:
        return str(filepath) + ext
    elif orig_type == PosixPath:
        return Path(str(filepath) + ext)
    raise TypeError(f"Cannot coerce {filepath} to type {orig_type}")
