import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def frequency_vis(epochs, config, title="Frequency Spectrum",
                  figsize=(14, 8), labelsize=24, titlesize=32):
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
    return fig, ax


def plot_bads(acq, figsize=(14, 8), SEPARATION=1e-10):
    chs = dead_channels(acq)
    data = acq.get_data()
    plt.figure(figsize=figsize)
    num = 0
    for i, ch in enumerate(acq.info["chs"]):
        if ch["ch_name"] in chs:
            num += 1
            signal = (data[i] - data[i].mean())
            signal = signal + (num * SEPARATION)
            plt.plot(acq.times, signal, ".", label=ch["ch_name"])
    plt.legend()
    plt.show()
