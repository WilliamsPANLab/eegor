"""
Incomplete. Patrick did not have time to finish this before he left

The idea is to collate the results from a directory of individual
reports so that the quality can be viewed at a glance
"""


from eegor.utils.os import load_json


def group(config):
    metrics = dict()
    dst = config.output_dir / "group_report.html"
    for sub in config.subjects:
        for ses in config.sessions:
            ses_dir = config.input_dir / f"sub-{sub}" / f"ses-{ses}"
            if not ses_dir.is_dir():
                continue  # subject, session does not have available data
            metrics = load_json(ses_dir / f"sub-{sub}_ses-{ses}_report.json")
    with open(dst, "w") as f:
        f.write(str(metrics))  # FIXME: save plots here
