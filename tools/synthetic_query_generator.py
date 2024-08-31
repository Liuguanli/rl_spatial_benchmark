import numpy as np
import pandas as pd
import argparse
import os
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)
from constants import *

np.random.seed(SEED)

from constants import KNN_QUERY_FILENAME_TEMPLATE, RANGE_QUERY_FILENAME_TEMPLATE, SYNTHETIC_QUERY_PATH

def generate_range_queries(n_queries, dimensions, distribution, query_range, bounds, skewness=None):
    queries = []
    query_range = [query_range[d] * (bounds[d][1] - bounds[d][0]) for d in range(dimensions)]

    if distribution == 'uniform':
        adjusted_bounds = [(b[0] + r/2, b[1] - r/2) for b, r in zip(bounds, query_range)]
        centers = np.random.uniform(low=[b[0] for b in adjusted_bounds], high=[b[1] for b in adjusted_bounds], size=(n_queries, dimensions))
    elif distribution == 'normal':
        centers = np.zeros((n_queries, dimensions))
        for d in range(dimensions):
            mean = (bounds[d][1] + bounds[d][0]) / 2
            std = (bounds[d][1] - bounds[d][0]) / 6
            # centers[:, d] = np.random.normal(loc=mean, scale=std, size=n_queries)
            centers[:, d] = np.clip(np.random.normal(loc=mean, scale=std, size=n_queries), bounds[d][0] + query_range[d]/2, bounds[d][1] - query_range[d]/2)
    elif distribution == 'skewed' and skewness is not None:
        centers = np.zeros((n_queries, dimensions))
        for d in range(dimensions):
            mean = (bounds[d][1] + bounds[d][0]) / 2
            std = (bounds[d][1] - bounds[d][0]) / 6
            skewed_data = np.random.normal(loc=mean, scale=std, size=n_queries) ** skewness
            centers[:, d] = np.clip(skewed_data, bounds[d][0] + query_range[d]/2, bounds[d][1] - query_range[d]/2)
    else:
        raise ValueError("Unsupported distribution type")

    # Generate query bounds
    for center in centers:
        min_bounds = []
        max_bounds = []
        for c, r, b in zip(center, query_range, bounds):
            min_bound = max(c - r/2, b[0])
            min_bound = min(min_bound, b[1] - r)
            max_bound = min(c + r/2, b[1])
            max_bound = max(max_bound, min_bound + r)
            min_bounds.append(min_bound)
            max_bounds.append(max_bound)
        query_bounds = min_bounds + max_bounds
        queries.append(query_bounds)

    return queries


def generate_knn_queries(n_queries, dimensions, distribution, bounds, skewness=None):
    if distribution == 'uniform':
        queries = np.random.uniform(low=[b[0] for b in bounds], high=[b[1] for b in bounds], size=(n_queries, dimensions))
    elif distribution == 'normal':
        queries = np.zeros((n_queries, dimensions))
        for d in range(dimensions):
            mean = (bounds[d][1] + bounds[d][0]) / 2
            std = (bounds[d][1] - bounds[d][0]) / 6
            # queries[:, d] = np.random.normal(loc=mean, scale=std, size=n_queries)
            queries[:, d] = np.clip(np.random.normal(loc=mean, scale=std, size=n_queries), bounds[d][0], bounds[d][1])
    elif distribution == 'skewed' and skewness is not None:
        queries = np.zeros((n_queries, dimensions))
        for d in range(dimensions):
            mean = (bounds[d][1] + bounds[d][0]) / 2
            std = (bounds[d][1] - bounds[d][0]) / 6
            skewed_data = np.random.normal(loc=mean, scale=std, size=n_queries) ** skewness
            queries[:, d] = np.clip(skewed_data, bounds[d][0], bounds[d][1])
    else:
        raise ValueError("Unsupported distribution type")

    return queries

