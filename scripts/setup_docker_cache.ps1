# Enable BuildKit
$env:DOCKER_BUILDKIT=1
$env:COMPOSE_DOCKER_CLI_BUILD=1
$env:COMPOSE_BAKE=1

# Create cache directories
$cacheDir = "$env:USERPROFILE\.docker\cache\freqai"
New-Item -ItemType Directory -Force -Path $cacheDir
New-Item -ItemType Directory -Force -Path ".\.docker\pip-cache"

# Set cache directory env var
$env:DOCKER_CACHE_DIR="$env:USERPROFILE\.docker\cache"

Write-Host "Docker build cache configured at: $cacheDir"
Write-Host "Pip cache configured at: .\.docker\pip-cache"