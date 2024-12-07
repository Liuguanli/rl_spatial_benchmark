# constants.py

SEED = 42

LOG_LEVEL = "DEBUG"  #DEBUG, WARNING, INFO, ERROR, CRITICAL

CONFIG_DIR = "exp_config"

SYNTHETIC_PATH = "data/synthetic"
SYNTHETIC_DATA_PATH = "data/synthetic/dataset"
SYNTHETIC_QUERY_PATH = "data/synthetic/query"
REAL_DATA_PATH = "data/real/dataset"
REAL_QUERY_PATH = "data/real/query"

SYNTHETIC_WORKLOAD_PATH = "data/synthetic/workloads"
REAL_WORKLOAD_PATH = "data/real/workloads"

IS_HDD = False

INDEX_PATH = "/media/liuguanli/DATA" if IS_HDD else "./benchmark"

# use this flag to remove generated files if space is limited
SAVE_SPACE = False
RUN_EXHAUSTIVE_SEARCH = False  # TODO uncomment the printing code first in e.g., libspatialindex/test/rtree/RTreeQuery.cc line 77
RUN_EXAMPLE = False
RUN_ALL_BASELINE_EXAMPLE = False

BLOCK_SIZE_SUFFIX = 4
BLOCK_SIZE = 1024 * BLOCK_SIZE_SUFFIX
BUFFER = 0

BENCHMARK_LIBSPATIALINDEX = "benchmark/libspatialindex"

SYNTHETIC_DATA_FILENAME_TEMPLATE = "data_{size}_{dimensions}_{distribution}_{skewness}.csv"

REAL_DATA_FILENAME_TEMPLATE = "home/research/datasets/{data_distribution}_{data_size}.csv"
RELATIVE_REAL_DATA_FILENAME = "{data_distribution}_{data_size}.csv"

DISK_TYPE = "HDD" if IS_HDD else "SSD"

Z_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/build/{data_file_prefix}_bits_{bit_num}.txt"
Z_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}.txt"
Z_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_bits_{bit_num}.txt"
Z_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/point/{data_file_prefix}_{point_query_prefix}_bits_{bit_num}.txt"
Z_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/insert/{data_file_prefix}_{insert_prefix}_bits_{bit_num}.txt"
Z_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/insert_point/{data_file_prefix}_{insert_point_prefix}_bits_{bit_num}.txt"
Z_ORDER_SORTED_OUTPUT = "benchmark/model/z_sorted_data"
Z_ORDER_OUTPUT = "benchmark/model/z_order_data.csv"
Z_ORDER_SORTED_DEFAULT = "benchmark/model/z_order_data_{data_file_prefix}_bits_{bit_num}"

ZM_DATA = "benchmark/libspatialindex/zm_data"
ZM_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/build/{data_file_prefix}_bits_{bit_num}.txt"
ZM_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}.txt"
ZM_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_bits_{bit_num}.txt"
ZM_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/point/{data_file_prefix}_{point_query_prefix}_bits_{bit_num}.txt"
# ZM_PARTITION_OUTPUT_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}.txt"
# ZM_PARTITION_OUTPUT_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}.txt"


RANK_SPACE_Z_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/build/{data_file_prefix}_bits_{bit_num}.txt"
RANK_SPACE_Z_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}.txt"
RANK_SPACE_Z_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_bits_{bit_num}.txt"
RANK_SPACE_Z_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/point/{data_file_prefix}_{point_query_prefix}_bits_{bit_num}.txt"
RANK_SPACE_Z_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/insert/{data_file_prefix}_{insert_prefix}_bits_{bit_num}.txt"
RANK_SPACE_Z_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/insert_point/{data_file_prefix}_{insert_point_prefix}_bits_{bit_num}.txt"
RANK_SPACE_Z_ORDER_SORTED_OUTPUT = "benchmark/model/rankspace_z_sorted_data"
RANK_SPACE_Z_ORDER_OUTPUT = "benchmark/model/rankspace_z_order_data.csv"
RANK_SPACE_Z_ORDER_SORTED_DEFAULT = "benchmark/model/rankspace_z_order_data_{data_file_prefix}_bits_{bit_num}"

BMTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/build/{data_file_prefix}_{query}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_INPUT = "rl_baseline/Learned-BMTree/sorted_data_with_sfc.csv"
BMTREE_OUTPUT_DEFAULT = "benchmark/model/bmtree_sorted_data_{data_file_prefix}_{query}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}"
BMTREE_OUTPUT = "benchmark/model/bmtree_sorted_data"
BMTREE_MODEL_OUTPUT = "benchmark/model/learned_bmtree_{data_file_prefix}_{query}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_MODEL_OUTPUT_DEFAULT = "rl_baseline/Learned-BMTree/learned_bmtree.txt"

PLATON_PARTITION_OUTPUT = "benchmark/model/platon_partition_{data_file_prefix}_{query}.txt"
PLATON_DATA = "benchmark/libspatialindex/platon_data"

PLATON_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/build/{data_file_prefix}_{query}.txt"
PLATON_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/range/{data_file_prefix}_{range_query_prefix}.txt"
PLATON_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}.txt"
PLATON_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}.txt"
PLATON_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}.txt"
PLATON_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}.txt"

