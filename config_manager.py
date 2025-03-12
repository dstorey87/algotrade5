#!/usr/bin/env python3
"""Configuration manager for AlgoTradPro5 using FreqTrade's configuration system"""
import os
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional
from freqtrade.configuration import Configuration
from freqtrade.configuration.load_config import load_config_file
from freqtrade.loggers import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

class ConfigManager:
    """Enhanced configuration manager using FreqTrade's system"""
    
    def __init__(self, config_files: list = None):
        """Initialize with optional list of config files"""
        self.config_files = config_files or ['freqtrade/config.json']
        self._load_configuration()
    
    def _load_configuration(self):
        """Load configuration using FreqTrade's system"""
        try:
            # Use FreqTrade's configuration system
            self.config = Configuration.from_files(self.config_files)
            
            # Add our custom validations
            self._validate_quantum_config()
            logger.info("Configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self.config = {}
    
    def _validate_quantum_config(self):
        """Validate quantum-specific configuration"""
        freqai_config = self.config.get('freqai', {})
        if not freqai_config.get('enabled', False):
            logger.warning("FreqAI is not enabled in configuration")
            
        model_params = freqai_config.get('model_training_parameters', {})
        if 'quantum_parameters' not in model_params:
            logger.warning("Quantum parameters not found in FreqAI configuration")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation with FreqTrade's getter"""
        try:
            return self.config.get(key_path, default)
        except Exception:
            return default
    
    def get_config(self) -> Dict:
        """Get full configuration"""
        return self.config
    
    def get_exchange_config(self) -> Dict:
        """Get exchange-specific configuration"""
        return self.config.get('exchange', {})
    
    def get_freqai_config(self) -> Dict:
        """Get FreqAI-specific configuration"""
        return self.config.get('freqai', {})
    
    def validate(self) -> bool:
        """Validate configuration"""
        try:
            # Use FreqTrade's validation
            self.config.validate()
            
            # Additional custom validations
            required_sections = ['freqai', 'exchange']
            for section in required_sections:
                if section not in self.config:
                    logger.error(f"Missing required config section: {section}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False

# Global instance
_config_manager = None

def get_config_manager(config_files: list = None) -> ConfigManager:
    """Get or create the global configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_files)
    return _config_manager

if __name__ == "__main__":
    # Test the configuration manager
    config_mgr = get_config_manager()
    
    if config_mgr.validate():
        print("\nConfiguration validated successfully")
        print("\nFreqAI Configuration:")
        print(json.dumps(config_mgr.get_freqai_config(), indent=2))
    else:
        print("\nConfiguration validation failed")