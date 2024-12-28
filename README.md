# Benchmarking RL-enhacned Spatial Indices

## Table of Contents
- [Framework Implementations](#framework-implementations)
- [Setup](#setup)
  - [1. Libraries](#1-libraries)
  - [2. Datasets](#2-datasets)
    - [Real Datasets](#real-datasets)
    - [Synthetic Datasets](#synthetic-datasets)
  - [3. Configuration](#3-configuration)
    - [Configs](#configs)
  - [4. Prerequisites Before Running Experiments](#4-prerequisites-before-running-experiments)
- [Experiments](#experiments)
  - [Index Tuning](#index-tuning)
  - [Index Building](#index-building)
  - [Read-only Workloads](#read-only-workloads)
    - [Point Query](#point-query)
    - [Range Query](#range-query)
    - [Range Query Varying range](#range-query-varying-range)
    - [Range Query Varying Aspect Ratio](#range-query-varying-aspect-ratio)
    - [Knn Query](#knn-query)
    - [Knn Query (Varying k)](#knn-query-varying-k)
  - [Varying Cardinality](#varying-cardinality)
  - [Write-only Workload](#write-only-workload)
  - [Write-heavy Workload](#write-heavy-workload)
  - [Read-heavy Workload](#read-heavy-workload)
  - [HDD vs. SSD](#hdd-vs-ssd)
  - [Overall](#overall)
  - [Improvement](#improvement)

---

## Framework Implementations

![Framework](./figs/data_img/Framework.png)

We propose a benchmarking framework 
to ensure a consistent and comprehensive evaluation of 
RLESIs, while facilitating their training, deployment, and integration into spatial systems. This framework consists of two modules: the index training module **ITM** and the index building module **IBM**.
ITM provides a unified environment for the training of RLESIs through *trainer*, which is based on PyTorch. The trainer standardizes the training process of RLESIs and outputs the trained RL models.
IBM extends the functionality of a disk-based spatial index library *libspatialindex, enabling the integration of RLESIs into spatial systems.
A critical component of IBM is the *loader*, which uses the C++ API of PyTorch to load trained RL models produced by ITM. This seamless integration supports the construction of RLESIs while preserving compatibility with traditional disk-based indexing techniques.


In IBM, we enhance the capabilities of libspatialindex to meet the requirements of our experimental study, as the original indices in libspatialindex do not fully satisfy our needs.
For DP-based indices, R-tree and R*-tree are originally supported, we 
integrate the implementation of PLATON, and add two new functions for RLR-tree to select a subtree and split a node.
For SP-based indices, we implement Kd-tree, which also serves as the foundation for GKd-tree and Qd-tree.
GKd-tree uses a heuristic algorithm for node splitting, while Qd-tree uses model predictions.
For MP-based indices, libspatialindex supports bulk-loading by loading an ordered dataset input file.
Therefore, we enable ZR-tree, ZRR-tree, and BM-tree by providing the ordered data points.
While ZM-index is implemented from scratch by changing the storage format of non-leaf nodes, integrating index learning, and adding point and range query methods with model prediction.


## Setup

### 1. Libraries

To run the experiments, you need to have LibTorch installed. Download it from the following link:

- [LibTorch v2.4.0 (CPU version)](https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-2.4.0%2Bcpu.zip)

### 2. Datasets

The datasets and Workloads required for the experiments can be downloaded from the following Dropbox link:

- [Download Datasets and Workloads](https://drive.google.com/drive/folders/15fTAbMIuJSNF1o3t36NODuaahtt3O7IV)

(Synthetic datasets and all the queries can be generated, thus, these folders are empty.)

After downloading, follow these steps:

1. Create a `data` folder in the root directory of your project (`./`).
2. Move all downloaded files to `./data/`.


#### Real Datasets

- ![Real data](./figs/data_img/real_dataset_10000_density.png)

- ![Real data point distribution](./figs/data_img/real_dataset_10000_hist_point.png)
- ![Real data range distribution](./figs/data_img/real_dataset_10000_hist_range.png)

#### Synthetic Datasets

- ![Synthetic data](./figs/data_img/synthetic_dataset_10000_density.png)

- ![Synthetic data point distribution](./figs/data_img/synthetic_dataset_10000_hist_point.png)
- ![Synthetic data range distribution](./figs/data_img/synthetic_dataset_10000_hist_range.png)

### 3. Configuration
#### Configs

Ensure that the experiment configurations are correctly set up by checking the `\exp_config` folder. Adjust the configurations as necessary for your experiments. For example:

```json
{
  "experiments": [
    {
      "available": true,
      "data": {
        "size": 100000000,
        "dimensions": 2,
        "distribution": "us",
        "skewness": 1,
        "bounds": [
          [0, 1],
          [0, 1]
        ]
      },
      "workloads": [
        "point_query_only.json", 
        "range_query_only.json", 
        "knn_query_only.json"
       ],
      "baseline": [
        {
          "name": "rankspace",
          "available": false,
          "config": {
            "fill_factor": 1.0,
            "page_size": 100,
            "bit_num": 32
          }
        },
        {
          "name": "kdgreedy",
          "available": true,
          "config": {
            "page_size": 100
          }
        }
      ]
    }
  ]
}
```
**Explanation**:

- **experiments**: An array containing experiment configurations.
  - **available**: A boolean indicating whether the experiment is available to run.
  - **data**: Describes the dataset used in the experiment.
    - **size**: The number of data points in the dataset.
    - **dimensions**: The number of dimensions (features) in the dataset.
    - **distribution**: The distribution type of the dataset (e.g., "us" for U.S. region-based distribution).
    - **skewness**: The skewness level of the data distribution, with `1` indicating a specific skewness degree.
    - **bounds**: The range of values for each dimension in the dataset, given as an array of min-max pairs.
  - **workloads**: A list of workload files specifying the types of queries to be executed (e.g., point, range, k-NN queries).
  - **baseline**: An array of baseline methods used for comparison in the experiment.
    - **name**: The name of the baseline method.
    - **available**: A boolean indicating whether the baseline method is available for the experiment.
    - **config**: Configuration parameters specific to the baseline method.
      - **fill_factor**: (For rankspace) The fill factor of the index structure.
      - **page_size**: The size of each page (node) in the index.
      - **bit_num**: (For rankspace) The number of bits used in the rank space method.


### 4. Prerequisites Before Running Experiments

1. **Configure .env**
  ```bash
    HDD_PATH="xxx"
    SSD_PATH="xxx"
    TORCH_LIB_PATH=xxx/libtorch/lib
  ```

2. **Install Extended Libspatialindex**:
   - Follow the instructions in the INSTALL.md in **libspatialindex** to install the extended version of `libspatialindex`.

3. **Verify Installation**:
   - Run `check_env.sh` to verify that `libspatialindex` is correctly installed.

4. **Configure Experiments**:
   <!-- - In `run_exp_from_config.py`, set `RUN_EXAMPLE=True` if you want to run the example configurations. -->
   - To run experiments:
     - Use `point_range_knn_queries` for all query-only workloads.
     - Use `write_only, read_heavy_only, write_heavy_only` for insertion-related workloads.

   - Uncomment the code in `run_all.sh` to run. For example:

    ```bash
    ####################### Traditional Start ######################################
    python run_exp_from_config.py exp_config/point_range_knn_queries/config_traditional.json
    python run_exp_from_config.py exp_config/point_range_knn_queries/config_traditional_vary_range.json

    python run_exp_from_config.py exp_config/write_only/config_traditional.json
    python run_exp_from_config.py exp_config/write_heavy_only/config_traditional.json
    python run_exp_from_config.py exp_config/read_heavy_only/config_traditional.json
    ####################### Traditional End ######################################
    ```

5. **Run Experiments**:

To run all the experiments, simply execute the following command in your terminal:

```bash
bash run_all.sh
```

6. **Plot Figures**:
  
  Use notebooks under `./notebook`


## Experiments

### Index Tuning

We use range query latency to choose the optimal configuration. 

![Index Tuning Time](./figs/exp_sigmod/all_query_time_build_time.png)

We use range query I/O to choose the optimal configuration. To ensure simplicity and consistency in the paper's implementation and analysis, we rely on latency as the primary criterion for choosing the optimal configuration.


![Index Tuning I/O](./figs/exp_sigmod/all_query_time_build_time_IO.png)

### Index building

The first two figures below are consistent with the figures presented in the paper.

![Index build time](./figs/exp_sigmod/build.png)
![Index size](./figs/exp_sigmod/index_size.png)

 This one reports the number of nodes in each index strucutre, where ZM-index has the least. This is becasue we set a relatively large leaf node capacity to be consistent with the feature of ZM-index.

![Node number](./figs/exp_sigmod/node_number.png)


### Read-only workloads

#### Point query

The figures below are consistent with those presented in the paper, except that Point I/O is not included.

![Point query time](./figs/exp_sigmod/point_query.png)
![Point I/O](./figs/exp_sigmod/point_IO.png)
![Point query P99](./figs/exp_sigmod/point_query_P99.png)
![Point query P1-P99](./figs/exp_sigmod/point_query_percentiles.png)


#### Range query

These four figures below are consistent with the figures presented in the paper.

![Range query time](./figs/exp_sigmod/range_query_time.png)
![Range query I/O](./figs/exp_sigmod/range_query_IO.png)
![Range query P99](./figs/exp_sigmod/range_query_P99.png)
![Range query P1-P99](./figs/exp_sigmod/range_query_percentiles.png)

#### Range query (varying range)

The figures below are consistent with those presented in the paper, except that the I/O results shown here are not included in the paper.

![Range query time varying range](./figs/exp_sigmod/range_query_time_varying_range.png)

![Range query time varying range I/O](./figs/exp_sigmod/range_query_IO_varying_range.png)


#### Range query (varying aspect ratio)

The figures below are consistent with those presented in the paper, except that the I/O results shown here are not included in the paper.

![Range query time varying range](./figs/exp_sigmod/range_query_time_varying_aspect_ratio.png)

![Range query time varying range I/O](./figs/exp_sigmod/range_query_IO_varying_aspect_ratio.png)


#### Knn query
The figures below are consistent with those presented in the paper, except that the I/O results shown here are not included in the paper.

![Knn query time](./figs/exp_sigmod/knn_query_time.png)
![Knn query I/O](./figs/exp_sigmod/knn_query_IO.png)
![Knn query P99](./figs/exp_sigmod/knn_query_P99.png)
![Knn query P1-P99](./figs/exp_sigmod/knn_query_percentiles.png)

#### Knn query (varying k)

The figures below are consistent with those presented in the paper, except that the I/O results shown here are not included in the paper.

![Knn query time varying k](./figs/exp_sigmod/knn_query_time_varying_k.png)
![Knn query I/O varying k](./figs/exp_sigmod/knn_query_IO_varying_k.png)
![Knn query P99 varying k](./figs/exp_sigmod/knn_query_P99_varying_k.png)

#### Varying Cardinality

Point query
![Point query](./figs/exp_sigmod/range_query_time_varying_cardinality.png)

Range query
![Range query](./figs/exp_sigmod/point_query_time_varying_cardinality.png)

KNN query
![KNN query](./figs/exp_sigmod/knn_query_time_varying_cardinality.png)


### Write-only workload

The figures below are consistent with those presented in the paper, except that the number of node reads and writes are not included.

![Write only](./figs/exp_sigmod/write_only.png)
![Write only P99](./figs/exp_sigmod/write_only_P99.png)
![Write only reads](./figs/exp_sigmod/write_only_reads.png)
![Write only writes](./figs/exp_sigmod/write_only_writes.png)
![Write only splits](./figs/exp_sigmod/write_only_splits.png)

### Write-heavy workload

The figures below are consistent with those presented in the paper, except that the P99 of query and insertion latency are not included.

![Write heavy query time](./figs/exp_sigmod/write_heavy_query_time.png)
![Write heavy insert time](./figs/exp_sigmod/write_heavy_insert_time.png)
![Write heavy query P99](./figs/exp_sigmod/write_heavy_query_time_P99.png)
![Write heavy insert P99](./figs/exp_sigmod/write_heavy_insert_time_P99.png)
![Write heavy splits](./figs/exp_sigmod/write_heavy_splits.png)


### Read-heavy workload

The figures below are consistent with those presented in the paper, except that the P99 of query and insertion latency are not included.

![Read heavy query time](./figs/exp_sigmod/read_heavy_query_time.png)
![Read heavy insert time](./figs/exp_sigmod/read_heavy_insert_time.png)
![Read heavy query P99](./figs/exp_sigmod/read_heavy_query_time_P99.png)
![Read heavy insert P99](./figs/exp_sigmod/read_heavy_insert_time_P99.png)



### HDD vs. SSD

![Point query](./figs/exp_sigmod/hdd_vs_ssd.png)


### Overall

![Overall](./figs/exp_sigmod/spider.png)

This figure below represents an alternative form of the radar figure, using stacked bars to illustrate the scores of each index across all metrics. The length of each stacked bar indicates the cumulative score, with longer bars representing higher overall performance. The index with the tallest bar achieves the highest total score, indicating the best overall performance among the indices.

![Overall Score](./figs/exp_sigmod/overall_spider.png)


### Improvement

The figures below are consistent with those presented in the paper, except that the improvement of I/O is not included.
![Improvement](./figs/exp_sigmod/bmtree_improved_time.png)

![Improvement](./figs/exp_sigmod/bmtree_improved.png)
