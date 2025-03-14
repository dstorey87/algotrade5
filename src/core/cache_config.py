import os
from pathlib import Path

CENTRAL_CACHE_DIR = Path("C:/ProgramData/AlgoTradePro5")
CACHE_LOCATIONS = {
    "docker": CENTRAL_CACHE_DIR / "docker_cache",
    "pip": CENTRAL_CACHE_DIR / "pip_cache",
    "models": CENTRAL_CACHE_DIR / "model_cache",
    "builds": CENTRAL_CACHE_DIR / "build_cache",
    "deps": CENTRAL_CACHE_DIR / "dependency_cache"
}

def init_cache_dirs():
    for cache_dir in CACHE_LOCATIONS.values():
        cache_dir.mkdir(parents=True, exist_ok=True)
