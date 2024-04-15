# #!/bin/bash

# # 假设你的JSON文件名为config.json
# json_file="config.json"

# # 解析data部分
# data_size=$(jq -r '.data.size' "$json_file")
# data_dimensions=$(jq -r '.data.dimensions' "$json_file")
# data_distribution=$(jq -r '.data.distribution' "$json_file")
# data_skewness=$(jq -r '.data.skewness' "$json_file")
# data_bounds=$(jq -r '.data.bounds[] | @csv' "$json_file" | sed 's/"//g')

# range_params=""

# while IFS= read -r bound; do
#     bound=$(echo "$bound" | sed 's/,/ /g')
#     range_params+="--range $bound "
# done <<< "$data_bounds"

# # echo "range_params: $range_params"


# echo "Data Size: $data_size"
# echo "Data Dimensions: $data_dimensions"
# echo "Data Distribution: $data_distribution"
# echo "Data Skewness: $data_skewness"
# echo "Data Bounds: $range_params"

# # 解析query数组
# echo "Queries:"
# jq -c '.query[]' "$json_file" | while read -r query; do
#     query_type=$(echo "$query" | jq -r '.type')
#     query_size=$(echo "$query" | jq -r '.size')
#     query_dimensions=$(echo "$query" | jq -r '.dimensions')
#     query_distribution=$(echo "$query" | jq -r '.distribution')
#     query_skewness=$(echo "$query" | jq -r '.skewness')
#     query_bounds=$(echo "$query" | jq -r '.bounds[] | @csv' | sed 's/"//g')
    
#     echo "  Type: $query_type"
#     echo "  Size: $query_size"
#     echo "  Dimensions: $query_dimensions"
#     echo "  Distribution: $query_distribution"
#     echo "  Skewness: $query_skewness"
#     echo "  Bounds: $query_bounds"

#     # 解析query部分的bounds

#     # 初始化query range参数字符串
#     query_bounds_params=""

#     # 构造每个维度的--range参数
#     while IFS= read -r bound; do
#         # 将逗号替换为空格，用于分隔min和max值
#         bound=$(echo "$bound" | sed 's/,/ /g')
#         # 添加到query range参数字符串
#         query_bounds_params+="--range $bound "
#     done <<< "$query_bounds"

#     # 显示构造好的query range参数
#     echo "query_bounds: $query_bounds_params"
    
#     # 特别处理query_range和k
#     if [ "$query_type" == "range" ]; then
#         # 假设query_range是从特定查询中解析的
#         query_range_values=$(echo "$query" | jq -r '.query_range[]')

#         # 初始化query range参数字符串
#         query_range_params="--query_range"

#         # 遍历每个维度的query range并构造参数
#         for val in $query_range_values; do
#             query_range_params+=" $val"
#         done

#         # 显示构造好的query range参数
#         echo "$query_range_params"
#     elif [ "$query_type" == "knn" ]; then
#         k=$(echo "$query" | jq -r '.k | @csv')
#         echo "  K: $k"
#     fi
# done

# # 解析baseline数组
# echo "Baselines:"
# jq -c '.baseline[]' "$json_file" | while read -r baseline; do
#     baseline_name=$(echo "$baseline" | jq -r '.name')
#     echo "  Name: $baseline_name"
    
#     # 根据不同的baseline名称，处理其配置
#     if [ "$baseline_name" == "zorder" ]; then
#         page_size=$(echo "$baseline" | jq -r '.config.page_size')
#         fill_factor=$(echo "$baseline" | jq -r '.config.fill_factor')
#         echo "  Page Size: $page_size"
#         echo "  Fill Factor: $fill_factor"
#     elif [ "$baseline_name" == "bmtree" ]; then
#         max_depth=$(echo "$baseline" | jq -r '.config.max_depth')
#         echo "  Max Depth: $max_depth"
#     fi
# done


# 假设你的JSON文件名为config.json
json_file="config.json"
counter=0

