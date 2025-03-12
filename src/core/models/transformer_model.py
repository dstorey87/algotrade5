"""
Transformer Model
===============

Market pattern recognition using Transformer architecture.

REQUIREMENTS:
- Multi-head self-attention
- Positional encoding
- Feed-forward networks
- Layer normalization
"""

import math
import torch
import torch.nn as nn
import numpy as np
from typing import Optional, Tuple

class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, max_len: int = 5000):
        """Initialize positional encoding"""
        super().__init__()
        
        # Create positional encoding matrix
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        
        # Apply sine and cosine functions
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Add positional encoding to input"""
        return x + self.pe[:, :x.size(1)]

class TransformerModel(nn.Module):
    def __init__(self,
                 input_size: int = 5,
                 d_model: int = 128,
                 nhead: int = 8,
                 num_layers: int = 6,
                 dim_feedforward: int = 512,
                 dropout: float = 0.1,
                 activation: str = "gelu"):
        """
        Initialize Transformer model for pattern recognition
        
        Args:
            input_size: Number of input features
            d_model: Model dimension
            nhead: Number of attention heads
            num_layers: Number of transformer layers
            dim_feedforward: Dimension of feedforward network
            dropout: Dropout rate
            activation: Activation function
        """
        super().__init__()
        
        self.input_size = input_size
        self.d_model = d_model
        
        # Input projection
        self.input_projection = nn.Linear(input_size, d_model)
        
        # Positional encoding
        self.pos_encoder = PositionalEncoding(d_model)
        
        # TODO: Add relative positional encoding
        # TODO: Implement adaptive attention span
        # TODO: Add local attention mechanism
        
        # Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            activation=activation,
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers,
            norm=nn.LayerNorm(d_model)
        )
        
        # Output layers
        self.fc1 = nn.Linear(d_model, d_model // 2)
        self.dropout1 = nn.Dropout(dropout)
        self.layer_norm1 = nn.LayerNorm(d_model // 2)
        
        self.fc2 = nn.Linear(d_model // 2, d_model // 4)
        self.dropout2 = nn.Dropout(dropout)
        self.layer_norm2 = nn.LayerNorm(d_model // 4)
        
        # Pattern recognition heads
        self.pattern_head = nn.Linear(d_model // 4, 1)  # Trade pattern probability
        self.risk_head = nn.Linear(d_model // 4, 1)     # Risk assessment
        self.trend_head = nn.Linear(d_model // 4, 3)    # Trend classification (up/down/sideways)
        
        # Initialize weights
        self._init_weights()
        
    def _init_weights(self):
        """Initialize model weights"""
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)
                
    def _generate_square_subsequent_mask(self, sz: int) -> torch.Tensor:
        """Generate attention mask for sequence"""
        mask = (torch.triu(torch.ones(sz, sz)) == 1).transpose(0, 1)
        mask = mask.float().masked_fill(mask == 0, float('-inf')).masked_fill(mask == 1, float(0.0))
        return mask
        
    def forward(self, src: torch.Tensor,
                src_mask: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Forward pass through transformer
        
        Args:
            src: Input tensor of shape (batch_size, sequence_length, input_size)
            src_mask: Optional mask for attention
            
        Returns:
            Tuple of (pattern_prob, risk_assessment, trend_prediction)
        """
        # Input projection and positional encoding
        x = self.input_projection(src) * math.sqrt(self.d_model)
        x = self.pos_encoder(x)
        
        # Generate attention mask if not provided
        if src_mask is None:
            src_mask = self._generate_square_subsequent_mask(src.size(1)).to(src.device)
            
        # Transformer encoder
        encoded = self.transformer_encoder(x, src_mask)
        
        # Take the last sequence output for prediction
        x = encoded[:, -1]
        
        # Fully connected layers
        x = self.fc1(x)
        x = self.dropout1(x)
        x = self.layer_norm1(x)
        x = torch.relu(x)
        
        x = self.fc2(x)
        x = self.dropout2(x)
        x = self.layer_norm2(x)
        x = torch.relu(x)
        
        # Pattern recognition heads
        pattern_prob = torch.sigmoid(self.pattern_head(x))
        risk_assessment = self.risk_head(x)
        trend_pred = torch.softmax(self.trend_head(x), dim=-1)
        
        return pattern_prob, risk_assessment, trend_pred
        
    def predict(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Make predictions with input validation"""
        if x.dim() != 3:
            raise ValueError(f"Expected 3D input tensor, got {x.dim()}D")
            
        if x.size(-1) != self.input_size:
            raise ValueError(f"Expected input size {self.input_size}, got {x.size(-1)}")
            
        return self.forward(x)