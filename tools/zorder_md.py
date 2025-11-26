import numpy as np
import pandas as pd
import argparse
import os
import struct
from typing import List

# ====== Bit utilities ======
def interleave_bits_md(values: List[int], bits_per_dimension: int) -> int:
    """
    Interleave bits for d-dimensional integer coordinates (len(values) == d).
    For each bit position b in [0, bits_per_dimension):
      emit bit of dimension 0, then 1, ..., then d-1.
    The final Morton (Z-order) code packs bits in the order:
      [b0_dim0, b0_dim1, ..., b0_dim{d-1}, b1_dim0, b1_dim1, ...]
    """
    d = len(values)
    zcode = 0
    for b in range(bits_per_dimension):
        for i, v in enumerate(values):
            bit = (v >> b) & 1
            zcode |= (bit << (b * d + i))
    return zcode

def float_to_int_bits(value: float, shift_length: int, offset: float = 0.0) -> int:
    """
    Convert a float to the top `shift_length` bits of its IEEE754 float32 encoding.
    Note: this is fast and matches your original approach, but it does NOT strictly
    preserve numeric ordering for negatives or mixed scales.
    """
    adjusted_value = value + offset
    binary_value = struct.pack('>f', float(adjusted_value))  # big-endian float32
    int_value = int.from_bytes(binary_value, 'big')
    int_bits = int_value >> (32 - shift_length)
    return int(int_bits)

def map_float_to_uint(value: float, vmin: float, vmax: float, bits: int) -> int:
    """
    Linearly scale value to [0, 2^bits - 1].
    This preserves numeric ordering (recommended for robust sorting).
    """
    if vmax <= vmin:
        return 0
    t = (value - vmin) / (vmax - vmin)
    t = 0.0 if t < 0 else (1.0 if t > 1 else t)
    return int(round(t * ((1 << bits) - 1)))

def convert_df_to_int_bits_md(
    df_coords: pd.DataFrame,
    bit_length: int,
    offset: float = 0.0,
    mode: str = "ieee",
    mins=None,
    maxs=None,
) -> pd.DataFrame:
    """
    Convert each coordinate column to an integer bit sequence.

    Parameters
    ----------
    df_coords : DataFrame with shape (n, d)
    bit_length : bits per dimension
    offset : used only in "ieee" mode
    mode : "ieee" (fast, original behavior) or "scale" (order-preserving)
    mins, maxs : per-dimension min/max for "scale" mode; if None, use data mins/maxs
    """
    out = df_coords.copy()
    if mode == "ieee":
        for c in out.columns:
            out[c] = out[c].apply(float_to_int_bits, args=(bit_length, offset))
    elif mode == "scale":
        if mins is None:
            mins = out.min(axis=0).values
        if maxs is None:
            maxs = out.max(axis=0).values
        for idx, c in enumerate(out.columns):
            vmin, vmax = float(mins[idx]), float(maxs[idx])
            out[c] = out[c].apply(map_float_to_uint, args=(vmin, vmax, bit_length))
    else:
        raise ValueError("mode must be 'ieee' or 'scale'")
    return out

# ====== Input loader ======
def load_coords_md(input_file: str, dim: int) -> pd.DataFrame:
    """
    Load coordinates from a generic CSV (no header).
    - If the file has >= dim columns: use the first dim columns.
    - If fewer: pad with zeros up to dim.
    """
    raw = pd.read_csv(input_file, header=None)
    c = raw.shape[1]
    if c >= dim:
        coords = raw.iloc[:, :dim].copy()
    else:
        pads = [0.0] * (dim - c)
        coords = pd.concat([raw, pd.DataFrame([pads] * len(raw), index=raw.index)], axis=1)
    coords.columns = list(range(dim))
    return coords

# ====== Processing ======
def process_file_md(
    input_file: str,
    output_file: str,
    bits_per_dimension: int,
    dim: int,
    offset: float = 0.0,
    mode: str = "ieee",
):
    """
    Pipeline:
      1) Read first `dim` columns (pad zeros if needed).
      2) Encode floats -> integer bit sequences ("ieee" or "scale").
      3) Compute d-D Morton (Z-order) code.
      4) Stable-sort by Z-order and write CSV (no header).
    """
    df_coords = load_coords_md(input_file, dim)
    df_bits = convert_df_to_int_bits_md(df_coords, bits_per_dimension, offset, mode=mode)

    z_vals = df_bits.apply(
        lambda row: interleave_bits_md(row.values.tolist(), bits_per_dimension), axis=1
    )

    out = df_coords.copy()
    out["Z-order"] = z_vals
    out = out.sort_values("Z-order", kind="mergesort")
    out.to_csv(output_file, index=False, header=False)

# ====== CLI entry ======
def main():
    parser = argparse.ArgumentParser(description="Sort d-dimensional data by Z-order (Morton) key.")
    parser.add_argument("input_file", type=str, help="Path to the input CSV file.")
    parser.add_argument("output_file", type=str, help="Path to save the sorted CSV file.")
    parser.add_argument("--dim", type=int, default=4, help="Number of dimensions (default: 3).")
    parser.add_argument("--bits", type=int, default=20, help="Bits per dimension (default: 20).")
    parser.add_argument("--offset", type=float, default=0.0, help="Offset for IEEE mode.")
    parser.add_argument(
        "--mode",
        type=str,
        default="ieee",
        choices=["ieee", "scale"],
        help="Encoding mode: 'ieee' (fast, original) or 'scale' (order-preserving).",
    )
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"Input file {args.input_file} does not exist.")

    process_file_md(
        args.input_file, args.output_file, args.bits, args.dim, args.offset, args.mode
    )

if __name__ == "__main__":
    main()
