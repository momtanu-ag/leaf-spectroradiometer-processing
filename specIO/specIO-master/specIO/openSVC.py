import pandas as pd, numpy as np
import os, datetime as dt
from scipy.interpolate import interp1d


######################################################################################################################################################
"""  ___  __   __  ___   
    / __| \ \ / / / __|  
    \__ \  \ V / | (__   
    |___/  _\_/_  \___|
"""  
######################################################################################################################################################

"""The following functions and classes are used to parse out SVC spectral data
from .sig files, not all attributes are enabled."""

class SVC(object):
    """SVC spectral data object"""

    def __init__(self):
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
        
        self.filename = np.nan               
        self.instrument = np.nan       
        self.scan_methodR=np.nan       
        self.scan_methodT=np.nan       
        self.coaddVNIRR=np.nan      
        self.coaddSWIR1R=np.nan       
        self.coaddSWIR2R=np.nan   
        self.coaddVNIRT=np.nan       
        self.coaddSWIR1T=np.nan      
        self.coaddSWIR2T=np.nan
        self.scan_timeR= np.nan   
        self.scan_timeT= np.nan       
        self.scan_settingR= np.nan       
        self.scan_settingT=np.nan       
        self.external_data_set1= np.nan       
        self.external_data_set2= np.nan       
        self.external_data_dark= np.nan       
        self.external_data_mask= np.nan       
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
        self.errorR= np.nan    
        self.errorT = np.nan    
        self.unitsR= np.nan    
        self.unitsT = np.nan    
        self.timeR= np.nan    
        self.timeT=  np.nan    
        self.longitude= np.nan                                
        self.latitude=   np.nan                                    
        self.gpstime=  np.nan                              
        self.comm=  np.nan    
        self.memory_slotR= np.nan    
        self.memory_slotT= np.nan    
        self.factors= np.nan    
        self.refr =  np.nan
        self.targ =  np.nan
        self.refl = np.nan
        self.detector = np.nan
    

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
        


def populateSVCClass(meta,reference,target,reflectance):
    """ This function creates an SVC class and populates it with supplied
    metadata and spectral data in.
    
    :type metadata: pandas series or dataframe
    :param metadata: Spectr(a/um) metadata
         
    :type reference: pandas series or dataframe
    :param reference: Reference DNs or radiance 
        
    :type target: pandas series or dataframe
    :param target: Target DNs or radiance 
        
    :type reflectance: pandas series or dataframe
    :param reflectance: Reflectance
        
    :return: A populated asdClass with metadata and spectra 
    :rtype asdClass   
    """
    
    svcClass = SVC()
    
    svcClass.filename = meta.filename                
    svcClass.instrument = meta.instrument       
    svcClass.scan_methodR= meta.scan_methodR    
    svcClass.scan_methodT=meta.scan_methodT        
    svcClass.coaddVNIRR=meta.coaddVNIRR       
    svcClass.coaddSWIR1R=meta.coaddSWIR1R        
    svcClass.coaddSWIR2R=meta.coaddSWIR2R    
    svcClass.coaddVNIRT=meta.coaddVNIRT       
    svcClass.coaddSWIR1T=meta.coaddSWIR1T        
    svcClass.coaddSWIR2T=meta.coaddSWIR2T
    svcClass.scan_timeR= meta.scan_timeR    
    svcClass.scan_timeT= meta.scan_timeT       
    svcClass.scan_settingR= meta.scan_settingT       
    svcClass.scan_settingT=meta.scan_settingT        
    svcClass.external_data_set1= meta.external_data_set1       
    svcClass.external_data_set2= meta.external_data_set2        
    svcClass.external_data_dark= meta.external_data_dark       
    svcClass.external_data_mask= meta.external_data_mask        
    svcClass.opticR= meta.opticR        
    svcClass.opticT= meta.opticT
    svcClass.integVNIRR= meta.integVNIRR
    svcClass.integSWIR1R= meta.integSWIR1R
    svcClass.integSWIR2R= meta.integSWIR2R
    svcClass.integVNIRT= meta.integVNIRT
    svcClass.integSWIR1T= meta.integSWIR1T
    svcClass.integSWIR2T= meta.integSWIR2T        
    svcClass.tempVNIRR= meta.tempVNIRR
    svcClass.tempSWIR1R= meta.tempSWIR1R
    svcClass.tempSWIR2R= meta.tempSWIR2R
    svcClass.tempVNIRT= meta.tempVNIRT
    svcClass.tempSWIR1T= meta.tempSWIR1T
    svcClass.tempSWIR2T= meta.tempSWIR2T      
    svcClass.batteryR=meta.batteryR       
    svcClass.batteryT=meta.batteryT       
    svcClass.errorR= meta.errorR        
    svcClass.errorT = meta.errorT       
    svcClass.unitsR= meta.unitsR   
    svcClass.unitsT= meta.unitsT      
    svcClass.dateR= meta.dateR     
    svcClass.dateT=  meta.dateT     
    svcClass.memory_slotR= meta.memory_slotR
    svcClass.memory_slotT= meta.memory_slotT
    svcClass.refr =  reference
    svcClass.targ =  target
    svcClass.refl = reflectance
    #svcClass.factors= meta.
    #svcClass.longitude= meta.                                  
    #svcClass.latitude=   meta.                                       
    #svcClass.gpstime=  meta.                      
    #svcClass.comm=  meta.
    

    return svcClass

