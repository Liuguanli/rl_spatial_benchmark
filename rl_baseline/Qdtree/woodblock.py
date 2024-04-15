from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.rllib.models.modelv2 import ModelV2
from ray.rllib.utils.typing import ModelConfigDict, TensorType
from gym.spaces import Space
from torch import nn, Tensor
import torch

class CombinedModel(nn.Module):
    def __init__(self, shared_fc, actor):
        super(CombinedModel, self).__init__()
        self.shared_fc = shared_fc
        self.actor = actor

    def forward(self, x):
        x = self.shared_fc(x)
        x = self.actor(x)
        indices = torch.argmax(x, dim=1)  # Again, assuming x is (batch_size, num_classes)
        return indices
        # return x

class WoodBlockAgent(TorchModelV2, nn.Module):
    """Custom model for RLlib, built using PyTorch.

    This model incorporates shared fully connected layers with separate actor and critic heads,
    suitable for actor-critic methods.

    Parameters:
    - obs_space (Space): The observation space of the environment.
    - action_space (Space): The action space of the environment.
    - num_outputs (int): Number of outputs (different from action_space.n if using action distribution options).
    - model_config (ModelConfigDict): Dictionary of model-specific configurations.
    - name (str): Name of the model.
    """

    def __init__(self,
                 obs_space: Space,
                 action_space: Space,
                 num_outputs: int,
                 model_config: ModelConfigDict,
                 name: str,
                 **kwargs):
        TorchModelV2.__init__(self, obs_space, action_space, num_outputs, model_config, name)
        nn.Module.__init__(self)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        hiddens: list = model_config.get("fcnet_hiddens", [512, 512])
        assert len(hiddens) == 2, "fcnet_hiddens configuration must consist of exactly two layers."

        self.shared_fc = nn.Sequential(
            nn.Linear(obs_space.shape[0], hiddens[0]),
            nn.ReLU(),
            nn.Linear(hiddens[0], hiddens[1]),
            nn.ReLU()
        )
        
        self.actor = nn.Linear(hiddens[1], action_space.n)
        self.critic = nn.Linear(hiddens[1], 1)
        # Placeholder for the last layer's features to be used in value_function
        self._feature: Tensor = None

        self.combined_model = CombinedModel(self.shared_fc, self.actor)

    def forward(self, input_dict: dict, state: list, seq_lens: Tensor):
        """Implements the forward pass of the model.

        Parameters:
        - input_dict (dict): Dictionary of inputs. Expected key: "obs" for observations.
        - state (list): State inputs (unused for this model).
        - seq_lens (Tensor): Sequence lengths (unused for this model).

        Returns:
        - (Tensor, list): A tuple containing action logits and the state (empty for this model).
        """
        x = input_dict["obs"].float()
        self._feature = self.shared_fc(x)
        action_logits = self.actor(self._feature)
        return action_logits, state
    
    def value_function(self) -> Tensor:
        """Calculates the value of the current state.

        Returns:
        - Tensor: Estimated value of the current state by the critic network.
        """
        return self.critic(self._feature).squeeze(-1)


# refer to: https://zhuanlan.zhihu.com/p/460637302
