"""
Configuration management for AlgoTradePro5.
Handles loading, validation, and access to configuration settings.
"""
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

class ConfigManager:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.getenv('CONFIG_PATH', 'config.json')
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from the config file."""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in configuration file: {self.config_path}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key."""
        return self.config.get(key, default)

    def validate(self) -> bool:
        """Validate the configuration."""
        required_keys = ['max_open_trades', 'stake_currency', 'stake_amount']
        return all(key in self.config for key in required_keys)

    def save(self) -> None:
        """Save current configuration to file."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def update(self, updates: Dict[str, Any]) -> None:
        """Update configuration with new values."""
        self.config.update(updates)
        self.save()