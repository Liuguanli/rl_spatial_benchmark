import osmium
import sys
import csv
import random
import pandas as pd


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

def sample_data(input_file, output_file, num_samples=1000):

    df = pd.read_csv(input_file)
    
    num_samples = min(num_samples, len(df))
    
    sample_df = df.sample(n=num_samples)
    
    sample_df.to_csv(output_file + "_" +  str(num_samples) + ".csv", index=False)

def main(osm_pbf_file, output_file, sample_output_file):
    handler = NodeHandler(output_file)
    handler.apply_file(osm_pbf_file)
    sample_data_reservoir(output_file, sample_output_file)

if __name__ == '__main__':

    sample_data('data/real/dataset/india.csv', 'data/real/dataset/india', 100000000)
    sample_data('data/real/dataset/australia.csv', 'data/real/dataset/australia', 100000000)
    sample_data('data/real/dataset/us.csv', 'data/real/dataset/us', 100000000)
    sample_data('data/real/dataset/india.csv', 'data/real/dataset/india', 10000000)
    sample_data('data/real/dataset/australia.csv', 'data/real/dataset/australia', 10000000)
    sample_data('data/real/dataset/us.csv', 'data/real/dataset/us', 10000000)
