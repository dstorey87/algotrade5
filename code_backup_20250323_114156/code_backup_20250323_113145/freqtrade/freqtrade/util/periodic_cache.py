# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import datetime, timezone

# REMOVED_UNUSED_CODE: from cachetools import TTLCache


# REMOVED_UNUSED_CODE: class PeriodicCache(TTLCache):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Special cache that expires at "straight" times
# REMOVED_UNUSED_CODE:     A timer with ttl of 3600 (1h) will expire at every full hour (:00).
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, maxsize, ttl, getsizeof=None):
# REMOVED_UNUSED_CODE:         def local_timer():
# REMOVED_UNUSED_CODE:             ts = datetime.now(timezone.utc).timestamp()
# REMOVED_UNUSED_CODE:             offset = ts % ttl
# REMOVED_UNUSED_CODE:             return ts - offset
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Init with smlight offset
# REMOVED_UNUSED_CODE:         super().__init__(maxsize=maxsize, ttl=ttl - 1e-5, timer=local_timer, getsizeof=getsizeof)
