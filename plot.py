import os, shutil
import matplotlib.pyplot as plt


def set_details(path_raw='', path_proc='', sub='', trial='', signal=''):
    """
    Initialise dictionary of testing details.

	Example:
        path_raw = '/home/joanna/Dropbox/Projects/thisProject/data/raw/'
		path_proc = '/home/joanna/Dropbox/Projects/thisProject/data/proc/'
		sub = 'sub01'
		trial = 'NV_UL'
		signal = 'force'
		type = 'filt' # OR 'raw' OR 'powerspec'

    :param path_raw: file path to raw data
    :type path_raw: str
    :param path_proc: file path to processed data
    :type path_proc: str
    :param sub: subject ID
    :type sub: str
    :param trial: trial
    :type trial: str
	:param signal: signal
    :type signal: str
    :return: file paths to raw and processed data, subject ID, trial, condition type
    :rtype: dict
    """
    try:
        if not os.path.exists(path_proc + sub):
            os.mkdir(path_proc + sub)
    except FileNotFoundError:
        print('Error: Not enough information to create directory for processed data')
    details = {'path_raw': path_raw, 'path_proc': path_proc, 'sub': sub, 'trial': trial, 'signal': signal}
    return details


def save_plot(details=None, cond_type=''):
    """
    If testing details are passed, save plot in directory for processed data.
    Otherwise save plot in local directory.

    :param details: file paths to raw and processed data, subject ID, trial, signal
    :type details: dict
	:param cond_type: condition type (eg. raw, filt, powerspec)
    :type cond_type: str
    :return:
    :rtype:
    """
    if details and cond_type:
        # save figure to processed data directory
        plt.savefig(details['trial'] + '_' + details['signal'] + '_' + cond_type + '.png')
        plt.close()
        shutil.move(details['path_raw'] + details['sub'] + '/' + details['trial'] + '_'  + details['signal'] + '_'  + cond_type + '.png',
                    details['path_proc'] + details['sub'] + '/' + details['trial'] + '_'  + details['signal'] + '_'  + cond_type + '.png')
    else:
        # save figure to local directory
        plt.savefig('figure.png')
        plt.close()


def plot_raw(data, details=None, cond_type='raw'):
    """
    Plot raw data.
    If testing details are passed, plot is saved in directory for processed data.
    Otherwise plot is saved in local directory.

    :param data: data
    :type data: ndarray
    :param details: file paths to raw and processed data, subject ID, trial, signal
    :type details: dict
	:param cond_type: condition type
    :type cond_type: str
    :return:
    :rtype:
    """
    plt.clf()
    plt.close()
    fig = plt.figure()
    plt.plot(data)
    plt.xlabel('Sample')
    plt.ylabel('EMG (a.u.)')
    plt.tight_layout()
    save_plot(details, cond_type)


def plot_filt(data, data_filt, freq, details=None, cond_type='filt'):
    """
    Plot filtered data: short section and full trial.
    If testing details are passed, plot is saved in directory for processed data.
    Otherwise plot is saved in local directory.

    :param data: data
    :type data: ndarray
    :param data_filt: filtered data
    :type data_filt: ndarray
    :param freq: sampling rate (Hz)
    :type freq: int
    :param details: file paths to raw and processed data, subject ID, trial, condition type
    :type details: dict
	:param cond_type: condition type
    :type cond_type: str
    :return:
    :rtype:
    """
    plt.clf()
    fig = plt.figure()
    axes1 = fig.add_subplot(2, 1, 1)
    axes1.set_ylabel('EMG (a.u.), 1 sec')
    axes1.plot(data[0 : 1 * freq], label='raw')
    axes1.plot(data_filt[0 : 1 * freq], label='filtered')
    plt.locator_params(axis='x', nbins=5)
    plt.locator_params(axis='y', nbins=5)
    plt.axis('tight')
    plt.legend(loc='best')
    axes2 = fig.add_subplot(2, 1, 2)
    axes2.set_ylabel('EMG (a.u.), full')
    axes2.set_xlabel('Sample')
    axes2.plot(data)
    axes2.plot(data_filt)
    plt.locator_params(axis='x', nbins=5)
    plt.locator_params(axis='y', nbins=5)
    plt.axis('tight')
    plt.tight_layout()
    save_plot(details, cond_type)
    plt.close()


