#!/bin/bash

# Define color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m' # pink
CYAN='\033[0;36m'
LIGHTGRAY='\033[0;37m'
DARKGRAY='\033[1;30m'
LIGHTRED='\033[1;31m'
LIGHTGREEN='\033[1;32m'
LIGHTYELLOW='\033[1;33m'
LIGHTBLUE='\033[1;34m'
LIGHTMAGENTA='\033[1;35m'
LIGHTCYAN='\033[1;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Print step with dynamic color
print_step() {
    local color=$1
    local message=$2
    echo -e "${color}----------------------------------------------------------------${NC}"
    echo -e "${color}${message}${NC}"
    echo -e "${color}----------------------------------------------------------------${NC}"
}

# Print sub-step with dynamic color
print_sub_step() {
    local color=$1
    local message=$2
    echo -e "${color}---- ${message} ----${NC}"
}

print_step $GREEN "Step 1: Check Environment"
bash check_env.sh
if [ $? -eq 0 ]; then
    echo -e "${GREEN}All required libraries are installed.${NC}"
else
    exit 1
fi


print_step $YELLOW "Step 2: Prepare RL-Spatial Indices"
print_sub_step $GREEN "Step 2.1: Prepare BMTree"
sh rl_baseline/prepare_bmtree.sh

echo -e "${RED}If you have any environment related question in running Learned-BMTree, please check environment.yml under Learned-BMTree.${NC}"
echo -e "${GREEN}BMTree is installed.${NC}"

print_sub_step $YELLOW "Step 2.2: Prepare RLRtree"
print_sub_step $YELLOW "Step 2.3: Prepare Qd-tree"

export LD_LIBRARY_PATH=/home/liuguanli/Documents/libtorch/lib:$LD_LIBRARY_PATH

print_step $YELLOW "Step 3: Start Experiments"


python run_exp_from_config.py




















# rm -rf ./data/synthetic/*
# cd data || exit
# python synthetic_data_generator.py --size 1000 --dimensions 2 --distribution uniform --range 0 1 --range 0 1
# python synthetic_data_generator.py --size 1000 --dimensions 2 --distribution normal --range 0 1 --range 0 1
# python synthetic_data_generator.py --size 1000 --dimensions 2 --distribution skewed --range 0 1 --range 0 1 --skewness 2

# python synthetic_query_generator.py --query_type range --n_queries 100 --dimensions 2 --distribution uniform --bounds 0 1 --bounds 0 1 --query_range 0.01 0.01
# python synthetic_query_generator.py --query_type range --n_queries 100 --dimensions 2 --distribution normal --bounds 0 1 --bounds 0 1 --query_range 0.01 0.01
# python synthetic_query_generator.py --query_type range --n_queries 100 --dimensions 2 --distribution skewed --skewness 2 --bounds 0 1 --bounds 0 1 --query_range 0.01 0.01
# python synthetic_query_generator.py --query_type knn --n_queries 100 --dimensions 2 --distribution uniform --bounds 0 1 --bounds 0 1
# python synthetic_query_generator.py --query_type knn --n_queries 100 --dimensions 2 --distribution normal --bounds 0 1 --bounds 0 1
# python synthetic_query_generator.py --query_type knn --n_queries 100 --dimensions 2 --distribution skewed --skewness 2 --bounds 0 1 --bounds 0 1
# cd ..

# echo -e "${GREEN}Synthetic data and query are generated.${NC}"



# print_sub_step $YELLOW "3.2 Real Data & Query"



# # TODO  deal with real data and queries.

# print_step $YELLOW "Step 4: Learn RL-Spatial Indices"
# print_sub_step $GREEN "Step 4.1: Run Z-order"

# python tools/zorder.py data/synthetic/dataset/data_1000_2_normal.csv z_order_data.csv

# print_sub_step $GREEN "Step 4.2: Learn BMTree"

# python rl_baseline/bmtree_data_transfer.py data/synthetic/dataset/data_1000_2_normal.csv data/synthetic/query/range_100_2_normal_0.01x0.01.csv
# bash rl_baseline/learn_bmtree.sh data_1000_2_normal range_100_2_normal_0.01x0.01


# print_sub_step $YELLOW "Step 4.3: Learn RLRtree"
# print_sub_step $YELLOW "Step 4.4: Learn Qd-tree"


# print_step $YELLOW "Step 5: Run Experiments"

# print_sub_step $YELLOW "Step 5.1: Format Data and Query"

# python tools/libspatialindex_data_adapter.py --type data --input z_order_data.csv --output benchmark/libspatialindex/z_sorted_data

# python tools/libspatialindex_data_adapter.py --type data --is_scaled --input rl_baseline/Learned-BMTree/sorted_data_with_sfc.csv --output benchmark/libspatialindex/bmtree_sorted_data

