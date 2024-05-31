import pandas as pd, numpy as np, matplotlib.pyplot as plt
import os, datetime as dt,struct

######################################################################################################################################################
""" ___    ___    ___    ___   _  _            ___     ___  _____   ___    ___    ___   
   / _ \  / __|  | __|  /   \ | \| |    o O O / _ \   | _ \|_   _| |_ _|  / __|  / __|  
  | (_) || (__   | _|   | - | | .` |   o     | (_) |  |  _/  | |    | |  | (__   \__ \  
   \___/  \___|  |___|  |_|_| |_|\_|  TS__[O] \___/  _|_|_  _|_|_  |___|  \___|  |___/  

"""
######################################################################################################################################################

"""The following functions and classes are used to parse out Ocean Optics spectral data
from .TXT files, not all attributes are enabled."""

class OO(object):
    """Ocean Optics spectral data object"""

    def __init__(self):
        
        self.filename = np.nan
        
        self.date = np.nan
                
        self.instrument = np.nan

        self.integration_time= np.nan
        
        self.auto_integration= np.nan
        
        self.trigger_mode = np.nan
        
        self.scans_averaged= np.nan
        
        self.nonlinearity_correction = np.nan
        
        self.boxcar_width= np.nan
        
        self.stray_light_correction=  np.nan
                                
        self.xaxis_mode=  np.nan
        
        self.stop_averaging = np.nan
        
        self.dark_spectrum_stored= np.nan
        
        self.number_pixels= np.nan

        self.tar= np.nan

        self.refr= np.nan

        self.refl= np.nan



def populateOOClass(meta,targ):
    
    classObject = OO()
    
    classObject.filename = meta.filename
    classObject.date = meta.date                                
    classObject.instrument = meta.instrument       
    classObject.integration_time= meta.integration_time    
    classObject.auto_integration=meta.auto_integration        
    classObject.trigger_mode=meta.trigger_mode       
    classObject.scans_averaged=meta.scans_averaged        
    classObject.nonlinearity_correction=meta.nonlinearity_correction    
    classObject.boxcar_width=meta.boxcar_width    
    if "stray_light_correction" in meta:     
        classObject.stray_light_correction=meta.stray_light_correction        
    classObject.xaxis_mode=meta.xaxis_mode
    classObject.stop_averaging= meta.stop_averaging    
    classObject.number_pixels= meta.number_pixels 
    if "dark_spectrum_stored" in meta:  
        classObject.dark_spectrum_stored= meta.dark_spectrum_stored    
    classObject.targ =  targ


    return classObject


