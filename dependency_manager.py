#!/usr/bin/env python3
"""
Dependency Management System for AlgoTradPro5
Handles automatic detection and installation of missing Python packages
"""
import os
import sys
import subprocess
import importlib
import logging
import json
import platform
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), "logs", "dependency.log"), mode="a"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Ensure logs directory exists
Path(os.path.join(os.path.dirname(__file__), "logs")).mkdir(exist_ok=True)

class DependencyManager:
    """
    Manages system dependencies for AlgoTradPro5
    Automatically detects and installs missing packages
    """
    def __init__(self):
        self.os_type = platform.system()
        self.project_root = Path(__file__).parent
        self.dependency_cache_file = self.project_root / "dependency_cache.json"
        self.core_dependencies = {
            "jsonschema": "jsonschema",
            "attrs": "attrs",
            "pyrsistent": "pyrsistent",
            "numpy": "numpy>=1.20.0",
            "pandas": "pandas>=1.3.0",
            "scikit-learn": "scikit-learn>=1.0.0"
        }
        
        self.component_dependencies = {
            "ai": [
                "torch>=2.0.0",
                "transformers>=4.15.0",
                "accelerate>=0.20.0"
            ],
            "quantitative": [
                "pandas-ta>=0.3.0",  # Replacing TA-Lib
                "statsmodels>=0.13.0",
                "matplotlib>=3.5.0",
                "yfinance>=0.2.0",  # Added for data fetching
                "scipy>=1.7.0"
            ],
            "quantum": [
                "pennylane>=0.30.0",
                "qiskit>=0.40.0"
            ],
            "api": [
                "fastapi>=0.95.0",
                "uvicorn>=0.20.0"
            ],
            "gpu": [
                "GPUtil",
                "nvidia-ml-py3"
            ]
        }
        
        # Load cached dependencies
        self.load_dependency_cache()

    def load_dependency_cache(self):
        """Load dependency cache from file if exists"""
        if self.dependency_cache_file.exists():
            try:
                with open(self.dependency_cache_file, 'r') as f:
                    self.cached_deps = json.load(f)
                logger.info(f"Loaded dependency cache with {len(self.cached_deps)} entries")
            except Exception as e:
                logger.warning(f"Failed to load dependency cache: {e}")
                self.cached_deps = {}
        else:
            self.cached_deps = {}
            
    def save_dependency_cache(self):
        """Save dependency cache to file"""
        try:
            with open(self.dependency_cache_file, 'w') as f:
                json.dump(self.cached_deps, f)
            logger.info(f"Saved dependency cache with {len(self.cached_deps)} entries")
        except Exception as e:
            logger.warning(f"Failed to save dependency cache: {e}")
            
    def is_package_installed(self, package_name: str) -> bool:
        """Check if a package is installed"""
        # Strip version info for import check
        import_name = package_name.split('>=')[0].split('==')[0].split('<')[0].strip()
        
        try:
            importlib.import_module(import_name)
            return True
        except ImportError:
            return False
            
    def get_missing_packages(self, components: List[str] = None) -> List[str]:
        """
        Get list of missing packages for specified components
        If components is None, check core dependencies only
        """
        missing_packages = []
        
        # Always check core dependencies
        for package, spec in self.core_dependencies.items():
            if not self.is_package_installed(package):
                missing_packages.append(spec)
                
        # Check component-specific dependencies if requested
        if components:
            for component in components:
                if component in self.component_dependencies:
                    for package_spec in self.component_dependencies[component]:
                        package = package_spec.split('>=')[0].split('==')[0].split('<')[0].strip()
                        if not self.is_package_installed(package):
                            missing_packages.append(package_spec)
        
        return missing_packages
        
    def install_packages(self, packages: List[str], verbose: bool = True) -> Tuple[bool, List[str]]:
        """
        Install specified packages using pip
        Returns (success, failed_packages)
        """
        if not packages:
            return True, []
            
        failed_packages = []
        success = True
        
        for package in packages:
            try:
                logger.info(f"Installing package: {package}")
                
                # Use different install commands based on the package
                if package == "ta-lib":
                    # Special handling for ta-lib
                    if self.os_type == "Windows":
                        # On Windows, use prebuilt wheel
                        wheel_url = "https://download.lfd.uci.edu/pythonlibs/w4tscw6k/TA_Lib-0.4.24-cp310-cp310-win_amd64.whl"
                        subprocess.check_call([sys.executable, "-m", "pip", "install", wheel_url])
                    else:
                        # On Linux/Mac, try regular install but it might require system libs
                        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                else:
                    # Normal pip install for other packages
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    
                # Update cache after successful install
                self.cached_deps[package] = True
                
            except Exception as e:
                logger.error(f"Failed to install {package}: {e}")
                failed_packages.append(package)
                success = False
                
        # Save updated cache
        self.save_dependency_cache()
        
        return success, failed_packages
        
    def check_and_install_dependencies(self, components: List[str] = None) -> bool:
        """
        Check for missing dependencies and install them if needed
        Returns True if all dependencies are satisfied
        """
        missing_packages = self.get_missing_packages(components)
        
        if not missing_packages:
            logger.info("All required dependencies are installed")
            return True
            
        logger.info(f"Found {len(missing_packages)} missing packages: {missing_packages}")
        
        # Attempt to install missing packages
        success, failed_packages = self.install_packages(missing_packages)
        
        if success:
            logger.info("All dependencies installed successfully")
            return True
        else:
            logger.error(f"Failed to install some dependencies: {failed_packages}")
            logger.error("Please install these packages manually and try again")
            return False
            
    def fix_imports_in_file(self, file_path: str) -> bool:
        """Add import error handling to a Python file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Check if our dependency handler is already imported
            if "from dependency_manager import ensure_dependencies" in content:
                return True
                
            # Add dependency handling to the file
            import_section_end = content.find("import", content.find("import") + 1) + content[content.find("import") + 1:].find("\n") + 1
            
            # Insert our dependency handling code
            modified_content = (
                content[:import_section_end] + 
                "\n\n# Ensure all dependencies are installed\n"
                "try:\n"
                "    from dependency_manager import ensure_dependencies\n"
                "    ensure_dependencies()\n"
                "except ImportError:\n"
                "    pass  # Dependency manager not available, proceed with standard imports\n\n" +
                content[import_section_end:]
            )
            
            with open(file_path, 'w') as f:
                f.write(modified_content)
                
            logger.info(f"Added dependency handling to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to modify {file_path}: {e}")
            return False
            
    def fix_imports_in_project(self):
        """Add import error handling to all main Python files in the project"""
        main_files = [
            "run_algotradpro5.py",
            "run_backtest.py",
            "continuous_backtester.py",
            "initialize_system.py"
        ]
        
        success = True
        for file in main_files:
            file_path = self.project_root / file
            if file_path.exists():
                if not self.fix_imports_in_file(str(file_path)):
                    success = False
                    
        return success

def ensure_dependencies(components: List[str] = None) -> bool:
    """
    Utility function to ensure all required dependencies are installed
    Returns True if all dependencies are installed/successfully installed
    """
    try:
        dep_manager = DependencyManager()
        return dep_manager.check_and_install_dependencies(components)
    except Exception as e:
        logger.error(f"Error checking dependencies: {e}")
        return False

if __name__ == "__main__":
    # When run directly, check and install all dependencies
    manager = DependencyManager()
    
    # Process command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--fix-imports":
            # Fix imports in project files
            manager.fix_imports_in_project()
        elif sys.argv[1] == "--components":
            # Install dependencies for specific components
            components = sys.argv[2].split(',') if len(sys.argv) > 2 else None
            manager.check_and_install_dependencies(components)
    else:
        # Default: install all core dependencies
        manager.check_and_install_dependencies()