from eegor.vis.timeseries import plot_eeg_channels, plot_rejects
from eegor.utils.eeg import get_interval

def raw_report(raw, config, subject):
    dst = root / "reports" / subject / "raw.html"
    title = "Raw"
    dst.parent.mkdir(exist_ok=True, parents=True)
    plot_eeg_channels(raw, dst, title, config)

def autoreject_report(acq, ar_log, epochs, subject, trial, config):
    dst = root / "reports" / subject / f"{trial}_rejected.html"
    title = "Autorejected"
    dst.parent.mkdir(exist_ok=True, parents=True)
    interval = get_interval(epochs)
    plot_rejects(acq, ar_log, interval, dst, config)
