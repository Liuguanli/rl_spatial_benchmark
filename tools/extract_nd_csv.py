# #!/usr/bin/env python3
# import argparse
# import os
# import pandas as pd

# import re
# import numpy as np

# _NULLS = {"", " ", "NA", "N/A", "na", "n/a", "NULL", "Null", "null", "None", "none", "NaN", "nan", "\\N", "--"}

# _unit_pat = re.compile(r"\s*(mi|mile|miles|km|kilometer|kilometre|usd|\$)\s*$", re.IGNORECASE)

# def _normalize_series(s: pd.Series) -> pd.Series:
#     # string normalize: commas, quotes, non-breaking space, currency/units, parentheses negatives
#     ss = s.astype("string").str.replace("\xa0", " ", regex=False).str.strip()
#     ss = ss.str.strip('"').str.strip("'").str.replace(",", "", regex=False)
#     # (123.45) -> -123.45
#     ss = ss.str.replace(r"^\(([-+]?\d*\.?\d+)\)$", r"-\1", regex=True)
#     # remove trailing units/currency
#     ss = ss.str.replace(_unit_pat, "", regex=True)
#     # map known nulls to <NA>
#     ss = ss.map(lambda x: None if x in _NULLS else x)
#     return ss

# def _to_float32(ss: pd.Series, fill_with=0.0) -> pd.Series:
#     out = pd.to_numeric(ss, errors="coerce")
#     if fill_with is not None:
#         out = out.fillna(fill_with)
#     return out.astype("float32")

# def extract_nyc_to_3d_csv(input_csv: str, output_csv: str, cols: list[str],
#                           max_rows: int = 100_000_000, chunksize: int = 1_000_000,
#                           fill_nan_with: float = 0.0,
#                           lon_bounds=(-75.0, -72.0), lat_bounds=(40.0, 42.0),
#                           dist_bounds=(0.0, 300.0),  # cap trip distance to 300 miles/km (adjust!)
#                           drop_invalid=True):        # set False to clip instead of drop
#     """
#     Writes a 3D CSV (no header) with x=lon, y=lat, z=distance as float32.
#     - Cleans tokens robustly, coerces numeric, replaces NaN with fill_nan_with.
#     - Filters by NYC-like bounds; either drops invalid rows (default) or clips.
#     """
#     assert len(cols) == 3, "You must provide exactly 3 column names."
#     os.makedirs(os.path.dirname(output_csv) or ".", exist_ok=True)

#     written = 0
#     stats = dict(seen=0, coerced_nan=0, dropped_bounds=0, clipped=0)

#     reader = pd.read_csv(
#         input_csv,
#         usecols=cols,
#         chunksize=chunksize,
#         dtype={c: "string" for c in cols},  # read as string to avoid mixed dtypes
#         engine="python",
#         on_bad_lines="skip",
#         encoding_errors="replace",
#     )

#     for chunk in reader:
#         # rename → x,y,z
#         chunk = chunk.rename(columns={cols[0]: "x", cols[1]: "y", cols[2]: "z"})[["x", "y", "z"]]
#         stats["seen"] += len(chunk)

#         # normalize → numeric
#         for c in ["x", "y", "z"]:
#             norm = _normalize_series(chunk[c])
#             num = pd.to_numeric(norm, errors="coerce")
#             stats["coerced_nan"] += int(num.isna().sum())
#             if fill_nan_with is not None:
#                 num = num.fillna(fill_nan_with)
#             chunk[c] = num.astype("float32")

#         if chunk.empty:
#             continue

#         # bounds check
#         x, y, z = chunk["x"].to_numpy(), chunk["y"].to_numpy(), chunk["z"].to_numpy()

#         if drop_invalid:
#             mask = (
#                 (x >= lon_bounds[0]) & (x <= lon_bounds[1]) &
#                 (y >= lat_bounds[0]) & (y <= lat_bounds[1]) &
#                 (z >= dist_bounds[0]) & (z <= dist_bounds[1])
#             )
#             stats["dropped_bounds"] += int((~mask).sum())
#             chunk = chunk.loc[mask]
#         else:
#             # clip instead of drop
#             np.clip(x, lon_bounds[0], lon_bounds[1], out=x); stats["clipped"] += 1
#             np.clip(y, lat_bounds[0], lat_bounds[1], out=y)
#             np.clip(z, dist_bounds[0], dist_bounds[1], out=z)
#             chunk["x"], chunk["y"], chunk["z"] = x, y, z

#         if chunk.empty:
#             continue

