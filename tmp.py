
class execution(_Config):
    """Configure run-level settings."""

    raw_dir = None
    """An existing path to the dataset."""
    output_dir = None
    """Folder where derivatives will be stored."""
    log_dir = None
    """The path to a directory that contains execution logs."""
    work_dir = Path("work").absolute()
    """Path to a working directory where intermediate results will be available."""
    run_uuid = f"{strftime('%Y%m%d-%H%M%S')}_{uuid4()}"
    """Unique identifier of this particular run."""
    participant_label = None
    """List of participant identifiers that are to be preprocessed."""

    _layout = None

    _paths = (
        "raw_dir",
        "output_dir",
        "work_dir",
        "log_dir",
    )

class loggers:
    """Keep loggers easily accessible (see :py:func:`init`)."""

    _fmt = "%(asctime)s,%(msecs)d %(name)-2s " "%(levelname)-2s:\n\t %(message)s"
    _datefmt = "%y%m%d-%H:%M:%S"

    default = logging.getLogger()
    """The root logger."""
    cli = logging.getLogger("cli")
    """Command-line interface logging."""

def dumps():
    from toml import dumps
    """Format config into toml."""
    return dumps(get())
