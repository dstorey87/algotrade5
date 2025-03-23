import math

import torch
from torch import nn


"""
The architecture is based on the paper “Attention Is All You Need”.
Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez,
Lukasz Kaiser, and Illia Polosukhin. 2017.
"""


# REMOVED_UNUSED_CODE: class PyTorchTransformerModel(nn.Module):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     A transformer approach to time series modeling using positional encoding.
# REMOVED_UNUSED_CODE:     The architecture is based on the paper “Attention Is All You Need”.
# REMOVED_UNUSED_CODE:     Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez,
# REMOVED_UNUSED_CODE:     Lukasz Kaiser, and Illia Polosukhin. 2017.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         input_dim: int = 7,
# REMOVED_UNUSED_CODE:         output_dim: int = 7,
# REMOVED_UNUSED_CODE:         hidden_dim=1024,
# REMOVED_UNUSED_CODE:         n_layer=2,
# REMOVED_UNUSED_CODE:         dropout_percent=0.1,
# REMOVED_UNUSED_CODE:         time_window=10,
# REMOVED_UNUSED_CODE:         nhead=8,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         super().__init__()
# REMOVED_UNUSED_CODE:         self.time_window = time_window
# REMOVED_UNUSED_CODE:         # ensure the input dimension to the transformer is divisible by nhead
# REMOVED_UNUSED_CODE:         self.dim_val = input_dim - (input_dim % nhead)
# REMOVED_UNUSED_CODE:         self.input_net = nn.Sequential(
# REMOVED_UNUSED_CODE:             nn.Dropout(dropout_percent), nn.Linear(input_dim, self.dim_val)
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Encode the timeseries with Positional encoding
# REMOVED_UNUSED_CODE:         self.positional_encoding = PositionalEncoding(d_model=self.dim_val, max_len=self.dim_val)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Define the encoder block of the Transformer
# REMOVED_UNUSED_CODE:         self.encoder_layer = nn.TransformerEncoderLayer(
# REMOVED_UNUSED_CODE:             d_model=self.dim_val, nhead=nhead, dropout=dropout_percent, batch_first=True
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         self.transformer = nn.TransformerEncoder(self.encoder_layer, num_layers=n_layer)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # the pseudo decoding FC
# REMOVED_UNUSED_CODE:         self.output_net = nn.Sequential(
# REMOVED_UNUSED_CODE:             nn.Linear(self.dim_val * time_window, int(hidden_dim)),
# REMOVED_UNUSED_CODE:             nn.ReLU(),
# REMOVED_UNUSED_CODE:             nn.Dropout(dropout_percent),
# REMOVED_UNUSED_CODE:             nn.Linear(int(hidden_dim), int(hidden_dim / 2)),
# REMOVED_UNUSED_CODE:             nn.ReLU(),
# REMOVED_UNUSED_CODE:             nn.Dropout(dropout_percent),
# REMOVED_UNUSED_CODE:             nn.Linear(int(hidden_dim / 2), int(hidden_dim / 4)),
# REMOVED_UNUSED_CODE:             nn.ReLU(),
# REMOVED_UNUSED_CODE:             nn.Dropout(dropout_percent),
# REMOVED_UNUSED_CODE:             nn.Linear(int(hidden_dim / 4), output_dim),
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def forward(self, x, mask=None, add_positional_encoding=True):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Args:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             x: Input features of shape [Batch, SeqLen, input_dim]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             mask: Mask to apply on the attention outputs (optional)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             add_positional_encoding: If True, we add the positional encoding to the input.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                       Might not be desired for some tasks.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         x = self.input_net(x)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if add_positional_encoding:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             x = self.positional_encoding(x)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         x = self.transformer(x, mask=mask)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         x = x.reshape(-1, 1, self.time_window * x.shape[-1])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         x = self.output_net(x)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return x


# REMOVED_UNUSED_CODE: class PositionalEncoding(nn.Module):
# REMOVED_UNUSED_CODE:     def __init__(self, d_model, max_len=5000):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Args
# REMOVED_UNUSED_CODE:             d_model: Hidden dimensionality of the input.
# REMOVED_UNUSED_CODE:             max_len: Maximum length of a sequence to expect.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         super().__init__()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Create matrix of [SeqLen, HiddenDim] representing the positional encoding
# REMOVED_UNUSED_CODE:         # for max_len inputs
# REMOVED_UNUSED_CODE:         pe = torch.zeros(max_len, d_model)
# REMOVED_UNUSED_CODE:         position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
# REMOVED_UNUSED_CODE:         div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
# REMOVED_UNUSED_CODE:         pe[:, 0::2] = torch.sin(position * div_term)
# REMOVED_UNUSED_CODE:         pe[:, 1::2] = torch.cos(position * div_term)
# REMOVED_UNUSED_CODE:         pe = pe.unsqueeze(0)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.register_buffer("pe", pe, persistent=False)

# REMOVED_UNUSED_CODE:     def forward(self, x):
# REMOVED_UNUSED_CODE:         x = x + self.pe[:, : x.size(1)]
# REMOVED_UNUSED_CODE:         return x
