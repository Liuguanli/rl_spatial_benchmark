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
    if distribution == 'uniform':
        centers = np.random.uniform(low=[b[0] for b in bounds], high=[b[1] for b in bounds], size=(n_queries, dimensions))
    elif distribution == 'normal':
        centers = np.zeros((n_queries, dimensions))
        for d in range(dimensions):
            mean = (bounds[d][1] + bounds[d][0]) / 2
            std = (bounds[d][1] - bounds[d][0]) / 6
            centers[:, d] = np.random.normal(loc=mean, scale=std, size=n_queries)
    elif distribution == 'skewed' and skewness is not None:
        centers = np.zeros((n_queries, dimensions))
        for d in range(dimensions):
            mean = (bounds[d][1] + bounds[d][0]) / 2
            std = (bounds[d][1] - bounds[d][0]) / 6
            skewed_data = np.random.normal(loc=mean, scale=std, size=n_queries) ** skewness
            centers[:, d] = np.clip(skewed_data, bounds[d][0], bounds[d][1])
    else:
        raise ValueError("Unsupported distribution type")

    # Generate query bounds
    for center in centers:
        min_bounds = []
        max_bounds = []
        for c, r, b in zip(center, query_range, bounds):
            min_bound = max(c - r/2, b[0])
            max_bound = min(c + r/2, b[1])
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
            queries[:, d] = np.random.normal(loc=mean, scale=std, size=n_queries)
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
    elif query_type == "knn":
        # For knn, the column names are simply the first 'dimensions' letters of 'xyz'
        column_names_base = 'xyz'
        column_names = [column_names_base[i % len(column_names_base)] + str(i // len(column_names_base) + 1) for i in range(dimensions)]
        df = pd.DataFrame(queries, columns=column_names)
    else:
        raise ValueError("Unsupported query type")

    df.to_csv(file_path, index=False, header=False)
    print(f"Queries saved to {file_path}")


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
    parser.add_argument("--query_type", type=str, choices=['range', 'knn'], required=True, help="Type of query to generate (range or knn).")
    parser.add_argument("--n_queries", type=int, required=True, help="Number of queries to generate.")
    parser.add_argument("--dimensions", type=int, required=True, help="Number of dimensions for the data points.")
    parser.add_argument("--distribution", type=str, required=True, choices=['uniform', 'normal', 'skewed'], help="Distribution of the query centers (uniform, normal, skewed).")
    parser.add_argument("--bounds", type=float, nargs=2, action='append', required=True, help="Bounds for each dimension. Use twice for two dimensions.")
    
    # Only for range queries
    parser.add_argument("--query_range", type=float, nargs='+', help="Range for each dimension in range queries. Provide one value per dimension.")
    
    # Optional for skewed distribution
    parser.add_argument("--skewness", type=int, default=1, help="Skewness factor for skewed distribution. Default is 1.0.")

    args = parser.parse_args()

    if args.query_type == 'range':
        if not args.query_range:
            parser.error("--query_range is required for range queries.")
        queries = generate_range_queries(n_queries=args.n_queries, dimensions=args.dimensions, distribution=args.distribution, query_range=args.query_range, bounds=args.bounds, skewness=args.skewness)
    elif args.query_type == 'knn':
        queries = generate_knn_queries(n_queries=args.n_queries, dimensions=args.dimensions, distribution=args.distribution, bounds=args.bounds, skewness=args.skewness)
    
    
    # if args.skewness:
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
    else:
        file_name = KNN_QUERY_FILENAME_TEMPLATE.format(
            query_type=args.query_type,
            n_queries=args.n_queries,
            dimensions=args.dimensions,
            distribution=args.distribution,
            skewness=args.skewness
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


# python your_script.py --query_type range --n_queries 100 --dimensions 2 --distribution uniform --bounds 0 100 --bounds 0 100 --query_range 10 10 --output range_queries.csv
# python your_script.py --query_type knn --n_queries 100 --dimensions 2 --distribution normal --bounds 0 100 --bounds 0 100 --k 5 --output knn_queries.csv
