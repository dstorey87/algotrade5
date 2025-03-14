"""
Cache Management System
===================

Handles all caching operations, monitoring, and cleanup for AlgoTradePro5.

CRITICAL REQUIREMENTS:
- Cache size monitoring
- Automatic cleanup
- Cache performance tracking
- Resource optimization
"""

import logging
import os
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import json
import psutil

from src.core.config_manager import get_config
from src.core.error_manager import ErrorManager, ErrorSeverity

logger = logging.getLogger(__name__)

class CacheManager:
    """Manages all system caching operations"""
    
    def __init__(self):
        """Initialize cache management system"""
        self.config = get_config()
        self.error_manager = ErrorManager()
        
        # Get workspace root from config
        workspace_root = Path(self.config.get('paths', 'BASE_PATH'))
        programdata_dir = workspace_root / 'docker' / 'programdata'
        
        # Load cache paths from environment, falling back to workspace paths
        self.cache_paths = {
            'docker': Path(os.getenv('DOCKER_CACHE_DIR', programdata_dir / 'docker_cache')),
            'pip': Path(os.getenv('PIP_CACHE_DIR', programdata_dir / 'pip_cache')),
            'model': Path(os.getenv('MODEL_CACHE_DIR', programdata_dir / 'model_cache')),
            'build': Path(os.getenv('BUILD_CACHE_DIR', programdata_dir / 'build_cache')),
            'dependency': Path(os.getenv('DEPENDENCY_CACHE_DIR', programdata_dir / 'dependency_cache'))
        }
        
        # Cache size limits in MB
        self.cache_limits = {
            'docker': 5000,    # 5GB
            'pip': 2000,       # 2GB
            'model': 10000,    # 10GB
            'build': 1000,     # 1GB
            'dependency': 500   # 500MB
        }
        
        # Initialize cache directories
        self._init_cache_dirs()
        
        # Cache statistics
        self.cache_stats = {}
        self.last_cleanup = {}
        
        # Load initial statistics
        self._update_cache_stats()
        
        logger.info("Cache Manager initialized with workspace paths")
        
    def _init_cache_dirs(self) -> None:
        """Initialize cache directories"""
        for cache_type, path in self.cache_paths.items():
            try:
                path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Cache directory verified: {cache_type}")
            except Exception as e:
                self.error_manager.log_error(
                    f"Failed to create cache directory for {cache_type}: {e}",
                    ErrorSeverity.HIGH.value,
                    "CacheManager"
                )
                
    def _update_cache_stats(self) -> None:
        """Update cache usage statistics"""
        for cache_type, path in self.cache_paths.items():
            if path.exists():
                total_size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
                total_files = sum(1 for _ in path.rglob('*') if _.is_file())
                oldest_file = min((f.stat().st_mtime, f) for f in path.rglob('*') if f.is_file())[1] if total_files > 0 else None
                
                self.cache_stats[cache_type] = {
                    'size_mb': total_size / (1024 * 1024),
                    'total_files': total_files,
                    'last_accessed': datetime.fromtimestamp(oldest_file.stat().st_atime).isoformat() if oldest_file else None,
                    'usage_percent': (total_size / (1024 * 1024)) / self.cache_limits[cache_type] * 100
                }
                
    def get_cache_stats(self) -> Dict:
        """Get current cache statistics"""
        self._update_cache_stats()
        return self.cache_stats
        
    def cleanup_cache(self, cache_type: Optional[str] = None, force: bool = False) -> bool:
        """Clean up cache directories based on size limits and age"""
        cache_types = [cache_type] if cache_type else self.cache_paths.keys()
        
        for c_type in cache_types:
            if c_type not in self.cache_paths:
                logger.warning(f"Invalid cache type: {c_type}")
                continue
                
            path = self.cache_paths[c_type]
            if not path.exists():
                continue
                
            try:
                # Get current cache size
                current_size = self.cache_stats[c_type]['size_mb']
                
                # Check if cleanup is needed
                if force or current_size > self.cache_limits[c_type]:
                    logger.info(f"Cleaning up {c_type} cache...")
                    
                    # Get list of files sorted by last access time
                    files = sorted(
                        ((f, f.stat()) for f in path.rglob('*') if f.is_file()),
                        key=lambda x: x[1].st_atime
                    )
                    
                    # Remove oldest files until under limit
                    for file, _ in files:
                        if current_size <= self.cache_limits[c_type] * 0.8 and not force:
                            break
                            
                        try:
                            size = file.stat().st_size / (1024 * 1024)
                            file.unlink()
                            current_size -= size
                            logger.debug(f"Removed cache file: {file.name}")
                        except Exception as e:
                            logger.warning(f"Failed to remove cache file {file}: {e}")
                            
                    self.last_cleanup[c_type] = datetime.now()
                    self._update_cache_stats()
                    
            except Exception as e:
                self.error_manager.log_error(
                    f"Cache cleanup failed for {c_type}: {e}",
                    ErrorSeverity.MEDIUM.value,
                    "CacheManager"
                )
                return False
                
        return True
        
    def monitor_cache_usage(self) -> Dict:
        """Monitor cache usage and trigger cleanup if needed"""
        self._update_cache_stats()
        alerts = {}
        
        for cache_type, stats in self.cache_stats.items():
            usage = stats['usage_percent']
            if usage > 90:
                alerts[cache_type] = {
                    'severity': 'HIGH',
                    'message': f"Cache usage critical: {usage:.1f}%",
                    'action': 'Immediate cleanup required'
                }
                self.cleanup_cache(cache_type)
            elif usage > 80:
                alerts[cache_type] = {
                    'severity': 'MEDIUM',
                    'message': f"Cache usage high: {usage:.1f}%",
                    'action': 'Monitoring'
                }
                
        return alerts

# Global instance
_cache_manager = None

def get_cache_manager():
    """Get global cache manager instance"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager