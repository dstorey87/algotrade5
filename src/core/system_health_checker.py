"""
System Health Checker
===================

CRITICAL REQUIREMENTS:
- Component health validation
- Resource monitoring
- Performance metrics
- Critical system checks

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import logging
import psutil
import os
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
import sqlite3

from error_manager import ErrorManager, ErrorSeverity

logger = logging.getLogger(__name__)

class SystemHealthChecker:
    """Monitors and validates system health"""
    
    def __init__(self):
        """Initialize health checker"""
        self.error_manager = ErrorManager()
        
    def check_system_health(self) -> bool:
        """
        Perform complete system health check
        
        Returns:
            bool: True if all checks pass
        """
        try:
            checks = [
                self._check_memory(),
                self._check_disk_space(),
                self._check_cpu_usage(),
                self._check_gpu_availability(),
                self._check_database_connection(),
                self._check_model_availability()
            ]
            
            return all(checks)
            
        except Exception as e:
            self.error_manager.log_error(
                f"Health check failed: {str(e)}",
                ErrorSeverity.HIGH.value,
                "HealthCheck"
            )
            return False
            
    def _check_memory(self) -> bool:
        """Check system memory usage"""
        try:
            memory = psutil.virtual_memory()
            
            # Alert if memory usage > 90%
            if memory.percent > 90:
                self.error_manager.log_error(
                    f"High memory usage: {memory.percent}%",
                    ErrorSeverity.HIGH.value,
                    "Memory"
                )
                return False
                
            # Warning if memory usage > 80%
            if memory.percent > 80:
                self.error_manager.log_error(
                    f"Elevated memory usage: {memory.percent}%",
                    ErrorSeverity.MEDIUM.value,
                    "Memory"
                )
                
            return True
            
        except Exception as e:
            self.error_manager.log_error(
                f"Memory check failed: {str(e)}",
                ErrorSeverity.HIGH.value,
                "Memory"
            )
            return False
            
    def _check_disk_space(self) -> bool:
        """Check available disk space"""
        try:
            # Check disk usage for data directory
            usage = psutil.disk_usage(Path.home())
            
            # Alert if disk usage > 95%
            if usage.percent > 95:
                self.error_manager.log_error(
                    f"Critical disk usage: {usage.percent}%",
                    ErrorSeverity.HIGH.value,
                    "Disk"
                )
                return False
                
            # Warning if disk usage > 85%
            if usage.percent > 85:
                self.error_manager.log_error(
                    f"High disk usage: {usage.percent}%",
                    ErrorSeverity.MEDIUM.value,
                    "Disk"
                )
                
            return True
            
        except Exception as e:
            self.error_manager.log_error(
                f"Disk check failed: {str(e)}",
                ErrorSeverity.HIGH.value,
                "Disk"
            )
            return False
            
    def _check_cpu_usage(self) -> bool:
        """Check CPU usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Alert if CPU usage > 95%
            if cpu_percent > 95:
                self.error_manager.log_error(
                    f"Critical CPU usage: {cpu_percent}%",
                    ErrorSeverity.HIGH.value,
                    "CPU"
                )
                return False
                
            # Warning if CPU usage > 85%
            if cpu_percent > 85:
                self.error_manager.log_error(
                    f"High CPU usage: {cpu_percent}%",
                    ErrorSeverity.MEDIUM.value,
                    "CPU"
                )
                
            return True
            
        except Exception as e:
            self.error_manager.log_error(
                f"CPU check failed: {str(e)}",
                ErrorSeverity.HIGH.value,
                "CPU"
            )
            return False
            
    def _check_gpu_availability(self) -> bool:
        """Check GPU availability and usage"""
        try:
            # Import conditionally to avoid errors if not installed
            import torch
            
            if not torch.cuda.is_available():
                self.error_manager.log_error(
                    "CUDA not available",
                    ErrorSeverity.MEDIUM.value,
                    "GPU"
                )
                return False
                
            # Check GPU memory usage
            for i in range(torch.cuda.device_count()):
                memory_allocated = torch.cuda.memory_allocated(i)
                memory_reserved = torch.cuda.memory_reserved(i)
                
                if memory_allocated / memory_reserved > 0.9:
                    self.error_manager.log_error(
                        f"High GPU memory usage on device {i}",
                        ErrorSeverity.HIGH.value,
                        "GPU"
                    )
                    return False
                    
            return True
            
        except ImportError:
            # Not critical if GPU is not required
            logger.warning("PyTorch not installed, skipping GPU checks")
            return True
            
        except Exception as e:
            self.error_manager.log_error(
                f"GPU check failed: {str(e)}",
                ErrorSeverity.HIGH.value,
                "GPU"
            )
            return False
            
    def _check_database_connection(self) -> bool:
        """Check database connectivity"""
        try:
            data_path = Path.home() / "AlgoTradPro5" / "data"
            db_path = data_path / "analysis.db"
            
            if not db_path.exists():
                self.error_manager.log_error(
                    f"Database not found at {db_path}",
                    ErrorSeverity.HIGH.value,
                    "Database"
                )
                return False
                
            # Test connection
            with sqlite3.connect(db_path) as conn:
                c = conn.cursor()
                c.execute("SELECT 1")
                
            return True
            
        except Exception as e:
            self.error_manager.log_error(
                f"Database check failed: {str(e)}",
                ErrorSeverity.HIGH.value,
                "Database"
            )
            return False
            
    def _check_model_availability(self) -> bool:
        """Check AI model availability"""
        try:
            model_path = Path.home() / "AlgoTradPro5" / "models"
            
            required_models = [
                "llm/deepseek",
                "llm/mistral",
                "ml/phi-2",
                "ml/quantum"
            ]
            
            missing_models = []
            for model in required_models:
                if not (model_path / model).exists():
                    missing_models.append(model)
                    
            if missing_models:
                self.error_manager.log_error(
                    f"Missing required models: {missing_models}",
                    ErrorSeverity.HIGH.value,
                    "Models"
                )
                return False
                
            return True
            
        except Exception as e:
            self.error_manager.log_error(
                f"Model check failed: {str(e)}",
                ErrorSeverity.HIGH.value,
                "Models"
            )
            return False

    def get_system_metrics(self) -> Dict:
        """Get current system metrics"""
        try:
            return {
                'memory_usage': psutil.virtual_memory().percent,
                'cpu_usage': psutil.cpu_percent(),
                'disk_usage': psutil.disk_usage(Path.home()).percent,
                'gpu_available': self._check_gpu_availability(),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get system metrics: {e}")
            return {}