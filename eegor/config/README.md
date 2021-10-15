# Config

If a `--config` flag is not used, then the config.json here is used.

### Variables


`notch` : `list`  
    A list of frequencies to be applied to the raw EEG data

`epoch` : `float`  
    A number (in seconds) that gives the length of each epoch

`low_pass` : `float`  
    A frequency (in Hz) for the low pass filter

`high_pass` : `float`  
    A frequency (in Hz) for the high pass filter

`autoreject_method` : `str`  
    The type of method to detect noisy epochs in the autoreject library. Can be either "bayesian_optimization" or "random_search" Bayesian Optimization is preferred over random_search  
    https://github.com/autoreject/autoreject/issues/84#issuecomment-341049798  

`duration_epsilon` : `float`  
    How much longer or shorter (in seconds) can a trial be before we throw an error?

`trial_duration` : `float`  
    The expected duration of each trial (in seconds)

`random_seed` : `int`  
    Read [this](https://en.wikipedia.org/wiki/Random_seed) if you don't know what this does. Essentially, it helps generate random numbers, but at the same time, makes these random numbers reproducible
