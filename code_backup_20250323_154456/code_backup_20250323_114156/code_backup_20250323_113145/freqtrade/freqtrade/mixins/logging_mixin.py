from collections.abc import Callable

from cachetools import TTLCache, cached


# REMOVED_UNUSED_CODE: class LoggingMixin:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Logging Mixin
# REMOVED_UNUSED_CODE:     Shows similar messages only once every `refresh_period`.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Disable output completely
# REMOVED_UNUSED_CODE:     show_output = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, logger, refresh_period: int = 3600):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         :param refresh_period: in seconds - Show identical messages in this intervals
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.logger = logger
# REMOVED_UNUSED_CODE:         self.refresh_period = refresh_period
# REMOVED_UNUSED_CODE:         self._log_cache: TTLCache = TTLCache(maxsize=1024, ttl=self.refresh_period)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def log_once(self, message: str, logmethod: Callable) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Logs message - not more often than "refresh_period" to avoid log spamming
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Logs the log-message as debug as well to simplify debugging.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param message: String containing the message to be sent to the function.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param logmethod: Function that'll be called. Most likely `logger.info`.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: None.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         @cached(cache=self._log_cache)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         def _log_once(message: str):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logmethod(message)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Log as debug first
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.logger.debug(message)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Call hidden function.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.show_output:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             _log_once(message)