def plot_powerspec(f, Pxx_den, lowpass, details=None, cond_type='powerspec'):
    """
    Plot power spectrum of data.
    This function requires a power spectral density analysis is first performed on the recorded signal.
    If testing details are passed, plot is saved in directory for processed data.
    Otherwise plot is saved in local directory.

    Example:
        import numpy as np
        import matplotlib.pyplot as plt
        from scipy import signal

        x = np.random.uniform(-1, 1, size=1000)
        x = filter_lowpass(x, 1000, 40)
        f, Pxx_den = signal.welch(x, 1000, nperseg=250)
        plot_powerspec(f, Pxx_den, lowpass=500, details=None, cond_type='powerspec')

    :param f: sample frequencies
    :type f: ndarray
    :param Pxx_den: power spectrum of data
    :type Pxx_den: ndarray
    :param lowpass: lowpass cut-off (Hz)
    :type lowpass: int
    :param details: file paths to raw and processed data, subject ID, trial, condition type
    :type details: dict
	:param cond_type: condition type
    :type cond_type: str
    :return:
    :rtype:
    """
    plt.clf()
    fig = plt.figure(figsize=(11, 7))
    plt.plot(f, Pxx_den, 'k-o')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD [V**2/Hz]')
    plt.xlim((1, lowpass / 2))
    plt.ylim(0, Pxx_den.max())  # print(Pxx_den.max())
    plt.locator_params(axis='x', nbins=5)
    plt.locator_params(axis='y', nbins=5)
    plt.tight_layout()
    save_plot(details, cond_type)
    plt.close()


def plot_spectrogram(f, t, Sxx, ylim_ul, xmargin, toffset=0, details=None, cond_type='specgram'):
    """
    Plot spectrogram of data.
    This function requires a spectrogram analysis is first performed on the recorded signal.
    If testing details are passed, plot is saved in directory for processed data.
    Otherwise plot is saved in local directory.

    Example:
        import numpy as np
        import matplotlib.pyplot as plt
        from scipy import signal

        x = np.random.uniform(-1, 1, size=1000)
        x = filter_lowpass(x, 1000, 40)
        f, t, Sxx = signal.spectrogram(x, fs=1000, window='hamming', nperseg=256)
        plot_spectrogram(f, t, Sxx, ylim_ul=50, xmargin=2, toffset=2, details=None, cond_type='specgram')

    :param f: sample frequencies
    :type f: ndarray
    :param t: segment times
    :type t: ndarray
    :param Sxx: spectrogram of x. By default, the last axis of Sxx corresponds to the segment times.
    :type Sxx: ndarray
    :param ylim_ul: frequencies upper limit
    :type ylim_ul: int
    :param xmargin: time margin between event and upper or lower limit
    :type xmargin: int
    :param toffset: time offset from event
    :type toffset: int
    :param details: file paths to raw and processed data, subject ID, trial, condition type
    :type details: dict
    :param cond_type: condition type
    :type cond_type: str
    :return:
    :rtype:
    """
    plt.clf()
    fig, ax = plt.subplots(1, figsize=(11,7))
    t = t - toffset
    p = ax.pcolormesh(t, f, Sxx)
    fig.colorbar(p)
    plt.ylim((0, ylim_ul))
    plt.xlim((t - xmargin, t + xmargin))
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.locator_params(axis='x', nbins=5)
    plt.locator_params(axis='y', nbins=5)
    plt.tight_layout()
    save_plot(details, cond_type)
    plt.close()

