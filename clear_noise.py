# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 09:10:39 2023
SVC functions

@author: Hamid
@edits: Momtanu
"""
import numpy as np
from scipy.interpolate import interp1d
import pandas as pd



def SVC_sig_cleanup(sig):   
    """
    

    Parameters
    ----------
    sig : svc reflectance or transmistance data
    

    Returns
    It returns a signal with 1 nm resolution with interpolation and cleans up over laps
    400-2500 nm

    """
    sig.index = sig.index.astype('float64')
    wave_lengths=sig.index.copy()

  


    
    dis=[]
    for i in range(len(wave_lengths)-1):
        
        
        if wave_lengths[i+1]<wave_lengths[i]:
            dis.append(i)
            
    A=wave_lengths[:dis[0]+1]
    B=wave_lengths[dis[0]+1:dis[1]+1]
    C=wave_lengths[dis[1]+1:]
    
    
    cut_band=[]    
    for wave_band in dis:
        
        low_nir=pd.to_numeric(wave_lengths[wave_band-30:wave_band])
        high_nir=pd.to_numeric(wave_lengths[wave_band+1:wave_band+20])
        
        wave_overlap=sig.loc[sig.index > wave_lengths[wave_band+1]]
        wave_overlap=wave_overlap.loc[wave_overlap.index < wave_lengths[wave_band]]
        wave_overlap.index = pd.to_numeric(wave_overlap.index, errors='coerce')
        start_wl_overlap=np.floor(min(wave_overlap.index))
        end_wl_overlap=np.ceil(max(wave_overlap.index))
        window_size=5
        
        tresh=100
        for wind in np.arange(start_wl_overlap,end_wl_overlap,window_size):
            lw=low_nir[low_nir>wind] 
            lw=lw[lw<wind+window_size]
            lwa=sig[lw].mean()
            
            hi=high_nir[high_nir>wind] 
            hi=hi[hi<wind+window_size]
            
            hia=sig[hi].mean()
            
            if abs(lwa-hia)<tresh:
                tresh=abs(lwa-hia)
                cut_band_temp=np.mean(lw)
        
        cut_band.append(cut_band_temp)
    
    
    A_cut=A[(A<cut_band[0]) & (A>=399)]
    B_cut=B[(B>cut_band[0]) & (B<cut_band[1])]
    C_cut=C[(C>cut_band[1]) & (C <= 2505)]
    
    ABC=A_cut
    ABC=ABC.union(B_cut)
    ABC=ABC.union(C_cut)
    
    cleaned_sig=sig[ABC]
    
    return cleaned_sig


def interpolateSVCSpectrum(cleaned_sig,wl_range=[400,2500]):
    df_spectrum=cleaned_sig
    wl = df_spectrum.index
    spec = df_spectrum.values
    f = interp1d(wl, spec)
    
    wl_new = range(wl_range[0],wl_range[1]+1)
    spec_new = f(wl_new)
    df_s = pd.DataFrame(spec_new, index=wl_new)
    
    return df_s

df = pd.read_csv(r'F:/svc/2023/Westwind/2023_May_westwind/new_files_cleaning/2023_05_24_westwind/csv/test/2023_may_westwind_spectra.csv')
df = df.transpose() 
df = df.iloc[1:, :]
# Create an empty DataFrame to store cleaned samples
cleaned_samples_df = pd.DataFrame()

# Iterate over columns in the original DataFrame
for col_name, col_data in df.items():
    # Apply the cleanup function to the spectral data in the column
    cleaned_data = SVC_sig_cleanup(col_data)
    interpolated_df = interpolateSVCSpectrum(cleaned_data)
    # Add the cleaned data as a new column to the cleaned_samples_df
    cleaned_samples_df[col_name] = interpolated_df
    

# Save the cleaned samples to a new CSV file
cleaned_samples_df.to_csv(r'F:/svc/2023/Westwind/2023_May_westwind/new_files_cleaning/2023_05_24_westwind/csv/test/2023_may_westwind_spectra_interpolated.csv', index=False)