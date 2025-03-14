#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil
from pathlib import Path

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def download_dependencies():
    base_dir = Path(__file__).parent.parent
    deps_dir = base_dir / 'dependencies' / 'site-packages'
    
    # Ensure directories exist
    ensure_dir(deps_dir)
    
    # List of requirements files to process
    req_files = [
        'requirements.txt',
        'requirements-quantum.txt',
        'requirements-llm.txt'
    ]
    
    for req_file in req_files:
        req_path = base_dir / req_file
        if req_path.exists():
            print(f"Processing {req_file}...")
            
            # Download packages to local directory
            cmd = [
                sys.executable, '-m', 'pip', 'download',
                '--dest', str(deps_dir),
                '-r', str(req_path)
            ]
            
            try:
                subprocess.run(cmd, check=True)
                print(f"Successfully downloaded dependencies from {req_file}")
            except subprocess.CalledProcessError as e:
                print(f"Error downloading dependencies from {req_file}: {e}")
                continue

if __name__ == "__main__":
    download_dependencies()