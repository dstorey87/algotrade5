@echo off
:: This script must be run as administrator
echo Checking for administrator privileges...
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires administrator privileges.
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo Setting CUDA 11.8 environment variables...

:: Set CUDA environment variables
setx CUDA_PATH "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8" /M
setx CUDA_HOME "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8" /M

:: Add CUDA bin to PATH if not already present
set "CUDA_BIN=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin"
echo %PATH% | find /i "%CUDA_BIN%" > nul
if errorlevel 1 (
    setx PATH "%PATH%;%CUDA_BIN%" /M
)

echo.
echo CUDA environment variables have been set.
echo Please restart your terminal for changes to take effect.
echo.
pause
