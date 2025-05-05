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

    is_tiger = "tiger" in input_file
    if is_tiger:
        df_raw = pd.read_csv(input_file, header=0, usecols=["minx", "miny", "maxx", "maxy"],
                            dtype={"minx": float, "miny": float, "maxx": float, "maxy": float})
        
        x_center = (df_raw["minx"] + df_raw["maxx"]) / 2
        y_center = (df_raw["miny"] + df_raw["maxy"]) / 2
        
        df = pd.concat([x_center, y_center], axis=1)
        df.columns = [0, 1] 
    else:

        df = pd.read_csv(input_file, header=None)
    df_copy = df.copy()
    adjusted_df = convert_data_to_int_bits(df_copy, bits_per_dimension, offset)

    # Calculate Z-order values directly from the data
    def map_and_interleave(row):
        values = row.tolist()
        return interleave_bits(values, bits_per_dimension)
    
    z_order = adjusted_df.apply(map_and_interleave, axis=1)
    df['Z-order'] = z_order

    # Sort dataframe based on Z-order and save to output file
    sorted_df = df.sort_values(by='Z-order')
    sorted_df.to_csv(output_file, index=False, header=False)

def main():
    parser = argparse.ArgumentParser(description='Sort data based on Z-order curve.')
    parser.add_argument('input_file', type=str, help='Path to the input CSV file.')
    parser.add_argument('output_file', type=str, help='Path to save the sorted CSV file.')
    parser.add_argument('bits', type=int, default=20, help='Number of bits per dimension for Z-order calculation.')
    
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"Input file {args.input_file} does not exist.")
    offset = 0
    process_file(args.input_file, args.output_file, args.bits, offset)
    # print(f"Processed {args.input_file} and saved sorted data to {args.output_file}.")

if __name__ == "__main__":
    main()
