import pandas as pd
import geopandas as gpd
# import geoplot as gplt
from shapely import geometry
import matplotlib.pyplot as plt 
import matplotlib
from PIL import Image
import copy
import time
import numpy as np
# import cupy as cp
import math
import csv
import argparse
import os

from env import RtreeEnv
from env import getMBR
from env import getOverlapMask

from mcts import MCTS
from mcts import Node

parser = argparse.ArgumentParser(description="R-tree Monte Carlo Tree Search Optimization")
parser.add_argument('--input_data_file', type=str, required=True, help='Path to the input GeoJSON Data file for queries')
parser.add_argument('--input_query_file', type=str, required=True, help='Path to the input GeoJSON Query file for queries')
parser.add_argument('--output_file', type=str, required=True, help='Path to the output CSV file for action list')

file_dir = "./benchmark/libspatialindex"

args = parser.parse_args()

# set data size

n = 100000000

# set number of queries
n_queries = 1000

# set number of test queries
n_queries_test = 1000

# set tree size
branch = 100
nlevel = 4

roll_out_count = 10

# find the bounds of your geodataframe
x_min, y_min, x_max, y_max = 0, 0, 1, 1
extent = (0, 0, 1, 1)

# data_type = "rect_0_0.001"
# input_data_file = "./data/data_{}_{}.npy".format(data_type, n)
input_data_file = os.path.join(file_dir, args.input_data_file + ".npy")
dataList = np.load(input_data_file)

# add z order value to column4
# zlevel = math.ceil(math.log2(n))
# dataList = dataList[dataList[:, 0].argsort()]
# dataList = np.hstack([dataList, np.arange(n)[:, np.newaxis]])
# dataList = dataList[dataList[:, 2].argsort()]
# dataList = np.hstack([dataList, np.arange(n)[:, np.newaxis]])
# dataList = np.hstack([dataList, np.array([get_z_key(zlevel, dataList[i][4].astype(int), dataList[i][5].astype(int)) for i in range(len(dataList))])[:, np.newaxis]])
# dataList = np.delete(dataList, 4, 1)
# dataList = np.delete(dataList, 4, 1)

# query_type = "aspect_0.01_0.001"

# input_query_file = './data/query_{}_train_{}.geojson'.format(query_type, n_queries)
input_query_file = os.path.join(file_dir, args.input_query_file + ".geojson")

query_gdf = gpd.read_file(input_query_file)
print(query_gdf.head())

queryList = [(row['minx'], row['maxx'], row['miny'], row['maxy']) for _, row in query_gdf.iterrows()]
queryList = np.array(queryList)
# np.save('./data/query_{}_train_{}.npy'.format(query_type, n_queries), queryList)
queryList = queryList[:n_queries]
# print(queryList)

test_query_list_set = []


initialMBR = getMBR(dataList)

rtreeSize = 0
for i in range(nlevel - 1):
    rtreeSize += (n // (branch ** (i+1)))
rtreeSize += 1
maxReward = rtreeSize * np.count_nonzero(getOverlapMask(queryList, initialMBR))
print("R tree size: {}, maxReward: {}".format(rtreeSize, maxReward))

maxRewardTest = [rtreeSize * np.count_nonzero(getOverlapMask(test_query_list_set[i], initialMBR)) for i in range(len(test_query_list_set))]


actionList = []

print("Starting Monte Carlo Tree Search")
start = time.time()
# mctsTree = MCTS()
treeEnv = RtreeEnv(dataList, initialMBR, branch, nlevel, queryList)
queue = [treeEnv]
totalReward = 0
totalSkipped = [0 for i in range(len(test_query_list_set))]
while queue:
    state_start = time.time()
    # mctsTree = MCTS()
    env = queue.pop(0)
    # state = Node(copy.deepcopy(env), 0, [], maxReward, None, 25)
    nChilds = math.ceil(len(env.partitionList[0][5]) / env.childSize)
    # print("number of cuts for current node: {}".format(nChilds))
    count = 0
    for i in range(nChilds - 1):
        idx, partition = env.getPartition()
        sampleQueryList = env.partitionList[idx][4]
        if len(sampleQueryList) == 0:
            count += 1
            action, position, _ = env.getRandomAction(idx)
        else:
            normalizeFactor = env.childPageSize * (len(env.partitionList[idx][5]) // env.childSize) * len(sampleQueryList)
            mctsTree = MCTS()
            # if env.level == 4:
            #     sampleRate = 0.0001
            # elif env.level == 3:
            #     sampleRate = 0.01
            # else: 
            #     sampleRate = 1
            sampleRate = 1
            state = Node(RtreeEnv(env.partitionList[idx][5], env.partitionList[idx][1], env.branch, env.level, env.sampleQueryList, posRange=env.partitionList[idx][3], sampleRate=sampleRate), 0, [], maxReward, None, 100, normalizeFactor)
            roll_out_start = time.time()
            for _ in range(roll_out_count):
                # print("roll out no {}".format(_))
                mctsTree.do_rollout(state)
            # print("roll out time: {}".format(time.time() - roll_out_start))
            state = mctsTree.choose(state)
            action, position = state.history[-1]
        actionList.append([0 if action==0 else 1, position-env.partitionList[idx][3][0]+1])
        reward, skipped = env.cutPartitionGreedyTest(idx, action, position, test_query_list_set)
        # reward = env.cutPartitionGreedy(idx, action, position)
        # print("action: {}, position: {}".format(action, position))
        # env.printPartitions()
        # print("reward: {}".format(reward))
        totalReward+= reward
        for i in range(len(skipped)):
            totalSkipped[i] += skipped[i]
    childEnvList = env.getChildEnv()
    if env.level >=3:
        for childEnv in childEnvList:
            numIntersectQuery = np.count_nonzero(getOverlapMask(childEnv.sampleQueryList, childEnv.partitionList[0][1]))
            # print(numIntersectQuery)
            # if numIntersectQuery != 0:
            #     queue.append(childEnv)
            queue.append(childEnv)
    # print("Current node reward: {}".format(totalReward))
    # print("state processing time: {}, number of partition skipped: {}".format(time.time() - state_start, count))

print("MCTS training totalReward: {}, totalIO: {}, total number of skipped blocks: {}, total io: {}, time: {}".format(totalReward, maxReward - totalReward, totalSkipped, [maxRewardTest[i]-totalSkipped[i] for i in range(len(totalSkipped))], time.time()-start))
# print("MCTS totalReward: {}, time: {}".format(totalReward, time.time() - start))
# print("number of actions in actionList: {}".format(len(actionList)))

# Ensure that the directory 'cut_list' exists
# output_directory = "./cut_list"
# if not os.path.exists(output_directory):
#     os.makedirs(output_directory)


# Write the actionList to the output file
# output_file = "mcts_{}_{}_{}_{}".format(data_type, n, query_type, n_queries)
output_file = args.output_file

# output_file = os.path.join("./cut_list", output_file)

with open(output_file, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in actionList:
        writer.writerow(row)

print(f"File saved to {output_file}")


# Test transform input data and query, and output

# Test platon in libspatialindex!!!