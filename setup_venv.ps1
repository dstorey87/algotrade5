# Setup virtual environment for AlgoTradPro5
# Creates Python venv and installs dependencies

Write-Host "`n==============================================================================="
Write-Host "                 AlgoTradPro5 Virtual Environment Setup                         " -ForegroundColor Cyan
Write-Host "===============================================================================`n"

# Check if Python is available
try {
    $pythonVersion = (python --version)
    Write-Host "Found $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "Error: Python not found in PATH. Please install Python 3.9+ and try again." -ForegroundColor Red
    exit 1
}

# Set CUDA environment variables
$env:CUDA_PATH = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8"
$env:CUDA_HOME = $env:CUDA_PATH
$env:Path = "$env:CUDA_PATH\bin;$env:Path"

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if (-not $?) {
        Write-Host "Error: Failed to create virtual environment." -ForegroundColor Red
        exit 1
    }
    Write-Host "Virtual environment created successfully." -ForegroundColor Green
}
else {
    Write-Host "Virtual environment already exists." -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
if (-not $?) {
    Write-Host "Error: Failed to activate virtual environment." -ForegroundColor Red
    exit 1
}
Write-Host "Virtual environment activated." -ForegroundColor Green

# Install core dependencies first
Write-Host "Installing core dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip wheel setuptools
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt

# Install additional CUDA-specific packages
pip install cupy-cuda118
pip install pennylane-lightning-gpu

# Check if dependency_manager.py exists and install from it
if (Test-Path "dependency_manager.py") {
    Write-Host "Installing dependencies using dependency manager..." -ForegroundColor Yellow
    python dependency_manager.py
    if (-not $?) {
        Write-Host "Warning: Dependency manager encountered issues." -ForegroundColor Yellow
        Write-Host "Falling back to requirements files..." -ForegroundColor Yellow
        # Fall back to requirements files if dependency manager fails
        if (Test-Path "requirements.txt") {
            python -m pip install -r requirements.txt
        }
    }
}
else {
    # If no dependency manager, use requirements files
    Write-Host "Installing dependencies from requirements files..." -ForegroundColor Yellow
    if (Test-Path "requirements.txt") {
        python -m pip install -r requirements.txt
    }
    
    # Check for additional requirements files
    if (Test-Path "requirements-full.txt") {
        $installFull = Read-Host "Do you want to install full dependencies (includes AI and quantum)? (y/n)"
        if ($installFull -eq "y") {
            python -m pip install -r requirements-full.txt
        }
    }
}

# Check for GPU support
try {
    python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
    if ($?) {
        Write-Host "PyTorch installation verified." -ForegroundColor Green
    }
}
catch {
    Write-Host "Warning: Could not verify PyTorch installation." -ForegroundColor Yellow
}

Write-Host "`nVirtual environment setup complete!" -ForegroundColor Cyan
Write-Host "To activate the environment, run: .\venv\Scripts\Activate.ps1" -ForegroundColor Green
Write-Host "To deactivate, run: deactivate" -ForegroundColor Green
Write-Host "`nYou may now run AlgoTradPro5 using: python run_algotradpro5.py" -ForegroundColor Cyan