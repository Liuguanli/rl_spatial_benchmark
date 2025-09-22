import os
from dotenv import load_dotenv

# load .env
load_dotenv()

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

DATA_SET_PATH = "/home/research/datasets/"
# DATA_SET_PATH = "/media/liuguanli/T7/Ubuntu_Datasets/RL_spatial_data/real/dataset/"

IS_HDD = True

HDD_PATH = os.getenv('HDD_PATH')
SSD_PATH = os.getenv('SSD_PATH')
INDEX_PATH = HDD_PATH if IS_HDD else SSD_PATH

# use this flag to remove generated files if space is limited
SAVE_SPACE = False
RUN_EXHAUSTIVE_SEARCH = False 
RUN_EXAMPLE = False
RUN_ALL_BASELINE_EXAMPLE = False

BLOCK_SIZE_SUFFIX = 4
BLOCK_SIZE = 1024 * BLOCK_SIZE_SUFFIX
BUFFER = 0

BENCHMARK_LIBSPATIALINDEX = "benchmark/libspatialindex"

SYNTHETIC_DATA_FILENAME_TEMPLATE = "data_{size}_{dimensions}_{distribution}_{skewness}.csv"
SYNTHETIC_DATA_FILENAME_TEMPLATE_3D = "data_{size}_{dimensions}_{distribution}_{skewness}_3d.csv"

REAL_DATA_FILENAME_TEMPLATE = "home/research/datasets/{data_distribution}_{data_size}.csv"
REAL_DATA_FILENAME_TEMPLATE_3D = "home/research/datasets/{data_distribution}_{data_size}_3d.csv"
RELATIVE_REAL_DATA_FILENAME = "{data_distribution}_{data_size}.csv"
RELATIVE_REAL_DATA_FILENAME_3D = "{data_distribution}_{data_size}_3d.csv"

DISK_TYPE = "HDD" if IS_HDD else "SSD"

Z_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/build/{data_file_prefix}_bits_{bit_num}.txt"
Z_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}.txt"
Z_JOIN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/join/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}.txt"
Z_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_bits_{bit_num}.txt"
Z_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/point/{data_file_prefix}_{point_query_prefix}_bits_{bit_num}.txt"
Z_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/insert/{data_file_prefix}_{insert_prefix}_bits_{bit_num}.txt"
Z_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/insert_point/{data_file_prefix}_{insert_point_prefix}_bits_{bit_num}.txt"
Z_ORDER_SORTED_OUTPUT = "benchmark/model/z_sorted_data"
Z_ORDER_OUTPUT = "benchmark/model/z_order_data.csv"
Z_ORDER_SORTED_DEFAULT = "benchmark/model/z_order_data_{data_file_prefix}_bits_{bit_num}"

Z_BUILD_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/build/{data_file_prefix}_bits_{bit_num}_3d.txt"
Z_RANGE_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}_3d.txt"
Z_JOIN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/join/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}_3d.txt"
Z_KNN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_bits_{bit_num}_3d.txt"
Z_POINT_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/point/{data_file_prefix}_{point_query_prefix}_bits_{bit_num}_3d.txt"
Z_INSERT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/insert/{data_file_prefix}_{insert_prefix}_bits_{bit_num}_3d.txt"
Z_INSERT_POINT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zorder/insert_point/{data_file_prefix}_{insert_point_prefix}_bits_{bit_num}_3d.txt"
Z_ORDER_SORTED_OUTPUT_3D = "benchmark/model/z_sorted_data_3d"
Z_ORDER_OUTPUT_3D = "benchmark/model/z_order_data_3d.csv"
Z_ORDER_SORTED_DEFAULT_3D = "benchmark/model/z_order_data_{data_file_prefix}_bits_{bit_num}_3d"

ZM_DATA = "benchmark/libspatialindex/zm_data"
ZM_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/build/{data_file_prefix}_bits_{bit_num}.txt"
ZM_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}.txt"
ZM_JOIN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/join/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}.txt"
ZM_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_bits_{bit_num}.txt"
ZM_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/point/{data_file_prefix}_{point_query_prefix}_bits_{bit_num}.txt"
ZM_PARTITION_OUTPUT_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/insert/{data_file_prefix}_{insert_prefix}_bits_{bit_num}.txt"
ZM_PARTITION_OUTPUT_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/insert_point/{data_file_prefix}_{insert_point_prefix}_bits_{bit_num}.txt"

