"""
Model Ensemble
============

Ensemble system combining LSTM and Transformer predictions with dynamic weighting.

REQUIREMENTS:
- Dynamic weight adjustment based on performance
- Multi-target prediction support
- Target-specific weighting
    - ROI predictions: 50%
    - Volatility predictions: 30%
    - Trend direction predictions: 20%
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn

from .lstm_model import LSTMModel
from .transformer_model import TransformerModel


class ModelEnsemble:
    def __init__(self, config: Dict):
        """Initialize model ensemble with configuration"""
        self.config = config

        # Initialize models
        self.lstm = LSTMModel(
            input_size=config.get("input_size", 5),
            hidden_size=config.get("lstm_hidden_size", 128),
            num_layers=config.get("lstm_layers", 3),
        )

        self.transformer = TransformerModel(
            input_size=config.get("input_size", 5),
            d_model=config.get("transformer_d_model", 128),
            nhead=config.get("transformer_heads", 8),
        )

        # Initialize weights (ROI:50%, Volatility:30%, Trend:20%)
        self.target_weights = {"roi": 0.5, "volatility": 0.3, "trend": 0.2}

        # Model performance tracking
        self.model_weights = {"lstm": 0.5, "transformer": 0.5}

        # Performance history
        self.performance_history = []

        # EMA alpha for weight updates (0.1 = slower adaptation)
        self.ema_alpha = 0.1

        # TODO: Add model checkpointing
        # TODO: Implement confidence thresholding
        # TODO: Add online learning capability

    def predict(
        self, data: torch.Tensor, update_weights: bool = True
    ) -> Dict[str, torch.Tensor]:
        """
        Make ensemble prediction with dynamic weighting

        Args:
            data: Input tensor of shape (batch_size, sequence_length, input_size)
            update_weights: Whether to update model weights based on performance

        Returns:
            Dictionary containing predictions and confidence scores
        """
        # LSTM predictions
        lstm_pred, lstm_attention = self.lstm(data)

        # Transformer predictions
        pattern_prob, risk_assessment, trend_pred = self.transformer(data)

        # Combine predictions with current weights
        weighted_predictions = {
            "roi": (
                lstm_pred * self.model_weights["lstm"]
                + pattern_prob * self.model_weights["transformer"]
            )
            * self.target_weights["roi"],
            "volatility": risk_assessment * self.target_weights["volatility"],
            "trend": trend_pred * self.target_weights["trend"],
        }

        # Calculate confidence scores
        confidence_scores = {
            "lstm": float(torch.mean(lstm_attention).item()),
            "transformer": float(torch.mean(pattern_prob).item()),
        }

        # Update weights if requested
        if update_weights:
            self._update_weights(confidence_scores)

        return {
            "predictions": weighted_predictions,
            "confidence": confidence_scores,
            "model_weights": self.model_weights.copy(),
        }

    def _update_weights(self, confidence_scores: Dict[str, float]):
        """Update model weights using exponential moving average"""
        total_confidence = sum(confidence_scores.values())
        if total_confidence > 0:
            # Calculate new weights
            new_weights = {
                model: score / total_confidence
                for model, score in confidence_scores.items()
            }

            # Update weights with EMA
            for model in self.model_weights:
                current_weight = self.model_weights[model]
                new_weight = new_weights[model]
                self.model_weights[model] = (
                    current_weight * (1 - self.ema_alpha) + new_weight * self.ema_alpha
                )

            # Store performance
            self.performance_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "weights": self.model_weights.copy(),
                    "confidence_scores": confidence_scores,
                }
            )

    def get_performance_metrics(self) -> Dict:
        """Get current performance metrics"""
        if not self.performance_history:
            return {}

        latest = self.performance_history[-1]
        return {
            "model_weights": latest["weights"],
            "confidence_scores": latest["confidence_scores"],
            "timestamp": latest["timestamp"],
        }

    def validate(self, validation_data: torch.Tensor) -> Dict[str, float]:
        """Run validation pass on ensemble"""
        with torch.no_grad():
            results = self.predict(validation_data, update_weights=False)

        metrics = {
            "lstm_confidence": float(results["confidence"]["lstm"]),
            "transformer_confidence": float(results["confidence"]["transformer"]),
            "combined_confidence": float(
                results["confidence"]["lstm"] * self.model_weights["lstm"]
                + results["confidence"]["transformer"]
                * self.model_weights["transformer"]
            ),
        }

        return metrics
