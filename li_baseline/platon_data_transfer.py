import os
import pandas as pd
import numpy as np
import json
import sys


def convert_csv_to_npy(csv_file, target_directory):
    """
    Converts a CSV file containing point data without headers into an .npy file with rectangular format.
    
    Parameters:
    csv_file (str): Path to the input CSV file.
    target_directory (str): Directory where the output .npy file will be saved.
    """
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)  # Create the target directory if it does not exist

    # Define the output file path
    npy_file = os.path.join(target_directory, os.path.splitext(os.path.basename(csv_file))[0] + ".npy")
    
    # Load data from the CSV file without headers
    if "tiger" in csv_file and "dataset" in csv_file:
        data = pd.read_csv(csv_file, header=None, skiprows=1)
    else:
        data = pd.read_csv(csv_file, header=None)
    # data = pd.read_csv(csv_file, header=None)
    

    # Assume the first column is x and the second column is y
    if data.shape[1] >= 2:  # Ensure there are at least two columns
        x = data[0]
        y = data[1]
        
        # Convert data by setting x_min, x_max, y_min, and y_max to the same x and y values for each point
        rectangles = np.column_stack((x, x, y, y))
        
        # Save as an .npy file
        np.save(npy_file, rectangles)
        
        print(f"Converted {csv_file} to {npy_file}")
    else:
        print("The CSV file does not contain at least two columns. Please check the file format.")


def convert_to_geojson(input_csv, target_directory):
    """
    Converts a CSV file containing rectangular bounds (minx, miny, maxx, maxy) without headers into a GeoJSON file.
    
    Parameters:
    input_csv (str): Path to the input CSV file.
    target_directory (str): Path to the output GeoJSON file.
    """
    # Load the CSV file without headers and specify column names
    data = pd.read_csv(input_csv, header=None, names=["minx", "miny", "maxx", "maxy"])

    # Initialize the GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            }
        },
        "features": []
    }

    # Populate the features
    for _, row in data.iterrows():
        minx, miny, maxx, maxy = row["minx"], row["miny"], row["maxx"], row["maxy"]
        feature = {
            "type": "Feature",
            "properties": {
                "minx": minx,
                "maxx": maxx,
                "miny": miny,
                "maxy": maxy
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [minx, miny],
                    [maxx, miny],
                    [maxx, maxy],
                    [minx, maxy],
                    [minx, miny]
                ]]
            }
        }
        geojson["features"].append(feature)
    
    # Write the GeoJSON to a file
    geojson_file = os.path.join(target_directory, os.path.splitext(os.path.basename(input_csv))[0] + ".geojson")

    with open(geojson_file, 'w') as f:
        json.dump(geojson, f, indent=2)

    print(f"Converted {input_csv} to {target_directory}")

target_directory = "./benchmark/libspatialindex"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <csv_file1> <csv_file2>")
        sys.exit(1)
    
    csv_data, csv_query = sys.argv[1:3]
    
    convert_csv_to_npy(csv_data, target_directory)
    
    convert_to_geojson(csv_query, target_directory)
