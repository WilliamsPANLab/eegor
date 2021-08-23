from math import ceil
import numpy as np
import plotly.graph_objects as go
from scipy.signal import detrend
from tqdm import tqdm

def pretty_eeg(channel, index, use_detrend=True, thresh=1e-16, offset_factor=4):
    """
    Unfortunately, the raw EEG signal can't be plotted as is, it won't
    be deceipherable by anyone. EEG signal gets better over time so
    scipy's detrend is used to remove this. The signal mean is changed so
    that there is a y-axis offset and EEG channels don't overlap. Finally,
    the data is divided by the standard deviation so that the signal amplitude
    is visible

    Parameters
    ----------
    channel : np.array
        The signal from 1 channel
    index : int
        The index placement of this channel (used to y-axis separate channels)
    thresh : float, optional
        If the standard deviation is less than this value, the channel is considered flat
    offset_factor : float, optional
        Determines how much y-axis separation is between two neighboring channels

    Returns
    -------
    The beautified eeg signal ready to plot
    """
    std = channel.std()
    offset = index * offset_factor
    if np.allclose(std, thresh):
        return channel - offset
    if use_detrend:
        channel = detrend(channel)
        std = channel.std() # get std again because detrending changes this value
    return (channel / std) - offset


def plot_eeg_channels(signal, dst, title, config):
    """
    Saves a plotly figure for all EEG channels in signal
    Parameters
    ----------
    signal : mne.io.cnt.cnt.RawCNT
        The raw EEG object to plot
    dst : str
        The location where to save the report
    title : str
        The title that will appear in the Plotly figure
    config : dict
        Configuration values given in `eegor/config.py`
    """
    # quicker plotly by resampling
    plot_downsample = config["plot_downsample"]
    # separate channels by tab
    max_channels = config["plot_max_channels"]

    fig = go.Figure()
    signal = signal.resample(plot_downsample)
    data   = signal.get_data()
    times = signal.times
    channels = signal.info["chs"]
    N = len(channels)

    for i, ch in enumerate(channels):
        y = pretty_eeg(data[i], i)
        name = ch["ch_name"]
        visible = 0 == i // max_channels
        fig.add_trace(
            go.Scatter(x=times, y=y, name=name, visible=visible)
        )

    # Set title
    fig.update_layout(title_text=title)

    # 64 channels is way too much so group the channels by `max_channel`
    # and switch between the groups with these buttons
    buttons = []
    for i in range(ceil(N / max_channels)):
        visibility = [i==(j // max_channels) for j in range(N)]
        start = max_channels * i
        end   = max_channels * (i + 1)
        label = f"Channels {start} to {end}"
        button = dict(
                     label = label,
                     method = "update",
                     args = [
                         {"visible": visibility},
                         {"title": label}
                         ]
                     )
        buttons.append(button)

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            # Darn, the `range` variable isn't working
            rangeslider={"visible": True, "range": [0, 30], "autorange": False},
        ),
        yaxis={"visible": False, "showticklabels": False},
        updatemenus=[go.layout.Updatemenu(buttons=buttons)]
    )
    fig.write_html(dst)

def plot_rejects(acq, ar_log, interval, dst, config):
    """
    Saves a plotly figure for all EEG channels in signal
    Parameters
    ----------
    acq: mne.io.cnt.cnt.RawCNT
        The preprocessed EEG object to plot
    ar_log : autoreject.autoreject.RejectLog
        The return object generated after running Autoreject
    interval : float
        The length of each epoch in seconds
    dst : str
        The location where to save the report
    config : dict
        Configuration values given in `eegor/config.py`

    Autoreject codes the status of channels/epochs in its return
    log instead of labeling them. The codes are currently
    {
        0: "good",
        1: "bad",
        2: "interpolated",
    }
    https://github.com/autoreject/autoreject/blob/c3f5a8186ed15fd7e16a4f44d36a3f22390ee2c4/autoreject/autoreject.py#L1226-L1228),
    """
    # quicker plotly by resampling
    plot_downsample = config["plot_downsample"]
    # separate channels by tab
    max_channels = config["plot_max_channels"]

    sampling = acq.info["sfreq"]
    tmp = acq.copy().resample(plot_downsample)
    data = tmp.get_data()
    times = tmp.times

    labels   = ar_log.labels
    channels = ar_log.ch_names
    bads     = ar_log.bad_epochs
    N1 = labels.shape[1]
    N2 = labels.shape[0]

    fig = go.Figure()
    for i, channel in tqdm(enumerate(channels), total=N1):
        signal = pretty_eeg(data[i], i)
        visible = 0 == i // max_channels
        for j, epoch in enumerate(labels[:, i]):
            indices = np.argwhere(np.logical_and(
                times > j * interval,
                times < (j+1)*interval)).flatten(
            )
            # needed to connect each epoch to the next
            indices = np.append(indices, [max(indices)+1, max(indices)+2])
            x = times[indices]
            y = signal[indices]
            if np.isnan(epoch) or bads[j]:
                color="red"
            else:
                color = {0: "black", 1: "red", 2: "gray"}[epoch]
            fig.add_trace(
                go.Scatter(x=x, y=y, name=channel, visible=visible, line=dict(color=color))
            )

    # 64 channels is way too much so group the channels by `max_channel`
    # and switch between the groups with these buttons
    buttons = []
    for i in range(ceil(N1 / max_channels)):
        visibility = [i==(j // max_channels) for j in range(N1) for _ in range(N2)]
        start = (max_channels * i) + 1
        end   = max_channels * (i + 1)
        label = f"Channels {start} to {end}"
        button = dict(
                     label = label,
                     method = "update",
                     args = [
                         {"visible": visibility},
                         {"title": label}
                         ]
                     )
        buttons.append(button)

    fig.update_layout(
        xaxis=dict(rangeslider={"visible": True}),
        yaxis={"visible": False, "showticklabels": False},
        updatemenus=[go.layout.Updatemenu(buttons=buttons)],
        showlegend=False
    )
    fig.write_html(dst)
