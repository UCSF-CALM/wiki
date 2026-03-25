---
layout: default
title: Python Scripts for TruLive
author: Herrington, Kari
---

# Python Scripts for TruLive

Kari\'s notes on Scripts from Jan Frankowski **(Notes are IN PROGRESS)**

### Packages recommended to install

- spyder
- tifffile
- h5py
- opencv-python
- auto-py-to-exe
- tkinter
- natsort

**Note:**
- Auto-py-to-exe can be used to compile into a .exe to run without any dependencies
- Had trouble installing tkinter but it is only used in the old version

## Scripts from Jan:

### OLD - Max intensity_easygui

To create a series of MIPS for a timelapse.

Note: does one color and position at a time.

General idea is it is easy and the script opens up a series of windows for prompting:

- Navigate to Raw data
- Output
- Choose long or short camera
  - There may be a bug (it was...)
- Name
- Choose subset Z → note have to know Z planes you want

Should write a simple set of files for each in a folder and you can drag the folder into ImageJ.

This is tedious for multicolor/multi position - but can be nice for quick checks.

Recommended to use the other two files Step 1 and Step 2.

<details>
<summary><strong>🐍 maxintensity_raw_easygui_0403224_dualcolor.py</strong> — OLD dual-color max intensity projection via easygui prompts</summary>
<pre><code># -*- coding: utf-8 -*-
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
from fnmatch import fnmatch

#%% prompt for dane

dane_choices = ['yes', 'no']
dane_yn = buttonbox("Would you like to use the Dane edition of the software?", choices=dane_choices)

if dane_yn == 'yes':
    msgbox(""" Who's the best light sheet specialist?
             8888888                 DDDD   AAAAA  N   N  EEEEE
            88     88============== D    D  A   A  NN  N  E
            88     88               D    D  AAAAA  N N N  EEEE
             8888888                D    D  A   A  N  NN  E
            88     88               D    D  A   A  N  NN  E
            88     88==============  DDDD   A   A  N   N  EEEEE
             8888888
             From here on out, Dane Edition is the same as non-Dane edition.
          """)
    else: continue

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
h5_list_len = str(len(h5_file_list))
print("Number of .h5 files detected: ", h5_list_len)

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

#%% parse original list with cam choice
selected_files = []

if cam_reply == "long":
    selected_files = [f for f in h5_file_list if fnmatch(os.path.basename(f), "Cam_long_*.lux.h5")]
elif cam_reply == "right":
    selected_files = [f for f in h5_file_list if fnmatch(os.path.basename(f), "Cam_right_*.lux.h5")]
elif cam_reply == "left":
    selected_files = [f for f in h5_file_list if fnmatch(os.path.basename(f), "Cam_left_*.lux.h5")]
elif cam_reply == "short":
    selected_files = [f for f in h5_file_list if fnmatch(os.path.basename(f), "Cam_short_*.lux.h5")]
else:
    selected_files = [f for f in h5_file_list if fnmatch(os.path.basename(f), "Cam_bottom__*.lux.h5")]

#keep track of time taken to create projection
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
for count, item in enumerate(selected_files):
    start_time = time.time()
    max_proj = h5_to_proj(item)
    tif_filename = output_name + '_' + str(count) + '.tif'
    tif_file_path = os.path.join(output_folder, tif_filename)
    imwrite(tif_file_path, max_proj, photometric='minisblack')
    print('Writing: ', tif_file_path)

    print("--- %0.3s s / frame ---" % (time.time() - start_time))
    time_per_frame = (time.time() - start_time)
    seconds_per_frame.append(time_per_frame)
    if len(seconds_per_frame) &lt; 3:
        print("...")
    else:
        t1 = seconds_per_frame[-1]
        t2 = seconds_per_frame[-2]
        t3 = seconds_per_frame[-3]
        avg_time = (t1 + t2 + t3) / 3
        frames_left = len(h5_file_list) - count
        min_left = (frames_left * avg_time) / 60
        print("~ %0.3s minutes remaining." % min_left)</code></pre>