ZM_DATA_3D = "benchmark/libspatialindex/zm_data"
ZM_BUILD_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/build/{data_file_prefix}_bits_{bit_num}_3d.txt"
ZM_RANGE_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}_3d.txt"
ZM_JOIN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/join/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}_3d.txt"
ZM_KNN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_bits_{bit_num}_3d.txt"
ZM_POINT_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/point/{data_file_prefix}_{point_query_prefix}_bits_{bit_num}_3d.txt"
ZM_PARTITION_OUTPUT_INSERT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/insert/{data_file_prefix}_{insert_prefix}_bits_{bit_num}_3d.txt"
ZM_PARTITION_OUTPUT_INSERT_POINT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/zm/insert_point/{data_file_prefix}_{insert_point_prefix}_bits_{bit_num}_3d.txt"


LISA_DATA = "benchmark/libspatialindex/lisa_data"
LISA_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/lisa/build/{data_file_prefix}.txt"
LISA_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/lisa/range/{data_file_prefix}_{range_query_prefix}.txt"
LISA_JOIN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/lisa/join/{data_file_prefix}_{range_query_prefix}.txt"
LISA_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/lisa/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}.txt"
LISA_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/lisa/point/{data_file_prefix}_{point_query_prefix}.txt"
LISA_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/lisa/insert/{data_file_prefix}_{insert_prefix}.txt"
LISA_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/lisa/insert_point/{data_file_prefix}_{insert_point_prefix}.txt"


LISA_DATA_3D = "benchmark/libspatialindex/lisa_data"
LISA_BUILD_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/lisa/build/{data_file_prefix}_3d.txt"
LISA_RANGE_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/lisa/range/{data_file_prefix}_{range_query_prefix}_3d.txt"
LISA_JOIN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/lisa/join/{data_file_prefix}_{range_query_prefix}_3d.txt"
LISA_KNN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/lisa/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_3d.txt"
LISA_POINT_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/lisa/point/{data_file_prefix}_{point_query_prefix}_3d.txt"
LISA_INSERT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/lisa/insert/{data_file_prefix}_{insert_prefix}_3d.txt"
LISA_INSERT_POINT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/lisa/insert_point/{data_file_prefix}_{insert_point_prefix}_3d.txt"


RANK_SPACE_Z_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/build/{data_file_prefix}_bits_{bit_num}.txt"
RANK_SPACE_Z_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}.txt"
RANK_SPACE_Z_JOIN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/join/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}.txt"
RANK_SPACE_Z_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_bits_{bit_num}.txt"
RANK_SPACE_Z_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/point/{data_file_prefix}_{point_query_prefix}_bits_{bit_num}.txt"
RANK_SPACE_Z_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/insert/{data_file_prefix}_{insert_prefix}_bits_{bit_num}.txt"
RANK_SPACE_Z_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/insert_point/{data_file_prefix}_{insert_point_prefix}_bits_{bit_num}.txt"
RANK_SPACE_Z_ORDER_SORTED_OUTPUT = "benchmark/model/rankspace_z_sorted_data"
RANK_SPACE_Z_ORDER_OUTPUT = "benchmark/model/rankspace_z_order_data.csv"
RANK_SPACE_Z_ORDER_SORTED_DEFAULT = "benchmark/model/rankspace_z_order_data_{data_file_prefix}_bits_{bit_num}"

RANK_SPACE_Z_BUILD_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/build/{data_file_prefix}_bits_{bit_num}_3d.txt"
RANK_SPACE_Z_RANGE_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}_3d.txt"
RANK_SPACE_Z_JOIN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/join/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}_3d.txt"
RANK_SPACE_Z_KNN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_bits_{bit_num}_3d.txt"
RANK_SPACE_Z_POINT_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/point/{data_file_prefix}_{point_query_prefix}_bits_{bit_num}_3d.txt"
RANK_SPACE_Z_INSERT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/insert/{data_file_prefix}_{insert_prefix}_bits_{bit_num}_3d.txt"
RANK_SPACE_Z_INSERT_POINT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rankspace_zorder/insert_point/{data_file_prefix}_{insert_point_prefix}_bits_{bit_num}_3d.txt"
RANK_SPACE_Z_ORDER_SORTED_OUTPUT_3D = "benchmark/model/rankspace_z_sorted_data_3d"
RANK_SPACE_Z_ORDER_OUTPUT_3D = "benchmark/model/rankspace_z_order_data_3d.csv"
RANK_SPACE_Z_ORDER_SORTED_DEFAULT_3D = "benchmark/model/rankspace_z_order_data_{data_file_prefix}_bits_{bit_num}_3d"


BMTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/build/{data_file_prefix}_{query}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_JOIN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/join/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_INPUT = "rl_baseline/Learned-BMTree/sorted_data_with_sfc.csv"
BMTREE_OUTPUT_DEFAULT = "benchmark/model/bmtree_sorted_data_{data_file_prefix}_{query}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}"
BMTREE_OUTPUT = "benchmark/model/bmtree_sorted_data"
BMTREE_MODEL_OUTPUT = "benchmark/model/learned_bmtree_{data_file_prefix}_{query}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREE_MODEL_OUTPUT_DEFAULT = "rl_baseline/Learned-BMTree/learned_bmtree.txt"

BMTREE_BUILD_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/build/{data_file_prefix}_{query}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d.txt"
BMTREE_RANGE_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d.txt"
BMTREE_JOIN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/join/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d.txt"
BMTREE_KNN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d.txt"
BMTREE_POINT_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d.txt"
BMTREE_INSERT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d.txt"
BMTREE_INSERT_POINT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d.txt"
BMTREE_INPUT_3D = "rl_baseline/Learned-BMTree/sorted_data_with_sfc_3d.csv"
BMTREE_OUTPUT_DEFAULT_3D = "benchmark/model/bmtree_sorted_data_{data_file_prefix}_{query}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d"
BMTREE_OUTPUT_3D = "benchmark/model/bmtree_sorted_data_3d"
BMTREE_MODEL_OUTPUT_3D = "benchmark/model/learned_bmtree_{data_file_prefix}_{query}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d.txt"
BMTREE_MODEL_OUTPUT_DEFAULT_3D = "rl_baseline/Learned-BMTree/learned_bmtree_3d.txt"


BMTREEIMPR_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree_impr/build/{data_file_prefix}_{query}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREEIMPR_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree_impr/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREEIMPR_JOIN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree_impr/join/{data_file_prefix}_{range_query_prefix}_{join_query_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREEIMPR_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree_impr/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREEIMPR_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree_impr/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREEIMPR_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree_impr/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREEIMPR_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree_impr/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREEIMPR_INPUT = "rl_baseline/Learned-BMTree/sorted_data_with_sfc.csv"
BMTREEIMPR_OUTPUT_DEFAULT = "benchmark/model/bmtree_impr_sorted_data_{data_file_prefix}_{query}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}"
BMTREEIMPR_OUTPUT = "benchmark/model/bmtree_impr_sorted_data"
BMTREEIMPR_MODEL_OUTPUT = "benchmark/model/learned_bmtree_impr_{data_file_prefix}_{query}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}.txt"
BMTREEIMPR_MODEL_OUTPUT_DEFAULT = "rl_baseline/Learned-BMTree/learned_bmtree_impr.txt"

BMTREEIMPR_BUILD_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree_impr/build/{data_file_prefix}_{query}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d.txt"
BMTREEIMPR_RANGE_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree_impr/range/{data_file_prefix}_{range_query_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d.txt"
BMTREEIMPR_JOIN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree_impr/join/{data_file_prefix}_{range_query_prefix}_{join_query_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d.txt"
BMTREEIMPR_KNN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree_impr/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d.txt"
BMTREEIMPR_POINT_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree_impr/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d.txt"
BMTREEIMPR_INSERT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree_impr/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d.txt"
BMTREEIMPR_INSERT_POINT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/bmtree_impr/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d.txt"
BMTREEIMPR_INPUT_3D = "rl_baseline/Learned-BMTree/sorted_data_with_sfc_3d.csv"
BMTREEIMPR_OUTPUT_DEFAULT_3D = "benchmark/model/bmtree_impr_sorted_data_{data_file_prefix}_{query}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d"
BMTREEIMPR_OUTPUT_3D = "benchmark/model/bmtree_impr_sorted_data_3d"
BMTREEIMPR_MODEL_OUTPUT_3D = "benchmark/model/learned_bmtree_impr_{data_file_prefix}_{query}_bits_{bit_num}_depth_{tree_depth}_sample_{sample_size}_3d.txt"
BMTREEIMPR_MODEL_OUTPUT_DEFAULT_3D = "rl_baseline/Learned-BMTree/learned_bmtree_impr_3d.txt"


PLATON_PARTITION_OUTPUT = "benchmark/model/platon_partition_{data_file_prefix}_{query}.txt"
PLATON_DATA = "benchmark/libspatialindex/platon_data"
PLATON_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/build/{data_file_prefix}_{query}.txt"
PLATON_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/range/{data_file_prefix}_{range_query_prefix}.txt"
PLATON_JOIN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/join/{data_file_prefix}_{range_query_prefix}_{join_query_prefix}.txt"
PLATON_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}.txt"
PLATON_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}.txt"
PLATON_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}.txt"
PLATON_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}.txt"

