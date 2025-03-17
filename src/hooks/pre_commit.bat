@echo off
:: AlgoTradePro5 pre-commit hook batch file
:: This file handles running the Python pre-commit hook correctly on Windows

:: Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0
set REPO_ROOT=%SCRIPT_DIR%\..\..

:: Create logs directory if it doesn't exist
if not exist "%REPO_ROOT%\logs" mkdir "%REPO_ROOT%\logs"

:: Set Python path explicitly - use installed Python
set PYTHON_EXE=python

:: Set the full path to the pre-commit hook script
set HOOK_SCRIPT=%REPO_ROOT%\src\hooks\run_pre_commit.py

:: Print debug information to a log file
echo Running pre-commit hook from %SCRIPT_DIR% > "%REPO_ROOT%\logs\pre-commit-debug.log"
echo Repository root: %REPO_ROOT% >> "%REPO_ROOT%\logs\pre-commit-debug.log"
echo Python executable: %PYTHON_EXE% >> "%REPO_ROOT%\logs\pre-commit-debug.log"
echo Hook script: %HOOK_SCRIPT% >> "%REPO_ROOT%\logs\pre-commit-debug.log"

:: Echo the command we're about to run
echo Running: %PYTHON_EXE% "%HOOK_SCRIPT%" >> "%REPO_ROOT%\logs\pre-commit-debug.log"

:: Change to the repository root directory
cd /d "%REPO_ROOT%"

:: Run the pre-commit hook script
%PYTHON_EXE% "%HOOK_SCRIPT%"

:: Check the exit code
if %ERRORLEVEL% neq 0 (
    echo Pre-commit hook failed with exit code %ERRORLEVEL% >> "%REPO_ROOT%\logs\pre-commit-debug.log"
    exit /b %ERRORLEVEL%
)

:: Success
echo Pre-commit hook completed successfully >> "%REPO_ROOT%\logs\pre-commit-debug.log"
exit /b 0