#!/usr/bin/env python3
"""
CUDA Configuration Script for AlgoTradPro5
Run this script to configure CUDA 11.8 settings across all components
"""
import os
import sys
import json
import logging
import subprocess
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def configure_cuda():
    """Configure CUDA settings across the system"""
    cuda_path = r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8"
    
    if not os.path.exists(cuda_path):
        logger.error(f"CUDA 11.8 not found at: {cuda_path}")
        logger.error("Please install CUDA 11.8 before running this script")
        return False
    
    try:
        # Set environment variables
        os.environ["CUDA_PATH"] = cuda_path
        os.environ["CUDA_HOME"] = cuda_path
        os.environ["PATH"] = os.path.join(cuda_path, "bin") + os.pathsep + os.environ["PATH"]
        
        # Update config.json with CUDA settings
        config_file = Path("freqtrade/config.json")
        if config_file.exists():
            with open(config_file) as f:
                config = json.load(f)
            
            # Update GPU settings
            config["gpu_settings"] = {
                "cuda_version": "11.8",
                "cuda_path": cuda_path,
                "gpu_memory_limit_mb": 8192,
                "use_gpu": True,
                "fallback_to_cpu": True
            }
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            logger.info("✅ Updated config.json with CUDA 11.8 settings")
        
        # Install CUDA-specific packages
        logger.info("Installing CUDA-specific packages...")
        packages = [
            "torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118",
            "cupy-cuda118",
            "pennylane-lightning-gpu"
        ]
        
        for package in packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", *package.split()])
                logger.info(f"✅ Installed {package}")
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Failed to install {package}: {e}")
        
        # Validate CUDA setup
        from validate_cuda import validate_cuda_environment
        results = validate_cuda_environment()
        
        if all(results[key] for key in ['cuda_found', 'environment_valid', 'pytorch_cuda_available']):
            logger.info("✅ CUDA 11.8 configured successfully")
            return True
        else:
            logger.error("❌ CUDA configuration validation failed")
            return False
            
    except Exception as e:
        logger.error(f"Error configuring CUDA: {e}")
        return False

if __name__ == "__main__":
    print("\n=== AlgoTradPro5 CUDA 11.8 Configuration ===\n")
    success = configure_cuda()
    sys.exit(0 if success else 1)