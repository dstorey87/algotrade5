$ErrorActionPreference = "Stop"
$CacheDir = "C:/ProgramData/AlgoTradePro5"

# Ensure cache directories exist
$cacheDirs = @(
    "$CacheDir/docker_cache",
    "$CacheDir/pip_cache",
    "$CacheDir/model_cache",
    "$CacheDir/build_cache",
    "$CacheDir/dependency_cache"
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
if (Test-Path "$CacheDir/build_cache") {
    Write-Host "Build cache verified"
} else {
    Write-Error "Build cache not created properly"
}
