@echo off
:: This is a Windows batch file wrapper for the Python pre-commit hook
:: It ensures that Python is called properly regardless of PATH configuration

:: Use a reliable path to Python. Adjust this path if your Python is installed elsewhere
set PYTHON_PATH=python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python not found in PATH, trying specific locations...
    
    if exist "C:\Python311\python.exe" (
        set PYTHON_PATH=C:\Python311\python.exe
    ) else if exist "C:\Python310\python.exe" (
        set PYTHON_PATH=C:\Python310\python.exe
    ) else if exist "C:\Python39\python.exe" (
        set PYTHON_PATH=C:\Python39\python.exe
    ) else if exist "C:\Python38\python.exe" (
        set PYTHON_PATH=C:\Python38\python.exe
    ) else if exist "C:\Program Files\Python311\python.exe" (
        set PYTHON_PATH="C:\Program Files\Python311\python.exe"
    ) else if exist "C:\Program Files\Python310\python.exe" (
        set PYTHON_PATH="C:\Program Files\Python310\python.exe"
    ) else if exist "C:\Program Files\Python39\python.exe" (
        set PYTHON_PATH="C:\Program Files\Python39\python.exe"
    ) else if exist "C:\Program Files\Python38\python.exe" (
        set PYTHON_PATH="C:\Program Files\Python38\python.exe"
    ) else if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
        set PYTHON_PATH="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    ) else if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
        set PYTHON_PATH="%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    ) else if exist "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" (
        set PYTHON_PATH="%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
    ) else if exist "%LOCALAPPDATA%\Programs\Python\Python38\python.exe" (
        set PYTHON_PATH="%LOCALAPPDATA%\Programs\Python\Python38\python.exe"
    ) else (
        echo ERROR: Python not found. Please install Python or update your PATH.
        echo You can temporarily disable the pre-commit hook by running:
        echo git commit --no-verify
        exit /b 1
    )
)

echo Using Python: %PYTHON_PATH%

:: Get the repository root directory
set REPO_ROOT=%~dp0..\..

:: Create logs directory if it doesn't exist
if not exist "%REPO_ROOT%\logs" mkdir "%REPO_ROOT%\logs"

:: Run the pre-commit hook script
cd /d "%REPO_ROOT%"
%PYTHON_PATH% "%REPO_ROOT%\src\hooks\run_pre_commit.py"

:: Return the exit code from Python
exit /b %ERRORLEVEL%