<p style="margin-top: 0.5em;">
  <a href="{{ '/assets/PythonScripts/Truelive/maxintensity_raw_easygui_0403224_dualcolor.py' | relative_url }}" target="_blank"><strong>↗ Open in new tab</strong></a>
  &nbsp;|&nbsp; <a href="{{ '/assets/PythonScripts/Truelive/maxintensity_raw_easygui_0403224_dualcolor.py' | relative_url }}" download><strong>⬇ Download Script</strong></a>
</p>
</details>

<details>
<summary><strong>🐍 maxintensity_raw_easygui_121522.py</strong> — OLD single-color max intensity projection via easygui prompts</summary>
<pre><code># -*- coding: utf-8 -*-
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

h5_folder = filedialog.askdirectory(title="Select folder containing .h5 files.")
print("Selected directory of .h5 files: " + h5_folder)

output_folder = filedialog.askdirectory(title="Select folder to output .tif files.")
print("Selected directory of output .tif files: " + output_folder)

#%% parse the filename to get the cam name
h5_file_list = glob.glob(os.path.join(h5_folder, '*.lux.h5'))
h5_file_list = natsorted(h5_file_list)

#%% find unique cam names
unique_filenames = []

for filename in h5_file_list:
    h5_file_parsed = filename.split('_')
    cam_name = h5_file_parsed[-2]
    if cam_name not in unique_filenames:
        unique_filenames.append(cam_name)

#%% prompt for which cam name
cam_choices = unique_filenames
cam_reply = buttonbox("Select the data to process:", choices=cam_choices)

output_name = enterbox("Type a name for the output .tif file series:")

#%% check length of .h5 file list
h5_list_len = str(len(h5_file_list))
print("Number of .h5 files detected: ", h5_list_len)

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

axis_choices = [0,1,2]
slice_z = int(choicebox("""Which axis to project along?
                       0 for Z projection
                       1 for Y projection
                       2 for X projection
                       """, choices=axis_choices))

#keep track of time taken to create projection
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
    max_proj = h5_to_proj(item)
    tif_filename = output_name + '_' + str(count) + '.tif'
    tif_file_path = os.path.join(output_folder, tif_filename)
    imwrite(tif_file_path, max_proj, photometric='minisblack')
    print('Writing: ', tif_file_path)

    print("--- %0.3s s / frame ---" % (time.time() - start_time))
    time_per_frame = (time.time() - start_time)
    seconds_per_frame.append(time_per_frame)
    if len(seconds_per_frame) &lt; 3:
        print("...")
    else:
        t1 = seconds_per_frame[-1]
        t2 = seconds_per_frame[-2]
        t3 = seconds_per_frame[-3]
        avg_time = (t1 + t2 + t3) / 3
        frames_left = len(h5_file_list) - count
        min_left = (frames_left * avg_time) / 60
        print("~ %0.3s minutes remaining." % min_left)</code></pre>
<p style="margin-top: 0.5em;">
  <a href="{{ '/assets/PythonScripts/Truelive/maxintensity_raw_easygui_121522.py' | relative_url }}" target="_blank"><strong>↗ Open in new tab</strong></a>
  &nbsp;|&nbsp; <a href="{{ '/assets/PythonScripts/Truelive/maxintensity_raw_easygui_121522.py' | relative_url }}" download><strong>⬇ Download Script</strong></a>
</p>
</details>

---

### Max_intensity_raw_030525 — STEP 1

Will down sample by default and will autodetect and split files.

Makes a new folder for each.

Gives line prompts:

- Point to raw data
- Folder for output
- Choose to down sample (default is Y)
- Allows you to assign Green, Magenta, Cyan, and Yellow
- Will autoscale/detect (or you can choose min and max for each channel)

<details>
<summary><strong>🐍 step1_maxintensity_raw_030525.py</strong> — Batch convert raw .h5 files to max-projection TIFFs with auto channel detection</summary>
<pre><code>import os
import h5py
import numpy as np
import tifffile
import glob
import re
import logging
from pathlib import Path
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('luxendo_processor.log')
    ]
)
logger = logging.getLogger(__name__)

