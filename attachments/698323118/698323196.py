import os
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
    
    Args:
        directory_path (str): Path to a directory containing stack and channel info
        
    Returns:
        tuple: (stack_id, channel_id, channel_name)
    """
    dir_name = os.path.basename(directory_path)
    
    # Extract stack ID
    stack_match = re.search(r'stack_(\d+)', dir_name)
    stack_id = stack_match.group(1) if stack_match else None
    
    # Extract channel ID and name
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
    Get all .h5 or .lux.h5 files in a directory
    
    Args:
        directory (str): Directory path
        
    Returns:
        list: Sorted list of h5 file paths
    """
    h5_files = glob.glob(os.path.join(directory, "*.h5")) + glob.glob(os.path.join(directory, "*.lux.h5"))
    h5_files.sort(key=natural_sort_key)
    return h5_files

def max_z_projection(h5_file_path, downsample=True):
    """
    Read an .h5 file and create a maximum intensity projection along the Z axis
    
    Args:
        h5_file_path (str): Path to the h5 file
        downsample (bool): Whether to downsample the output by 2x laterally
        
    Returns:
        numpy.ndarray: 2D array of maximum intensity projection
    """
    try:
        with h5py.File(h5_file_path, 'r') as f:
            # Check if the file has a flat or nested structure
            if 'Data' in f:
                # Flat structure
                data = f['Data'][:]
            else:
                # Find the Data dataset in a nested structure
                for group_name in f:
                    group = f[group_name]
                    if 'Data' in group:
                        data = group['Data'][:]
                        break
                else:
                    # If we didn't find Data, raise an error
                    raise KeyError("Could not find 'Data' dataset in the h5 file")
            
            # Create max projection along Z axis (assuming Z is axis 0)
            max_projection = np.max(data, axis=0)
            
            # Downsample by 2x if requested
            if downsample:
                max_projection = max_projection[::2, ::2]
            
            return max_projection
            
    except Exception as e:
        logger.error(f"Error processing {h5_file_path}: {e}")
        raise

def process_h5_to_tiff(base_dir, output_base_dir, downsample=True):
    """
    Process all h5 files in the raw directory structure and create TIFF files
    
    Args:
        base_dir (str): Base directory containing the raw folder
        output_base_dir (str): Base directory where output will be saved
        downsample (bool): Whether to downsample the output by 2x laterally
        
    Returns:
        int: Number of files processed
    """
    # Find the raw folder
    raw_dir = os.path.join(base_dir, "raw")
    if not os.path.exists(raw_dir):
        logger.error(f"Raw directory not found at {raw_dir}")
        return 0
    
    # Find all subdirectories (stack/channel combinations)
    subdirs = [d for d in glob.glob(os.path.join(raw_dir, "*")) if os.path.isdir(d)]
    
    # Counter for processed files
    files_processed = 0
    
    # Process each subdirectory
    for subdir in subdirs:
        # Extract stack and channel information
        stack_id, channel_id, channel_name = extract_stack_channel_info(subdir)
        
        if not all([stack_id, channel_id, channel_name]):
            logger.warning(f"Could not extract stack/channel info from {subdir}, skipping")
            continue
        
        logger.info(f"Processing stack_{stack_id}, channel_{channel_id}-{channel_name}")
        
        # Create output directory structure
        stack_dir = os.path.join(output_base_dir, f"stack_{stack_id}")
        os.makedirs(stack_dir, exist_ok=True)
        
        channel_dir = os.path.join(stack_dir, channel_name)
        os.makedirs(channel_dir, exist_ok=True)
        
        # Get all h5 files in this directory
        h5_files = get_h5_files(subdir)
        
        if not h5_files:
            logger.warning(f"No .h5 files found in {subdir}")
            continue
        
        # Process each h5 file - create max projection and save as TIFF
        for i, h5_file in enumerate(h5_files):
            try:
                # Get a timepoint identifier from the filename
                file_basename = os.path.basename(h5_file)
                timepoint_match = re.search(r'(\d+)(?:\.lux)?\.h5$', file_basename)
                
                if timepoint_match:
                    timepoint = timepoint_match.group(1)
                else:
                    # Use index if no timepoint in filename
                    timepoint = f"{i:05d}"
                
                # Output filename - add a suffix if downsampled
                suffix = "_ds2x" if downsample else "_full"
                tiff_filename = f"stk{stack_id}_{channel_name}_{timepoint}{suffix}.tif"
                tiff_path = os.path.join(channel_dir, tiff_filename)
                
                # Skip if file already exists
                if os.path.exists(tiff_path):
                    logger.info(f"File {tiff_filename} already exists, skipping")
                    continue
                
                # Create max projection with downsampling option
                max_proj = max_z_projection(h5_file, downsample)
                
                # Save as TIFF (16-bit)
                tifffile.imwrite(tiff_path, max_proj.astype(np.uint16))
                logger.info(f"Saved {tiff_filename}")
                files_processed += 1
                
            except Exception as e:
                logger.error(f"Error processing {h5_file}: {e}")
    
    return files_processed

def main():
    print("\n==== Luxendo Max Projection Processor ====\n")
    
    # Prompt user for input and output directories
    input_dir = input("Enter the input directory containing the raw folder: ").strip()
    if not os.path.exists(input_dir):
        print(f"Error: Directory '{input_dir}' does not exist.")
        return
    
    output_dir = input("Enter the output directory for max projections: ").strip()
    
    # Prompt for downsampling option
    downsample_input = input("Downsample images by 2x laterally? (Y/n, default=Y): ").strip().lower()
    downsample = not downsample_input.startswith('n')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process h5 files to TIFF
    print(f"\nProcessing h5 files from {input_dir}")
    print(f"Output will be saved to {output_dir}")
    print(f"Downsampling: {'Enabled (2x)' if downsample else 'Disabled (full resolution)'}")
    print("\nStarting conversion...")
    
    files_processed = process_h5_to_tiff(input_dir, output_dir, downsample)
    
    # Print summary
    print("\n==== Processing Summary ====")
    print(f"Files processed: {files_processed}")
    print(f"Output directory: {output_dir}")
    print("============================")
    
    if files_processed == 0:
        print("\nNo files were processed. Please check input directory and log for details.")
    else:
        print("\nProcessing complete!")

if __name__ == "__main__":
    main()