import argparse
from pathlib import Path, PosixPath
from eegor.utils.os import load_json
from eegor.utils.objects import dotdict


def get_subjects(args):
    if (args.participant_label is not None and
            args.participant_tsv is not None):
        raise RuntimeError("Cannot provide both --participant-label and "
                           "participant-tsv flags")
    if args.participant_label is not None:
        return args.participant_label
    elif args.participant_tsv is not None:
        subjects = open(args.participant_tsv, "r").readlines()
        return [_drop_sub(sub).replace("\n", "") for sub in subjects]
    else:
        # Default to the participant TSV in the BIDS directory
        input_dir = args.input_dir
        subjects = open(input_dir / "participant.tsv", "r").readlines()
        return [_drop_sub(sub).replace("\n", "") for sub in subjects]


def get_sessions(args):
    if args.session_label is not None:
        return args.session_label
    else:
        # Default to all sessions if flag not provided
        return ["00", "01", "02"]


def _drop_sub(value):
    return value[4:] if value.startswith("sub-") else value


def _drop_ses(value):
    return int(value[4:]) if value.startswith("ses-") else value


def parse_args():
    parser = argparse.ArgumentParser(description="EEGOR config parser")
    parser.add_argument("input_dir", type=PosixPath,
                        help="The input directory of EEG subjects")
    parser.add_argument("output_dir", type=PosixPath,
                        help="The output directory for EEGOR outputs")
    parser.add_argument("--config", type=PosixPath,
                        help="Path to the config file")
    parser.add_argument("--participant-label",
                        action="store",
                        nargs="+",
                        type=_drop_sub,
                        help="a space delimited list of participant "
                        "identifiers or a single identifier (the sub- prefix "
                        "can be removed). Defaults to list in "
                        "participants.tsv.")
    parser.add_argument("--session-label",
                        action="store",
                        nargs="+",
                        type=_drop_ses,
                        help="a space delimited list of session "
                        "identifiers or a single identifier (the ses- prefix "
                        "can be removed). Defaults to all sessions.")
    parser.add_argument("--participant-tsv", type=PosixPath,
                        help="A path to a TSV with the IDs of subjects to "
                        "be processed")
    parser.add_argument("--group", action="store_true",
                        help="Runs a group report instead of individual "
                        "processing")
    return parser.parse_args()


def setup_config():
    args = parse_args()
    if args.config is None:
        import eegor.config as config_dir
        config_dir = Path(config_dir.__file__).parent
        config_path = config_dir / "config.json"
    else:
        config_path = args.config
    assert config_path.is_file(), f"Cannot find config: {config_path}"
    config = load_json(config_path)
    config["subjects"] = get_subjects(args)
    config["sessions"] = get_sessions(args)
    return dotdict({**config, **vars(args)})
