#!/usr/bin/python3
import json
from pathlib import Path, PosixPath


class DuplicateFileError(Exception):
    pass


class MissingFileError(Exception):
    pass


def find_file(folder, regex: str):
    matches = list(Path(folder).glob(regex))
    if len(matches) == 0:
        raise MissingFileError("Cannot find matches for", (folder / regex))
    elif len(matches) != 1:
        raise DuplicateFileError("Cannot find matches for", (folder / regex))
    else:
        return matches.pop()


def remove_ext(filepath):
    """
    Removes the extension from a filepath.
    NOTE: this will fail if "." is part of the filename
    """
    filepath = Path(filepath)
    filename = filepath.name
    if "." not in filename:
        return filepath
    return filepath.parent / filename.split(".")[0]


def replace_ext(filepath, ext):
    orig_type = type(filepath)
    filepath_wo_ext = remove_ext(filepath)
    if orig_type == str:
        return str(filepath_wo_ext) + ext
    elif orig_type == PosixPath:
        return Path(str(filepath_wo_ext) + ext)
    raise TypeError(f"Cannot coerce {filepath} to type {orig_type}")


def load_json(fp):
    with open(fp, "r") as f:
        return json.load(f)


class dotdict(dict):
    """
    dot.notation access to dictionary attributes

    Thanks to https://stackoverflow.com/a/23689767/9104642

    FIXME: does not belong in utils/os.py
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
