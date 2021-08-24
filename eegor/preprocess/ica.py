import mne


def ica(epochs, config):
    seed = config["seed"]
    N = config["num_ica_components"]
    ica = mne.preprocessing.ICA(n_components=N, max_iter="auto",
                                random_state=seed)
    ica.fit(epochs)
    ica.plot_sources(epochs, show_scrollbars=True)
