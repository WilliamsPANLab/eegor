from tqdm import tqdm
from eegor.vis.timeseries import plot_eeg_channels, plot_rejects
from eegor.utils.eeg import get_interval
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def frequency_report(epochs, config, title, dst, figsize=(14, 8),
                     labelsize=24, titlesize=32):
    fig, ax = plt.subplots(figsize=figsize)
    fig = epochs.plot_psd(
            fmin=config["high_pass"],
            fmax=config["low_pass"],
            average=False, ax=ax, show=False)
    xlabel = ax.xaxis.get_label().get_text()
    ax.set_xlabel(xlabel, fontsize=labelsize)
    ylabel = ax.yaxis.get_label().get_text()
    ax.set_ylabel(ylabel, fontsize=labelsize)
    ax.set_title(title, fontsize=titlesize)
    ax.set_ylim([5, 50])
    fig.savefig(dst)


def raw_plot(raw, dst):
    width, height = 2**8, 8
    skip = 20
    data = raw.get_data()
    times = raw.times
    N = data.shape[0]
    fig, axarr = plt.subplots(N, 1, figsize=(width, height*N))
    for i in tqdm(range(N)):
        axarr[i].plot(times[::skip], data[i, ::skip])
        axarr[i].set_xlim([min(times), max(times)])
        axarr[i].set_xticks(range(int(min(times)), int(max(times)), 10))
        axarr[i].set_ylabel(raw.info["chs"][i]["ch_name"], fontsize=32)
    plt.tight_layout()
    plt.savefig(dst)


def raw_report(raw, config, dst):
    title = "Raw"
    dst.parent.mkdir(exist_ok=True, parents=True)
    plot_eeg_channels(raw, str(dst), title, config)


def autoreject_report(acq, ar_log, epochs, dst, config):
    dst.parent.mkdir(exist_ok=True, parents=True)
    interval = get_interval(epochs)
    plot_rejects(acq, ar_log, interval, str(dst), config)
