#!/usr/bin/env python3
"""
Package installer for AlgoTradPro5
Now delegates to dependency_manager.py while maintaining backward compatibility
"""
import subprocess
import sys
import os
import logging
from pathlib import Path
import platform
import json
import shutil

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_gpu_availability():
    """Check for CUDA-capable GPU"""
    try:
        import torch
        gpu_available = torch.cuda.is_available()
        if gpu_available:
            gpu_name = torch.cuda.get_device_name(0)
            logger.info(f"GPU detected: {gpu_name}")
            return True
        else:
            logger.warning("No CUDA-capable GPU detected")
            return False
    except ImportError:
        logger.warning("PyTorch not installed yet")
        return False

def setup_environment():
    """Setup environment variables for GPU and quantum computing"""
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1'
    os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'
    if platform.system() == 'Windows':
        os.environ['PATH'] = os.environ['PATH'] + ';C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.8\\bin'

def check_python_version():
    """Verify Python version is compatible"""
    if sys.version_info < (3, 9):
        logger.error("Python 3.9 or higher is required")
        sys.exit(1)

def setup_freqai_environment():
    """Setup FreqAI environment and copy necessary files"""
    try:
        base_path = Path(__file__).parent
        freqtrade_path = base_path / "freqtrade"
        
        # Define critical paths
        paths = [
            base_path / "user_data" / "models",
            base_path / "user_data" / "strategies",
            base_path / "user_data" / "freqaimodels",
            freqtrade_path / "freqai" / "prediction_models",
        ]
        
        # Create directories
        for path in paths:
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {path}")
        
        # Define source and destination paths for strategy files
        file_mapping = [
            (
                freqtrade_path / "user_data" / "strategies" / "QuantumHybridStrategy.py",
                base_path / "user_data" / "strategies" / "QuantumHybridStrategy.py"
            ),
            (
                freqtrade_path / "freqai" / "prediction_models" / "QuantumEnhancedPredictor.py",
                base_path / "user_data" / "freqaimodels" / "QuantumEnhancedPredictor.py"
            ),
            (
                base_path / "quantum_optimizer.py",
                freqtrade_path / "quantum_optimizer.py"
            )
        ]
        
        # Copy files with proper path handling
        for src_path, dest_path in file_mapping:
            if src_path.exists():
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dest_path)
                logger.info(f"Copied {src_path.name} to {dest_path.parent}")
            else:
                logger.warning(f"Source file not found: {src_path}")
        
        logger.info("FreqAI environment setup completed")
        
    except Exception as e:
        logger.error(f"Error setting up FreqAI environment: {e}")
        sys.exit(1)

def use_dependency_manager(components=None):
    """Use the dependency manager if available"""
    if os.path.exists(os.path.join(os.path.dirname(__file__), "dependency_manager.py")):
        try:
            logger.info("Using dependency manager for package installation")
            
            # Try to import and use it directly
            try:
                sys.path.append(os.path.dirname(__file__))
                from dependency_manager import ensure_dependencies
                
                # Install all components if none specified
                if components is None:
                    components = ["quantitative", "ai", "quantum", "api"]
                
                success = ensure_dependencies(components=components)
                if success:
                    logger.info("Dependencies successfully installed via dependency manager")
                    return True
                else:
                    logger.warning("Some dependencies could not be installed")
                    return False
                    
            except ImportError:
                # Fall back to command-line execution
                logger.info("Executing dependency manager via command line")
                cmd = [sys.executable, "dependency_manager.py"]
                
                if components:
                    cmd.extend(["--components", ",".join(components)])
                
                result = subprocess.run(cmd, check=False)
                if result.returncode == 0:
                    logger.info("Dependencies successfully installed via dependency manager")
                    return True
                else:
                    logger.warning("Some dependencies could not be installed")
                    return False
        except Exception as e:
            logger.error(f"Error using dependency manager: {e}")
            return False
    else:
        logger.warning("dependency_manager.py not found, falling back to legacy installation")
        return False

def legacy_install_dependencies():
    """Install dependencies using the legacy method (requirements files)"""
    logger.info("Using legacy dependency installation")
    
    # Install core dependencies first
    essential_packages = [
        "jsonschema",
        "SQLAlchemy==1.4.48",  # FreqTrade requires this specific version
        "python-telegram-bot==13.15",
        "pandas",
        "numpy",
        "scikit-learn",
        "python-rapidjson",
        "joblib",
        "rich",
        "pyaml",
        "ccxt",
        "arrow",
        "tables",
        "flask",
        "requests",
        "typing_extensions",
        "packaging",
        "pandas-ta>=0.3.0"  # Added pandas-ta for technical analysis
    ]
    
    for package in essential_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            logger.info(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install {package}: {e}")
    
    # Install CUDA dependencies
    try:
        import torch
        if not torch.cuda.is_available() and platform.system() == 'Windows':
            logger.warning("CUDA not detected. Installing CUDA toolkit...")
            # Download and install CUDA toolkit
            subprocess.check_call([sys.executable, "-m", "pip", "install", "cuda-python"])
    except ImportError:
        # Install PyTorch with CUDA
        if platform.system() == 'Windows':
            subprocess.check_call([sys.executable, "-m", "pip", "install", "torch", "torchvision", "torchaudio"])
        else:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cu118"])
    
    # Install from requirements files
    requirement_files = [
        "requirements.txt",
        "requirements-full.txt",
    ]
    
    for req_file in requirement_files:
        if os.path.exists(req_file):
            logger.info(f"Installing requirements from {req_file}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
            except subprocess.CalledProcessError as e:
                logger.error(f"Error installing {req_file}: {e}")
    
    return True

def main():
    """Main installation process"""
    try:
        logger.info("Starting AlgoTradPro5 installation...")
        
        check_python_version()
        setup_environment()
        
        if check_gpu_availability():
            logger.info("GPU support will be enabled")
        else:
            logger.warning("Running in CPU-only mode")
        
        # Try to use the dependency manager first
        if use_dependency_manager():
            logger.info("Dependencies installed via dependency manager")
        else:
            # Fall back to legacy installation if dependency manager fails
            logger.info("Falling back to legacy installation method")
            legacy_install_dependencies()
        
        # Setup FreqAI environment (both methods need this)
        setup_freqai_environment()
        
        logger.info("Installation completed successfully!")
        logger.info("You can now run 'python run_algotradpro5.py' to start the system")
        
    except KeyboardInterrupt:
        logger.info("\nInstallation interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()