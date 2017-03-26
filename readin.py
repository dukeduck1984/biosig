import os
import numpy as np
import warnings


def read_data(file, channels={}):
    """
    Read in data from a data text file.
    Data from each channel are stored in columns. Values are tab-separated.
    The function requires a dictionary of channel keys and values to be specified.
    Channel columns are zero-indexed.

    Example:
        channels = {'force':0, 'emg':1, 'distance':2}
        data = read_data('V_L.txt', channel=channels)

    :param file: file name
    :type file: str
    :param channels: dictionary of channel keys and values
    :type channels: dict
    :return: dictionary of channel keys and values
    :rtype: dict
    """
    infile = open(file, 'r')
    lines = infile.readlines()
    infile.close()
    data_list = [row.strip().split('\t') for row in lines]
    data_dict = {}
    if channels:
        for k,v in channels.items():
            data_dict[k] = np.array([float(row[v]) for row in data_list])
        # update dictionary to return free variables in function block using keys
        locals().update(data_dict)
        return data_dict
    else:
        warnings.warn('Dictionary of channel keys and values was not specified')
        pass


def make_time(freq, var):
    """
    Create time (sec) based on sampling rate.

    :param freq: sampling rate (Hz)
    :type freq: int
    :param var: channel values
    :type var: ndarray
    :return: time (sec)
    :rtype: ndarray
    """
    step = 1 / freq
    time = np.arange(0, len(var)/freq, step)
    return time


def read_log(file):
    """
    Template to read in data from a log text file.
    This function will require editing to customise output for each experiment.

    :param file: file name
    :type file: str
    :return: values from log file
    :rtype: int or float
    """
    infile = open(file, 'r')
    lines = infile.readlines()
    infile.close()
    for row in lines:
        var = row.strip().split(' ')
        if var[0]=='subject' and var[1]=='number':
            id = var[2]
        elif var[0]=='transducer' and var[1]=='1' and var[2]=='calibration:':
            scale1 = float(var[3])
        elif var[0]=='transducer' and var[1]=='2' and var[2]=='calibration:':
            scale2 = float(var[3])
        elif var[0]=='sampling' and var[1]=='rate:':
            freq = int(var[2])
        elif var[0]=='age:':
            age = int(var[1])
        elif var[0]=='sex:':
            sex = var[1]
        elif var[0]=='height:':
            height = float(var[1]) # meters
        elif var[0]=='weight:':
            weight = float(var[1]) # kg
    return id, scale1, scale2, freq, age, sex, height, weight


def calibrate(data, scale, offset):
    """
    Remove offset and calibrate raw voltage to meaningful values.

    :param data: uncalibrated data
    :type data: ndarray
    :param scale: calibration scale
    :type scale: float
    :param offset: calibration offset
    :type offset: float
    :return: calibrated data
    :rtype: ndarray
    """
    data = (data - offset) * scale
    return data

