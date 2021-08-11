config = {
    "root": "/Users/pstetz/Desktop/eeg",
    "notch": [60], # Hz
    "low_pass": 100 # Hz
    "high_pass": 2 # Hz
    "epoch": 2, # sec
    "eyes_open_start_cut": 15, # sec
    "eyes_closed_start_cut": 15, # sec
    "trial_duration": 285, # sec
    # If the EEG duration is less than this throw an error (FIXME: or record it somewhere)
    "duration_epsilon": 1, # sec
    "seed": 42,
    "num_ica_components": 64, # channels
}
