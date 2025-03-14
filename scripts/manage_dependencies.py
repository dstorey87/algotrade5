#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
from pathlib import Path
import hashlib
import json

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def get_file_hash(filepath):
    """Calculate SHA256 hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def load_dependency_cache():
    """Load dependency cache from JSON"""
    cache_file = Path("dependency_cache.json")
    if cache_file.exists():
        with open(cache_file) as f:
            return json.load(f)
    return {}

def save_dependency_cache(cache):
    """Save dependency cache to JSON"""
    with open("dependency_cache.json", "w") as f:
        json.dump(cache, f, indent=2)

def download_dependencies():
    base_dir = Path(__file__).parent.parent
    deps_dir = base_dir / "dependencies" / "site-packages"
    cache = load_dependency_cache()
    
    # Ensure directories exist
    ensure_dir(deps_dir)
    
    # List of requirements files to process
    req_files = [
        'requirements.txt',
        'requirements-quantum.txt',
        'requirements-llm.txt'
    ]
    
    updated = False
    for req_file in req_files:
        req_path = base_dir / req_file
        if req_path.exists():
            # Check if requirements have changed
            current_hash = get_file_hash(req_path)
            if cache.get(req_file) != current_hash:
                print(f"Processing {req_file}...")
                
                # Download packages to local directory
                cmd = [
                    sys.executable, '-m', 'pip', 'download',
                    '--dest', str(deps_dir),
                    '--no-deps',  # Don't download dependencies recursively
                    '-r', str(req_path)
                ]
                
                try:
                    subprocess.run(cmd, check=True)
                    print(f"Successfully downloaded dependencies from {req_file}")
                    cache[req_file] = current_hash
                    updated = True
                except subprocess.CalledProcessError as e:
                    print(f"Error downloading dependencies from {req_file}: {e}")
                    continue

    if updated:
        save_dependency_cache(cache)
        print("Dependency cache updated successfully")
    else:
        print("All dependencies are up to date")

def cleanup_old_packages():
    """Remove old package versions keeping only the latest"""
    deps_dir = Path("dependencies/site-packages")
    packages = {}
    
    # Group package files by name
    for file in deps_dir.glob("*.whl"):
        pkg_name = file.name.split("-")[0].lower()
        if pkg_name not in packages:
            packages[pkg_name] = []
        packages[pkg_name].append(file)
    
    # Keep only the latest version of each package
    for pkg_files in packages.values():
        if len(pkg_files) > 1:
            # Sort by creation time, newest first
            pkg_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            # Remove older versions
            for old_file in pkg_files[1:]:
                print(f"Removing old package: {old_file.name}")
                old_file.unlink()

if __name__ == "__main__":
    download_dependencies()
    cleanup_old_packages()