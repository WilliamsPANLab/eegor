# Config

If a `--config` flag is not used, then the config.json here is used.

### Variables

`min_acq_time` : `float`  
    The minimum acceptable time (in seconds) for an acquisition. Acquisitions shorter than this time will not be processed

`max_acq_time` : `float`  
    The maximum acceptable time (in seconds) for an acquisition. Acquisitions longer than this time will be cut down to the `max_acq_time`

`notch` : `list`  
    A list of frequencies to be applied to the raw EEG data

`epoch` : `float`  
    A number (in seconds) that gives the length of each epoch

`low_pass` : `float`  
    A frequency (in Hz) for the low pass filter

`high_pass` : `float`  
    A frequency (in Hz) for the high pass filter

`ref_channel` : `str`  
    The name of the channel to rereference all data to (usually set as "average")

`autoreject_method` : `str`  
    The type of method to detect noisy epochs in the autoreject library. Can be either "bayesian_optimization" or "random_search" Bayesian Optimization is preferred over random_search  
    https://github.com/autoreject/autoreject/issues/84#issuecomment-341049798  

`random_seed` : `int`  
    Read [this](https://en.wikipedia.org/wiki/Random_seed) if you don't know what this does. Essentially, it helps generate random numbers, but at the same time, makes these random numbers reproducible
