@echo off
REM AlgoTradPro5 System Launcher
echo ===============================================================================
echo                 AlgoTradPro5 Quantum-Enhanced Trading System                      
echo ===============================================================================
echo.

REM Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python not found in PATH. Please install Python 3.9+ and try again.
    pause
    exit /b 1
)

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Process command parameters
set verify_only=0
set skip_checks=0
set docker_mode=0
set backtesting=0
set mode_arg=

:parse_args
if "%1"=="" goto :end_parse_args
if /i "%1"=="--verify-only" (
    set verify_only=1
    set mode_arg=--verify-only
    shift
    goto :parse_args
)
if /i "%1"=="--skip-checks" (
    set skip_checks=1
    set mode_arg=%mode_arg% --skip-checks
    shift
    goto :parse_args
)
if /i "%1"=="--docker" (
    set docker_mode=1
    set mode_arg=--docker
    shift
    goto :parse_args
)
if /i "%1"=="--backtesting" (
    set backtesting=1
    set mode_arg=--backtesting
    shift
    goto :parse_args
)
if /i "%1"=="--timerange" (
    set mode_arg=%mode_arg% --timerange %2
    shift
    shift
    goto :parse_args
)
if /i "%1"=="--logs" (
    set mode_arg=%mode_arg% --logs
    shift
    goto :parse_args
)
if /i "%1"=="--help" (
    goto :help
)

shift
goto :parse_args

:end_parse_args
echo.
echo Checking dependencies...

REM Check for dependency manager and ensure all required components are installed
if exist dependency_manager.py (
    echo Installing dependencies...
    python -c "from dependency_manager import ensure_dependencies; ensure_dependencies(components=['quantitative', 'ai', 'quantum', 'api'])" 2>nul
    if %ERRORLEVEL% neq 0 (
        echo Some dependencies may be missing. Running dependency manager...
        python dependency_manager.py
    ) else (
        echo Dependencies already installed.
    )
) else (
    echo Warning: dependency_manager.py not found. Dependencies may need to be installed manually.
)

REM Check for installation issues
if %verify_only%==1 (
    echo Running verification only...
) else (
    REM Check if all required packages are available before starting
    python -c "import torch; import pennylane; import numpy; import pandas" 2>nul
    if %ERRORLEVEL% neq 0 (
        echo Error: Some core dependencies are missing.
        echo Please run setup_venv.bat first to set up the environment.
        pause
        exit /b 1
    )
)

REM Run the main system
echo.
echo Starting AlgoTradPro5...
echo.

python run_algotradpro5.py %mode_arg%

REM If there's an error, pause to show the message
if %ERRORLEVEL% neq 0 (
    echo.
    echo An error occurred. See above for details.
    pause
    exit /b 1
)

echo.
if %verify_only%==1 (
    echo Verification completed.
) else (
    echo AlgoTradPro5 execution completed successfully.
)

pause
exit /b 0

:help
echo.
echo AlgoTradPro5 Options:
echo.
echo   --verify-only     - Only verify requirements without running
echo   --skip-checks     - Skip verification checks
echo   --docker          - Run using Docker instead of standalone mode
echo   --backtesting     - Run in backtesting mode
echo   --timerange       - Specify timerange for backtesting (format: YYYYMMDD-YYYYMMDD)
echo   --logs            - Follow Docker logs after startup
echo   --help            - Show this help message
echo.
echo Example usage:
echo   run_algotradpro5.bat --backtesting --timerange 20220101-20230101
echo   run_algotradpro5.bat --docker --logs
echo.
pause
exit /b 0