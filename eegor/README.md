<a id="toc"></a>

# Introduction

This is the EEG processing pipeline that will be used for the EEG data collected in the multisite [VA TMS study](#https://bmcpsychiatry.biomedcentral.com/articles/10.1186/s12888-020-03030-z). (Linked is the MRI arm of the study. The EEG protocol paper is hitting the presses soon!)

The main software used is the [MNE](https://github.com/mne-tools/mne-python). However matplotlib and other visualization software is commonly used

This pipeine may not extend to your study!

### [Processing steps](preprocess)

TODO

The parameters used for this step can be found in the [config.py](./config.py) file.

### QA

For EEG data, it's very helpful to check that the data has been preprocessed correctly, bad channels are caught, and the correct ICA components are flagged

> ICA applied. Start with one run through and test if a second ICA is required.

### Checks

The incoming data should be at the 2,000 Hz sampling rate

> Generate EEG values for primary measures of interest. Establish the range of expected values. Set criteria for identifying extreme scores post-ICA so as to have an alert to go back and do a more detailed visual inspection

### Group-level

> Identify the parameters that may produce systematic issues, and violate the assumption that noise will be random – such as subject or site characteristics
