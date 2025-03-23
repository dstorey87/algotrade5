import logging

# REMOVED_UNUSED_CODE: import torch
from torch import nn


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class PyTorchMLPModel(nn.Module):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     A multi-layer perceptron (MLP) model implemented using PyTorch.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     This class mainly serves as a simple example for the integration of PyTorch model's
# REMOVED_UNUSED_CODE:     to freqai. It is not optimized at all and should not be used for production purposes.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     :param input_dim: The number of input features. This parameter specifies the number
# REMOVED_UNUSED_CODE:         of features in the input data that the MLP will use to make predictions.
# REMOVED_UNUSED_CODE:     :param output_dim: The number of output classes. This parameter specifies the number
# REMOVED_UNUSED_CODE:         of classes that the MLP will predict.
# REMOVED_UNUSED_CODE:     :param hidden_dim: The number of hidden units in each layer. This parameter controls
# REMOVED_UNUSED_CODE:         the complexity of the MLP and determines how many nonlinear relationships the MLP
# REMOVED_UNUSED_CODE:         can represent. Increasing the number of hidden units can increase the capacity of
# REMOVED_UNUSED_CODE:         the MLP to model complex patterns, but it also increases the risk of overfitting
# REMOVED_UNUSED_CODE:         the training data. Default: 256
# REMOVED_UNUSED_CODE:     :param dropout_percent: The dropout rate for regularization. This parameter specifies
# REMOVED_UNUSED_CODE:         the probability of dropping out a neuron during training to prevent overfitting.
# REMOVED_UNUSED_CODE:         The dropout rate should be tuned carefully to balance between underfitting and
# REMOVED_UNUSED_CODE:         overfitting. Default: 0.2
# REMOVED_UNUSED_CODE:     :param n_layer: The number of layers in the MLP. This parameter specifies the number
# REMOVED_UNUSED_CODE:         of layers in the MLP architecture. Adding more layers to the MLP can increase its
# REMOVED_UNUSED_CODE:         capacity to model complex patterns, but it also increases the risk of overfitting
# REMOVED_UNUSED_CODE:         the training data. Default: 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     :returns: The output of the MLP, with shape (batch_size, output_dim)
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, input_dim: int, output_dim: int, **kwargs):
# REMOVED_UNUSED_CODE:         super().__init__()
# REMOVED_UNUSED_CODE:         hidden_dim: int = kwargs.get("hidden_dim", 256)
# REMOVED_UNUSED_CODE:         dropout_percent: int = kwargs.get("dropout_percent", 0.2)
# REMOVED_UNUSED_CODE:         n_layer: int = kwargs.get("n_layer", 1)
# REMOVED_UNUSED_CODE:         self.input_layer = nn.Linear(input_dim, hidden_dim)
# REMOVED_UNUSED_CODE:         self.blocks = nn.Sequential(*[Block(hidden_dim, dropout_percent) for _ in range(n_layer)])
# REMOVED_UNUSED_CODE:         self.output_layer = nn.Linear(hidden_dim, output_dim)
# REMOVED_UNUSED_CODE:         self.relu = nn.ReLU()
# REMOVED_UNUSED_CODE:         self.dropout = nn.Dropout(p=dropout_percent)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def forward(self, x: torch.Tensor) -> torch.Tensor:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # x: torch.Tensor = tensors[0]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         x = self.relu(self.input_layer(x))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         x = self.dropout(x)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         x = self.blocks(x)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         x = self.output_layer(x)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return x


# REMOVED_UNUSED_CODE: class Block(nn.Module):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     A building block for a multi-layer perceptron (MLP).
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     :param hidden_dim: The number of hidden units in the feedforward network.
# REMOVED_UNUSED_CODE:     :param dropout_percent: The dropout rate for regularization.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     :returns: torch.Tensor. with shape (batch_size, hidden_dim)
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, hidden_dim: int, dropout_percent: int):
# REMOVED_UNUSED_CODE:         super().__init__()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.ff = FeedForward(hidden_dim)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.dropout = nn.Dropout(p=dropout_percent)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.ln = nn.LayerNorm(hidden_dim)

# REMOVED_UNUSED_CODE:     def forward(self, x: torch.Tensor) -> torch.Tensor:
# REMOVED_UNUSED_CODE:         x = self.ff(self.ln(x))
# REMOVED_UNUSED_CODE:         x = self.dropout(x)
# REMOVED_UNUSED_CODE:         return x


class FeedForward(nn.Module):
    """
    A simple fully-connected feedforward neural network block.

    :param hidden_dim: The number of hidden units in the block.
    :return: torch.Tensor. with shape (batch_size, hidden_dim)
    """

    def __init__(self, hidden_dim: int):
        super().__init__()
# REMOVED_UNUSED_CODE:         self.net = nn.Sequential(
# REMOVED_UNUSED_CODE:             nn.Linear(hidden_dim, hidden_dim),
# REMOVED_UNUSED_CODE:             nn.ReLU(),
# REMOVED_UNUSED_CODE:         )

# REMOVED_UNUSED_CODE:     def forward(self, x: torch.Tensor) -> torch.Tensor:
# REMOVED_UNUSED_CODE:         return self.net(x)
