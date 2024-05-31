import pandas as pd, numpy as np
import os, datetime as dt
from .readSEraw import readSEraw
from scipy.interpolate import interp1d

######################################################################################################################################################
"""   ___      ___    ___     ___              ___   __   __   ___
     / __|    | _ \  | __|   / __|     o O O  | __|  \ \ / /  / _ \
     \__ \    |  _/  | _|   | (__     o       | _|    \ V /  | (_) |
     |___/   _|_|_   |___|   \___|   TS__[O]  |___|   _\_/_   \___/
"""
######################################################################################################################################################

"""The following functions and classes are used to parse out SPRECTRAL EVOLUTION spectral data
from .sed files, not all attributes are enabled."""

class SE(object):
    """Spec Evo spectral data object"""

    def __init__(self):
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""

        self.filename = np.nan
        self.instrument = np.nan
        self.detectorsVNIR=np.nan
        self.detectorsSWIR1=np.nan
        self.detectorsSWIR2=np.nan
        self.averagesR= np.nan
        self.averagesR= np.nan
        self.measurement=np.nan
        self.dateR=np.nan
        self.dateT=np.nan
        self.opticR= np.nan
        self.opticT= np.nan
        self.integVNIRR= np.nan
        self.integSWIR1R= np.nan
        self.integSWIR2R= np.nan
        self.integVNIRT= np.nan
        self.integSWIR1T= np.nan
        self.integSWIR2T= np.nan
        self.tempVNIRR= np.nan
        self.tempSWIR1R= np.nan
        self.tempSWIR2R= np.nan
        self.tempVNIRT= np.nan
        self.tempSWIR1T= np.nan
        self.tempSWIR2T= np.nan
        self.batteryR=np.nan
        self.batteryT=np.nan
        self.dark_modeR= np.nan
        self.dark_modeT= np.nan
        self.radiometric_calibration = np.nan
        self.units = np.nan
        self.timeT=  np.nan
        self.longitude= np.nan
        self.latitude=   np.nan
        self.altitude=  np.nan
        self.gpstime=  np.nan
        self.satellites=  np.nan
        self.channels= np.nan
        self.refr =  np.nan
        self.targ =  np.nan
        self.refl = np.nan

    def cycleRefl(self):


        for spectra in self.refl.iteritems():
            spectra.plot()
            plt.show()
            age = raw_input("Keep Data? (Y)es (N)o (C)ancel")

            if age =="Y":
                plt.close()
                continue
            elif age == "N":
                plt.close()
                print("Removed")
            elif age == "C":
                plt.close()
                break
            else:
                plt.close()
                print("Unrecognized input")
        return


    def changeColumnNames(self,byColumn):
        for key, value in self.__dict__.items():
            print(key)

    def resample(self,new_waves, kind = 'linear'):
        ''' resample reflectance data

        :param new_waves: list of new wavelengths to resample data to
        :param kind: interpolation type see scipy.interpolate.interp1d docs
        '''
        #create sampling object
        resampler = interp1d(self.refl.index, self.refl.T, kind= kind,bounds_error = False)
        #resample data
        resampled = resampler(new_waves)

        self.refl = pd.DataFrame(resampled.T,index= new_waves)



def populateSEClass(meta,refr,targ,refl):

    classObject = SE()

    classObject.filename = meta.filename
    classObject.instrument = meta.instrument
    classObject.detectorsVNIR=meta.detectorsVNIR
    classObject.detectorsSWIR1=meta.detectorsSWIR1
    classObject.detectorsSWIR1=meta.detectorsSWIR2
    classObject.measurement=meta.measurement
    classObject.dateR=meta.dateR
    classObject.dateT=meta.dateT
    classObject.averagesR= meta.averagesR
    classObject.averagesT= meta.averagesT
    classObject.opticR= meta.opticR
    classObject.opticT= meta.opticT
    classObject.integVNIRR= meta.integVNIRR
    classObject.integSWIR1R= meta.integSWIR1R
    classObject.integSWIR2R= meta.integSWIR2R
    classObject.integVNIRT= meta.integVNIRT
    classObject.integSWIR1T= meta.integSWIR1T
    classObject.integSWIR2T= meta.integSWIR2T
    classObject.tempVNIRR= meta.tempVNIRR
    classObject.tempSWIR1R= meta.tempSWIR1R
    classObject.tempSWIR2R= meta.tempSWIR2R
    classObject.tempVNIRT= meta.tempVNIRT
    classObject.tempSWIR1T= meta.tempSWIR1T
    classObject.tempSWIR2T= meta.tempSWIR2T
    classObject.batteryR=meta.batteryR
    classObject.batteryT=meta.batteryT
    classObject.dark_modeR= meta.dark_modeR
    classObject.dark_modeT= meta.dark_modeT
    classObject.radiometric_calibration = meta.radiometric_calibration
    classObject.units = meta.units
    classObject.channels= meta.channels
    classObject.refr =  refr
    classObject.targ =  targ
    classObject.refl = refl

    #classObject.longitude= meta.longitude
    #classObject.latitude=  meta.latitude
    #classObject.gpstime=  meta.gpstime

    return classObject



