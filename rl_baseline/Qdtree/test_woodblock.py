# import torch
# from ray.rllib.models import ModelCatalog
# from gym.spaces import Box, Discrete
# from woodblock import WoodBlockAgent 

# import torch
# from ray.rllib.models import ModelCatalog
# from gym.spaces import Box, Discrete

# class DummyEnv:
#     def __init__(self):
#         self.observation_space = Box(low=-1.0, high=1.0, shape=(4,))
#         self.action_space = Discrete(2)

# def test_wood_block_agent():
#     print("Testing WoodBlockAgent...")

#      # Define your custom fcnet_hiddens
#     custom_fcnet_hiddens = [256, 256]  # Example custom hidden layer sizes

#     # Create a dummy environment to get observation and action spaces
#     env = DummyEnv()

#     # Instantiate the model using dummy environment spaces and custom fcnet_hiddens
#     model = WoodBlockAgent(
#         obs_space=env.observation_space,
#         action_space=env.action_space,
#         num_outputs=env.action_space.n,
#         model_config={
#             "fcnet_hiddens": custom_fcnet_hiddens,  # Pass custom_fcnet_hiddens via model_config
#         },
#         name="WoodBlockAgent"
#     )

#     print("Model instantiated successfully!")

#     # Perform a forward pass using mock data
#     input_dict = {"obs": torch.rand(size=(1, *env.observation_space.shape))}
#     state = []
#     seq_lens = torch.tensor([1])
#     model_out, _ = model.forward(input_dict, state, seq_lens)
#     print("Forward pass check passed!")
#     print("Model output:", model_out)

#     # Check the value function
#     value = model.value_function()
#     print("Value function check passed!")
#     print("Value estimate:", value)

# if __name__ == "__main__":
#     test_wood_block_agent()


import numpy as np
import gym
from gym.spaces import Box, Discrete
import torch
from ray.rllib.models import ModelCatalog
from ray.rllib.agents.ppo import PPOTrainer
from ray import tune
from qdtree_env import QdtreeEnv

# Assuming woodblock.py contains the WoodBlockAgent definition
from woodblock import WoodBlockAgent


class DummyEnv(gym.Env):
    """A simple dummy environment to illustrate the use of RLlib with custom models"""
    def __init__(self, config=None):
        super(DummyEnv, self).__init__()
        self.observation_space = Box(low=-1.0, high=1.0, shape=(4,))
        self.action_space = Discrete(2)
        self.state = np.random.uniform(low=-1.0, high=1.0, size=(4,))
    
    def reset(self):
        self.state = np.random.uniform(low=-1.0, high=1.0, size=(4,))
        return self.state

    def step(self, action):
        next_state = np.random.uniform(low=-1.0, high=1.0, size=(4,))
        reward = np.random.rand()
        done = np.random.choice([True, False], p=[0.1, 0.9])
        return next_state, reward, done, {}

# Register the custom model to be used with RLlib
ModelCatalog.register_custom_model("woodblock_model", WoodBlockAgent)

def test_model_training():
    # Configuration for the training
    config = {
        "env": QdtreeEnv,  # Specify the environment class directly here
        "env_config": {  # Pass initialization arguments to your env through env_config
            "leaf_threshold": 100,
            "dataset_path": "data/synthetic/dataset/data_3200000_2_uniform_1.csv",
            "workload_path": "data/synthetic/query/range_1000_2_uniform_1_0.01x0.01.csv",
            "dimension": 2,
            "dump_dir": ".",
            "sampling_ratio": 0.001,
            "action_sampling_size": 100
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
    for i in range(1):
        result = trainer.train()
        print(f"Iteration: {i}, reward: {result['episode_reward_mean']}")

        if i % 10 == 0:
            checkpoint = trainer.save()
            print(f"Checkpoint saved at {checkpoint}")

            # Model tracing and saving
            model = trainer.get_policy().model
            model.eval()  # Ensure model is in evaluation mode
            
            # Creating a dummy input according to the model's expected input format
            example_input = torch.rand(1, 32 * 2 * 2 + 2 + 100).to(model.device)  # Adjust the dimension according to your needs

            # Ensure no gradient calculations
            with torch.no_grad():
                output = model.combined_model.forward(example_input)
                print("formard", output)
                traced_script_module = torch.jit.trace(model.combined_model, example_input)

                traced_script_module.save(f"model_checkpoint_{i}.pth")
                print(f"JIT model saved at model_checkpoint_{i}.pth")


            loaded_model = torch.jit.load(f"model_checkpoint_{i}.pth")
            print("Model loaded successfully.")

            # Predict
            with torch.no_grad():
                prediction = loaded_model(example_input)
                print("Prediction:", prediction)

            assert torch.equal(output, prediction) # model is saved or loaded incorrectly.



def test_wood_block_agent():
    print("Testing WoodBlockAgent...")
    # env = DummyEnv()
    
    env = QdtreeEnv(leaf_threshold=100, 
                    dataset_path="data/synthetic/dataset/data_100000_2_uniform_1.csv",
                    workload_path="data/synthetic/query/range_1000_2_uniform_1_0.01x0.01.csv",
                    dimension=2,
                    dump_dir=".",
                    sampling_ratio=0.01,
                    action_sampling_size=200)
    
    model = WoodBlockAgent(
        obs_space=env.observation_space,
        action_space=env.action_space,
        num_outputs=env.action_space.n,
        model_config={"fcnet_hiddens": [256, 256]},
        name="WoodBlockAgent"
    )
    print("Model instantiated successfully!")

    input_dict = {"obs": torch.rand(size=(1, *env.observation_space.shape))}
    state = env.reset()
    seq_lens = torch.tensor([1])
    model_out, _ = model.forward(input_dict, state, seq_lens)
    print("Forward pass check passed!")
    print("Model output:", model_out)

    value = model.value_function()
    print("Value function check passed!")
    print("Value estimate:", value)

if __name__ == "__main__":
    # test_wood_block_agent()
    test_model_training()
