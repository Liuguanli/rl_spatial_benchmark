
#!/bin/bash
if [ $# -ne 6 ]; then
    echo "Usage: $0 <data_num> <data_distribution> <skewness> <min_range> <max_range> <dimensions>"
    exit 1
fi

data_num=$1
data_distribution=$2
skewness=$3
min_range=$4
max_range=$5
dimensions=$6

echo "Data Number: $data_num"
echo "Data Distribution: $data_distribution"
echo "Skewness: $skewness"
echo "Data Range: Min=$min_range Max=$max_range"
echo "Dimensions: $dimensions"

rm -rf ./data/synthetic/*
rm -rf ./data/real/*
cd data || exit

valid_distributions="uniform normal skewed"
if [[ $valid_distributions =~ $data_distribution ]]; then
    echo "Generating synthetic data with distribution: $data_distribution"
    
    if [ "$data_distribution" == "skewed" ]; then
        python synthetic_data_generator.py --size $data_num --dimensions $dimensions --distribution skewed --skewness $skewness_value --range $min_range $max_range --range $min_range $max_range
    else
        python synthetic_data_generator.py --size $data_num --dimensions $dimensions --distribution $data_distribution --range $min_range $max_range --range $min_range $max_range
    fi
else
    echo "Processing real data with name or tag: $data_distribution"
fi

cd ..

# ./your_script.sh 1000 uniform 100 gaussian 0 100



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