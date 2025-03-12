#!/usr/bin/env python3
"""CUDA Environment Validation for AlgoTradPro5"""
import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_cuda_environment():
    """Validate CUDA environment setup"""
    cuda_path = r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8"
    validation_results = {
        'cuda_found': False,
        'environment_valid': False,
        'torch_gpu': False,
        'pytorch_cuda_available': False,
        'cupy_available': False,
        'quantum_gpu': False
    }
    
    try:
        # Check CUDA installation
        if os.path.exists(cuda_path):
            validation_results['cuda_found'] = True
            logger.info(f"✅ CUDA 11.8 found at: {cuda_path}")
        else:
            logger.error(f"❌ CUDA 11.8 not found at: {cuda_path}")
            return validation_results
            
        # Validate environment variables
        cuda_env_valid = True
        if os.environ.get('CUDA_PATH') != cuda_path:
            logger.error(f"❌ CUDA_PATH not set correctly. Expected: {cuda_path}")
            cuda_env_valid = False
        if os.environ.get('CUDA_HOME') != cuda_path:
            logger.error(f"❌ CUDA_HOME not set correctly. Expected: {cuda_path}")
            cuda_env_valid = False
            
        cuda_bin = os.path.join(cuda_path, 'bin')
        if cuda_bin not in os.environ['PATH']:
            logger.error(f"❌ CUDA bin directory not in PATH: {cuda_bin}")
            cuda_env_valid = False
            
        validation_results['environment_valid'] = cuda_env_valid
        if cuda_env_valid:
            logger.info("✅ CUDA environment variables correctly set")
            
        # Check PyTorch GPU support
        try:
            import torch
            validation_results['torch_gpu'] = True
            if torch.cuda.is_available():
                validation_results['pytorch_cuda_available'] = True
                device_name = torch.cuda.get_device_name(0)
                logger.info(f"✅ PyTorch GPU available: {device_name}")
                logger.info(f"   CUDA Version: {torch.version.cuda}")
            else:
                logger.warning("⚠️ PyTorch installed but CUDA not available")
        except ImportError:
            logger.error("❌ PyTorch not installed")
            
        # Check CuPy
        try:
            import cupy
            validation_results['cupy_available'] = True
            logger.info(f"✅ CuPy available with CUDA {cupy.cuda.runtime.runtimeGetVersion()}")
        except ImportError:
            logger.error("❌ CuPy not installed")
        except Exception as e:
            logger.error(f"❌ CuPy error: {str(e)}")
            
        # Check Quantum GPU support
        try:
            import pennylane as qml
            try:
                dev = qml.device('lightning.gpu', wires=2)
                validation_results['quantum_gpu'] = True
                logger.info("✅ Quantum GPU support available")
            except Exception as e:
                logger.warning(f"⚠️ Quantum GPU device not available: {str(e)}")
        except ImportError:
            logger.error("❌ PennyLane not installed")
            
    except Exception as e:
        logger.error(f"Error during validation: {str(e)}")
        
    return validation_results

def main():
    """Main validation function"""
    logger.info("\nValidating CUDA Environment for AlgoTradPro5...")
    results = validate_cuda_environment()
    
    # Print summary
    print("\nValidation Summary:")
    print("==================")
    status_map = {True: "✅ Pass", False: "❌ Fail"}
    for key, value in results.items():
        print(f"{key:.<25} {status_map[value]}")
    
    # Determine if environment is usable
    critical_features = ['cuda_found', 'environment_valid', 'pytorch_cuda_available']
    is_usable = all(results[feature] for feature in critical_features)
    
    print("\nEnvironment Status:")
    if is_usable:
        print("✅ Environment is properly configured for GPU operations")
        return 0
    else:
        print("❌ Environment needs attention before GPU operations will work")
        return 1

if __name__ == "__main__":
    sys.exit(main())