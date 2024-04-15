import collections
import time
import os
import csv
import random

import numpy as np
import pickle
import copy
from gym.spaces import Tuple, Box, Discrete, Dict

from ray.rllib.env import MultiAgentEnv
from ray.rllib.evaluation.rollout_worker import get_global_worker

from qdtree import QDTree, Node


class QdtreeEnv(MultiAgentEnv):

    def __init__(self, config):
        super().__init__()
        self.leaf_threshold = config.get("leaf_threshold", 100)
        self.dataset_path = config["dataset_path"]
        self.workload_path = config["workload_path"]
        self.dimension = config.get("dimension", 2)
        self.sampling_ratio = config.get("sampling_ratio", 0.01)
        self.action_sampling_size = config.get("action_sampling_size", 200)

        self.points = self.load_data(self.dataset_path, self.sampling_ratio)
        self.query_rectangles = self.load_workloads(self.workload_path)
        self.actions = self.gen_actions(True, self.action_sampling_size)
        self.flatten_actions = []
        for i in range(self.dimension):
            self.flatten_actions.extend(self.actions[i])

        np.array(self.actions).flatten()
        self.domain = self.cal_domain()

        self.node_queue = []

        self._agent_ids = {0}
        
        # Define action and observation spaces
        self.action_space = Discrete(self.action_sampling_size)  # Assume 2 actions per dimension (split at median, quartiles, etc.)
        # self.observation_space = Box(low=0, high=1, shape=(32 * 2 * self.dimension + self.dimension + self.action_sampling_size,), dtype=np.float32)
        self.observation_space = Box(low=0, high=1, shape=(32 * 2 * self.dimension,), dtype=np.float32)

        self.reset()


    def load_data(self, dataset_path, sampling_ratio=0.01):

        # Open the file in read mode
        with open(dataset_path, 'r') as file:
            # Create a CSV reader object specifying the delimiter, which is comma in this case
            reader = csv.reader(file, delimiter=',')
            
            points = []

            for row in reader:
                point = []
                for item in row:
                    point.append(float(item))

                for i in range(self.dimension):
                    point.append(point[i])

                points.append(point)

        sampling_size = int(len(points) * sampling_ratio)

        assert sampling_size > 1

        points = random.sample(points, sampling_size)

        return points
    

    def cal_domain(self):

        assert len(self.points) > 0

        domain = [[float('inf'), float('-inf')] for _ in range(self.dimension)]

        for point in self.points:
            for i in range(self.dimension):
                domain[i][0] = min(domain[i][0], point[i])
                domain[i][1] = max(domain[i][1], point[i + self.dimension])

        return domain


    def load_workloads(self, workload_path):

        with open(workload_path, 'r') as file:
            # Create a CSV reader object specifying the delimiter, which is comma in this case
            reader = csv.reader(file, delimiter=',')
            
            rectangles = []

            for row in reader:
                rectangle = []
                length = len(row) // self.dimension

                for i in range(length):
                    dim_value = []
                    dim_value.append(float(row[i]))
                    dim_value.append(float(row[i + self.dimension]))
                    rectangle.append(dim_value)

                rectangles.append(rectangle)

        return rectangles
    
    def gen_actions(self, is_sample=True, sample_size=400):

        assert len(self.query_rectangles) > 0

        actions = []
        for i in range(self.dimension):
            dim_actions = []
            for rect in self.query_rectangles:
                dim_actions.append((i, rect[i][0]))
                dim_actions.append((i, rect[i][i]))
            actions.append(sorted(dim_actions, key=lambda x: x[1]))

        sample_size = sample_size // self.dimension
        sample_size += 1 # will remove the first sampled rectangle since the split value can be 0.0

        if is_sample:
            for i in range(self.dimension):
                interval = len(actions[i]) // sample_size
                if interval > 0:
                    actions[i] = [actions[i][j * interval] for j in range(sample_size)]
                else:
                    actions[i] = random.sample(actions[i], sample_size)  # Fallback to random sampling if interval is 0
                actions[i].pop(0)

        return actions
    

    def reset(self):
        # Reset the environment to an initial state
        self.node_queue = []
        self.tree = QDTree(leaf_capacity=self.leaf_threshold, dimension=self.dimension, query_rectangles=self.query_rectangles)  
        root = self.tree.build(self.points, domain=self.domain)
        self.node_queue.append(root)
        # print("reset domain:", node.domain)
        return {root.id: np.array(root.get_state())}

    def step(self, action_dict):
        # Execute one time step within the environment based on the action
        # Optionally, capture and store the intermediate state before applying the action
        # print()
        # print("--------------------------------step--------------------------------")
        # print("step(self, action_dict)", action_dict)

        rewards = {}
        dones = {"__all__": False}
        next_obs = {}
        infos = {}

        # print("STEP 0: len(self.node_queue):", len(self.node_queue))

        if not self.node_queue:
            self._calculate_reward(self.tree.root)
            next_obs, rewards = self.get_tree_states_and_rewards(self.tree.root)
            for agent_id in rewards.keys():
                dones[agent_id] = True
                # rewards[agent_id] = reward
                # next_obs[agent_id] = np.zeros(self.observation_space.shape)  # Assuming all agents share the same observation space
                infos[agent_id] = {}
            dones["__all__"] = True
            # print("_, reward", _, reward)
            return next_obs, rewards, dones, infos

        node = self.node_queue[0]

        for agent_id, action in action_dict.items():

            split_dim, split_value = self.flatten_actions[action]

            # if cannot split do split again

            # print(node.domain[split_dim][0], split_value, node.domain[split_dim][1])

            if node.domain[split_dim][0] >= split_value or node.domain[split_dim][1] <= split_value:
                next_obs[agent_id] = np.array(node.get_state())  # Make sure get_state() is properly returning the state
                rewards[agent_id] = 0
                dones[agent_id] = False
                infos[agent_id] = {'invalid_split': True}
                continue
            
            # print("STEP 1: len(self.node_queue):", len(self.node_queue))
            left_points = [point for point in node.points if (point[split_dim] + point[split_dim + self.dimension]) / 2 <= split_value]
            right_points = [point for point in node.points if (point[split_dim] + point[split_dim + self.dimension]) / 2 > split_value]

            if len(left_points) == 0 or len(right_points) == 0:
                next_obs[agent_id] = np.array(node.get_state())  # Make sure get_state() is properly returning the state
                rewards[agent_id] = 0
                dones[agent_id] = False
                infos[agent_id] = {'invalid_split': True}
                continue

            self.node_queue.pop(0)

            left_domain = copy.deepcopy(node.domain)
            left_domain[split_dim][1] = split_value

            right_domain = copy.deepcopy(node.domain)
            right_domain[split_dim][0] = split_value

            left_node = Node(points=left_points, capacity=self.leaf_threshold, domain=left_domain, id=node.id*2+1)
            right_node = Node(points=right_points, capacity=self.leaf_threshold, domain=right_domain, id=node.id*2+2)

            node.left = left_node
            node.right = right_node

            # print("node points:", len(node.points), " left_node points:", len(left_node.points), " right_node points:", len(right_node.points))
            # print("step domain:", node.domain[split_dim][0], split_value, node.domain[split_dim][1], split_dim)

            # print("left_node:", left_node.domain)
            # print("right_node:", right_node.domain)

            if not left_node.is_leaf():
                self.node_queue.append(left_node)

            if not right_node.is_leaf():
                self.node_queue.append(right_node)

            # print("STEP 2: len(self.node_queue):", len(self.node_queue))
            
            if not self.node_queue:
                self._calculate_reward(self.tree.root)
                next_obs, rewards = self.get_tree_states_and_rewards(self.tree.root)
                for agent_id in rewards.keys():
                    dones[agent_id] = True
                    # rewards[agent_id] = reward
                    # next_obs[agent_id] = np.zeros(self.observation_space.shape)  # Assuming all agents share the same observation space
                    infos[agent_id] = {}
                dones["__all__"] = True
                break

            next_obs[agent_id] = np.array(self.node_queue[0].get_state()) #if self.node_queue else np.zeros(self.observation_space.shape)
            dones[agent_id] = False
            dones["__all__"] = False
            rewards[agent_id] = 0
            infos[agent_id] = {}
        
        return next_obs, rewards, dones, infos
    

    def get_tree_states_and_rewards(self, root):

        level_nodes = [root]

        states = {}
        rewards = {}

        while level_nodes:
            node = level_nodes.pop(0)
            states[node.id] = np.array(node.get_state())
            rewards[node.id] = node.reward
            if not node.is_leaf():
                level_nodes.append(node.left)
                level_nodes.append(node.right)

        return states, rewards

    def _calculate_reward(self, node):

        skip = 0
        normalised_reward = 0.0

        assert self.query_rectangles is not None # "self.query_rectangles is not None"
        assert node.points is not None # "node.points is not None"
        assert len(self.query_rectangles) > 0 # self.query_rectangles more than 0
        assert len(node.points) > 0 # node.points more than 0
        
        if node.left == None or node.right == None or node.is_leaf():
            for rec in self.query_rectangles:
                if not self._is_interacted(rec, node.domain):
                    skip += len(node.points)
            normalised_reward = skip / (len(self.query_rectangles) * len(node.points))
        else:
            skip_left, _ = self._calculate_reward(node.left)
            skip_right, _ = self._calculate_reward(node.right)    
            skip = skip_left + skip_right
            normalised_reward = skip / (len(self.query_rectangles) * len(node.points))
        node.reward = normalised_reward
        return skip, normalised_reward
    

    def _is_interacted(self, rec1, rec2):

        low_x_1 = rec1[0][0]
        high_x_1 = rec1[0][1]

        low_y_1 = rec1[1][0]
        high_y_1 = rec1[1][1]

        low_x_2 = rec2[0][0]
        high_x_2 = rec2[0][1]

        low_y_2 = rec2[1][0]
        high_y_2 = rec2[1][1]

        if low_x_1 > high_x_2 or high_x_1 < low_x_2:
            return False
        
        if low_y_1 > high_y_2 or high_y_1 < low_y_2:
            return False
        
        return True
    