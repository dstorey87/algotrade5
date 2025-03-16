"""
Configuration Manager
==================

Unified configuration management for AlgoTradePro5.

CRITICAL REQUIREMENTS:
- Environment variable mapping
- Parameter validation
- Real-time updates
- Version tracking
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import dotenv

logger = logging.getLogger(__name__)


class ConfigManager:
    def __init__(self, base_path: Optional[Path] = None):
        """Initialize configuration manager"""
        self.base_path = base_path or Path("C:/AlgoTradPro5")

        # Load environment variables
        self._load_env_vars()

        # Trading parameters
        self.trading_params = {
            "initial_capital": 10.0,  # £10 starting capital
            "target_capital": 1000.0,  # £1000 target
            "max_days": 7,  # 7-day target timeframe
            "min_win_rate": 0.85,  # STRICT: 85% minimum
            "max_drawdown": 0.10,  # 10% maximum drawdown
            "risk_per_trade": 0.02,  # 2% maximum risk per trade
            "min_reward_ratio": 2.0,  # Minimum 2:1 reward/risk
        }

        # Model parameters
        self.model_params = {
            "llm": {
                "min_confidence": 0.85,
                "max_refinement_steps": 5,
                "improvement_threshold": 0.02,
                "model_path": "models/llm/openchat_3.5-GPTQ",
            },
            "quantum": {
                "n_qubits": 4,
                "shots": 1000,
                "min_confidence": 0.85,
                "use_gpu": True,
            },
        }

        # System parameters
        self.system_params = {
            "log_level": "INFO",
            "max_cpu_usage": 0.8,
            "max_gpu_usage": 0.9,
            "backup_interval": 3600,  # 1 hour
            "health_check_interval": 300,  # 5 minutes
        }

        # Load and validate configuration
        self.load_config()
        self._validate_config()

    def _load_env_vars(self) -> None:
        """Load environment variables from .env file"""
        try:
            env_path = self.base_path / ".env"
            if env_path.exists():
                dotenv.load_dotenv(env_path)
            else:
                self._create_default_env()

        except Exception as e:
            logger.error(f"Failed to load environment variables: {e}")
            raise

    def _create_default_env(self) -> None:
        """Create default .env file"""
        try:
            env_path = self.base_path / ".env"

            default_vars = {
                "INITIAL_CAPITAL": "10.0",
                "TARGET_CAPITAL": "1000.0",
                "MAX_DAYS": "7",
                "MIN_WIN_RATE": "0.85",
                "MAX_DRAWDOWN": "0.10",
                "RISK_PER_TRADE": "0.02",
                "MIN_REWARD_RATIO": "2.0",
                "LOG_LEVEL": "INFO",
            }

            with open(env_path, "w") as f:
                for key, value in default_vars.items():
                    f.write(f"{key}={value}\n")

        except Exception as e:
            logger.error(f"Failed to create default .env file: {e}")
            raise

    def load_config(self) -> None:
        """Load configuration from files"""
        try:
            # Load trading parameters from env
            self.trading_params.update(
                {
                    "initial_capital": float(os.getenv("INITIAL_CAPITAL", "10.0")),
                    "target_capital": float(os.getenv("TARGET_CAPITAL", "1000.0")),
                    "max_days": int(os.getenv("MAX_DAYS", "7")),
                    "min_win_rate": float(os.getenv("MIN_WIN_RATE", "0.85")),
                    "max_drawdown": float(os.getenv("MAX_DRAWDOWN", "0.10")),
                    "risk_per_trade": float(os.getenv("RISK_PER_TRADE", "0.02")),
                    "min_reward_ratio": float(os.getenv("MIN_REWARD_RATIO", "2.0")),
                }
            )

            # Load custom configurations
            config_path = self.base_path / "config"

            if (config_path / "model_config.json").exists():
                with open(config_path / "model_config.json", "r") as f:
                    self.model_params.update(json.load(f))

            if (config_path / "system_config.json").exists():
                with open(config_path / "system_config.json", "r") as f:
                    self.system_params.update(json.load(f))

        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise

    def save_config(self) -> None:
        """Save configuration to files"""
        try:
            config_path = self.base_path / "config"
            config_path.mkdir(parents=True, exist_ok=True)

            # Save model configuration
            with open(config_path / "model_config.json", "w") as f:
                json.dump(self.model_params, f, indent=4)

            # Save system configuration
            with open(config_path / "system_config.json", "w") as f:
                json.dump(self.system_params, f, indent=4)

            # Create backup
            backup_path = config_path / "backups"
            backup_path.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            with open(backup_path / f"config_backup_{timestamp}.json", "w") as f:
                json.dump(
                    {
                        "trading_params": self.trading_params,
                        "model_params": self.model_params,
                        "system_params": self.system_params,
                        "timestamp": datetime.now().isoformat(),
                    },
                    f,
                    indent=4,
                )

        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            raise

    def _validate_config(self) -> None:
        """Validate configuration parameters"""
        try:
            # Validate trading parameters
            if self.trading_params["initial_capital"] <= 0:
                raise ValueError("Initial capital must be positive")

            if (
                self.trading_params["target_capital"]
                <= self.trading_params["initial_capital"]
            ):
                raise ValueError("Target capital must be greater than initial capital")

            if not 0 < self.trading_params["min_win_rate"] <= 1:
                raise ValueError("Win rate must be between 0 and 1")

            if not 0 < self.trading_params["risk_per_trade"] <= 0.02:
                raise ValueError("Risk per trade cannot exceed 2%")

            # Validate model parameters
            if self.model_params["quantum"]["n_qubits"] < 2:
                raise ValueError("Quantum circuit needs at least 2 qubits")

            if self.model_params["quantum"]["shots"] < 100:
                raise ValueError("Quantum simulation needs at least 100 shots")

            if not 0 < self.model_params["llm"]["min_confidence"] <= 1:
                raise ValueError("LLM confidence must be between 0 and 1")

            # Validate system parameters
            if not 0 < self.system_params["max_cpu_usage"] <= 1:
                raise ValueError("CPU usage limit must be between 0 and 1")

            if not 0 < self.system_params["max_gpu_usage"] <= 1:
                raise ValueError("GPU usage limit must be between 0 and 1")

        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            raise

    def get_trading_param(self, param_name: str) -> Any:
        """Get trading parameter value"""
        return self.trading_params.get(param_name)

    def get_model_param(self, model_type: str, param_name: str) -> Any:
        """Get model parameter value"""
        return self.model_params.get(model_type, {}).get(param_name)

    def get_system_param(self, param_name: str) -> Any:
        """Get system parameter value"""
        return self.system_params.get(param_name)

    def update_trading_param(self, param_name: str, value: Any) -> None:
        """Update trading parameter"""
        try:
            if param_name not in self.trading_params:
                raise ValueError(f"Invalid trading parameter: {param_name}")

            # Validate critical parameters
            if param_name == "risk_per_trade" and value > 0.02:
                raise ValueError("Risk per trade cannot exceed 2%")

            if param_name == "min_win_rate" and value < 0.85:
                raise ValueError("Win rate cannot be below 85%")

            # Update parameter
            self.trading_params[param_name] = value

            # Save configuration
            self.save_config()

        except Exception as e:
            logger.error(f"Failed to update trading parameter: {e}")
            raise

    def update_model_param(self, model_type: str, param_name: str, value: Any) -> None:
        """Update model parameter"""
        try:
            if model_type not in self.model_params:
                raise ValueError(f"Invalid model type: {model_type}")

            if param_name not in self.model_params[model_type]:
                raise ValueError(f"Invalid parameter for {model_type}: {param_name}")

            # Validate critical parameters
            if param_name == "min_confidence" and value < 0.85:
                raise ValueError("Confidence threshold cannot be below 85%")

            # Update parameter
            self.model_params[model_type][param_name] = value

            # Save configuration
            self.save_config()

        except Exception as e:
            logger.error(f"Failed to update model parameter: {e}")
            raise

    def update_system_param(self, param_name: str, value: Any) -> None:
        """Update system parameter"""
        try:
            if param_name not in self.system_params:
                raise ValueError(f"Invalid system parameter: {param_name}")

            # Update parameter
            self.system_params[param_name] = value

            # Save configuration
            self.save_config()

        except Exception as e:
            logger.error(f"Failed to update system parameter: {e}")
            raise
