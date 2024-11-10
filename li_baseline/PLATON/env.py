import math
import numpy as np
import random
import time
import random

def getMBR(data):
    
    # minx = data['minx'].min()
    # maxx = data['maxx'].max()
    # miny = data['miny'].min()
    # maxy = data['maxy'].max()
    # minx = 1
    # maxx = 0
    # miny = 1
    # maxy = 0
    # for i in range(len(data)):
    #     if data[i][0] < minx: 
    #         minx = data[i][0]
    #     if data[i][1] > maxx: 
    #         maxx = data[i][1]
    #     if data[i][2] < miny: 
    #         miny = data[i][2]
    #     if data[i][3] > maxy: 
    #         maxy = data[i][3]
    return (data[:, 0].min(), data[:, 1].max(), data[:, 2].min(), data[:, 3].max())

def getMBRList(data, childSize):
    # print("length of data: {}".format(len(data)))
    # print("childSize: {}".format(childSize))
    result_list_1 = []
    result_list_2 = []
    minx = 1
    maxx = 0
    miny = 1
    maxy = 0
    for i in range(math.ceil(len(data) / childSize) - 1):
        startIdx = i*childSize
        endIdx = min(len(data), (i+1)*childSize)
        currentMinx = data[startIdx:endIdx, 0].min()
        if currentMinx < minx: 
            minx = currentMinx
        currentMaxx = data[startIdx:endIdx, 1].max()
        if currentMaxx > maxx: 
            maxx = currentMaxx
        currentMiny = data[startIdx:endIdx, 2].min()
        if currentMiny < miny: 
            miny = currentMiny
        currentMaxy = data[startIdx:endIdx, 3].max()
        if currentMaxy > maxy: 
            maxy = currentMaxy
        result_list_1.append((minx, maxx, miny, maxy))
    minx = 1
    maxx = 0
    miny = 1
    maxy = 0
    for i in range(math.ceil(len(data) / childSize)-1, 0, -1):
        startIdx = i*childSize
        endIdx = min(len(data), (i+1)*childSize)
        currentMinx = data[startIdx:endIdx, 0].min()
        if currentMinx < minx: 
            minx = currentMinx
        currentMaxx = data[startIdx:endIdx, 1].max()
        if currentMaxx > maxx: 
            maxx = currentMaxx
        currentMiny = data[startIdx:endIdx, 2].min()
        if currentMiny < miny: 
            miny = currentMiny
        currentMaxy = data[startIdx:endIdx, 3].max()
        if currentMaxy > maxy: 
            maxy = currentMaxy
        result_list_2.append((minx, maxx, miny, maxy))
    return np.array(result_list_1), np.array(result_list_2[::-1])

def getMBRListVector(data, childSize):
    # print("length of data: {}".format(len(data)))
    # print("childSize: {}".format(childSize))
    minxListFull = np.minimum.reduceat(data[:, 0], np.r_[:data.shape[0]:childSize])
    minyListFull = np.minimum.reduceat(data[:, 2], np.r_[:data.shape[0]:childSize])
    maxxListFull = np.maximum.reduceat(data[:, 1], np.r_[:data.shape[0]:childSize])
    maxyListFull = np.maximum.reduceat(data[:, 3], np.r_[:data.shape[0]:childSize])

    mbrNumber = math.ceil(len(data) / childSize)-1
    minxList = minxListFull[:mbrNumber]
    minyList = minyListFull[:mbrNumber]
    maxxList = maxxListFull[:mbrNumber]
    maxyList = maxyListFull[:mbrNumber]
    minxCumList = np.minimum.accumulate(minxList)
    minyCumList = np.minimum.accumulate(minyList)
    maxxCumList = np.maximum.accumulate(maxxList)
    maxyCumList = np.maximum.accumulate(maxyList)
    result1 = np.stack([minxCumList, maxxCumList, minyCumList, maxyCumList]).transpose()


    minxListRev = minxListFull[::-1][:mbrNumber]
    minyListRev = minyListFull[::-1][:mbrNumber]
    maxxListRev = maxxListFull[::-1][:mbrNumber]
    maxyListRev = maxyListFull[::-1][:mbrNumber]
    minxCumList = np.minimum.accumulate(minxListRev)
    minyCumList = np.minimum.accumulate(minyListRev)
    maxxCumList = np.maximum.accumulate(maxxListRev)
    maxyCumList = np.maximum.accumulate(maxyListRev)
    result2 = np.stack([minxCumList, maxxCumList, minyCumList, maxyCumList]).transpose()
    return result1, result2[::-1]
    
