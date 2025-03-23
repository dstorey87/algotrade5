#!/usr/bin/env python
"""
Pre-commit hook installer for AlgoTradePro5
This script copies the pre-commit hook to the Git hooks directory
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def install_hook():
    """Install the pre-commit hook into the Git repository."""
    # Get repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    git_hooks_dir = repo_root / ".git" / "hooks"
    
    # Check if .git/hooks directory exists
    if not git_hooks_dir.exists():
        print(f"Error: Git hooks directory not found at {git_hooks_dir}")
        print("Are you sure this is a Git repository?")
        return 1
    
    # Source files
    pre_commit_bat = script_dir / "pre_commit.bat"
    pre_commit_hook_py = script_dir / "pre_commit_hook.py"
    python_wrapper_bat = script_dir / "python_wrapper.bat"
    
    # Destination file
    pre_commit_hook = git_hooks_dir / "pre-commit"
    
    # Create a Windows-friendly wrapper script for Git
    with open(python_wrapper_bat, 'w') as f:
        f.write('@echo off\n')
        f.write(f'"{pre_commit_bat}" %*\n')
        f.write('if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%\n')
    
    # Copy the pre-commit hook to the Git hooks directory
    try:
        # For Windows, we create a script that calls our batch file
        with open(pre_commit_hook, 'w') as f:
            f.write('#!/bin/sh\n')
            f.write(f'"{repo_root / "src" / "hooks" / "python_wrapper.bat"}"\n')
            f.write('exit $?\n')
        
        # Make the hook executable (might not matter on Windows but good practice)
        try:
            os.chmod(pre_commit_hook, 0o755)
        except Exception as e:
            print(f"Warning: Could not make hook executable: {e}")
        
        print(f"Pre-commit hook installed successfully at {pre_commit_hook}")
        print("The hook will run automatically before each commit.")
        
        # Create required directories
        logs_dir = repo_root / "logs"
        docs_dir = repo_root / "src" / "docs"
        
        os.makedirs(logs_dir, exist_ok=True)
        os.makedirs(docs_dir, exist_ok=True)
        
        print(f"Created logs directory at {logs_dir}")
        print(f"Created docs directory at {docs_dir}")
        
        # Test that the hook is working
        print("\nTesting pre-commit hook...")
        result = subprocess.run([sys.executable, pre_commit_hook_py], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Pre-commit hook test successful!")
        else:
            print("Pre-commit hook test failed with the following output:")
            print(result.stdout)
            print(result.stderr)
            
        return 0
        
    except Exception as e:
        print(f"Error installing pre-commit hook: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(install_hook())