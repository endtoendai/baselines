"""
dqn.py
"""
import torch
import torch.nn as nn


class DQN(nn.Module):
    def __init__(self, num_inputs: int, num_actions: int) -> None:
        """
        The deep Q-network specified in DQN2015 paper. Can be used with
        84x84 frame environments.
        """
        super().__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(num_inputs, 32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU(),
        )
        self.fc_layers = nn.Sequential(
            nn.Linear(3136, 512),
            nn.ReLU(),
            nn.Linear(512, num_actions)
        )

    def forward(self, x: torch.tensor) -> torch.tensor:
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        x = self.fc_layers(x)
        return x
