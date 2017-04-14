import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def remove_mean(data, plot=False):
    """
    Remove the mean from a recorded signal.

    :param data: data
    :type data: ndarray
    :param plot: show plot of original and mean-removed data
    :type plot: bool
    :return: data with mean removed
    :rtype: ndarray
    """
    data_removedmean = data - np.mean(data)
    if plot:
        plt.clf()
        plt.close()
        plt.plot(data, label='original')
        plt.plot(data_removedmean, label='removed mean')
        plt.legend(loc='best')
        plt.show()
    else:
        pass
    return data_removedmean


def filter_bandpass(data, freq, highpass=30, lowpass=500, plot=False):
    """
    Apply bandpass filter to a recorded signal (usually EMG).

    :param data: data
    :type data: ndarray
    :param freq: sampling rate (Hz)
    :type freq: int
    :param highpass: high pass cut-off (Hz)
    :type highpass: int
    :param lowpass: low pass cut-off (Hz)
    :type lowpass: int
    :param plot: show plot of original and filtered data
    :type plot: bool
    :return: filtered data
    :rtype: ndarray
    """
    freq_nyq = freq/2
    high, low = highpass/freq_nyq, lowpass/freq_nyq
    b, a = signal.butter(4, [high, low], btype='bandpass')
    data_filt = signal.filtfilt(b, a, data)
    if plot:
        plt.clf()
        plt.close()
        plt.plot(data, label='original')
        plt.plot(data_filt, label='filtered')
        plt.legend(loc='best')
        plt.show()
    else:
        pass
    return data_filt


def rectify(data, plot=False):
    """
    Rectify a recorded signal (usually EMG) to get absolute values.

    :param data: data
    :type data: ndarray
    :param plot: show plot of original and rectified data
    :type plot: bool
    :return: rectified data
    :rtype: ndarray
    """
    data_rect = abs(data)
    if plot:
        plt.clf()
        plt.close()
        plt.plot(data, label='original')
        plt.plot(data_rect, label='rectified')
        plt.legend(loc='best')
        plt.show()
    else:
        pass
    return data_rect


def find_mvc(data, plot=False):
    """
    Find index and value of MVC EMG.

    :param data: data
    :type data: ndarray
    :param plot: show plot of data and MVC value
    :type plot: bool
    :return: index and value at MVC EMG or force
    :rtype: int or float
    """
    mvc_value = np.max(data)
    mvc_index = int(np.where(data == mvc_value)[0][0])
    if plot:
        plt.clf()
        plt.close()
        plt.plot(data)
        plt.plot(mvc_index, mvc_value, 'ro')
        plt.show()
    else:
        pass
    return mvc_index, mvc_value


def calc_halfwidth(freq, window):
    """
    For a given window of time (ms), calculate half of the window width (samples).

    :param freq: sampling rate (Hz)
    :type freq: int
    :param window: window of time (ms)
    :type window: int
    :return: half of the window width (samples)
    :rtype: int
    """
    halfwidth = round((window / 1000) / 2 * freq)
    return halfwidth


def calc_mvc(data, mvc_index, mvc_value, freq, window, type='rms', plot=False):
    """
    Calculate average MVC EMG using the root-mean-square ('rms')
    or using the mean over a window of time across the peak EMG ('mean').

    :param data: data
    :type data: ndarray
    :param mvc_index: index at MVC EMG or force
    :type mvc_index: int
    :param mvc_value: value of MVC EMG or force
    :type mvc_value: float
    :param freq: sampling rate (Hz)
    :type freq: int
    :param window: window of time (ms)
    :type window: int
    :param type: mean or rms
    :type type: str
    :param plot: show plot of data and window across peak EMG
    :type plot: bool
    :return: MVC EMG
    :rtype: float
    """
    halfwidth = calc_halfwidth(freq, window)
    if type == 'rms':
        mvc = np.sqrt(np.mean((data[mvc_index - halfwidth : mvc_index + halfwidth]) ** 2))
    elif type == 'mean':
        mvc = np.mean(data[mvc_index - halfwidth : mvc_index + halfwidth])
    if plot:
        plt.clf()
        plt.close()
        plt.plot(data)
        plt.plot([mvc_index - halfwidth, mvc_index + halfwidth],
                 [mvc_value + (mvc_value/10), mvc_value + (mvc_value/10)],
                 'r-', linewidth=4)
        plt.show()
    else:
        pass
    return mvc


