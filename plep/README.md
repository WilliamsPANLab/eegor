<a id="toc"></a>

# Introduction

The main software used is the [MNE](https://github.com/mne-tools/mne-python). However matplotlib and other visualization software is commonly used

### Processing steps

1.) A high pass filter of 0.3Hz, a low pass filter of 100Hz

2.) 60Hz Notch filter

3.) Downsampled to 500 Hz

4.) Reference to average electrodes

5.) Noisy channels will be identified with [Maxwell filtering](https://mne.tools/stable/generated/mne.preprocessing.find_bad_channels_maxwell.html)

6.) Noisy channels will be replaced via interpolation with neighboring electrodes

7.) Epochs of 2 second sections will be formed

8.) ICA will be run and an attempt to idenify artifacts will be made


### QA

For EEG data, it's very helpful to check that the data has been preprocessed correctly, bad channels are caught, and the correct ICA components are flagged

> ICA applied. Start with one run through and test if a second ICA is required.

### Checks

The incoming data should be at the 2,000 Hz sampling rate

> Generate EEG values for primary measures of interest. Establish the range of expected values. Set criteria for identifying extreme scores post-ICA so as to have an alert to go back and do a more detailed visual inspection

### Group-level

> Identify the parameters that may produce systematic issues, and violate the assumption that noise will be random – such as subject or site characteristics
