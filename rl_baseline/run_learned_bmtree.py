import psycopg2
import json
import torch
import os
import sys
import random
import math
from bmtree.bmtree_env import BMTEnv
from int2binary import Int2BinaryTransformer

import configs
args = configs.set_config()
import csv
from utils.query import Query
import numpy as np
import time
from utils.curves import ZorderModule, DesignQuiltsModule, HighQuiltsModule,  Z_Curve_Module




'''Set the state_dim and action_dim, for now'''
bit_length = args.bit_length
data_dim = len(bit_length)
bit_length = [int(i) for i in bit_length]
data_space = [2**(bit_length[i]) - 1 for i in range(len(bit_length))]
bmtree_file = 'learned_bmtree.txt'
binary_transfer = Int2BinaryTransformer(data_space)
smallest_split_card = args.smallest_split_card
max_depth = args.max_depth


def load_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def compute_sfc_values(dataset, env):
    sfc_values = []
    for data in dataset:
        sfc_value = env.tree.output(data)
        sfc_values.append((data, sfc_value)) 
    return sfc_values

def sort_by_sfc(sfc_values):
    sorted_sfc_values = sorted(sfc_values, key=lambda x: x[1])
    return sorted_sfc_values

def save_to_csv(sorted_sfc_values_with_data, output_file_path):
    with open(output_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for data, sfc_value in sorted_sfc_values_with_data:
            writer.writerow(list(data) + [sfc_value])

def main():
    data_path = 'data/{}.json'.format(args.data)
    dataset = load_data(data_path)
    env = BMTEnv(list(dataset), None, bit_length, bmtree_file, binary_transfer, smallest_split_card, max_depth)

    sfc_values_with_data = compute_sfc_values(dataset, env)
    sorted_sfc_values_with_data = sort_by_sfc(sfc_values_with_data)

    output_file_path = 'sorted_data_with_sfc.csv'
    save_to_csv(sorted_sfc_values_with_data, output_file_path)

    print("Sorted data and SFC values saved to:", output_file_path)

if __name__ == '__main__':
    main()