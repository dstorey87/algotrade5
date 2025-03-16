@echo off
setlocal EnableDelayedExpansion

:: Get the repository root directory
cd %~dp0..
set "REPO_ROOT=%CD%"

:: Set Python path from virtual environment
set "PYTHON_PATH=%REPO_ROOT%\.venv\Scripts\python.exe"

:: Get list of staged files
for /f "tokens=*" %%f in ('git diff --cached --name-only') do (
    echo Checking %%f...
    
    :: Check Python files
    if "%%~xf"==".py" (
        echo Running pylint...
        call "%PYTHON_PATH%" -m pylint "%%f"
        if !errorlevel! neq 0 (
            echo Pylint check failed. Please fix the issues using GitHub Copilot.
            exit /b 1
        )
        
        echo Running type checking...
        call "%PYTHON_PATH%" -m mypy "%%f"
        if !errorlevel! neq 0 (
            echo Type checking failed. Please fix the issues using GitHub Copilot.
            exit /b 1
        )
    )
    
    :: Check JavaScript/TypeScript files
    if "%%~xf"==".ts" (
        echo Running ESLint...
        call npx eslint "%%f"
        if !errorlevel! neq 0 (
            echo ESLint check failed. Please fix the issues using GitHub Copilot.
            exit /b 1
        )
    )
)

:: Update documentation
echo Updating documentation...
call "%PYTHON_PATH%" "%REPO_ROOT%\.git\hooks\doc_manager.py"
if !errorlevel! neq 0 (
    echo Documentation update failed.
    exit /b 1
)

echo Pre-commit checks passed successfully!
exit /b 0