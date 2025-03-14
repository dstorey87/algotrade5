"""
Initialize Cache Monitoring
========================

Initializes and starts the cache monitoring system.

Usage: python init_cache_monitoring.py
"""

import logging
import os
from pathlib import Path
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/cache_monitor.log', encoding='utf-8')
    ]
)

logger = logging.getLogger("AlgoTradePro5")

def ensure_directories():
    """Ensure required directories exist"""
    base_dir = Path(os.getenv('BASE_PATH', 'C:/AlgoTradPro5'))
    cache_dirs = {
        'docker': base_dir / 'docker/programdata/docker_cache',
        'pip': base_dir / 'docker/programdata/pip_cache',
        'model': base_dir / 'docker/programdata/model_cache',
        'build': base_dir / 'docker/programdata/build_cache',
        'dependency': base_dir / 'docker/programdata/dependency_cache'
    }
    
    for name, path in cache_dirs.items():
        try:
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"[OK] Cache directory verified: {name} at {path}")
        except Exception as e:
            logger.error(f"[ERROR] Failed to create cache directory {name}: {e}")
            return False
    return True

def validate_environment():
    """Validate environment variables and paths"""
    required_vars = [
        'BASE_PATH',
        'DOCKER_CACHE_DIR',
        'PIP_CACHE_DIR',
        'MODEL_CACHE_DIR',
        'BUILD_CACHE_DIR',
        'DEPENDENCY_CACHE_DIR'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"[ERROR] Missing environment variables: {', '.join(missing_vars)}")
        return False
        
    logger.info("[OK] Environment variables validated")
    return True

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
            
        logger.info("[OK] Cache monitoring initialized successfully")
        
    except Exception as e:
        logger.error(f"[ERROR] Cache monitoring initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()