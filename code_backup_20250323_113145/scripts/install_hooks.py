#!/usr/bin/env python
"""
Install script for AlgoTradPro5 pre-commit hooks.
This script sets up the Git pre-commit hook to properly use Python on Windows.
"""

import os
# REMOVED_UNUSED_CODE: import shutil
# REMOVED_UNUSED_CODE: import subprocess
import sys
from pathlib import Path


def main():
    """Set up the pre-commit hook for the repository."""
    # Get the root directory of the repository
    repo_root = Path(__file__).resolve().parent.parent
    
    # Define paths
    git_hooks_dir = repo_root / ".git" / "hooks"
    src_hooks_dir = repo_root / "src" / "hooks"
    pre_commit_bat = src_hooks_dir / "pre_commit.bat"
    git_pre_commit = git_hooks_dir / "pre-commit"
    
    # Ensure the src/hooks directory exists
    os.makedirs(src_hooks_dir, exist_ok=True)
    
    # Create the pre_commit.bat file in src/hooks
    with open(pre_commit_bat, "w") as f:
        f.write("""@echo off
:: This is a Windows batch file wrapper for the Python pre-commit hook
:: It ensures that Python is called properly regardless of PATH configuration

:: Use a reliable path to Python. Adjust this path if your Python is installed elsewhere
set PYTHON_PATH=python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python not found in PATH, trying specific locations...
    
    if exist "C:\\Python311\\python.exe" (
        set PYTHON_PATH=C:\\Python311\\python.exe
    ) else if exist "C:\\Python310\\python.exe" (
        set PYTHON_PATH=C:\\Python310\\python.exe
    ) else if exist "C:\\Python39\\python.exe" (
        set PYTHON_PATH=C:\\Python39\\python.exe
    ) else if exist "C:\\Python38\\python.exe" (
        set PYTHON_PATH=C:\\Python38\\python.exe
    ) else if exist "C:\\Program Files\\Python311\\python.exe" (
        set PYTHON_PATH="C:\\Program Files\\Python311\\python.exe"
    ) else if exist "C:\\Program Files\\Python310\\python.exe" (
        set PYTHON_PATH="C:\\Program Files\\Python310\\python.exe"
    ) else if exist "C:\\Program Files\\Python39\\python.exe" (
        set PYTHON_PATH="C:\\Program Files\\Python39\\python.exe"
    ) else if exist "C:\\Program Files\\Python38\\python.exe" (
        set PYTHON_PATH="C:\\Program Files\\Python38\\python.exe"
    ) else if exist "%LOCALAPPDATA%\\Programs\\Python\\Python311\\python.exe" (
        set PYTHON_PATH="%LOCALAPPDATA%\\Programs\\Python\\Python311\\python.exe"
    ) else if exist "%LOCALAPPDATA%\\Programs\\Python\\Python310\\python.exe" (
        set PYTHON_PATH="%LOCALAPPDATA%\\Programs\\Python\\Python310\\python.exe"
    ) else if exist "%LOCALAPPDATA%\\Programs\\Python\\Python39\\python.exe" (
        set PYTHON_PATH="%LOCALAPPDATA%\\Programs\\Python\\Python39\\python.exe"
    ) else if exist "%LOCALAPPDATA%\\Programs\\Python\\Python38\\python.exe" (
        set PYTHON_PATH="%LOCALAPPDATA%\\Programs\\Python\\Python38\\python.exe"
    ) else (
        echo ERROR: Python not found. Please install Python or update your PATH.
        echo You can temporarily disable the pre-commit hook by running:
        echo git commit --no-verify
        exit /b 1
    )
)

echo Using Python: %PYTHON_PATH%

:: Get the repository root directory
set REPO_ROOT=%~dp0..\\..

:: Create logs directory if it doesn't exist
if not exist "%REPO_ROOT%\\logs" mkdir "%REPO_ROOT%\\logs"

:: Run the pre-commit hook script
cd /d "%REPO_ROOT%"
%PYTHON_PATH% "%REPO_ROOT%\\src\\hooks\\run_pre_commit.py"

:: Return the exit code from Python
exit /b %ERRORLEVEL%
""")
    
    # Create a simple shell script as pre-commit in .git/hooks
    with open(git_pre_commit, "w") as f:
        f.write(f"""#!/bin/sh
# This is a wrapper script that calls the actual pre-commit hook
# Windows systems will use pre_commit.bat, others will use run_pre_commit.py directly

REPO_ROOT="{repo_root.as_posix()}"
BAT_SCRIPT="$REPO_ROOT/src/hooks/pre_commit.bat"
PY_SCRIPT="$REPO_ROOT/src/hooks/run_pre_commit.py"

# Determine if we're on Windows
case "$(uname -s)" in
    CYGWIN*|MINGW*|MSYS*|Windows_NT*)
        # Windows system - use the batch file
        cmd.exe /c "$BAT_SCRIPT"
        exit $?
        ;;
    *)
        # Unix-like system - use Python directly
        python "$PY_SCRIPT"
        exit $?
        ;;
esac
""")
    
    # Make the pre-commit hook executable on Unix-like systems
    try:
        os.chmod(git_pre_commit, 0o755)
    except:
        print("Note: Could not make pre-commit hook executable. This is normal on Windows.")
    
    print(f"Pre-commit hook installed successfully in {git_pre_commit}")
    print("The hook will call the appropriate script based on your operating system.")

if __name__ == "__main__":
    main()