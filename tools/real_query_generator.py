import numpy as np
import pandas as pd
import argparse
import os
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)
from constants import *

np.random.seed(SEED)

def generate_range_queries(data_file, n_queries, dimensions, query_range, distribution='uniform', skewness=None):

    df = pd.read_csv(data_file, header=None)
    # Initialize an empty list to store the generated queries.
    queries = []
    bounds = [(df[col].min(), df[col].max()) for col in df.columns]
    # mean = df.mean().values
    # std = df.std().values
    
    # Generate query centers based on the specified distribution.
    if distribution == 'uniform':
        # Randomly sample n_queries points from the dataframe to serve as query centers.
        sample_indices = np.random.choice(df.index, size=n_queries, replace=False)
        centers = df.iloc[sample_indices].values
    elif distribution == 'normal':
        # Calculate the mean and standard deviation for each dimension in the dataframe.
        centers = np.zeros((n_queries, dimensions))
        for d in range(dimensions):
            mean = (bounds[d][1] + bounds[d][0]) / 2
            std = (bounds[d][1] - bounds[d][0]) / 6
            lower_bound = np.full((n_queries,), bounds[d][0] + query_range[d]/2)
            upper_bound = np.full((n_queries,), bounds[d][1] - query_range[d]/2)
            centers[:, d] = np.clip(np.random.normal(loc=mean, scale=std, size=n_queries), lower_bound, upper_bound)
    elif distribution == 'skewed' and skewness is not None:
        # Apply skewness transformation to the dataframe.
        # skewed_data = df ** skewness
        centers = np.zeros((n_queries, dimensions))
        for d in range(dimensions):
            mean = (bounds[d][1] + bounds[d][0]) / 2
            std = (bounds[d][1] - bounds[d][0]) / 6
            skewed_data = np.random.normal(loc=mean, scale=std, size=n_queries) ** skewness
            lower_bound = np.full((n_queries,), bounds[d][0] + query_range[d]/2)
            upper_bound = np.full((n_queries,), bounds[d][1] - query_range[d]/2)
            centers[:, d] = np.clip(skewed_data, lower_bound, upper_bound)
        # # Randomly sample n_queries points from the skewed dataframe to serve as query centers.
        # sample_indices = np.random.choice(skewed_data.index, size=n_queries, replace=False)
        # centers = skewed_data.iloc[sample_indices].values
    else:
        # Raise an error if the distribution type is unsupported.
        raise ValueError("Unsupported distribution type")

    # Generate query bounds for each center.
    for center in centers:
        min_bounds = []
        max_bounds = []
        for c, r, b in zip(center, query_range, bounds):
            # Calculate the minimum and maximum bounds for each dimension.
            min_bound = max(c - r/2, b[0])
            min_bound = min(min_bound, b[1] - r)
            max_bound = min(c + r/2, b[1])
            max_bound = max(max_bound, min_bound + r)
            min_bounds.append(min_bound)
            max_bounds.append(max_bound)
        # Combine the minimum and maximum bounds to form the query bounds.
        query_bounds = min_bounds + max_bounds
        # Append the query bounds to the list of queries.
        queries.append(query_bounds)

    queries = np.array(queries, dtype=np.float64)
    return queries


