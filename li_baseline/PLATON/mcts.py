import pandas as pd
import geopandas as gpd
import geoplot as gplt
from shapely import geometry
import matplotlib.pyplot as plt 
import numpy as np
import matplotlib
from PIL import Image
import copy
import hashlib
from collections import defaultdict
import math
import time

from env import RtreeEnv
from env import getMBR

class MCTS:
    "Monte Carlo tree searcher. First rollout the tree then choose a move."

    def __init__(self, exploration_weight=1):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight

    def choose(self, node):
        "Choose the best successor of node. (Choose a move in the game)"
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            # return self.Q[n] / self.N[n]  # average reward
            return self.Q[n]

        bestChild = max(self.children[node], key=score)
        # print("score of best child: {}".format(self.Q[bestChild] * bestChild.normalizeFactor))
        return bestChild

    def do_rollout(self, node):
        # "Make the tree one layer better. (Train for one iteration.)"
        start = time.time()
        path = self._select(node)
        # print("_select time: {}".format(time.time() - start))
        leaf = path[-1]
        # print(leaf.history)
        self._expand(leaf)
        # print("_expand time: {}".format(time.time() - start))
        reward = self._simulate(leaf)
        # print("_simulate time: {}".format(time.time() - start))
        # print("normalized reward: {}".format(reward))
        # print("normalize factor: {}".format(leaf.normalizeFactor))
        # print("Actual reward: {}".format(reward * node.maxReward))
        self._backpropagate(path, reward)
        # print("_backprop time: {}".format(time.time() - start))


    def _select(self, node):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # print("current node unexplored")
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            # print(unexplored)
            if unexplored:
                # print("explore unexplored child")
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node):
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        self.children[node] = node.find_children()

    def _simulate(self, node):
        "Returns the reward for a random simulation (to completion) of `node`"
        # while True:
        #     # print(node)
        #     if node.is_terminal():
        #         reward = node.reward()
        #         return reward
        #     node = node.find_random_child()
        if node.is_terminal():
            reward = node.reward() / node.normalizeFactor
        else:
            reward = node.simulate_reward() / node.normalizeFactor
        return reward
        # return node.simulate_reward_total()

    def _backpropagate(self, path, reward):
        "Send the reward back up to the ancestors of the leaf"
        for node in reversed(path):
            self.N[node] += 1
            # self.Q[node] += reward
            if self.Q[node] < reward:
                self.Q[node] = reward

    def _uct_select(self, node):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        # assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            # return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
            #     log_N_vertex / self.N[n]
            # )
            return self.Q[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )
            

        return max(self.children[node], key=uct)



