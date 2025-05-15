import torch
from torch import nn


class DQN:
    def __init__(self, num_of_in_nodes, layer1_nodes, num_outputs):
        super().__init__()
        self.fc1 = nn.Linear(
            num_of_in_nodes, layer1_nodes
        )  # first fully connected layer
        self.out = nn.Linear(layer1_nodes, num_outputs)  # ouptut layer


num_states = 42
num_actions = 7
myDQN = DQN(num_states, num_states, num_actions)
