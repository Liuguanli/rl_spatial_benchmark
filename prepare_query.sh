#!/bin/bash
if [ $# -ne 8 ]; then
    echo "Usage: $0 <data_distribution> <query_type> <query_num> <query_distribution> <skewness> <min_range> <max_range> <dimensions>"
    exit 1
fi


data_distribution=$1
query_type=$2
query_num=$3
query_distribution=$4
skewness=$5
min_range=$6
max_range=$7
dimensions=$8

echo "Data Distribution: $data_distribution"
echo "Query type: $query_type"
echo "Query Number: $query_num"
echo "Query Distribution: $query_distribution"
echo "Skewness: $skewness"
echo "Data Range: Min=$min_range Max=$max_range"
echo "Dimensions: $dimensions"


cd data || exit

python synthetic_query_generator.py --query_type $query_type --n_queries $query_num --dimensions $dimensions --distribution $query_distribution --bounds $min_range $max_range --bounds $min_range $max_range --query_range 0.01 0.01
# python synthetic_query_generator.py --query_type range --n_queries 100 --dimensions 2 --distribution normal --bounds 0 1 --bounds 0 1 --query_range 0.01 0.01
# python synthetic_query_generator.py --query_type range --n_queries 100 --dimensions 2 --distribution skewed --skewness 2 --bounds 0 1 --bounds 0 1 --query_range 0.01 0.01
# python synthetic_query_generator.py --query_type knn --n_queries 100 --dimensions 2 --distribution uniform --bounds 0 1 --bounds 0 1
# python synthetic_query_generator.py --query_type knn --n_queries 100 --dimensions 2 --distribution normal --bounds 0 1 --bounds 0 1
# python synthetic_query_generator.py --query_type knn --n_queries 100 --dimensions 2 --distribution skewed --skewness 2 --bounds 0 1 --bounds 0 1

cd ..