def getOverlap(MBR1, MBR2):
    return (min(MBR1[1], MBR2[1]) - max(MBR1[0], MBR2[0])) * (min(MBR1[3], MBR2[3]) - max(MBR1[2], MBR2[2]))

def getArea(MBR):
    return (MBR[1] - MBR[0]) * (MBR[3] - MBR[2])


def hasOverlap(MBR1, MBR2):
    if MBR1[1] < MBR2[0] or MBR1[3] < MBR2[2] or MBR1[0] > MBR2[1] or MBR1[2] > MBR2[3]:
        return False
    else:
        return True

def getOverlapQueryNumber(queries, currentMBR, childMBR):

    intersectCurrent = np.logical_not((queries[:, 1] < currentMBR[0]) | (queries[:, 3] < currentMBR[2]) | (queries[:, 0] > currentMBR[1]) | (queries[:, 2] > currentMBR[3]))
    noIntersectChild = (queries[:, 1] < childMBR[0]) | (queries[:, 3] < childMBR[2]) | (queries[:, 0] > childMBR[1]) | (queries[:, 2] > childMBR[3])
    # print(queries[:, 1] < currentMBR[0])
    # print(queries[:, 3] < currentMBR[2])
    # print(queries[:, 0] > currentMBR[1])
    # print(queries[:, 2] > currentMBR[3])
    # print(intersectCurrent)
    # print(noIntersectChild)
    return np.count_nonzero(intersectCurrent & noIntersectChild), np.logical_not(noIntersectChild)
    # return cp.count_nonzero(intersectCurrent & noIntersectChild)

def getOverlapQueryNumberBroadcast(queries, currentMBR, childMBR):

    intersectCurrent = np.logical_not((queries[:, 1] < currentMBR[0]) | (queries[:, 3] < currentMBR[2]) | (queries[:, 0] > currentMBR[1]) | (queries[:, 2] > currentMBR[3]))
    noIntersectChild = (queries[:, 1, None] < childMBR[None, 0, :]) | (queries[:, 3, None] < childMBR[None, 2, :]) | (queries[:, 0, None] > childMBR[None, 1, :]) | (queries[:, 2, None] > childMBR[None, 3, :])
    # intersectCurrent = cp.logical_not((queries[:, 1] < currentMBR[0]) | (queries[:, 3] < currentMBR[2]) | (queries[:, 0] > currentMBR[1]) | (queries[:, 2] > currentMBR[3]))
    # noIntersectChild = (queries[:, 1] < childMBR[0]) | (queries[:, 3] < childMBR[2]) | (queries[:, 0] > childMBR[1]) | (queries[:, 2] > childMBR[3])
    # print(queries[:, 1] < currentMBR[0])
    # print(queries[:, 3] < currentMBR[2])
    # print(queries[:, 0] > currentMBR[1])
    # print(queries[:, 2] > currentMBR[3])
    # print(intersectCurrent)
    # print(noIntersectChild)
    return np.count_nonzero(np.transpose(noIntersectChild) & intersectCurrent, axis=1)
    # return cp.count_nonzero(intersectCurrent & noIntersectChild)

def getOverlapMask(queries, currentMBR):
    return np.logical_not((queries[:, 1] < currentMBR[0]) | (queries[:, 3] < currentMBR[2]) | (queries[:, 0] > currentMBR[1]) | (queries[:, 2] > currentMBR[3]))

