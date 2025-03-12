@echo off
setlocal

:: Set CUDA environment variables
set CUDA_PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8
set CUDA_HOME=%CUDA_PATH%
set PATH=%CUDA_PATH%\bin;%PATH%

REM AlgoTradPro5 Backtesting Launcher
echo ===============================================================================
echo                 AlgoTradPro5 Quantum-Enhanced Backtesting                      
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
) else (
    echo Virtual environment not found, running setup...
    call setup_venv.bat
    if exist "venv\Scripts\activate.bat" (
        call venv\Scripts\activate.bat
    ) else (
        echo Failed to create virtual environment
        exit /b 1
    )
)

REM Process command parameters
set mode=default

if "%1"=="btc" (
    echo Running BTC/USDT backtest for 1 year...
    set mode=btc
) else if "%1"=="eth" (
    echo Running ETH/USDT backtest for 1 year...
    set mode=eth
) else if "%1"=="top5" (
    echo Running top 5 cryptocurrencies backtest...
    set mode=top5
) else if "%1"=="1h" (
    echo Running 1-hour timeframe backtest...
    set mode=1h
) else if "%1"=="daily" (
    echo Running daily timeframe backtest...
    set mode=daily
) else if "%1"=="help" (
    goto :help
)

echo.
echo Checking dependencies...

REM Check for dependency manager and install core dependencies if needed
if exist dependency_manager.py (
    python -c "from dependency_manager import ensure_dependencies; ensure_dependencies(components=['quantitative'])" 2>nul
    if %ERRORLEVEL% neq 0 (
        echo Installing dependencies...
        python dependency_manager.py --components quantitative
    ) else (
        echo Dependencies already installed.
    )
)

echo.
echo Checking required models...

REM Check if ALL required models exist
set MODELS_EXIST=1
if not exist c:\aimodels\llm\Mixtral-8x7B-v0.1-GPTQ (set MODELS_EXIST=0)
if not exist c:\aimodels\llm\openchat_3.5-GPTQ (set MODELS_EXIST=0)
if not exist c:\aimodels\ml\phi-2 (set MODELS_EXIST=0)

if %MODELS_EXIST%==0 (
    echo Required AI models are missing. Running download_models.py...
    python download_models.py
    if %ERRORLEVEL% neq 0 (
        echo Error downloading models. Please run 'python download_models.py' manually.
        pause
        exit /b 1
    )
)

echo All required models found. Starting backtest...
echo.
echo Preparing backtest environment...

REM Run the backtest based on the selected mode
if "%mode%"=="btc" (
    python %~dp0run_backtest.py --pairs BTC/USDT --timerange 20220101-20230101
) else if "%mode%"=="eth" (
    python %~dp0run_backtest.py --pairs ETH/USDT --timerange 20220101-20230101
) else if "%mode%"=="top5" (
    python %~dp0run_backtest.py --pairs BTC/USDT,ETH/USDT,BNB/USDT,XRP/USDT,ADA/USDT --timerange 20220101-20230101
) else if "%mode%"=="1h" (
    python %~dp0run_backtest.py --timeframe 1h --timerange 20210101-20230101
) else if "%mode%"=="daily" (
    python %~dp0run_backtest.py --timeframe 1d --timerange 20180101-20230101
) else (
    REM Default: pass all arguments directly to run_backtest.py
    python %~dp0run_backtest.py %*
)

REM If there's an error, pause to show the message
if %ERRORLEVEL% neq 0 (
    echo.
    echo An error occurred while running the backtest.
    pause
    exit /b 1
)

echo.
echo Backtest completed successfully.
pause
exit /b 0

:help
echo.
echo AlgoTradPro5 Backtesting Options:
echo.
echo   run_backtest.bat btc       - Run BTC/USDT backtest for 1 year
echo   run_backtest.bat eth       - Run ETH/USDT backtest for 1 year
echo   run_backtest.bat top5      - Run top 5 cryptocurrencies backtest
echo   run_backtest.bat 1h        - Run backtest with 1-hour timeframe
echo   run_backtest.bat daily     - Run backtest with daily timeframe
echo.
echo Advanced Usage:
echo   run_backtest.bat --pairs BTC/USDT,ETH/USDT --timerange 20210101-20220101
echo   run_backtest.bat --timeframe 15m --strategy QuantumHybridStrategy
echo.
pause
exit /b 0