PLATON_PARTITION_OUTPUT_3D = "benchmark/model/platon_partition_{data_file_prefix}_{query}_3d.txt"
PLATON_DATA_3D = "benchmark/libspatialindex/platon_data_3d"
PLATON_BUILD_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/build/{data_file_prefix}_{query}_3d.txt"
PLATON_RANGE_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/range/{data_file_prefix}_{range_query_prefix}_3d.txt"
PLATON_JOIN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/join/{data_file_prefix}_{range_query_prefix}_{join_query_prefix}_3d.txt"
PLATON_KNN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}_3d.txt"
PLATON_POINT_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}_3d.txt"
PLATON_INSERT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}_3d.txt"
PLATON_INSERT_POINT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/platon/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}_3d.txt"


RTREE_DATA = "benchmark/libspatialindex/rtree_data"
RTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/build/{data_file_prefix}_{variant}.txt"
RTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/range/{data_file_prefix}_{range_query_prefix}_{variant}.txt"
RTREE_JOIN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/join/{data_file_prefix}_{range_query_prefix}_{variant}.txt"
RTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_{variant}.txt"
RTREE_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/point/{data_file_prefix}_{point_query_prefix}_{variant}.txt"
RTREE_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/insert/{data_file_prefix}_{insert_prefix}_{variant}.txt"
RTREE_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/insert_point/{data_file_prefix}_{insert_point_prefix}_{variant}.txt"

RTREE_DATA_3D = "benchmark/libspatialindex/rtree_data"
RTREE_BUILD_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/build/{data_file_prefix}_{variant}_3d.txt"
RTREE_RANGE_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/range/{data_file_prefix}_{range_query_prefix}_{variant}_3d.txt"
RTREE_JOIN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/join/{data_file_prefix}_{range_query_prefix}_{variant}_3d.txt"
RTREE_KNN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_{variant}_3d.txt"
RTREE_POINT_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/point/{data_file_prefix}_{point_query_prefix}_{variant}_3d.txt"
RTREE_INSERT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/insert/{data_file_prefix}_{insert_prefix}_{variant}_3d.txt"
RTREE_INSERT_POINT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rtree/insert_point/{data_file_prefix}_{insert_point_prefix}_{variant}_3d.txt"


R_STAR_TREE_DATA = "benchmark/libspatialindex/r_star_tree_data"
R_STAR_TREE_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/build/{data_file_prefix}_{variant}.txt"
R_STAR_TREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/range/{data_file_prefix}_{range_query_prefix}_{variant}.txt"
R_STAR_TREE_JOIN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/join/{data_file_prefix}_{range_query_prefix}_{variant}.txt"
R_STAR_TREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_{variant}.txt"
R_STAR_TREE_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/point/{data_file_prefix}_{point_query_prefix}_{variant}.txt"
R_STAR_TREE_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/insert/{data_file_prefix}_{insert_prefix}_{variant}.txt"
R_STAR_TREE_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/insert_point/{data_file_prefix}_{insert_point_prefix}_{variant}.txt"

R_STAR_TREE_DATA_3D = "benchmark/libspatialindex/r_star_tree_data"
R_STAR_TREE_BUILD_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/build/{data_file_prefix}_{variant}_3d.txt"
R_STAR_TREE_RANGE_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/range/{data_file_prefix}_{range_query_prefix}_{variant}_3d.txt"
R_STAR_TREE_JOIN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/join/{data_file_prefix}_{range_query_prefix}_{variant}_3d.txt"
R_STAR_TREE_KNN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_{variant}_3d.txt"
R_STAR_TREE_POINT_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/point/{data_file_prefix}_{point_query_prefix}_{variant}_3d.txt"
R_STAR_TREE_INSERT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/insert/{data_file_prefix}_{insert_prefix}_{variant}_3d.txt"
R_STAR_TREE_INSERT_POINT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/r_star_tree/insert_point/{data_file_prefix}_{insert_point_prefix}_{variant}_3d.txt"


