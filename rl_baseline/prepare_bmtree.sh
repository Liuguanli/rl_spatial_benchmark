#!/bin/bash

# Define the paths for the project directory, data directory, and the subdirectory where you'll work with Learned-BMTree
data_dir="./data"  # Data directory relative to the current directory
sub_dir="./rl_baseline"  # Subdirectory for Learned-BMTree relative to the current directory
# repo_url="https://github.com/gravesprite/Learned-BMTree.git"
repo_url="git@github.com:AI-DB-UoM/Learned-BMTree.git"
env_name="base"  # Your existing conda environment name

# Attempt to clone the Learned-BMTree repository into the specified subdirectory
# If the directory exists, pull the latest changes instead
repo_path="${sub_dir}/Learned-BMTree"
if [ -d "$repo_path" ]; then
    echo "Repository directory exists. Pulling latest changes..."
    # git -C "$repo_path" pull
else
    echo "Cloning Learned-BMTree repository..."
    mkdir -p "$sub_dir"
    git clone "$repo_url" "$repo_path"
fi

# Update the existing environment with dependencies from the environment.yml file
# echo "Updating the '${env_name}' environment with dependencies from environment.yml..."
# env_file="${sub_dir}/Learned-BMTree/environment.yml"
# conda activate "$env_name" && conda env update --name "$env_name" --file "$env_file"
