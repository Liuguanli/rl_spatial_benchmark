#!/bin/bash

sub_dir="./rl_baseline"

# Check if two arguments are passed
if [ "$#" -ne 7 ]; then
    echo "Usage: $0 <data_file_name> <query_file_name> <epoch> <sample_size> <learning_rate> <gamma> <rl_method>"
    exit 1
fi

# Assign the arguments to variables
# current_dir=$(pwd)
# data_file="${current_dir}/$1"
# query_file="${current_dir}/$2"
data_file=$1
query_file=$2
epoch=$3
sample_size=$4
learning_rate=$5
gamma=$6
rl_method=$7

train_choose_subtree="model_ChooseSubtree.py"
train_split="model_Split.py"
compile_sh="compile.sh"

split_model_path="benchmark/model/split_data_100000000_2_uniform_1_range_1000_2_uniform_1_0.001x0.001_rlrtree_epoch_10_sample_10000.pth"
choose_subtree_model_path="benchmark/model/choose_subtree_data_100000000_2_uniform_1_range_1000_2_uniform_1_0.001x0.001_rlrtree_epoch_10_sample_10000.pth"

compile_rtree_command="sh $compile_sh"
train_choose_subtree_command="python $sub_dir/RLRTree/$train_choose_subtree -model_path $split_model_path -gamma $gamma -lr $learning_rate -rl_method $rl_method -dataset_filename $data_file -queryset_filename $query_file -epoch $epoch -sample_size $sample_size"
train_train_split_command="python $sub_dir/RLRTree/$train_split -model_path $choose_subtree_model_path -gamma $gamma -lr $learning_rate -dataset_filename $data_file -queryset_filename $query_file -epoch $epoch -sample_size $sample_size"

# Execute the training command 
# cd "${sub_dir}/RLRTree" 

pushd $sub_dir/RLRTree
echo "compile Rtree"
eval "$compile_rtree_command"
popd


echo "Training started with data file $data_file and query file $query_file"

eval "$train_choose_subtree_command"
# cp choose_subtree.pth benchmark/model

echo "Training CHOOSE SUBTREE Finished"

eval "$train_train_split_command"
# cp split.pth benchmark/model

echo "Training SPLIT Finished"