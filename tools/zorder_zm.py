import numpy as np
import pandas as pd
import argparse
import os
import struct

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

def float_to_int_bits(value, shift_length, offset=0):
    adjusted_value = value + offset
    binary_value = struct.pack('>f', adjusted_value)
    int_value = int.from_bytes(binary_value, 'big')
    int_bits = int_value >> (32 - shift_length)
    return int(int_bits)

def convert_data_to_int_bits(data_frame, bit_length, offset=0):
    for col in data_frame.columns:
        data_frame[col] = data_frame[col].apply(float_to_int_bits, args=(bit_length, offset))
    return data_frame


def process_file(input_file, output_file, bits_per_dimension, offset=0):
    # Load data from the input file
    df = pd.read_csv(input_file, header=None)
    df_copy = df.copy()
    adjusted_df = convert_data_to_int_bits(df_copy, bits_per_dimension, offset)

    # Calculate Z-order values directly from the data
    def map_and_interleave(row):
        values = row.tolist()
        return interleave_bits(values, bits_per_dimension)
    
    z_order = adjusted_df.apply(map_and_interleave, axis=1)
    df['Z-order'] = z_order
    # df['Z-order_normalized'] = (df['Z-order'] - df['Z-order'].min()) / (df['Z-order'].max() - df['Z-order'].min())


    # Sort dataframe based on Z-order and save to output file
    sorted_df = df.sort_values(by='Z-order')
    sorted_df.to_csv(output_file, index=False, header=False)

def main():
    parser = argparse.ArgumentParser(description='Sort data based on Z-order curve.')
    parser.add_argument('input_file', type=str, help='Path to the input CSV file.')
    parser.add_argument('output_file', type=str, help='Path to save the sorted CSV file.')
    parser.add_argument('bits', type=int, default=20, help='Number of bits per dimension for Z-order calculation.')
    parser.add_argument('offset', type=int, default=0, help='deal with negative locations')
    
    args = parser.parse_args()

    dim = 2

    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"Input file {args.input_file} does not exist.")
    process_file(args.input_file, args.output_file, int(args.bits / dim), args.offset)
    # print(f"Processed {args.input_file} and saved sorted data to {args.output_file}.")


def test():
    # Test case for convert_data_to_int_bits
    data = {'col1': [1.1, 2.2, 3.3], 'col2': [4.4, 5.5, 6.6]}  # Example DataFrame
    df = pd.DataFrame(data)
    bit_length = 32  # Example bit length
    offset = 0.0  # Example offset
    converted_df = convert_data_to_int_bits(df, bit_length, offset)
    print("Converted DataFrame:")
    print(converted_df)

    interleaved_results = converted_df.apply(lambda row: interleave_bits(row.values, bit_length), axis=1)

    print("\nInterleaved Z-order results:")
    print(interleaved_results.tolist())

if __name__ == "__main__":
    main()
    # test()
