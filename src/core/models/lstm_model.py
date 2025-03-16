"""
LSTM Model
=========

Trade prediction model using LSTM architecture with attention mechanism.

REQUIREMENTS:
- Multi-layer LSTM with dropout
- Attention mechanism
- Residual connections
- Layer normalization
"""

from typing import Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


class LSTMModel(nn.Module):
    def __init__(
        self,
        input_size: int = 5,
        hidden_size: int = 128,
        num_layers: int = 3,
        dropout: float = 0.2,
        bidirectional: bool = True,
    ):
        """
        Initialize LSTM model for trade prediction

        Args:
            input_size: Number of input features
            hidden_size: LSTM hidden state size
            num_layers: Number of LSTM layers
            dropout: Dropout rate
            bidirectional: Whether to use bidirectional LSTM
        """
        super().__init__()

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.dropout = dropout
        self.bidirectional = bidirectional
        self.num_directions = 2 if bidirectional else 1

        # Layer normalization for input
        self.layer_norm_input = nn.LayerNorm(input_size)

        # LSTM layers with residual connections
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout if num_layers > 1 else 0,
            bidirectional=bidirectional,
            batch_first=True,
        )

        # Attention mechanism
        attention_size = hidden_size * self.num_directions
        self.attention = nn.Sequential(
            nn.Linear(attention_size, attention_size // 2),
            nn.Tanh(),
            nn.Linear(attention_size // 2, 1),
            nn.Softmax(dim=1),
        )

        # Output layers
        self.fc1 = nn.Linear(attention_size, attention_size // 2)
        self.dropout1 = nn.Dropout(dropout)
        self.layer_norm1 = nn.LayerNorm(attention_size // 2)

        self.fc2 = nn.Linear(attention_size // 2, attention_size // 4)
        self.dropout2 = nn.Dropout(dropout)
        self.layer_norm2 = nn.LayerNorm(attention_size // 4)

        self.fc3 = nn.Linear(attention_size // 4, 1)

        # TODO: Add trade-specific output heads
        # TODO: Implement position-wise feedforward
        # TODO: Add skip connections between layers

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass with attention mechanism

        Args:
            x: Input tensor of shape (batch_size, sequence_length, input_size)

        Returns:
            Tuple of (predictions, attention_weights)
        """
        # Layer normalization
        x = self.layer_norm_input(x)

        # LSTM layers
        lstm_out, _ = self.lstm(x)

        # Attention mechanism
        attention_weights = self.attention(lstm_out)
        attention_output = torch.sum(lstm_out * attention_weights, dim=1)

        # Fully connected layers with residual connections
        out = self.fc1(attention_output)
        out = self.dropout1(out)
        out = self.layer_norm1(out)
        out = F.relu(out)

        # Residual connection
        residual = out

        out = self.fc2(out)
        out = self.dropout2(out)
        out = self.layer_norm2(out)
        out = F.relu(out)

        # Add residual
        out = out + residual[:, : out.size(1)]

        # Final prediction
        predictions = self.fc3(out)

        return predictions, attention_weights

    def predict(self, x: torch.Tensor) -> torch.Tensor:
        """Make prediction with input validation"""
        if x.dim() != 3:
            raise ValueError(f"Expected 3D input tensor, got {x.dim()}D")

        if x.size(-1) != self.input_size:
            raise ValueError(f"Expected input size {self.input_size}, got {x.size(-1)}")

        predictions, _ = self.forward(x)
        return predictions
