# specIO

specIO (spectra Input/Ouput) is a python library for reading data files from number of spectrometer
manufacturers including ASD, Spectral Evolution, Spectral Vista Corp and Ocean Optics. This library
reads in a file or folder and parses all the data into a pandas dataframe. In addition to the actual
spectrum it also stores associated metadata for each file including battery voltage, integration, 
gain and offset much more!!! Metadata are especially useful for diagnosing data quality issues.

specIO primarily for reading files but contains a few processing options like jump correction for
the ASD and spectrum interpolation. Once the spectra are in a dataframe its easy to use packages
like [scipy](https://www.scipy.org/) and [scikit-learn](https://scikit-learn.org/stable/) for data
processing and analysis.

# Requirements
	- pandas
	- scipy
	- numpy
