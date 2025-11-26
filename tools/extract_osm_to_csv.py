import osmium
import sys
import os
import csv
import random
import pandas as pd
import numpy as np

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)
from constants import *

np.random.seed(SEED)
random.seed(SEED)


class NodeHandler(osmium.SimpleHandler):
    def __init__(self, file):
        osmium.SimpleHandler.__init__(self)
        self.csv_file = open(file, 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.csv_file)
        # self.writer.writerow(['node_id', 'latitude', 'longitude'])  
    def node(self, n):
        # self.writer.writerow([n.id, n.location.lat, n.location.lon])
        self.writer.writerow([n.location.lat, n.location.lon])

    def __del__(self):
        self.csv_file.close()


def sample_data_reservoir(full_file, sample_file, num_samples=10000):
    with open(full_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        reservoir = []
        for i, row in enumerate(reader):
            if i < num_samples:
                reservoir.append(row)
            else:
                m = random.randint(0, i)
                if m < num_samples:
                    reservoir[m] = row

    with open(sample_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(reservoir)

def sample_data(input_file, output_file, num_samples=[1000]):

    df = pd.read_csv(input_file)
    
    for num_sample in num_samples:
        num_sample = min(num_sample, len(df))
        
        sample_df = df.sample(n=num_sample)
        
        sample_df.to_csv(output_file + "_" +  str(num_sample) + ".csv", index=False, header=False)

def main(osm_pbf_file, output_file, sample_output_file):
    handler = NodeHandler(output_file)
    handler.apply_file(osm_pbf_file)
    sample_data_reservoir(output_file, sample_output_file)

if __name__ == '__main__':

    # data_sizes1 = [100000, 1000000, 20000000, 40000000, 60000000, 80000000]
    data_sizes1 = [10000]
    # data_sizes1 = [1000000, 5000000, 10000000, 50000000]

    # sample_data('data/real/dataset/india_100000000.csv', 'data/real/dataset/india', data_sizes1)
    # sample_data('data/real/dataset/us_10000000.csv', 'data/real/dataset/us', data_sizes1)
    # sample_data('data/real/dataset/australia_100000000.csv', 'data/real/dataset/australia', data_sizes1)
    sample_data('data/real/dataset/tiger_blocks_8180866.csv', 'data/real/dataset/tiger_blocks', data_sizes1)
    sample_data('data/real/dataset/tiger_linearwater_5668549.csv', 'data/real/dataset/tiger_linearwater', data_sizes1)
    sample_data('data/real/dataset/tiger_roads_17813006.csv', 'data/real/dataset/tiger_roads', data_sizes1)

    # sample_data('data/real/dataset/india_100000000.csv', 'data/real/dataset/india', 50000000)
    # sample_data('data/real/dataset/us_100000000.csv', 'data/real/dataset/us', 50000000)
    # sample_data('data/real/dataset/india_100000000.csv', 'data/real/dataset/india', 5000000)
    # sample_data('data/real/dataset/us_100000000.csv', 'data/real/dataset/us', 5000000)
