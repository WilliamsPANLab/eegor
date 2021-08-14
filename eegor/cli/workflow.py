"""
The workflow builder factory method.
All the checks and the construction of the workflow are done
inside this function that has pickleable inputs and output
dictionary (``retval``) to allow isolation using a
``multiprocessing.Process`` that allows fmriprep to enforce
a hard-limited memory-scope.
"""
from pathlib import Path
from pkg_resources import resource_filename as pkgrf
from niworkflows.utils.bids import collect_participants, check_pipeline_version
from niworkflows.utils.misc import check_valid_fs_license
from niworkflows.reports import generate_reports
from .. import config
from ..utils.misc import check_deps
from ..workflows.base import init_fmriprep_wf


def build_workflow(config_file, retval):
    """Create the Nipype Workflow that supports the whole execution graph."""

    config.load(config_file)
    build_log = config.loggers.workflow

    fmriprep_dir = config.execution.fmriprep_dir
    version = config.environment.version

    retval["return_code"] = 1
    retval["workflow"] = None

    banner = [f"Running fMRIPrep version {version}"]
    notice_path = Path(pkgrf("fmriprep", "data/NOTICE"))
    if notice_path.exists():
        banner[0] += "\n"
        banner += [f"License NOTICE {'#' * 50}"]
        banner += [f"fMRIPrep {version}"]
        banner += notice_path.read_text().splitlines(keepends=False)[1:]
        banner += ["#" * len(banner[1])]
    build_log.log(25, f"\n{' ' * 9}".join(banner))

    # warn if older results exist: check for dataset_description.json in output folder
    msg = check_pipeline_version(version, fmriprep_dir / "dataset_description.json")
    if msg is not None:
        build_log.warning(msg)

    # Please note this is the input folder's dataset_description.json
    dset_desc_path = config.execution.bids_dir / "dataset_description.json"
    if dset_desc_path.exists():
        from hashlib import sha256

        desc_content = dset_desc_path.read_bytes()
        config.execution.bids_description_hash = sha256(desc_content).hexdigest()

    # First check that bids_dir looks like a BIDS folder
    subject_list = collect_participants(
        config.execution.layout, participant_label=config.execution.participant_label
    )

    # Called with reports only
    if config.execution.reports_only:
        build_log.log(
            25, "Running --reports-only on participants %s", ", ".join(subject_list)
        )
        retval["return_code"] = generate_reports(
            subject_list,
            fmriprep_dir,
            config.execution.run_uuid,
            config=pkgrf("fmriprep", "data/reports-spec.yml"),
            packagename="fmriprep",
        )
        return retval

    # Build main workflow
    init_msg = [
        "Building fMRIPrep's workflow:",
        f"BIDS dataset path: {config.execution.bids_dir}.",
        f"Participant list: {subject_list}.",
        f"Run identifier: {config.execution.run_uuid}.",
        f"Output spaces: {config.execution.output_spaces}.",
    ]

    if config.execution.anat_derivatives:
        init_msg += [
            f"Anatomical derivatives: {config.execution.anat_derivatives}."
        ]

    if config.execution.fs_subjects_dir:
        init_msg += [
            f"Pre-run FreeSurfer's SUBJECTS_DIR: {config.execution.fs_subjects_dir}."
        ]

    build_log.log(25, f"\n{' ' * 11}* ".join(init_msg))

    retval["workflow"] = init_fmriprep_wf()

    # Check for FS license after building the workflow
    if not check_valid_fs_license():
        from ..utils.misc import fips_enabled
        if fips_enabled():
            build_log.critical("""\
ERROR: Federal Information Processing Standard (FIPS) mode is enabled on your system. \
FreeSurfer (and thus fMRIPrep) cannot be used in FIPS mode. \
Contact your system administrator for assistance.""")
        else:
            build_log.critical("""\
ERROR: a valid license file is required for FreeSurfer to run. fMRIPrep looked for an existing \
license file at several paths, in this order: 1) command line argument ``--fs-license-file``; \
2) ``$FS_LICENSE`` environment variable; and 3) the ``$FREESURFER_HOME/license.txt`` path. Get it \
(for free) by registering at https://surfer.nmr.mgh.harvard.edu/registration.html""")
        retval["return_code"] = 126  # 126 == Command invoked cannot execute.
        return retval

    # Check workflow for missing commands
    missing = check_deps(retval["workflow"])
    if missing:
        build_log.critical(
            "Cannot run fMRIPrep. Missing dependencies:%s",
            "\n\t* ".join(
                [""] + [f"{cmd} (Interface: {iface})" for iface, cmd in missing]
            ),
        )
        retval["return_code"] = 127  # 127 == command not found.
        return retval

    config.to_filename(config_file)
    build_log.info(
        "fMRIPrep workflow graph with %d nodes built successfully.",
        len(retval["workflow"]._get_all_nodes()),
    )
    retval["return_code"] = 0
    return retval