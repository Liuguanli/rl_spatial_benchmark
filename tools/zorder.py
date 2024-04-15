# import numpy as np
# import pandas as pd
# import argparse
# import os

# def interleave_bits(values, bits_per_dimension):
#     z = 0
#     num_dimensions = len(values)
#     for bit_pos in range(bits_per_dimension):
#         for dim in range(num_dimensions):
#             z |= (values[dim] & (1 << bit_pos)) << (bit_pos * num_dimensions + dim)
#     return z

# def float_to_int_mapping(float_val, max_val, bits_per_dimension):
#     return int((float_val / max_val) * ((1 << bits_per_dimension) - 1))

# def process_file(input_file, output_file, bits_per_dimension):
#     # Load data from the input file
#     df = pd.read_csv(input_file, header=None)
#     df = (df * 1000000).astype(int)
#     num_dimensions = df.shape[1]
#     max_val = df.to_numpy().max()

#     # Map floating-point coordinates to integers and calculate Z-order values
#     def map_and_interleave(row):
#         mapped_coords = [float_to_int_mapping(row[dim], max_val, bits_per_dimension) for dim in range(num_dimensions)]
#         return interleave_bits(mapped_coords, bits_per_dimension)
    
#     z_order = df.apply(map_and_interleave, axis=1)

#     df = df / 1000000

#     df['Z-order'] = z_order

#     # Sort dataframe based on Z-order and save to output file
#     sorted_df = df.sort_values(by='Z-order')
#     # sorted_df.drop(columns=['Z-order'], inplace=True)
#     sorted_df.to_csv(output_file, index=False, header=False, sep=' ')


# def main():
#     parser = argparse.ArgumentParser(description='Sort data based on Z-order curve.')
#     parser.add_argument('input_file', type=str, help='Path to the input CSV file.')
#     parser.add_argument('output_file', type=str, help='Path to save the sorted CSV file.')
#     parser.add_argument('--bits', type=int, default=20, help='Number of bits per dimension for Z-order calculation.')
    
#     args = parser.parse_args()

#     if not os.path.exists(args.input_file):
#         raise FileNotFoundError(f"Input file {args.input_file} does not exist.")
    
#     process_file(args.input_file, args.output_file, args.bits)
#     print(f"Processed {args.input_file} and saved sorted data to {args.output_file}.")

# if __name__ == "__main__":
#     main()

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

    # Calculate Z-order values directly from the data
    def map_and_interleave(row):
        values = row.tolist()
        return interleave_bits(values, bits_per_dimension)
    
    z_order = df.apply(map_and_interleave, axis=1)
    df = df / 1000000
    df['Z-order'] = z_order

    # Sort dataframe based on Z-order and save to output file
    sorted_df = df.sort_values(by='Z-order')
    sorted_df.to_csv(output_file, index=False, header=False)

def main():
    parser = argparse.ArgumentParser(description='Sort data based on Z-order curve.')
    parser.add_argument('input_file', type=str, help='Path to the input CSV file.')
    parser.add_argument('output_file', type=str, help='Path to save the sorted CSV file.')
    parser.add_argument('--bits', type=int, default=20, help='Number of bits per dimension for Z-order calculation.')
    
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"Input file {args.input_file} does not exist.")
    
    process_file(args.input_file, args.output_file, args.bits)
    print(f"Processed {args.input_file} and saved sorted data to {args.output_file}.")

if __name__ == "__main__":
    main()
