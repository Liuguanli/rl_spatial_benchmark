
import numpy as np
import pandas as pd
import argparse
import os

def interleave_bits(values, bits_per_dimension):
    z = 0
    num_dimensions = len(values)
    for bit_pos in range(bits_per_dimension):
        for dim in range(num_dimensions):
            # Ensure the value is treated as positive
            value = values[dim] & (1 << bit_pos)
            shift_amount = bit_pos + dim
            z |= (value & (1 << bit_pos)) << shift_amount
    return z


def process_file(input_file, output_file, bits_per_dimension):
    # Load data from the input file
    df = pd.read_csv(input_file, header=None)
    df = (df * 1000000).astype(int)

    num_columns = df.shape[1]
    rank_columns = []
    for i in range(num_columns):
        # Sort the DataFrame by current dimension to future dimensions
        sorted_column_indexes = list(range(i, num_columns))
        df_sorted = df.sort_values(by=sorted_column_indexes).reset_index(drop=True)
        # Create a new column that contains the order of data points based on the current dimension sort
        order_column_name = f'dim_{i}_order'
        df_sorted[order_column_name] = df_sorted.index
        rank_columns.append(order_column_name)
        df = df_sorted

    # Extract only the rank columns for Z-order calculation
    rank_df = df[rank_columns]

    # Calculate Z-order values directly from the rank data
    def map_and_interleave(row):
        values = row.tolist()
        return interleave_bits(values, bits_per_dimension)
    
    z_order = rank_df.apply(map_and_interleave, axis=1)
    df['Z-order'] = z_order / 1000000  # Assuming you want to normalize or scale back the data

    # Sort dataframe based on Z-order and save to output file
    sorted_df = df.sort_values(by='Z-order')

    sorted_df = sorted_df.drop(columns=rank_columns)
    
    sorted_df.to_csv(output_file, index=False, header=False)

def main():
    parser = argparse.ArgumentParser(description='Sort data based on Z-order curve.')
    parser.add_argument('input_file', type=str, help='Path to the input CSV file.')
    parser.add_argument('output_file', type=str, help='Path to save the sorted CSV file.')
    parser.add_argument('bits', type=int, default=20, help='Number of bits per dimension for Z-order calculation.')
    
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"Input file {args.input_file} does not exist.")
    
    process_file(args.input_file, args.output_file, args.bits)
    # print(f"Processed {args.input_file} and saved sorted data to {args.output_file}.")

if __name__ == "__main__":
    main()