# python tools/libspatialindex_data_adapter.py --type range_query --input data/synthetic/query/range_100_2_normal_0.01x0.01.csv --output benchmark/libspatialindex/range_100_2_normal_0.01x0.01
# python tools/libspatialindex_data_adapter.py --type knn_query --input data/synthetic/query/knn_100_2_normal.csv --output benchmark/libspatialindex/knn_100_2_normal



# print_sub_step $YELLOW "Step 5.1: SFCRtree"

# # comment this to avoid the verification of the query results
# RUN_EXHAUSTIVE_SEARCH=1

# function prepare_output_directory() {
#     local output_path="$1"
#     local directory_path="$(dirname "$output_path")"

#     if [ ! -d "$directory_path" ]; then
#         echo "Creating directory: $directory_path"
#         mkdir -p "$directory_path"
#     else
#         echo "Directory already exists: $directory_path"
#     fi
# }

# function test_libspatialindex_sfcrtree() {

#     z_sorted_data="benchmark/libspatialindex/$1"
#     range_query="benchmark/libspatialindex/$2"
#     knn_query="benchmark/libspatialindex/$3"
#     k_size="$4"
#     index_name="result/libspatialindex/$5"
#     tag="$6"

#     build_output_path="$index_name/build/$tag.txt"
#     range_output_path="$index_name/range/$tag.txt"
#     knn_output_path="$index_name/knn/$tag.txt"

#     prepare_output_directory "$build_output_path"
#     prepare_output_directory "$range_output_path"
#     prepare_output_directory "$knn_output_path"

#     echo -e "${RED}Change output to save time.${NC}"

#     echo "Starting R-Tree bulk load using sorted data: $z_sorted_data"
#     test-rtree-SFCRTreeBulkLoad "$z_sorted_data" tree 100 0.9  2> "$build_output_path"

#     echo "Querying R-Tree with range query file: $range_query"
#     test-rtree-RTreeQuery "$range_query" tree intersection > range_res 2> "$range_output_path"
#     cat $z_sorted_data $range_query > .t_range

#     if [[ $RUN_EXHAUSTIVE_SEARCH -eq 1 ]]; then
#         echo "Running exhaustive search"
#         test-rtree-Exhaustive .t_range intersection > range_res2
#     fi

#     echo "Querying R-Tree with KNN query file: $knn_query and K=$k_size"
#     test-rtree-RTreeQuery "$knn_query" tree 10NN > knn_res 2> "$knn_output_path"
#     cat $z_sorted_data $knn_query > .t_knn

#     if [[ $RUN_EXHAUSTIVE_SEARCH -eq 1 ]]; then
#         echo "Running exhaustive search"
#         test-rtree-Exhaustive .t_knn 10NN > knn_res2
#     fi

#     echo "Comparing results"
#     sort -n range_res > a
#     sort -n knn_res > c
#     if [[ $RUN_EXHAUSTIVE_SEARCH -eq 1 ]]; then
#         sort -n range_res2 > b
#         if diff a b > /dev/null; then
#             echo "(Range) Same results with exhaustive search. Everything seems fine."
#         else
#             echo "(Range) PROBLEM! We got different results from exhaustive search!"
#         fi

#         sort -n knn_res2 > d
#         if diff c d > /dev/null; then
#             echo "(KNN) Same results with exhaustive search. Everything seems fine."
#         else
#             echo "(KNN) PROBLEM! We got different results from exhaustive search!"
#         fi

#     fi
#     # echo "Results: $(wc -l a)"
#     # echo "Results: $(wc -l c)"
#     # echo "Results: $(wc -l d)"
#     rm -rf a b c d range_res range_res2 knn_res knn_res2 .t* tree.*
#     # cd ../../
# }

# # prepare data and query
# sorted_data_path="z_sorted_data"
# range_query_file="range_100_2_normal_0.01x0.01"
# knn_query_file="knn_100_2_normal"
# k_size=10

# # print_sub_step $YELLOW "Step 5.1.1: Z-order"
# echo -e "${GREEN}Run Zorder.${NC}"
# test_libspatialindex_sfcrtree "$sorted_data_path" "$range_query_file" "$knn_query_file" "$k_size" "zorder" "result1"

# # print_sub_step $GREEN "Step 5.1.2: BMTree"

# sorted_data_path="bmtree_sorted_data"
# test_libspatialindex_sfcrtree "$sorted_data_path" "$range_query_file" "$knn_query_file" "$k_size" "bmtree" "result1"

















# path" "$range_query_file" "$knn_query_file" "$k_size" "zorder" "result1"

# # print_sub_step $GREEN "Step 5.1.2: BMTree"

# sorted_data_path="bmtree_sorted_data"
# test_libspatialindex_sfcrtree "$sorted_data_path" "$range_query_file" "$knn_query_file" "$k_size" "bmtree" "result1"