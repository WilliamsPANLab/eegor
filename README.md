# EEGOR (EEG Operationalized Refinement)

These are EEG processing scripts that are used for the TMS Biomarkers collaboration study.

### Installation

```
git clone https://github.com/WilliamsPANLab/eegor
cd eegor
pip3 install .
```

### Updating code

To reflect modifications to master code run the following commands while in the repository root

```
git pull origin master
pip3 unstall eegor
pip3 install .
```

### Processing steps

Please see the [readme](eegor#toc) under the `eegor` folder for details


### Preparing to run EEGOR

The organization will be pseudo-BIDS (`.cnt` files aren't allow for BIDS). The 
TMS Biomarkers EEG data is straightforward so there's only two input files per 
subject/session. They should look like the below

`$INPUT/sub-$SUBJECT/ses-$SESSION/sub-$SUBJECT_ses-$SESSION_task-{open,closed}.cnt`

### Running EEGOR!

EEGOR is designed to run similar to [fMRIPrep](https://github.com/nipreps/fmriprep)


```
python (...)/eegor/eegor.py [--config]
                            [--participant-label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]] 
                            [--session-label SESSION_LABEL [SESSION_LABEL ...]] 
                            [--participant-tsv]
                            $INPUT $OUTPUT
```

If both the `--participant-label` and `--participant-tsv` flags aren't provided, then the subjects listed in the `$INPUT/participants.tsv` will be used.

If a `--session-label` flag isn't provided, then the sessions will be: 
`ses-00`, `ses-01`, and `ses-02`
