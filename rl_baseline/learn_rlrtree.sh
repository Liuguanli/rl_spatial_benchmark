#!/bin/bash

sub_dir="./rl_baseline"

# Check if two arguments are passed
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <data_file_name> <query_file_name>"
    exit 1
fi

# Assign the arguments to variables
# current_dir=$(pwd)
# data_file="${current_dir}/$1"
# query_file="${current_dir}/$2"
data_file=$1
query_file=$2

train_choose_subtree="model_ChooseSubtree.py"
train_split="model_Split.py"
compile_sh="compile.sh"

compile_rtree_command="sh $compile_sh"
train_choose_subtree_command="python $sub_dir/RLRTree/$train_choose_subtree -dataset_filename $data_file -queryset_filename $query_file -epoch 1"
train_train_split_command="python $sub_dir/RLRTree/$train_split -dataset_filename $data_file -queryset_filename $query_file -epoch 1"

# Execute the training command
# cd "${sub_dir}/RLRTree" 

pushd $sub_dir/RLRTree
echo "compile Rtree"
eval "$compile_rtree_command"
popd


echo "Training started with data file $data_file and query file $query_file"

eval "$train_choose_subtree_command"
cp choose_subtree.pth benchmark/libspatialindex

echo "Training CHOOSE SUBTREE Finished"

eval "$train_train_split_command"
cp split.pth benchmark/libspatialindex

echo "Training SPLIT Finished"



# cd ..

# # Filename to be copied
# source_filename="run_learned_bmtree.py"

# # Target directory where the file will be copied
# target_directory="Learned-BMTree"

# # Full path of the file in the target directory
# target_file="$target_directory/$source_filename"

# # Check if the file already exists in the target directory
# if [ ! -f "$target_file" ]; then
#     # If the file does not exist, copy it
#     cp "./$source_filename" "$target_file"
#     echo "File '$source_filename' copied to '$target_directory'."
# else
#     # If the file already exists, do not copy
#     echo "File '$source_filename' already exists in '$target_directory'. Not copying."
# fi

# cd $target_directory


# python $source_filename --data $data_file --action_depth $tree_depth

# # remove data and queries.


# # data_file=$1
# # query_file=$2

# # Remove the data and query files after the training is complete
# rm -f "./data/${data_file}.json"
# rm -f "./query/${query_file}.json"

# echo "Removed data file $data_file and query file $query_file after training."

# cd ../../
