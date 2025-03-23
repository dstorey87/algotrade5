"""
CUDA Utilities Module
===================

CRITICAL REQUIREMENTS:
- Memory management
- Resource monitoring
- Error handling
- Performance optimization
- Device synchronization

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import logging
import os
import time
from typing import Dict, Optional, Tuple

from src.core.error_manager import ErrorSeverity, get_error_manager

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

logger = logging.getLogger(__name__)


class CUDAUtils:
    """CUDA utility functions for GPU operations"""

    def __init__(self):
        """Initialize CUDA utilities"""
        self.error_manager = get_error_manager()
        self.has_gpu = torch is not None and torch.cuda.is_available()
        self.device = torch.device("cuda:0") if self.has_gpu else torch.device("cpu")

    def get_memory_info(self) -> Dict[str, int]:
        """Get GPU memory information"""
        if not self.has_gpu:
            return {"total": 0, "used": 0, "free": 0}

        try:
            gpu = GPUtil.getGPUs()[0] if GPUtil else None
            if gpu:
                return {
                    "total": gpu.memoryTotal * 1024 * 1024,  # Convert to bytes
                    "used": gpu.memoryUsed * 1024 * 1024,
                    "free": (gpu.memoryTotal - gpu.memoryUsed) * 1024 * 1024,
                }
            else:
                props = torch.cuda.get_device_properties(0)
                allocated = torch.cuda.memory_allocated(0)
                return {
                    "total": props.total_memory,
                    "used": allocated,
                    "free": props.total_memory - allocated,
                }

        except Exception as e:
            self.error_manager.log_error(
                f"Failed to get GPU memory info: {e}", ErrorSeverity.LOW.value, "CUDA"
            )
            return {"total": 0, "used": 0, "free": 0}

    def optimize_memory(self) -> bool:
        """Optimize GPU memory usage"""
        if not self.has_gpu:
            return False

        try:
            # Clear cache
            torch.cuda.empty_cache()

            # Enable memory saving features
            if hasattr(torch.backends.cudnn, "benchmark"):
                torch.backends.cudnn.benchmark = True
            if hasattr(torch.cuda, "memory_stats"):
                torch.cuda.reset_peak_memory_stats()

            return True

        except Exception as e:
            self.error_manager.log_error(
                f"Memory optimization failed: {e}", ErrorSeverity.MEDIUM.value, "CUDA"
            )
            return False

    def measure_execution_time(
        self, func: callable, *args, **kwargs
    ) -> Tuple[float, Optional[Exception]]:
        """Measure GPU execution time of a function"""
        if not self.has_gpu:
            return -1.0, RuntimeError("No GPU available")

        try:
            # Synchronize before timing
            torch.cuda.synchronize()
            start_time = time.perf_counter()

            # Execute function
            result = func(*args, **kwargs)

            # Synchronize and measure
            torch.cuda.synchronize()
            end_time = time.perf_counter()

            return end_time - start_time, None

        except Exception as e:
            self.error_manager.log_error(
                f"Execution time measurement failed: {e}",
                ErrorSeverity.LOW.value,
                "CUDA",
            )
            return -1.0, e

    def run_stress_test(self, size: int = 5000) -> Dict:
        """Run GPU stress test"""
        if not self.has_gpu:
            return {"success": False, "error": "No GPU available"}

        try:
            results = {}

            # Matrix multiplication test
            x = torch.randn(size, size, device=self.device)
            y = torch.randn(size, size, device=self.device)

            matmul_time, matmul_error = self.measure_execution_time(torch.matmul, x, y)
            results["matmul"] = {
                "time": matmul_time,
                "error": str(matmul_error) if matmul_error else None,
            }

            # Convolution test
            if size <= 1000:  # Avoid memory issues with large sizes
                x = torch.randn(1, 3, size, size, device=self.device)
                conv = torch.nn.Conv2d(3, 64, 3).to(self.device)

                conv_time, conv_error = self.measure_execution_time(conv, x)
                results["conv"] = {
                    "time": conv_time,
                    "error": str(conv_error) if conv_error else None,
                }

            # Memory test
            mem_info = self.get_memory_info()
            results["memory"] = mem_info

            # Cleanup
            del x, y
            if "conv" in results:
                del conv
            torch.cuda.empty_cache()

            results["success"] = True
            return results

        except Exception as e:
            self.error_manager.log_error(
                f"GPU stress test failed: {e}", ErrorSeverity.MEDIUM.value, "CUDA"
            )
            return {"success": False, "error": str(e)}

    def is_tensor_on_gpu(self, tensor: torch.Tensor) -> bool:
        """Check if a tensor is on GPU"""
        return tensor.is_cuda if torch is not None else False

    def sync_device(self) -> None:
        """Synchronize GPU device"""
        if self.has_gpu:
            torch.cuda.synchronize()

    def cleanup(self) -> None:
        """Clean up GPU resources"""
        if self.has_gpu:
            try:
                torch.cuda.empty_cache()
                if hasattr(torch.cuda, "memory_stats"):
                    torch.cuda.reset_peak_memory_stats()
            except Exception as e:
                self.error_manager.log_error(
                    f"CUDA cleanup failed: {e}", ErrorSeverity.LOW.value, "CUDA"
                )


# Create global instance
_cuda_utils = CUDAUtils()


def get_cuda_utils() -> CUDAUtils:
    """Global function to get CUDA utilities instance"""
    return _cuda_utils
