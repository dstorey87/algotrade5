"""
Cache Manager
===========

Manages cache operations and statistics for AlgoTradePro5.

CRITICAL REQUIREMENTS:
- Cache usage monitoring
- Cleanup policies
- Size tracking
- Performance optimization
"""

import logging
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from src.core.config_manager import get_config
from src.core.error_manager import ErrorManager, ErrorSeverity

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages cache operations and statistics"""

    def __init__(self):
        """Initialize cache manager"""
        self.config = get_config()
        self.error_manager = ErrorManager()

        # Get workspace paths with defaults
        workspace_root = Path(self.config.get("paths", "BASE_PATH", str(Path.cwd())))
        self.programdata_dir = workspace_root / "docker" / "programdata"
        self.programdata_dir.mkdir(parents=True, exist_ok=True)

        # Cache settings from config
        self.cache_config = {
            "max_size_gb": float(self.config.get("resources", "CACHE_SIZE_LIMIT", 10)),
            "cleanup_threshold": float(
                self.config.get("resources", "CACHE_CLEANUP_THRESHOLD", 0.85)
            ),
            "monitor_interval": int(
                self.config.get("resources", "CACHE_MONITOR_INTERVAL", 300)
            ),
        }

        # Initialize cache directories
        self._init_cache_dirs()
        logger.info("Cache Manager initialized")

    def _init_cache_dirs(self) -> None:
        """Initialize cache directories"""
        cache_types = ["docker", "pip", "model", "build", "dependency"]
        for cache_type in cache_types:
            cache_dir = self.programdata_dir / f"{cache_type}_cache"
            cache_dir.mkdir(parents=True, exist_ok=True)

    def get_cache_stats(self) -> Dict:
        """Get statistics for all cache directories"""
        stats = {}
        try:
            for cache_dir in self.programdata_dir.glob("*_cache"):
                if cache_dir.is_dir():
                    cache_type = cache_dir.name.replace("_cache", "")
                    stats[cache_type] = self._get_dir_stats(cache_dir)
            return stats
        except Exception as e:
            self.error_manager.log_error(
                f"Failed to get cache stats: {e}",
                ErrorSeverity.MEDIUM.value,
                "CacheManager",
            )
            return {}

    def _get_dir_stats(self, path: Path) -> Dict:
        """Get statistics for a directory"""
        try:
            total_size = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
            total_files = sum(1 for _ in path.rglob("*") if _.is_file())
            size_mb = total_size / (1024 * 1024)  # Convert to MB
            size_limit_mb = self.cache_config["max_size_gb"] * 1024  # Convert GB to MB
            usage_percent = (size_mb / size_limit_mb) * 100 if size_limit_mb > 0 else 0

            return {
                "size_mb": size_mb,
                "total_files": total_files,
                "usage_percent": usage_percent,
                "last_access": max(
                    (f.stat().st_atime for f in path.rglob("*") if f.is_file()),
                    default=0,
                ),
            }
        except Exception as e:
            self.error_manager.log_error(
                f"Failed to get directory stats for {path}: {e}",
                ErrorSeverity.LOW.value,
                "CacheManager",
            )
            return {
                "size_mb": 0,
                "total_files": 0,
                "usage_percent": 0,
                "last_access": 0,
            }

    def cleanup_cache(self, cache_type: str) -> bool:
        """Clean up a specific cache directory"""
        try:
            cache_dir = self.programdata_dir / f"{cache_type}_cache"
            if not cache_dir.exists():
                return False

            # Get current stats
            stats = self._get_dir_stats(cache_dir)
            if stats["usage_percent"] <= self.cache_config["cleanup_threshold"]:
                return True

            # Find oldest files
            files = [
                (f, f.stat().st_atime) for f in cache_dir.rglob("*") if f.is_file()
            ]
            files.sort(key=lambda x: x[1])  # Sort by access time

            # Remove oldest files until below threshold
            target_size = (
                self.cache_config["max_size_gb"]
                * 1024
                * self.cache_config["cleanup_threshold"]
            )  # MB

            current_size = stats["size_mb"]
            for file_path, _ in files:
                if current_size <= target_size:
                    break
                try:
                    size = file_path.stat().st_size / (1024 * 1024)  # Convert to MB
                    file_path.unlink()
                    current_size -= size
                except Exception as e:
                    logger.warning(f"Failed to remove cache file {file_path}: {e}")

            return True

        except Exception as e:
            self.error_manager.log_error(
                f"Failed to clean up cache {cache_type}: {e}",
                ErrorSeverity.MEDIUM.value,
                "CacheManager",
            )
            return False

    def clear_cache(self, cache_type: str) -> bool:
        """Clear entire cache directory"""
        try:
            cache_dir = self.programdata_dir / f"{cache_type}_cache"
            if not cache_dir.exists():
                return False

            shutil.rmtree(cache_dir)
            cache_dir.mkdir(parents=True)
            return True

        except Exception as e:
            self.error_manager.log_error(
                f"Failed to clear cache {cache_type}: {e}",
                ErrorSeverity.HIGH.value,
                "CacheManager",
            )
            return False


# Global instance
_cache_manager = None


def get_cache_manager():
    """Get global cache manager instance"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager
