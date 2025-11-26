import pandas as pd
import argparse
import os
import numpy as np

def transform_data_md(input_file, output_file, is_learned, dim):
    df = pd.read_csv(input_file, header=None)

    # df[0] = pd.to_numeric(df[0], errors='coerce')
    # df[1] = pd.to_numeric(df[1], errors='coerce')
    # print(df.head())
    # print(df.tail())
    # df = df.head()
    # n, d = df.shape
    transformed_df = {
        "Col1": [1] * len(df),
        "Col2": list(range(len(df))),
    }

    for j in range(dim):
        transformed_df[f"Col{3+j}"] = df[j]          # min
    for j in range(dim):
        transformed_df[f"Col{3+dim+j}"] = df[j]        # max

    if is_learned:
        if df.shape[1] > dim:  # Check if there are more than 'dim' columns
            transformed_df[f"Col{3+dim+dim}"] = df[dim]

    transformed_df = pd.DataFrame(transformed_df)

    transformed_df.to_csv(output_file, sep=' ', index=False, header=False)

def transform_data(input_file, output_file, is_learned):
    print(input_file)
    if "tiger" in input_file:
        df = pd.read_csv(input_file, usecols=["minx", "miny", "maxx", "maxy"],
                        dtype={"minx": float, "miny": float, "maxx": float, "maxy": float})
        
        # new DataFrame
        transformed_df = pd.DataFrame({
            'Col1': [1] * len(df),
            'Col2': list(range(len(df))),
            'Col3': df['minx'].values,
            'Col4': df['miny'].values,
            'Col5': df['maxx'].values,
            'Col6': df['maxy'].values
        })
    else:
        df = pd.read_csv(input_file, header=None)

        # df[0] = pd.to_numeric(df[0], errors='coerce')
        # df[1] = pd.to_numeric(df[1], errors='coerce')
        # print(df.head())
        # print(df.tail())
        # df = df.head()
        transformed_df = pd.DataFrame({
            'Col1': 1, 
            'Col2': range(len(df)), 
            'Col3': df[0], 
            'Col4': df[1], 
            'Col5': df[0], 
            'Col6': df[1]
        })

    if is_learned:
        if df.shape[1] > 2:  # Check if there are more than two columns
            transformed_df['Col7'] = df[2]

    transformed_df.to_csv(output_file, sep=' ', index=False, header=False)

def transform_range_query(input_file, output_file, dim):
    # print("Transforming range query...")

    df = pd.read_csv(input_file, header=None)

    transformed_df = {
        "Col1": 2,
        "Col2": 9999999,
    }

    for j in range(dim * 2):
        transformed_df[f"Col{3+j}"] = df[j]   

    transformed_df = pd.DataFrame(transformed_df)

    # transformed_df = pd.DataFrame({
    #     'Col1': 2,
    #     'Col2': 9999999,
    #     'Col3': df[0], 
    #     'Col4': df[1], 
    #     'Col5': df[2], 
    #     'Col6': df[3]
    # })

    transformed_df.to_csv(output_file, sep=' ', index=False, header=False)

def transform_join(input_file, output_file, dim):
    # print("Transforming join query...")

    df = pd.read_csv(input_file, header=None)

    transformed_df = {
        "Col1": 2,
        "Col2": 9999999,
    }

    for j in range(dim * 2):
        transformed_df[f"Col{3+j}"] = df[j]   
  
    transformed_df = pd.DataFrame(transformed_df)

    # transformed_df = pd.DataFrame({
    #     'Col1': 2,
    #     'Col2': 9999999,
    #     'Col3': df[0], 
    #     'Col4': df[1], 
    #     'Col5': df[2], 
    #     'Col6': df[3]
    # })

    transformed_df.to_csv(output_file, sep=' ', index=False, header=False)


def transform_knn_query(input_file, output_file, dim):
    # print("Transforming knn query...")
    df = pd.read_csv(input_file, header=None)

    transformed_df = {
        "Col1": 2,
        "Col2": 9999999,
    }

    for j in range(dim):
        transformed_df[f"Col{3+j}"] = df[j]          # min
    for j in range(dim):
        transformed_df[f"Col{3+dim+j}"] = df[j]        # max

    transformed_df = pd.DataFrame(transformed_df)

    # transformed_df = pd.DataFrame({
    #     'Col1': 2,
    #     'Col2': 9999999,
    #     'Col3': df[0], 
    #     'Col4': df[1], 
    #     'Col5': df[0], 
    #     'Col6': df[1]
    # })

    transformed_df.to_csv(output_file, sep=' ', index=False, header=False)

