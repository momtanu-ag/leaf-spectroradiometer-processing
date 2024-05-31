import pandas as pd, numpy as np
import os, datetime as dt,struct



######################################################################################################################################################
""" ___     ___     ___   
   /   \   / __|   |   \  
   | - |   \__ \   | |) | 
   |_|_|   |___/   |___/  

"""
######################################################################################################################################################                                                                                                                                                                                                    
"""The following functions and classes are used to parse out ASD spectral data
from .asd files, not all attributes are enabled."""

class ASD(object):
    """ASD spectral data object"""

    def __init__(self):
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
        
        self.filename = np.nan               
        self.instrument = np.nan       
        self.comments = np.nan       
        self.averagesD= np.nan       
        self.averagesR= np.nan       
        self.averagest= np.nan       
        self.measurement=np.nan       
        self.dateD=np.nan       
        self.dateR=np.nan               
        self.dateT=np.nan               
        self.opticFOV= np.nan       
        self.integVNIR= np.nan       
        self.gainSWIR1= np.nan       
        self.gainSWIR2= np.nan       
        self.offsetSWIR1= np.nan       
        self.offsetSWIR2= np.nan
        self.darkCorrected=  np.nan 
        self.darkValue=  np.nan 
        self.longitude= np.nan                                   
        self.latitude=   np.nan       
        self.altitude=  np.nan                                      
        self.gpstime=  np.nan   
        self.splice1=  np.nan                                      
        self.splice2=  np.nan       
        self.refr =  np.nan
        self.targ =  np.nan
        self.refl = np.nan

def populateASDClass(meta,refr,targ,refl):
    
    classObject = ASD()
    classObject.filename = meta.filename
    #classObject.instrument = meta.intrument
    classObject.comments = meta.comments
    classObject.averagesD= meta.averagesD
    classObject.averagesR= meta.averagesR
    classObject.averagest= meta.averagesT
    classObject.dateD=meta.dateD
    classObject.dateR=meta.dateR         
    classObject.dateT=meta.dateT
    classObject.opticFOV= meta.opticFOV
    classObject.integVNIR= meta.integVNIR
    classObject.gainSWIR1= meta.gainSWIR1
    classObject.gainSWIR2= meta.gainSWIR2
    classObject.offsetSWIR1= meta.offsetSWIR1
    classObject.offsetSWIR2= meta.offsetSWIR2
    classObject.darkCorrected=  meta.darkCorrected
    classObject.darkValue=  meta.darkValue
    classObject.splice1=  meta.splice1
    classObject.splice2=  meta.splice2                     
    classObject.channels= meta.channels
    classObject.refr =  refr
    classObject.targ =  targ
    classObject.refl = refl
    #classObject.longitude= meta.longitude            
    #classObject.latitude=  meta.latitude
    #classObject.gpstime=  meta.gpstime 
    
    
    return classObject

fullpathname = "/Users/adam/Dropbox/test.asd"

