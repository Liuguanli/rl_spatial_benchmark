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

BENCHMARK_LIBSPATIALINDEX = "benchmark/libspatialindex"

# QUERY_TYPE_RANGE = "range"
# QUERY_TYPE_KNN = "knn"

SYNTHETIC_DATA_FILENAME_TEMPLATE = "data_{size}_{dimensions}_{distribution}_{skewness}.csv"

REAL_DATA_FILENAME_TEMPLATE = "home/research/datasets/{data_distribution}_{data_size}.csv"
RELATIVE_REAL_DATA_FILENAME = "{data_distribution}_{data_size}.csv"

Z_BUILD_OUTPUT_PATH = "result/libspatialindex/zorder/build/{data_file_prefix}.txt"
Z_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/zorder/range/{data_file_prefix}_{range_query_prefix}.txt"
Z_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/zorder/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}.txt"
Z_ORDER_SORTED_OUTPUT = "benchmark/libspatialindex/z_sorted_data"
Z_ORDER_OUTPUT = "z-order_data.csv"


BMTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/bmtree/build/{data_file_prefix}_{query}_depth_{tree_depth}.txt"
BMTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/bmtree/range/{data_file_prefix}_{range_query_prefix}_depth_{tree_depth}.txt"
BMTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/bmtree/knn/{data_file_prefix}_{range_query_prefix}_depth_{tree_depth}_{knn_query_prefix}_k_{k}.txt"
BMTREE_INPUT = "rl_baseline/Learned-BMTree/sorted_data_with_sfc.csv"
BMTREE_OUTPUT = "benchmark/libspatialindex/bmtree_sorted_data"

RTREE_DATA = "benchmark/libspatialindex/rtree_data"
RTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/rtree/build/{data_file_prefix}_{variant}.txt"
RTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/rtree/range/{data_file_prefix}_{range_query_prefix}_{variant}.txt"
RTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/rtree/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_{variant}.txt"

RLRTREE_DATA = "benchmark/libspatialindex/rlrtree_data"
RLRTREE_TRAINING_DATA = "rl_baseline/RLRTree/"
RLRTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/rlrtree/build/{data_file_prefix}_{variant}.txt"
RLRTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/rlrtree/range/{data_file_prefix}_{range_query_prefix}_{variant}.txt"
RLRTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/rlrtree/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_{variant}.txt"

KDTREE_DATA = "benchmark/libspatialindex/kdtree_data"
KDTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/kdtree/build/{data_file_prefix}.txt"
KDTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/kdtree/range/{data_file_prefix}_{range_query_prefix}.txt"
KDTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/kdtree/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}.txt"

QDTREE_DATA = "benchmark/libspatialindex/qdtree_data"
QDTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/qdtree/build/{data_file_prefix}.txt"
QDTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/qdtree/range/{data_file_prefix}_{range_query_prefix}.txt"
QDTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/qdtree/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}.txt"

RANGE_QUERY_FILENAME_TEMPLATE = "{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{range_str}.csv"
KNN_QUERY_FILENAME_TEMPLATE = "{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}.csv"


REAL_RANGE_QUERY_FILENAME_TEMPLATE = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{range_str}.csv"
REAL_KNN_QUERY_FILENAME_TEMPLATE = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}.csv"

