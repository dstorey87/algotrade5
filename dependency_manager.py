#!/usr/bin/env python3
"""Enhanced dependency management using Poetry for AlgoTradPro5"""
import os
import sys
import logging
import subprocess
from pathlib import Path
from typing import List, Optional, Dict
import tomli
import importlib.util
from importlib.metadata import version, PackageNotFoundError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DependencyManager:
    """Manages Python dependencies using Poetry, with runtime dependency detection"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.pyproject_path = self.project_root / "pyproject.toml"
        self.poetry_lock_path = self.project_root / "poetry.lock"
        self._load_project_config()
    
    def _load_project_config(self) -> None:
        """Load project configuration from pyproject.toml"""
        try:
            with open(self.pyproject_path, "rb") as f:
                self.project_config = tomli.load(f)
        except Exception as e:
            logger.error(f"Failed to load pyproject.toml: {e}")
            self.project_config = {}
    
    def _get_required_version(self, package: str) -> Optional[str]:
        """Get required version of a package from pyproject.toml"""
        try:
            deps = self.project_config["tool"]["poetry"]["dependencies"]
            if package in deps:
                version_spec = deps[package]
                if isinstance(version_spec, dict):
                    return version_spec["version"]
                return version_spec
            return None
        except (KeyError, TypeError):
            return None
    
    def is_package_installed(self, package: str) -> bool:
        """Check if a package is installed with correct version"""
        try:
            installed_version = version(package)
            required_version = self._get_required_version(package)
            
            if not required_version:
                return True
                
            # Handle version specifiers
            if '^' in required_version:
                min_version = required_version.replace('^', '')
                return installed_version >= min_version
            elif '>=' in required_version:
                min_version = required_version.replace('>=', '')
                return installed_version >= min_version
                
            return True
        except PackageNotFoundError:
            return False
    
    def ensure_package(self, package: str) -> bool:
        """Ensure a package is installed using Poetry"""
        try:
            if not self.is_package_installed(package):
                logger.info(f"Installing package {package} with Poetry...")
                subprocess.run(
                    ["poetry", "add", package],
                    check=True,
                    capture_output=True,
                    text=True
                )
                return True
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install {package}: {e.stderr}")
            return False
    
    def _add_import_hook(self):
        """Add import hook to automatically install missing packages"""
        class AutoInstallImporter:
            def __init__(self, dependency_manager):
                self.dependency_manager = dependency_manager
            
            def find_spec(self, fullname, path, target=None):
                if fullname in sys.modules:
                    return None
                    
                try:
                    # Try normal import first
                    spec = importlib.util.find_spec(fullname)
                    if spec is not None:
                        return spec
                    
                    # If import fails, try to install
                    logger.info(f"Attempting to install missing package: {fullname}")
                    if self.dependency_manager.ensure_package(fullname):
                        return importlib.util.find_spec(fullname)
                    
                except Exception as e:
                    logger.debug(f"Import hook error for {fullname}: {e}")
                return None
        
        sys.meta_path.insert(0, AutoInstallImporter(self))
    
    def ensure_environment(self) -> bool:
        """Ensure Poetry virtual environment is active and configured"""
        try:
            # Check if we're in a Poetry virtual environment
            if "POETRY_ACTIVE" not in os.environ:
                logger.warning("Not running in Poetry environment. Please run 'poetry shell' or 'poetry run python'")
                return False
            
            # Verify Poetry is installed and accessible
            subprocess.run(
                ["poetry", "--version"],
                check=True,
                capture_output=True,
                text=True
            )
            
            # Install base dependencies if lock file is missing
            if not self.poetry_lock_path.exists():
                subprocess.run(
                    ["poetry", "install"],
                    check=True,
                    capture_output=True,
                    text=True
                )
            
            # Add import hook for runtime dependencies
            self._add_import_hook()
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Poetry environment check failed: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Environment setup failed: {e}")
            return False

# Global instance
_manager = None

def get_dependency_manager() -> DependencyManager:
    """Get or create the global dependency manager instance"""
    global _manager
    if _manager is None:
        _manager = DependencyManager()
    return _manager

def ensure_dependencies() -> bool:
    """Ensure all dependencies are available"""
    manager = get_dependency_manager()
    return manager.ensure_environment()

if __name__ == "__main__":
    # When run directly, ensure all dependencies
    success = ensure_dependencies()
    sys.exit(0 if success else 1)