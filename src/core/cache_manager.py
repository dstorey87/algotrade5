
import shutil
import logging
from pathlib import Path
from .cache_config import CACHE_LOCATIONS

class CacheManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def verify_cache(self, cache_type):
        """Verify cache exists and is valid"""
        cache_path = CACHE_LOCATIONS.get(cache_type)
        if not cache_path or not cache_path.exists():
            self.logger.warning(f"Cache missing for {cache_type}")
            return False
        return True

    def clear_cache(self, cache_type):
        """Clear specific cache type"""
        cache_path = CACHE_LOCATIONS.get(cache_type)
        if cache_path and cache_path.exists():
            shutil.rmtree(cache_path)
            cache_path.mkdir(parents=True)
            self.logger.info(f"Cleared {cache_type} cache")

    def get_cache_size(self, cache_type):
        """Get size of specific cache"""
        cache_path = CACHE_LOCATIONS.get(cache_type)
        if cache_path and cache_path.exists():
            return sum(f.stat().st_size for f in cache_path.glob('**/*') if f.is_file())
        return 0