#         remain = max_rows - written
#         if remain <= 0:
#             break
#         if len(chunk) > remain:
#             chunk = chunk.iloc[:remain]

#         chunk.to_csv(output_csv, index=False, header=False, mode="a", float_format="%.6f")
#         written += len(chunk)
#         if written >= max_rows:
#             break

#     print(
#         f"Done. Wrote {written:,} rows → {output_csv} (no header, float32). "
#         f"Seen: {stats['seen']:,}, coerced-NaN: {stats['coerced_nan']:,}, "
#         f"{'dropped' if drop_invalid else 'clipped'}: {stats['dropped_bounds'] if drop_invalid else stats['clipped']:,}."
#     )


# def main():
#     parser = argparse.ArgumentParser(description="Extract 3 columns from a large CSV to build a 3D dataset (x,y,z).")
#     parser.add_argument("--input", required=True, help="Path to the input CSV file (already preprocessed).")
#     parser.add_argument("--output", required=True, help="Path to save the output 3D CSV file.")
#     parser.add_argument("--cols", required=True, nargs=3, metavar=("COL_X", "COL_Y", "COL_Z"),
#                         help="Three column names to extract as x,y,z.")
#     parser.add_argument("--max_rows", type=int, default=100_000_000,
#                         help="Target number of rows (default: 100 million).")
#     parser.add_argument("--chunksize", type=int, default=1_000_000,
#                         help="CSV chunk size (default: 1M rows).")
#     args = parser.parse_args()

#     extract_nyc_to_3d_csv(args.input, args.output, args.cols, args.max_rows, args.chunksize)

# if __name__ == "__main__":
#     main()


#!/usr/bin/env python3
import argparse
import os
import re
import numpy as np
import pandas as pd
from typing import Dict, Tuple, List, Optional

_NULLS = {"", " ", "NA", "N/A", "na", "n/a", "NULL", "Null", "null", "None", "none", "NaN", "nan", "\\N", "--"}
_unit_pat = re.compile(r"\s*(mi|mile|miles|km|kilometer|kilometre|usd|\$)\s*$", re.IGNORECASE)

def _normalize_series(s: pd.Series) -> pd.Series:
    ss = s.astype("string").str.replace("\xa0", " ", regex=False).str.strip()
    ss = ss.str.strip('"').str.strip("'").str.replace(",", "", regex=False)
    ss = ss.str.replace(r"^\(([-+]?\d*\.?\d+)\)$", r"-\1", regex=True)  # (123.45) -> -123.45
    ss = ss.str.replace(_unit_pat, "", regex=True)
    ss = ss.map(lambda x: None if x in _NULLS else x)
    return ss

def _parse_bounds(bound_list: List[str]) -> Dict[str, Tuple[float, float]]:
    """
    Each item like 'COL:MIN:MAX'. Example: --bounds lon:-75:-72 --bounds lat:40:42
    """
    out: Dict[str, Tuple[float, float]] = {}
    for spec in bound_list or []:
        try:
            col, lo, hi = spec.split(":", 2)
            out[col] = (float(lo), float(hi))
        except Exception as e:
            raise ValueError(f"Invalid --bounds '{spec}'. Use COL:MIN:MAX") from e
    return out

