#!/usr/bin/env python3
"""System initialization and validation for AlgoTradPro5"""
import os
import sys
import logging
from pathlib import Path

from freqtrade.configuration import Configuration
from freqtrade.configuration.directory_operations import create_userdata_dir
from freqtrade.loggers import setup_logging
from system_health_checker import check_system_health
from gpu_monitor import GPUMonitor

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

def ensure_configuration():
    """Ensure configuration exists and is valid"""
    try:
        config_path = Path("freqtrade/config.json")
        if not config_path.exists():
            logger.info("Configuration not found, generating from template...")
            from setup_config import setup_configuration
            setup_configuration()
        
        # Load and validate configuration
        config = Configuration.from_files([str(config_path)])
        config.validate()
        return True
        
    except Exception as e:
        logger.error(f"Configuration error: {e}")
        return False

def initialize_system():
    """Initialize the AlgoTradPro5 system"""
    try:
        # Check system health and documentation
        logger.info("Checking system health and documentation...")
        if not check_system_health():
            return False

        # Ensure configuration is valid
        logger.info("Validating configuration...")
        if not ensure_configuration():
            return False

        # Initialize GPU monitoring
        try:
            gpu_monitor = GPUMonitor()
            gpu_info = gpu_monitor.get_gpu_info()
            if 'error' not in gpu_info:
                logger.info(f"GPU initialized: {gpu_info.get('device_name', 'Unknown GPU')}")
            else:
                logger.warning(f"GPU monitoring issue: {gpu_info['error']}")
        except Exception as e:
            logger.warning(f"GPU monitoring not available: {e}")

        # Initialize quantum backend
        try:
            import pennylane as qml
            dev = qml.device('default.qubit', wires=4)
            logger.info("Quantum computing backend initialized")
        except Exception as e:
            logger.error(f"Failed to initialize quantum backend: {e}")
            return False

        # Initialize AI model manager
        try:
            from freqtrade.freqai.freqai_interface import IFreqaiModel
            logger.info("FreqAI system initialized")
        except Exception as e:
            logger.error(f"Failed to initialize AI system: {e}")
            return False

        # Initialize databases
        try:
            create_userdata_dir("freqtrade", "user_data")
            logger.info("Database directories initialized")
        except Exception as e:
            logger.error(f"Failed to initialize databases: {e}")
            return False

        logger.info("System initialization completed successfully!")
        return True

    except Exception as e:
        logger.error(f"System initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = initialize_system()
    sys.exit(0 if success else 1)