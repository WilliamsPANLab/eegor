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

    for ch in range(max_channels):
        y = pretty_eeg(data[ch], ch)
        name = signal.info["chs"][ch]["ch_name"]
        fig.add_trace(
            go.Scatter(x=times, y=y, name=name)
        )

    # Set title
    fig.update_layout(
        title_text=title
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            # Darn, the `range` variable isn't working
            rangeslider={"visible": True, "range": [0, 30], "autorange": False},
        ),
        yaxis={'visible': False, 'showticklabels': False}
    )
    fig.write_html(dst)

