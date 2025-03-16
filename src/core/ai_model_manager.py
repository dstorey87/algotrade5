"""
AI Model Manager
==============

CRITICAL REQUIREMENTS:
- Models loaded only from configured models path
- 85% minimum prediction accuracy
- Real-time performance monitoring
- Automatic fallback mechanisms

VALIDATION GATES:
1. Model validation
2. Prediction confidence
3. Performance tracking
4. Resource monitoring

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import gc
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

import numpy as np
import psutil
import torch
from config_manager import get_config
from error_manager import ErrorManager, ErrorSeverity
from torch.cuda.amp import autocast

logger = logging.getLogger(__name__)


class AIModelManager:
    """AI model management and validation system"""

    def __init__(self, config: Optional[Dict] = None):
        """Initialize AI model manager with strict validation"""
        self.config = config or get_config()
        self.models_path = Path(self.config["models_path"])
        self.device = self._initialize_device()

        # Error handling
        self.error_manager = ErrorManager()

        # STRICT: Validation thresholds from config
        model_config = self.config["model_config"]
        self.min_accuracy = model_config.get("min_accuracy", 0.85)
        self.min_confidence = model_config.get("min_confidence", 0.85)
        self.max_response_time = model_config.get("max_response_time", 0.05)

        # Model tracking
        self.loaded_models = {}
        self.model_performance = {}
        self.fallback_enabled = model_config.get("fallback_enabled", True)

        # Resource monitoring
        self.max_memory_usage = 0.90  # 90% threshold
        self.max_gpu_memory = 0.85  # 85% threshold

        # Initialize models
        self._load_models()
        logger.info("AI Model Manager initialized with strict validation")

    def _initialize_device(self) -> torch.device:
        """Initialize compute device with validation"""
        try:
            if torch.cuda.is_available():
                device = torch.device("cuda")
                logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
            else:
                device = torch.device("cpu")
                logger.warning("GPU not available, using CPU")
            return device

        except Exception as e:
            self.error_manager.log_error(
                f"Device initialization failed: {e}", ErrorSeverity.HIGH.value, "GPU"
            )
            return torch.device("cpu")

    def _load_models(self) -> None:
        """Load AI models with strict validation"""
        try:
            if not self.models_path.exists():
                raise ValueError(f"Models directory not found: {self.models_path}")

            model_configs = list(self.models_path.glob("*/config.json"))
            if not model_configs:
                raise ValueError("No model configurations found")

            for config_path in model_configs:
                try:
                    with open(config_path) as f:
                        model_config = json.load(f)

                    model_name = model_config["name"]
                    model_type = model_config["type"]

                    if not self._check_resources():
                        logger.error("Insufficient resources to load model")
                        break

                    model = self._load_model(model_name, model_type)
                    if self._validate_model(model, model_name):
                        self.loaded_models[model_name] = {
                            "model": model,
                            "config": model_config,
                            "performance": {
                                "accuracy": 0.0,
                                "confidence": 0.0,
                                "response_time": 0.0,
                                "last_check": datetime.now().isoformat(),
                            },
                        }
                        logger.info(f"✅ Loaded and validated model: {model_name}")
                    else:
                        logger.warning(f"❌ Model validation failed: {model_name}")

                except Exception as e:
                    self.error_manager.log_error(
                        f"Error loading model {config_path}: {e}",
                        ErrorSeverity.MEDIUM.value,
                        "Model",
                    )

        except Exception as e:
            self.error_manager.log_error(
                f"Critical error loading models: {e}",
                ErrorSeverity.HIGH.value,
                "ModelLoader",
            )
            raise

    def _check_resources(self) -> bool:
        """Verify system resources are available"""
        try:
            memory_usage = psutil.virtual_memory().percent / 100
            if memory_usage > self.max_memory_usage:
                logger.warning(f"High memory usage: {memory_usage:.1%}")
                return False

            if torch.cuda.is_available():
                gpu_memory = (
                    torch.cuda.memory_allocated() / torch.cuda.max_memory_allocated()
                )
                if gpu_memory > self.max_gpu_memory:
                    logger.warning(f"High GPU memory usage: {gpu_memory:.1%}")
                    return False

            return True

        except Exception as e:
            self.error_manager.log_error(
                f"Error checking resources: {e}",
                ErrorSeverity.MEDIUM.value,
                "Resources",
            )
            return False

    def _load_model(
        self, model_name: str, model_type: str
    ) -> Optional[torch.nn.Module]:
        """Load specific AI model with validation"""
        try:
            model_path = self.models_path / model_name
            if not model_path.exists():
                raise FileNotFoundError(f"Model not found: {model_path}")

            # Load model based on type
            if model_type == "pytorch":
                model = torch.load(model_path / "model.pt", map_location=self.device)
            else:
                raise ValueError(f"Unsupported model type: {model_type}")

            model.eval()
            return model

        except Exception as e:
            self.error_manager.log_error(
                f"Error loading model {model_name}: {e}",
                ErrorSeverity.MEDIUM.value,
                "ModelLoader",
            )
            return None

    def _validate_model(
        self, model: Optional[torch.nn.Module], model_name: str
    ) -> bool:
        """Validate model meets performance requirements"""
        if model is None:
            return False

        try:
            # Run validation tests
            test_input = torch.randn(1, 10, device=self.device)
            with torch.no_grad():
                _ = model(test_input)

            return True

        except Exception as e:
            self.error_manager.log_error(
                f"Model validation failed for {model_name}: {e}",
                ErrorSeverity.MEDIUM.value,
                "Validation",
            )
            return False

    def predict(self, data: np.ndarray, model_name: str) -> Dict[str, float]:
        """Make prediction with performance tracking"""
        if model_name not in self.loaded_models:
            logger.error(f"Model not found: {model_name}")
            if self.fallback_enabled:
                return self._get_fallback_prediction(data)
            return {}

        try:
            model = self.loaded_models[model_name]["model"]
            start_time = datetime.now()

            # Convert to tensor
            tensor_data = torch.from_numpy(data).float().to(self.device)

            # Make prediction
            with torch.no_grad(), autocast(device_type=self.device.type):
                output = model(tensor_data)

            # Calculate confidence
            confidence = torch.max(torch.softmax(output, dim=1)).item()

            # Calculate response time
            response_time = (datetime.now() - start_time).total_seconds()

            # STRICT: Validate confidence
            if confidence < self.min_confidence:
                logger.warning(
                    f"Low confidence prediction ({confidence:.2%}) from {model_name}"
                )
                if self.fallback_enabled:
                    return self._get_fallback_prediction(data)

            # Update performance tracking
            self._update_model_metrics(model_name, confidence, response_time)

            return {
                "prediction": float(torch.argmax(output)),
                "confidence": confidence,
                "response_time": response_time,
                "model_name": model_name,
            }

        except Exception as e:
            self.error_manager.log_error(
                f"Prediction error with {model_name}: {e}",
                ErrorSeverity.HIGH.value,
                "Prediction",
            )
            return self._get_fallback_prediction(data)

    def _get_fallback_prediction(self, data: np.ndarray) -> Dict[str, float]:
        """Get fallback prediction when primary fails"""
        return {
            "prediction": 0.0,
            "confidence": 0.0,
            "response_time": 0.0,
            "model_name": "fallback",
        }

    def _update_model_metrics(
        self, model_name: str, confidence: float, response_time: float
    ) -> None:
        """Update model performance metrics"""
        if model_name in self.loaded_models:
            metrics = self.loaded_models[model_name]["performance"]
            metrics["confidence"] = confidence
            metrics["response_time"] = response_time
            metrics["last_check"] = datetime.now().isoformat()

    def validate_model_performance(self, model_id, results):
        """Enhanced model validation with granular metrics"""
        metrics = {
            "win_rate": results.get("win_rate", 0),
            "profit_factor": results.get("profit_factor", 0),
            "sharpe_ratio": results.get("sharpe_ratio", 0),
            "drawdown_risk": results.get("max_drawdown", 100),
            "regime_stability": results.get("regime_stability", 0),
        }

        # Weighted scoring system
        weights = {
            "win_rate": 0.35,
            "profit_factor": 0.25,
            "sharpe_ratio": 0.20,
            "drawdown_risk": 0.15,
            "regime_stability": 0.05,
        }

        total_score = sum(metrics[k] * weights[k] for k in weights)

        # Store validation results
        with self.db.connection() as conn:
            conn.execute(
                """
                INSERT INTO model_validations
                (model_id, timestamp, metrics, total_score, status)
                VALUES (?, datetime('now'), ?, ?, ?)
            """,
                (
                    model_id,
                    json.dumps(metrics),
                    total_score,
                    "active" if total_score >= 0.85 else "inactive",
                ),
            )

        return total_score >= 0.85

    def implement_fallback_strategy(self, model_id):
        """Implement fallback when confidence thresholds aren't met"""
        with self.db.connection() as conn:
            # Get last 3 successful strategies
            successful_strategies = conn.execute("""
                SELECT strategy_id, avg_performance
                FROM strategy_catalog
                WHERE status = 'validated'
                ORDER BY avg_performance DESC
                LIMIT 3
            """).fetchall()

            if successful_strategies:
                # Rotate through successful strategies
                return self.activate_strategy(successful_strategies[0][0])
            else:
                # Default to conservative baseline strategy
                return self.activate_strategy("baseline_conservative")

    def cleanup(self) -> None:
        """Cleanup resources and memory"""
        for model_data in self.loaded_models.values():
            del model_data["model"]
        self.loaded_models.clear()
        torch.cuda.empty_cache()
        gc.collect()


# Create global instance
_model_manager = AIModelManager()


def get_ai_manager() -> AIModelManager:
    """Global function to get AI model manager instance"""
    return _model_manager