class Node():
    """
    A representation of a single state.
    MCTS works by constructing a tree of these Nodes.
    Could be e.g. a chess or checkers board state.
    """
    def __init__(self, env, cumulativeReward, history, maxReward, parent, step, normalizeFactor):
        self.env = env
        self.cumulativeReward = cumulativeReward
        self.history = history
        self.maxReward = maxReward
        self.parent = parent
        self.step = step
        self.normalizeFactor = normalizeFactor

    def find_children(self):
        "All possible successors of this board state"
        if self.env is None:
            self.buildEnv() 
        childSet = set()
        if self.is_terminal():
            return childSet
        idx, partition = self.env.getPartition()
        # for dim in range(4):
        for dim in [0, 2]:
            for pos in range(self.env.partitionList[idx][3][0], self.env.partitionList[idx][3][1]+1):
                # state = copy.deepcopy(self.env)
                history = copy.copy(self.history)
                history.append((dim, pos))
                # idx, partition = state.getPartition()
                # reward = state.cutPartition(idx, dim, pos)
                newNode = Node(None, -1, history, self.maxReward, self, self.step - 1, self.normalizeFactor)
                childSet.add(newNode)
            # pos, reward = self.env.getGreedyActionByDim(idx, dim)
            # history = copy.copy(self.history)
            # history.append((dim, pos))
            # newNode = Node(None, -1, history, self.maxReward, self)
            # childSet.add(newNode)
            
        return childSet

    def find_random_child(self):
        "Random successor of this board state (for more efficient simulation)"
        if self.env is None:
            self.buildEnv() 
        idx, partition = self.env.getPartition()
        state = copy.deepcopy(self.env)
        action, position, _ = state.getGreedyAction(idx)
        reward = state.cutPartitionGreedy(idx, action, position)

        history = copy.copy(self.history)
        history.append((action, position))
        return Node(state, self.cumulativeReward + reward, history, self.maxReward, self, self.step-1)

    def is_terminal(self):
        "Returns True if the node has no children"
        return len(self.env.partitionList) == self.env.nChilds

    def reward(self):
        "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
        if self.env is None:
            self.buildEnv() 

        return self.cumulativeReward
        
        queue = []
        if self.env.level >=3:
            childEnvList = self.env.getChildEnv()
            for childEnv in childEnvList:
                queue.append(childEnv)
        totalRewardGreedy = self.cumulativeReward
        while queue:
            env = queue.pop(0)
            for i in range(env.branch - 1):
                # print(len(env.partitionList))
                # for p in env.partitionList:
                #     print(len(p[0]), end = ' ')
                # print()
                idx, partition = env.getPartition()
                action, position, bestReward = getGreedyAction(env, idx)
                # action, position, bestReward = env.getRandomAction(idx)
                reward = env.cutPartitionGreedy(idx, action, position)
                # env.printPartitions()
                # print("reward: {}".format(reward))
                # print("two step best reward: {}".format(bestReward))
                totalRewardGreedy += reward
            if env.level >=3 :
                childEnvList = env.getChildEnv()
                for childEnv in childEnvList:
                    queue.append(childEnv)

        # return totalRewardGreedy / self.maxReward
        return totalRewardGreedy

    def simulate_reward(self):
        "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
        # get_greedy_time = 0
        # cut_time = 0
        # start = time.time()
        if self.env is None:
            self.buildEnv() 
        # print("build env time: {}".format(time.time() - start))

        totalRewardGreedy = self.cumulativeReward

        # start = time.time()
        env = copy.deepcopy(self.env)
        # print("copy env time: {}".format(time.time() - start))
        # n_steps = env.branch - len(env.partitionList)
        step_count = 0
        while True:
            # print(len(env.partitionList))
            # for p in env.partitionList:
            #     print(len(p[0]), end = ' ')
            # print()
            idx, partition = env.getPartition()
            # print(idx, partition)
            if idx == -1 or step_count == self.step: 
                break

            # start = time.time()
            sampleQueryList = env.partitionList[idx][4]
            if len(sampleQueryList) == 0:
                action, position, _ = env.getRandomAction(idx)
            else:
                action, position, bestReward = env.getGreedyAction(idx)
            # get_greedy_time += (time.time() - start)
            # action, position, bestReward = env.getRandomAction(idx)

            # print("getGreedyAction time: {}".format(time.time() - start))
            # action, position, bestReward = env.getGreedyOverlapAction(idx)
            # start = time.time()
            reward = env.cutPartitionGreedy(idx, action, position)
            # cut_time += (time.time() - start)
            # env.printPartitions()
            # print("reward: {}".format(reward))
            # print("two step best reward: {}".format(bestReward))
            totalRewardGreedy += reward
            step_count += 1
        
        # print("time to get greedy action: {}".format(get_greedy_time))
        # print("time to cut partition: {}".format(cut_time))

        # return totalRewardGreedy / self.maxReward
        return totalRewardGreedy

    def simulate_reward_total(self):
        "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
        if self.env is None:
            self.buildEnv() 
        
        queue = []
        if len(self.env.partitionList) == self.env.branch and self.env.level >=3:
            childEnvList = self.env.getChildEnv()
            for childEnv in childEnvList:
                queue.append(childEnv)
        elif len(self.env.partitionList) != self.env.branch:
            queue.append(copy.deepcopy(self.env))
        totalRewardGreedy = self.cumulativeReward
        while queue:
            env = queue.pop(0)
            nstep = env.branch - len(env.partitionList)
            while True:

                # print(len(env.partitionList))
                # for p in env.partitionList:
                #     print(len(p[0]), end = ' ')
                # print()

                idx, partition = env.getPartition()
                # print(idx, partition)
                if idx == -1: 
                    break

                idx, partition = env.getPartition()
                # action, position, bestReward = env.getRandomAction(idx)
                action, position, bestReward = env.getGreedyAction(idx)
                # action, position, bestReward = env.getGreedyOverlapAction(idx)
                reward = env.cutPartitionGreedy(idx, action, position)
                # env.printPartitions()
                # print("reward: {}".format(reward))
                # print("two step best reward: {}".format(bestReward))
                totalRewardGreedy += reward
            if env.level >=3 :
                childEnvList = env.getChildEnv()
                for childEnv in childEnvList:
                    queue.append(childEnv)

        # return totalRewardGreedy / self.maxReward
        return totalRewardGreedy

    def buildEnv(self):
        self.env = copy.deepcopy(self.parent.env)
        idx, partition = self.env.getPartition()
        action, pos = self.history[-1]
        reward = self.env.cutPartitionGreedy(idx, action, pos)
        self.cumulativeReward = self.parent.cumulativeReward + reward


            
    def __hash__(self):
        "Nodes must be hashable"
        def historyToString(history):
            "Upper confidence bound for trees"
            historyStr = ""
            for (dim, pos) in history:
                historyStr += str(dim)
                historyStr += ','
                historyStr += str(pos)
            return historyStr
        return int(hashlib.sha256(historyToString(self.history).encode('utf-8')).hexdigest(), 16)

    def __eq__(node1, node2):
        "Nodes must be comparable"
        return node1.history == node2.history