def SEspectraSeries(fullpathname,readRaw,normRaw):
    #this function take as input a single spectra and returns a pandas series

    #intitiate dictionary to hold spectral metadata
    metadata = {}

    #read spectral text file
    text = open(fullpathname,'r')

    #get filename
    metadata["filename"] = os.path.basename(fullpathname)

    #read first line
    line = text.readline().rstrip()

    #cycle through header data
    while "Wvl" not in line:


        if 'Instrument:' in line:
            #get instrument name
            line = line.split(":")
            metadata["instrument"] =  line[1]
            line = text.readline().rstrip()

        elif "Version" in line:
            line = line.split(":")
            metadata["version"] =  float(line[1])
            line = text.readline().rstrip()

        elif 'Integration:' in line:

            #split line
            line = line.split(":")
            line = line[1].split(",")
            #get reference VNIR integration time
            metadata["integVNIRR"] = float(line[0])
            #get reference SWIR1 integration time
            metadata["integSWIR1R"] =  float(line[1])
            #get reference SWIR2 integration time
            metadata["integSWIR2R"] =  float(line[2])
            #get target VNIR integration time
            metadata["integVNIRT"] =  float(line[3])
            #get target SWIR1 integration time
            metadata["integSWIR1T"] =  float(line[4])
            #get target SWIR2 integration time
            metadata["integSWIR2T"] = float(line[5])
            #read next line
            line = text.readline().rstrip()

        elif'Detectors:' in line:
            line = line.split(":")
            line = line[1].split(",")
            #get number of VNIR detectors
            metadata["detectorsVNIR"] =  int(line[0])
            #get number of SWIR1 detectors
            metadata["detectorsSWIR1"] =  int(line[1])
            #get number of SWIR2 detectors
            metadata["detectorsSWIR2"] =  int(line[2])
            #read next line
            line = text.readline().rstrip()

        elif 'Measurement:'  in line:
            #split line
            line = line.split(":")
            #get measurement type
            metadata["measurement"] =  line[1]
            #read next line
            line = text.readline().rstrip()

        elif 'Units:'  in line:
            #split line
            line = line.split(":")
            #get measurement units
            metadata["units"] =  line[1]
            #read next line
            line = text.readline().rstrip()

        elif'Channels:' in line:
            #split line
            line = line.split(":")
            #get number of channels
            metadata["channels"] =  float(line[1])
            #read next line
            line = text.readline().rstrip()


        elif'Foreoptic:'  in line:
            #check version
            if metadata["version"] == 2.2:
                #split line
                line = line.split(":")
                line = line[1].split(",")
                #get reference optic type
                metadata["opticR"] =  line[0]
                #get target optic type
                metadata["opticT"] =  line[1]

            else:
                line = line.split(",")
                #get reference optic type
                metadata["opticR"] =  line[0]
                #get target optic type
                metadata["opticT"] =  " ".join(line[1].split(":"))
            #read next line
            line = text.readline().rstrip()

        elif 'Temperature'  in line:
            #split line
            line = line.split(":")
            line = line[1].split(",")
            #get reference VNIR detector temperature
            metadata["tempVNIRR"] =  float(line[0])
            #get reference SWIR1 detector temperature
            metadata["tempSWIR1R"] = float(line[1])
            #get reference SWIR2 detector temperature
            metadata["tempSWIR2R"] =  float(line[2])
            #get target VNIR detector temperature
            metadata["tempVNIRT"] =  float(line[3])
            #get target SWIR1 detector temperature
            metadata["tempSWIR1T"] =  float(line[4])
            #get target SWIR2 detector temperature
            metadata["tempSWIR2T"] = float(line[5])
            #read next line
            line = text.readline().rstrip()

        elif'Battery'  in line:
            #split line
            line = line.split(":")
            line = line[1].split(",")
            #get reference battery voltage
            metadata["batteryR"] =  float(line[0])
            #get target battery voltage
            metadata["batteryT"] =  float(line[1])
            #read next line
            line = text.readline().rstrip()

        elif'Averages:'  in line:
            #split line
            line = line.split(":")
            line = line[1].split(",")
            #get number of samples averaged for reference measurement
            metadata["averagesR"] =  float(line[0])
            #get number of samples average for target measurement
            metadata["averagesT"] =  float(line[1])
            line = text.readline().rstrip()

        elif'Dark Mode:'  in line:
            #split line
            line = line.split(":")
            line = line[1].split(",")
            #get reference dark mode
            metadata["dark_modeR"] = line[0]
            #get target dark mode
            metadata["dark_modeT"] =  line[1]
            #read next line
            line = text.readline().rstrip()

        ################################################
        # Future development
        #########
        #elif'Longitude='   in line:
        #elif'Altitude='   in line:
        #elif'Latitude=' in line:
        #elif'GPS Time=' in line:
        #elif'Satellites='  in line:
        ################################################


        elif'Radiometric Calibration:' in line:
            #split line
            line = line.split(":")
            #get radiometric calibration type
            metadata["radiometric_calibration"] =  line[1]
            #read next line
            line = text.readline().rstrip()

        elif 'Time:' in line and "GPS" not in line:
            #split line
            line = line.split("e:")
            line = line[1].split(",")
            #get reference time
            timeR = line[0].strip()
            #get target time
            timeT = line[1]
            #read next line
            line = text.readline().rstrip()

        elif 'Date:' in line:
            #split line
            line = line.split(":")
            line = line[1].split(",")
            #get reference date
            dateR = line[0].strip()
            #get target date
            dateT = line[1]
            #read next line
            line = text.readline().rstrip()

        else:
            line = text.readline().rstrip()

    #combine target date and time into a datetime object
    metadata["dateT"] =  dt.datetime.strptime(dateT+timeT,"%m/%d/%Y%H:%M:%S.%f")

    #combine reference date and time into a datetime object
    metadata["dateR"] = dt.datetime.strptime(dateR+timeR,"%m/%d/%Y%H:%M:%S.%f")

    if readRaw:

            #load  metadata, reference, target and reflectance data into pandas series
            refrSeries,targSeries = readSEraw(fullpathname,metadata,normRaw)
            metaSeries = pd.Series(metadata.values(),index = metadata.keys())
            reflSeries = targSeries/refrSeries

    else:
    #read data from the .sed file

        #get the column names
        columns_names= line.split('\t')
        line = text.readline().rstrip()


        #change column names
        for i,column in enumerate(columns_names):
            if "Target" in column:
                columns_names[i] = "target"
            if ("Ref." in column) and ('Tgt.' not in column):
                columns_names[i] = "reference"
            if ("Reflect" in column) | (" Tgt./Ref. %"in column):
                columns_names[i] = "reflectance"

        #list to hold numerical data
        data= []

        #cycle through spectral data to end of file
        while line:

            #split line
            line = line.split('\t')
            data.append([float(x) for x in line])
            #read next line
            line = text.readline().rstrip()

        #populate a dataframe with the numerical data
        dataFrame = pd.DataFrame(data,columns = columns_names)
        #change datafram index to wavelength
        dataFrame.index = dataFrame.Wvl

        #load  metadata, reference, target and reflectance data into pandas series
        if "reflectance" not in columns_names:
            refrSeries = dataFrame["reference"]
            targSeries = dataFrame["target"]
            reflSeries = dataFrame["target"]/dataFrame["reference"]

        elif "reference" in columns_names:
            reflSeries = dataFrame["reflectance"]
            refrSeries = dataFrame["reference"]
            targSeries = dataFrame["target"]
        else:
            reflSeries = dataFrame["reflectance"]
            refrSeries = np.nan
            targSeries = np.nan

    #return data series;
    metaSeries = pd.Series(list(metadata.values()),index = metadata.keys())
    return metaSeries,refrSeries,targSeries,reflSeries