def calc_rms(data, freq, window, plot=False):
    """
    Process a recorded signal (usually EMG) using a moving root-mean-square window.

    Example:
        import numpy as np
        import matplotlib.pyplot as plt
        data = np.random.rand(10000,1)
        freq, window = 2000, 50
        data_rms = calc_rms(data, freq, window)
        plt.plot(data)
        plt.plot(data_rms)
        plt.show()

    :param data: data
    :type data: ndarray
    :param freq: sampling rate (Hz)
    :type freq: int
    :param window: window of time (ms)
    :type window: int
    :param plot: show plot of original and rms data
    :type plot: bool
    :return: RMS data
    :rtype: ndarray
    """
    halfwidth = calc_halfwidth(freq, window)
    # Initialise variable.
    data_rms = np.zeros(data.size)
    # Loop through and compute normalised moving window.
    # Window is smaller at the start and the end of the signal.
    for i in range(data.size - 1):
        if i < halfwidth:
            data_rms[i] = np.sqrt(np.mean((data[0 : i + halfwidth]) ** 2))
        elif i > data.size - halfwidth:
            data_rms[i] = np.sqrt(np.mean((data[i - halfwidth : data.size - 1]) ** 2))
        else:
            data_rms[i] = np.sqrt(np.mean((data[i - halfwidth : i + halfwidth]) ** 2))
    if plot:
        plt.clf()
        plt.close()
        plt.plot(data, label='original')
        plt.plot(data_rms, 'r-', label='rms')
        plt.legend(loc='best')
        plt.show()
    else:
        pass
    return data_rms


def calc_mean(data, mvc, freq, window, plot=False):
    """
    Process a recorded signal (usually EMG) using a moving average normalised to MVC.

    Example:
        import numpy as np
        import matplotlib.pyplot as plt
        data = np.random.rand(10000,1)
        freq, window = 2000, 50
        data_mean = calc_mean(data, mvc, freq, window)
        plt.plot(data)
        plt.plot(mean_data)
        plt.show()

    :param data: data
    :type data: ndarray
    :param mvc: MVC EMG
    :type mvc: float
    :param freq: sampling rate (Hz)
    :type freq: int
    :param window: window of time (ms)
    :type window: int
    :param plot: show plot of original (V) and mean (%MVC) data
    :type plot: bool
    :return: mean data (% MVC)
    :rtype: ndarray
    """
    halfwidth = calc_halfwidth(freq, window)
    # Initialise variable.
    data_mean = np.zeros(data.size)
    # Loop through and compute normalised moving window.
    # Window is smaller at the start and the end of the signal.
    for i in range(data.size - 1):
        if i < halfwidth:
            data_mean[i] = np.mean(data[0: i + halfwidth]) / mvc * 100
        elif i > data.size - halfwidth:
            data_mean[i] = np.mean(data[i - halfwidth: data.size - 1]) / mvc * 100
        else:
            data_mean[i] = np.mean(data[i - halfwidth: i + halfwidth]) / mvc * 100
    if plot:
        plt.clf()
        plt.close()
        fig, ax1 = plt.subplots()
        ax1.plot(data, 'b-')
        ax1.set_xlabel('sample')
        ax1.set_ylabel('V', color='b')
        ax1.tick_params('y', colors='b')
        # plot two y-axes on same x-axis
        ax2 = ax1.twinx()
        ax2.plot(data_mean, 'r-')
        ax2.set_ylabel('%MVC', color='r')
        ax2.tick_params('y', colors='r')
        fig.tight_layout()
        plt.show()
    else:
        pass
    return data_mean


"""
if __name__ == '__main__':
    import sys

print usage
print example
"""


