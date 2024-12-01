#!/bin/bash

sub_dir="./li_baseline/PLATON"

# Check if two arguments are passed
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <input_data_file> <input_query_file> <output_file>"
    exit 1
fi

# Assign the arguments to variables
input_data_file=$1
input_query_file=$2
output_file=$3

# echo "is_train: $is_train"

# cd "${sub_dir}/PLATON" 

# if [ "$is_train" = "True" ]; then

learn_platon="mcts-pack.py"

train_command="python $sub_dir/$learn_platon --input_data_file $input_data_file --input_query_file $input_query_file --output_file $output_file"

# Print the full command (optional)
echo "Train Command: $train_command"

echo "Training started with data file $data_file and query file $query_file"

eval "$train_command"

echo "Training Finished"

# else
#     echo "No training performed, processing $absolute_data_file with bit_num $bit_num."
# fi

# cd ..