import os
import random
import numpy as np
from pathlib import Path
from time import strftime

config = {
    "root": "/Users/pstetz/Desktop/eeg",
    "notch": [60], # Hz
    "low_pass": 100, # Hz
    "high_pass": 2, # Hz
    "epoch": 2, # sec
    "eyes_open_start_cut": 15, # sec
    "eyes_closed_start_cut": 15, # sec
    "trial_duration": 285, # sec
    # If the EEG duration is less than this throw an error (FIXME: or record it somewhere)
    "duration_epsilon": 1, # sec
    "seed": 5,
    "num_ica_components": 64, # channels
    "plot_downsample": 10, # Hz
    "plot_max_channels": 16, # channels
    "subjects": ["pat2"]
}
config["root"] = Path(config["root"])

class _Config:
    """An abstract class forbidding instantiation."""

    _paths = tuple()

    def __init__(self):
        """Avert instantiation."""
        raise RuntimeError("Configuration type is not instantiable.")

    @classmethod
    def load(cls, settings, init=True, ignore=None):
        """Store settings from a dictionary."""
        ignore = ignore or {}
        for k, v in settings.items():
            if k in ignore or v is None:
                continue
            if k in cls._paths:
                setattr(cls, k, Path(v).absolute())
            elif hasattr(cls, k):
                setattr(cls, k, v)

        if init:
            try:
                cls.init()
            except AttributeError:
                pass

    @classmethod
    def get(cls):
        """Return defined settings."""
        out = {}
        for k, v in cls.__dict__.items():
            if k.startswith("_") or v is None:
                continue
            if callable(getattr(cls, k)):
                continue
            if k in cls._paths:
                v = str(v)
            out[k] = v
        return out

class environment(_Config):
    """
    Read-only options regarding the platform and environment.
    The ``environment`` section is not loaded in from file,
    only written out when settings are exported.
    This config section is useful when reporting issues,
    and these variables are tracked whenever the user does not
    opt-out using the ``--notrack`` argument.
    """

    cpu_count = os.cpu_count()
    """Number of available CPUs."""
    #version = __version__
    """*EEGOR*'s version."""

class seeds(_Config):
    """Initialize the PRNG and track random seed assignments"""

    _random_seed = None
    master = None
    """Master random seed to initialize the Pseudorandom Number Generator (PRNG)"""
    numpy = None
    """Seed used by NumPy"""

    @classmethod
    def init(cls):
        if cls._random_seed is not None:
            cls.master = cls._random_seed
        if cls.master is None:
            cls.master = random.randint(1, 65536)
        random.seed(cls.master)  # initialize the PRNG
        # functions to set program specific seeds
        cls.numpy = _set_numpy_seed()

def _set_numpy_seed():
    """NumPy's random seed is independant from Python's `random` module"""
    val = random.randint(1, 65536)
    np.random.seed(val)
    return val

def get(flat=False):
    """Get config as a dict."""
    settings = {
        "environment": environment.get(),
        "execution": execution.get(),
        "workflow": workflow.get(),
        "seeds": seeds.get(),
    }
    if not flat:
        return settings

    return {
        ".".join((section, k)): v
        for section, configs in settings.items()
        for k, v in configs.items()
    }

def to_filename(filename):
    """Write settings to file."""
    filename = Path(filename)
    filename.write_text(dumps())