def generate_knn_queries(data_file, n_queries, dimensions, distribution='uniform', skewness=None):
    df = pd.read_csv(data_file, header=None)
    mean = df.mean().values
    std = df.std().values

    bounds = [(df[col].min(), df[col].max()) for col in df.columns]

    # Generate query centers based on the specified distribution.
    queries = np.zeros((n_queries, dimensions))
    if distribution == 'uniform':
        # Randomly sample n_queries points from the dataframe to serve as query centers.
        sample_indices = np.random.choice(df.index, size=n_queries, replace=False)
        queries = df.iloc[sample_indices].values
    elif distribution == 'normal':
        # Use mean and standard deviation of each dimension to generate normally distributed queries.
        for d in range(dimensions):
            queries[:, d] = np.clip(np.random.normal(loc=mean[d], scale=std[d], size=n_queries), bounds[d][0], bounds[d][1])
    elif distribution == 'skewed' and skewness is not None:
        for d in range(dimensions):
            skewed_data = np.random.normal(loc=mean[d], scale=std[d], size=n_queries) ** skewness
            queries[:, d] = np.clip(skewed_data, bounds[d][0], bounds[d][1])
    else:
        # Raise an error if the distribution type is unsupported.
        raise ValueError("Unsupported distribution type")

    # Ensure queries are within bounds.
    for dim in range(dimensions):
        queries[:, dim] = np.clip(queries[:, dim], bounds[dim][0], bounds[dim][1])

    return queries


def generate_point_queries(data_file, n_queries, dimensions, distribution='uniform', skewness=None):
    df = pd.read_csv(data_file, header=None)    
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


def generate_insertions(data_file, n_queries, dimensions, distribution='uniform', skewness=None):
    """
    Generates unique insertion points that do not overlap with existing data points in the DataFrame.

    Parameters:
    - data_file: Path to the CSV file containing the dataset.
    - n_points: The number of unique insertion points to generate.
    - dimensions: The number of dimensions in the dataset.
    - bounds: A list of tuples specifying the min and max for each dimension.

    Returns:
    - A numpy array containing the generated unique insertion points.
    """
    df = pd.read_csv(data_file, header=None)
    mean = df.mean().values
    std = df.std().values
    bounds = [(df[col].min(), df[col].max()) for col in df.columns]
    existing_points = set(map(tuple, df.values.tolist()))  # Convert existing points to a set of tuples for fast lookup

    # Generate unique points ensuring they do not overlap with existing data
    insertion_points = []
    if 'india' in data_file:
        df_source = pd.read_csv("data/real/dataset/india_100000000.csv", header=None)
    elif 'australia' in data_file:
        df_source = pd.read_csv("data/real/dataset/australia_100000000.csv", header=None)
    elif 'us' in data_file:
        df_source = pd.read_csv("data/real/dataset/us_100000000.csv", header=None)
    else:
        raise ValueError("Unsupported distribution type")
    while len(insertion_points) < n_queries:
        
        random_index = np.random.randint(0, len(df_source))
        # Retrieve the point at the random index
        point = df_source.iloc[random_index]

        # if distribution == 'uniform':
        #     # Randomly sample n_queries points from the dataframe to serve as query centers.
        #     point = np.random.uniform([b[0] for b in bounds], [b[1] for b in bounds])
        # elif distribution == 'normal':
        #     # Use mean and standard deviation of the dataframe to generate normal distributed queries.
        #     point = np.random.normal(mean, std)
        #     point = np.clip(point, [b[0] for b in bounds], [b[1] for b in bounds])
        # elif distribution == 'skewed' and skewness is not None:
        #     point = np.random.normal([b[0] for b in bounds], [b[1] for b in bounds]) ** skewness
        #     point = np.clip(point, [b[0] for b in bounds], [b[1] for b in bounds])
        # else:
        #     # Raise an error if the distribution type is unsupported.
        #     raise ValueError("Unsupported distribution type")
        point_tuple = tuple(point)
        
        # Check if the generated point is unique
        if point_tuple not in existing_points:
            insertion_points.append(point)
            existing_points.add(point_tuple)  # Update the set to include the new point

    return np.array(insertion_points)

