"""
Model Factory
===========

Factory class for creating and configuring AI models.

REQUIREMENTS:
- Standardized model initialization
- Configuration validation
- Resource management
- Model caching
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Optional, Type, Union

import torch

from .lstm_model import LSTMModel
from .model_ensemble import ModelEnsemble
from .transformer_model import TransformerModel

logger = logging.getLogger(__name__)


class ModelFactory:
    """Factory for creating and managing AI models"""

    # Model type registry
    MODEL_TYPES = {
        "lstm": LSTMModel,
        "transformer": TransformerModel,
        "ensemble": ModelEnsemble,
    }

    def __init__(self, base_path: Union[str, Path] = "C:/AlgoTradPro5/models"):
        """Initialize model factory"""
        self.base_path = Path(base_path)
        self.model_cache = {}

        # Default configurations
        self.default_configs = {
            "lstm": {
                "input_size": 5,
                "hidden_size": 128,
                "num_layers": 3,
                "dropout": 0.2,
                "bidirectional": True,
            },
            "transformer": {
                "input_size": 5,
                "d_model": 128,
                "nhead": 8,
                "num_layers": 6,
                "dim_feedforward": 512,
                "dropout": 0.1,
                "activation": "gelu",
            },
            "ensemble": {
                "input_size": 5,
                "lstm_hidden_size": 128,
                "lstm_layers": 3,
                "transformer_d_model": 128,
                "transformer_heads": 8,
            },
        }

        # TODO: Add model versioning
        # TODO: Implement model signature verification
        # TODO: Add dynamic configuration updates

    def create_model(
        self, model_type: str, config: Optional[Dict] = None, use_cache: bool = True
    ) -> torch.nn.Module:
        """
        Create a model instance with validation

        Args:
            model_type: Type of model to create
            config: Model configuration
            use_cache: Whether to use cached models

        Returns:
            Instantiated model
        """
        if model_type not in self.MODEL_TYPES:
            raise ValueError(f"Unknown model type: {model_type}")

        # Generate cache key
        cache_key = f"{model_type}_{hash(str(config))}" if config else model_type

        # Check cache first
        if use_cache and cache_key in self.model_cache:
            logger.info(f"Using cached model: {cache_key}")
            return self.model_cache[cache_key]

        # Merge with default config
        final_config = self.default_configs[model_type].copy()
        if config:
            final_config.update(config)

        # Validate configuration
        self._validate_config(model_type, final_config)

        # Create model instance
        model_class = self.MODEL_TYPES[model_type]
        model = model_class(**final_config)

        # Cache if requested
        if use_cache:
            self.model_cache[cache_key] = model

        return model

    def _validate_config(self, model_type: str, config: Dict):
        """Validate model configuration"""
        required_params = {
            "lstm": ["input_size", "hidden_size", "num_layers"],
            "transformer": ["input_size", "d_model", "nhead", "num_layers"],
            "ensemble": ["input_size", "lstm_hidden_size", "transformer_d_model"],
        }

        # Check required parameters
        missing = [p for p in required_params[model_type] if p not in config]
        if missing:
            raise ValueError(f"Missing required parameters for {model_type}: {missing}")

        # Type validation
        type_checks = {
            "input_size": int,
            "hidden_size": int,
            "d_model": int,
            "num_layers": int,
            "nhead": int,
        }

        for param, expected_type in type_checks.items():
            if param in config and not isinstance(config[param], expected_type):
                raise TypeError(
                    f"Parameter {param} must be {expected_type.__name__}, "
                    f"got {type(config[param]).__name__}"
                )

    def load_model_weights(
        self, model: torch.nn.Module, model_name: str, strict: bool = True
    ):
        """Load model weights from file"""
        weights_path = self.base_path / model_name / "weights.pth"

        if not weights_path.exists():
            raise FileNotFoundError(f"Model weights not found: {weights_path}")

        state_dict = torch.load(weights_path, map_location=torch.device("cpu"))
        model.load_state_dict(state_dict, strict=strict)

    def save_model_weights(
        self, model: torch.nn.Module, model_name: str, overwrite: bool = False
    ):
        """Save model weights to file"""
        weights_dir = self.base_path / model_name
        weights_dir.mkdir(parents=True, exist_ok=True)

        weights_path = weights_dir / "weights.pth"
        if weights_path.exists() and not overwrite:
            raise FileExistsError(f"Model weights already exist: {weights_path}")

        torch.save(model.state_dict(), weights_path)

    def get_model_config(self, model_name: str) -> Dict:
        """Load model configuration from file"""
        config_path = self.base_path / model_name / "config.json"

        if not config_path.exists():
            raise FileNotFoundError(f"Model config not found: {config_path}")

        with open(config_path) as f:
            return json.load(f)

    def clear_cache(self):
        """Clear model cache"""
        self.model_cache.clear()
        torch.cuda.empty_cache()
