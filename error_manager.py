#!/usr/bin/env python3
"""Error management system for AlgoTradPro5"""
import logging
from datetime import datetime
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class ErrorManager:
    def __init__(self):
        self.errors = []
        
    def log_error(self, message: str, component: str = "System", severity: str = "MEDIUM") -> None:
        """Log an error with severity and component information"""
        error = {
            'timestamp': self.get_current_timestamp(),
            'message': message,
            'component': component,
            'severity': severity
        }
        self.errors.append(error)
        logger.error(f"[{severity}] {component}: {message}")
        
    def get_errors(self, component: Optional[str] = None) -> list:
        """Get errors, optionally filtered by component"""
        if component:
            return [e for e in self.errors if e['component'] == component]
        return self.errors
        
    def get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()
        
    def clear_errors(self, component: Optional[str] = None) -> None:
        """Clear all errors or those for a specific component"""
        if component:
            self.errors = [e for e in self.errors if e['component'] != component]
        else:
            self.errors = []