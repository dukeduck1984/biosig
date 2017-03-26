BIOLOGICAL AND TRANSDUCER SIGNAL PROCESSING
=

This Python package provides functions to process and plot biological (EMG) and transducer (force) signals. 

This package will be extended over time to include functions to process other types of signals, and improve ease of package installation.

Version 1.0 [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.438155.svg)](https://doi.org/10.5281/zenodo.438155) 

### Citation and license

If this code is used to analyse data or generate figures for publication, please cite the code as:

Diong J (2017) Biological and transducer signal processing in Python. DOI: 10.5281/zenodo.438155.

This code is released under the GNU General Public License. 

### Installation

Clone or download the `biosig` repository to the local computer, and point Python to the location where `biosig` is stored. For example:

```python
import sys

sys.path.append("/home/joanna/Dropbox/Sketchbook/python/")
import biosig
```

Note, filepaths are specified differently in: 

* Linux or Mac: `"/home/joanna/Dropbox/Sketchbook/python/"` 
* Windows: `"C:\\Users\\joanna\\Dropbox\\Sketchbook\\python\\"`

### Description

File structure:

* biosig
	* emg
		* process
	* force
		* process
	* plot
	* readin
	* spectral

### Dependencies

* matplotlib
* numpy
* os
* scipy
* shutil
* sys
* warnings

### Short example of usage

Supply a dictionary of names and data values.
Read in the raw data, where data are stored in columns in a text file. 
Remove DC offset, band pass filter the EMG data, and calculate the root-mean-square (RMS) EMG.

```python
import sys

sys.path.append("/home/joanna/Dropbox/Sketchbook/python/")
import biosig

channels = {'force':0, 'emg':1, 'distance':2}
data = biosig.readin.read_data('data.txt', channel=channels)
emg = data['emg']
emg = biosig.emg.process.remove_mean(emg)
emg_filt = biosig.emg.process.filter_bandpass(emg, fq=2000, highpass=30, lowpass=500)
rms_emg = biosig.emg.process.calc_rms(emg, fq=2000, window=50, plot=True) 
```

### Acknowledgements

With thanks to [Martin Héroux](https://github.com/MartinHeroux) for contributions to the RMS EMG functions.

### References

Merletti R and Parker P (2004) [Electromyography : physiology, engineering, and noninvasive applications.]((http://onlinelibrary.wiley.com/book/10.1002/0471678384)) John Wiley & Sons & Wiley InterScience (Online Service); Piscataway, NJ : IEEE Press, Hoboken, NJ. 