RLRTREE_DATA = "benchmark/libspatialindex/rlrtree_data"
RLRTREE_TRAINING_DATA = "rl_baseline/RLRTree/"
RLRTREE_MODEL_PATH = "benchmark/model"

RLRTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/build/{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}.txt"
RLRTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/range/{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}.txt"
RLRTREE_JOIN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/join/{data_file_prefix}_{range_query_prefix}_{join_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}.txt"
RLRTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}_{variant}_epoch_{epoch}_sample_{sample_size}.txt"
RLRTREE_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}.txt"
RLRTREE_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}.txt"
RLRTREE_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}.txt"

CHOOSE_SUBTREE_MODEL_NAME = "benchmark/model/choose_subtree.pth"
CHOOSE_SUBTREE_MODEL_NAME_DEFAULT = "benchmark/model/choose_subtree_{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}.pth"
SPLIT_MODEL_NAME = "benchmark/model/split.pth"
SPLIT_MODEL_NAME_DEFAULT = "benchmark/model/split_{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}.pth"


RLRTREE_BUILD_OUTPUT_PATH_TUNING = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/build/{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}_gamma_{gamma}_learning_rate_{learning_rate}_rl_method_{rl_method}.txt"
RLRTREE_RANGE_QUERY_OUTPUT_PATH_TUNING = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/range/{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}_gamma_{gamma}_learning_rate_{learning_rate}_rl_method_{rl_method}.txt"
RLRTREE_JOIN_QUERY_OUTPUT_PATH_TUNING = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/join/{data_file_prefix}_{range_query_prefix}_{join_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}_gamma_{gamma}_learning_rate_{learning_rate}_rl_method_{rl_method}.txt"
RLRTREE_KNN_QUERY_OUTPUT_PATH_TUNING = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}_{variant}_epoch_{epoch}_sample_{sample_size}_gamma_{gamma}_learning_rate_{learning_rate}_rl_method_{rl_method}.txt"
RLRTREE_POINT_QUERY_OUTPUT_PATH_TUNING = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}_gamma_{gamma}_learning_rate_{learning_rate}_rl_method_{rl_method}.txt"
RLRTREE_INSERT_OUTPUT_PATH_TUNING = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}_gamma_{gamma}_learning_rate_{learning_rate}_rl_method_{rl_method}.txt"
RLRTREE_INSERT_POINT_OUTPUT_PATH_TUNING = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}_gamma_{gamma}_learning_rate_{learning_rate}_rl_method_{rl_method}.txt"
CHOOSE_SUBTREE_MODEL_NAME_DEFAULT_TUNING = "benchmark/model/choose_subtree_{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}_gamma_{gamma}_learning_rate_{learning_rate}_rl_method_{rl_method}.pth"
SPLIT_MODEL_NAME_DEFAULT_TUNING = "benchmark/model/split_{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}_gamma_{gamma}_learning_rate_{learning_rate}_rl_method_{rl_method}.pth"




RLRTREE_DATA_3D = "benchmark/libspatialindex/rlrtree_data_3d"
RLRTREE_TRAINING_DATA_3D = "rl_baseline/RLRTree/"
RLRTREE_MODEL_PATH_3D = "benchmark/model"
RLRTREE_BUILD_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/build/{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}_3d.txt"
RLRTREE_RANGE_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/range/{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}_3d.txt"
RLRTREE_JOIN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/join/{data_file_prefix}_{range_query_prefix}_{join_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}_3d.txt"
RLRTREE_KNN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}_{variant}_epoch_{epoch}_sample_{sample_size}_3d.txt"
RLRTREE_POINT_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}_3d.txt"
RLRTREE_INSERT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}_3d.txt"
RLRTREE_INSERT_POINT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/rlrtree/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}_3d.txt"
# CHOOSE_SUBTREE_MODEL_NAME_3D = "benchmark/model/choose_subtree_3d.pth"
CHOOSE_SUBTREE_MODEL_NAME_DEFAULT_3D = "benchmark/model/choose_subtree_{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}_3d.pth"
# SPLIT_MODEL_NAME_3D = "benchmark/model/split_3d.pth"
SPLIT_MODEL_NAME_DEFAULT_3D = "benchmark/model/split_{data_file_prefix}_{range_query_prefix}_{variant}_epoch_{epoch}_sample_{sample_size}_3d.pth"


