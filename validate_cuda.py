#!/usr/bin/env python3
"""CUDA Environment Validation for AlgoTradePro5"""
import os
import sys
import logging
import subprocess
from pathlib import Path
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_cuda_environment():
    """Reset CUDA environment to default state"""
    cuda_path = r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8"
    os.environ["CUDA_PATH"] = cuda_path
    os.environ["CUDA_HOME"] = cuda_path
    os.environ["PATH"] = os.path.join(cuda_path, "bin") + os.pathsep + os.environ["PATH"]
    return True

def reinstall_cuda_packages():
    """Reinstall CUDA-dependent packages"""
    packages = [
        "torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118",
        "cupy-cuda118",
        "pennylane-lightning-gpu"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y"] + package.split())
            time.sleep(1)  # Wait between uninstall and install
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + package.split())
            logger.info(f"Successfully reinstalled {package}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to reinstall {package}: {e}")
            return False
    return True

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
        if os.environ.get('CUDA_PATH') != cuda_path or os.environ.get('CUDA_HOME') != cuda_path:
            logger.warning("⚠️ CUDA environment variables incorrect, attempting reset...")
            if reset_cuda_environment():
                logger.info("✅ CUDA environment variables reset successfully")
                cuda_env_valid = True
            else:
                cuda_env_valid = False
        
        cuda_bin = os.path.join(cuda_path, 'bin')
        if cuda_bin not in os.environ['PATH']:
            logger.warning("⚠️ CUDA bin directory not in PATH, attempting fix...")
            if reset_cuda_environment():
                logger.info("✅ PATH updated with CUDA bin directory")
                cuda_env_valid = True
            else:
                cuda_env_valid = False
            
        validation_results['environment_valid'] = cuda_env_valid
        
        # Check PyTorch GPU support with recovery
        try:
            import torch
            validation_results['torch_gpu'] = True
            if torch.cuda.is_available():
                validation_results['pytorch_cuda_available'] = True
                device_name = torch.cuda.get_device_name(0)
                logger.info(f"✅ PyTorch GPU available: {device_name}")
                logger.info(f"   CUDA Version: {torch.version.cuda}")
            else:
                logger.warning("⚠️ PyTorch CUDA not available, attempting recovery...")
                if reinstall_cuda_packages():
                    # Retry PyTorch GPU check
                    import importlib
                    importlib.reload(torch)
                    if torch.cuda.is_available():
                        validation_results['pytorch_cuda_available'] = True
                        logger.info("✅ PyTorch GPU support recovered successfully")
        except ImportError:
            logger.warning("⚠️ PyTorch not installed, attempting installation...")
            if reinstall_cuda_packages():
                validation_results['torch_gpu'] = True
            
        # Check CuPy with recovery
        try:
            import cupy
            validation_results['cupy_available'] = True
            logger.info(f"✅ CuPy available with CUDA {cupy.cuda.runtime.runtimeGetVersion()}")
        except (ImportError, Exception) as e:
            logger.warning(f"⚠️ CuPy issue detected: {str(e)}, attempting recovery...")
            if reinstall_cuda_packages():
                try:
                    import importlib
                    import cupy
                    importlib.reload(cupy)
                    validation_results['cupy_available'] = True
                    logger.info("✅ CuPy support recovered successfully")
                except Exception as e:
                    logger.error(f"❌ CuPy recovery failed: {str(e)}")
            
        # Check Quantum GPU support with recovery
        try:
            import pennylane as qml
            try:
                dev = qml.device('lightning.gpu', wires=2)
                validation_results['quantum_gpu'] = True
                logger.info("✅ Quantum GPU support available")
            except Exception as e:
                logger.warning(f"⚠️ Quantum GPU device not available: {str(e)}, attempting recovery...")
                if reinstall_cuda_packages():
                    try:
                        dev = qml.device('lightning.gpu', wires=2)
                        validation_results['quantum_gpu'] = True
                        logger.info("✅ Quantum GPU support recovered successfully")
                    except Exception as e:
                        logger.error(f"❌ Quantum GPU recovery failed: {str(e)}")
        except ImportError:
            logger.warning("⚠️ PennyLane not installed, attempting installation...")
            if reinstall_cuda_packages():
                try:
                    import pennylane as qml
                    dev = qml.device('lightning.gpu', wires=2)
                    validation_results['quantum_gpu'] = True
                    logger.info("✅ Quantum GPU support installed successfully")
                except Exception as e:
                    logger.error(f"❌ PennyLane installation/setup failed: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error during validation: {str(e)}")
        
    return validation_results

def main():
    """Main validation function"""
    print("\n=== AlgoTradePro5 CUDA Validation ===\n")
    results = validate_cuda_environment()
    
    all_valid = all(results.values())
    if all_valid:
        print("\n✅ All CUDA components validated successfully!")
    else:
        print("\n⚠️ Some CUDA components need attention:")
        for component, status in results.items():
            status_icon = "✅" if status else "❌"
            print(f"{status_icon} {component}")
    
    return 0 if all_valid else 1

if __name__ == "__main__":
    sys.exit(main())