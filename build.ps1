#!/usr/bin/env pwsh
# Build script for AlgoTradePro5
# Handles dependency caching and Docker builds

# Ensure we're in the project root
$ProjectRoot = $PSScriptRoot

Write-Host "Caching dependencies..." -ForegroundColor Cyan
python scripts/cache_dependencies.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to cache dependencies"
    exit 1
}

Write-Host "Building Docker image..." -ForegroundColor Cyan
docker-compose build --no-cache
if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker build failed"
    exit 1
}

Write-Host "Starting services..." -ForegroundColor Cyan
docker-compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to start services"
    exit 1
}

Write-Host "Waiting for FreqTrade API..." -ForegroundColor Cyan
$attempts = 0
$maxAttempts = 30
do {
    $attempts++
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8080/api/v1/ping" -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "FreqTrade API is ready!" -ForegroundColor Green
            exit 0
        }
    }
    catch {
        Write-Host "." -NoNewline
        Start-Sleep -Seconds 2
    }
} while ($attempts -lt $maxAttempts)

Write-Error "FreqTrade API failed to respond in time"
exit 1
