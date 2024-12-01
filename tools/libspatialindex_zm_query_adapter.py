import pandas as pd
import argparse
import os
import numpy as np
from rank_space_z import interleave_bits

def calculate_rank(input_file):
    """
    Read the data and independently sort each column, then assign sorted values to the original DataFrame.
    """
    df = pd.read_csv(input_file, header=None)

    # Sort each column independently
    sorted_col0 = df[0].sort_values(ascending=True).reset_index(drop=True)
    sorted_col1 = df[1].sort_values(ascending=True).reset_index(drop=True)

    # Assign sorted values back to the original DataFrame
    df[0] = sorted_col0
    df[1] = sorted_col1

    return df


def get_rank(df, column, value, method='min'):
    """
    Get the integer rank of a given value in a sorted column using binary search.
    
    Args:
        df (pd.DataFrame): The input dataframe (sorted by column).
        column (int): The column index to rank (must be sorted).
        value: The value to rank in the column.
        method (str): The ranking method ('min' or 'max').
                      'min': Assign the smallest rank to ties.
                      'max': Assign the largest rank to ties.
    
    Returns:
        int: The integer rank of the value.
    """
    # Ensure the column is sorted
    sorted_values = df[column].values
    
    if method == 'min':
        rank = np.searchsorted(sorted_values, value, side='left') + 1
    elif method == 'max':
        rank = np.searchsorted(sorted_values, value, side='right')
    else:
        raise ValueError("Invalid method. Choose 'min' or 'max'.")
    
    return rank


def transform_json_to_csv(data, output_filename):

    # Transform JSON to DataFrame

    df = pd.DataFrame(data)
    transformed_df = pd.DataFrame({
        'Col1': 2,
        'Col2': 9999999,
        'Col3': df['x1'],
        'Col4': df['y1'],
        'Col5': df['x2'],
        'Col6': df['y2'],
        'Col7': df['key_min'],
        'Col8': df['key_max']
    })

    transformed_df.to_csv(os.path.join("./benchmark/libspatialindex", output_filename), sep=' ', index=False, header=False)


def process_all_queries(input, query_list, bits):
    df = calculate_rank(input)
    print(df)
    if query_list:
        # all_queries = {}
        for query_file in query_list:
            print(f"Processing query file: {query_file}")
            is_real = os.path.exists(os.path.join("./data/synthetic/query", query_file))
            if is_real:
                query_ = pd.read_csv(os.path.join("./data/synthetic/query", query_file), header=None)
            else:
                query_ = pd.read_csv(os.path.join("./data/real/query", query_file), header=None)

            results = []

            for index, row in query_.iterrows():
                if "point" in query_file or "knn" in query_file:
                    x1, y1 = row[0], row[1]
                    x2, y2 = row[0], row[1]
                    x_min_rank = get_rank(df, 0, x1, 'min')
                    x_max_rank = get_rank(df, 0, x2, 'max')
                    y_min_rank = get_rank(df, 1, y1, 'min')
                    y_max_rank = get_rank(df, 1, y2, 'max')
                else:
                    x1, y1, x2, y2 = row[0], row[1], row[2], row[3]
                    x_min_rank = get_rank(df, 0, x1, 'min')
                    x_max_rank = get_rank(df, 0, x2, 'max')
                    y_min_rank = get_rank(df, 1, y1, 'min')
                    y_max_rank = get_rank(df, 1, y2, 'max')

                key_min = interleave_bits([x_min_rank, y_min_rank], bits)
                key_max = interleave_bits([x_max_rank, y_max_rank], bits)


                results.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'key_min': key_min, 'key_max': key_max})

            query_file_name = os.path.splitext(query_file)[0] + "_zm"
            print(f"Processing query file (without extension): {query_file_name}")
            transform_json_to_csv(results, query_file_name)
    else:
        print("No query files provided.")



def main():
    parser = argparse.ArgumentParser(description='Transform CSV files based on type.')
    parser.add_argument('--bits', type=int, default=20, help='Number of bits per dimension for Z-order calculation.')
    parser.add_argument('--data', type=str, required=True, help='Path to the input CSV file.')
    parser.add_argument("--query_list", type=str, nargs='+', help="A list of queries.")

    args = parser.parse_args()

    process_all_queries(args.data, args.query_list, args.bits)

    # calculate_rank(args.data)

if __name__ == '__main__':
    main()

# python tools/libspatialindex_zm_query_adapter.py --bits 32 --data ./data/real/dataset/us_10000.csv --query_list ./data/real/query/us_10000_point_2000_2_uniform_1.csv ./data/real/query/us_10000_range_20_2_uniform_1_0.1x0.1.csv ./data/real/query/us_10000_knn_1000_2_uniform_1.csv