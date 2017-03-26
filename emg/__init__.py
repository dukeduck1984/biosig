__all__ = ['process']

from biosig.emg import process

from biosig.emg.process import \
    remove_mean, filter_bandpass, rectify, \
    calc_halfwidth, find_mvc, calc_mvc, \
    calc_rms, calc_mean

