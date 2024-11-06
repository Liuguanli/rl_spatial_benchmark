#!/bin/bash

sub_dir="./rl_baseline"

# Check if two arguments are passed
if [ "$#" -ne 7 ]; then
    echo "Usage: $0 <data_file_name> <query_file_name> <depth> <sample_size> <bit_num> <absolute_file_name> <is_train>"
    exit 1
fi

# Assign the arguments to variables
data_file=$1
query_file=$2
tree_depth=$3
sample_size=$4
bit_num=$5
absolute_data_file=$6
is_train=$7

echo "is_train: $is_train"


# Execute the training command
cd "${sub_dir}/Learned-BMTree" 


if [ "$is_train" = "True" ]; then

learn_bmtree="exp_opt_fast.py"

train_command="python $learn_bmtree --data $data_file --query $query_file --action_depth $tree_depth --data_sample_points $sample_size --bit_length $bit_num $bit_num"

# Print the full command (optional)
echo "Train Command: $train_command"

# ------------------------------------------------------------------------------------------------
# To make life easier!
# The following code is used to add a code snippet that copy the trained bmtree to root directory
# ------------------------------------------------------------------------------------------------

# Define a unique identifier for the code snippet
snippet_identifier="shutil.copy(result_save_path + 'best_tree.txt'"

# Check if the identifier is already in the file
if ! grep -q "$snippet_identifier" "$learn_bmtree"; then
    # If not, append the code snippet
    cat << 'EOF' >> $learn_bmtree
    import shutil
    # Get the current working directory
    current_directory = os.getcwd()
    # Define the destination path with the same filename in the current working directory
    dest_file = os.path.join(current_directory, "learned_bmtree.txt")
    # Copy the file
    shutil.copy(result_save_path + 'best_tree.txt'.format(args.result_appendix), dest_file)
    print(f"Copied file to: {dest_file}")
EOF
    echo "Python code appended to $learn_bmtree"
else
    echo "Code snippet already present in $learn_bmtree"
fi

echo "Training started with data file $data_file and query file $query_file"

eval "$train_command"

echo "Training Finished"

else
    echo "No training performed, processing $absolute_data_file with bit_num $bit_num."
fi


cd ..

# Filename to be copied
order_by_bmtree="run_learned_bmtree.py"

# Target directory where the file will be copied
target_directory="Learned-BMTree"

# Full path of the file in the target directory
target_file="$target_directory/$order_by_bmtree"

# Check if the file already exists in the target directory
if [ ! -f "$target_file" ]; then
    # If the file does not exist, copy it
    cp "./$order_by_bmtree" "$target_file"
    echo "File '$order_by_bmtree' copied to '$target_directory'."
else
    # If the file already exists, do not copy
    echo "File '$order_by_bmtree' already exists in '$target_directory'. Not copying."
fi

cd $target_directory

echo $absolute_data_file

python $order_by_bmtree --data $absolute_data_file --bit_length $bit_num $bit_num

# remove data and queries.

# data_file=$1
# query_file=$2

# Remove the data and query files after the training is complete
rm -f "./data/${data_file}.json"
rm -f "./query/${query_file}.json"

echo "Removed data file $data_file and query file $query_file after training."

cd ../../

bmtree_path="benchmark/model/learned_bmtree_${data_file}_${query_file}_bits_${bit_num}_depth_${tree_depth}_sample_${sample_size}.txt"

mv "rl_baseline/Learned-BMTree/learned_bmtree.txt" $bmtree_path
