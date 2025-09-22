#!/bin/bash

sub_dir="./rl_baseline"

# Check if two arguments are passed
if [ "$#" -ne 6 ]; then
    echo "Usage: $0 <data_file_name> <query_file_name> <episode> <sampling_ratio> <action_sampling_size> <dimension>"
    exit 1
fi

# Assign the arguments to variables
data_file=$1
query_file=$2
episode=$3
sampling_ratio=$4
action_sampling_size=$5
dim=$6

python_file="run_qdtree.py"


train_command="python $sub_dir/Qdtree/$python_file --dataset $data_file --workloads $query_file --episode $episode --sampling_ratio $sampling_ratio --action_sampling_size $action_sampling_size --dimension $dim"  

echo "Training started with data file $data_file and query file $query_file"

eval "$train_command"

echo "Training Finished"