def ASDspectraSeries(fullpathname,jump_correct):
    #this function take as input a single spectra and return a pandas series 
    
    #intitiate list to hold spectral metadata    
    metadata = [[],[]]    

    #open asd binary file
    with open(fullpathname, 'rb') as f:
        asdbinary = f.read()
        
    #append filename    
    metadata[0].append("filename")
    metadata[1].append(os.path.basename(fullpathname))

    #get the file version
    fileversion = b"".join(struct.unpack("ccc", asdbinary[0:(0 + 3)]))
    fileversion = fileversion.decode("utf-8")
    #get the time of the target measurement
    second = struct.unpack('h', asdbinary[160:(160 + 2)])[0]
    minute = struct.unpack('h', asdbinary[162:(162 + 2)])[0]
    hour = struct.unpack('h', asdbinary[164:(164 + 2)])[0]
    day = struct.unpack('h', asdbinary[166:(166 + 2)])[0]
    month = struct.unpack('h', asdbinary[168:(168 + 2)])[0] +1
    year = 1900 + struct.unpack('h', asdbinary[170:(170 + 2)])[0]
    dateT = dt.datetime(year,month,day,hour,minute, second)
    metadata[0].append("dateT")
    metadata[1].append(dateT)
    
    #get dark current time (seconds since Jan 1 1970)
    darkSeconds =struct.unpack('I', asdbinary[182:(182 + 4)])[0]
    dateD = dt.datetime(1970,1,1,0,0, 0) + dt.timedelta(0,darkSeconds)
    metadata[0].append("dateD")
    metadata[1].append(dateD)
    
    #get reference time (seconds since Jan 1 1970)
    refSeconds =struct.unpack('I', asdbinary[187:(187 + 4)])[0]
    dateR = dt.datetime(1970,1,1,0,0, 0) + dt.timedelta(0,refSeconds)
    metadata[0].append("dateR")
    metadata[1].append(dateR)

    #comments
    comments = struct.unpack('c'*157, asdbinary[3:(3 + 157)])[0]
    metadata[0].append("comments")
    metadata[1].append(comments)

    #instrument number
    number = str(struct.unpack("H", asdbinary[400:(400 + 2)])[0])
    metadata[0].append("instrumentNumber")
    metadata[1].append(number)

    #instrument model 
    model = struct.unpack("B", asdbinary[431:(431 + 1)])[0]
    metadata[0].append("instrumentModel")
    metadata[1].append(model)
    
    #SWIR1 detector settings
    metadata[0].append("gainSWIR1")
    gainSwir1 = float(struct.unpack("H", asdbinary[436:(436 + 2)])[0])
    metadata[1].append(gainSwir1)
    metadata[0].append("offsetSWIR1")
    offsetSWIR1 = float(struct.unpack("H", asdbinary[440:(440 + 2)])[0])
    metadata[1].append(offsetSWIR1)
    
    #SWIR1 detector settings
    metadata[0].append("gainSWIR2")
    gainSwir2 = float(struct.unpack("H", asdbinary[438:(438 + 2)])[0])
    metadata[1].append(gainSwir2)
    metadata[0].append("offsetSWIR2")
    offsetSWIR2 = float(struct.unpack("H", asdbinary[442:(442 + 2)])[0])
    metadata[1].append(offsetSWIR2)        
    
    #VNIR detector settings
    metadata[0].append("integVNIR")
    integVNIR  = float(struct.unpack("I", asdbinary[390:(390 + 4)])[0])
    metadata[1].append(integVNIR)
    
    #foreoptic FOV setting
    metadata[0].append("opticFOV")
    foreoptic  = float(struct.unpack("h", asdbinary[394:(394 + 2)])[0])
    metadata[1].append(foreoptic)
            
    #Dark correction applied?
    dark = struct.unpack("B", asdbinary[181:(181 + 1)])[0]
    metadata[0].append("darkCorrected")
    if dark == 1:
        metadata[1].append(True)
    else:
        metadata[1].append(True)
        
    #dark correction value
    darkval = struct.unpack("H", asdbinary[396:(396 + 2)])[0]
    metadata[0].append("darkValue")
    metadata[1].append(darkval)
    
    #Number of dark spectra averaged 
    darkCounts = struct.unpack("H", asdbinary[425:(425 + 2)])[0]
    metadata[0].append("averagesD")   
    metadata[1].append(darkCounts)   
    
    #Number of reference spectra averaged 
    refCounts = struct.unpack("H", asdbinary[427:(427 + 2)])[0]
    metadata[0].append("averagesR")   
    metadata[1].append(refCounts)                
        
    #Number of targets average
    targCounts = struct.unpack("H", asdbinary[429:(429 + 2)])[0]
    metadata[0].append("averagesT")   
    metadata[1].append(targCounts)    
    
    #get splice1 wavelength VNIR - SWIR1
    splice1 = struct.unpack("f", asdbinary[444:(444 + 4)])[0]
    metadata[0].append("splice1")   
    metadata[1].append(splice1)  
    
    #get splice1 wavelength VNIR - SWIR1
    splice2 = struct.unpack("f", asdbinary[448:(448 + 4)])[0]
    metadata[0].append("splice2")   
    metadata[1].append(splice2)  
    
    #number of channels
    numchannels = struct.unpack("h", asdbinary[204:(204 + 2)])[0]
    metadata[0].append("channels")   
    metadata[1].append(numchannels)  
        
    #retrieve wavelength data
    ###########################################    
    
    #starting wavelength     
    wavestart = struct.unpack("f", asdbinary[191:(191 + 4)])[0]
    
    #step wavelength
    wavestep = struct.unpack("f", asdbinary[195:(195 + 4)])[0]
    
    #data format
    data_format = struct.unpack("B", asdbinary[199:(199 + 1)])[0]    
    
    #format string to unpack target and reference values
    fmt = "f"*numchannels  
                               
    if data_format == 2:
        fmt = 'd'*numchannels
    if data_format == 0:
        fmt = 'f'*numchannels

    #ending wavelength
    wavestop = wavestart + numchannels*wavestep - 1
    
    #create wavelength array
    waves = np.linspace(wavestart, wavestop, numchannels)

    #date size
    size = numchannels*8
    
    if fileversion == 'ASD':
        #get reflectance data
        reflectance = np.array(struct.unpack(fmt, asdbinary[484:(484 + size)]))  
        refrSeries =np.nan
        targSeries =np.nan

    if fileversion == 'as7':
        #get reference and target data
        start = 484 + size
        first, last = start + 18, start + 20
        ref_desc_length = struct.unpack('H', asdbinary[first:last])[0]
        first = start + 20 + ref_desc_length
        last = first + size
        reference = np.array(struct.unpack(fmt, asdbinary[first:last]))
        
        target = np.array(struct.unpack(fmt, asdbinary[484:(484 + size)]))
        refrSeries = pd.Series(reference,index = waves)
        targSeries = pd.Series(target,index = waves)  
        
        #calculate reflectance
        reflectance = target/reference
              
    #load  data into a pandas series
    metaSeries = pd.Series(metadata[1],index = metadata[0])
    reflSeries = pd.Series(reflectance,index = waves)
    
    #apply jump correction to reflectance data
    if jump_correct == True:
        reflSeries.loc[350:metaSeries.splice1]  =reflSeries.loc[350:metaSeries.splice1+1] +  (reflSeries[metaSeries.splice1+1] - reflSeries[metaSeries.splice1])
        reflSeries.loc[metaSeries.splice2+1:2500]  =reflSeries.loc[metaSeries.splice2+1:2500] +  (reflSeries[metaSeries.splice2] - reflSeries[metaSeries.splice2+1])
    
    
    
    return metaSeries,targSeries,refrSeries,reflSeries
        


