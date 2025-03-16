# Setup virtual environment for AlgoTradPro5
Write-Host "Setting up virtual environment..." -ForegroundColor Green

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Green
pip install -r requirements-full.txt

Write-Host "Setting up FreqTrade environment..." -ForegroundColor Green

# Initialize FreqTrade user directory if it doesn't exist
if (-not (Test-Path ".\freqtrade\user_data")) {
    mkdir .\freqtrade\user_data
    mkdir .\freqtrade\user_data\strategies
}

Write-Host "Setup completed successfully!" -ForegroundColor Green