def SVCspectraSeries(fullpathname):
    #this function take as input a single spectra and return a pandas series 
    #list to holde spectral data    
    
    #initiate metadat lise
    metadata = [[],[]]    

    #read spectral text file
    text = open(fullpathname,'r')
    
    #get file name
    metadata[0].append("filename")
    metadata[1].append(os.path.basename(fullpathname))
    
    #read next line
    line = text.readline().rstrip()

    #cycle through header data
    while "data=" not in line:
        
        if 'instrument=' in line:
            
            #split line
            line = line.split("=")
            
            #get instrument name
            metadata[0].append(line[0])
            metadata[1].append(line[1])
            
            #read next line
            line = text.readline().rstrip()
            
        elif 'integration=' in line:
            
            #split line
            line = line.split("=")
            line = line[1].split(",")
            
            #get reference VNIR integration time
            metadata[0].append("integVNIRR")
            metadata[1].append(float(line[0]))
            
            #get reference SWIR1 integration time
            metadata[0].append("integSWIR1R")
            metadata[1].append(float(line[1]))
            
            #get reference SWIR2 integration time
            metadata[0].append("integSWIR2R")
            metadata[1].append(float(line[2]))
            
            #get target VNIR integration time
            metadata[0].append("integVNIRT")
            metadata[1].append(float(line[3]))
            
            #get target SWIR1 integration time
            metadata[0].append("integSWIR1T")
            metadata[1].append(float(line[4]))
            
            #get target SWIR2 integration time
            metadata[0].append("integSWIR2T")
            metadata[1].append(float(line[5]))
            
            #read next line
            line = text.readline().rstrip()
            
        elif'scan method=' in line:
            
            #split line
            line = line.split("=")
            line = line[1].split(",")

            #get reference scan method
            metadata[0].append("scan_methodR")
            metadata[1].append(line[0])
            
            #get target scan method 
            metadata[0].append("scan_methodT")
            metadata[1].append(line[1])

            #read next line
            line = text.readline().rstrip()


        elif'scan coadds=' in line:
            
            #split line
            line = line.split("=")
            line = line[1].split(",")
            
            #get reference VNIR coadd
            metadata[0].append("coaddVNIRR")
            metadata[1].append(float(line[0]))
            
            #get reference SWIR1 coadd
            metadata[0].append("coaddSWIR1R")
            metadata[1].append(float(line[1]))
            
            #get reference SWIR2 coadd
            metadata[0].append("coaddSWIR2R")
            metadata[1].append(float(line[2]))
            
            #get target VNIR coadd
            metadata[0].append("coaddVNIRT")
            metadata[1].append(float(line[3]))
            
            #get target SWIR1 coadd
            metadata[0].append("coaddSWIR1T")
            metadata[1].append(float(line[4]))
            
            #get target SWIR2 coadd
            metadata[0].append("coaddSWIR2T")
            metadata[1].append(float(line[5]))
        
            #read next line
            line = text.readline().rstrip()
            
            
        elif'scan time=' in line:
            
            #split line
            line = line.split("=")
            line = line[1].split(",")
            
            #get reference scan time
            metadata[0].append("scan_timeR")
            metadata[1].append(float(line[0]))
            
            #get target scan time
            metadata[0].append("scan_timeT")
            metadata[1].append(float(line[1]))
            
            #move to next line
            line = text.readline().rstrip()
            
        elif'scan settings=' in line:
            
            #split line
            line = line.split("=")
            line = line[1].split(",")
            
            #get reference scan setting
            metadata[0].append("scan_settingR")
            metadata[1].append(line[0])
            
            #get target scan setting
            metadata[0].append("scan_settingT")
            metadata[1].append(line[1])
            
            #read next line
            line = text.readline().rstrip()
            
            
        elif'external data set1='  in line:
            
            #split line
            line = line.split("=")
            
            #get external dataset 1
            metadata[0].append("external_data_set1")
            metadata[1].append(line[1])
            
            #read next line
            line = text.readline().rstrip()
            
        elif'external data set2='  in line:
            
            #split line
            line = line.split("=")
            
            #get external dataset 2
            metadata[0].append("external_data_set2")
            metadata[1].append(line[1])
            
            #read next line
            line = text.readline().rstrip()
            
        elif'external data dark=' in line:
            
            #split line
            line = line.split("=")
            
            #get external dark data
            metadata[0].append("external_data_dark")
            metadata[1].append(line[1])
            
            #read next line
            line = text.readline().rstrip()
            
        elif 'external data mask=' in line:
            
            #split line
            line = line.split("=")
            
            #get external data mask
            metadata[0].append("external_data_mask")
            metadata[1].append(line[1])
            
            #read next line
            line = text.readline().rstrip()
        
        elif'optic='  in line:
            
            #split line
            line = line.split("=")
            line = line[1].split(",")
            
            #get reference optic
            metadata[0].append("opticR")
            metadata[1].append(line[0])
            
            #get target optic
            metadata[0].append("opticT")
            metadata[1].append(line[1])
            
            #read next line
            line = text.readline().rstrip()
            
        elif'temp='  in line:
            
            #split line
            line = line.split("=")
            line = line[1].split(",")
            
            #get VNIR detector reference temperature
            metadata[0].append("tempVNIRR")
            metadata[1].append(float(line[0]))
            
            #get SWIR1 detector reference temperature
            metadata[0].append("tempSWIR1R")
            metadata[1].append(float(line[1]))
            
            #get SWIR2 detector reference temperature
            metadata[0].append("tempSWIR2R")
            metadata[1].append(float(line[2]))
            
            #get VNIR detector target temperature
            metadata[0].append("tempVNIRT")
            metadata[1].append(float(line[3]))
            
            #get SWIR1 detector target temperature
            metadata[0].append("tempSWIR1T")
            metadata[1].append(float(line[4]))
            
            #get SWIR2 detector target temperature
            metadata[0].append("tempSWIR2T")
            metadata[1].append(float(line[5]))
            
            #read next line
            line = text.readline().rstrip()
            
            
        elif'battery='  in line:
            
            #split line
            line = line.split("=")
            line = line[1].split(",")
            
            #get reference battery voltage
            metadata[0].append("batteryR")
            metadata[1].append(line[0])
            
            #get target batter voltage
            metadata[0].append("batteryT")
            metadata[1].append(line[1])
            
            #read next line
            line = text.readline().rstrip()
            
        elif'error='  in line:
            
            #split line
            line = line.split("=")
            line = line[1].split(",")
            
            #get reference error
            metadata[0].append("errorR")
            metadata[1].append(float(line[0]))
            
            #get target error
            metadata[0].append("errorT")
            metadata[1].append(float(line[1]))
            
            #read next line
            line = text.readline().rstrip()
            
        elif'units='  in line:
            
            #split line
            line = line.split("=")
            line = line[1].split(",")
            
            #get reference units
            metadata[0].append("unitsR")
            metadata[1].append(line[0])
            
            #get target units
            metadata[0].append("unitsT")
            metadata[1].append(line[1])
            
            #read next line
            line = text.readline().rstrip()
            
        elif 'time=' in line and "scan" not in line and "gps" not in line:
            
            #split line
            line = line.split("=")
            line = line[1].split(",")
            
            #get reference date
            metadata[0].append("dateR")
            metadata[1].append(dt.datetime.strptime(line[0]," %m/%d/%Y %H:%M:%S%p"))
            
            #get target data
            metadata[0].append("dateT")
            metadata[1].append(dt.datetime.strptime(line[1]," %m/%d/%Y %H:%M:%S%p"))
            
            #read next line
            line = text.readline().rstrip()
            
        ##########################################
        #For future developement
        #####   
        #elif'longitude='   in line:             
        #elif'latitude=' in line:               
        #elif'gpstime=' in line:                
        #elif'comm='  in line:
        #elif'factors=' in line: 
        ##########################################
            
            
        elif'memory slot=' in line:
            
            #split line
            line = line.split("=")
            line = line[1].split(",")
            
            #get reference memory slot
            metadata[0].append("memory_slotR")
            metadata[1].append(float(line[0]))
            
            #get target memory slot
            metadata[0].append("memory_slotT")
            metadata[1].append(float(line[1]))
            
            #read next line
            line = text.readline().rstrip()
    
        else:     
            #read next line 
            line = text.readline().rstrip()  
    
    #move to first line of spectral data
    line = text.readline().rstrip()      
            
    #initiate lists to hold spectral data     
    spectraRefr = [[],[]]  
    spectraTarg = [[],[]]
    spectraRefl = [[],[]]       
    
    #cycle through spectral data                        
    while line:
        
        #split line
        line = line.split('  ')
        
        #append wavelength data to reference, target and reflectance lists
        spectraRefr[0].append(float(line[0]))
        spectraTarg[0].append(float(line[0]))
        spectraRefl[0].append(float(line[0]))

        #append spectral data to reference, target and reflectance lists           
        spectraRefr[1].append(float(line[1]))
        spectraTarg[1].append(float(line[2]))
        spectraRefl[1].append(float(line[3]))
        
        #read next line
        line = text.readline().rstrip()
        
    #load  metadata, reference, target and reflectance data into pandas series
    metaSeries = pd.Series(metadata[1],index = metadata[0])
    refrSeries = pd.Series(spectraRefr[1],index = spectraRefr[0])
    targSeries = pd.Series(spectraTarg[1],index = spectraTarg[0])
    reflSeries = pd.Series(spectraRefl[1],index = spectraRefl[0])
    
    return metaSeries,refrSeries,targSeries,reflSeries
        


def openSVC(foldORfile):
    #this function is used to open spectral datafiles SVCspectrometers. 
    #It can take an input a folder or a single file. If a single file is input it will return
    # a pandas series, if a folder is input it will return a pandas dataframe containing all the spectra



    #if the input path is a file
    if os.path.isfile(foldORfile):

        meta,refr,targ,refl=  SVCspectraSeries(foldORfile)
        
        SVC =  populateSVCClass(meta,refr,targ,refl)
        
        return SVC

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
        files = [txt for txt in os.listdir(foldORfile) if txt.endswith(".sig")]
        
        #cycle through each of the spectra
        for i,filename in enumerate(files): 

            series = SVCspectraSeries(foldORfile +filename)
        
            #load spectral data into a pandas series
            metaDF[i] = series[0]
            refrDF[i] = series[1]
            targDF[i] = series[2]
            reflDF[i] = series[3]
                        
        
        SVC =   populateSVCClass(metaDF.T,refrDF,targDF,reflDF)
        
        print("Loaded %s SVC spectral files" % SVC.refr.shape[1])
        return SVC
        
        
    else:
        print("Pathname is neither a file nor a folder!!!!!")
        return
        
        
