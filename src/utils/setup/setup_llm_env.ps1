# Setup script for LLM environment
Write-Host "Setting up LLM environment for AlgoTradePro5..."

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate

# Install LLM dependencies
Write-Host "Installing LLM dependencies..."
pip install -r requirements-llm.txt

# Create models directory structure
Write-Host "Setting up models directory..."
$modelPaths = @(
    "models/llm/openchat_3.5-GPTQ",
    "models/llm/mixtral",
    "models/ml/phi-1.5",
    "models/ml/phi-2"
)

foreach ($path in $modelPaths) {
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force
    }
}

# Verify CUDA availability for PyTorch
Write-Host "Verifying CUDA setup..."
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
if ($LASTEXITCODE -eq 0) {
    Write-Host "PyTorch CUDA verification successful"
} else {
    Write-Host "Warning: CUDA not available for PyTorch"
}

Write-Host "LLM environment setup complete!"