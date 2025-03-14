import os
import json
import hashlib
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional

class DependencyManager:
    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent.parent
        self.deps_dir = self.base_dir / "dependencies" / "site-packages"
        self.cache_file = self.base_dir / "dependency_cache.json"
        self.deps_dir.mkdir(parents=True, exist_ok=True)
        self.cache = self.load_cache()

    def load_cache(self) -> Dict:
        """Load dependency cache from JSON"""
        cache = {"packages": {}, "requirements": {}}
        if self.cache_file.exists():
            try:
                with open(self.cache_file) as f:
                    loaded_cache = json.load(f)
                    cache.update(loaded_cache)
            except json.JSONDecodeError:
                print("Warning: Cache file corrupted, creating new cache")
        return cache

    def save_cache(self):
        """Save dependency cache to JSON"""
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f, indent=2)

    def get_file_hash(self, filepath: Path) -> str:
        """Calculate SHA256 hash of a file"""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def is_package_cached(self, package_name: str, version: Optional[str] = None) -> bool:
        """Check if package is in local cache"""
        if not version:
            return any(pkg.startswith(f"{package_name}-") for pkg in os.listdir(self.deps_dir))
        return any(pkg.startswith(f"{package_name}-{version}") for pkg in os.listdir(self.deps_dir))

    def download_requirements(self, req_file: Path):
        """Download packages from requirements file to local cache"""
        if not req_file.exists():
            return
        
        # Check if requirements have changed
        current_hash = self.get_file_hash(req_file)
        if self.cache["requirements"].get(str(req_file)) == current_hash:
            print(f"Requirements {req_file.name} unchanged, using cached packages")
            return

        print(f"Downloading packages from {req_file.name} to local cache...")
        cmd = [
            "pip", "download",
            "--dest", str(self.deps_dir),
            "-r", str(req_file)
        ]
        try:
            subprocess.run(cmd, check=True)
            self.cache["requirements"][str(req_file)] = current_hash
            self.save_cache()
        except subprocess.CalledProcessError as e:
            print(f"Error downloading packages: {e}")

    def get_package_path(self, package_name: str, version: Optional[str] = None) -> Optional[Path]:
        """Get path to package in local cache"""
        if not self.is_package_cached(package_name, version):
            return None
            
        for pkg in os.listdir(self.deps_dir):
            if pkg.startswith(f"{package_name}-{version if version else ''}"):
                return self.deps_dir / pkg
        return None

    def cleanup_old_versions(self):
        """Remove old package versions keeping only the latest"""
        packages: Dict[str, List[Path]] = {}
        
        # Group package files by name
        for pkg_file in self.deps_dir.glob("*.whl"):
            pkg_name = pkg_file.name.split("-")[0].lower()
            if pkg_name not in packages:
                packages[pkg_name] = []
            packages[pkg_name].append(pkg_file)
        
        # Keep only latest version of each package
        for pkg_name, pkg_files in packages.items():
            if len(pkg_files) > 1:
                # Sort by creation time, newest first
                pkg_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                # Remove older versions
                for old_file in pkg_files[1:]:
                    print(f"Removing old package version: {old_file.name}")
                    old_file.unlink()

    def create_pip_conf(self, extra_index_url: Optional[str] = None):
        """Create pip.conf to prioritize local packages"""
        pip_conf_dir = Path.home() / ".pip"
        pip_conf_dir.mkdir(exist_ok=True)
        
        pip_conf = pip_conf_dir / "pip.conf"
        content = [
            "[global]",
            f"find-links = {self.deps_dir}",
            "no-index = true"
        ]
        
        if extra_index_url:
            content.extend([
                "no-index = false",
                f"extra-index-url = {extra_index_url}"
            ])
            
        pip_conf.write_text("\n".join(content))

    def get_cached_packages(self) -> List[str]:
        """Get list of cached package names"""
        return [pkg.split("-")[0] for pkg in os.listdir(self.deps_dir) if pkg.endswith(".whl")]

if __name__ == "__main__":
    manager = DependencyManager()
    
    # Process all requirements files
    base_dir = Path(__file__).parent.parent
    req_files = [
        "requirements.txt",
        "requirements-quantum.txt",
        "requirements-llm.txt"
    ]
    
    for req_file in req_files:
        req_path = base_dir / req_file
        if req_path.exists():
            manager.download_requirements(req_path)
    
    manager.cleanup_old_versions()
    manager.create_pip_conf()