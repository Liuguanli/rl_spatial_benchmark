#!/bin/bash

sub_dir="./rl_baseline"

# Check if two arguments are passed
if [ "$#" -ne 6 ]; then
    echo "Usage: $0 <data_file_name> <query_file_name> <depth> <sample_size> <bit_num> <absolute_file_name>"
    exit 1
fi

# Assign the arguments to variables
data_file=$1
query_file=$2
tree_depth=$3
sample_size=$4
bit_num=$5
absolute_data_file=$6

python_file="exp_opt_fast.py"

train_command="python $python_file --data $data_file --query $query_file --action_depth $tree_depth --data_sample_points $sample_size --bit_length $bit_num $bit_num"

# Execute the training command
cd "${sub_dir}/Learned-BMTree" 

# ------------------------------------------------------------------------------------------------
# To make life easier!
# The following code is used to add a code snippet that copy the trained bmtree to root directory
# ------------------------------------------------------------------------------------------------

# Define a unique identifier for the code snippet
snippet_identifier="shutil.copy(result_save_path + 'best_tree.txt'"

# Check if the identifier is already in the file
if ! grep -q "$snippet_identifier" "$python_file"; then
    # If not, append the code snippet
    cat << 'EOF' >> $python_file
    import shutil
    # Get the current working directory
    current_directory = os.getcwd()
    # Define the destination path with the same filename in the current working directory
    dest_file = os.path.join(current_directory, "learned_bmtree.txt")
    # Copy the file
    shutil.copy(result_save_path + 'best_tree.txt'.format(args.result_appendix), dest_file)
    print(f"Copied file to: {dest_file}")
EOF
    echo "Python code appended to $python_file"
else
    echo "Code snippet already present in $python_file"
fi

echo "Training started with data file $data_file and query file $query_file"

eval "$train_command"

echo "Training Finished"

cd ..

# Filename to be copied
source_filename="run_learned_bmtree.py"

# Target directory where the file will be copied
target_directory="Learned-BMTree"

# Full path of the file in the target directory
target_file="$target_directory/$source_filename"

# Check if the file already exists in the target directory
if [ ! -f "$target_file" ]; then
    # If the file does not exist, copy it
    cp "./$source_filename" "$target_file"
    echo "File '$source_filename' copied to '$target_directory'."
else
    # If the file already exists, do not copy
    echo "File '$source_filename' already exists in '$target_directory'. Not copying."
fi

cd $target_directory


python $source_filename --data $absolute_data_file --action_depth $tree_depth

# remove data and queries.

# data_file=$1
# query_file=$2

# Remove the data and query files after the training is complete
rm -f "./data/${data_file}.json"
rm -f "./query/${query_file}.json"

echo "Removed data file $data_file and query file $query_file after training."

cd ../../
