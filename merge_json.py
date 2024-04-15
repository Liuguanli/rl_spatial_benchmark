import os
import json
from constants import *

def merge_json_files():
    all_data = {'experiments': []}  # Initialize with 'experiments' key
    directory = CONFIG_DIR
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                print(file_path)
                # with open(file_path, 'r') as f:
                #     data = json.load(f)
                #     # Assuming each file contains an "experiments" list
                #     all_data['experiments'].extend(data['experiments'])

    # output_file = "merged.json"
    # with open(output_file, 'w') as f:
    #     json.dump(all_data, f, indent=2)

merge_json_files()