def natural_sort_key(s):
    """
    Sort strings with embedded numbers naturally.
    E.g., "file_9.h5" comes before "file_10.h5"
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def extract_stack_channel_info(directory_path):
    """
    Extract stack and channel information from directory names.
    """
    dir_name = os.path.basename(directory_path)

    stack_match = re.search(r'stack_(\d+)', dir_name)
    stack_id = stack_match.group(1) if stack_match else None

    channel_match = re.search(r'channel_(\d+)-(\w+)', dir_name)
    if channel_match:
        channel_id = channel_match.group(1)
        channel_name = channel_match.group(2)
    else:
        channel_id = None
        channel_name = None

    return stack_id, channel_id, channel_name

def get_h5_files(directory):
    """
    Get all .h5 or .lux.h5 files in a directory.
    """
    h5_files = glob.glob(os.path.join(directory, "*.h5")) + glob.glob(os.path.join(directory, "*.lux.h5"))
    h5_files.sort(key=natural_sort_key)
    return h5_files

def max_z_projection(h5_file_path, downsample=True):
    """
    Read an .h5 file and create a maximum intensity projection along the Z axis.
    """
    try:
        with h5py.File(h5_file_path, 'r') as f:
            if 'Data' in f:
                data = f['Data'][:]
            else:
                for group_name in f:
                    group = f[group_name]
                    if 'Data' in group:
                        data = group['Data'][:]
                        break
                else:
                    raise KeyError("Could not find 'Data' dataset in the h5 file")

            max_projection = np.max(data, axis=0)

            if downsample:
                max_projection = max_projection[::2, ::2]

            return max_projection

    except Exception as e:
        logger.error(f"Error processing {h5_file_path}: {e}")
        raise

def process_h5_to_tiff(base_dir, output_base_dir, downsample=True):
    """
    Process all h5 files in the raw directory structure and create TIFF files.
    """
    raw_dir = os.path.join(base_dir, "raw")
    if not os.path.exists(raw_dir):
        logger.error(f"Raw directory not found at {raw_dir}")
        return 0

    subdirs = [d for d in glob.glob(os.path.join(raw_dir, "*")) if os.path.isdir(d)]

    files_processed = 0

    for subdir in subdirs:
        stack_id, channel_id, channel_name = extract_stack_channel_info(subdir)

        if not all([stack_id, channel_id, channel_name]):
            logger.warning(f"Could not extract stack/channel info from {subdir}, skipping")
            continue

        logger.info(f"Processing stack_{stack_id}, channel_{channel_id}-{channel_name}")

        stack_dir = os.path.join(output_base_dir, f"stack_{stack_id}")
        os.makedirs(stack_dir, exist_ok=True)

        channel_dir = os.path.join(stack_dir, channel_name)
        os.makedirs(channel_dir, exist_ok=True)

        h5_files = get_h5_files(subdir)

        if not h5_files:
            logger.warning(f"No .h5 files found in {subdir}")
            continue

        for i, h5_file in enumerate(h5_files):
            try:
                file_basename = os.path.basename(h5_file)
                timepoint_match = re.search(r'(\d+)(?:\.lux)?\.h5$', file_basename)

                if timepoint_match:
                    timepoint = timepoint_match.group(1)
                else:
                    timepoint = f"{i:05d}"

                suffix = "_ds2x" if downsample else "_full"
                tiff_filename = f"stk{stack_id}_{channel_name}_{timepoint}{suffix}.tif"
                tiff_path = os.path.join(channel_dir, tiff_filename)

                if os.path.exists(tiff_path):
                    logger.info(f"File {tiff_filename} already exists, skipping")
                    continue

                max_proj = max_z_projection(h5_file, downsample)

                tifffile.imwrite(tiff_path, max_proj.astype(np.uint16))
                logger.info(f"Saved {tiff_filename}")
                files_processed += 1

            except Exception as e:
                logger.error(f"Error processing {h5_file}: {e}")

    return files_processed

def main():
    print("\n==== Luxendo Max Projection Processor ====\n")

    input_dir = input("Enter the input directory containing the raw folder: ").strip()
    if not os.path.exists(input_dir):
        print(f"Error: Directory '{input_dir}' does not exist.")
        return

    output_dir = input("Enter the output directory for max projections: ").strip()

    downsample_input = input("Downsample images by 2x laterally? (Y/n, default=Y): ").strip().lower()
    downsample = not downsample_input.startswith('n')

    os.makedirs(output_dir, exist_ok=True)

    print(f"\nProcessing h5 files from {input_dir}")
    print(f"Output will be saved to {output_dir}")
    print(f"Downsampling: {'Enabled (2x)' if downsample else 'Disabled (full resolution)'}")
    print("\nStarting conversion...")

    files_processed = process_h5_to_tiff(input_dir, output_dir, downsample)

    print("\n==== Processing Summary ====")
    print(f"Files processed: {files_processed}")
    print(f"Output directory: {output_dir}")
    print("============================")

    if files_processed == 0:
        print("\nNo files were processed. Please check input directory and log for details.")
    else:
        print("\nProcessing complete!")

if __name__ == "__main__":
    main()</code></pre>
<p style="margin-top: 0.5em;">
  <a href="{{ '/assets/PythonScripts/Truelive/step1_maxintensity_raw_030525.py' | relative_url }}" target="_blank"><strong>↗ Open in new tab</strong></a>
  &nbsp;|&nbsp; <a href="{{ '/assets/PythonScripts/Truelive/step1_maxintensity_raw_030525.py' | relative_url }}" download><strong>⬇ Download Script</strong></a>
</p>
</details>

---

### Video_030525 — STEP 2

Runs on the previous MIPs output from Step 1.

Will give overlay video and montage.

Recommended FPS is 7.

Auto mirrors images from the short camera.

<details>
<summary><strong>🐍 step2_video_030525.py</strong> — Generate side-by-side and overlay multichannel videos from TIFF stacks</summary>
<pre><code># -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 03:42:01 2025
@author: SPIM
"""
import os
import glob
import numpy as np
import cv2
from tifffile import imread
import re
import math

