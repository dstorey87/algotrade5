#!/usr/bin/env python3
"""System initialization and validation for AlgoTradPro5"""
import os
import sys
import logging
import subprocess
from pathlib import Path

# Set up basic logging first
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def install_core_dependency_manager():
    """Install the core dependency manager if not present"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "jsonschema", "attrs", "pyrsistent"])
        return True
    except Exception as e:
        logger.error(f"Failed to install core dependency manager: {e}")
        return False

def ensure_dependencies():
    """Ensure all required dependencies are installed"""
    try:
        from dependency_manager import ensure_dependencies
        return ensure_dependencies(components=["quantitative", "ai", "quantum", "api"])
    except ImportError:
        logger.warning("Dependency manager not found, installing...")
        if not install_core_dependency_manager():
            return False
        try:
            from dependency_manager import ensure_dependencies
            return ensure_dependencies(components=["quantitative", "ai", "quantum", "api"])
        except ImportError:
            logger.error("Failed to import dependency manager even after installation")
            return False

def retry_imports():
    """Try importing required modules, return True if all succeed"""
    try:
        import torch
        import pennylane as qml
        from gpu_monitor import GPUMonitor
        from freqtrade.main import main
        return True
    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        return False

def install_freqtrade_dependencies():
    """Install FreqTrade and its dependencies"""
    try:
        import subprocess
        # Install FreqTrade's dependencies first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "freqtrade"])
        
        # Now ensure our custom components are available
        from dependency_manager import ensure_dependencies
        return ensure_dependencies(components=["quantitative", "api"])
    except Exception as e:
        logger.error(f"Failed to install FreqTrade dependencies: {e}")
        return False

def retry_freqtrade_imports():
    """Retry importing FreqTrade dependencies"""
    try:
        from freqtrade.main import main
        from freqtrade.commands import Arguments
        from freqtrade.configuration import Configuration
        return True
    except ImportError as e:
        logger.error(f"Failed to import FreqTrade dependencies: {e}")
        return False

def initialize_system():
    """Initialize the AlgoTradPro5 system"""
    try:
        # First ensure FreqTrade dependencies are available
        logger.info("Checking FreqTrade dependencies...")
        if not retry_freqtrade_imports():
            if not install_freqtrade_dependencies():
                logger.error("Failed to install FreqTrade dependencies")
                return False
            if not retry_freqtrade_imports():
                logger.error("Failed to import FreqTrade dependencies even after installation")
                return False

        # Now ensure all other dependencies are available
        logger.info("Checking and installing other dependencies...")
        if not retry_imports():
            if not ensure_dependencies():
                logger.error("Failed to install required dependencies")
                return False
            if not retry_imports():
                logger.error("Failed to import dependencies even after installation")
                return False

        # Initialize GPU monitoring
        try:
            from gpu_monitor import GPUMonitor
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
            from ai_model_manager import AIModelManager
            ai_manager = AIModelManager(config_path="freqtrade/config.json")
            logger.info("AI model manager initialized")
        except Exception as e:
            logger.error(f"Failed to initialize AI model manager: {e}")
            return False

        # Initialize FreqTrade components
        try:
            from freqtrade.commands import Arguments
            from freqtrade.configuration import Configuration
            
            # Load FreqTrade configuration
            config = Configuration.from_files(['freqtrade/config.json'])
            
            # Initialize databases
            logger.info("Initializing databases...")
            for db_path in ['user_data/trading.db', 'user_data/analysis.db', 'user_data/catalog.db']:
                db_file = Path(db_path)
                db_file.parent.mkdir(parents=True, exist_ok=True)
                if not db_file.exists():
                    db_file.touch()
                    logger.info(f"Created database: {db_path}")
            
            logger.info("FreqTrade components initialized")
        except Exception as e:
            logger.error(f"Failed to initialize FreqTrade components: {e}")
            return False

        logger.info("System initialization completed successfully!")
        return True

    except Exception as e:
        logger.error(f"System initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = initialize_system()
    sys.exit(0 if success else 1)