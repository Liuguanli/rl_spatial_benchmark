# constants.py

SEED = 42



CONFIG_DIR = "exp_config"

SYNTHETIC_PATH = "data/synthetic"
SYNTHETIC_DATA_PATH = "data/synthetic/dataset"
SYNTHETIC_QUERY_PATH = "data/synthetic/query"
REAL_DATA_PATH = "data/real/dataset"
REAL_QUERY_PATH = "data/real/query"

# use this flag to remove generated files if space is limited
SAVE_SPACE = False
RUN_EXHAUSTIVE_SEARCH = False  # TODO uncomment the printing code first in e.g., libspatialindex/test/rtree/RTreeQuery.cc line 77
RUN_EXAMPLE = True
RUN_ALL_BASELINE_EXAMPLE = False

BENCHMARK_LIBSPATIALINDEX = "benchmark/libspatialindex"

# QUERY_TYPE_RANGE = "range"
# QUERY_TYPE_KNN = "knn"

SYNTHETIC_DATA_FILENAME_TEMPLATE = "data_{size}_{dimensions}_{distribution}_{skewness}.csv"

REAL_DATA_FILENAME_TEMPLATE = "home/research/datasets/{data_distribution}_{data_size}.csv"
RELATIVE_REAL_DATA_FILENAME = "{data_distribution}_{data_size}.csv"

Z_BUILD_OUTPUT_PATH = "result/libspatialindex/zorder/build/{data_file_prefix}_bits_{bit_num}.txt"
Z_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/zorder/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}.txt"
Z_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/zorder/knn/{data_file_prefix}_{knn_query_prefix}_bits_{bit_num}_k_{k}.txt"
Z_ORDER_SORTED_OUTPUT = "benchmark/libspatialindex/z_sorted_data"
Z_ORDER_OUTPUT = "z_order_data.csv"

RANK_SPACE_Z_BUILD_OUTPUT_PATH = "result/libspatialindex/rankspace_zorder/build/{data_file_prefix}_bits_{bit_num}.txt"
RANK_SPACE_Z_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/rankspace_zorder/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}.txt"
RANK_SPACE_Z_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/rankspace_zorder/knn/{data_file_prefix}_{knn_query_prefix}_bits_{bit_num}_k_{k}.txt"
RANK_SPACE_Z_ORDER_SORTED_OUTPUT = "benchmark/libspatialindex/rankspace_z_sorted_data"
RANK_SPACE_Z_ORDER_OUTPUT = "rankspace_z_order_data.csv"

BMTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/bmtree/build/{data_file_prefix}_{query}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/bmtree/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/bmtree/knn/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_{knn_query_prefix}_k_{k}.txt"
BMTREE_INPUT = "rl_baseline/Learned-BMTree/sorted_data_with_sfc.csv"
BMTREE_OUTPUT = "benchmark/libspatialindex/bmtree_sorted_data"

RTREE_DATA = "benchmark/libspatialindex/rtree_data"
RTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/rtree/build/{data_file_prefix}_{variant}.txt"
RTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/rtree/range/{data_file_prefix}_{range_query_prefix}_{variant}.txt"
RTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/rtree/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_{variant}.txt"

R_STAR_TREE_DATA = "benchmark/libspatialindex/r_star_tree_data"
R_STAR_TREE_BUILD_OUTPUT_PATH = "result/libspatialindex/r_star_tree/build/{data_file_prefix}_{variant}.txt"
R_STAR_TREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/r_star_tree/range/{data_file_prefix}_{range_query_prefix}_{variant}.txt"
R_STAR_TREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/r_star_tree/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_{variant}.txt"

RLRTREE_DATA = "benchmark/libspatialindex/rlrtree_data"
RLRTREE_TRAINING_DATA = "rl_baseline/RLRTree/"
RLRTREE_MODEL_PATH = "benchmark/libspatialindex"
RLRTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/rlrtree/build/{data_file_prefix}_{variant}_epoch_{epoch}.txt"
RLRTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/rlrtree/range/{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}.txt"
RLRTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/rlrtree/knn/{data_file_prefix}_{range_query_prefix}_epoch_{epoch}_{knn_query_prefix}_k_{k}_{variant}.txt"

KDTREE_DATA = "benchmark/libspatialindex/kdtree_data"
KDTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/kdtree/build/{data_file_prefix}.txt"
KDTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/kdtree/range/{data_file_prefix}_{range_query_prefix}.txt"
KDTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/kdtree/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}.txt"

KDTREE_GREEDY_DATA = "benchmark/libspatialindex/kdtree_greedy_data"
KDTREE_GREEDY_BUILD_OUTPUT_PATH = "result/libspatialindex/kdtree_greedy/build/{data_file_prefix}_{range_query_prefix}.txt"
KDTREE_GREEDY_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/kdtree_greedy/range/{data_file_prefix}_{range_query_prefix}.txt"
KDTREE_GREEDY_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/kdtree_greedy/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}.txt"

QDTREE_DATA = "benchmark/libspatialindex/qdtree_data"
QDTREE_MODEL_PATH = "benchmark/libspatialindex"
QDTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/qdtree/build/{data_file_prefix}_{range_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.txt"
QDTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/qdtree/range/{data_file_prefix}_{range_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.txt"
QDTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/qdtree/knn/{data_file_prefix}_{range_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}_{knn_query_prefix}_k_{k}.txt"

RANGE_QUERY_FILENAME_TEMPLATE = "{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{range_str}.csv"
KNN_QUERY_FILENAME_TEMPLATE = "{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}.csv"

REAL_RANGE_QUERY_FILENAME_TEMPLATE = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{range_str}.csv"
REAL_KNN_QUERY_FILENAME_TEMPLATE = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}.csv"

