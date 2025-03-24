#!/usr/bin/env pwsh
# Build script for AlgoTradePro5
# Handles dependency caching and Docker builds

# Ensure we're in the project root
$ProjectRoot = $PSScriptRoot

# Enable BuildKit for all docker commands
$env:DOCKER_BUILDKIT = 1

# Create required directories
New-Item -ItemType Directory -Force -Path "./docker/buildcache"
New-Item -ItemType Directory -Force -Path "./docker/frontend_buildcache"
New-Item -ItemType Directory -Force -Path "./docker/programdata/pip_cache"

Write-Host "Caching dependencies..." -ForegroundColor Cyan
python scripts/cache_dependencies.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to cache dependencies"
    exit 1
}

# Build FreqAI image with caching
Write-Host "Building FreqAI image..."
docker build `
    --build-arg BUILDKIT_INLINE_CACHE=1 `
    --cache-from type=local,src=./docker/buildcache `
    --cache-to type=local,dest=./docker/buildcache,mode=max `
    -t algotradpro5-freqai:latest `
    -f Dockerfile.freqai-custom .

# Build frontend image with caching
Write-Host "Building frontend image..."
docker build `
    --build-arg BUILDKIT_INLINE_CACHE=1 `
    --cache-from type=local,src=./docker/frontend_buildcache `
    --cache-to type=local,dest=./docker/frontend_buildcache,mode=max `
    -t algotradpro5-frontend:latest `
    -f frontend/Dockerfile ./frontend

Write-Host "Building Docker image..." -ForegroundColor Cyan
docker-compose build --no-cache
if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker build failed"
    exit 1
}

Write-Host "Build complete. Starting containers..."
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
