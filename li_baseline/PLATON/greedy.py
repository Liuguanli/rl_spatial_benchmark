import pandas as pd
import geopandas as gpd
import geoplot as gplt
from shapely import geometry
import matplotlib.pyplot as plt 
import matplotlib
from PIL import Image
import copy
import time
import numpy as np
import torch
import math
import csv

from env import RtreeEnv
from env import getMBR
from env import getOverlapMask

from mcts import MCTS
from mcts import Node

# set data size
n = 1000000

# set number of queries
n_queries = 10000

# set number of test queries
n_queries_test = 10000

# set tree size
branch = 100
nlevel = 3

# find the bounds of your geodataframe
x_min, y_min, x_max, y_max = 0, 0, 1, 1
extent = (0, 0, 1, 1)

data_type = "rect_0_0.001"
dataList = np.load("./data/data_{}_{}.npy".format(data_type, n))

query_type = "aspect_0.01_0.001"
query_gdf = gpd.read_file('./data/query_{}_train_{}.geojson'.format(query_type, n_queries))
print(query_gdf.head())

queryList = [(row['minx'], row['maxx'], row['miny'], row['maxy']) for _, row in query_gdf.iterrows()]
queryList = np.array(queryList)
queryList = queryList[:n_queries]
# print(queryList)
# print(queryList.dtype)
# queryList = torch.from_numpy(queryList)
# queryList.to(device)
# print(queryList.type)

test_query_list_set = []

initialMBR = getMBR(dataList)

rtreeSize = 0
for i in range(nlevel - 1):
    rtreeSize += (n // (branch ** (i+1)))
rtreeSize += 1
maxReward = rtreeSize * np.count_nonzero(getOverlapMask(queryList, initialMBR))
print("R tree size: {}, maxReward: {}".format(rtreeSize, maxReward))

maxRewardTest = [rtreeSize * np.count_nonzero(getOverlapMask(test_query_list_set[i], initialMBR)) for i in range(len(test_query_list_set))]

treeEnv = RtreeEnv(dataList, initialMBR, branch, nlevel, queryList)

actionList = []
start = time.time()
greedyTime = 0
sortTime = 0
mbrTime = 0
rewardTime = 0
# sampleRate = float(10000) / len(dataList) 
sampleRate = 1
# if nlevel == 4:
#     sampleRate = 0.0001
# elif nlevel == 3:
#     sampleRate = 0.01
# else: 
#     sampleRate = 1
treeEnv = RtreeEnv(dataList, initialMBR, branch, nlevel, queryList, sampleRate=sampleRate)
queue = [treeEnv]
totalRewardGreedy1 = 0
totalSkipped = [0 for i in range(len(test_query_list_set))]
while queue:
    env = queue.pop(0)
    nChilds = math.ceil(len(env.partitionList[0][5]) / env.childSize)
    for i in range(nChilds - 1):
        idx, partition = env.getPartition()
        startTime = time.time()
        # action, position, bestReward, sort_time, mbr_time, reward_time = env.getGreedyAction(idx)
        action, position, bestReward = env.getGreedyAction(idx)
        # sortTime += sort_time
        # mbrTime += mbr_time
        # rewardTime += reward_time
        greedyTime += (time.time() - startTime)
        reward, skipped = env.cutPartitionGreedyTest(idx, action, position, test_query_list_set)
        # print("action: {}, position: {}, reward: {}".format(action, position, reward))
        # env.printPartitions()
        totalRewardGreedy1 += reward
        actionList.append([0 if action==0 else 1, position-env.partitionList[idx][3][0]+1])
        for i in range(len(skipped)):
            totalSkipped[i] += skipped[i]
    childEnvList = env.getChildEnv()
    if env.level >=3:
        for childEnv in childEnvList:
            # if childEnv.level >= 2:
            #     print(childEnv.sampleRate)
            queue.append(childEnv)
    if env.level == 4:
        for childEnv in childEnvList:
            print(childEnv.partitionList[0][1])
    # print("current time: {}".format(time.time()-start))
    # print("Current node reward: {}".format(totalRewardGreedy1))

print("Greedy training totalReward: {}, totalIO: {}, total number of skipped blocks: {}, total io: {}, time: {}".format(totalRewardGreedy1, maxReward - totalRewardGreedy1, totalSkipped, [maxRewardTest[i]-totalSkipped[i] for i in range(len(totalSkipped))], time.time()-start))
print("Greedy time: ", greedyTime)
print("Sort time: ", sortTime)
print("mbr time: ", mbrTime)
print("reward time: ", rewardTime)
# with open("./cut_list/mcts_tiger_area_water_{}_data_0.0001_0.001_{}_sample_10000_greedy".format(n, n_queries), 'w') as csvfile:
# with open("./cut_list/mcts_{}_{}_data_{}_{}_greedy".format(data_type, n, query_type, n_queries), 'w') as csvfile:
with open("./cut_list/mcts_{}_{}_{}_{}_greedy".format(data_type, n, query_type, n_queries), 'w') as csvfile:
# with open("./cut_list/mcts_{}_{}_{}_greedy".format(data_type, n, n_queries), 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in actionList:
        writer.writerow(row)