def OOspectraSeries(fullpathname):
    #this function take as input a single spectra and return a pandas series 
    #list to hold spectral data    
    
    metadata = [[],[]]    

    text = open(fullpathname,'r')
    
    metadata[0].append("filename")
    metadata[1].append(os.path.basename(fullpathname))
    line = text.readline().rstrip()

    while "Begin Spectral Data" not in line:
        
        if 'Spectrometer' in line:
            
            line = line.split(":")
            metadata[0].append("instrument")
            metadata[1].append(line[1])
            line = text.readline().rstrip()
            
        elif "Date" in line:
            
            line = line.split()
            metadata[0].append("date")
            
            #remove the "Date:" and the timezone from the list
            line.remove(line[0])
            line.remove(line[4])
            line = "-".join(line)
            date = dt.datetime.strptime(line,"%a-%b-%d-%H:%M:%S-%Y")
            metadata[1].append(date)
            line = text.readline().rstrip()

            
        elif 'Autoset integration time' in line:
            
            line = line.split(":")
            metadata[0].append("auto_integration")
            
            if line[1] == "false":
                metadata[1].append(False)
            else:
                metadata[1].append(True)
            
            line = text.readline().rstrip()
            
        elif'Trigger' in line:
            
            line = line.split(":")
            metadata[0].append("trigger_mode")
            metadata[1].append(line[1])
            line = text.readline().rstrip()


        elif 'Integration Time (sec)' in line:
            
            line = line.split(":")
            metadata[0].append("integration_time")
            metadata[1].append(float(line[1]))
            line = text.readline().rstrip()
            
        elif 'Scans to average' in line:
            
            line = line.split(":")
            metadata[0].append("scans_averaged")
            metadata[1].append(float(line[1]))
            line = text.readline().rstrip()
            
        elif'Nonlinearity' in line:
            
            line = line.split(":")
            metadata[0].append("nonlinearity_correction")
           
            if line[1] == "false":
                metadata[1].append(False)
            else:
                metadata[1].append(True)
            
            line = text.readline().rstrip()
            
        elif'Boxcar'  in line:
            
            line = line.split(":")
            metadata[0].append("boxcar_width")
            metadata[1].append(float(line[1]))
            
            line = text.readline().rstrip()
            
        elif 'Stray' in line:
            
            line = line.split(":")
            
            metadata[0].append("stray_light_correction")
            
            if line[1] == "false":
                metadata[1].append(False)
            else:
                metadata[1].append(True) 
                
            line = text.readline().rstrip() 
            
        elif'XAxis'  in line:
            line = line.split(":")
            metadata[0].append("xaxis_mode")
            metadata[1].append(line[1])
            line = text.readline().rstrip()
            
        elif'Stop averaging' in line:
            line = line.split(":")
            
            metadata[0].append("stop_averaging")
            
            if line[1] == "false":
                metadata[1].append(False)
            else:
                metadata[1].append(True)
                
            line = text.readline().rstrip()
            
        elif 'Storing dark spectrum' in line:
            
            line = line.split(":")
            metadata[0].append("dark_spectrum_stored")
            
            if line[1] == "false":
                metadata[1].append(False)
            else:
                metadata[1].append(True)
        
            line = text.readline().rstrip()
        
        elif'Number of Pixels in Spectrum'  in line:
            
            line = line.split(":")
            metadata[0].append("number_pixels")
            metadata[1].append(float(line[1]))
            line = text.readline().rstrip()
             
        else:      
            line = text.readline().rstrip()  
    
    #move to first line of spectral data
    line = text.readline().rstrip()      
            
    #lists to hold spectral data     
    #spectraRefr = [[],[]]  
    spectraTarg = [[],[]]
    #spectraRefl = [[],[]]       
                
    while line:
        line = line.split()
        
        #spectraRefr[0].append(float(line[0]))
        spectraTarg[0].append(float(line[0]))
        #spectraRefl[0].append(float(line[0]))
        
        #spectraRefr[1].append(float(line[1]))
        spectraTarg[1].append(float(line[1]))
        #spectraRefl[1].append(float(line[3]))
        
        line = text.readline().rstrip()
        
    #load  data into a pandas series'
    metaSeries = pd.Series(metadata[1],index = metadata[0])
    #refrSeries = pd.Series(spectraRefr[1],index = spectraRefr[0])
    targSeries = pd.Series(spectraTarg[1],index = spectraTarg[0])
    #reflSeries = pd.Series(spectraRefl[1],index = spectraRefl[0])
    
    return metaSeries,targSeries
        


def openOO(foldORfile):
    #this function is used to open spectral datafiles Ocean Optics spectrometers. 
    #It can take an input a folder or a single file. If a single file is input it will return
    # a pandas series, if a folder is input it will return a pandas dataframe containing all the spectra
    # This function assumes that all of the txt files containg in the folder are OO spectra.


    #if the input path is a file
    if os.path.isfile(foldORfile) and foldORfile.endswith(".txt"):

        meta,targ=  OOspectraSeries(foldORfile)
        
        OO =  populateOOClass(meta,targ)
        
        return OO

    #if the patgh is a folder    
    elif os.path.isdir(foldORfile):

        #create empty dataframe to hold metadata
        metaDF = pd.DataFrame()
        
        #create empty dataframe to hold refrerence data
        #refrDF = pd.DataFrame()
        
        #create empty dataframe to hold target data
        targDF = pd.DataFrame()
        
        #create empty dataframe to hold reflectance data
        #reflDF = pd.DataFrame()

        #get list of txt files in the folder
        files = [txt for txt in os.listdir(foldORfile) if txt.endswith(".txt")]
        
        #cycle through each of the spectra
        for i,filename in enumerate(files): 

            series = OOspectraSeries(foldORfile +filename)
        
            #load spectral data into a pandas series
            metaDF[i] = series[0]
            #refrDF[i] = series[1]
            targDF[i] = series[1]
            #reflDF[i] = series[3]
                        
        
        OO =  populateOOClass(metaDF.T,targDF)
        
        print("Loaded %s Ocean Optics spectral files" % OO.targ.shape[1])
        return OO
        
        
    else:
        print("Pathname is neither a file nor a folder!!!!!")
        return