def extract_to_md_csv(
    input_csv: str,
    output_csv: str,
    cols: List[str],
    max_rows: int = 100_000_000,
    chunksize: int = 1_000_000,
    fill_nan_with: Optional[float] = 0.0,
    bounds: Optional[Dict[str, Tuple[float, float]]] = None,
    drop_invalid: bool = True,
):
    """
    Write an N-D CSV (no header) with selected columns coerced to float32.
    - `cols`: 2+ column names, order preserved in output.
    - `bounds`: optional dict {col: (min, max)}; applies per-column.
    - `drop_invalid=True`: drop rows violating any bounded column; else clip per bounded column.
    """
    assert len(cols) >= 2, "Provide at least 2 columns for N-D output."
    os.makedirs(os.path.dirname(output_csv) or ".", exist_ok=True)

    bounds = bounds or {}
    stats = {
        "seen": 0,
        "written": 0,
        "dropped_bounds": 0,
        "clipped_rows": 0,
        "coerced_nan": {c: 0 for c in cols},
    }

    reader = pd.read_csv(
        input_csv,
        usecols=cols,
        chunksize=chunksize,
        dtype={c: "string" for c in cols},
        engine="python",
        on_bad_lines="skip",
        encoding_errors="replace",
    )

    for chunk in reader:
        stats["seen"] += len(chunk)
        if chunk.empty:
            continue

        # normalize -> numeric (float32), track NaNs per column
        for c in cols:
            norm = _normalize_series(chunk[c])
            num = pd.to_numeric(norm, errors="coerce")
            stats["coerced_nan"][c] += int(num.isna().sum())
            if fill_nan_with is not None:
                num = num.fillna(fill_nan_with)
            chunk[c] = num.astype("float32")

        if chunk.empty:
            continue

        # bounds enforcement
        if bounds:
            if drop_invalid:
                mask = np.ones(len(chunk), dtype=bool)
                for c, (lo, hi) in bounds.items():
                    if c in chunk.columns:
                        v = chunk[c].to_numpy()
                        mask &= (v >= lo) & (v <= hi)
                stats["dropped_bounds"] += int((~mask).sum())
                chunk = chunk.loc[mask]
                if chunk.empty:
                    continue
            else:
                # clip per bounded column
                before = len(chunk)
                for c, (lo, hi) in bounds.items():
                    if c in chunk.columns:
                        v = chunk[c].to_numpy()
                        np.clip(v, lo, hi, out=v)
                        chunk[c] = v
                stats["clipped_rows"] += before  # count rows touched (approx)

        # write with cap
        remain = max_rows - stats["written"]
        if remain <= 0:
            break
        if len(chunk) > remain:
            chunk = chunk.iloc[:remain]

        # ensure column order
        out = chunk[cols]
        out.to_csv(output_csv, index=False, header=False, mode="a", float_format="%.6f")
        stats["written"] += len(out)
        if stats["written"] >= max_rows:
            break

    # summary
    percol = ", ".join(f"{c}: {stats['coerced_nan'][c]:,}" for c in cols)
    action = "dropped" if drop_invalid else "clipped"
    print(
        f"Done. Wrote {stats['written']:,} rows → {output_csv} (no header, float32). "
        f"Seen: {stats['seen']:,}. Coerced-NaN per col [{percol}]. "
        f"{action}: {stats['dropped_bounds'] if drop_invalid else stats['clipped_rows']:,}."
    )

def main():
    p = argparse.ArgumentParser(description="Extract N columns from a large CSV to build an N-D dataset (float32, no header).")
    p.add_argument("--input", required=True, help="Path to the input CSV file.")
    p.add_argument("--output", required=True, help="Path to save the output CSV (no header).")
    p.add_argument("--cols", required=True, nargs="+", help="Column names to extract (2 or more). Order is preserved.")
    p.add_argument("--max_rows", type=int, default=100_000_000, help="Max rows to write (default: 100M).")
    p.add_argument("--chunksize", type=int, default=1_000_000, help="CSV chunk size (default: 1M).")
    p.add_argument("--fill_nan_with", type=float, default=0.0, help="Value to fill NaNs with; set to None to keep NaN.")
    p.add_argument("--bounds", action="append", default=[],
                   help="Per-column bounds as COL:MIN:MAX. Repeatable. Example: --bounds lon:-75:-72 --bounds lat:40:42")
    p.add_argument("--clip", action="store_true", help="Clip out-of-bounds instead of dropping rows.")
    args = p.parse_args()

    bounds = _parse_bounds(args.bounds)
    extract_to_md_csv(
        input_csv=args.input,
        output_csv=args.output,
        cols=args.cols,
        max_rows=args.max_rows,
        chunksize=args.chunksize,
        fill_nan_with=args.fill_nan_with if args.fill_nan_with is not None else None,
        bounds=bounds,
        drop_invalid=not args.clip,
    )

if __name__ == "__main__":
    main()

# python extract_nyc_to_3d_csv.py \
#   --input /media/liuguanli/T7/Ubuntu_Datasets/yellow_taxi/2009/NYC_2009_cleaned.csv \
#   --output /media/liuguanli/T7/Ubuntu_Datasets/yellow_taxi/2009/NYC_2009_100m_3d.csv \
#   --cols Start_Lon Start_Lat Trip_Distance \  # Total_Amt
#   --max_rows 100000000

# python tools/extract_nd_csv.py \
#   --input /media/liuguanli/T7/Ubuntu_Datasets/yellow_taxi/2009/NYC_2009_cleaned.csv \
#   --output /media/liuguanli/T7/Ubuntu_Datasets/yellow_taxi/2009/NYC_2009_100m_4d.csv \
#   --cols Start_Lon Start_Lat Trip_Distance Total_Amt \
#   --bounds Start_Lon:-75:-72 --bounds Start_Lat:40:42 --bounds Trip_Distance:0:300 \
#   --clip
