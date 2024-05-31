import pandas as pd, numpy as np, matplotlib.pyplot as plt
import os, datetime as dt,struct

def readSEraw(fullpathname,metadata,normRaw):

    #read in data from .raw files    
    print("Reading raw")
    
    #open the .raw file as a binary file
    rawFile =  os.path.splitext(fullpathname)[0] + ".raw"
    
    #check if the raw file exists, it most be located in the same directory as the .sed file and
    #must have the same basename
    if os.path.isfile(rawFile):
        
        with open(rawFile, 'rb') as f:
            #read the file
            sav = f.read()
     
            #get number of wavelength values         
            channels1 = struct.unpack("I", sav[:4])[0] 
                     
            #store number of channels in the metadata dictionary  
            metadata["channels"] = channels1     

            #list to hold wavelengths    
            wavelengths= []
           
            #cycle through data to get wavelengths
            for x in range(channels1):
                #get wavelength
                wavelength = struct.unpack("h", sav[4+(x*2): 4+(x*2)+2])[0] 
                #append wavelngth to wavelength list
                wavelengths.append(wavelength/10.)
        
            #calculate the start of the second channel length
            ch2_start =  4+ channels1*2 
                  
            #get number of reference values         
            channels2 = struct.unpack("i", sav[ch2_start:ch2_start+4])[0] 

            #list to hold reference DNs
            referenceDNs = []
            
            #cycle through data to get reference DNS
            for x in range(channels2):
                #get reference DN
                reference = struct.unpack("h", sav[ch2_start+(x*2): ch2_start+(x*2)+2])[0] 
                #append reference DN to list
                referenceDNs.append(reference)
            
            #calcualte the start of the third channel length
            ch3_start =    4 + ch2_start+ channels2*2
            
            #get number of target values         
            channels3  = struct.unpack("i", sav[ch3_start:ch3_start+4])[0] 

            #list to hold target DNs    
            targetDNs= []
            
            #cycle through data to get target DNs
            for x in range(channels3):
                #get target DN
                target = struct.unpack("h", sav[ch3_start+(x*2): ch3_start+(x*2)+2])[0] 
                #append target DN to list
                targetDNs.append(target)

            #normalize rawDN data
            if normRaw:      
                refNorm =   np.array([metadata["integVNIRR"] for x in range(metadata["detectorsVNIR"])] + \
                            [metadata["integSWIR1R"] for x in range(metadata["detectorsSWIR1"])] + \
                            [metadata["integSWIR2R"] for x in range(metadata["detectorsSWIR2"])])
                            
                targNorm =   np.array([metadata["integVNIRT"] for x in range(metadata["detectorsVNIR"])] + \
                            [metadata["integSWIR1T"] for x in range(metadata["detectorsSWIR1"])] + \
                            [metadata["integSWIR2T"] for x in range(metadata["detectorsSWIR2"])])
                
                referenceDNs = np.array(referenceDNs)/refNorm
                targetDNs =  np.array(targetDNs)/targNorm

            refrSeries = pd.Series(referenceDNs,index = wavelengths)
            targSeries = pd.Series(targetDNs,index = wavelengths)
        return refrSeries,targSeries
    
    else:
        print("Raw file for %s could not be found" % rawFile)    
        return