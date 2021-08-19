from eegor.vis.timeseries import plot_eeg_channels, plot_rejects
from eegor.utils.eeg import get_interval

def frequency_report(epochs, config, title, dst, figsize=(14, 8), labelsize=24, titlesize=32):
    fig, ax = plt.subplots(figsize=figsize)
    fig = epochs.plot_psd(
            fmin=config["high_pass"],
            fmax=config["low_pass"],
            average=False, ax=ax)
    xlabel = ax.xaxis.get_label().get_text()
    ax.set_xlabel(xlabel, fontsize=labelsize)
    ylabel = ax.yaxis.get_label().get_text()
    ax.set_ylabel(ylabel, fontsize=labelsize)
    ax.set_title(title, fontsize=titlesize)
    fig.savefig(dst)

def raw_report(raw, config, dst):
    title = "Raw"
    dst.parent.mkdir(exist_ok=True, parents=True)
    plot_eeg_channels(raw, str(dst), title, config)

def autoreject_report(acq, ar_log, epochs, dst, config):
    title = "Autorejected"
    dst.parent.mkdir(exist_ok=True, parents=True)
    interval = get_interval(epochs)
    plot_rejects(acq, ar_log, interval, str(dst), config)