KDTREE_DATA = "benchmark/libspatialindex/kdtree_data"
KDTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/build/{data_file_prefix}.txt"
KDTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/range/{data_file_prefix}_{range_query_prefix}.txt"
KDTREE_JOIN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/join/{data_file_prefix}_{range_query_prefix}.txt"
KDTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}.txt"
KDTREE_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/point/{data_file_prefix}_{point_query_prefix}.txt"
KDTREE_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/insert/{data_file_prefix}_{insert_prefix}.txt"
KDTREE_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/insert_point/{data_file_prefix}_{insert_point_prefix}.txt"

KDTREE_DATA_3D = "benchmark/libspatialindex/kdtree_data_3d"
KDTREE_BUILD_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/build/{data_file_prefix}_3d.txt"
KDTREE_RANGE_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/range/{data_file_prefix}_{range_query_prefix}_3d.txt"
KDTREE_JOIN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/join/{data_file_prefix}_{range_query_prefix}_3d.txt"
KDTREE_KNN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/knn/{data_file_prefix}_{knn_query_prefix}_k_{k}_3d.txt"
KDTREE_POINT_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/point/{data_file_prefix}_{point_query_prefix}_3d.txt"
KDTREE_INSERT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/insert/{data_file_prefix}_{insert_prefix}_3d.txt"
KDTREE_INSERT_POINT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree/insert_point/{data_file_prefix}_{insert_point_prefix}_3d.txt"


KDTREE_GREEDY_DATA = "benchmark/libspatialindex/kdtree_greedy_data"
KDTREE_GREEDY_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/build/{data_file_prefix}_{range_query_prefix}.txt"
KDTREE_GREEDY_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/range/{data_file_prefix}_{range_query_prefix}.txt"
KDTREE_GREEDY_JOIN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/join/{data_file_prefix}_{range_query_prefix}_{join_query_prefix}.txt"
KDTREE_GREEDY_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}.txt"
KDTREE_GREEDY_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}.txt"
KDTREE_GREEDY_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}.txt"
KDTREE_GREEDY_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}.txt"

KDTREE_GREEDY_DATA_3D = "benchmark/libspatialindex/kdtree_greedy_data_3d"
KDTREE_GREEDY_BUILD_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/build/{data_file_prefix}_{range_query_prefix}_3d.txt"
KDTREE_GREEDY_RANGE_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/range/{data_file_prefix}_{range_query_prefix}_3d.txt"
KDTREE_GREEDY_JOIN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/join/{data_file_prefix}_{range_query_prefix}_{join_query_prefix}_3d.txt"
KDTREE_GREEDY_KNN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}_3d.txt"
KDTREE_GREEDY_POINT_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}_3d.txt"
KDTREE_GREEDY_INSERT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}_3d.txt"
KDTREE_GREEDY_INSERT_POINT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/kdtree_greedy/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}_3d.txt"


