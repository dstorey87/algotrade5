import logging
# REMOVED_UNUSED_CODE: import time
# REMOVED_UNUSED_CODE: from collections.abc import Callable

# REMOVED_UNUSED_CODE: from cachetools import TTLCache


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class MeasureTime:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Measure the time of a block of code and call a callback if the time limit is exceeded.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self, callback: Callable[[float, float], None], time_limit: float, ttl: int = 3600 * 4
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         :param callback: The callback to call if the time limit is exceeded.
# REMOVED_UNUSED_CODE:             This callback will be called once every "ttl" seconds,
# REMOVED_UNUSED_CODE:             with the parameters "duration" (in seconds) and
# REMOVED_UNUSED_CODE:             "time limit" - representing the passed in time limit.
# REMOVED_UNUSED_CODE:         :param time_limit: The time limit in seconds.
# REMOVED_UNUSED_CODE:         :param ttl: The time to live of the cache in seconds.
# REMOVED_UNUSED_CODE:             defaults to 4 hours.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self._callback = callback
# REMOVED_UNUSED_CODE:         self._time_limit = time_limit
# REMOVED_UNUSED_CODE:         self.__cache: TTLCache = TTLCache(maxsize=1, ttl=ttl)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __enter__(self):
# REMOVED_UNUSED_CODE:         self._start = time.time()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def __exit__(self, *args):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         end = time.time()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.__cache.get("value"):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         duration = end - self._start
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if duration < self._time_limit:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._callback(duration, self._time_limit)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.__cache["value"] = True
