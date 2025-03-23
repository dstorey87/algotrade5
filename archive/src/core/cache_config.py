import os
from pathlib import Path

CENTRAL_CACHE_DIR = Path(os.getenv("DOCKER_CACHE_DIR", "C:/ProgramData/AlgoTradePro5"))
CACHE_LOCATIONS = {
    "docker": CENTRAL_CACHE_DIR / "docker_cache",
    "pip": Path(os.getenv("PIP_CACHE_DIR", CENTRAL_CACHE_DIR / "pip_cache")),
    "models": Path(os.getenv("MODEL_CACHE_DIR", CENTRAL_CACHE_DIR / "model_cache")),
    "builds": Path(os.getenv("BUILD_CACHE_DIR", CENTRAL_CACHE_DIR / "build_cache")),
    "deps": Path(
        os.getenv("DEPENDENCY_CACHE_DIR", CENTRAL_CACHE_DIR / "dependency_cache")
    ),
}


def init_cache_dirs():
    for cache_dir in CACHE_LOCATIONS.values():
        cache_dir.mkdir(parents=True, exist_ok=True)