def openASD(foldORfile,jump_correct = False):
    #this function is used to open spectral datafiles ASD spectrometers. 
    #It can take an input a folder or a single file. If a single file is input it will return
    # a pandas series, if a folder is input it will return a pandas dataframe containing all the spectra


    #if the input path is a file
    if os.path.isfile(foldORfile) and (foldORfile.endswith(".asd") or foldORfile.endswith(".ASD")):

        #read spectral file
        meta,refr,targ,refl=  ASDspectraSeries(foldORfile,jump_correct)
        
        #get a populated ASD object
        ASD =  populateASDClass(meta,refr,targ,refl)
        
        return ASD

    #if the path is a folder    
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
        files = [txt for txt in os.listdir(foldORfile) if (txt.endswith(".asd") or txt.endswith(".ASD"))]
        
        #cycle through each of the spectra
        for i,filename in enumerate(files): 

            #read spectral file
            series = ASDspectraSeries(foldORfile +filename,jump_correct)
            
            #load spectral data into a pandas series
            metaDF[i] = series[0]
            refrDF[i] = series[1]
            targDF[i] = series[1]
            reflDF[i] = series[3]
                        
        #get a populated ASD object
        ASD =   populateASDClass(metaDF.T,refrDF,targDF,reflDF)
        
        print("Loaded %s ASD spectral files" % ASD.refr.shape[1])
        return ASD
        
        
    else:
        print("Pathname is neither a file nor a folder!!!!!")
        return
