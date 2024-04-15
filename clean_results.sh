#!/bin/bash

# Define the base directory
base_directory="result/libspatialindex/"

# Check if the base directory exists
if [ ! -d "$base_directory" ]; then
    echo "Directory does not exist: $base_directory"
    exit 1
fi

# Find and delete all files in subdirectories
# This command does not delete the directories themselves, only the files within them
find "$base_directory" -type f -exec rm -f {} \;