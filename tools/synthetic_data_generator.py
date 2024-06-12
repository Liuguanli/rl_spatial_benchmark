import numpy as np
import pandas as pd
import argparse
import os
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)
from constants import *

np.random.seed(SEED)

def generate_data(size, dimensions, distribution, range_per_dimension, skewness=None):
    if distribution == 'uniform':
        data = np.random.uniform(low=[r[0] for r in range_per_dimension], high=[r[1] for r in range_per_dimension], size=(size, dimensions))
    elif distribution == 'normal':
        data = np.zeros((size, dimensions))
        for d in range(dimensions):
            mean = (range_per_dimension[d][1] + range_per_dimension[d][0]) / 2
            std = (range_per_dimension[d][1] - range_per_dimension[d][0]) / 6  # 99.7% data within 3 std devs
            data[:, d] = np.random.normal(loc=mean, scale=std, size=size)
            # Clip data to ensure it's within the range
            data[:, d] = np.clip(data[:, d], range_per_dimension[d][0], range_per_dimension[d][1])
            
    elif distribution == 'skewed' and skewness is not None:
        # Generate skewed distribution data for each dimension
        data = np.zeros((size, dimensions))
        for d in range(dimensions):
            mean = (range_per_dimension[d][1] + range_per_dimension[d][0]) / 2
            std = (range_per_dimension[d][1] - range_per_dimension[d][0]) / 6
            data[:, d] = np.random.normal(loc=mean, scale=std, size=size)
            data[:, d] = np.clip(data[:, d], range_per_dimension[d][0], range_per_dimension[d][1])
            data[:, d] = data[:, d] ** skewness
            # Clip again after skewing
            data[:, d] = np.clip(data[:, d], range_per_dimension[d][0], range_per_dimension[d][1])
    else:
        raise ValueError("Unsupported distribution type")
    
    return data

def save_to_csv(data, file_path):
    data = np.round(data, 6)
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False, header=False)
    # print(f"Data saved to {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic data.")
    parser.add_argument("--size", type=int, default=10000, help="Number of data points to generate.", required=True)
    parser.add_argument("--dimensions", type=int, default=2, help="Number of dimensions.", required=True)
    parser.add_argument("--distribution", type=str, default="uniform", help="Type of distribution (uniform, normal, skewed).", required=True)
    parser.add_argument("--skewness", type=int, default=1, help="Skewness of skew data.", required=False)
    parser.add_argument("--range", type=float, nargs=2, action='append', help="Range for each dimension. Repeat this argument for each dimension.", required=True)
    # parser.add_argument("--output", type=str, help="Output CSV file path.", required=True)
    
    args = parser.parse_args()

    data = generate_data(size=args.size, dimensions=args.dimensions, distribution=args.distribution, range_per_dimension=args.range, skewness=args.skewness)
    file_name = SYNTHETIC_DATA_FILENAME_TEMPLATE.format(
        size=args.size,
        dimensions=args.dimensions,
        distribution=args.distribution,
        skewness=args.skewness
    )
    
    dir_path = SYNTHETIC_DATA_PATH
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    file_name = os.path.join(dir_path, file_name)
    save_to_csv(data, file_name)
    return file_name


if __name__ == "__main__":
    main()

# python tools/synthetic_data_generator.py --size 10000 --dimensions 2 --distribution uniform --skewness 1 --range 0 1 --range 0 1
# python tools/synthetic_data_generator.py --size 10000 --dimensions 2 --distribution skewed --skewness 2 --range 0 1 --range 0 1
# python tools/synthetic_data_generator.py --size 10000 --dimensions 2 --distribution normal --skewness 1 --range 0 1 --range 0 1




    