def generate_insertion_points(data_file, n_queries, dimensions, frequency, distribution='uniform', skewness=None):
    
    step = n_queries // sum(frequency)
    insertion_num = step * frequency[0]
    point_num = step * frequency[1]
    assert insertion_num + point_num == n_queries

    queries = []
    insertions = generate_insertions(data_file, insertion_num, dimensions, distribution, skewness)

    df = pd.read_csv(data_file, header=None)

    for i in range(step):
        insertion_slice = insertions[i * frequency[0] : i * frequency[0] + frequency[0]].tolist() 
        df = pd.concat([df, pd.DataFrame(insertion_slice)])
        new_points = []
        if distribution == 'uniform':
            # Randomly sample n_queries points from the dataframe to serve as query centers.
            sample_indices = np.random.choice(df.index, size=frequency[1], replace=False)
            new_points = df.iloc[sample_indices].values
        elif distribution == 'normal':
            # Normalize data and sample
            normalized_df = (df - df.mean()) / df.std()
            sample_indices = np.random.choice(normalized_df.index, size=frequency[1], replace=False)
            new_points = df.iloc[sample_indices].values  # Return original data points
        elif distribution == 'skewed' and skewness is not None:
            # Skew data and sample
            skewed_df = df ** skewness
            sample_indices = np.random.choice(skewed_df.index, size=frequency[1], replace=False)
            new_points = skewed_df.iloc[sample_indices].values

        point_slice = new_points.tolist()
        for record in insertion_slice:
            record_with_id = np.insert(record, 0, 1)
            queries.append(record_with_id)
        for record in point_slice:
            record_with_id = np.insert(record, 0, 2)
            queries.append(record_with_id)

    queries = np.array(queries, dtype=np.float64)

    return queries


