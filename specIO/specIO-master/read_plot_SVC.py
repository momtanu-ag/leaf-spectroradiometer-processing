# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 01:35:37 2021
Modified heavily on May 31 2024

@author: Sirapoom Peanusaha
@edits: Momtanu Chakraborty
"""

#%% Libraries 

# Import standard libraries and modules
import os
import sys
import pandas as pd
from natsort import natsorted

# Ensure the specIO module is correctly added to the system path
sys.path.insert(0, r"D:/UCDavis-grad/Research/Alireza/nitrogen/specIO/specIO-master")
import specIO as svc

#%% Helper functions

def get_refl(variable):
    """Function to extract reflectance data from an SVC file."""
    if variable is not None:
        reflectance = variable.refl
        return reflectance
    else:
        return None

#%% Importing data (Part 1)

# Insert main folder location
pot_loc = r'F:/svc/2023/Westwind/2023_May_westwind/new_files_cleaning/2023_05_24_westwind/sigfiles/sig'
folder_list = natsorted(os.listdir(pot_loc))

#%% Processing and concatenating reflectance data

refl_list = []
all_file_names = []

# Process each item in the directory
for item in folder_list:
    path = os.path.join(pot_loc, item)
    
    # Check if the current path is a directory or a file before processing
    if os.path.isdir(path):
        # Open and process each SVC file in the directory
        for file_name in natsorted(os.listdir(path)):
            full_file_path = os.path.join(path, file_name)
            temp_dat = svc.openSVC(full_file_path)
            temp_df = get_refl(temp_dat)
            if temp_df is not None:
                refl_list.append(temp_df)
            else:
                print(f"Failed to open file at path: {full_file_path}")
            all_file_names.append(file_name)
    elif os.path.isfile(path):
        # Handle the file directly if it's a file
        temp_dat = svc.openSVC(path)
        temp_df = get_refl(temp_dat)
        if temp_df is not None:
            refl_list.append(temp_df)
            all_file_names.append(item)
        else:
            print(f"Failed to open file at path: {path}")
    else:
        print(f"Invalid path: {path}")

# Convert list of DataFrames to a single DataFrame
refl_list_df = pd.concat(refl_list, axis=1).T

#%% Saving data to CSV

# Save the concatenated reflectance data
refl_list_df.to_csv(r'F:/svc/2023/Westwind/2023_May_westwind/new_files_cleaning/2023_05_24_westwind/csv/test/2023_may_westwind_spectra.csv')

# Save the file names
file_names_df = pd.DataFrame({'FileNames': all_file_names})
file_names_df.to_csv(r'F:/svc/2023/Westwind/2023_May_westwind/new_files_cleaning/2023_05_24_westwind/csv/test/2023_may_westwind_signames_1.csv', index=False)







