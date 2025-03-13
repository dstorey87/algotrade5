@echo off
REM AlgoTradPro5 Virtual Environment Setup
echo ===============================================================================
echo                  AlgoTradPro5 Virtual Environment Setup
echo ===============================================================================
echo.

REM Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python not found in PATH. Please install Python 3.9+ and try again.
    pause
    exit /b 1
)

FOR /F "tokens=* USEBACKQ" %%F IN (`python --version`) DO (
    SET python_version=%%F
)
echo Found %python_version%

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo Error: Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to activate virtual environment.
    pause
    exit /b 1
)
echo Virtual environment activated.

REM Install core dependencies first
echo Installing core dependencies...
python -m pip install --upgrade pip wheel setuptools
python -m pip install jsonschema attrs pyrsistent

REM Check if dependency_manager.py exists and install from it
if exist dependency_manager.py (
    echo Installing dependencies using dependency manager...
    python dependency_manager.py
    if %ERRORLEVEL% neq 0 (
        echo Warning: Dependency manager encountered issues.
        echo Falling back to requirements files...
        REM Fall back to requirements files if dependency manager fails
        if exist requirements.txt (
            python -m pip install -r requirements.txt
        )
    )
) else (
    REM If no dependency manager, use requirements files
    echo Installing dependencies from requirements files...
    if exist requirements.txt (
        python -m pip install -r requirements.txt
    )
    
    REM Check for additional requirements files
    if exist requirements-full.txt (
        set /p install_full="Do you want to install full dependencies (includes AI and quantum)? (y/n): "
        if /I "%install_full%"=="y" (
            python -m pip install -r requirements-full.txt
        )
    )
)

REM Check for GPU support
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')" 2>nul
if %ERRORLEVEL% == 0 (
    echo PyTorch installation verified.
) else (
    echo Warning: Could not verify PyTorch installation.
)

echo.
echo Virtual environment setup complete!
echo To activate the environment, run: venv\Scripts\activate.bat
echo To deactivate, run: deactivate
echo.
echo You may now run AlgoTradPro5 using: python run_algotradpro5.py
echo.
pause