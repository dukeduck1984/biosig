import numpy as np
from numpy import trapz


def find_index(f, lowpass, band_ll, band_ul):
    """
    Find the start and stop indices and values of a nominated frequency bandwith to calculate
    the proportion of spectral power for that bandwidth.
    This function requires a spectral analysis is first performed on the recorded signal.

    Example:
        import numpy as np
        import matplotlib.pyplot as plt
        from scipy import signal

        x = np.random.uniform(-1, 1, size=1000)
        x = filter_lowpass(x, 1000, 40)
        f, Pxx_den = signal.welch(x, 1000, nperseg=250)
        plt.plot(f, Pxx_den)
        start_idx, start_val, stop_idx, stop_val = find_index(f, 40, 8, 12)

    :param f: sample frequencies
    :type f: ndarray
    :param lowpass: low pass cut-off (Hz)
    :type lowpass: int
    :param band_ll: lower limit of bandwidth (Hz)
    :type band_ll: int
    :param band_ul: upper limit of bandwidth (Hz)
    :type band_ul: int
    :return: start and stop indices and values
    :rtype: int or float
    """
    def find_nearest(f, lowpass, limit):
        """
        In an array of frequencies, find the nearest index and value of the nominated frequency.

        :param f: sample frequencies (Hz)
        :type f: ndarray
        :param lowpass: low pass cut-off (Hz)
        :type lowpass: int
        :param limit: nominated frequency (Hz)
        :type limit: int
        :return: index and value
        :rtype: int or float
        """
        assert limit <= lowpass, 'Error: The nominated frequency is greater than the low pass cut-off'
        idx = (np.abs(f - limit)).argmin()
        return idx, f[idx]
    start_idx, start_val = find_nearest(f, lowpass, band_ll)
    stop_idx, stop_val = find_nearest(f, lowpass, band_ul)
    return start_idx, start_val, stop_idx, stop_val


def calc_percentpower(Pxx_den, start_idx, stop_idx):
    """
    Calculate proportion of spectral power in a recorded signal over a nominated frequency bandwidth.
    This function requires a spectral analysis is first performed on the recorded signal.

    Example:
        import numpy as np
        import matplotlib.pyplot as plt
        from scipy import signal

        x = np.random.uniform(-1, 1, size=1000)
        x = filter_lowpass(x, 1000, 40)
        f, Pxx_den = signal.welch(x, 1000, nperseg=250)
        plt.plot(f, Pxx_den)
        start_idx, start_val, stop_idx, stop_val = find_index(f, 40, 8, 12)
        percentpower = calc_percentpower(Pxx_den, start_idx, stop_idx)

    :param Pxx_den: power spectral density or power spectrum
    :type Pxx_den: ndarray
    :param start_idx: start index
    :type start_idx: int
    :param stop_idx: stop index
    :type stop_idx: int
    :return: percent of power
    :rtype: float
    """
    area_full = trapz(Pxx_den, dx=1)
    area_band = trapz(Pxx_den[start_idx: stop_idx], dx=1)
    percentpower = area_band / area_full * 100
    print('Proportion of power in bandwidth (%): {:.3f}'.format(percentpower))
    return percentpower


