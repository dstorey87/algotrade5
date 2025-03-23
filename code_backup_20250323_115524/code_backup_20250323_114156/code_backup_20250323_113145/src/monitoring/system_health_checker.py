import logging
import sys
# REMOVED_UNUSED_CODE: from pathlib import Path
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from typing import Dict, List, Optional

# REMOVED_UNUSED_CODE: from doc_validator import get_documentation, validate_documentation
from error_manager import ErrorManager
from gpu_monitor import GPUMonitor

# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


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
                    component="Documentation",
                )
                return False
            return True
        except Exception as e:
            self.error_manager.log_error(
                f"Documentation validation error: {str(e)}",
                severity="HIGH",
                component="Documentation",
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
            if "error" in gpu_info:
                self.error_manager.log_error(
                    f"GPU issue detected: {gpu_info['error']}",
                    severity="MEDIUM",
                    component="GPU",
                )

            # Additional health checks can be added here

            self._last_check_result = {
                "documentation_valid": True,
                "gpu_status": "ok" if "error" not in gpu_info else "error",
                "timestamp": self.error_manager.get_current_timestamp(),
            }

            return True

        except Exception as e:
            self.error_manager.log_error(
                f"System health check failed: {str(e)}",
                severity="HIGH",
                component="SystemHealth",
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


# REMOVED_UNUSED_CODE: def get_last_health_check() -> Dict:
# REMOVED_UNUSED_CODE:     """Global function to get last health check results"""
# REMOVED_UNUSED_CODE:     return _health_checker.get_last_check_result()
