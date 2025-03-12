#!/usr/bin/env python3
"""
Environment setup script for AlgoTradPro5
Must be imported before any other modules that use CUDA
"""
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_cuda_environment():
    """Setup CUDA environment variables"""
    cuda_path = r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8"
    
    if os.path.exists(cuda_path):
        # Set CUDA environment variables
        os.environ["CUDA_PATH"] = cuda_path
        os.environ["CUDA_HOME"] = cuda_path
        
        # Update PATH to include CUDA bin
        cuda_bin = os.path.join(cuda_path, "bin")
        if cuda_bin not in os.environ["PATH"].split(os.pathsep):
            os.environ["PATH"] = cuda_bin + os.pathsep + os.environ["PATH"]
        
        logger.info(f"CUDA environment configured for version 11.8")
        return True
    else:
        logger.error(f"CUDA 11.8 not found at: {cuda_path}")
        return False

# Set up environment when module is imported
setup_cuda_environment()