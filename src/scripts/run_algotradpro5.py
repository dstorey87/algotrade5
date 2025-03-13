#!/usr/bin/env python3
"""
AlgoTradPro5 System Runner
Handles system startup and configuration for quantum-enhanced algorithmic trading
"""
import os
import sys
import logging
import argparse
import json
import asyncio
import time
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def install_core_dependencies():
    """Install core dependency manager and its requirements"""
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "jsonschema", "attrs", "pyrsistent"])
        return True
    except Exception as e:
        logger.error(f"Failed to install core dependencies: {e}")
        return False

def ensure_system_dependencies(components=None):
    """Ensure all system dependencies are installed"""
    try:
        from dependency_manager import ensure_dependencies
        return ensure_dependencies(components=components)
    except ImportError:
        logger.warning("Dependency manager not found, installing core dependencies...")
        if not install_core_dependencies():
            return False
        try:
            from dependency_manager import ensure_dependencies
            return ensure_dependencies(components=components)
        except ImportError:
            logger.error("Failed to import dependency manager even after installation")
            return False

def retry_imports():
    """Retry importing dependencies after installation"""
    try:
        import torch
        import pandas as pd
        import numpy as np
        from freqtrade.main import main
        return True
    except ImportError as e:
        logger.error(f"Failed to import dependencies: {e}")
        return False

# Setup CUDA environment before any GPU imports
sys.path.append(str(Path(__file__).parent))
import setup_env

# Try importing dependencies, install if missing
if not retry_imports():
    logger.info("Installing missing dependencies...")
    if ensure_system_dependencies(components=["quantitative", "ai", "quantum", "api"]):
        if not retry_imports():
            logger.error("Failed to import dependencies even after installation")
            sys.exit(1)
    else:
        logger.error("Failed to install dependencies")
        sys.exit(1)

# Import our custom modules
from freqtrade.freqai.custom_models.ai_model_manager import AIModelManager
from quantum_optimizer import QuantumOptimizer
from gpu_monitor import GPUMonitor

