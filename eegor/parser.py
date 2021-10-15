import argparse
from pathlib import PosixPath
from eegor.utils.os import find_file, load_json

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
                        default=config,
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
    args = parser.parse_args()
    src = args.input_file
    dst_dir = args.output_dir
    trial = args.trial
    config = load_json(args.config)
    return {
            "src": src, "dst_dir": dst_dir,
            "trial": trial, "config": config
    }