def save_queries_to_csv(queries, file_path, query_type="range"):
    # # 6 decimal places
    # queries = np.round(queries, 6)
    
    # Determine number of dimensions
    dimensions = queries.shape[1]
    if query_type == "range":
        # Generate column names based on dimensions
        dimensions = dimensions // 2
        column_names = [f"{dim}{i}" for i in range(1, 3) for dim in 'xyz'[:dimensions]]
        df = pd.DataFrame(queries, columns=column_names)
    else:
        # For knn, the column names are simply the first 'dimensions' letters of 'xyz'
        column_names_base = 'xyz'
        column_names = [column_names_base[i % len(column_names_base)] + str(i // len(column_names_base) + 1) for i in range(dimensions)]
        df = pd.DataFrame(queries, columns=column_names)

    df.to_csv(file_path, index=False, header=False)
    # print(f"Queries saved to {file_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate queries for synthetic data.")
    parser.add_argument("--data", type=str, required=True, help="The real dataset.")
    parser.add_argument("--query_type", type=str, choices=['range', 'knn', 'point', 'insert', 'insert_point'], required=True, help="Type of query to generate (range or knn).")
    parser.add_argument("--n_queries", type=int, required=True, help="Number of queries to generate.")
    parser.add_argument("--dimensions", type=int, required=True, help="Number of dimensions for the data points.")
    parser.add_argument("--distribution", type=str, required=True, choices=['uniform', 'normal', 'skewed'], help="Distribution of the query centers (uniform, normal, skewed).")
    parser.add_argument("--bounds", type=float, nargs=2, action='append', required=False, help="Bounds for each dimension. Use twice for two dimensions.")
    
    # Only for range queries
    parser.add_argument("--query_range", type=float, nargs='+', help="Range for each dimension in range queries. Provide one value per dimension.")
    
    # Optional for skewed distribution
    parser.add_argument("--skewness", type=int, default=1, help="Skewness factor for skewed distribution. Default is 1.0.")

    # Only for insert_point
    parser.add_argument("--frequency", type=int, nargs='+', help="Frequency of insertions and point queries.")

    args = parser.parse_args()

    if args.query_type == 'range':
        if not args.query_range:
            parser.error("--query_range is required for range queries.")
        queries = generate_range_queries(args.data, n_queries=args.n_queries, dimensions=args.dimensions, distribution=args.distribution, query_range=args.query_range, skewness=args.skewness)
    elif args.query_type == 'knn':
        queries = generate_knn_queries(args.data, n_queries=args.n_queries, dimensions=args.dimensions, distribution=args.distribution, skewness=args.skewness)
    elif args.query_type == 'point':
        queries = generate_point_queries(args.data, n_queries=args.n_queries, dimensions=args.dimensions, distribution=args.distribution, skewness=args.skewness)
    elif args.query_type == 'insert':
        queries = generate_insertions(args.data, n_queries=args.n_queries, dimensions=args.dimensions, distribution=args.distribution, skewness=args.skewness)
    elif args.query_type == 'insert_point':
        queries = generate_insertion_points(args.data, n_queries=args.n_queries, dimensions=args.dimensions, frequency=args.frequency, distribution=args.distribution, skewness=args.skewness)

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
    elif args.query_type == 'knn':
        file_name = REAL_KNN_QUERY_FILENAME_TEMPLATE.format(
            data=base_name,
            query_type=args.query_type,
            n_queries=args.n_queries,
            dimensions=args.dimensions,
            distribution=args.distribution,
            skewness=args.skewness
        )
    elif args.query_type == 'point':
        file_name = REAL_POINT_QUERY_FILENAME_TEMPLATE.format(
            data=base_name,
            query_type=args.query_type,
            n_queries=args.n_queries,
            dimensions=args.dimensions,
            distribution=args.distribution,
            skewness=args.skewness
        )
    elif args.query_type == 'insert':
        file_name = REAL_INSERT_FILENAME_TEMPLATE.format(
            data=base_name,
            query_type=args.query_type,
            n_queries=args.n_queries,
            dimensions=args.dimensions,
            distribution=args.distribution,
            skewness=args.skewness
        )
    elif args.query_type == 'insert_point':
        frequency_str = "_".join([str(_) for _ in args.frequency])
        file_name = REAL_INSERT_POINT_FILENAME_TEMPLATE.format(
            data=base_name,
            query_type=args.query_type,
            n_queries=args.n_queries,
            dimensions=args.dimensions,
            distribution=args.distribution,
            skewness=args.skewness,
            frequency=frequency_str
        )

    dir_path = REAL_QUERY_PATH
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    save_queries_to_csv(queries, os.path.join(dir_path, file_name), args.query_type)

if __name__ == "__main__":
    main()

## range
# python tools/real_query_generator.py --data data/real/dataset/india_10000.csv --query_type range --n_queries 100 --dimensions 2 --distribution uniform --skewness 1 --query_range 1.0 1.0
# python tools/real_query_generator.py --data data/real/dataset/australia_10000.csv --query_type range --n_queries 100 --dimensions 2 --distribution normal --skewness 1 --query_range 1.0 1.0
# python tools/real_query_generator.py --data data/real/dataset/us_10000.csv --query_type range --n_queries 100 --dimensions 2 --distribution skewed --skewness 2 --query_range 1.0 1.0

## knn
# python tools/real_query_generator.py --data data/real/dataset/india_10000.csv --query_type knn --n_queries 100 --dimensions 2 --distribution uniform --skewness 1
# python tools/real_query_generator.py --data data/real/dataset/australia_10000.csv --query_type knn --n_queries 100 --dimensions 2 --distribution normal --skewness 1
# python tools/real_query_generator.py --data data/real/dataset/us_10000.csv --query_type knn --n_queries 100 --dimensions 2 --distribution skewed --skewness 2


# insert
# python tools/real_query_generator.py --data data/real/dataset/india_10000.csv --query_type insert --n_queries 1000 --dimensions 2 --distribution uniform --skewness 1
# python tools/real_query_generator.py --data data/real/dataset/australia_10000.csv --query_type insert --n_queries 1000 --dimensions 2 --distribution uniform --skewness 1
# python tools/real_query_generator.py --data data/real/dataset/us_10000.csv --query_type insert --n_queries 1000 --dimensions 2 --distribution uniform --skewness 1