def openSE(foldORfile, readRaw = False, normRaw = True):
    #this function is used to open spectral datafiles Ocean Optics spectrometers.
    #It can take an input a folder or a single file. If a single file is input it will return
    # a pandas series, if a folder is input it will return a pandas dataframe containing all the spectra
    # This function assumes that all of the txt files containg in the folder are OO spectra.


    #if the input path is a file
    if os.path.isfile(foldORfile) and foldORfile.endswith(".sed"):
        #read spectral data
        meta,refr,targ,refl=  SEspectraSeries(foldORfile,readRaw,normRaw)
        #get a populated SE object
        SE =  populateSEClass(meta,refr,targ,refl)
        return SE

    #if the patgh is a folder
    elif os.path.isdir(foldORfile):

        #create empty dataframe to hold metadata
        metaDF = pd.DataFrame()
        #create empty dataframe to hold refrerence data
        refrDF = pd.DataFrame()
        #create empty dataframe to hold target data
        targDF = pd.DataFrame()
        #create empty dataframe to hold reflectance data
        reflDF = pd.DataFrame()
        #get list of txt files in the folder
        files = [txt for txt in os.listdir(foldORfile) if txt.endswith(".sed")]

        #cycle through each of the spectra
        for i,filename in enumerate(files):
            series = SEspectraSeries(foldORfile +filename,readRaw,normRaw)
            #load spectral data into a pandas series
            metaDF[i] = series[0]
            refrDF[i] = series[1]
            targDF[i] = series[2]
            reflDF[i] = series[3]

        #get a populated ASD object
        SE =   populateSEClass(metaDF.T,refrDF,targDF,reflDF)

        print("Loaded %s Spectral Evolution spectral files" % SE.refr.shape[1])
        return SE


    else:

        print("Pathname is neither a file nor a folder!!!!!")
        return









