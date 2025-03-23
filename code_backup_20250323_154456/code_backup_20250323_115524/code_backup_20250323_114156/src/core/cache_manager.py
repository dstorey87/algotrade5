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
# REMOVED_UNUSED_CODE: import time
# REMOVED_UNUSED_CODE: from datetime import datetime
from pathlib import Path
# REMOVED_UNUSED_CODE: from typing import Dict, Optional

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

# REMOVED_UNUSED_CODE:     def get_cache_stats(self) -> Dict:
# REMOVED_UNUSED_CODE:         """Get statistics for all cache directories"""
# REMOVED_UNUSED_CODE:         stats = {}
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             for cache_dir in self.programdata_dir.glob("*_cache"):
# REMOVED_UNUSED_CODE:                 if cache_dir.is_dir():
# REMOVED_UNUSED_CODE:                     cache_type = cache_dir.name.replace("_cache", "")
# REMOVED_UNUSED_CODE:                     stats[cache_type] = self._get_dir_stats(cache_dir)
# REMOVED_UNUSED_CODE:             return stats
# REMOVED_UNUSED_CODE:         except Exception as e:
# REMOVED_UNUSED_CODE:             self.error_manager.log_error(
# REMOVED_UNUSED_CODE:                 f"Failed to get cache stats: {e}",
# REMOVED_UNUSED_CODE:                 ErrorSeverity.MEDIUM.value,
# REMOVED_UNUSED_CODE:                 "CacheManager",
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             return {}

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

# REMOVED_UNUSED_CODE:     def cleanup_cache(self, cache_type: str) -> bool:
# REMOVED_UNUSED_CODE:         """Clean up a specific cache directory"""
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             cache_dir = self.programdata_dir / f"{cache_type}_cache"
# REMOVED_UNUSED_CODE:             if not cache_dir.exists():
# REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Get current stats
# REMOVED_UNUSED_CODE:             stats = self._get_dir_stats(cache_dir)
# REMOVED_UNUSED_CODE:             if stats["usage_percent"] <= self.cache_config["cleanup_threshold"]:
# REMOVED_UNUSED_CODE:                 return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Find oldest files
# REMOVED_UNUSED_CODE:             files = [
# REMOVED_UNUSED_CODE:                 (f, f.stat().st_atime) for f in cache_dir.rglob("*") if f.is_file()
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE:             files.sort(key=lambda x: x[1])  # Sort by access time
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Remove oldest files until below threshold
# REMOVED_UNUSED_CODE:             target_size = (
# REMOVED_UNUSED_CODE:                 self.cache_config["max_size_gb"]
# REMOVED_UNUSED_CODE:                 * 1024
# REMOVED_UNUSED_CODE:                 * self.cache_config["cleanup_threshold"]
# REMOVED_UNUSED_CODE:             )  # MB
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             current_size = stats["size_mb"]
# REMOVED_UNUSED_CODE:             for file_path, _ in files:
# REMOVED_UNUSED_CODE:                 if current_size <= target_size:
# REMOVED_UNUSED_CODE:                     break
# REMOVED_UNUSED_CODE:                 try:
# REMOVED_UNUSED_CODE:                     size = file_path.stat().st_size / (1024 * 1024)  # Convert to MB
# REMOVED_UNUSED_CODE:                     file_path.unlink()
# REMOVED_UNUSED_CODE:                     current_size -= size
# REMOVED_UNUSED_CODE:                 except Exception as e:
# REMOVED_UNUSED_CODE:                     logger.warning(f"Failed to remove cache file {file_path}: {e}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         except Exception as e:
# REMOVED_UNUSED_CODE:             self.error_manager.log_error(
# REMOVED_UNUSED_CODE:                 f"Failed to clean up cache {cache_type}: {e}",
# REMOVED_UNUSED_CODE:                 ErrorSeverity.MEDIUM.value,
# REMOVED_UNUSED_CODE:                 "CacheManager",
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             return False

# REMOVED_UNUSED_CODE:     def clear_cache(self, cache_type: str) -> bool:
# REMOVED_UNUSED_CODE:         """Clear entire cache directory"""
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             cache_dir = self.programdata_dir / f"{cache_type}_cache"
# REMOVED_UNUSED_CODE:             if not cache_dir.exists():
# REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             shutil.rmtree(cache_dir)
# REMOVED_UNUSED_CODE:             cache_dir.mkdir(parents=True)
# REMOVED_UNUSED_CODE:             return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         except Exception as e:
# REMOVED_UNUSED_CODE:             self.error_manager.log_error(
# REMOVED_UNUSED_CODE:                 f"Failed to clear cache {cache_type}: {e}",
# REMOVED_UNUSED_CODE:                 ErrorSeverity.HIGH.value,
# REMOVED_UNUSED_CODE:                 "CacheManager",
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             return False


# Global instance
_cache_manager = None


# REMOVED_UNUSED_CODE: def get_cache_manager():
# REMOVED_UNUSED_CODE:     """Get global cache manager instance"""
# REMOVED_UNUSED_CODE:     global _cache_manager
# REMOVED_UNUSED_CODE:     if _cache_manager is None:
# REMOVED_UNUSED_CODE:         _cache_manager = CacheManager()
# REMOVED_UNUSED_CODE:     return _cache_manager
