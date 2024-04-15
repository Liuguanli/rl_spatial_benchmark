import numpy as np
import pandas as pd
import argparse
import os
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)
from constants import *

np.random.seed(SEED)

def generate_range_queries_from_df(df, n_queries, dimensions, query_range, distribution='uniform', skewness=None):
    # Initialize an empty list to store the generated queries.
    queries = []
    bounds = [(df[col].min(), df[col].max()) for col in df.columns]
    
    # Generate query centers based on the specified distribution.
    if distribution == 'uniform':
        # Randomly sample n_queries points from the dataframe to serve as query centers.
        sample_indices = np.random.choice(df.index, size=n_queries, replace=False)
        centers = df.iloc[sample_indices].values
    elif distribution == 'normal':
        # Calculate the mean and standard deviation for each dimension in the dataframe.
        mean = df.mean().values
        std = df.std().values
        # Generate query centers with a normal distribution based on the calculated mean and std.
        centers = np.random.normal(loc=mean, scale=std, size=(n_queries, dimensions))
    elif distribution == 'skewed' and skewness is not None:
        # Apply skewness transformation to the dataframe.
        skewed_data = df ** skewness
        # Randomly sample n_queries points from the skewed dataframe to serve as query centers.
        sample_indices = np.random.choice(skewed_data.index, size=n_queries, replace=False)
        centers = skewed_data.iloc[sample_indices].values
    else:
        # Raise an error if the distribution type is unsupported.
        raise ValueError("Unsupported distribution type")

    # Generate query bounds for each center.
    for center in centers:
        min_bounds = []
        max_bounds = []
        for c, r, b in zip(center, query_range, bounds):
            # Calculate the minimum and maximum bounds for each dimension.
            min_bound = max(c - r / 2, b[0])
            max_bound = min(c + r / 2, b[1])
            min_bounds.append(min_bound)
            max_bounds.append(max_bound)
        # Combine the minimum and maximum bounds to form the query bounds.
        query_bounds = min_bounds + max_bounds
        # Append the query bounds to the list of queries.
        queries.append(query_bounds)

    # Return the list of generated queries.
    return queries



def generate_knn_queries_from_df(df, n_queries, dimensions, distribution='uniform', skewness=None):
    """
    Generates k-NN (k-Nearest Neighbor) queries from a given DataFrame.

    Parameters:
    - df: DataFrame containing the dataset.
    - n_queries: The number of queries to generate.
    - query_range: The range of the queries.
    - bounds: The bounds of the dataset for each dimension.
    - distribution: The distribution type of the queries ('uniform', 'normal', or 'skewed').
    - skewness: The skewness parameter for the 'skewed' distribution.

    Returns:
    - A numpy array containing the generated k-NN queries.
    """

    bounds = [(df[col].min(), df[col].max()) for col in df.columns]

    # Generate query centers based on the specified distribution.
    if distribution == 'uniform':
        # Randomly sample n_queries points from the dataframe to serve as query centers.
        sample_indices = np.random.choice(df.index, size=n_queries, replace=False)
        queries = df.iloc[sample_indices].values
    elif distribution == 'normal':
        # Use mean and standard deviation of the dataframe to generate normal distributed queries.
        mean = df.mean().values
        std = df.std().values
        queries = np.random.normal(loc=mean, scale=std, size=(n_queries, dimensions))
    elif distribution == 'skewed' and skewness is not None:
        # Apply skewness transformation and sample n_queries points for skewed distribution.
        skewed_data = df ** skewness
        sample_indices = np.random.choice(skewed_data.index, size=n_queries, replace=False)
        queries = skewed_data.iloc[sample_indices].values
    else:
        # Raise an error if the distribution type is unsupported.
        raise ValueError("Unsupported distribution type")

    # Ensure queries are within bounds.
    for dim in range(dimensions):
        queries[:, dim] = np.clip(queries[:, dim], bounds[dim][0], bounds[dim][1])

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


def main():
    parser = argparse.ArgumentParser(description="Generate queries for synthetic data.")
    parser.add_argument("--data", type=str, required=True, help="The real dataset.")
    parser.add_argument("--query_type", type=str, choices=['range', 'knn'], required=True, help="Type of query to generate (range or knn).")
    parser.add_argument("--n_queries", type=int, required=True, help="Number of queries to generate.")
    parser.add_argument("--dimensions", type=int, required=True, help="Number of dimensions for the data points.")
    parser.add_argument("--distribution", type=str, required=True, choices=['uniform', 'normal', 'skewed'], help="Distribution of the query centers (uniform, normal, skewed).")
    # parser.add_argument("--bounds", type=float, nargs=2, action='append', required=True, help="Bounds for each dimension. Use twice for two dimensions.")
    
    # Only for range queries
    parser.add_argument("--query_range", type=float, nargs='+', help="Range for each dimension in range queries. Provide one value per dimension.")
    
    # Optional for skewed distribution
    parser.add_argument("--skewness", type=int, default=1, help="Skewness factor for skewed distribution. Default is 1.0.")

    args = parser.parse_args()

    df = pd.read_csv(args.data, header=None)

    if args.query_type == 'range':
        if not args.query_range:
            parser.error("--query_range is required for range queries.")
        queries = generate_range_queries_from_df(df, n_queries=args.n_queries, dimensions=args.dimensions, distribution=args.distribution, query_range=args.query_range, skewness=args.skewness)
    elif args.query_type == 'knn':
        queries = generate_knn_queries_from_df(df, n_queries=args.n_queries, dimensions=args.dimensions, distribution=args.distribution, skewness=args.skewness)
    
    base_name, extension = os.path.splitext(os.path.basename(args.data))

    # if args.skewness:
    if args.query_type == 'range':
        range_str = "x".join([str(_) for _ in args.query_range])
        file_name = REAL_RANGE_QUERY_FILENAME_TEMPLATE.format(
            data=base_name,
            query_type=args.query_type,
            n_queries=args.n_queries,
            dimensions=args.dimensions,
            distribution=args.distribution,
            skewness=args.skewness,
            range_str=range_str
        )
    else:
        file_name = REAL_KNN_QUERY_FILENAME_TEMPLATE.format(
            data=base_name,
            query_type=args.query_type,
            n_queries=args.n_queries,
            dimensions=args.dimensions,
            distribution=args.distribution,
            skewness=args.skewness
        )

    dir_path = REAL_QUERY_PATH
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    save_queries_to_csv(queries, os.path.join(dir_path, file_name), args.query_type)

if __name__ == "__main__":
    main()