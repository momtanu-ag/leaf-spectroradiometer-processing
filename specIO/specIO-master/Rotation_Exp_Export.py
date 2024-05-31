# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 20:18:49 2021
This code will read and export the rotation experiment on 10_16_2021 into dataframe
@author: Sirapoom Peanusaha
"""

#import libraries
import os
import sys
sys.path.insert(0,r"C:\Users\si_si\Desktop\DA_code\specIO-master") # list path to the module location
import specIO as svc
import pandas as pd
import numpy as np

# make function to extract mean of wavebands by boundaries
def extractbound(df, lowb, upperb):
    summation = 0
    count = 0
    for i in range(len(df.index)):
        if df.index[i]>= lowb and df.index[i]<=upperb:
            summation = summation+df.iloc[i,0] # add value to the pot
            count = count+1
    print(summation)
    print(count)
    average = summation/count
    return(average)
            


# read data 
data_loc = 'C:/Users/si_si/Desktop/Data_DA/SVC/MATT_7_27/sig_only/temperature_matched/combined_data'

# read file names inside the main folder
file_list = os.listdir(data_loc)


list_filename = []
list_meta = []
list_rectime = []
list_refl = []
list_B = []
list_G = []
list_R = []
list_RE = []
list_NIR = []


# use for loop to extract data from each file and record it in a list

for i in range(len(file_list)):
    path = data_loc+'/'+file_list[i] # create path for each file
    temp_dat = svc.SVCspectraSeries(path) # open the file with SVCspectraSeries
    indi_meta = temp_dat[0] # this is whole meta data in tuple
    indi_name = temp_dat[0].filename # get file name
    indi_refl = temp_dat[3] # get reflectance in pandas series with index being wavelength
    indi_rectime = temp_dat[0].dateT # get the scan time
    
    
    # get reflectane in panda Series
    refl_frame = pd.DataFrame(indi_refl)
    
    # extract the average in each band we want 
    # B
    indi_B = extractbound(refl_frame, 434, 456)
    # G
    indi_G = extractbound(refl_frame, 544, 576)
    # R
    indi_R = extractbound(refl_frame, 634, 666)
    # RE
    indi_RE = extractbound(refl_frame, 714, 746)
    # NIR
    indi_NIR = extractbound(refl_frame, 814, 866)
    
    
    
    # append these data to the list
    list_filename.append(indi_name)
    list_meta.append(indi_meta)
    list_refl.append(indi_refl)
    list_rectime.append(indi_rectime)
    list_B.append(indi_B)
    list_G.append(indi_G)
    list_R.append(indi_R)
    list_RE.append(indi_RE)
    list_NIR.append(indi_NIR)
    
    
data = {'FileName':list_filename,
    'Meta_data':list_meta,
    'Reflectance':list_refl,
    'Record_time':list_rectime}

df = pd.DataFrame(data)



# More elaborated dataset
data_ver2 = {'FileName':list_filename,
    'Record_time':list_rectime,
    'Blue': list_B,
    'Green':list_G,
    'Red':list_R,
    'RedEdge':list_RE,
    'NIR':list_NIR
    }

df_ver2 = pd.DataFrame(data_ver2)

# OPTION 3 : ONLY EXPORT REFLECTANCE, FILENAMES AND RECORD TIME
data_ver3 = {
    'FileName':list_filename,
    'Record_time':list_rectime,
    }

df_ver3 = pd.DataFrame(data_ver3)

# convert reflectance list to dataframe
refl_df = pd.concat(list_refl, axis=1, keys=[s.name for s in list_refl]).transpose()
# set index to integer
refl_df = refl_df.reset_index(drop=True)
# concat the data_ver3 to reflectance_df
df_ver3 = pd.concat([df_ver3,refl_df],axis = 1)



# save dataset to xlsx
#df.to_excel("D:/SVC/RotationExperiment_10_16_2021/Temperature_matched/OutputXLSX/RotationExperiment_df_Version1.xlsx")

#df_ver2.to_excel("D:/SVC/RotationExperiment_10_16_2021/Temperature_matched/OutputXLSX/RotationExperiment_df_Version2.xlsx")


df_ver3.to_excel("C:/Users/si_si/Desktop/Data_DA/SVC/MATT_7_27/Potted_Vines_7_27_2021.xlsx")

    

    
    
    
    
    
    
    
    
# development trash #####################


# sample = 'D:/SVC/RotationExperiment_10_16_2021/Temperature_matched/Comined_datasets/0054_moc.sig' 

# raw = svc.openSVC(sample)
# raw3 = svc.SVCspectraSeries(sample)

# list_name = raw3[0].filename


# # create a for loop to record all the data

# mata = raw3[0]
# data = pd.DataFrame({'tuple':mata})
