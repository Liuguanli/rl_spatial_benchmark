# Benchmarking RL-enhacned Spatial Indices

## Setup


### 1. Libraries

To run the experiments, you need to have LibTorch installed. Download it from the following link:

- [LibTorch v2.4.0 (CPU version)](https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-2.4.0%2Bcpu.zip)

### 2. Datasets

The datasets and workloads required for the experiments can be downloaded from the following Dropbox link:

- [Download Datasets and Workloads](https://www.dropbox.com/scl/fo/nthnm8in7pdvmfeq6o28x/AGRfXnULbIK1xwMwjuwsE_E?rlkey=f4wze475ygnq4z6xem6g57zos&st=gmdv0mgs&dl=0)

After downloading, follow these steps:

1. Create a `data` folder in the root directory of your project (`./`).
2. Move the `real` and `synthetic` folders from the `resources` directory to the newly created `data` folder.

### 3. Dataset Distributions

Here are some visualizations of the dataset distributions used in the experiments:

#### Real Data

- ![Real data](./figs/data_img/real_dataset_10000_density.png)

- ![Real data point distribution](./figs/data_img/real_dataset_10000_hist_point.png)
- ![Real data range distribution](./figs/data_img/real_dataset_10000_hist_range.png)

#### Synthetic Data

- ![Synthetic data](./figs/data_img/synthetic_dataset_10000_density.png)

- ![Synthetic data point distribution](./figs/data_img/synthetic_dataset_10000_hist_point.png)
- ![Synthetic data range distribution](./figs/data_img/synthetic_dataset_10000_hist_range.png)

### 4. Configuration
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


### Prerequisites Before Running Experiments

1. **Install Extended Libspatialindex**:
   - Follow the instructions in the [Installation Guide](https://github.com/AI-DB-UoM/libspatialindex/blob/master/INSTALL) to install the extended version of `libspatialindex`.

2. **Verify Installation**:
   - Run `check_env.sh` to verify that `libspatialindex` is correctly installed.

3. **Update Environment Variables**:
   - Replace the following line in your environment setup:
     ```bash
     export LD_LIBRARY_PATH=/home/liuguanli/Documents/libtorch/lib:$LD_LIBRARY_PATH
     ```
   - with the path to your own installed `libtorch` library.

4. **Configure and Run Experiments**:
   - In `run_exp_from_config.py`, set `RUN_EXAMPLE=True` if you want to run the example configurations.
   - To run experiments:
     - Use `point_range_knn_queries` for all query-only workloads.
     - Use `["write_only", "read_heavy_only", "write_heavy_only"]` for insertion-related workloads.

```python
def main():

    global logger
    configs = []
    if RUN_EXAMPLE:
        if RUN_ALL_BASELINE_EXAMPLE:
            configs = ["example_config_all_baselines.json",
                       "example_config_all_baselines_insert.json",
                       "example_config_all_baselines_read_heavy.json",
                       "example_config_all_baselines_write_heavy.json"]
            configs = ["example_config_all_baselines_point_rank_space_100m.json"]
        else: # for debug specific index
            configs = ["example_config_debug_bmtree.json"]
    else:
        directory = CONFIG_DIR
        # First run point_range_knn_queries to make sure queries are generated first for RL based.
        special_candidate = "point_range_knn_queries"
        for root, dirs, files in os.walk(directory):
            if root.split("/")[-1] == special_candidate:
                for file in files:
                    if file.endswith(".json"):
                        config_file_path = os.path.join(root, file)
                        configs.append(config_file_path)

        candidates = ["write_only", "read_heavy_only", "write_heavy_only"]
        for root, dirs, files in os.walk(directory):
            if root.split("/")[-1] not in candidates:
                continue
            for file in files:
                if file.endswith(".json"):
                    config_file_path = os.path.join(root, file)
                    configs.append(config_file_path)
```

### Run experiments

To run all the experiments, simply execute the following command in your terminal:

```bash
bash run_all.sh
```

### Index building

![Index build time](./figs/exp/build.png)
![Index size](./figs/exp/index_size.png)
![Node number](./figs/exp/node_number.png)

### Read-only workloads


#### Point query

![Point query time](./figs/exp/point_query.png)
![Point I/O](./figs/exp/point_IO.png)
![Point query P50](./figs/exp/point_query_P50.png)
![Point query P99](./figs/exp/point_query_P99.png)

#### Range query

![Range query time](./figs/exp/range_query_time.png)
![Range query I/O](./figs/exp/range_query_IO.png)
![Range query P50](./figs/exp/range_query_P50.png)
![Range query P99](./figs/exp/range_query_P99.png)

#### Knn query

![Knn query time](./figs/exp/knn_query_time.png)
![Knn query I/O](./figs/exp/knn_query_IO.png)
![Knn query P50](./figs/exp/knn_query_P50.png)
![Knn query P99](./figs/exp/knn_query_P99.png)


#### Knn query (varying k)

![Knn query time varying k](./figs/exp/knn_query_time_varying_k.png)
![Knn query I/O varying k](./figs/exp/knn_query_IO_varying_k.png)
![Knn query P50 varying k](./figs/exp/knn_query_P50_varying_k.png)
![Knn query P99 varying k](./figs/exp/knn_query_P99_varying_k.png)

### Write-only workload

![Write only](./figs/exp/write_only.png)
![Write only P50](./figs/exp/write_only_P50.png)
![Write only P99](./figs/exp/write_only_P99.png)
![Write only reads](./figs/exp/write_only_reads.png)
![Write only writes](./figs/exp/write_only_writes.png)
![Write only splits](./figs/exp/write_only_splits.png)

### Write-heavy workload

![Write heavy query time](./figs/exp/write_heavy_query_time.png)
![Write heavy insert time](./figs/exp/write_heavy_insert_time.png)
![Write heavy query P50](./figs/exp/write_heavy_query_time_P50.png)
![Write heavy query P99](./figs/exp/write_heavy_query_time_P99.png)
![Write heavy insert P50](./figs/exp/write_heavy_insert_time_P50.png)
![Write heavy insert P99](./figs/exp/write_heavy_insert_time_P99.png)
![Write heavy splits](./figs/exp/write_heavy_splits.png)

### Balanced workload

![Balcanced query time](./figs/exp/balanced_query_time.png)
![Balcancedinsert time](./figs/exp/balanced_insert_time.png)
![Balcancedquery P50](./figs/exp/balanced_query_P50.png)
![Balcanced query P99](./figs/exp/balanced_query_time_P99.png)
![Balcanced insert P50](./figs/exp/balanced_insert_time_P50.png)
![Balcanced insert P99](./figs/exp/balanced_insert_time_P99.png)
![Balcanced splits](./figs/exp/balanced_splits.png)


### Read-heavy workload
![Read heavy query time](./figs/exp/read_heavy_query_time.png)
![Read heavy insert time](./figs/exp/read_heavy_insert_time.png)
![Read heavy query P50](./figs/exp/read_heavy_query_time_P50.png)
![Read heavy query P99](./figs/exp/read_heavy_query_time_P99.png)
![Read heavy insert P50](./figs/exp/read_heavy_insert_time_P50.png)
![Read heavy insert P99](./figs/exp/read_heavy_insert_time_P99.png)
<!-- ![Balcanced splits](./figs/exp/balanced_splits.png) -->