rm -rf ./data/synthetic/*
rm -rf ./data/real/*

# 解析实验数组
jq -c '.experiments[]' "$json_file" | while read -r experiment; do

    ((counter++))  # 递增计数器
    echo "-----------------Processing experiment #$counter-----------------"

    cd data || exit

    # 解析data部分
    data_size=$(echo "$experiment" | jq -r '.data.size')
    data_dimensions=$(echo "$experiment" | jq -r '.data.dimensions')
    data_distribution=$(echo "$experiment" | jq -r '.data.distribution')
    data_skewness=$(echo "$experiment" | jq -r '.data.skewness')
    data_bounds=$(echo "$experiment" | jq -r '.data.bounds[] | @csv' | sed 's/"//g')

    range_params=""
    while IFS= read -r bound; do
        bound=$(echo "$bound" | sed 's/,/ /g')
        range_params+="--range $bound "
    done <<< "$data_bounds"

    # echo "Data Size: $data_size"
    # echo "Data Dimensions: $data_dimensions"
    # echo "Data Distribution: $data_distribution"
    # echo "Data Skewness: $data_skewness"
    # echo "Data Bounds: $range_params"

    python synthetic_data_generator.py --size $data_size --dimensions $data_dimensions --distribution $data_distribution --skewness $data_skewness $range_params


    # 解析query数组
    echo "Queries:"
    echo "$experiment" | jq -c '.query[]' | while read -r query; do
        query_type=$(echo "$query" | jq -r '.type')
        query_size=$(echo "$query" | jq -r '.size')
        query_dimensions=$(echo "$query" | jq -r '.dimensions')
        query_distribution=$(echo "$query" | jq -r '.distribution')
        query_skewness=$(echo "$query" | jq -r '.skewness')
        query_bounds=$(echo "$query" | jq -r '.bounds[] | @csv' | sed 's/"//g')
        query_bounds_params=""
        while IFS= read -r bound; do
            bound=$(echo "$bound" | sed 's/,/ /g')
            query_bounds_params+="--bounds $bound "
        done <<< "$query_bounds"

        echo "  Type: $query_type"
        echo "  Size: $query_size"
        echo "  Dimensions: $query_dimensions"
        echo "  Distribution: $query_distribution"
        echo "  Skewness: $query_skewness"
        echo "  Bounds: $query_bounds"
        echo "query_bounds: $query_bounds_params"

        if [ "$query_type" == "range" ]; then
            query_range_values=$(echo "$query" | jq -r '.query_range[]')

            query_range_params="--query_range"

            # 遍历每个维度的query range并构造参数
            for val in $query_range_values; do
                query_range_params+=" $val"
            done

            # 显示构造好的query range参数
            echo "$query_range_params"

            python synthetic_query_generator.py --query_type $query_type --n_queries $query_size --dimensions $query_dimensions --distribution $query_distribution --skewness $query_skewness $query_bounds_params $query_range_params

        elif [ "$query_type" == "knn" ]; then
            python synthetic_query_generator.py --query_type $query_type --n_queries $query_size --dimensions $query_dimensions --distribution $query_distribution --skewness $query_skewness $query_bounds_params
        fi
    done

    cd ..


    # 解析baseline数组
    echo "Baselines:"
    echo "$experiment" | jq -c '.baseline[]' | while read -r baseline; do
        baseline_name=$(echo "$baseline" | jq -r '.name')
        echo "  Name: $baseline_name"

        # echo "  Build index"
        # echo "  Execute range query"
        # echo "  Execute knn query"

        case $baseline_name in
            zorder)
                print_sub_step $GREEN "Run Z-order"
                python tools/zorder.py data/synthetic/dataset/data_1000_2_normal.csv z-order_data.csv
                
                ;;
            bmtree)
                print_sub_step $GREEN "Learn BMTree"
                python rl_baseline/bmtree_data_transfer.py data/synthetic/dataset/data_1000_2_normal.csv data/synthetic/query/range_100_2_normal_0.01x0.01.csv
                bash rl_baseline/learn_bmtree.sh data_1000_2_normal range_100_2_normal_0.01x0.01
                ;;
            rtree)
                echo "Executing logic for rtree"
                # 在这里添加针对 baseline3 的逻辑
                ;;
            rlrtree)
                echo "Executing logic for rlrtree"
                # 在这里添加针对 baseline4 的逻辑
                ;;
            kdtree)
                echo "Executing logic for kdtree"
                # 在这里添加针对 baseline5 的逻辑
                ;;
            qdtree)
                echo "Executing logic for qdtree"
                # 在这里添加针对 baseline6 的逻辑
                ;;
            *)
                echo "Baseline name $baseline_name is not recognized. Skipping."
                ;;
        esac


    done

    rm -rf ./data/synthetic/*
    rm -rf ./data/real/*

    # remove libspatialindex data files
    # remove sorted bmtree files
    # remove z-order_data.csv

    echo "-----------------Finish experiment #$counter-----------------"
done




