# Create buildx builder instance
docker buildx create --name algotrader-builder --use

# Create cache directories if they don't exist
New-Item -ItemType Directory -Force -Path "$env:TEMP\.buildx-cache"

# Enable BuildKit
$env:DOCKER_BUILDKIT=1
$env:COMPOSE_DOCKER_CLI_BUILD=1

# Set environment variables for compose
$env:DOCKER_DEFAULT_PLATFORM="linux/amd64"

Write-Host "Docker buildx configured successfully. Cache directory: $env:TEMP\.buildx-cache"