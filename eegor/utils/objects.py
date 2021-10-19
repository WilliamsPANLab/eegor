JSON_OBJECTS = [str, int, float, list, dict, bool]


def is_json_serializable(value):
    if isinstance(value, JSON_OBJECTS):
        return True
    return value is None


class dotdict(dict):
    """
    dot.notation access to dictionary attributes

    Thanks to https://stackoverflow.com/a/23689767/9104642
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
