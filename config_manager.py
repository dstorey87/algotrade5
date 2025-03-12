#!/usr/bin/env python3
"""Configuration manager for AlgoTradPro5"""
import os
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigManager:
    def __init__(self, config_path: str = None):
        """Initialize ConfigManager with optional custom config path"""
        self.config_path = config_path or os.path.join('freqtrade', 'config.json')
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            logger.info("Configuration loaded successfully")
            return config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}
            
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        Example: get('freqai.model_type')
        """
        try:
            value = self.config
            for key in key_path.split('.'):
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
            
    def get_model_path(self, model_type: str) -> Optional[str]:
        """Get AI model path from configuration"""
        try:
            model_config = self.config.get('ai_model_config', {}).get(model_type, {})
            model_path = model_config.get('model_path')
            
            if model_path:
                # Convert to absolute path if relative
                if not os.path.isabs(model_path):
                    model_path = os.path.join(os.path.dirname(self.config_path), '..', model_path)
                
                # Check if the model file exists
                if os.path.exists(model_path):
                    logger.info(f"Found model at {model_path}")
                    return model_path
                else:
                    # Try to find alternative formats
                    directory = os.path.dirname(model_path)
                    basename = os.path.splitext(os.path.basename(model_path))[0]
                    
                    # Check if Python script with same name exists
                    py_path = os.path.join(directory, f"{basename}.py")
                    if os.path.exists(py_path):
                        logger.info(f"Model file {model_path} not found, using Python script {py_path} instead")
                        return py_path
                    
                    logger.warning(f"Model file not found: {model_path} and no alternative exists")
            
            return None
        except Exception as e:
            logger.error(f"Error getting model path for {model_type}: {e}")
            return None
            
    def validate(self) -> bool:
        """Validate configuration"""
        try:
            required_sections = ['freqai', 'ai_model_config', 'exchange']
            for section in required_sections:
                if section not in self.config:
                    logger.error(f"Missing required config section: {section}")
                    return False
                    
            # Check model paths
            model_types = ['regime', 'pattern', 'trend']
            for model_type in model_types:
                path = self.get_model_path(model_type)
                if not path:
                    logger.warning(f"Model path not configured for {model_type}")
                elif not os.path.exists(path):
                    logger.warning(f"Model file not found: {path}")
                    
            logger.info("Configuration validated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error validating config: {e}")
            return False
            
    def set(self, key_path: str, value: Any) -> None:
        """Set configuration value using dot notation"""
        try:
            keys = key_path.split('.')
            config_ref = self.config
            
            # Navigate to the appropriate level
            for key in keys[:-1]:
                if key not in config_ref:
                    config_ref[key] = {}
                config_ref = config_ref[key]
                
            # Set the value
            config_ref[keys[-1]] = value
            logger.debug(f"Set {key_path} = {value}")
            
        except Exception as e:
            logger.error(f"Error setting config value {key_path}: {e}")

if __name__ == "__main__":
    # Test the configuration manager
    config = ConfigManager()
    
    # Validate configuration
    if config.validate():
        print("\nCurrent configuration:")
        print(json.dumps(config.config, indent=2))
    else:
        print("\nConfiguration validation failed")
        
    # Test setting and getting values
    config.set("trading.stake_amount", 20.0)
    stake_amount = config.get("trading.stake_amount")
    print(f"\nUpdated stake amount: {stake_amount}")