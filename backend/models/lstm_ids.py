"""PyTorch LSTM model for intrusion detection (multi-class).

Defines a reusable LSTM classifier with configurable layers and dropout.
"""
from __future__ import annotations

import torch
import torch.nn as nn


class LSTMIDS(nn.Module):
    """LSTM-based classifier.

    Args
    ----
    input_size: int
        Number of input features per timestep.
    hidden_size: int
        Hidden size for LSTM layers.
    num_layers: int
        Number of stacked LSTM layers.
    num_classes: int
        Number of output classes.
    dropout: float
        Dropout probability applied after LSTM.
    """

    def __init__(self, input_size: int, hidden_size: int = 128, num_layers: int = 2, num_classes: int = 2, dropout: float = 0.3) -> None:
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers=num_layers, batch_first=True, dropout=dropout)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (batch, seq_len, input_size)
        out, _ = self.lstm(x)
        # take last time step output
        out = out[:, -1, :]
        out = self.dropout(out)
        out = self.fc(out)
        return out
