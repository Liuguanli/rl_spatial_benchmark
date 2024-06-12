import os
import sys
import pandas as pd
import struct


sub_dir = "./rl_baseline"
repo_path = os.path.join(sub_dir, "Learned-BMTree")


def float_to_int_bits(value, shift_length):
    binary_value = struct.pack('>f', value)
    int_value = int.from_bytes(binary_value, 'big')
    int_20_bits = int_value >> (32 - shift_length)
    return int(int_20_bits)

def convert_data_to_int_bits(data_frame, bit_length):
    for col in data_frame.columns:
        data_frame[col] = data_frame[col].apply(float_to_int_bits, args=(bit_length,))
    return data_frame

def convert_csv_to_json(csv_file, target_directory, bit_length=20):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)  

    json_file = os.path.join(target_directory, os.path.splitext(os.path.basename(csv_file))[0] + ".json")
    
    df = pd.read_csv(csv_file, header=None)
    df = convert_data_to_int_bits(df, bit_length)

    df.to_json(json_file, orient='values', indent=0)
    
    print(f"Converted {csv_file} to {json_file}")



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <csv_file1> <csv_file2>")
        sys.exit(1)
    
    csv_file1, csv_file2 = sys.argv[1:3]
    
    convert_csv_to_json(csv_file1, os.path.join(repo_path, "data"))
    
    convert_csv_to_json(csv_file2, os.path.join(repo_path, "query"))
