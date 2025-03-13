"""
System Initialization Manager
=========================

Handles startup sequence, path validation, and component initialization.
Ensures all required directories and files exist before system startup.

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import logging
import json
import torch
import psutil

from .error_manager import get_error_manager, ErrorSeverity, ErrorCategory

class SystemInitializer:
    """Manages system initialization and validation"""
    
    def __init__(self):
        self.error_manager = get_error_manager()
        self.logger = logging.getLogger('AlgoTradePro5.init')
        self.base_path = Path('C:/AlgoTradPro5')
        
        # Required paths
        self.required_paths = {
            'models': self.base_path / 'models',
            'data': self.base_path / 'data',
            'logs': self.base_path / 'logs',
            'config': self.base_path / 'config',
            'aimodels': self.base_path / 'aimodels',
            'src': self.base_path / 'src'
        }
        
        # Required files
        self.required_files = {
            '.env': self.base_path / '.env',
            'config.json': self.base_path / 'config.json',
            'freqai_config.json': self.base_path / 'freqai_config.json'
        }
        
    def validate_paths(self) -> bool:
        """Validate all required paths exist"""
        success = True
        
        for name, path in self.required_paths.items():
            if not path.exists():
                try:
                    path.mkdir(parents=True)
                    self.logger.info(f"Created directory: {path}")
                except Exception as e:
                    self.error_manager.log_error(
                        f"Failed to create {name} directory: {e}",
                        ErrorSeverity.HIGH.value,
                        ErrorCategory.SETUP.value,
                        path=str(path)
                    )
                    success = False
                    
        return success
        
    def validate_files(self) -> bool:
        """Validate all required files exist"""
        success = True
        
        for name, path in self.required_files.items():
            if not path.exists():
                self.error_manager.log_error(
                    f"Required file missing: {name}",
                    ErrorSeverity.HIGH.value,
                    ErrorCategory.SETUP.value,
                    path=str(path)
                )
                success = False
                
        return success
        
    def check_system_requirements(self) -> bool:
        """Verify system meets minimum requirements"""
        success = True
        
        # Check RAM
        ram_gb = psutil.virtual_memory().total / (1024**3)
        if ram_gb < 16:
            self.error_manager.log_error(
                f"Insufficient RAM: {ram_gb:.1f}GB (min 16GB required)",
                ErrorSeverity.HIGH.value,
                ErrorCategory.SYSTEM.value
            )
            success = False
            
        # Check CUDA
        if not torch.cuda.is_available():
            self.error_manager.log_error(
                "CUDA not available",
                ErrorSeverity.HIGH.value,
                ErrorCategory.CUDA.value
            )
            success = False
        else:
            gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            if gpu_mem < 4:
                self.error_manager.log_error(
                    f"Insufficient GPU memory: {gpu_mem:.1f}GB (min 4GB required)",
                    ErrorSeverity.HIGH.value,
                    ErrorCategory.GPU.value
                )
                success = False
                
        return success
        
    def validate_environment(self) -> bool:
        """Validate environment variables"""
        required_vars = [
            'BINANCE_API_KEY',
            'BINANCE_API_SECRET',
            'JWT_SECRET_KEY',
            'HUGGINGFACE_TOKEN'
        ]
        
        success = True
        for var in required_vars:
            if not os.getenv(var):
                self.error_manager.log_error(
                    f"Missing environment variable: {var}",
                    ErrorSeverity.HIGH.value,
                    ErrorCategory.SETUP.value
                )
                success = False
                
        return success
        
    def initialize_system(self) -> bool:
        """Run full system initialization"""
        self.logger.info("Starting system initialization...")
        
        # Run all validation checks
        checks = [
            self.validate_paths(),
            self.validate_files(),
            self.check_system_requirements(),
            self.validate_environment()
        ]
        
        if all(checks):
            self.logger.info("System initialization successful")
            return True
        else:
            self.error_manager.log_error(
                "System initialization failed",
                ErrorSeverity.CRITICAL.value,
                ErrorCategory.SETUP.value
            )
            return False
            
    def get_system_info(self) -> Dict:
        """Get current system information"""
        return {
            'ram_gb': psutil.virtual_memory().total / (1024**3),
            'cuda_available': torch.cuda.is_available(),
            'gpu_info': {
                'name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
                'memory_gb': (torch.cuda.get_device_properties(0).total_memory / (1024**3)) 
                           if torch.cuda.is_available() else None
            },
            'paths': {name: str(path) for name, path in self.required_paths.items()},
            'python_version': sys.version
        }

# Create global instance
_system_initializer = SystemInitializer()

def get_system_initializer() -> SystemInitializer:
    """Get global system initializer instance"""
    return _system_initializer