def generate_point_queries(n_queries, data_file_name, dimensions, distribution, skewness=None):
    df = pd.read_csv(os.path.join(SYNTHETIC_DATA_PATH, data_file_name), header=None)
        # Generate query centers based on the specified distribution.
    if distribution == 'uniform':
        # Randomly sample n_queries points from the dataframe to serve as query centers.
        sample_indices = np.random.choice(df.index, size=n_queries, replace=False)
        points = df.iloc[sample_indices].values
    elif distribution == 'normal':
        # Normalize data and sample
        normalized_df = (df - df.mean()) / df.std()
        sample_indices = np.random.choice(normalized_df.index, size=n_queries, replace=False)
        points = df.iloc[sample_indices].values  # Return original data points
    elif distribution == 'skewed' and skewness is not None:
        # Skew data and sample
        skewed_df = df ** skewness
        sample_indices = np.random.choice(skewed_df.index, size=n_queries, replace=False)
        points = df.iloc[sample_indices].values
    else:
        # Raise an error if the distribution type is unsupported.
        raise ValueError("Unsupported distribution type")
    
    return points

def generate_insertions(n_queries, dimensions, distribution, bounds, skewness=None):
    if distribution == 'uniform':
        queries = np.random.uniform(low=[b[0] for b in bounds], high=[b[1] for b in bounds], size=(n_queries, dimensions))
    elif distribution == 'normal':
        queries = np.zeros((n_queries, dimensions))
        for d in range(dimensions):
            mean = (bounds[d][1] + bounds[d][0]) / 2
            std = (bounds[d][1] - bounds[d][0]) / 6
            # queries[:, d] = np.random.normal(loc=mean, scale=std, size=n_queries)
            queries[:, d] = np.clip(np.random.normal(loc=mean, scale=std, size=n_queries), bounds[d][0], bounds[d][1])
    elif distribution == 'skewed' and skewness is not None:
        queries = np.zeros((n_queries, dimensions))
        for d in range(dimensions):
            mean = (bounds[d][1] + bounds[d][0]) / 2
            std = (bounds[d][1] - bounds[d][0]) / 6
            skewed_data = np.random.normal(loc=mean, scale=std, size=n_queries) ** skewness
            queries[:, d] = np.clip(skewed_data, bounds[d][0], bounds[d][1])
    else:
        raise ValueError("Unsupported distribution type")

    return queries

def generate_insertion_points(n_queries, data_file_name, dimensions, distribution, bounds, frequency, skewness=None):

    step = n_queries // sum(frequency)
    insertion_num = step * frequency[0]
    point_num = step * frequency[1]
    assert insertion_num + point_num == n_queries

    insertions = generate_insertions(insertion_num, dimensions, distribution, bounds, skewness)
    insertions_df = pd.DataFrame(insertions)
    df = pd.read_csv(os.path.join(SYNTHETIC_DATA_PATH, data_file_name), header=None)

    if distribution == 'uniform':
        shuffled_df = df.sample(frac=1).reset_index(drop=True)
    elif distribution == 'normal':
        # Normalize data and sample
        normalized_df = (df - df.mean()) / df.std()
        shuffled_df = normalized_df.sample(frac=1).reset_index(drop=True)
    elif distribution == 'skewed' and skewness is not None:
        # Skew data and sample
        skewed_df = df ** skewness
        shuffled_df = skewed_df.sample(frac=1).reset_index(drop=True)

    insertions_df = insertions_df.sample(n=min(insertion_num, len(insertions_df))).reset_index(drop=True)
    query_df = shuffled_df.sample(n=min(point_num, len(shuffled_df))).reset_index(drop=True)
    insertions_list = insertions_df.values.tolist()
    query_list = query_df.values.tolist()

    combined_list = []
    for i in range(step):
        insertion_slice = insertions_list[i * frequency[0] : i * frequency[0] + frequency[0]]
        point_slice = query_list[i * frequency[1] : i * frequency[1] + frequency[1]]
        insertion_slice = [[1] + item for item in insertion_slice]
        point_slice = [[2] + item for item in point_slice]
        # df_combined = pd.concat([df_combined, insertion_slice, point_slice], ignore_index=True)
        combined_list.extend(insertion_slice)
        combined_list.extend(point_slice)

    return np.array(combined_list)


