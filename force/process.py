import numpy as np
import matplotlib.pyplot as plt


def filter_lowpass(data, freq, lowpass=30, plot=False):
    """
    Apply low pass filter to a recorded transducer signal (eg. force).

    :param data: data
    :type data: ndarray
    :param freq: sampling rate (Hz)
    :type freq: int
    :param lowpass: low pass cut-off
    :type lowpass: int
    :param plot: show plot of original and filtered data
    :type plot: bool
    :return: filtered data
    :rtype: ndarray
    """
    freq_nyq = freq/2
    high = lowpass/freq_nyq
    b, a = signal.butter(4, high, btype='low')
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


def calc_var(data):
    """
    Calculate standard deviation and coefficient of variation of a recorded transducer signal (eg. force).

    :param data: data
    :type data: ndarray
    :return: standard deviation and coefficient of variation
    :rtype: float
    """
    std_dev = np.std(data)
    cv = np.std(data) / np.mean(data)
    # print('Standard deviation (N): {:.3f}'.format(std_dev))
    # print('Coeff of variation: {:.3f}'.format(cv))
    return std_dev, cv

