from math import ceil
import numpy as np
import plotly.graph_objects as go
from scipy.signal import detrend

def pretty_eeg(channel, index, thresh=1e-16, offset_factor=4):
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
    """
    std = channel.std()
    offset = index * offset_factor
    if np.allclose(std, thresh):
        return channel - offset
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
                     label = label
                     method = 'update',
                     args = [
                         {'visible': visibility},
                         {'title': label}
                         ]
                     )
        buttons.append(button)

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            # Darn, the `range` variable isn't working
            rangeslider={"visible": True, "range": [0, 30], "autorange": False},
        ),
        yaxis={'visible': False, 'showticklabels': False},
        updatemenus=[go.layout.Updatemenu(buttons=buttons)]
    )
    fig.write_html(dst)
