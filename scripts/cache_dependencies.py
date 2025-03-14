#!/usr/bin/env python3
"""
Dependency Cache Manager
=====================

Handles downloading and caching of Python packages for Docker builds.
Ensures packages are downloaded only once and stored locally.
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DependencyCacheManager:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.cache_dir = self.project_root / "dependencies" / "site-packages"
        self.requirements_files = [
            "requirements.txt",
            "requirements-quantum.txt",
            "requirements-llm.txt"
        ]
        self.cache_index = self.project_root / "dependency_cache.json"
        
    def ensure_cache_dir(self):
        """Ensure cache directory exists"""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def get_cached_packages(self):
        """Get list of currently cached packages"""
        if self.cache_index.exists():
            with open(self.cache_index) as f:
                return json.load(f)
        return {}
        
    def cache_packages(self):
        """Download and cache all required packages"""
        self.ensure_cache_dir()
        cached = self.get_cached_packages()
        
        for req_file in self.requirements_files:
            req_path = self.project_root / req_file
            if not req_path.exists():
                continue
                
            logger.info(f"Processing {req_file}")
            subprocess.run([
                sys.executable, "-m", "pip", "install",
                "-t", str(self.cache_dir),
                "-r", str(req_path)
            ], check=True)
            
            # Update cache index
            with open(req_path) as f:
                for line in f:
                    if line.strip() and not line.startswith("#"):
                        package = line.split("==")[0].strip()
                        cached[package] = {"source": req_file}
                        
        # Save cache index
        with open(self.cache_index, "w") as f:
            json.dump(cached, f, indent=2)
            
        logger.info(f"Cached {len(cached)} packages in {self.cache_dir}")

if __name__ == "__main__":
    try:
        cache_manager = DependencyCacheManager()
        cache_manager.cache_packages()
    except Exception as e:
        logger.error(f"Failed to cache dependencies: {e}")
        sys.exit(1)