# Initialize dependency manager
Write-Host "Initializing dependency management..."
python src/dependency_manager.py

# Verify dependencies are cached
if (-not (Test-Path "dependencies/site-packages")) {
    Write-Error "Dependencies directory not found or empty. Check dependency manager output."
    exit 1
}

Write-Host "Building Docker container..."
docker-compose build --no-cache

Write-Host "Starting services..."
docker-compose up -d

Write-Host "Checking FreqTrade container status..."
docker ps | Select-String "freqtrade"