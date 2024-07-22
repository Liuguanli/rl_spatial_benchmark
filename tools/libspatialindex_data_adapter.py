import pandas as pd
import argparse
import os

def transform_data(input_file, output_file):
    df = pd.read_csv(input_file, header=None)

    # df[0] = pd.to_numeric(df[0], errors='coerce')
    # df[1] = pd.to_numeric(df[1], errors='coerce')


    transformed_df = pd.DataFrame({
        'Col1': 1,
        'Col2': range(len(df)),
        'Col3': df[0], 
        'Col4': df[1], 
        'Col5': df[0], 
        'Col6': df[1]
    })

    transformed_df.to_csv(output_file, sep=' ', index=False, header=False)

def transform_range_query(input_file, output_file):
    # print("Transforming range query...")

    df = pd.read_csv(input_file, header=None)

    transformed_df = pd.DataFrame({
        'Col1': 2,
        'Col2': 9999999,
        'Col3': df[0], 
        'Col4': df[1], 
        'Col5': df[2], 
        'Col6': df[3]
    })

    transformed_df.to_csv(output_file, sep=' ', index=False, header=False)

def transform_knn_query(input_file, output_file):
    # print("Transforming knn query...")
    df = pd.read_csv(input_file, header=None)

    transformed_df = pd.DataFrame({
        'Col1': 2,
        'Col2': 9999999,
        'Col3': df[0], 
        'Col4': df[1], 
        'Col5': df[0], 
        'Col6': df[1]
    })

    transformed_df.to_csv(output_file, sep=' ', index=False, header=False)

def transform_point_query(input_file, output_file):
    df = pd.read_csv(input_file, header=None)

    transformed_df = pd.DataFrame({
        'Col1': 2,
        'Col2': 9999999,
        'Col3': df[0], 
        'Col4': df[1], 
        'Col5': df[0], 
        'Col6': df[1]
    })

    transformed_df.to_csv(output_file, sep=' ', index=False, header=False)

def transform_insert(input_file, output_file):
    df = pd.read_csv(input_file, header=None)

    transformed_df = pd.DataFrame({
        'Col1': 1,
        'Col2': 9999999,
        'Col3': df[0], 
        'Col4': df[1], 
        'Col5': df[0], 
        'Col6': df[1]
    })

    transformed_df.to_csv(output_file, sep=' ', index=False, header=False)

def transform_insert_point(input_file, output_file):
    df = pd.read_csv(input_file, header=None)

    transformed_df = pd.DataFrame({
        'Col1': df[0].astype(int),
        'Col2': 9999999,
        'Col3': df[1], 
        'Col4': df[2], 
        'Col5': df[1], 
        'Col6': df[2]
    })

    transformed_df.to_csv(output_file, sep=' ', index=False, header=False)

def main():
    parser = argparse.ArgumentParser(description='Transform CSV files based on type.')
    parser.add_argument('--type', type=str, choices=['data', 'range_query', 'knn_query', 'point_query', 'insert', 'insert_point'], required=True, help='Type of transformation: data or query.')
    parser.add_argument('--input', type=str, required=True, help='Path to the input CSV file.')
    parser.add_argument('--output', type=str, required=True, help='Path to save the transformed CSV file.')
    parser.add_argument('--is_scaled', action='store_true', help='If set, scale the data.')

    parser.add_argument("--frequency", type=int, nargs='+', help="Frequency of insertions and point queries.")

    args = parser.parse_args()

    if args.type == 'data':
        transform_data(args.input, args.output) #, args.is_scaled)
    elif args.type == 'range_query':
        transform_range_query(args.input, args.output)
    elif args.type == 'knn_query':
        transform_knn_query(args.input, args.output)
    elif args.type == 'point_query':
        transform_point_query(args.input, args.output)
    elif args.type == 'insert':
        transform_insert(args.input, args.output)
    elif args.type == 'insert_point':
        transform_insert_point(args.input, args.output)
    else:
        raise ValueError("Unsupported transformation type.")

if __name__ == '__main__':
    main()
