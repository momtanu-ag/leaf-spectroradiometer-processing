# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 01:42:32 2021

@author: si_si
"""


import specIO as svc

# filepath = r'C:/Users/si_si/Desktop/Data_DA/SVC_PottedVines/MATT_06_29_21_PV/Temperature_matched/P40/'

# df = svc.openSVC(filepath)

# list paths for each pot

p40 = r'C:/Users/si_si/Desktop/Data_DA/SVC_PottedVines/MATT_06_29_21_PV/Temperature_matched/P40/'
p41 = r'C:/Users/si_si/Desktop/Data_DA/SVC_PottedVines/MATT_06_29_21_PV/Temperature_matched/P41/'
p42 = r'C:/Users/si_si/Desktop/Data_DA/SVC_PottedVines/MATT_06_29_21_PV/Temperature_matched/P42/'
p43 = r'C:/Users/si_si/Desktop/Data_DA/SVC_PottedVines/MATT_06_29_21_PV/Temperature_matched/P43/'
p44 = r'C:/Users/si_si/Desktop/Data_DA/SVC_PottedVines/MATT_06_29_21_PV/Temperature_matched/P44/'
p45 = r'C:/Users/si_si/Desktop/Data_DA/SVC_PottedVines/MATT_06_29_21_PV/Temperature_matched/P45/'
p46 = r'C:/Users/si_si/Desktop/Data_DA/SVC_PottedVines/MATT_06_29_21_PV/Temperature_matched/P46/'
p47 = r'C:/Users/si_si/Desktop/Data_DA/SVC_PottedVines/MATT_06_29_21_PV/Temperature_matched/P47/'
p48 = r'C:/Users/si_si/Desktop/Data_DA/SVC_PottedVines/MATT_06_29_21_PV/Temperature_matched/P48/'

# read each data set

d40 = svc.openSVC(p40)
d41 = svc.openSVC(p41)
d42 = svc.openSVC(p42)
d43 = svc.openSVC(p43)
d44 = svc.openSVC(p44)
d45 = svc.openSVC(p45)
d46 = svc.openSVC(p46)
d47 = svc.openSVC(p47)
d48 = svc.openSVC(p48)

# extrct reflectance data
def getrefl(variable):
    reflectance = variable.refl
    return reflectance

# create data list
dat_list = [d40,d41,d42,d43,d44,d45,d46,d47,d48]
refl_list = []

# store dataframe of each pot in a list
for i in range(len(dat_list)):
    refl_list.append(getrefl(dat_list[i]))
    
    
# create function to extract data from 510-550 and 550-590 nm
def slice510590(df):
    # extract the data 
    extract = df.loc[510.5:590.2]
    # calculate the average of each pot
    emean = extract.mean(axis = 1)
    # calculate the heatmap
    head = emean.head(29)
    head_n = head.to_list()
    tail = emean.tail(29)
    tail_n = tail.to_list()
    # print(head)
    # print(tail)
    import numpy as np
    matrix = np.zeros((30,30))
    for i in range(len(tail_n)):
        for j in range(len(head_n)):
            matrix[i,j] = (tail_n[i] - head_n[j])/(tail_n[i]+head_n[j])
            #matrix[i,j] = head_n[j]
            #print(head.index[j])
            matrix[i+1, j] = head.index[j]
        matrix[i,j+1] = tail.index[i]
    return matrix
    

# plot matrix in color map 
attack = 8
prius = slice510590(refl_list[attack])
import matplotlib.pyplot as plt
no_wing = prius[:29,:29]
plt.imshow(no_wing, cmap = 'hot', interpolation = 'nearest', extent = [510.5,549.9,549.9,590.2])
plt.colorbar()
plt.title('Pot4'+str(attack))