class RtreeEnv:

    def __init__(self, data, initialMBR, branch, level, sampleQueryList, lowx=0, highx=1, lowy=0, highy=1, gridSize=32, initialGridMap=None, posRange=None, sampleRate=1):
        self.branch = branch
        self.level = level
        self.childSize = branch ** (level-1)
        if level != 1:
            self.childPageSize = (branch ** (level-1) - 1) // (branch - 1)
        else: 
            self.childPageSize = 0
        self.sampleQueryList = sampleQueryList
        self.lowx = lowx
        self.highx = highx
        self.lowy = lowy
        self.highy = highy
        self.gridSize = gridSize
        self.nChilds = math.ceil(len(data) / self.childSize)
        # if initialGridMap is not None:
        #     gridMap = initialGridMap
        # else:
        #     gridMap = self.getGridMap(data)
        gridMap = initialGridMap
        if not posRange:
            posRange = (1, self.nChilds - 1)
        self.sampleRate = sampleRate
        if self.sampleRate < 1:
            data_sample = random.sample(range(len(data)), int(len(data)*self.sampleRate))
            sampledData = data[data_sample]
        else:
            sampledData = data
        initialSampledMBR = getMBR(sampledData)
        self.partitionList = [(sampledData, initialSampledMBR, gridMap, posRange, sampleQueryList, data)]
        self.nextPartitionIdx = 0
        # print("childSize: {}".format(self.childSize))
        # print("childPageSize: {}".format(self.childPageSize))


    def getPartition(self):
        # print("length of partitionList: {}".format(len(self.partitionList)))
        # for p in self.partitionList:
        #     print(len(p[0]), end = ' ')
        # print()
        if self.nextPartitionIdx == len(self.partitionList):
                return -1, None
        while len(self.partitionList[self.nextPartitionIdx][0]) <= self.childSize*self.sampleRate:
            self.nextPartitionIdx += 1
            if self.nextPartitionIdx == len(self.partitionList):
                return -1, None
        return self.nextPartitionIdx, self.partitionList[self.nextPartitionIdx]

            
        
        
    def getReward(self, idx, dim, position):
        currentData, currentMBR, _, posRange = self.partitionList[idx]
        # currentData.sort(key=lambda x: x[dim])
        # currentData = currentData[currentData[:, dim].argsort()]
        currentData = currentData[np.argpartition(currentData[:, dim], self.childSize*(position - posRange[0] + 1))*self.sampleRate]
        data1 = currentData[:self.childSize*(position - posRange[0] + 1)*self.sampleRate]
        data2 = currentData[self.childSize*(position - posRange[0] + 1)*self.sampleRate:]
        MBR1 = getMBR(data1)
        MBR2 = getMBR(data2)
        
        reward = 0
        for query in self.sampleQueryList:
            if hasOverlap(currentMBR, query):
                if not hasOverlap(MBR1, query):
                    reward += (math.ceil(len(data1) / (self.childSize*self.sampleRate))) * self.childPageSize
                if not hasOverlap(MBR2, query):
                    reward += (math.ceil(len(data2) / (self.childSize*self.sampleRate))) * self.childPageSize
        
        return reward

    def getGreedyAction(self, idx):
        # sort_time = 0
        # mbr_time = 0
        # reward_time = 0
        currentData, currentMBR, _, posRange, sampleQueryList, _ = self.partitionList[idx]
        bestReward = -1
        bestDim = 0
        bestPos = 1
        # for dim in range(4):
        for dim in [0, 2]:
            # start = time.time()
            # currentData.sort(key=lambda x: x[dim])
            # currentData = currentData[currentData[:, dim].argsort()]
            currentData = currentData[np.argpartition(currentData[:, dim], [int(self.childSize*self.sampleRate)*(i - posRange[0] + 1) for i in range(posRange[0], posRange[1]+1)])]
            # sort_time += (time.time() - start)
            # start = time.time()
            # MBRList = getMBRList(currentData, int(self.childSize*self.sampleRate))
            MBRList = getMBRListVector(currentData, int(self.childSize*self.sampleRate))
            # if not ((MBRList[0] == MBRList2[0]).all() and (MBRList[1] == MBRList2[1]).all()):
            #     print(len(currentData))
            #     print(MBRList)
            #     print(MBRList2)
            #     exit()
            # mbr_time += (time.time() - start)
            # print(len(MBRList[0]))
            # print(len(MBRList[1]))
            # print(self.partitionList[idx][3][0])
            # print(self.partitionList[idx][3][1]+1)

            # start = time.time()
            reward = getOverlapQueryNumberBroadcast(self.sampleQueryList, currentMBR, np.transpose(MBRList[0])) * np.arange(1, posRange[1] - posRange[0] + 2) * self.childPageSize + \
                 getOverlapQueryNumberBroadcast(self.sampleQueryList, currentMBR, np.transpose(MBRList[1])) * np.arange(posRange[1] - posRange[0] + 1, 0, -1) * self.childPageSize
            
            if reward.max() > bestReward:
                bestReward = reward.max()
                bestDim = dim
                bestPos = np.argmax(reward) + posRange[0]
            # reward_time += (time.time() - start)

            # for pos in range(self.partitionList[idx][3][0], self.partitionList[idx][3][1]+1):

            # # maxpos = math.ceil(len(self.partitionList[idx][0]) / self.childSize) - 1
            # # for pos in range(1, maxpos + 1):
            # #     data1 = currentData[:self.childSize*pos]
            # #     data2 = currentData[self.childSize*pos:]

            #     # start = time.time()
            #     # MBR1 = getMBR(data1)
            #     # MBR2 = getMBR(data2)
            #     # print(time.time() - start)
            #     # mbr_time += (time.time() - start)

            #     # print(posRange[0])
            #     # print(posRange[1])
            #     # print(pos)
            #     # print(len(MBRList[0]))

            #     MBR1 = MBRList[0][pos - posRange[0]]
            #     MBR2 = MBRList[1][pos - posRange[0]]
        
            #     start = time.time()
            #     # print(dim)
            #     # print(pos)
            #     # print(sampleQueryList.shape)
            #     reward = getOverlapQueryNumber(sampleQueryList, currentMBR, MBR1)[0] *(math.ceil(pos - posRange[0] + 1)) * self.childPageSize + \
            #     getOverlapQueryNumber(sampleQueryList, currentMBR, MBR2)[0] *(math.ceil(posRange[1] - pos + 1)) * self.childPageSize
            #     # reward = 0
            #     # for query in self.sampleQueryList:
            #     #     if hasOverlap(currentMBR, query):
            #     #         if not hasOverlap(MBR1, query):
            #     #             reward += (math.ceil(len(data1) / self.childSize)) * self.childPageSize
            #     #         if not hasOverlap(MBR2, query):
            #     #             reward += (math.ceil(len(data2) / self.childSize)) * self.childPageSize

            #     reward_time += (time.time() - start)

            #     # if reward != vectorReward:
            #     #     print("dim: {}, pos: {}, reward: {}, vectorReward: {}".format(dim, pos, reward, vectorReward))
            #     #     print(self.sampleQueryList)
            #     #     print(currentMBR)
            #     #     print(MBR1)
            #     #     print(MBR2)
            #     # print("dim: {}, pos: {}, reward: {}".format(dim, pos, reward))
            #     # print("MBR1: {}, MBR2: {}, currentMBR: {}".format(MBR1, MBR2, currentMBR))
            #     if reward > bestReward:
            #         bestReward = reward
            #         bestDim = dim
            #         bestPos = pos

        # print("time to sort data: {}".format(sort_time))
        # print("time to getmbr: {}".format(mbr_time))
        # print("time to calculate reward: {}".format(reward_time))
        # if bestPos < self.partitionList[idx][3][0]:
        #     print("invalid position returned:")
        #     print(self.partitionList[idx][3][0])
        #     print(self.partitionList[idx][3][1])
        #     print(bestPos)
        return bestDim, bestPos, bestReward

    def getRandomAction(self, idx):
        currentData, currentMBR, _, posRange, numIntersect, _ = self.partitionList[idx]
        dim_idx = random.randrange(0, 2)
        dim = [0, 2][dim_idx]
        pos = random.randrange(self.partitionList[idx][3][0], self.partitionList[idx][3][1]+1)
        return dim, pos, 0

    
    def getGreedyActionByDim(self, idx, dim):
        currentData, currentMBR, _, posRange = self.partitionList[idx]
        bestReward = -1
        bestPos = 1
        # currentData.sort(key=lambda x: x[dim])
        # currentData = currentData[currentData[:, dim].argsort()]
        currentData = currentData[np.argpartition(currentData[:, dim], [self.childSize*(i - posRange[0] + 1) for i in range(posRange[0], posRange[1]+1)])]
        for pos in range(self.partitionList[idx][3][0], self.partitionList[idx][3][1]+1):
            data1 = currentData[:self.childSize*(pos - posRange[0] + 1)*self.sampleRate]
            data2 = currentData[self.childSize*(pos - posRange[0] + 1)*self.sampleRate:]
            MBR1 = getMBR(data1)
            MBR2 = getMBR(data2)
    
            reward = 0
            for query in self.sampleQueryList:
                if hasOverlap(currentMBR, query):
                    if not hasOverlap(MBR1, query):
                        reward += (math.ceil(len(data1) / (self.childSize*self.sampleRate))) * self.childPageSize
                    if not hasOverlap(MBR2, query):
                        reward += (math.ceil(len(data2) / (self.childSize*self.sampleRate))) * self.childPageSize
            if reward > bestReward:
                bestReward = reward
                bestPos = pos
        return bestPos, bestReward

    def getGreedyOverlapAction(self, idx):
        currentData, currentMBR, _, posRange = self.partitionList[idx]
        minOverlap = 1
        bestDim = 0
        bestPos = 1
        for dim in [0, 2]:
            # currentData.sort(key=lambda x: x[dim])
            # currentData = currentData[currentData[:, dim].argsort()]
            currentData = currentData[np.argpartition(currentData[:, dim], [self.childSize*(i - posRange[0] + 1)*self.sampleRate for i in range(posRange[0], posRange[1]+1)])]
            for pos in range(self.partitionList[idx][3][0], self.partitionList[idx][3][1]+1):
                data1 = currentData[:self.childSize*(pos - posRange[0] + 1)*self.sampleRate]
                data2 = currentData[self.childSize*(pos - posRange[0] + 1)*self.sampleRate:]
                MBR1 = getMBR(data1)
                MBR2 = getMBR(data2)
                
        
                overlap = getOverlap(MBR1, MBR2)
                
                if overlap < minOverlap:
                    minOverlap = overlap
                    bestDim = dim
                    bestPos = pos
        return bestDim, bestPos, minOverlap


    def getGreedyAreaAction(self, idx):
        currentData, currentMBR, _, posRange, sampleQueryList, _ = self.partitionList[idx]
        minArea = 1e10
        bestDim = 0
        bestPos = 1
        for dim in [0, 2]:
            currentData = currentData[currentData[:, dim].argsort()]
            MBRList = getMBRListVector(currentData, int(self.childSize*self.sampleRate))

            for pos in range(self.partitionList[idx][3][0], self.partitionList[idx][3][1]+1):

                MBR1 = MBRList[0][pos - posRange[0]]
                MBR2 = MBRList[1][pos - posRange[0]]
        
                area = getArea(MBR1) + getArea(MBR2)
                
                if area < minArea:
                    minArea = area
                    bestDim = dim
                    bestPos = pos

        if bestPos < self.partitionList[idx][3][0]:
            print("invalid position returned:")
            print(self.partitionList[idx][3][0])
            print(self.partitionList[idx][3][1])
            print(bestPos)
        return bestDim, bestPos, minArea


    def getGridMap(self, data):
        gridMap = np.zeros((self.gridSize, self.gridSize))
        xcell = (self.highx - self.lowx) / self.gridSize
        ycell = (self.highy - self.lowy) / self.gridSize
        for i in range(len(data)):
            lowxidx = int((data.iloc[i]['minx'] - self.lowx) / xcell)
            highxidx = int((data.iloc[i]['maxx'] - self.lowx) / xcell)
            lowyidx = int((data.iloc[i]['miny'] - self.lowy) / ycell)
            highyidx = int((data.iloc[i]['maxy'] - self.lowy) / ycell)
            if highxidx == self.gridSize:
                highxidx = self.gridSize - 1
            if highyidx == self.gridSize:
                highyidx = self.gridSize - 1
            # print("indices: {}, {}, {}, {}".format(lowxidx, highxidx, lowyidx, highyidx))
            gridMap[lowxidx:highxidx+1, lowyidx:highyidx+1] = gridMap[lowxidx:highxidx+1, lowyidx:highyidx+1] + 1
            # print(self.gridMap)
        return gridMap

    def cutPartition(self, idx, dim, position):
        currentData, currentMBR, _, posRange = self.partitionList[idx]
        # currentData.sort(key=lambda x: x[dim])
        # currentData = currentData[currentData[:, dim].argsort()]
        currentData = currentData[np.argpartition(currentData[:, dim], self.childSize*(position - posRange[0] + 1)*self.sampleRate)]

        data1 = currentData[:self.childSize*(position - posRange[0] + 1)*self.sampleRate]
        data2 = currentData[self.childSize*(position - posRange[0] + 1)*self.sampleRate:]
        # data1 = currentData[:self.childSize*position]
        # data2 = currentData[self.childSize*position:]

        del self.partitionList[idx]
        MBR1 = getMBR(data1)
        MBR2 = getMBR(data2)
        gridMap1 = self.getGridMap(data1)
        gridMap2 = self.getGridMap(data2)
        partition1 = (data1, MBR1, gridMap1, (posRange[0], position - 1))
        partition2 = (data2, MBR2, gridMap2, (position + 1, posRange[1]))
        self.partitionList.insert(idx, partition1)
        self.partitionList.insert(idx + 1, partition2)

        # print(MBR1)
        # print(MBR2)
        
        reward = 0
        for query in self.sampleQueryList:
            if hasOverlap(currentMBR, query):
                if not hasOverlap(MBR1, query):
                    reward += (math.ceil(len(data1) / (self.childSize*self.sampleRate))) * self.childPageSize
                if not hasOverlap(MBR2, query):
                    reward += (math.ceil(len(data2) / (self.childSize*self.sampleRate))) * self.childPageSize
            # print("reward: {}".format(reward))
        
        return reward

    def cutPartitionGreedyByDim(self, idx, dim):
        position, reward = self.getGreedyActionByDim(idx, dim)
        currentData, currentMBR, _, posRange = self.partitionList[idx]
        # currentData.sort(key=lambda x: x[dim])
        # currentData = currentData[currentData[:, dim].argsort()]
        currentData = currentData[np.argpartition(currentData[:, dim], self.childSize*(position - posRange[0] + 1)*self.sampleRate)]
        data1 = currentData[:self.childSize*(position - posRange[0] + 1)*self.sampleRate]
        data2 = currentData[self.childSize*(position - posRange[0] + 1)*self.sampleRate:]
        del self.partitionList[idx]
        MBR1 = getMBR(data1)
        MBR2 = getMBR(data2)
        gridMap1 = self.getGridMap(data1)
        gridMap2 = self.getGridMap(data2)
        partition1 = (data1, MBR1, gridMap1, (posRange[0], position - 1))
        partition2 = (data2, MBR2, gridMap2, (position + 1, posRange[1]))
        self.partitionList.insert(idx, partition1)
        self.partitionList.insert(idx + 1, partition2)
        
        return reward
    

    def cutPartitionGreedy(self, idx, dim, position):
        currentSampledData, currentMBR, _, posRange, sampleQueryList, currentData = self.partitionList[idx]
        
        # partition sampled data
        # currentData = currentData[currentData[:, dim].argsort()]
        if int(self.childSize*(position - posRange[0] + 1)*self.sampleRate) < 0 or int(self.childSize*(position - posRange[0] + 1)*self.sampleRate) > len(currentSampledData):
            print(position)
            print(posRange[0])
            print(posRange[1])
            print(self.childSize)
            print(self.sampleRate)
            print(len(currentSampledData))
        currentSampledData = currentSampledData[np.argpartition(currentSampledData[:, dim], int(self.childSize*(position - posRange[0] + 1)*self.sampleRate))]
        sampledData1 = currentSampledData[:int(self.childSize*(position - posRange[0] + 1)*self.sampleRate)]
        sampledData2 = currentSampledData[int(self.childSize*(position - posRange[0] + 1)*self.sampleRate):]

        # partition actual data
        currentData = currentData[np.argpartition(currentData[:, dim], self.childSize*(position - posRange[0] + 1))]
        data1 = currentData[:self.childSize*(position - posRange[0] + 1)]
        data2 = currentData[self.childSize*(position - posRange[0] + 1):]

        del self.partitionList[idx]
        MBR1 = getMBR(sampledData1)
        MBR2 = getMBR(sampledData2)
        
        # reward = 0
        # for query in self.sampleQueryList:
        #     if hasOverlap(currentMBR, query):
        #         if not hasOverlap(MBR1, query):
        #             reward += (math.ceil(len(data1) / self.childSize)) * self.childPageSize
        #         if not hasOverlap(MBR2, query):
        #             reward += (math.ceil(len(data2) / self.childSize)) * self.childPageSize
        reward1, overlapMask1 = getOverlapQueryNumber(sampleQueryList, currentMBR, MBR1)
        reward2, overlapMask2 = getOverlapQueryNumber(sampleQueryList, currentMBR, MBR2)
        sampleQueryList1 = sampleQueryList[overlapMask1]
        sampleQueryList2 = sampleQueryList[overlapMask2]
        # print(idx)
        # print(dim)
        # print(pos)
        # print(sampleQueryList1.shape)
        # print(sampleQueryList2.shape)
        reward = reward1 * (position - posRange[0] + 1) * self.childPageSize + \
                reward2 * (posRange[1] - position + 1) * self.childPageSize

        partition1 = (sampledData1, MBR1, None, (posRange[0], position - 1), sampleQueryList1, data1)
        partition2 = (sampledData2, MBR2, None, (position + 1, posRange[1]), sampleQueryList2, data2)
        self.partitionList.insert(idx, partition1)
        self.partitionList.insert(idx + 1, partition2)
            
        return reward

    def cutPartitionGreedyTest(self, idx, dim, position, testQueryListSet=[]):
        currentSampledData, currentMBR, _, posRange, sampleQueryList, currentData = self.partitionList[idx]
        # currentData = currentData.sort_values(by=[dim])

        # partition sampled data
        # currentData = currentData[currentData[:, dim].argsort()]
        currentSampledData = currentSampledData[np.argpartition(currentSampledData[:, dim], int(self.childSize*(position - posRange[0] + 1)*self.sampleRate))]
        sampledData1 = currentSampledData[:int(self.childSize*(position - posRange[0] + 1)*self.sampleRate)]
        sampledData2 = currentSampledData[int(self.childSize*(position - posRange[0] + 1)*self.sampleRate):]

        # partition actual data
        currentData = currentData[np.argpartition(currentData[:, dim], self.childSize*(position - posRange[0] + 1))]
        data1 = currentData[:self.childSize*(position - posRange[0] + 1)]
        data2 = currentData[self.childSize*(position - posRange[0] + 1):]

        del self.partitionList[idx]
        MBR1 = getMBR(sampledData1)
        MBR2 = getMBR(sampledData2)
        
        reward1, overlapMask1 = getOverlapQueryNumber(sampleQueryList, currentMBR, MBR1)
        reward2, overlapMask2 = getOverlapQueryNumber(sampleQueryList, currentMBR, MBR2)
        sampleQueryList1 = sampleQueryList[overlapMask1]
        sampleQueryList2 = sampleQueryList[overlapMask2]
        reward = reward1 * (position - posRange[0] + 1)  * self.childPageSize + \
                reward2 * (posRange[1] - position + 1) * self.childPageSize
        # reward = getOverlapQueryNumber(self.sampleQueryList, currentMBR, MBR1)[0] *(math.ceil(len(data1) / self.childSize)) * self.childPageSize + \
        #         getOverlapQueryNumber(self.sampleQueryList, currentMBR, MBR2)[0] *(math.ceil(len(data2) / self.childSize)) * self.childPageSize

        partition1 = (sampledData1, MBR1, None, (posRange[0], position - 1), sampleQueryList1, data1)
        partition2 = (sampledData2, MBR2, None, (position + 1, posRange[1]), sampleQueryList2, data2)
        self.partitionList.insert(idx, partition1)
        self.partitionList.insert(idx + 1, partition2)
            

        # skipped = 0
        # if testQueryList:
        #     for query in testQueryList:
        #         if hasOverlap(currentMBR, query):
        #             if not hasOverlap(MBR1, query):
        #                 skipped += (math.ceil(len(data1) / self.childSize)) * self.childPageSize
        #             if not hasOverlap(MBR2, query):
        #                 skipped += (math.ceil(len(data2) / self.childSize)) * self.childPageSize
        skippedList=[]
        for testQueryList in testQueryListSet:
            skipped = getOverlapQueryNumber(testQueryList, currentMBR, MBR1)[0] * (position - posRange[0] + 1) * self.childPageSize + \
                getOverlapQueryNumber(testQueryList, currentMBR, MBR2)[0] * (posRange[1] - position + 1) * self.childPageSize
            skippedList.append(skipped)
            
        return reward, skippedList


    
    def printPartitions(self):
        for partition in self.partitionList:
            print(len(partition[0]), end=' ')
        print()

            # print(partition[1])

    def getChildEnv(self):
        childEnvList = []
        for partition in self.partitionList:
            # if self.level - 1 == 4:
            #     sampleRate = 0.0001
            # elif self.level - 1 == 3:
            #     sampleRate = 0.01
            # else: 
            #     sampleRate = 1
            sampleRate = 1
            childEnvList.append(RtreeEnv(partition[5], partition[1], self.branch, self.level-1, partition[4], initialGridMap=partition[2], sampleRate=sampleRate))
            # childEnvList.append(RtreeEnv(partition[5], partition[1], self.branch, self.level-1, partition[4], initialGridMap=partition[2], sampleRate=1))
        return childEnvList





    