QDTREE_DATA = "benchmark/libspatialindex/qdtree_data"
QDTREE_MODEL_PATH = "benchmark/model"
QDTREE_BUILD_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/build/{data_file_prefix}_{range_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.txt"
QDTREE_RANGE_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/range/{data_file_prefix}_{range_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.txt"
QDTREE_JOIN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/join/{data_file_prefix}_{range_query_prefix}_{join_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.txt"
QDTREE_KNN_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.txt"
QDTREE_POINT_QUERY_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.txt"
QDTREE_INSERT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.txt"
QDTREE_INSERT_POINT_OUTPUT_PATH = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.txt"
QDTREE_MODEL_NAME = "benchmark/model/qdtree.pth"
QDTREE_MODEL_NAME_DEFAULT = "benchmark/model/qdtree_{data_file_prefix}_{range_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}.pth"

QDTREE_DATA_3D = "benchmark/libspatialindex/qdtree_data_3d"
QDTREE_MODEL_PATH_3D = "benchmark/model"
QDTREE_BUILD_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/build/{data_file_prefix}_{range_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}_3d.txt"
QDTREE_RANGE_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/range/{data_file_prefix}_{range_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}_3d.txt"
QDTREE_JOIN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/join/{data_file_prefix}_{range_query_prefix}_{join_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}_3d.txt"
QDTREE_KNN_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/knn/{data_file_prefix}_{range_query_prefix}_{knn_query_prefix}_k_{k}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}_3d.txt"
QDTREE_POINT_QUERY_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/point/{data_file_prefix}_{range_query_prefix}_{point_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}_3d.txt"
QDTREE_INSERT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/insert/{data_file_prefix}_{range_query_prefix}_{insert_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}_3d.txt"
QDTREE_INSERT_POINT_OUTPUT_PATH_3D = "result/libspatialindex/" + DISK_TYPE + "/" + str(BLOCK_SIZE_SUFFIX) + "K" + "/qdtree/insert_point/{data_file_prefix}_{range_query_prefix}_{insert_point_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}_3d.txt"
# QDTREE_MODEL_NAME_3D = "benchmark/model/qdtree.pth"
QDTREE_MODEL_NAME_DEFAULT_3D = "benchmark/model/qdtree_{data_file_prefix}_{range_query_prefix}_episode_{episode}_sampling_ratio_{sampling_ratio}_action_space_{action_sampling_size}_3d.pth"


RANGE_QUERY_FILENAME_DEFAULT = "range_1000_2_uniform_1_0.001x0.001.csv"
RANGE_QUERY_FILENAME_TEMPLATE = "{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{range_str}.csv"
JOIN_QUERY_FILENAME_TEMPLATE = "{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{range_str}.csv"
KNN_QUERY_FILENAME_TEMPLATE = "{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}.csv"
POINT_QUERY_FILENAME_TEMPLATE = "{query_type}_{n_queries}_{data}_{dimensions}_{distribution}_{skewness}.csv"
INSERT_FILENAME_TEMPLATE = "{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}.csv"
INSERT_POINT_FILENAME_TEMPLATE = "{query_type}_{n_queries}_{data}_{dimensions}_{distribution}_{skewness}_{frequency}.csv"

REAL_RANGE_QUERY_FILENAME_DEFAULT = "{data}_range_1000_2_uniform_1_0.001x0.001.csv"
REAL_RANGE_QUERY_FILENAME_TEMPLATE = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{range_str}.csv"
REAL_JOIN_QUERY_FILENAME_TEMPLATE = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{range_str}.csv"
REAL_KNN_QUERY_FILENAME_TEMPLATE = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}.csv"
REAL_POINT_QUERY_FILENAME_TEMPLATE = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}.csv"
REAL_INSERT_FILENAME_TEMPLATE = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}.csv"
REAL_INSERT_POINT_FILENAME_TEMPLATE = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{frequency}.csv"

RANGE_QUERY_FILENAME_DEFAULT_3D = "range_1000_2_uniform_1_0.001x0.001x0.001_3d.csv"
RANGE_QUERY_FILENAME_TEMPLATE_3D = "{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{range_str}_3d.csv"
JOIN_QUERY_FILENAME_TEMPLATE_3D = "{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{range_str}_3d.csv"
KNN_QUERY_FILENAME_TEMPLATE_3D = "{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_3d.csv"
POINT_QUERY_FILENAME_TEMPLATE_3D = "{query_type}_{n_queries}_{data}_{dimensions}_{distribution}_{skewness}_3d.csv"
INSERT_FILENAME_TEMPLATE_3D = "{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_3d.csv"
INSERT_POINT_FILENAME_TEMPLATE_3D = "{query_type}_{n_queries}_{data}_{dimensions}_{distribution}_{skewness}_{frequency}_3d.csv"

REAL_RANGE_QUERY_FILENAME_DEFAULT_3D = "{data}_range_1000_2_uniform_1_0.001x0.001x0.001_3d.csv"
REAL_RANGE_QUERY_FILENAME_TEMPLATE_3D = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{range_str}_3d.csv"
REAL_JOIN_QUERY_FILENAME_TEMPLATE_3D = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{range_str}_3d.csv"
REAL_KNN_QUERY_FILENAME_TEMPLATE_3D = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_3d.csv"
REAL_POINT_QUERY_FILENAME_TEMPLATE_3D = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_3d.csv"
REAL_INSERT_FILENAME_TEMPLATE_3D = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_3d.csv"
REAL_INSERT_POINT_FILENAME_TEMPLATE_3D = "{data}_{query_type}_{n_queries}_{dimensions}_{distribution}_{skewness}_{frequency}_3d.csv"






