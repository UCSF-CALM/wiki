# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 15:13:15 2022

@author: Jan.Frankowski
"""
from easygui import *
try:
    import h5py
except ImportError:
    print("Install h5py using the following command in the terminal: pip install h5py")
    
try:
    import tifffile
except ImportError:
    print("Install tifffile using the following command in the terminal: pip install tifffile")
    
try:
    import numpy
except ImportError:
    print("Install numpy using the following command in the terminal: pip install numpy")
    
try:
    import tkinter
except ImportError:
    print("Install tkinter using the following command in the terminal: pip install tkinter")   
    
try: 
    import natsort
except ImportError:
    print("Install natsort using the following command in the terminal: pip install natsort")   

import os
import numpy as np
from tifffile import imwrite
from tkinter import Tk, filedialog
import glob
import time
from natsort import natsorted

#%%

msgbox(""" Jan C. Frankowski, Ph.D. - Jan.Frankowski@Bruker.com
      This script creates maximum intensity projections from a series of luxdata .h5 files. 
      This script is for raw data only. When prompted, type a response and press Enter to proceed.
      
      You will be prompted for:
          - A folder containing raw .lux.h5 files.
          - A folder to save exported .tif files.
          - The name of the camera (eg. Long, short, left, right etc).
          - Whether to slice the Z series, if so, the start and end planes. (starting at 0).
          - Option to project along Z, Y, or X axes.
          
    The script will report each file being read, the file being written, and the estimated time
    remaining.
      """)

#%% define input and output folder
root = Tk()
root.withdraw()
root.attributes('-topmost', True)

#prompt for directory of .h5 files
h5_folder = filedialog.askdirectory(title="Select folder containing .h5 files.")
print("Selected directory of .h5 files: " + h5_folder)

#prompt for directory to output .tif files
output_folder = filedialog.askdirectory(title="Select folder to output .tif files.")
print("Selected directory of output .tif files: " + output_folder)

#%% parse the filename to get the cam name

h5_file_list = glob.glob(os.path.join(h5_folder, '*.lux.h5'))
#sort in natural order
h5_file_list = natsorted(h5_file_list)

#%% find unique cam names within the folder containing .lux.h5 files

unique_filenames = []

for filename in h5_file_list:
    h5_file_parsed = filename.split('_')
    cam_name = h5_file_parsed[-2]
    if cam_name not in unique_filenames:
        unique_filenames.append(cam_name)
      
#%% prompt for which cam name
      
cam_choices = unique_filenames
cam_reply = buttonbox("Select the data to process:", choices=cam_choices)

#%%
#prompt for output name
output_name = enterbox("Type a name for the output .tif file series:")

#%% check length of .h5 file list
#report number of .h5 files found
h5_list_len = str(len(h5_file_list))
print("Number of .h5 files detected: ", h5_list_len)

#check to see if .h5 files were detected
if len(h5_file_list) == 0:
        print("No .h5 files detected. Check to see that the selected directory contains .lux.h5 files.")
        raise ValueError
        
#%% slice z series
z_start = None
z_end = None
slice_yn = ynbox("Subset the Z series?")

if slice_yn == True:
    z_start = int(enterbox("Type the start Z plane: "))
    z_end = int(enterbox("Type the end Z plane: "))
elif slice_yn == False:
    z_start = 0
    z_end = -1
else:
    print("Invalid input for slicing; defaulting to Z projecting full stack.")

#Option to project along different axis
axis_choices = [0,1,2]
slice_z = int(choicebox("""Which axis to project along?
                       0 for Z projection
                       1 for Y projection
                       2 for X projection
                       """, choices=axis_choices))
#%%

#keep track of time taken to create projecton
seconds_per_frame = []

#%% define h5 to numpy array function
def h5_to_proj(filename):
    h5_file = h5py.File(filename,'r')
    print("Reading: ", filename)
    h5_data = h5_file.get('Data')
    h5_array = np.array(h5_data)
    if z_start != z_end:
        max_projection = np.max(h5_array, axis = slice_z)
    else:
        max_projection = h5_array[z_start]
    return max_projection

#%% process the list of .h5 files
for count, item in enumerate(h5_file_list):
    start_time = time.time()
    #create max intensity projection
    max_proj = h5_to_proj(item)
    #create .tif filename
    tif_filename = output_name + '_' + str(count) + '.tif'
    #create path to save max projection to .tif file
    tif_file_path = os.path.join(output_folder, tif_filename)
    #write file
    imwrite(tif_file_path, max_proj, photometric='minisblack')
    print('Writing: ', tif_file_path)
    
    #calculate time remaining
    print("--- %0.3s s / frame ---" % (time.time() - start_time))
    time_per_frame = (time.time() - start_time)
    seconds_per_frame.append(time_per_frame)    
    #wait to average 3 values
    if len(seconds_per_frame) < 3:
        print("...")
    else:
        t1 = seconds_per_frame[-1]
        t2 = seconds_per_frame[-2]
        t3 = seconds_per_frame[-3]
        avg_time = (t1 + t2 + t3) / 3
        frames_left = len(h5_file_list) - count
        min_left = (frames_left * avg_time) / 60
        print("~ %0.3s minutes remaining." % min_left)

