"""
GPU Setup and Validation Script
===========================

CRITICAL REQUIREMENTS:
- CUDA toolkit validation
- GPU driver verification
- PyTorch GPU support
- Quantum circuit GPU optimization
- Memory configuration

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import logging
import os
import sys
from pathlib import Path
from typing import Dict, Optional

from src.core.error_manager import ErrorSeverity, get_error_manager

logger = logging.getLogger(__name__)

try:
    import torch
    import torch.cuda as cuda
except ImportError:
    torch = None
    cuda = None

try:
    import GPUtil
except ImportError:
    GPUtil = None


def check_cuda_available() -> bool:
    """Check if CUDA is available"""
    return torch is not None and torch.cuda.is_available()


def get_gpu_info() -> Dict:
    """Get detailed GPU information"""
    info = {
        "cuda_available": False,
        "gpu_name": None,
        "cuda_version": None,
        "driver_version": None,
        "memory_total": None,
    }

    if not check_cuda_available():
        return info

    try:
        info.update(
            {
                "cuda_available": True,
                "gpu_name": torch.cuda.get_device_name(0),
                "cuda_version": torch.version.cuda,
                "driver_version": GPUtil.getGPUs()[0].driver if GPUtil else None,
                "memory_total": torch.cuda.get_device_properties(0).total_memory,
            }
        )
    except Exception as e:
        logger.error(f"Error getting GPU info: {e}")

    return info


def configure_gpu_memory() -> bool:
    """Configure GPU memory settings"""
    if not check_cuda_available():
        return False

    try:
        # Get available GPU memory
        gpu = GPUtil.getGPUs()[0] if GPUtil else None
        total_memory = gpu.memoryTotal if gpu else None

        if total_memory:
            # Reserve 10% memory for system
            max_memory = int(total_memory * 0.9)
            torch.cuda.set_per_process_memory_fraction(0.9)

            # Set memory growth
            if hasattr(torch.cuda, "memory_reserved"):
                torch.cuda.memory_reserved(0)
            if hasattr(torch.cuda, "empty_cache"):
                torch.cuda.empty_cache()

        return True

    except Exception as e:
        get_error_manager().log_error(
            f"GPU memory configuration failed: {e}", ErrorSeverity.MEDIUM.value, "GPU"
        )
        return False


def test_gpu_compute() -> bool:
    """Test basic GPU computation"""
    if not check_cuda_available():
        return False

    try:
        # Test tensor operations
        device = torch.device("cuda:0")
        x = torch.randn(1000, 1000).to(device)
        y = torch.randn(1000, 1000).to(device)
        z = torch.matmul(x, y)
        del x, y, z
        torch.cuda.empty_cache()

        return True

    except Exception as e:
        get_error_manager().log_error(
            f"GPU compute test failed: {e}", ErrorSeverity.HIGH.value, "GPU"
        )
        return False


def setup_quantum_gpu() -> bool:
    """Configure GPU for quantum circuit simulation"""
    if not check_cuda_available():
        return False

    try:
        # Set environment variables for quantum libraries
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"

        # Configure PyTorch for quantum operations
        torch.backends.cudnn.benchmark = True
        torch.backends.cuda.matmul.allow_tf32 = True

        return True

    except Exception as e:
        get_error_manager().log_error(
            f"Quantum GPU setup failed: {e}", ErrorSeverity.MEDIUM.value, "GPU"
        )
        return False


def validate_gpu_setup() -> Dict[str, bool]:
    """Validate complete GPU setup"""
    return {
        "cuda_available": check_cuda_available(),
        "memory_configured": configure_gpu_memory(),
        "compute_test": test_gpu_compute(),
        "quantum_ready": setup_quantum_gpu(),
    }


def main() -> int:
    """Main GPU setup function"""
    print("Starting GPU setup and validation...")

    # Get GPU information
    info = get_gpu_info()
    if info["cuda_available"]:
        print(f"Found GPU: {info['gpu_name']}")
        print(f"CUDA version: {info['cuda_version']}")
        print(f"Driver version: {info['driver_version']}")
    else:
        print("No GPU detected - system will run on CPU")
        return 0

    # Configure and validate GPU
    validation = validate_gpu_setup()

    if not all(validation.values()):
        failed = [k for k, v in validation.items() if not v]
        print(f"GPU setup failed for: {', '.join(failed)}")
        return 1

    print("GPU setup completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
