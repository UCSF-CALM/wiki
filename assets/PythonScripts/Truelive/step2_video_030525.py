# -*- coding: utf-8 -*-
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
    
    Args:
        images (list): List of numpy arrays representing images
        
    Returns:
        list: List of images with the same dimensions
    """
    if not images:
        return []
    
    # Find maximum dimensions
    max_h = max(img.shape[0] for img in images)
    max_w = max(img.shape[1] for img in images)
    
    # Resize all images to match maximum dimensions
    result_images = []
    for img in images:
        h, w = img.shape
        
        # If dimensions already match, no need to resize
        if h == max_h and w == max_w:
            result_images.append(img)
            continue
        
        # Create result array with target dimensions
        result_img = np.zeros((max_h, max_w), dtype=img.dtype)
        
        # Calculate centering offsets
        y_offset = (max_h - h) // 2
        x_offset = (max_w - w) // 2
        
        # Copy data with centering (padding if necessary)
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
    
    Args:
        directory_path (str): Path to check
        
    Returns:
        bool: True if images should be mirrored
    """
    # Check if "short" appears in the path
    return "short" in directory_path.lower()

def create_multichannel_videos(channel_dirs, output_path_side, output_path_overlay, fps=10, min_values=None, max_values=None):
    """
    Creates side-by-side and overlay animations from 1-4 image time series.
    
    Args:
        channel_dirs (list): List of directories containing channel images
        output_path_side (str): Path for the side-by-side output video file
        output_path_overlay (str): Path for the overlay output video file
        fps (int): Frames per second for the video
        min_values (list): Minimum values for each channel's LUT scaling (None for auto)
        max_values (list): Maximum values for each channel's LUT scaling (None for auto)
        
    Returns:
        bool: True if animations were created successfully, False otherwise
    """
    # Determine which channels need mirroring (from "short" camera)
    should_mirror = [should_mirror_horizontally(directory) for directory in channel_dirs]
    mirror_statuses = ["(mirrored)" if mirror else "" for mirror in should_mirror]
    print("  Camera detection:")
    for i, (directory, mirror) in enumerate(zip(channel_dirs, should_mirror)):
        camera_type = "short" if mirror else "long"
        print(f"    Channel {i+1}: Detected as '{camera_type}' camera {mirror_statuses[i]}")

    # Define colors for each channel: Green, Magenta, Cyan, Yellow
    COLORS = [
        [0, 255, 0],    # Green (G channel)
        [255, 0, 255],  # Magenta (R+B channels)
        [0, 255, 255],  # Cyan (G+B channels)
        [255, 255, 0]   # Yellow (R+G channels)
    ]
    
    num_channels = len(channel_dirs)
    
    if num_channels == 0:
        print("Error: No channel directories provided.")
        return False
    
    if num_channels > 4:
        print("Warning: Only the first 4 channels will be used.")
        channel_dirs = channel_dirs[:4]
        num_channels = 4
    
    # Set default min/max values if not provided
    if min_values is None:
        min_values = [None] * num_channels
    if max_values is None:
        max_values = [None] * num_channels
    
    # Ensure we have enough min/max values
    min_values = min_values[:num_channels] + [None] * (num_channels - len(min_values))
    max_values = max_values[:num_channels] + [None] * (num_channels - len(max_values))
    
    # Find all tiff files for each channel
    all_files = []
    for channel_dir in channel_dirs:
        files = glob.glob(os.path.join(channel_dir, "*.tif"))
        files.sort(key=natural_sort_key)
        all_files.append(files)
    
    # Check if we have files for each channel
    for i, files in enumerate(all_files):
        if not files:
            print(f"Error: Missing files in channel {i+1} directory.")
            return False
    
    # Find minimum number of frames across all channels
    n_frames = min(len(files) for files in all_files)
    if n_frames == 0:
        print("Error: No frames found in one or more channels.")
        return False
    
    # Check if counts mismatch
    for i, files in enumerate(all_files):
        if len(files) != n_frames:
            print(f"Warning: Channel {i+1} has {len(files)} frames, different from minimum {n_frames}.")
            print(f"Using first {n_frames} frames from each channel.")
    
    # Read first images to determine dimensions
    try:
        first_images = []
        for i, files in enumerate(all_files):
            img = imread(files[0])
            
            # Apply horizontal mirroring for "short" camera images
            if should_mirror[i]:
                img = np.fliplr(img)
                
            first_images.append(img)
        
        # Ensure all images have the same dimensions
        first_images = ensure_same_dimensions(first_images)
    except Exception as e:
        print(f"Error reading image files: {e}")
        return False
    
    height, width = first_images[0].shape
    
    # Auto-determine min/max if not provided
    for i, files in enumerate(all_files):
        if min_values[i] is None or max_values[i] is None:
            # Sample a few frames to determine min/max
            sample_indices = np.linspace(0, len(files)-1, min(10, len(files)), dtype=int)
            min_auto = float('inf')
            max_auto = float('-inf')
            
            for idx in sample_indices:
                img = imread(files[idx])
                
                # Apply horizontal mirroring if needed (to ensure consistent calculations)
                if should_mirror[i]:
                    img = np.fliplr(img)
                    
                min_auto = min(min_auto, np.percentile(img, 0.1))
                max_auto = max(max_auto, np.percentile(img, 99.9))
            
            min_values[i] = min_values[i] if min_values[i] is not None else min_auto
            max_values[i] = max_values[i] if max_values[i] is not None else max_auto
        
        mirror_status = " (mirrored)" if should_mirror[i] else ""
        print(f"  Channel {i+1}{mirror_status} LUT range: {min_values[i]} - {max_values[i]}")
    
    # Calculate the side-by-side width based on number of channels
    side_width = width * num_channels
    
    # Set up video writers - 8-bit RGB output
    fourcc_side = cv2.VideoWriter_fourcc(*'XVID') if output_path_side.endswith('.avi') else cv2.VideoWriter_fourcc(*'mp4v')
    video_side = cv2.VideoWriter(output_path_side, fourcc_side, fps, (side_width, height))
    
    fourcc_overlay = cv2.VideoWriter_fourcc(*'XVID') if output_path_overlay.endswith('.avi') else cv2.VideoWriter_fourcc(*'mp4v')
    video_overlay = cv2.VideoWriter(output_path_overlay, fourcc_overlay, fps, (width, height))
    
    # Process each frame
    for frame_idx in range(n_frames):
        # Print progress every 10%
        if frame_idx % max(1, n_frames // 10) == 0:
            print(f"  Processing frame {frame_idx+1}/{n_frames}...")
        
        # Read images for this frame from each channel
        frame_images = []
        for i, files in enumerate(all_files):
            img = imread(files[frame_idx])
            
            # Apply horizontal mirroring for "short" camera images
            if should_mirror[i]:
                img = np.fliplr(img)
                
            frame_images.append(img)
        
        # Ensure all images have the same dimensions
        frame_images = ensure_same_dimensions(frame_images)
        
        # Create colored versions of each channel for side-by-side
        colored_images = []
        for i, img in enumerate(frame_images):
            # Apply LUT scaling
            scaled = np.clip((img - min_values[i]) / (max_values[i] - min_values[i]) * 255, 0, 255).astype(np.uint8)
            
            # Create RGB image with appropriate coloring
            colored = np.zeros((height, width, 3), dtype=np.uint8)
            color = COLORS[i]
            
            # Apply the color - set each RGB channel that should be included
            for c in range(3):
                if color[c] > 0:
                    colored[:, :, c] = scaled
            
            colored_images.append(colored)
        
        # Create side-by-side composite
        side_by_side = np.hstack(colored_images)
        video_side.write(side_by_side)
        
        # Create overlay composite
        overlay = np.zeros((height, width, 3), dtype=np.uint8)
        for i, img in enumerate(frame_images):
            # Apply LUT scaling
            scaled = np.clip((img - min_values[i]) / (max_values[i] - min_values[i]) * 255, 0, 255).astype(np.uint8)
            
            # Create temporary colored version
            temp = np.zeros((height, width, 3), dtype=np.uint8)
            color = COLORS[i]
            
            # Apply the color
            for c in range(3):
                if color[c] > 0:
                    temp[:, :, c] = scaled
            
            # Apply additive blending (clamping at 255)
            overlay = np.clip(overlay.astype(np.int16) + temp.astype(np.int16), 0, 255).astype(np.uint8)
        
        video_overlay.write(overlay)
    
    # Release video writers
    video_side.release()
    video_overlay.release()
    
    print(f"  Side-by-side animation saved to {output_path_side}")
    print(f"  Overlay animation saved to {output_path_overlay}")
    print(f"  Video details: {n_frames} frames, {fps} fps")
    print(f"  Side-by-side resolution: {side_width}x{height}")
    print(f"  Overlay resolution: {width}x{height}")
    
    return True

def find_unique_subdirectories(output_dir):
    """
    Find all unique subdirectory names within stack directories.
    
    Args:
        output_dir (str): Directory containing the stack folders
        
    Returns:
        dict: Dictionary of stack names and their subdirectories
        set: Set of all unique subdirectory names
    """
    # Find all stack directories
    stack_dirs = [d for d in os.listdir(output_dir) 
                 if os.path.isdir(os.path.join(output_dir, d)) and d.startswith("stack_")]
    
    print(f"Found {len(stack_dirs)} stack directories.")
    
    all_subdirs = {}
    unique_subdirs = set()
    
    # Process each stack directory
    for stack_dir in stack_dirs:
        stack_path = os.path.join(output_dir, stack_dir)
        
        # Get all subdirectories
        subdirs = [d for d in os.listdir(stack_path) 
                  if os.path.isdir(os.path.join(stack_path, d))]
        
        # Add to tracking
        all_subdirs[stack_dir] = subdirs
        unique_subdirs.update(subdirs)
        
        print(f"  {stack_dir} contains subdirectories: {', '.join(subdirs)}")
    
    print(f"\nUnique subdirectory names found: {', '.join(sorted(unique_subdirs))}")
    
    return all_subdirs, unique_subdirs

def create_videos_from_stacks(output_dir, videos_dir, fps, min_values, max_values, channel_labels):
    """
    Create videos from all the stack directories in the output folder.
    
    Args:
        output_dir (str): Directory containing the stack folders
        videos_dir (str): Directory where videos will be saved
        fps (int): Frames per second for videos
        min_values, max_values: Lists of LUT range values for each channel
        channel_labels (list): Labels for the channel directories
    """
    # Find all stack directory subdirs
    all_subdirs, unique_subdirs = find_unique_subdirectories(output_dir)
    
    if not all_subdirs:
        print("No stack directories found.")
        return
    
    # Define color names for labeling
    COLOR_NAMES = ["GREEN", "MAGENTA", "CYAN", "YELLOW"]
    
    # Find valid stack directories based on user-selected labels
    valid_stacks = []
    for stack_name, subdirs in all_subdirs.items():
        stack_path = os.path.join(output_dir, stack_name)
        
        # Check which of the selected labels exist in this stack
        channels_present = []
        channel_dirs = []
        
        for i, label in enumerate(channel_labels):
            if label in subdirs:
                # Get path
                channel_dir = os.path.join(stack_path, label)
                
                # Check if directory contains .tif files
                tif_files = glob.glob(os.path.join(channel_dir, "*.tif"))
                
                if tif_files:
                    channels_present.append(i)
                    channel_dirs.append(channel_dir)
        
        # Stack is valid if it has at least one of the requested channels
        if channel_dirs:
            channels_desc = ", ".join([f"'{channel_labels[i]}' ({COLOR_NAMES[i]})" for i in channels_present])
            print(f"  Found valid channels in {stack_name}: {channels_desc}")
            valid_stacks.append((stack_name, channel_dirs, [channel_labels[i] for i in channels_present]))
        else:
            print(f"  Warning: {stack_name} has no directories with .tif files matching the selected channels")
    
    if not valid_stacks:
        print(f"No stacks found with any of the selected channel directories containing .tif files.")
        return
    
    # Create videos directory if needed
    if not os.path.exists(videos_dir):
        os.makedirs(videos_dir)
        print(f"Created videos directory: {videos_dir}")
    
    # Process each valid stack
    successful_videos = 0
    failed_videos = 0
    
    print("\nCreating animations:")
    for i, (stack_name, channel_dirs, channels_used) in enumerate(valid_stacks):
        # Create descriptive filename
        channels_suffix = "_".join(channels_used)
        output_base = os.path.join(videos_dir, f"{stack_name}_{channels_suffix}")
        output_path_side = f"{output_base}_side.avi"
        output_path_overlay = f"{output_base}_overlay.avi"
        
        print(f"\nProcessing {i+1}/{len(valid_stacks)}: {stack_name}")
        
        # Select only the min/max values for the channels being used
        channel_indices = [channel_labels.index(ch) for ch in channels_used]
        used_min_values = [min_values[i] for i in channel_indices]
        used_max_values = [max_values[i] for i in channel_indices]
        
        # Create animations
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
    
    # Print final summary
    print("\nAnimation Creation Summary:")
    print(f"  Successful videos: {successful_videos}")
    print(f"  Failed videos: {failed_videos}")
    print(f"  Videos saved to: {videos_dir}")

if __name__ == "__main__":
    # Get the output directory from the user
    output_dir = input("Enter the directory containing the stack folders: ")
    
    # Check if the directory exists
    if not os.path.isdir(output_dir):
        print(f"Error: '{output_dir}' is not a valid directory.")
        exit(1)
    
    # Find unique subdirectories
    all_subdirs, unique_subdirs = find_unique_subdirectories(output_dir)
    if not unique_subdirs:
        print("No subdirectories found in stack folders.")
        exit(1)
    
    # Convert to sorted list for consistent ordering
    sorted_subdirs = sorted(unique_subdirs)
    
    # Allow selecting up to 4 channels
    MAX_CHANNELS = 4
    COLOR_NAMES = ["GREEN", "MAGENTA", "CYAN", "YELLOW"]
    
    print("\nYou can select up to 4 channels to include in your videos.")
    print("Each channel will be assigned a color in this order: GREEN, MAGENTA, CYAN, YELLOW")
    
    # Prompt user to select which directories/channels to use
    selected_channels = []
    selected_labels = []
    
    for i in range(MAX_CHANNELS):
        # Print selection options
        print(f"\nSelect subdirectory for channel {i+1} ({COLOR_NAMES[i]}):")
        print("0. NONE (don't include this channel)")
        for j, subdir in enumerate(sorted_subdirs):
            print(f"{j+1}. {subdir}")
        
        while True:
            choice = input(f"Enter number for {COLOR_NAMES[i]} channel (0 to skip): ")
            try:
                idx = int(choice)
                if idx == 0:
                    # User wants to skip this channel
                    print(f"  Skipping {COLOR_NAMES[i]} channel")
                    break
                elif 1 <= idx <= len(sorted_subdirs):
                    label = sorted_subdirs[idx-1]
                    selected_channels.append(i)
                    selected_labels.append(label)
                    print(f"  Selected '{label}' for {COLOR_NAMES[i]} channel")
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        # If all remaining channels are skipped, we're done
        if i == 0 and len(selected_channels) == 0:
            print("Error: You must select at least one channel.")
            continue
        elif i > 0 and len(selected_channels) == 0:
            print("Warning: No channels selected. At least one channel is required.")
            continue
        elif i == MAX_CHANNELS - 1 or i >= len(sorted_subdirs) - 1:
            # We've either offered all possible channels or run out of subdirectories
            break
    
    if len(selected_channels) == 0:
        print("Error: No channels selected. Exiting.")
        exit(1)
    
    # Summarize selections
    print("\nSelected channels:")
    for i, label in enumerate(selected_labels):
        channel_idx = selected_channels[i]
        print(f"  Channel {channel_idx+1} ({COLOR_NAMES[channel_idx]}): '{label}'")
    
    # Get the videos directory
    videos_dir = input("Enter the directory where videos should be saved: ")
    
    # Get global video settings
    fps = input("Enter frames per second for all videos (default: 10): ")
    fps = int(fps) if fps.strip() else 10
    
    # Prepare full lists of min/max values (None for channels not selected)
    min_values = [None] * MAX_CHANNELS
    max_values = [None] * MAX_CHANNELS
    
    # LUT range inputs
    print("\nLUT Range Settings (leave blank for auto-detection):")
    print("These settings will be applied to ALL videos.")
    
    for i in range(MAX_CHANNELS):
        if i in selected_channels:
            min_val = input(f"{COLOR_NAMES[i]} channel minimum value: ")
            max_val = input(f"{COLOR_NAMES[i]} channel maximum value: ")
            
            # Convert inputs to integers if provided
            min_values[i] = int(min_val) if min_val.strip() else None
            max_values[i] = int(max_val) if max_val.strip() else None
    
    # Create full list of channel labels (None for channels not selected)
    channel_labels = [None] * MAX_CHANNELS
    for i, label in enumerate(selected_labels):
        channel_idx = selected_channels[i]
        channel_labels[channel_idx] = label
    
    # Create videos from the stack directories
    create_videos_from_stacks(output_dir, videos_dir, fps, min_values, max_values, channel_labels)