def ensure_same_dimensions(images):
    """
    Ensures all images have the same dimensions by padding smaller images.
    """
    if not images:
        return []

    max_h = max(img.shape[0] for img in images)
    max_w = max(img.shape[1] for img in images)

    result_images = []
    for img in images:
        h, w = img.shape

        if h == max_h and w == max_w:
            result_images.append(img)
            continue

        result_img = np.zeros((max_h, max_w), dtype=img.dtype)

        y_offset = (max_h - h) // 2
        x_offset = (max_w - w) // 2

        result_img[y_offset:y_offset+h, x_offset:x_offset+w] = img
        result_images.append(result_img)

    return result_images

def natural_sort_key(s):
    """
    Sort strings with embedded numbers naturally.
    E.g., "stk0_GFP_9.tif" comes before "stk0_GFP_10.tif"
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def should_mirror_horizontally(directory_path):
    """
    Determines if images from this directory should be mirrored horizontally.
    Images from the "short" camera should be mirrored.
    """
    return "short" in directory_path.lower()

def create_multichannel_videos(channel_dirs, output_path_side, output_path_overlay, fps=10, min_values=None, max_values=None):
    """
    Creates side-by-side and overlay animations from 1-4 image time series.
    """
    should_mirror = [should_mirror_horizontally(directory) for directory in channel_dirs]
    mirror_statuses = ["(mirrored)" if mirror else "" for mirror in should_mirror]
    print("  Camera detection:")
    for i, (directory, mirror) in enumerate(zip(channel_dirs, should_mirror)):
        camera_type = "short" if mirror else "long"
        print(f"    Channel {i+1}: Detected as '{camera_type}' camera {mirror_statuses[i]}")

    # Define colors for each channel: Green, Magenta, Cyan, Yellow
    COLORS = [
        [0, 255, 0],    # Green
        [255, 0, 255],  # Magenta
        [0, 255, 255],  # Cyan
        [255, 255, 0]   # Yellow
    ]

    num_channels = len(channel_dirs)

    if num_channels == 0:
        print("Error: No channel directories provided.")
        return False

    if num_channels &gt; 4:
        print("Warning: Only the first 4 channels will be used.")
        channel_dirs = channel_dirs[:4]
        num_channels = 4

    if min_values is None:
        min_values = [None] * num_channels
    if max_values is None:
        max_values = [None] * num_channels

    min_values = min_values[:num_channels] + [None] * (num_channels - len(min_values))
    max_values = max_values[:num_channels] + [None] * (num_channels - len(max_values))

    all_files = []
    for channel_dir in channel_dirs:
        files = glob.glob(os.path.join(channel_dir, "*.tif"))
        files.sort(key=natural_sort_key)
        all_files.append(files)

    for i, files in enumerate(all_files):
        if not files:
            print(f"Error: Missing files in channel {i+1} directory.")
            return False

    n_frames = min(len(files) for files in all_files)
    if n_frames == 0:
        print("Error: No frames found in one or more channels.")
        return False

    for i, files in enumerate(all_files):
        if len(files) != n_frames:
            print(f"Warning: Channel {i+1} has {len(files)} frames, different from minimum {n_frames}.")

    try:
        first_images = []
        for i, files in enumerate(all_files):
            img = imread(files[0])
            if should_mirror[i]:
                img = np.fliplr(img)
            first_images.append(img)
        first_images = ensure_same_dimensions(first_images)
    except Exception as e:
        print(f"Error reading image files: {e}")
        return False

    height, width = first_images[0].shape

    for i, files in enumerate(all_files):
        if min_values[i] is None or max_values[i] is None:
            sample_indices = np.linspace(0, len(files)-1, min(10, len(files)), dtype=int)
            min_auto = float('inf')
            max_auto = float('-inf')

            for idx in sample_indices:
                img = imread(files[idx])
                if should_mirror[i]:
                    img = np.fliplr(img)
                min_auto = min(min_auto, np.percentile(img, 0.1))
                max_auto = max(max_auto, np.percentile(img, 99.9))

            min_values[i] = min_values[i] if min_values[i] is not None else min_auto
            max_values[i] = max_values[i] if max_values[i] is not None else max_auto

        mirror_status = " (mirrored)" if should_mirror[i] else ""
        print(f"  Channel {i+1}{mirror_status} LUT range: {min_values[i]} - {max_values[i]}")

    side_width = width * num_channels

    fourcc_side = cv2.VideoWriter_fourcc(*'XVID') if output_path_side.endswith('.avi') else cv2.VideoWriter_fourcc(*'mp4v')
    video_side = cv2.VideoWriter(output_path_side, fourcc_side, fps, (side_width, height))

    fourcc_overlay = cv2.VideoWriter_fourcc(*'XVID') if output_path_overlay.endswith('.avi') else cv2.VideoWriter_fourcc(*'mp4v')
    video_overlay = cv2.VideoWriter(output_path_overlay, fourcc_overlay, fps, (width, height))

    for frame_idx in range(n_frames):
        if frame_idx % max(1, n_frames // 10) == 0:
            print(f"  Processing frame {frame_idx+1}/{n_frames}...")

        frame_images = []
        for i, files in enumerate(all_files):
            img = imread(files[frame_idx])
            if should_mirror[i]:
                img = np.fliplr(img)
            frame_images.append(img)

        frame_images = ensure_same_dimensions(frame_images)

        colored_images = []
        for i, img in enumerate(frame_images):
            scaled = np.clip((img - min_values[i]) / (max_values[i] - min_values[i]) * 255, 0, 255).astype(np.uint8)
            colored = np.zeros((height, width, 3), dtype=np.uint8)
            color = COLORS[i]
            for c in range(3):
                if color[c] &gt; 0:
                    colored[:, :, c] = scaled
            colored_images.append(colored)

        side_by_side = np.hstack(colored_images)
        video_side.write(side_by_side)

        overlay = np.zeros((height, width, 3), dtype=np.uint8)
        for i, img in enumerate(frame_images):
            scaled = np.clip((img - min_values[i]) / (max_values[i] - min_values[i]) * 255, 0, 255).astype(np.uint8)
            temp = np.zeros((height, width, 3), dtype=np.uint8)
            color = COLORS[i]
            for c in range(3):
                if color[c] &gt; 0:
                    temp[:, :, c] = scaled
            overlay = np.clip(overlay.astype(np.int16) + temp.astype(np.int16), 0, 255).astype(np.uint8)

        video_overlay.write(overlay)

    video_side.release()
    video_overlay.release()

    print(f"  Side-by-side animation saved to {output_path_side}")
    print(f"  Overlay animation saved to {output_path_overlay}")
    print(f"  Video details: {n_frames} frames, {fps} fps")

    return True

def find_unique_subdirectories(output_dir):
    """
    Find all unique subdirectory names within stack directories.
    """
    stack_dirs = [d for d in os.listdir(output_dir)
                 if os.path.isdir(os.path.join(output_dir, d)) and d.startswith("stack_")]

    print(f"Found {len(stack_dirs)} stack directories.")

    all_subdirs = {}
    unique_subdirs = set()

    for stack_dir in stack_dirs:
        stack_path = os.path.join(output_dir, stack_dir)
        subdirs = [d for d in os.listdir(stack_path)
                  if os.path.isdir(os.path.join(stack_path, d))]
        all_subdirs[stack_dir] = subdirs
        unique_subdirs.update(subdirs)
        print(f"  {stack_dir} contains subdirectories: {', '.join(subdirs)}")

    print(f"\nUnique subdirectory names found: {', '.join(sorted(unique_subdirs))}")

    return all_subdirs, unique_subdirs

def create_videos_from_stacks(output_dir, videos_dir, fps, min_values, max_values, channel_labels):
    """
    Create videos from all the stack directories in the output folder.
    """
    all_subdirs, unique_subdirs = find_unique_subdirectories(output_dir)

    if not all_subdirs:
        print("No stack directories found.")
        return

    COLOR_NAMES = ["GREEN", "MAGENTA", "CYAN", "YELLOW"]

    valid_stacks = []
    for stack_name, subdirs in all_subdirs.items():
        stack_path = os.path.join(output_dir, stack_name)
        channels_present = []
        channel_dirs = []

        for i, label in enumerate(channel_labels):
            if label in subdirs:
                channel_dir = os.path.join(stack_path, label)
                tif_files = glob.glob(os.path.join(channel_dir, "*.tif"))
                if tif_files:
                    channels_present.append(i)
                    channel_dirs.append(channel_dir)

        if channel_dirs:
            channels_desc = ", ".join([f"'{channel_labels[i]}' ({COLOR_NAMES[i]})" for i in channels_present])
            print(f"  Found valid channels in {stack_name}: {channels_desc}")
            valid_stacks.append((stack_name, channel_dirs, [channel_labels[i] for i in channels_present]))
        else:
            print(f"  Warning: {stack_name} has no directories with .tif files matching the selected channels")

    if not valid_stacks:
        print(f"No stacks found with any of the selected channel directories containing .tif files.")
        return

    if not os.path.exists(videos_dir):
        os.makedirs(videos_dir)

    successful_videos = 0
    failed_videos = 0

    print("\nCreating animations:")
    for i, (stack_name, channel_dirs, channels_used) in enumerate(valid_stacks):
        channels_suffix = "_".join(channels_used)
        output_base = os.path.join(videos_dir, f"{stack_name}_{channels_suffix}")
        output_path_side = f"{output_base}_side.avi"
        output_path_overlay = f"{output_base}_overlay.avi"

        print(f"\nProcessing {i+1}/{len(valid_stacks)}: {stack_name}")

        channel_indices = [channel_labels.index(ch) for ch in channels_used]
        used_min_values = [min_values[i] for i in channel_indices]
        used_max_values = [max_values[i] for i in channel_indices]

        success = create_multichannel_videos(
            channel_dirs,
            output_path_side,
            output_path_overlay,
            fps,
            used_min_values,
            used_max_values
        )

        if success:
            successful_videos += 1
        else:
            failed_videos += 1

    print("\nAnimation Creation Summary:")
    print(f"  Successful videos: {successful_videos}")
    print(f"  Failed videos: {failed_videos}")
    print(f"  Videos saved to: {videos_dir}")

if __name__ == "__main__":
    output_dir = input("Enter the directory containing the stack folders: ")

    if not os.path.isdir(output_dir):
        print(f"Error: '{output_dir}' is not a valid directory.")
        exit(1)

    all_subdirs, unique_subdirs = find_unique_subdirectories(output_dir)
    if not unique_subdirs:
        print("No subdirectories found in stack folders.")
        exit(1)

    sorted_subdirs = sorted(unique_subdirs)

    MAX_CHANNELS = 4
    COLOR_NAMES = ["GREEN", "MAGENTA", "CYAN", "YELLOW"]

    print("\nYou can select up to 4 channels to include in your videos.")
    print("Each channel will be assigned a color in this order: GREEN, MAGENTA, CYAN, YELLOW")

    selected_channels = []
    selected_labels = []

    for i in range(MAX_CHANNELS):
        print(f"\nSelect subdirectory for channel {i+1} ({COLOR_NAMES[i]}):")
        print("0. NONE (don't include this channel)")
        for j, subdir in enumerate(sorted_subdirs):
            print(f"{j+1}. {subdir}")

        while True:
            choice = input(f"Enter number for {COLOR_NAMES[i]} channel (0 to skip): ")
            try:
                idx = int(choice)
                if idx == 0:
                    print(f"  Skipping {COLOR_NAMES[i]} channel")
                    break
                elif 1 &lt;= idx &lt;= len(sorted_subdirs):
                    label = sorted_subdirs[idx-1]
                    selected_channels.append(i)
                    selected_labels.append(label)
                    print(f"  Selected '{label}' for {COLOR_NAMES[i]} channel")
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

        if i == 0 and len(selected_channels) == 0:
            print("Error: You must select at least one channel.")
            continue
        elif i &gt; 0 and len(selected_channels) == 0:
            print("Warning: No channels selected. At least one channel is required.")
            continue
        elif i == MAX_CHANNELS - 1 or i &gt;= len(sorted_subdirs) - 1:
            break

    if len(selected_channels) == 0:
        print("Error: No channels selected. Exiting.")
        exit(1)

    print("\nSelected channels:")
    for i, label in enumerate(selected_labels):
        channel_idx = selected_channels[i]
        print(f"  Channel {channel_idx+1} ({COLOR_NAMES[channel_idx]}): '{label}'")

    videos_dir = input("Enter the directory where videos should be saved: ")

    fps = input("Enter frames per second for all videos (default: 10): ")
    fps = int(fps) if fps.strip() else 10

    min_values = [None] * MAX_CHANNELS
    max_values = [None] * MAX_CHANNELS

    print("\nLUT Range Settings (leave blank for auto-detection):")
    print("These settings will be applied to ALL videos.")

    for i in range(MAX_CHANNELS):
        if i in selected_channels:
            min_val = input(f"{COLOR_NAMES[i]} channel minimum value: ")
            max_val = input(f"{COLOR_NAMES[i]} channel maximum value: ")
            min_values[i] = int(min_val) if min_val.strip() else None
            max_values[i] = int(max_val) if max_val.strip() else None

    channel_labels = [None] * MAX_CHANNELS
    for i, label in enumerate(selected_labels):
        channel_idx = selected_channels[i]
        channel_labels[channel_idx] = label

    create_videos_from_stacks(output_dir, videos_dir, fps, min_values, max_values, channel_labels)</code></pre>
<p style="margin-top: 0.5em;">
  <a href="{{ '/assets/PythonScripts/Truelive/step2_video_030525.py' | relative_url }}" target="_blank"><strong>↗ Open in new tab</strong></a>
  &nbsp;|&nbsp; <a href="{{ '/assets/PythonScripts/Truelive/step2_video_030525.py' | relative_url }}" download><strong>⬇ Download Script</strong></a>
</p>
</details>