def save_queries_to_csv(queries, file_path, query_type="range"):
    # 6 decimal places
    queries = np.round(queries, 6)
    
    # Determine number of dimensions
    dimensions = queries.shape[1]
    if query_type == "range":
        # Generate column names based on dimensions
        dimensions = dimensions // 2
        column_names = [f"{dim}{i}" for i in range(1, 3) for dim in 'xyz'[:dimensions]]
        df = pd.DataFrame(queries, columns=column_names)
    else:
        # For knn, point, insertion, the column names are simply the first 'dimensions' letters of 'xyz'
        column_names_base = 'xyz'
        column_names = [column_names_base[i % len(column_names_base)] + str(i // len(column_names_base) + 1) for i in range(dimensions)]
        df = pd.DataFrame(queries, columns=column_names)
   
    df.to_csv(file_path, index=False, header=False)
    # print(f"Queries saved to {file_path}")


# def save_queries_to_csv(queries, file_path, query_type="range"):
#     # 6 decimal places
#     queries = np.round(queries, 6)
#     if query_type == "range":
#         df = pd.DataFrame(queries, columns=['x1', 'y1', 'x2', 'y2'])
#     elif query_type == "knn":
#         df = pd.DataFrame(queries, columns=['x', 'y'])
#     else:
#         raise ValueError("Unsupported query type")
    
#     df.to_csv(file_path, index=False, header=False)
#     # print(f"Queries saved to {file_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate queries for synthetic data.")
    parser.add_argument("--query_type", type=str, choices=['range', 'knn', 'point', 'insert', 'insert_point'], required=True, help="Type of query to generate (range or knn).")
    parser.add_argument("--n_queries", type=int, required=True, help="Number of queries to generate.")
    parser.add_argument("--dimensions", type=int, required=True, help="Number of dimensions for the data points.")
    parser.add_argument("--distribution", type=str, required=True, choices=['uniform', 'normal', 'skewed'], help="Distribution of the query centers (uniform, normal, skewed).")
    parser.add_argument("--bounds", type=float, nargs=2, action='append', required=False, help="Bounds for each dimension. Use twice for two dimensions.")
    
    # Only for range queries
    parser.add_argument("--query_range", type=float, nargs='+', help="Range for each dimension in range queries. Provide one value per dimension.")
    
    # Optional for skewed distribution
    parser.add_argument("--skewness", type=int, default=1, help="Skewness factor for skewed distribution. Default is 1.0.")

    # Optional for point query
    parser.add_argument("--data_file_name", type=str, help="For point query to sample data.")

    # Only for insert_point
    parser.add_argument("--frequency", type=int, nargs='+', help="Frequency of insertions and point queries.")



    args = parser.parse_args()

    if args.query_type == 'range':
        if not args.query_range:
            parser.error("--query_range is required for range queries.")
        queries = generate_range_queries(n_queries=args.n_queries, dimensions=args.dimensions, distribution=args.distribution, query_range=args.query_range, bounds=args.bounds, skewness=args.skewness)
    elif args.query_type == 'knn':
        queries = generate_knn_queries(n_queries=args.n_queries, dimensions=args.dimensions, distribution=args.distribution, bounds=args.bounds, skewness=args.skewness)
    elif args.query_type == 'point':
        queries = generate_point_queries(n_queries=args.n_queries, data_file_name=args.data_file_name, dimensions=args.dimensions, distribution=args.distribution, skewness=args.skewness)
    elif args.query_type == 'insert':
        queries = generate_insertions(n_queries=args.n_queries, dimensions=args.dimensions, distribution=args.distribution, bounds=args.bounds, skewness=args.skewness)
    elif args.query_type == 'insert_point':
        queries = generate_insertion_points(n_queries=args.n_queries, data_file_name=args.data_file_name, dimensions=args.dimensions, distribution=args.distribution, bounds=args.bounds, frequency=args.frequency, skewness=args.skewness)

    if args.query_type == 'range':
        range_str = "x".join([str(_) for _ in args.query_range])
        file_name = RANGE_QUERY_FILENAME_TEMPLATE.format(
            query_type=args.query_type,
            n_queries=args.n_queries,
            dimensions=args.dimensions,
            distribution=args.distribution,
            skewness=args.skewness,
            range_str=range_str
        )
    elif args.query_type == 'knn':
        file_name = KNN_QUERY_FILENAME_TEMPLATE.format(
            query_type=args.query_type,
            n_queries=args.n_queries,
            dimensions=args.dimensions,
            distribution=args.distribution,
            skewness=args.skewness
        )
    elif args.query_type == 'point':
        base_name, extension = os.path.splitext(os.path.basename(args.data_file_name))
        file_name = POINT_QUERY_FILENAME_TEMPLATE.format(
            query_type=args.query_type,
            n_queries=args.n_queries,
            data=base_name,
            dimensions=args.dimensions,
            distribution=args.distribution,
            skewness=args.skewness
        )
    elif args.query_type == 'insert':
        file_name = INSERT_FILENAME_TEMPLATE.format(
            query_type=args.query_type,
            n_queries=args.n_queries,
            dimensions=args.dimensions,
            distribution=args.distribution,
            skewness=args.skewness
        )
    elif args.query_type == 'insert_point':
        base_name, extension = os.path.splitext(os.path.basename(args.data_file_name))
        frequency_str = "_".join([str(_) for _ in args.frequency])
        file_name = INSERT_POINT_FILENAME_TEMPLATE.format(
            query_type=args.query_type,
            n_queries=args.n_queries,
            data=base_name,
            dimensions=args.dimensions,
            distribution=args.distribution,
            skewness=args.skewness,
            frequency=frequency_str
        )
    # else:
    #     if args.query_type == 'range':
    #         bounds_str = "x".join([str(_) for _ in args.query_range])
    #         file_name = f"{args.query_type}_{args.n_queries}_{args.dimensions}_{args.distribution}_{bounds_str}.csv"
    #     else:
    #         file_name = f"{args.query_type}_{args.n_queries}_{args.dimensions}_{args.distribution}.csv"

    dir_path = SYNTHETIC_QUERY_PATH
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    save_queries_to_csv(queries, os.path.join(dir_path, file_name), args.query_type)

if __name__ == "__main__":
    main()


## range
# python tools/synthetic_query_generator.py --query_type range --n_queries 20 --dimensions 2 --distribution normal --bounds 0 1 --bounds 0 1 --query_range 0.1 0.1
# python tools/synthetic_query_generator.py --query_type range --n_queries 20 --dimensions 2 --distribution skewed --skewness 4 --bounds 0 1 --bounds 0 1 --query_range 0.1 0.1
# python tools/synthetic_query_generator.py --query_type range --n_queries 20 --dimensions 2 --distribution uniform --bounds 0 1 --bounds 0 1 --query_range 0.1 0.1

## knn
# python tools/synthetic_query_generator.py --query_type knn --n_queries 100 --dimensions 2 --distribution normal --bounds 0 1 --bounds 0 1
# python tools/synthetic_query_generator.py --query_type knn --n_queries 100 --dimensions 2 --distribution skewed --skewness 2 --bounds 0 1 --bounds 0 1
# python tools/synthetic_query_generator.py --query_type knn --n_queries 100 --dimensions 2 --distribution uniform --bounds 0 1 --bounds 0 1


## insert_point
# python tools/synthetic_query_generator.py --query_type insert_point --n_queries 1000 --dimensions 2 --distribution normal --bounds 0 1 --bounds 0 1 --query_range 0.01 0.01 --frequency 18 2 --data_file_name data_10000_2_uniform_1.csv

## insert
# python tools/synthetic_query_generator.py --query_type insert --n_queries 1000 --dimensions 2 --distribution uniform --skewness 1 --bounds 0 1 --bounds 0 1
# python tools/synthetic_query_generator.py --query_type insert --n_queries 1000 --dimensions 2 --distribution normal --skewness 1 --bounds 0 1 --bounds 0 1
# python tools/synthetic_query_generator.py --query_type insert --n_queries 1000 --dimensions 2 --distribution normal --skewness 1 --bounds 0 1 --bounds 0 1
# python tools/synthetic_query_generator.py --query_type insert --n_queries 1000 --dimensions 2 --distribution skewed --skewness 4 --bounds 0 1 --bounds 0 1