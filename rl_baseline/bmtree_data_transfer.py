import os
import sys
import pandas as pd

sub_dir = "./rl_baseline"
repo_path = os.path.join(sub_dir, "Learned-BMTree")

def convert_csv_to_json(csv_file, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)  

    json_file = os.path.join(target_directory, os.path.splitext(os.path.basename(csv_file))[0] + ".json")
    
    df = pd.read_csv(csv_file, header=None)
    df = (df * 1000000).astype(int)
    df.to_json(json_file, orient='values', indent=0)
    
    print(f"Converted {csv_file} to {json_file}")



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <csv_file1> <csv_file2>")
        sys.exit(1)
    
    csv_file1, csv_file2 = sys.argv[1:3]
    
    convert_csv_to_json(csv_file1, os.path.join(repo_path, "data"))
    
    convert_csv_to_json(csv_file2, os.path.join(repo_path, "query"))