RTREE_DATA = "benchmark/libspatialindex/rtree_data"
RTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/build/{data_file_prefix}_{variant}.txt"
RTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/range/{data_file_prefix}_{range_query_prefix}_{variant}.txt"
RTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_{variant}.txt"
RTREE_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/point/{data_file_prefix}_{point_query_prefix}_{variant}.txt"
RTREE_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/insert/{data_file_prefix}_{insert_prefix}_{variant}.txt"
RTREE_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/insert_point/{data_file_prefix}_{insert_point_prefix}_{variant}.txt"

R_STAR_TREE_DATA = "benchmark/libspatialindex/r_star_tree_data"
R_STAR_TREE_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/build/{data_file_prefix}_{variant}.txt"
R_STAR_TREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/range/{data_file_prefix}_{range_query_prefix}_{variant}.txt"
R_STAR_TREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_{variant}.txt"
R_STAR_TREE_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/point/{data_file_prefix}_{point_query_prefix}_{variant}.txt"
R_STAR_TREE_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/insert/{data_file_prefix}_{insert_prefix}_{variant}.txt"
R_STAR_TREE_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/insert_point/{data_file_prefix}_{insert_point_prefix}_{variant}.txt"

RLRTREE_DATA = "benchmark/libspatialindex/rlrtree_data"
RLRTREE_TRAINING_DATA = "rl_baseline/RLRTree/"
RLRTREE_MODEL_PATH = "benchmark/model"
RLRTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/build/{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}.txt"
RLRTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/range/{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}.txt"
RLRTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}_{variant}_epoch_{epoch}_sample_{sample_size}.txt"
RLRTREE_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}.txt"
RLRTREE_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}.txt"
RLRTREE_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}.txt"
CHOOSE_SUBTREE_MODEL_NAME = "benchmark/model/choose_subtree.pth"
CHOOSE_SUBTREE_MODEL_NAME_DEFAULT = "benchmark/model/choose_subtree_{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}.pth"
SPLIT_MODEL_NAME = "benchmark/model/split.pth"
SPLIT_MODEL_NAME_DEFAULT = "benchmark/model/split_{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}.pth"

KDTREE_DATA = "benchmark/libspatialindex/kdtree_data"
KDTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/build/{data_file_prefix}.txt"
KDTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/range/{data_file_prefix}_{range_query_prefix}.txt"
KDTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}.txt"
KDTREE_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/point/{data_file_prefix}_{point_query_prefix}.txt"
KDTREE_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/insert/{data_file_prefix}_{insert_prefix}.txt"
KDTREE_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/insert_point/{data_file_prefix}_{insert_point_prefix}.txt"

KDTREE_GREEDY_DATA = "benchmark/libspatialindex/kdtree_greedy_data"
KDTREE_GREEDY_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/build/{data_file_prefix}_{range_query_prefix}.txt"
KDTREE_GREEDY_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/range/{data_file_prefix}_{range_query_prefix}.txt"
KDTREE_GREEDY_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}.txt"
KDTREE_GREEDY_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}.txt"
KDTREE_GREEDY_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}.txt"
KDTREE_GREEDY_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}.txt"

QDTREE_DATA = "benchmark/libspatialindex/qdtree_data"
QDTREE_MODEL_PATH = "benchmark/model"
QDTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/build/{data_file_prefix}_{range_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.txt"
QDTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/range/{data_file_prefix}_{range_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.txt"
QDTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.txt"
QDTREE_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.txt"
QDTREE_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.txt"
QDTREE_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.txt"
QDTREE_MODEL_NAME = "benchmark/model/qdtree.pth"
QDTREE_MODEL_NAME_DEFAULT = "benchmark/model/qdtree_{data_file_prefix}_{range_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.pth"


RANGE_QUERY_FILENAME_DEFAULT = "range_1000_2_uniform_1_0.001x0.001.csv"
RANGE_QUERY_FILENAME_TEMPLATE = "{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{range_str}.csv"
KNN_QUERY_FILENAME_TEMPLATE = "{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}.csv"
POINT_QUERY_FILENAME_TEMPLATE = "{query_type}_{n_queries}_{data}_{dimensions}_{distribution}_{skewness}.csv"
INSERT_FILENAME_TEMPLATE = "{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}.csv"
INSERT_POINT_FILENAME_TEMPLATE = "{query_type}_{n_queries}_{data}_{dimensions}_{distribution}_{skewness}_{frequency}.csv"

REAL_RANGE_QUERY_FILENAME_DEFAULT = "{data}_range_1000_2_uniform_1_0.001x0.001.csv"
REAL_RANGE_QUERY_FILENAME_TEMPLATE = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{range_str}.csv"
REAL_KNN_QUERY_FILENAME_TEMPLATE = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}.csv"
REAL_POINT_QUERY_FILENAME_TEMPLATE = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}.csv"
REAL_INSERT_FILENAME_TEMPLATE = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}.csv"
REAL_INSERT_POINT_FILENAME_TEMPLATE = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{frequency}.csv"
