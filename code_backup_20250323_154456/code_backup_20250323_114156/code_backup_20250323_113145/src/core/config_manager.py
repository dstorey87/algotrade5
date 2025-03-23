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
# REMOVED_UNUSED_CODE: from datetime import datetime
from pathlib import Path
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from typing import Any, Dict, List, Optional, Union

import dotenv

logger = logging.getLogger(__name__)


class ConfigManager:
    """Central configuration management system for AlgoTradePro5"""

    def __init__(self, base_path: Optional[Path] = None):
        """Initialize configuration manager"""
        # Base paths
        self.base_path = base_path or Path(os.getenv("BASE_PATH", "C:/AlgoTradPro5"))
        self.config_dir = self.base_path / "config"

        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Load environment variables
        dotenv.load_dotenv(self.base_path / ".env")

        # Configuration storage
        self.global_config = {}
        self.component_configs = {}

        # Load global configuration
        self._load_global_config()

        logger.info(f"ConfigManager initialized with base path: {self.base_path}")

    def _load_global_config(self) -> None:
        """Load global configuration from environment variables"""
        # Load trading parameters
        self.global_config["trading"] = {
            "initial_capital": float(os.getenv("INITIAL_CAPITAL", 10.0)),
            "target_capital": float(os.getenv("TARGET_CAPITAL", 1000.0)),
            "max_days": int(os.getenv("MAX_DAYS", 7)),
            "min_win_rate": float(os.getenv("MIN_WIN_RATE", 0.85)),
            "warning_win_rate": float(os.getenv("WARNING_WIN_RATE", 0.87)),
            "max_drawdown": float(os.getenv("MAX_DRAWDOWN", 0.10)),
            "warning_drawdown": float(os.getenv("WARNING_DRAWDOWN", 0.08)),
            "risk_per_trade": float(os.getenv("RISK_PER_TRADE", 0.02)),
            "min_reward_ratio": float(os.getenv("MIN_REWARD_RATIO", 2.0)),
            "tradable_balance_ratio": float(os.getenv("TRADABLE_BALANCE_RATIO", 0.99)),
        }

        # Load model configuration
        self.global_config["model"] = {
            "min_accuracy": float(os.getenv("MIN_MODEL_ACCURACY", 0.85)),
            "min_confidence": float(os.getenv("MIN_MODEL_CONFIDENCE", 0.85)),
            "max_response_time": float(os.getenv("MAX_RESPONSE_TIME", 0.05)),
            "fallback_enabled": os.getenv("FALLBACK_ENABLED", "true").lower() == "true",
            "model_path": os.getenv("MODEL_PATH", "models/llm/openchat_3.5-GPTQ"),
        }

        # Load paths
        self.global_config["paths"] = {
            "base_path": os.getenv("BASE_PATH", "C:/AlgoTradPro5"),
            "models_dir": os.getenv("MODELS_DIR", "C:/AlgoTradPro5/models"),
            "log_dir": os.getenv("LOG_DIR", "C:/AlgoTradPro5/logs"),
            "data_dir": os.getenv("DATA_DIR", "C:/AlgoTradPro5/data"),
            "backup_dir": os.getenv("BACKUP_DIR", "C:/AlgoTradPro5/backups"),
            "config_path": os.getenv("CONFIG_PATH", "C:/AlgoTradPro5/config.json"),
        }

        # Load FreqAI configuration
        self.global_config["freqai"] = {
            "enabled": os.getenv("FREQAI_ENABLED", "true").lower() == "true",
            "purge_old_models": os.getenv("FREQAI_PURGE_OLD_MODELS", "true").lower()
            == "true",
            "train_period_days": int(os.getenv("FREQAI_TRAIN_PERIOD_DAYS", 30)),
            "backtest_period_days": int(os.getenv("FREQAI_BACKTEST_PERIOD_DAYS", 7)),
            "live_retrain_hours": int(os.getenv("FREQAI_LIVE_RETRAIN_HOURS", 1)),
            "identifier": os.getenv("FREQAI_IDENTIFIER", "quantum"),
            "di_threshold": float(os.getenv("FREQAI_DI_THRESHOLD", 0.9)),
        }

        # Load quantum configuration
        self.global_config["quantum"] = {
            "n_qubits": int(os.getenv("N_QUBITS", 4)),
            "shots": int(os.getenv("QUANTUM_SHOTS", 1000)),
            "shift": float(os.getenv("QUANTUM_SHIFT", 0.1)),
            "max_iterations": int(os.getenv("MAX_QUANTUM_ITERATIONS", 100)),
        }

        # Load database configuration
        self.global_config["database"] = {
            "name": os.getenv("DB_NAME", "algotradepro5"),
            "user": os.getenv("DB_USER", "freqtrade"),
            "password": os.getenv("DB_PASSWORD", "freqtrade123"),
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", 5432)),
            "url": os.getenv("DB_URL", "sqlite:///data/trading.db"),
            "url_dryrun": os.getenv(
                "DB_URL_DRYRUN", "sqlite:///data/tradesv3.dryrun.sqlite"
            ),
        }

        # Load resources configuration
        self.global_config["resources"] = {
            "max_memory_usage": float(os.getenv("MAX_MEMORY_USAGE", 0.90)),
            "max_gpu_memory": float(os.getenv("MAX_GPU_MEMORY", 0.85)),
            "max_cpu_usage": float(os.getenv("MAX_CPU_USAGE", 0.8)),
            "backup_interval": int(os.getenv("BACKUP_INTERVAL", 3600)),
            "health_check_interval": int(os.getenv("HEALTH_CHECK_INTERVAL", 300)),
        }

        # Load notification configuration
        self.global_config["notification"] = {
            "slack_webhook_url": os.getenv("SLACK_WEBHOOK_URL", ""),
            "slack_channel": os.getenv("SLACK_CHANNEL", "#trading-alerts"),
            "email_notifications_enabled": os.getenv(
                "EMAIL_NOTIFICATIONS_ENABLED", "true"
            ).lower()
            == "true",
            "email_smtp_server": os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com"),
            "email_smtp_port": int(os.getenv("EMAIL_SMTP_PORT", 587)),
            "email_from": os.getenv("EMAIL_FROM", ""),
            "email_password": os.getenv("EMAIL_PASSWORD", ""),
        }

        logger.debug("Global configuration loaded from environment variables")

    def load_component_config(self, component_name: str) -> Dict:
        """Load component-specific configuration"""
        if component_name in self.component_configs:
            return self.component_configs[component_name]

        config_file = self.config_dir / f"{component_name}.json"

        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
                    self.component_configs[component_name] = config
                    logger.debug(
                        f"Loaded configuration for component: {component_name}"
                    )
                    return config
            except Exception as e:
                logger.error(
                    f"Error loading component config for {component_name}: {e}"
                )

        # Create default config if it doesn't exist
        default_config = {}
        self.component_configs[component_name] = default_config
        self.save_component_config(component_name, default_config)

        return default_config

    def save_component_config(self, component_name: str, config: Dict) -> bool:
        """Save component-specific configuration"""
        try:
            config_file = self.config_dir / f"{component_name}.json"

            with open(config_file, "w") as f:
                json.dump(config, f, indent=4)

            self.component_configs[component_name] = config
            logger.debug(f"Saved configuration for component: {component_name}")
            return True
        except Exception as e:
            logger.error(f"Error saving component config for {component_name}: {e}")
            return False

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get configuration value from global config"""
        if section in self.global_config and key in self.global_config[section]:
            value = self.global_config[section][key]
            # Handle path values
            if key.endswith("_path") or key.endswith("_dir"):
                return str(value)
            return value
        return default

# REMOVED_UNUSED_CODE:     def get_component_value(self, component: str, key: str, default: Any = None) -> Any:
# REMOVED_UNUSED_CODE:         """Get configuration value from component config"""
# REMOVED_UNUSED_CODE:         component_config = self.load_component_config(component)
# REMOVED_UNUSED_CODE:         return component_config.get(key, default)

# REMOVED_UNUSED_CODE:     def set(self, section: str, key: str, value: Any) -> None:
# REMOVED_UNUSED_CODE:         """Set configuration value in global config"""
# REMOVED_UNUSED_CODE:         if section not in self.global_config:
# REMOVED_UNUSED_CODE:             self.global_config[section] = {}
# REMOVED_UNUSED_CODE:         self.global_config[section][key] = value

# REMOVED_UNUSED_CODE:     def set_component_value(self, component: str, key: str, value: Any) -> None:
# REMOVED_UNUSED_CODE:         """Set configuration value in component config"""
# REMOVED_UNUSED_CODE:         component_config = self.load_component_config(component)
# REMOVED_UNUSED_CODE:         component_config[key] = value
# REMOVED_UNUSED_CODE:         self.save_component_config(component, component_config)

# REMOVED_UNUSED_CODE:     def save_global_config(self) -> bool:
# REMOVED_UNUSED_CODE:         """Save global configuration to file"""
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             config_file = self.config_dir / "global_config.json"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             with open(config_file, "w") as f:
# REMOVED_UNUSED_CODE:                 json.dump(self.global_config, f, indent=4)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             logger.debug("Saved global configuration")
# REMOVED_UNUSED_CODE:             return True
# REMOVED_UNUSED_CODE:         except Exception as e:
# REMOVED_UNUSED_CODE:             logger.error(f"Error saving global config: {e}")
# REMOVED_UNUSED_CODE:             return False

# REMOVED_UNUSED_CODE:     def validate_config(self) -> Dict[str, bool]:
# REMOVED_UNUSED_CODE:         """Validate configuration values"""
# REMOVED_UNUSED_CODE:         validation_results = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Validate trading parameters
# REMOVED_UNUSED_CODE:         validation_results["trading"] = (
# REMOVED_UNUSED_CODE:             self.global_config["trading"]["min_win_rate"] >= 0.5
# REMOVED_UNUSED_CODE:             and self.global_config["trading"]["max_drawdown"] <= 0.2
# REMOVED_UNUSED_CODE:             and self.global_config["trading"]["risk_per_trade"] <= 0.05
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Validate model parameters
# REMOVED_UNUSED_CODE:         validation_results["model"] = (
# REMOVED_UNUSED_CODE:             self.global_config["model"]["min_accuracy"] >= 0.5
# REMOVED_UNUSED_CODE:             and self.global_config["model"]["min_confidence"] >= 0.5
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Validate paths
# REMOVED_UNUSED_CODE:         validation_results["paths"] = all(
# REMOVED_UNUSED_CODE:             Path(p).exists() or Path(p).parent.exists()
# REMOVED_UNUSED_CODE:             for p in self.global_config["paths"].values()
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Overall validation
# REMOVED_UNUSED_CODE:         validation_results["overall"] = all(validation_results.values())
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return validation_results


# Global instance
_config_manager = None


# REMOVED_UNUSED_CODE: def get_config() -> ConfigManager:
# REMOVED_UNUSED_CODE:     """Get global configuration manager instance"""
# REMOVED_UNUSED_CODE:     global _config_manager
# REMOVED_UNUSED_CODE:     if _config_manager is None:
# REMOVED_UNUSED_CODE:         _config_manager = ConfigManager()
# REMOVED_UNUSED_CODE:     return _config_manager
