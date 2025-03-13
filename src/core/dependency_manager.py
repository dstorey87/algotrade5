"""
Dependency Management System
=========================

CRITICAL REQUIREMENTS:
- Validate all required Python packages
- Verify system dependencies (CUDA, Docker)
- Ensure model availability
- Track component dependencies

VALIDATION GATES:
1. Package validation
2. System requirements
3. Model verification
4. Integration checks

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import logging
import sys
import pkg_resources
import subprocess
from typing import Dict, List, Optional, Set, Tuple
from pathlib import Path
import json
import torch
from datetime import datetime

from error_manager import ErrorManager, ErrorSeverity
from config_manager import get_config

logger = logging.getLogger(__name__)

class DependencyManager:
    """Manages and validates system dependencies"""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize dependency manager"""
        self.config = config or get_config()
        self.error_manager = ErrorManager()
        
        # Load dependency requirements
        self.requirements = {
            'python_version': '>=3.9',
            'cuda_version': '>=11.0',
            'min_memory_gb': 16,
            'min_gpu_memory_gb': 8
        }
        
        # Component validation status
        self.validation_status = {}
        
        # Initialize dependency cache
        self._initialize_cache()
        
    def _initialize_cache(self) -> None:
        """Initialize dependency cache"""
        cache_path = Path("dependency_cache.json")
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    self.cache = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load dependency cache: {e}")
                self.cache = {}
        else:
            self.cache = {}
            
    def _save_cache(self) -> None:
        """Save dependency cache"""
        try:
            with open("dependency_cache.json", 'w') as f:
                json.dump(self.cache, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save dependency cache: {e}")
            
    def validate_python_packages(self) -> bool:
        """Validate required Python packages"""
        try:
            requirements_files = [
                'requirements.txt',
                'requirements-llm.txt',
                'requirements-quantum.txt'
            ]
            
            all_requirements: Set[str] = set()
            for req_file in requirements_files:
                if Path(req_file).exists():
                    with open(req_file) as f:
                        all_requirements.update(f.read().splitlines())
                        
            # Check each requirement
            missing_packages = []
            for req in all_requirements:
                if not req or req.startswith('#'):
                    continue
                try:
                    pkg_resources.require(req)
                except Exception:
                    missing_packages.append(req)
                    
            if missing_packages:
                logger.error(f"Missing packages: {', '.join(missing_packages)}")
                return False
                
            return True
            
        except Exception as e:
            self.error_manager.log_error(
                f"Package validation error: {e}",
                ErrorSeverity.HIGH.value,
                "Dependencies"
            )
            return False
            
    def validate_cuda(self) -> bool:
        """Validate CUDA installation and GPU access"""
        if not torch.cuda.is_available():
            logger.error("CUDA not available")
            return False
            
        try:
            # Check CUDA version
            cuda_version = torch.version.cuda
            if cuda_version and float(cuda_version.split('.')[0]) >= 11.0:
                logger.info(f"CUDA {cuda_version} available")
                return True
            else:
                logger.error(f"CUDA version {cuda_version} below requirement")
                return False
                
        except Exception as e:
            self.error_manager.log_error(
                f"CUDA validation error: {e}",
                ErrorSeverity.HIGH.value,
                "CUDA"
            )
            return False
            
    def validate_models(self) -> bool:
        """Validate required AI models are available"""
        try:
            models_path = Path(self.config['models_path'])
            if not models_path.exists():
                logger.error(f"Models directory not found: {models_path}")
                return False
                
            # Check required model directories
            required_models = {
                'llm': ['mistral', 'mixtral'],
                'ml': ['phi-2', 'quantum']
            }
            
            missing_models = []
            for category, models in required_models.items():
                category_path = models_path / category
                if not category_path.exists():
                    missing_models.extend([f"{category}/{model}" for model in models])
                    continue
                    
                for model in models:
                    if not (category_path / model).exists():
                        missing_models.append(f"{category}/{model}")
                        
            if missing_models:
                logger.error(f"Missing models: {', '.join(missing_models)}")
                return False
                
            return True
            
        except Exception as e:
            self.error_manager.log_error(
                f"Model validation error: {e}",
                ErrorSeverity.HIGH.value,
                "Models"
            )
            return False
            
    def validate_system_resources(self) -> bool:
        """Validate system meets resource requirements"""
        try:
            import psutil
            import GPUtil
            
            # Check system memory
            memory_gb = psutil.virtual_memory().total / (1024**3)
            if memory_gb < self.requirements['min_memory_gb']:
                logger.error(
                    f"Insufficient memory: {memory_gb:.1f}GB < "
                    f"{self.requirements['min_memory_gb']}GB required"
                )
                return False
                
            # Check GPU memory if available
            if torch.cuda.is_available():
                gpu = GPUtil.getGPUs()[0]
                if gpu.memoryTotal < (self.requirements['min_gpu_memory_gb'] * 1024):
                    logger.error(
                        f"Insufficient GPU memory: {gpu.memoryTotal/1024:.1f}GB < "
                        f"{self.requirements['min_gpu_memory_gb']}GB required"
                    )
                    return False
                    
            return True
            
        except Exception as e:
            self.error_manager.log_error(
                f"Resource validation error: {e}",
                ErrorSeverity.MEDIUM.value,
                "Resources"
            )
            return False
            
    def validate_docker(self) -> bool:
        """Validate Docker installation and access"""
        try:
            result = subprocess.run(
                ['docker', '--version'],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                logger.error("Docker not installed or accessible")
                return False
                
            # Check Docker Compose
            result = subprocess.run(
                ['docker-compose', '--version'],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                logger.error("Docker Compose not installed")
                return False
                
            return True
            
        except Exception as e:
            self.error_manager.log_error(
                f"Docker validation error: {e}",
                ErrorSeverity.HIGH.value,
                "Docker"
            )
            return False
            
    def ensure_dependencies(self, components: Optional[List[str]] = None) -> bool:
        """Ensure all required dependencies are available"""
        try:
            # Default to all components if none specified
            if not components:
                components = ['python', 'cuda', 'models', 'resources', 'docker']
                
            validation_map = {
                'python': self.validate_python_packages,
                'cuda': self.validate_cuda,
                'models': self.validate_models,
                'resources': self.validate_system_resources,
                'docker': self.validate_docker
            }
            
            # Validate requested components
            results = []
            for component in components:
                if component in validation_map:
                    is_valid = validation_map[component]()
                    self.validation_status[component] = {
                        'valid': is_valid,
                        'timestamp': datetime.now().isoformat()
                    }
                    results.append(is_valid)
                else:
                    logger.warning(f"Unknown component: {component}")
                    
            # Cache validation results
            self._save_cache()
            
            return all(results)
            
        except Exception as e:
            self.error_manager.log_error(
                f"Dependency validation error: {e}",
                ErrorSeverity.CRITICAL.value,
                "Dependencies"
            )
            return False
            
    def get_validation_status(self) -> Dict:
        """Get current validation status"""
        return {
            'status': self.validation_status,
            'cache': self.cache,
            'requirements': self.requirements
        }
        
# Create global instance
_dependency_manager = DependencyManager()

def get_dependency_manager() -> DependencyManager:
    """Global function to get dependency manager instance"""
    return _dependency_manager