#!/usr/bin/env python3
"""
Dependency Manager
================

Manages Python package dependencies and Docker build context:
1. Caches dependencies locally
2. Cleans up unused packages
3. Maintains build context size
4. Updates dependency tracking
"""

import os
import sys
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DependencyManager:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.config_path = self.project_root / "dependency_manager.json"
        self.load_config()
        
    def load_config(self):
        """Load dependency configuration"""
        with open(self.config_path) as f:
            self.config = json.load(f)
            
    def save_config(self):
        """Save updated dependency configuration"""
        self.config["last_update"] = datetime.now().strftime("%Y-%m-%d")
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)
            
    def get_cache_size(self, path: Path) -> float:
        """Get size of directory in GB"""
        total = 0
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total += os.path.getsize(fp)
        return total / (1024 * 1024 * 1024)  # Convert to GB
        
    def cleanup_cache(self):
        """Clean up cache if size exceeds threshold"""
        site_packages = self.project_root / self.config["cache_paths"]["site-packages"]
        current_size = self.get_cache_size(site_packages)
        
        if current_size >= self.config["build_context"]["cleanup_trigger_gb"]:
            logger.info(f"Cache size ({current_size:.2f}GB) exceeds threshold, cleaning...")
            
            # Remove excluded patterns
            for pattern in self.config["build_context"]["exclude_patterns"]:
                for path in site_packages.glob(pattern):
                    if path.is_file():
                        os.remove(path)
                    else:
                        shutil.rmtree(path)
                        
            # Remove old versions of packages
            for group in self.config["package_groups"].values():
                for package, version in group.items():
                    pkg_path = site_packages / package
                    if pkg_path.exists():
                        for item in pkg_path.glob("*"):
                            if version not in str(item):
                                if item.is_file():
                                    os.remove(item)
                                else:
                                    shutil.rmtree(item)
                                    
            new_size = self.get_cache_size(site_packages)
            logger.info(f"Cleanup complete. New size: {new_size:.2f}GB")
            
    def update_dependencies(self):
        """Update dependencies based on configuration"""
        logger.info("Updating dependencies...")
        
        # Ensure directories exist
        for path in self.config["cache_paths"].values():
            (self.project_root / path).mkdir(parents=True, exist_ok=True)
            
        # Install/update packages
        for group_name, packages in self.config["package_groups"].items():
            logger.info(f"Processing {group_name} dependencies...")
            for package, version in packages.items():
                cmd = [
                    sys.executable, "-m", "pip", "install",
                    f"{package}=={version}",
                    "-t", str(self.project_root / self.config["cache_paths"]["site-packages"]),
                    "--no-deps"  # Don't install dependencies to control versions
                ]
                subprocess.run(cmd, check=True)
                
        self.cleanup_cache()
        self.save_config()
        
    def validate_dependencies(self) -> bool:
        """Validate all required dependencies are cached"""
        site_packages = self.project_root / self.config["cache_paths"]["site-packages"]
        
        for group in self.config["package_groups"].values():
            for package, version in group.items():
                pkg_path = site_packages / package
                if not pkg_path.exists():
                    logger.error(f"Missing package: {package}")
                    return False
                    
                # Check version
                try:
                    import importlib.metadata as importlib_metadata
                    pkg_version = importlib_metadata.version(package)
                    if pkg_version != version:
                        logger.error(f"Version mismatch for {package}: {pkg_version} != {version}")
                        return False
                except:
                    logger.warning(f"Could not verify version for {package}")
                    
        return True

if __name__ == "__main__":
    try:
        manager = DependencyManager()
        
        if not manager.validate_dependencies():
            logger.info("Dependencies need updating")
            manager.update_dependencies()
            
        if not manager.validate_dependencies():
            logger.error("Dependency validation failed after update")
            sys.exit(1)
            
        logger.info("Dependencies validated successfully")
        
    except Exception as e:
        logger.error(f"Failed to manage dependencies: {e}")
        sys.exit(1)