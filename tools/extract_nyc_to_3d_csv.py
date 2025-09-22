#!/usr/bin/env python3
import argparse
import os
import pandas as pd

import re
import numpy as np

_NULLS = {"", " ", "NA", "N/A", "na", "n/a", "NULL", "Null", "null", "None", "none", "NaN", "nan", "\\N", "--"}

_unit_pat = re.compile(r"\s*(mi|mile|miles|km|kilometer|kilometre|usd|\$)\s*$", re.IGNORECASE)

def _normalize_series(s: pd.Series) -> pd.Series:
    # string normalize: commas, quotes, non-breaking space, currency/units, parentheses negatives
    ss = s.astype("string").str.replace("\xa0", " ", regex=False).str.strip()
    ss = ss.str.strip('"').str.strip("'").str.replace(",", "", regex=False)
    # (123.45) -> -123.45
    ss = ss.str.replace(r"^\(([-+]?\d*\.?\d+)\)$", r"-\1", regex=True)
    # remove trailing units/currency
    ss = ss.str.replace(_unit_pat, "", regex=True)
    # map known nulls to <NA>
    ss = ss.map(lambda x: None if x in _NULLS else x)
    return ss

def _to_float32(ss: pd.Series, fill_with=0.0) -> pd.Series:
    out = pd.to_numeric(ss, errors="coerce")
    if fill_with is not None:
        out = out.fillna(fill_with)
    return out.astype("float32")

def extract_nyc_to_3d_csv(input_csv: str, output_csv: str, cols: list[str],
                          max_rows: int = 100_000_000, chunksize: int = 1_000_000,
                          fill_nan_with: float = 0.0,
                          lon_bounds=(-75.0, -72.0), lat_bounds=(40.0, 42.0),
                          dist_bounds=(0.0, 300.0),  # cap trip distance to 300 miles/km (adjust!)
                          drop_invalid=True):        # set False to clip instead of drop
    """
    Writes a 3D CSV (no header) with x=lon, y=lat, z=distance as float32.
    - Cleans tokens robustly, coerces numeric, replaces NaN with fill_nan_with.
    - Filters by NYC-like bounds; either drops invalid rows (default) or clips.
    """
    assert len(cols) == 3, "You must provide exactly 3 column names."
    os.makedirs(os.path.dirname(output_csv) or ".", exist_ok=True)

    written = 0
    stats = dict(seen=0, coerced_nan=0, dropped_bounds=0, clipped=0)

    reader = pd.read_csv(
        input_csv,
        usecols=cols,
        chunksize=chunksize,
        dtype={c: "string" for c in cols},  # read as string to avoid mixed dtypes
        engine="python",
        on_bad_lines="skip",
        encoding_errors="replace",
    )

    for chunk in reader:
        # rename → x,y,z
        chunk = chunk.rename(columns={cols[0]: "x", cols[1]: "y", cols[2]: "z"})[["x", "y", "z"]]
        stats["seen"] += len(chunk)

        # normalize → numeric
        for c in ["x", "y", "z"]:
            norm = _normalize_series(chunk[c])
            num = pd.to_numeric(norm, errors="coerce")
            stats["coerced_nan"] += int(num.isna().sum())
            if fill_nan_with is not None:
                num = num.fillna(fill_nan_with)
            chunk[c] = num.astype("float32")

        if chunk.empty:
            continue

        # bounds check
        x, y, z = chunk["x"].to_numpy(), chunk["y"].to_numpy(), chunk["z"].to_numpy()

        if drop_invalid:
            mask = (
                (x >= lon_bounds[0]) & (x <= lon_bounds[1]) &
                (y >= lat_bounds[0]) & (y <= lat_bounds[1]) &
                (z >= dist_bounds[0]) & (z <= dist_bounds[1])
            )
            stats["dropped_bounds"] += int((~mask).sum())
            chunk = chunk.loc[mask]
        else:
            # clip instead of drop
            np.clip(x, lon_bounds[0], lon_bounds[1], out=x); stats["clipped"] += 1
            np.clip(y, lat_bounds[0], lat_bounds[1], out=y)
            np.clip(z, dist_bounds[0], dist_bounds[1], out=z)
            chunk["x"], chunk["y"], chunk["z"] = x, y, z

        if chunk.empty:
            continue

        remain = max_rows - written
        if remain <= 0:
            break
        if len(chunk) > remain:
            chunk = chunk.iloc[:remain]

        chunk.to_csv(output_csv, index=False, header=False, mode="a", float_format="%.6f")
        written += len(chunk)
        if written >= max_rows:
            break

    print(
        f"Done. Wrote {written:,} rows → {output_csv} (no header, float32). "
        f"Seen: {stats['seen']:,}, coerced-NaN: {stats['coerced_nan']:,}, "
        f"{'dropped' if drop_invalid else 'clipped'}: {stats['dropped_bounds'] if drop_invalid else stats['clipped']:,}."
    )


def main():
    parser = argparse.ArgumentParser(description="Extract 3 columns from a large CSV to build a 3D dataset (x,y,z).")
    parser.add_argument("--input", required=True, help="Path to the input CSV file (already preprocessed).")
    parser.add_argument("--output", required=True, help="Path to save the output 3D CSV file.")
    parser.add_argument("--cols", required=True, nargs=3, metavar=("COL_X", "COL_Y", "COL_Z"),
                        help="Three column names to extract as x,y,z.")
    parser.add_argument("--max_rows", type=int, default=100_000_000,
                        help="Target number of rows (default: 100 million).")
    parser.add_argument("--chunksize", type=int, default=1_000_000,
                        help="CSV chunk size (default: 1M rows).")
    args = parser.parse_args()

    extract_nyc_to_3d_csv(args.input, args.output, args.cols, args.max_rows, args.chunksize)

if __name__ == "__main__":
    main()

# python extract_nyc_to_3d_csv.py \
#   --input /media/liuguanli/T7/Ubuntu_Datasets/yellow_taxi/2009/NYC_2009_cleaned.csv \
#   --output /media/liuguanli/T7/Ubuntu_Datasets/yellow_taxi/2009/NYC_2009_100m_3d.csv \
#   --cols Start_Lon Start_Lat Trip_Distance \
#   --max_rows 100000000