def verify_requirements():
    """Verify system requirements are met"""
    logger.info("Verifying system requirements...")
    requirements_met = True
    
    # Check if Python version is compatible
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 9):
        logger.error(f"Python version {python_version.major}.{python_version.minor} is not supported. Please use Python 3.9+")
        requirements_met = False
    else:
        logger.info(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check for GPU
    if not torch.cuda.is_available():
        logger.warning("CUDA GPU not detected - system will run in CPU mode (very slow)")
        requirements_met = False
    else:
        device_count = torch.cuda.device_count()
        for i in range(device_count):
            device_properties = torch.cuda.get_device_properties(i)
            logger.info(f"GPU {i}: {device_properties.name} ({device_properties.total_memory / 1024**3:.1f}GB)")
    
    # Check for model files
    model_paths = [
        Path("c:/aimodels/phi-2"),
        Path("c:/aimodels/mixtral"),
        Path("c:/aimodels/openchat")
    ]
    
    missing_models = []
    for path in model_paths:
        if not path.exists() or not (path / "config.json").exists():
            missing_models.append(path.name)
    
    if missing_models:
        logger.warning(f"Missing AI models: {', '.join(missing_models)}")
        logger.warning("Run download_models.py first to download the required models")
        requirements_met = False
    else:
        logger.info("All required AI models found")
    
    return requirements_met

async def check_ai_models():
    """Check AI models can be loaded"""
    logger.info("Checking AI models...")
    try:
        ai_manager = AIModelManager(config_path="freqtrade/config.json")
        models_initialized = await ai_manager.initialize_models()
        
        if models_initialized:
            logger.info("✅ AI models initialized successfully")
            await ai_manager.cleanup()
            return True
        else:
            logger.error("❌ Failed to initialize AI models")
            return False
    except Exception as e:
        logger.error(f"Error checking AI models: {e}")
        return False

def check_quantum_optimizer():
    """Check quantum optimizer functionality"""
    logger.info("Checking quantum optimizer...")
    try:
        # Create a simple quantum optimizer
        quantum_opt = QuantumOptimizer(n_qubits=2, shots=100)
        
        # Test with dummy data
        import pandas as pd
        import numpy as np
        
        test_data = pd.DataFrame({
            'open': np.random.random(10) * 100 + 100,
            'high': np.random.random(10) * 10 + 110,
            'low': np.random.random(10) * 10 + 90,
            'close': np.random.random(10) * 100 + 100,
            'volume': np.random.random(10) * 1000 + 1000
        })
        
        # Run a basic test
        result = quantum_opt.analyze_pattern(test_data)
        
        if 'pattern_score' in result and 'confidence' in result:
            logger.info(f"✅ Quantum optimizer working (pattern_score: {result['pattern_score']:.2f}, " 
                        f"confidence: {result['confidence']:.2f})")
            return True
        else:
            logger.error("❌ Quantum optimizer test failed")
            return False
    except Exception as e:
        logger.error(f"Error in quantum optimizer: {e}")
        return False

def check_gpu_monitor():
    """Check GPU monitor functionality"""
    logger.info("Checking GPU monitor...")
    try:
        gpu_monitor = GPUMonitor()
        gpu_info = gpu_monitor.get_gpu_info()
        
        if 'error' in gpu_info:
            logger.warning(f"GPU monitor warning: {gpu_info['error']}")
            return True  # Non-critical, can continue
        else:
            logger.info(f"✅ GPU monitor working ({gpu_info.get('device_name', 'Unknown GPU')})")
            
            # Log memory stats
            memory_stats = gpu_monitor.get_memory_stats()
            if 'allocated' in memory_stats and 'cached' in memory_stats:
                allocated_gb = memory_stats['allocated'] / (1024**3)
                cached_gb = memory_stats['cached'] / (1024**3)
                logger.info(f"GPU Memory: {allocated_gb:.2f}GB allocated, {cached_gb:.2f}GB cached")
            
            return True
    except Exception as e:
        logger.error(f"Error in GPU monitor: {e}")
        return False  # Non-critical, can continue

def verify_config():
    """Verify configuration file"""
    logger.info("Verifying configuration...")
    try:
        # Check if config.json exists
        config_path = Path("freqtrade/config.json")
        if not config_path.exists():
            logger.error(f"Configuration file not found: {config_path}")
            return False
        
        # Load and validate config
        with open(config_path) as f:
            config = json.load(f)
        
        # Check required sections
        required_sections = ['freqai', 'ai_model_config', 'exchange']
        missing_sections = [section for section in required_sections if section not in config]
        
        if missing_sections:
            logger.error(f"Missing required configuration sections: {', '.join(missing_sections)}")
            return False
        
        # Check AI model paths
        if 'ai_model_config' in config:
            for model_name, model_config in config['ai_model_config'].items():
                model_path = Path(model_config['model_path'])
                if not model_path.exists():
                    logger.warning(f"Model path for {model_name} not found: {model_path}")
        
        # Check FreqAI configuration
        if 'freqai' in config and 'model_training_parameters' in config['freqai']:
            if 'quantum_parameters' not in config['freqai']['model_training_parameters']:
                logger.warning("Quantum parameters not found in FreqAI configuration")
        
        logger.info("✅ Configuration validated")
        return True
        
    except Exception as e:
        logger.error(f"Error validating configuration: {e}")
        return False

def run_system(args):
    """Run the full AlgoTradPro5 system"""
    if args.docker:
        return run_with_docker(args)
    else:
        return run_standalone(args)

def run_standalone(args):
    """Run the system in standalone mode"""
    logger.info("Starting AlgoTradPro5 in standalone mode...")
    
    # First check if we need to install any dependencies
    try:
        from dependency_manager import ensure_dependencies
        logger.info("Running dependency check before system start...")
        ensure_dependencies(components=["quantitative", "ai", "quantum", "api"])
    except ImportError:
        logger.warning("Dependency manager not available. Skipping dependency check.")
    
    cmd = ["python", "freqtrade/initialize_system.py"]
    
    logger.info(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    
    # Build freqtrade command based on args
    cmd = ["freqtrade"]
    
    if args.backtesting:
        cmd.extend([
            "backtesting",
            "--strategy", "QuantumHybridStrategy",
            "--config", "freqtrade/config.json",
            "--freqaimodel", "QuantumEnhancedPredictor"
        ])
        
        if args.timerange:
            cmd.extend(["--timerange", args.timerange])
    else:
        cmd.extend([
            "trade",
            "--strategy", "QuantumHybridStrategy",
            "--config", "freqtrade/config.json",
            "--freqaimodel", "QuantumEnhancedPredictor"
        ])
    
    logger.info(f"Running command: {' '.join(cmd)}")
    
    try:
        return subprocess.run(cmd, check=True).returncode == 0
    except subprocess.CalledProcessError:
        logger.error("Error executing freqtrade command")
        return False

def run_with_docker(args):
    """Run the system using Docker"""
    logger.info("Starting AlgoTradPro5 using Docker...")
    
    docker_file = "docker-compose.analysis.yml" if args.backtesting else "docker-compose.yml"
    
    # Check if docker-compose.yml exists
    if not Path(docker_file).exists() and docker_file == "docker-compose.yml":
        logger.info("docker-compose.yml not found, using docker-compose.analysis.yml")
        docker_file = "docker-compose.analysis.yml"
        
    # Check if the selected docker-compose file exists
    if not Path(docker_file).exists():
        logger.error(f"Docker compose file not found: {docker_file}")
        return False
        
    # Build the Docker containers
    logger.info(f"Building Docker containers from {docker_file}")
    cmd = ["docker-compose", "-f", docker_file, "build"]
    
    try:
        if subprocess.run(cmd, check=True).returncode != 0:
            logger.error("Error building Docker containers")
            return False
    except subprocess.CalledProcessError:
        logger.error("Error executing docker-compose build command")
        return False
        
    # Start the Docker containers
    logger.info("Starting Docker containers")
    
    service = "freqtrade-backtest" if args.backtesting else "freqtrade-analysis"
    cmd = ["docker-compose", "-f", docker_file, "up", "-d", service]
    
    try:
        if subprocess.run(cmd, check=True).returncode != 0:
            logger.error("Error starting Docker containers")
            return False
    except subprocess.CalledProcessError:
        logger.error("Error executing docker-compose up command")
        return False
        
    logger.info(f"Docker containers started. Service: {service}")
    
    # Follow logs if requested
    if args.logs:
        cmd = ["docker-compose", "-f", docker_file, "logs", "-f", service]
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            logger.info("Log viewing interrupted")
    
    return True

def setup_argparse():
    """Set up command-line argument parsing"""
    parser = argparse.ArgumentParser(description='AlgoTradPro5 System Runner')
    
    # Add mutually exclusive mode group
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--verify-only', action='store_true', 
                          help='Only verify requirements without running')
    mode_group.add_argument('--docker', action='store_true',
                          help='Run using Docker instead of standalone mode')
    mode_group.add_argument('--backtesting', action='store_true',
                          help='Run in backtesting mode')
    
    # Additional options
    parser.add_argument('--skip-checks', action='store_true',
                       help='Skip verification checks')
    parser.add_argument('--timerange', type=str,
                       help='Timerange for backtesting (format: YYYYMMDD-YYYYMMDD)')
    parser.add_argument('--logs', action='store_true',
                       help='Follow Docker logs after startup')
    parser.add_argument('--install-deps', action='store_true',
                       help='Force installation of dependencies before running')
    
    return parser.parse_args()

async def main():
    """Main entry point"""
    print("\n" + "=" * 80)
    print("AlgoTradPro5 - Quantum-Enhanced Trading System".center(80))
    print("=" * 80 + "\n")
    
    args = setup_argparse()
    
    # Force dependency installation if requested
    if args.install_deps:
        try:
            logger.info("Installing dependencies as requested...")
            subprocess.check_call([sys.executable, "dependency_manager.py"])
        except Exception as e:
            logger.error(f"Error installing dependencies: {e}")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                return False
    
    # Skip verification if requested
    if not args.skip_checks:
        # Verify requirements first
        if not verify_requirements():
            logger.warning("Some system requirements are not met.")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                logger.info("Exiting due to unmet requirements.")
                return False
        
        # Verify configuration
        if not verify_config():
            logger.warning("Configuration verification failed.")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                logger.info("Exiting due to configuration issues.")
                return False
        
        # Check quantum optimizer
        if not check_quantum_optimizer():
            logger.warning("Quantum optimizer check failed.")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                logger.info("Exiting due to quantum optimizer issues.")
                return False
        
        # Check GPU monitor
        check_gpu_monitor()  # Non-critical, continue regardless
        
        # Check AI models
        if not await check_ai_models():
            logger.warning("AI model check failed.")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                logger.info("Exiting due to AI model issues.")
                return False
    else:
        logger.info("Skipping verification checks as requested")
    
    # Exit if only verification was requested
    if args.verify_only:
        logger.info("Verification completed. Exiting as requested (--verify-only).")
        return True
    
    # Run the system
    success = run_system(args)
    return success

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\nAlgoTradPro5 execution interrupted by user.")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        sys.exit(1)