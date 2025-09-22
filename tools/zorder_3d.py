import numpy as np
import pandas as pd
import argparse
import os
import struct

# ====== Bit utilities ======
def interleave_bits_3d(values, bits_per_dimension: int) -> int:
    """
    Interleave the bits of three integer coordinates (x, y, z).
    For each bit position, distribute bits into positions:
        bit_pos*3 + 0 -> x
        bit_pos*3 + 1 -> y
        bit_pos*3 + 2 -> z
    """
    x, y, z = values
    zcode = 0
    for bit_pos in range(bits_per_dimension):
        bx = (x >> bit_pos) & 1
        by = (y >> bit_pos) & 1
        bz = (z >> bit_pos) & 1
        zcode |= (bx << (bit_pos * 3 + 0))
        zcode |= (by << (bit_pos * 3 + 1))
        zcode |= (bz << (bit_pos * 3 + 2))
    return zcode

def float_to_int_bits(value: float, shift_length: int, offset: float = 0.0) -> int:
    """
    Convert a float to an integer bit sequence.
    - Add an offset to ensure non-negative values if needed.
    - Encode as 32-bit float (IEEE754), then truncate to 'shift_length' bits.
    """
    adjusted_value = value + offset
    binary_value = struct.pack('>f', float(adjusted_value))  # big-endian float32
    int_value = int.from_bytes(binary_value, 'big')
    int_bits = int_value >> (32 - shift_length)
    return int(int_bits)

def convert_df_to_int_bits_3d(df_xyz: pd.DataFrame, bit_length: int, offset: float = 0.0) -> pd.DataFrame:
    """
    Convert each coordinate column in df_xyz (x, y, z) into integer bit sequences.
    """
    out = df_xyz.copy()
    for c in out.columns:
        out[c] = out[c].apply(float_to_int_bits, args=(bit_length, offset))
    return out

# ====== Input loader ======
def load_xyz_3d(input_file: str) -> pd.DataFrame:
    """
    Load 3D coordinates into a DataFrame with columns [0:x, 1:y, 2:z].
    Supported input:
      - General CSV (header=None):
          * If >=3 columns: take the first 3 as x, y, z.
          * If only 2 columns: take x, y and set z=0.
      - "tiger" dataset:
          * If columns contain minx, miny, maxx, maxy: use center as x,y.
          * If also contain minz, maxz: use center as z, else z=0.
    """
    if "tiger" in input_file:
        df = pd.read_csv(input_file)
        if {'minx','miny','maxx','maxy'}.issubset(df.columns):
            x_center = (df['minx'] + df['maxx']) / 2.0
            y_center = (df['miny'] + df['maxy']) / 2.0
        else:
            raise ValueError("Tiger input missing minx/miny/maxx/maxy columns")

        if {'minz','maxz'}.issubset(df.columns):
            z_center = (df['minz'] + df['maxz']) / 2.0
        else:
            z_center = pd.Series(np.zeros(len(df)), index=df.index)

        xyz = pd.concat([x_center, y_center, z_center], axis=1)
        xyz.columns = [0, 1, 2]
        return xyz

    # General CSV
    raw = pd.read_csv(input_file, header=None)
    if raw.shape[1] >= 3:
        xyz = raw.iloc[:, :3].copy()
        xyz.columns = [0, 1, 2]
    elif raw.shape[1] == 2:
        xyz = pd.DataFrame({0: raw.iloc[:, 0], 1: raw.iloc[:, 1], 2: 0.0})
    else:
        raise ValueError("Input must have at least 2 columns (x,y).")
    return xyz

# ====== Processing ======
def process_file_3d(input_file: str, output_file: str, bits_per_dimension: int, offset: float = 0.0):
    """
    Main pipeline:
      1. Load (x,y,z) coordinates from input_file.
      2. Convert float coords to integer bit sequences.
      3. Compute 3D Z-order value for each row.
      4. Sort by Z-order and write to output_file.
    """
    df_xyz = load_xyz_3d(input_file)
    df_bits = convert_df_to_int_bits_3d(df_xyz, bits_per_dimension, offset)

    z_vals = df_bits.apply(lambda row: interleave_bits_3d(row.values.tolist(), bits_per_dimension), axis=1)

    out = df_xyz.copy()
    out['Z-order'] = z_vals
    # Use mergesort for stable ordering
    out = out.sort_values('Z-order', kind='mergesort')
    out.to_csv(output_file, index=False, header=False)

# ====== CLI entry ======
def main():
    parser = argparse.ArgumentParser(description='Sort 3D data based on Z-order curve.')
    parser.add_argument('input_file', type=str, help='Path to the input CSV file.')
    parser.add_argument('output_file', type=str, help='Path to save the sorted CSV file.')
    parser.add_argument('bits', type=int, nargs='?', default=20, help='Bits per dimension (default: 20).')
    parser.add_argument('--offset', type=float, default=0.0, help='Offset to shift all coords into non-negative range.')
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"Input file {args.input_file} does not exist.")

    process_file_3d(args.input_file, args.output_file, args.bits, args.offset)

if __name__ == "__main__":
    main()
