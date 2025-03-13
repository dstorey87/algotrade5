import logging
import sys
from typing import Dict, List, Optional
from pathlib import Path

from doc_validator import validate_documentation, get_documentation
from gpu_monitor import GPUMonitor
from error_manager import ErrorManager

logger = logging.getLogger(__name__)

class SystemHealthChecker:
    def __init__(self):
        self.error_manager = ErrorManager()
        self.gpu_monitor = GPUMonitor()
        self._last_check_result = {}

    def check_documentation(self) -> bool:
        """Validate system documentation is up to date"""
        try:
            if not validate_documentation():
                self.error_manager.log_error(
                    "Documentation validation failed. System cannot proceed without valid documentation.",
                    severity="HIGH",
                    component="Documentation"
                )
                return False
            return True
        except Exception as e:
            self.error_manager.log_error(
                f"Documentation validation error: {str(e)}",
                severity="HIGH",
                component="Documentation"
            )
            return False

    def check_system_health(self) -> bool:
        """Check overall system health including documentation"""
        # Documentation must be valid before proceeding
        if not self.check_documentation():
            return False

        # Continue with other health checks
        try:
            # Check GPU availability
            gpu_info = self.gpu_monitor.get_gpu_info()
            if 'error' in gpu_info:
                self.error_manager.log_error(
                    f"GPU issue detected: {gpu_info['error']}",
                    severity="MEDIUM",
                    component="GPU"
                )

            # Additional health checks can be added here
            
            self._last_check_result = {
                'documentation_valid': True,
                'gpu_status': 'ok' if 'error' not in gpu_info else 'error',
                'timestamp': self.error_manager.get_current_timestamp()
            }
            
            return True

        except Exception as e:
            self.error_manager.log_error(
                f"System health check failed: {str(e)}",
                severity="HIGH",
                component="SystemHealth"
            )
            return False

    def get_last_check_result(self) -> Dict:
        """Get results of the last health check"""
        return self._last_check_result

# Create global instance
_health_checker = SystemHealthChecker()

def check_system_health() -> bool:
    """Global function to check system health"""
    return _health_checker.check_system_health()

def get_last_health_check() -> Dict:
    """Global function to get last health check results"""
    return _health_checker.get_last_check_result()