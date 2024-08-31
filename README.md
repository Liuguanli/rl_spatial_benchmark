## Benchmarking RL-enhacned Spatial Indices


#### Datasets


Download datasets and workloads from [Dropbox Link](https://www.dropbox.com/scl/fo/nthnm8in7pdvmfeq6o28x/AGRfXnULbIK1xwMwjuwsE_E?rlkey=f4wze475ygnq4z6xem6g57zos&st=gmdv0mgs&dl=0)

Add a **data** folder under **./**.

Move **real** and **synthetic** folders from **resources** to **data**.

#### Dataset distributions

![Real data](./figs/data_img/real_dataset_10000_density.png)

![Synthetic data](./figs/data_img/synthetic_dataset_10000_density.png)


![Real data point](./figs/data_img/real_dataset_10000_hist_point.png)

![Real data range](./figs/data_img/real_dataset_10000_hist_range.png)


![Synthetic data point](./figs/data_img/synthetic_dataset_10000_hist_point.png)

![Synthetic data range](./figs/data_img/synthetic_dataset_10000_hist_range.png)


#### Configs

check folder: **\exp_config**

### Run experiments

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

