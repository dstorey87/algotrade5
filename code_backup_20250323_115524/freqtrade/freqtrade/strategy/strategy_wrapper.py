import logging
# REMOVED_UNUSED_CODE: from collections.abc import Callable
# REMOVED_UNUSED_CODE: from copy import deepcopy
# REMOVED_UNUSED_CODE: from functools import wraps
# REMOVED_UNUSED_CODE: from typing import Any, TypeVar, cast

# REMOVED_UNUSED_CODE: from freqtrade.exceptions import StrategyError


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: F = TypeVar("F", bound=Callable[..., Any])


# REMOVED_UNUSED_CODE: def strategy_safe_wrapper(f: F, message: str = "", default_retval=None, supress_error=False) -> F:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Wrapper around user-provided methods and functions.
# REMOVED_UNUSED_CODE:     Caches all exceptions and returns either the default_retval (if it's not None) or raises
# REMOVED_UNUSED_CODE:     a StrategyError exception, which then needs to be handled by the calling method.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @wraps(f)
# REMOVED_UNUSED_CODE:     def wrapper(*args, **kwargs):
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             if not (getattr(f, "__qualname__", "")).startswith("IStrategy."):
# REMOVED_UNUSED_CODE:                 # Don't deep-copy if the function is not implemented in the user strategy.``
# REMOVED_UNUSED_CODE:                 if "trade" in kwargs:
# REMOVED_UNUSED_CODE:                     # Protect accidental modifications from within the strategy
# REMOVED_UNUSED_CODE:                     kwargs["trade"] = deepcopy(kwargs["trade"])
# REMOVED_UNUSED_CODE:             return f(*args, **kwargs)
# REMOVED_UNUSED_CODE:         except ValueError as error:
# REMOVED_UNUSED_CODE:             logger.warning(f"{message}Strategy caused the following exception: {error}{f}")
# REMOVED_UNUSED_CODE:             if default_retval is None and not supress_error:
# REMOVED_UNUSED_CODE:                 raise StrategyError(str(error)) from error
# REMOVED_UNUSED_CODE:             return default_retval
# REMOVED_UNUSED_CODE:         except Exception as error:
# REMOVED_UNUSED_CODE:             logger.exception(f"{message}Unexpected error {error} calling {f}")
# REMOVED_UNUSED_CODE:             if default_retval is None and not supress_error:
# REMOVED_UNUSED_CODE:                 raise StrategyError(str(error)) from error
# REMOVED_UNUSED_CODE:             return default_retval
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return cast(F, wrapper)
