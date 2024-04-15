import os
import pandas as pd

def convert_json_to_csv(json_file, target_directory):

    # Define the CSV file path based on the JSON file name
    csv_file = os.path.join(target_directory, os.path.splitext(os.path.basename(json_file))[0] + ".csv")
    
    # Read the JSON file
    df = pd.read_json(json_file)
    df = (df / 1000000).astype(float)

        # Sample 1% of the data
    df = df.sample(frac=0.0001)

    
    # Convert the DataFrame to CSV and save
    df.to_csv(csv_file, index=False, header=False)  # index=False means do not write row indices
    
    print(f"Converted {json_file} to {csv_file}")

# Example usage
json_file_path = '/home/research/datasets/OSM_100000000.json'
convert_json_to_csv(json_file_path, "/home/research/datasets")