def transform_point_query(input_file, output_file, dim):
    df = pd.read_csv(input_file, header=None)

    transformed_df = {
        "Col1": 2,
        "Col2": 9999999,
    }

    for j in range(dim):
        transformed_df[f"Col{3+j}"] = df[j]          # min
    for j in range(dim):
        transformed_df[f"Col{3+dim+j}"] = df[j]        # max

    transformed_df = pd.DataFrame(transformed_df)
    # transformed_df = pd.DataFrame({
    #     'Col1': 2,
    #     'Col2': 9999999,
    #     'Col3': df[0], 
    #     'Col4': df[1], 
    #     'Col5': df[0], 
    #     'Col6': df[1]
    # })

    transformed_df.to_csv(output_file, sep=' ', index=False, header=False)

def transform_insert(input_file, output_file, dim):
    df = pd.read_csv(input_file, header=None)

    transformed_df = {
        "Col1": 1,
        "Col2": 9999999,
    }

    for j in range(dim):
        transformed_df[f"Col{3+j}"] = df[j]          # min
    for j in range(dim):
        transformed_df[f"Col{3+dim+j}"] = df[j]        # max

    transformed_df = pd.DataFrame(transformed_df)

    # transformed_df = pd.DataFrame({
    #     'Col1': 1,
    #     'Col2': 9999999,
    #     'Col3': df[0], 
    #     'Col4': df[1], 
    #     'Col5': df[0], 
    #     'Col6': df[1]
    # })

    transformed_df.to_csv(output_file, sep=' ', index=False, header=False)

def transform_insert_point(input_file, output_file, dim):
    df = pd.read_csv(input_file, header=None)

    transformed_df = {
        "Col1": df[0].astype(int),
        "Col2": 9999999,
    }

    for j in range(dim):
        transformed_df[f"Col{3+j}"] = df[j + 1]          # min
    for j in range(dim):
        transformed_df[f"Col{3+dim+j}"] = df[j + 1]        # max

    transformed_df = pd.DataFrame(transformed_df)

    # transformed_df = pd.DataFrame({
    #     'Col1': df[0].astype(int),
    #     'Col2': 9999999,
    #     'Col3': df[1], 
    #     'Col4': df[2], 
    #     'Col5': df[1], 
    #     'Col6': df[2]
    # })

    transformed_df.to_csv(output_file, sep=' ', index=False, header=False)

def main():
    parser = argparse.ArgumentParser(description='Transform CSV files based on type.')
    parser.add_argument('--type', type=str, choices=['data', 'range_query', 'knn_query', 'point_query', 'insert', 'insert_point', 'join'], required=True, help='Type of transformation: data or query.')
    parser.add_argument('--input', type=str, required=True, help='Path to the input CSV file.')
    parser.add_argument('--output', type=str, required=True, help='Path to save the transformed CSV file.')
    parser.add_argument('--is_scaled', action='store_true', help='If set, scale the data.')
    parser.add_argument('--is_learned', type=bool, default=False, help='If learned')
    parser.add_argument("--dimensions", type=int, required=False, default=2, help="Number of dimensions for the data points.")


    parser.add_argument("--frequency", type=int, nargs='+', help="Frequency of insertions and point queries.")

    args = parser.parse_args()

    if args.type == 'data':
        if args.dimensions > 2:
            transform_data_md(args.input, args.output, args.is_learned, args.dimensions) #, args.is_scaled)
        else:
            transform_data(args.input, args.output, args.is_learned) #, args.is_scaled)
    elif args.type == 'range_query':
        transform_range_query(args.input, args.output, args.dimensions)
    elif args.type == 'join':
        transform_join(args.input, args.output, args.dimensions)
    elif args.type == 'knn_query':
        transform_knn_query(args.input, args.output, args.dimensions)
    elif args.type == 'point_query':
        transform_point_query(args.input, args.output, args.dimensions)
    elif args.type == 'insert':
        transform_insert(args.input, args.output, args.dimensions)
    elif args.type == 'insert_point':
        transform_insert_point(args.input, args.output, args.dimensions)
    else:
        raise ValueError("Unsupported transformation type.")

if __name__ == '__main__':
    main()
