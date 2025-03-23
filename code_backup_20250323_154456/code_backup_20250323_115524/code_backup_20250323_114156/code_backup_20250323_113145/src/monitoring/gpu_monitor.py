"""
GPU Monitoring System
==================

CRITICAL REQUIREMENTS:
- GPU resource monitoring
- Memory usage tracking
- Temperature monitoring
- Utilization alerts
- Graceful CPU fallback

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import logging
from datetime import datetime
from typing import Dict, Optional

import psutil

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


class GPUMonitor:
    """Monitor GPU health and resource usage"""

    def __init__(self):
        """Initialize GPU monitoring"""
        self.error_manager = get_error_manager()
        self.has_gpu = torch is not None and torch.cuda.is_available()
        self.gpu_index = 0  # Primary GPU

        # Thresholds
        self.memory_threshold = 0.90  # 90% memory usage alert
        self.temp_threshold = 80.0  # 80°C temperature alert
        self.util_threshold = 0.95  # 95% utilization alert

        # Last recorded metrics
        self.last_metrics: Dict = {}

    def validate_gpu(self) -> bool:
        """Validate GPU availability and configuration"""
        if not self.has_gpu:
            logger.warning("No GPU available - system will use CPU only")
            return False

        try:
            # Test CUDA initialization
            torch.cuda.init()
            device = torch.device("cuda:0")

            # Test tensor operations
            test_tensor = torch.rand(100, 100).to(device)
            test_result = torch.matmul(test_tensor, test_tensor)
            del test_tensor, test_result
            torch.cuda.empty_cache()

            logger.info(f"GPU validated: {torch.cuda.get_device_name(0)}")
            return True

        except Exception as e:
            self.error_manager.log_error(
                f"GPU validation failed: {e}", ErrorSeverity.MEDIUM.value, "GPU"
            )
            return False

    def check_gpu_health(self) -> bool:
        """Check GPU health and resource usage"""
        if not self.has_gpu:
            return True  # No GPU to check

        try:
            metrics = self.get_metrics()

            # Check memory usage
            if metrics["memory_used_percent"] > self.memory_threshold:
                self.error_manager.log_error(
                    f"High GPU memory usage: {metrics['memory_used_percent']:.1%}",
                    ErrorSeverity.HIGH.value,
                    "GPU",
                )

            # Check temperature
            if metrics["temperature"] > self.temp_threshold:
                self.error_manager.log_error(
                    f"High GPU temperature: {metrics['temperature']}°C",
                    ErrorSeverity.HIGH.value,
                    "GPU",
                )

            # Check utilization
            if metrics["utilization"] > self.util_threshold:
                self.error_manager.log_error(
                    f"High GPU utilization: {metrics['utilization']:.1%}",
                    ErrorSeverity.MEDIUM.value,
                    "GPU",
                )

            return True

        except Exception as e:
            self.error_manager.log_error(
                f"GPU health check failed: {e}", ErrorSeverity.MEDIUM.value, "GPU"
            )
            return False

    def get_metrics(self) -> Dict:
        """Get current GPU metrics"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "gpu_available": self.has_gpu,
            "memory_used_percent": 0.0,
            "temperature": 0.0,
            "utilization": 0.0,
            "memory_total": 0,
            "memory_used": 0,
            "gpu_name": "CPU Only",
        }

        if not self.has_gpu:
            return metrics

        try:
            # Get GPU metrics using GPUtil if available
            if GPUtil:
                gpu = GPUtil.getGPUs()[self.gpu_index]
                metrics.update(
                    {
                        "memory_used_percent": gpu.memoryUtil,
                        "temperature": gpu.temperature,
                        "utilization": gpu.load,
                        "memory_total": gpu.memoryTotal,
                        "memory_used": gpu.memoryUsed,
                        "gpu_name": gpu.name,
                    }
                )
            # Fallback to torch.cuda
            elif cuda:
                metrics.update(
                    {
                        "memory_used_percent": cuda.memory_allocated()
                        / cuda.get_device_properties(self.gpu_index).total_memory,
                        "memory_total": cuda.get_device_properties(
                            self.gpu_index
                        ).total_memory,
                        "memory_used": cuda.memory_allocated(),
                        "gpu_name": cuda.get_device_name(self.gpu_index),
                    }
                )

            self.last_metrics = metrics
            return metrics

        except Exception as e:
            self.error_manager.log_error(
                f"Failed to get GPU metrics: {e}", ErrorSeverity.LOW.value, "GPU"
            )
            return self.last_metrics or metrics

    def is_healthy(self) -> bool:
        """Check if GPU is in a healthy state"""
        if not self.has_gpu:
            return True  # No GPU to check

        metrics = self.get_metrics()

        return (
            metrics["memory_used_percent"] < self.memory_threshold
            and metrics["temperature"] < self.temp_threshold
            and metrics["utilization"] < self.util_threshold
        )

    def cleanup(self) -> None:
        """Clean up GPU resources"""
        if self.has_gpu:
            try:
                torch.cuda.empty_cache()
            except Exception as e:
                self.error_manager.log_error(
                    f"GPU cleanup failed: {e}", ErrorSeverity.LOW.value, "GPU"
                )


# Create global instance
_gpu_monitor = GPUMonitor()


def get_gpu_monitor() -> GPUMonitor:
    """Global function to get GPU monitor instance"""
    return _gpu_monitor
