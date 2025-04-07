#!/bin/bash

# Get the current timestamp in the format YYYY-MM-DD_HH-MM-SS
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")

# Define the output directory where the bags will be stored
output_dir="/home/avalor/holybro_avia/src/holybro_prep/bags"

# Create a new directory or use the existing one with the timestamp
mkdir -p "$output_dir"

# Run ros2 bag record with the timestamped output directory
ros2 bag record -a -o "$output_dir/rosbag2_$timestamp"
