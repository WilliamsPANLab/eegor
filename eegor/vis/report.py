from eegor.vis.timeseries import plot_eeg_channels, plot_rejects
from eegor.utils.eeg import get_interval

def raw_report(raw, config, dst):
    title = "Raw"
    dst.parent.mkdir(exist_ok=True, parents=True)
    plot_eeg_channels(raw, str(dst), title, config)

def autoreject_report(acq, ar_log, epochs, dst, config):
    title = "Autorejected"
    dst.parent.mkdir(exist_ok=True, parents=True)
    interval = get_interval(epochs)
    plot_rejects(acq, ar_log, interval, str(dst), config)
