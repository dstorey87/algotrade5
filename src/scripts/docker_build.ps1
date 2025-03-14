$ErrorActionPreference = "Stop"
$CacheDir = $env:DOCKER_CACHE_DIR

# Ensure cache directories exist
$cacheDirs = @(
    "$CacheDir/docker_cache",
    "$env:PIP_CACHE_DIR",
    "$env:MODEL_CACHE_DIR",
    "$env:BUILD_CACHE_DIR",
    "$env:DEPENDENCY_CACHE_DIR"
)

foreach ($dir in $cacheDirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir
        Write-Host "Created cache directory: $dir"
    }
}

# Build with cache
Write-Host "Building with cache..."
docker-compose build --build-arg BUILDKIT_INLINE_CACHE=1

# Verify cache
if (Test-Path "$env:BUILD_CACHE_DIR") {
    Write-Host "Build cache verified"
} else {
    Write-Error "Build cache not created properly"
}
