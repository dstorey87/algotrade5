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
# REMOVED_UNUSED_CODE: from typing import Dict, Optional

# REMOVED_UNUSED_CODE: import psutil

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

# REMOVED_UNUSED_CODE:     def validate_gpu(self) -> bool:
# REMOVED_UNUSED_CODE:         """Validate GPU availability and configuration"""
# REMOVED_UNUSED_CODE:         if not self.has_gpu:
# REMOVED_UNUSED_CODE:             logger.warning("No GPU available - system will use CPU only")
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             # Test CUDA initialization
# REMOVED_UNUSED_CODE:             torch.cuda.init()
# REMOVED_UNUSED_CODE:             device = torch.device("cuda:0")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Test tensor operations
# REMOVED_UNUSED_CODE:             test_tensor = torch.rand(100, 100).to(device)
# REMOVED_UNUSED_CODE:             test_result = torch.matmul(test_tensor, test_tensor)
# REMOVED_UNUSED_CODE:             del test_tensor, test_result
# REMOVED_UNUSED_CODE:             torch.cuda.empty_cache()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             logger.info(f"GPU validated: {torch.cuda.get_device_name(0)}")
# REMOVED_UNUSED_CODE:             return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         except Exception as e:
# REMOVED_UNUSED_CODE:             self.error_manager.log_error(
# REMOVED_UNUSED_CODE:                 f"GPU validation failed: {e}", ErrorSeverity.MEDIUM.value, "GPU"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             return False

# REMOVED_UNUSED_CODE:     def check_gpu_health(self) -> bool:
# REMOVED_UNUSED_CODE:         """Check GPU health and resource usage"""
# REMOVED_UNUSED_CODE:         if not self.has_gpu:
# REMOVED_UNUSED_CODE:             return True  # No GPU to check
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             metrics = self.get_metrics()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Check memory usage
# REMOVED_UNUSED_CODE:             if metrics["memory_used_percent"] > self.memory_threshold:
# REMOVED_UNUSED_CODE:                 self.error_manager.log_error(
# REMOVED_UNUSED_CODE:                     f"High GPU memory usage: {metrics['memory_used_percent']:.1%}",
# REMOVED_UNUSED_CODE:                     ErrorSeverity.HIGH.value,
# REMOVED_UNUSED_CODE:                     "GPU",
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Check temperature
# REMOVED_UNUSED_CODE:             if metrics["temperature"] > self.temp_threshold:
# REMOVED_UNUSED_CODE:                 self.error_manager.log_error(
# REMOVED_UNUSED_CODE:                     f"High GPU temperature: {metrics['temperature']}°C",
# REMOVED_UNUSED_CODE:                     ErrorSeverity.HIGH.value,
# REMOVED_UNUSED_CODE:                     "GPU",
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Check utilization
# REMOVED_UNUSED_CODE:             if metrics["utilization"] > self.util_threshold:
# REMOVED_UNUSED_CODE:                 self.error_manager.log_error(
# REMOVED_UNUSED_CODE:                     f"High GPU utilization: {metrics['utilization']:.1%}",
# REMOVED_UNUSED_CODE:                     ErrorSeverity.MEDIUM.value,
# REMOVED_UNUSED_CODE:                     "GPU",
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         except Exception as e:
# REMOVED_UNUSED_CODE:             self.error_manager.log_error(
# REMOVED_UNUSED_CODE:                 f"GPU health check failed: {e}", ErrorSeverity.MEDIUM.value, "GPU"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             return False

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

# REMOVED_UNUSED_CODE:     def is_healthy(self) -> bool:
# REMOVED_UNUSED_CODE:         """Check if GPU is in a healthy state"""
# REMOVED_UNUSED_CODE:         if not self.has_gpu:
# REMOVED_UNUSED_CODE:             return True  # No GPU to check
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         metrics = self.get_metrics()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return (
# REMOVED_UNUSED_CODE:             metrics["memory_used_percent"] < self.memory_threshold
# REMOVED_UNUSED_CODE:             and metrics["temperature"] < self.temp_threshold
# REMOVED_UNUSED_CODE:             and metrics["utilization"] < self.util_threshold
# REMOVED_UNUSED_CODE:         )

# REMOVED_UNUSED_CODE:     def cleanup(self) -> None:
# REMOVED_UNUSED_CODE:         """Clean up GPU resources"""
# REMOVED_UNUSED_CODE:         if self.has_gpu:
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 torch.cuda.empty_cache()
# REMOVED_UNUSED_CODE:             except Exception as e:
# REMOVED_UNUSED_CODE:                 self.error_manager.log_error(
# REMOVED_UNUSED_CODE:                     f"GPU cleanup failed: {e}", ErrorSeverity.LOW.value, "GPU"
# REMOVED_UNUSED_CODE:                 )


# Create global instance
_gpu_monitor = GPUMonitor()


# REMOVED_UNUSED_CODE: def get_gpu_monitor() -> GPUMonitor:
# REMOVED_UNUSED_CODE:     """Global function to get GPU monitor instance"""
# REMOVED_UNUSED_CODE:     return _gpu_monitor
