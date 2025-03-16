"""
Error Management System
===================

CRITICAL REQUIREMENTS:
- Centralized error handling
- Severity-based logging
- Error aggregation
- Notification system
- Recovery procedures

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import datetime
import enum
import json
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict, List, Optional


class ErrorSeverity(enum.Enum):
    """Error severity levels"""

    LOW = 1  # Non-critical issues
    MEDIUM = 2  # Important but non-blocking issues
    HIGH = 3  # Critical issues requiring attention
    CRITICAL = 4  # System-stopping issues


class ErrorCategory(enum.Enum):
    """Error categories for classification"""

    SYSTEM = "System"
    TRADE = "Trade"
    MODEL = "Model"
    DATA = "Data"
    NETWORK = "Network"
    GPU = "GPU"
    QUANTUM = "Quantum"
    SETUP = "Setup"
    CUDA = "CUDA"
    OTHER = "Other"


class ErrorManager:
    """Central error management system"""

    def __init__(self, log_dir: str = "logs"):
        """Initialize error manager"""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Configure logging
        self._setup_logging()

        # Error statistics
        self.error_counts: Dict[str, int] = {}
        self.last_errors: Dict[str, List[Dict]] = {}

        # Recovery procedures
        self.recovery_handlers = {
            ErrorCategory.GPU.value: self._handle_gpu_error,
            ErrorCategory.MODEL.value: self._handle_model_error,
            ErrorCategory.TRADE.value: self._handle_trade_error,
            ErrorCategory.DATA.value: self._handle_data_error,
        }

    def _setup_logging(self) -> None:
        """Set up logging configuration"""
        # Main logger
        self.logger = logging.getLogger("AlgoTradePro5")
        self.logger.setLevel(logging.DEBUG)

        # Console handler
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console.setFormatter(console_format)
        self.logger.addHandler(console)

        # File handler
        log_file = self.log_dir / "error.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)

    def log_error(
        self, message: str, severity: int, category: str = "OTHER", **kwargs
    ) -> None:
        """Log an error with given severity and category"""
        # Update statistics
        self.error_counts[category] = self.error_counts.get(category, 0) + 1

        # Format error details
        error_detail = {
            "message": message,
            "severity": severity,
            "timestamp": datetime.datetime.now().isoformat(),
            "category": category,
            **kwargs,
        }

        # Add to recent errors
        if category not in self.last_errors:
            self.last_errors[category] = []
        self.last_errors[category].append(error_detail)

        # Keep only last 100 errors per category
        self.last_errors[category] = self.last_errors[category][-100:]

        # Log based on severity
        if severity >= ErrorSeverity.CRITICAL.value:
            self.logger.critical(f"[{category}] {message}")
            self._handle_critical_error(error_detail)
        elif severity >= ErrorSeverity.HIGH.value:
            self.logger.error(f"[{category}] {message}")
            self._attempt_recovery(error_detail)
        elif severity >= ErrorSeverity.MEDIUM.value:
            self.logger.warning(f"[{category}] {message}")
        else:
            self.logger.info(f"[{category}] {message}")

    def _handle_critical_error(self, error: Dict) -> None:
        """Handle critical system errors"""
        try:
            # Save error state
            state_file = self.log_dir / "critical_error_state.json"
            with open(state_file, "w") as f:
                json.dump(error, f, indent=2)

            # Attempt recovery if handler exists
            self._attempt_recovery(error)

        except Exception as e:
            self.logger.critical(f"Failed to handle critical error: {e}")

    def _attempt_recovery(self, error: Dict) -> None:
        """Attempt to recover from error"""
        category = error.get("category", "OTHER")
        handler = self.recovery_handlers.get(category)

        if handler:
            try:
                handler(error)
            except Exception as e:
                self.logger.error(f"Recovery failed for {category}: {e}")

    def _handle_gpu_error(self, error: Dict) -> None:
        """Handle GPU-related errors"""
        try:
            import torch

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.reset_peak_memory_stats()
        except ImportError:
            pass

    def _handle_model_error(self, error: Dict) -> None:
        """Handle ML model errors"""
        # Implement model error recovery
        pass

    def _handle_trade_error(self, error: Dict) -> None:
        """Handle trading errors"""
        # Implement trade error recovery
        pass

    def _handle_data_error(self, error: Dict) -> None:
        """Handle data-related errors"""
        # Implement data error recovery
        pass

    def get_error_summary(self) -> Dict:
        """Get summary of error statistics"""
        return {
            "counts": self.error_counts,
            "recent": {k: v[-5:] for k, v in self.last_errors.items()},
            "categories": [c.value for c in ErrorCategory],
        }

    def clear_errors(self, category: Optional[str] = None) -> None:
        """Clear error statistics"""
        if category:
            self.error_counts.pop(category, None)
            self.last_errors.pop(category, None)
        else:
            self.error_counts.clear()
            self.last_errors.clear()


# Create global instance
_error_manager = ErrorManager()


def get_error_manager() -> ErrorManager:
    """Get global error manager instance"""
    return _error_manager
