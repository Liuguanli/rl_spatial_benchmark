import argparse
import json
import os
import parser

import gym
import numpy as np
import ray
import torch
import torch.optim as optim
from gym.spaces import Box, Discrete
from qdtree_env import QdtreeEnv
from ray import tune
from ray.rllib.agents.ppo import PPOTrainer
from ray.rllib.models import ModelCatalog
from ray.tune import grid_search, run_experiments
from ray.tune.registry import register_env
from torch.distributions import Categorical
# Assuming woodblock.py contains the WoodBlockAgent definition
from woodblock import WoodBlockAgent

parser = argparse.ArgumentParser()

parser.add_argument(
    "--dump_dir",
    type=str,
    default="./benchmark/libspatialindex",
    required=False,
    help="Dump valid trees to this directory for later inspection.")

parser.add_argument(
    "--leaf_threshold",
    type=int,
    default=100,
    required=False,
    help="The number of recoreds in leaf node.")

parser.add_argument(
    "--dimension",
    type=int,
    default=2,
    required=False,
    help="Dimensionality of data points and queries.")

parser.add_argument(
    "--dataset",
    type=str,
    default=None,
    required=True,
    help="Training dataset.")

parser.add_argument(
    "--workloads",
    type=str,
    default=None,
    required=True,
    help="Query workloads.")

parser.add_argument(
    "--sampling_ratio",
    type=float,
    default=0.01,
    required=False,
    help="Sampling ratio for training")

parser.add_argument(
    "--action_sampling_size",
    type=int,
    default=400,
    required=False,
    help="Sampling ratio for training")

parser.add_argument(
    "--episode",
    type=int,
    default=100,
    required=False,
    help="Sampling ratio for training")


def save_model(trainer, args):
    # Model tracing and saving
    model = trainer.get_policy().model
    model.eval()  # Ensure model is in evaluation mode
    
    # Creating a dummy input according to the model's expected input format
    example_input = torch.rand(1, 32 * 2 * args.dimension).to(model.device) 

    # Ensure no gradient calculations
    with torch.no_grad():
        traced_script_module = torch.jit.trace(model.combined_model, example_input)
        traced_script_module.save(os.path.join(args.dump_dir, "qdtree.pth"))



def train_model(args):
    # Configuration for the training
    config = {
        "env": QdtreeEnv,  # Specify the environment class directly here
        "env_config": {  # Pass initialization arguments to your env through env_config
            "leaf_threshold": args.leaf_threshold,
            "dataset_path": args.dataset,  # "data/synthetic/dataset/data_3200000_2_uniform_1.csv"
            "workload_path": args.workloads, # "data/synthetic/query/range_1000_2_uniform_1_0.01x0.01.csv"
            "dimension": args.dimension,
            "sampling_ratio": args.sampling_ratio,
            "action_sampling_size": args.action_sampling_size
        },
        "model": {
            "custom_model": "woodblock_model",
            "custom_model_config": {
                "fcnet_hiddens": [512, 512],
            },
        },
        "num_workers": 1,
        "num_envs_per_worker": 1,
        "rollout_fragment_length": 200,
        "train_batch_size": 4000,
        "framework": "torch",
        "lr": 5e-3,
    }

    trainer = PPOTrainer(config=config)
    for i in range(args.episode):
        result = trainer.train()
        print(f"Iteration: {i}, reward: {result['episode_reward_mean']}")

        # if i % 10 == 0:
        #     checkpoint = trainer.save()
        #     print(f"Checkpoint saved at {checkpoint}")

    save_model(trainer, args)

if __name__ == "__main__":

    ModelCatalog.register_custom_model("woodblock_model", WoodBlockAgent)

    args = parser.parse_args()
    
    train_model(args)