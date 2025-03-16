"""
Initialize Cache Monitoring
========================

Initializes and starts the cache monitoring system.

Usage: python init_cache_monitoring.py
"""

import logging
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.config_manager import get_config
from src.core.error_manager import ErrorManager, ErrorSeverity
from src.services.cache_monitor_service import get_cache_monitor_service

# Configure logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("AlgoTradePro5")


def ensure_directories() -> bool:
    """Ensure required directories exist"""
    try:
        config = get_config()
        base_dir = Path(config.get("paths", "BASE_PATH", str(project_root)))
        programdata_dir = base_dir / "docker" / "programdata"

        cache_dirs = {
            "docker": programdata_dir / "docker_cache",
            "pip": programdata_dir / "pip_cache",
            "model": programdata_dir / "model_cache",
            "build": programdata_dir / "build_cache",
            "dependency": programdata_dir / "dependency_cache",
        }

        for name, path in cache_dirs.items():
            try:
                path.mkdir(parents=True, exist_ok=True)
                logger.info(f"[OK] Cache directory verified: {name} at {path}")
            except Exception as e:
                logger.error(f"[ERROR] Failed to create cache directory {name}: {e}")
                return False
        return True
    except Exception as e:
        logger.error(f"[ERROR] Failed to initialize cache directories: {e}")
        return False


def validate_environment() -> bool:
    """Validate environment variables and paths"""
    try:
        config = get_config()
        required_paths = ["BASE_PATH", "DATA_DIR", "LOG_DIR"]

        for path_key in required_paths:
            path = Path(
                config.get("paths", path_key, str(project_root / path_key.lower()))
            )
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
                logger.info(f"[OK] Created required directory: {path}")

        return True

    except Exception as e:
        logger.error(f"[ERROR] Environment validation failed: {e}")
        return False


def main():
    """Initialize and validate cache monitoring"""
    try:
        logger.info("Starting cache monitoring initialization...")

        # Validate environment
        if not validate_environment():
            logger.error("[ERROR] Environment validation failed")
            sys.exit(1)

        # Ensure directories exist
        if not ensure_directories():
            logger.error("[ERROR] Directory creation failed")
            sys.exit(1)

        # Initialize cache monitoring service
        monitor_service = get_cache_monitor_service()
        monitor_service.start()

        logger.info("[OK] Cache monitoring initialized successfully")
        return True

    except Exception as e:
        logger.error(f"[ERROR] Cache monitoring initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
