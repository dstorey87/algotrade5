import asyncio
import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar, cast, overload

from freqtrade.constants import ExchangeConfig
from freqtrade.exceptions import DDosProtection, RetryableOrderError, TemporaryError
from freqtrade.mixins import LoggingMixin


logger = logging.getLogger(__name__)
__logging_mixin = None


# REMOVED_UNUSED_CODE: def _reset_logging_mixin():
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Reset global logging mixin - used in tests only.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     global __logging_mixin
# REMOVED_UNUSED_CODE:     __logging_mixin = LoggingMixin(logger)


def _get_logging_mixin():
    # Logging-mixin to cache kucoin responses
    # Only to be used in retrier
    global __logging_mixin
    if not __logging_mixin:
        __logging_mixin = LoggingMixin(logger)
    return __logging_mixin


# Maximum default retry count.
# Functions are always called RETRY_COUNT + 1 times (for the original call)
API_RETRY_COUNT = 4
# REMOVED_UNUSED_CODE: API_FETCH_ORDER_RETRY_COUNT = 5

# REMOVED_UNUSED_CODE: BAD_EXCHANGES = {
# REMOVED_UNUSED_CODE:     "bitmex": "Various reasons.",
# REMOVED_UNUSED_CODE:     "probit": "Requires additional, regular calls to `signIn()`.",
# REMOVED_UNUSED_CODE:     "poloniex": "Does not provide fetch_order endpoint to fetch both open and closed orders.",
# REMOVED_UNUSED_CODE:     "kucoinfutures": "Unsupported futures exchange.",
# REMOVED_UNUSED_CODE:     "poloniexfutures": "Unsupported futures exchange.",
# REMOVED_UNUSED_CODE:     "binancecoinm": "Unsupported futures exchange.",
# REMOVED_UNUSED_CODE: }

# REMOVED_UNUSED_CODE: MAP_EXCHANGE_CHILDCLASS = {
# REMOVED_UNUSED_CODE:     "binanceus": "binance",
# REMOVED_UNUSED_CODE:     "binanceje": "binance",
# REMOVED_UNUSED_CODE:     "binanceusdm": "binance",
# REMOVED_UNUSED_CODE:     "okex": "okx",
# REMOVED_UNUSED_CODE:     "myokx": "okx",
# REMOVED_UNUSED_CODE:     "gateio": "gate",
# REMOVED_UNUSED_CODE:     "huboi": "htx",
# REMOVED_UNUSED_CODE: }

# REMOVED_UNUSED_CODE: SUPPORTED_EXCHANGES = [
# REMOVED_UNUSED_CODE:     "binance",
# REMOVED_UNUSED_CODE:     "bingx",
# REMOVED_UNUSED_CODE:     "bitmart",
# REMOVED_UNUSED_CODE:     "bybit",
# REMOVED_UNUSED_CODE:     "gate",
# REMOVED_UNUSED_CODE:     "htx",
# REMOVED_UNUSED_CODE:     "hyperliquid",
# REMOVED_UNUSED_CODE:     "kraken",
# REMOVED_UNUSED_CODE:     "okx",
# REMOVED_UNUSED_CODE: ]

# either the main, or replacement methods (array) is required
# REMOVED_UNUSED_CODE: EXCHANGE_HAS_REQUIRED: dict[str, list[str]] = {
# REMOVED_UNUSED_CODE:     # Required / private
# REMOVED_UNUSED_CODE:     "fetchOrder": ["fetchOpenOrder", "fetchClosedOrder"],
# REMOVED_UNUSED_CODE:     "fetchL2OrderBook": ["fetchTicker"],
# REMOVED_UNUSED_CODE:     "cancelOrder": [],
# REMOVED_UNUSED_CODE:     "createOrder": [],
# REMOVED_UNUSED_CODE:     "fetchBalance": [],
# REMOVED_UNUSED_CODE:     # Public endpoints
# REMOVED_UNUSED_CODE:     "fetchOHLCV": [],
# REMOVED_UNUSED_CODE: }

# REMOVED_UNUSED_CODE: EXCHANGE_HAS_OPTIONAL = [
# REMOVED_UNUSED_CODE:     # Private
# REMOVED_UNUSED_CODE:     "fetchMyTrades",  # Trades for order - fee detection
# REMOVED_UNUSED_CODE:     "createLimitOrder",
# REMOVED_UNUSED_CODE:     "createMarketOrder",  # Either OR for orders
# REMOVED_UNUSED_CODE:     # 'setLeverage',  # Margin/Futures trading
# REMOVED_UNUSED_CODE:     # 'setMarginMode',  # Margin/Futures trading
# REMOVED_UNUSED_CODE:     # 'fetchFundingHistory', # Futures trading
# REMOVED_UNUSED_CODE:     # Public
# REMOVED_UNUSED_CODE:     "fetchOrderBook",
# REMOVED_UNUSED_CODE:     "fetchL2OrderBook",
# REMOVED_UNUSED_CODE:     "fetchTicker",  # OR for pricing
# REMOVED_UNUSED_CODE:     "fetchTickers",  # For volumepairlist?
# REMOVED_UNUSED_CODE:     "fetchTrades",  # Downloading trades data
# REMOVED_UNUSED_CODE:     # 'fetchFundingRateHistory',  # Futures trading
# REMOVED_UNUSED_CODE:     # 'fetchPositions',  # Futures trading
# REMOVED_UNUSED_CODE:     # 'fetchLeverageTiers',  # Futures initialization
# REMOVED_UNUSED_CODE:     # 'fetchMarketLeverageTiers',  # Futures initialization
# REMOVED_UNUSED_CODE:     # 'fetchOpenOrder', 'fetchClosedOrder',  # replacement for fetchOrder
# REMOVED_UNUSED_CODE:     # 'fetchOpenOrders', 'fetchClosedOrders',  # 'fetchOrders',  # Refinding balance...
# REMOVED_UNUSED_CODE:     # ccxt.pro
# REMOVED_UNUSED_CODE:     "watchOHLCV",
# REMOVED_UNUSED_CODE: ]


# REMOVED_UNUSED_CODE: def remove_exchange_credentials(exchange_config: ExchangeConfig, dry_run: bool) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Removes exchange keys from the configuration and specifies dry-run
# REMOVED_UNUSED_CODE:     Used for backtesting / hyperopt / edge and utils.
# REMOVED_UNUSED_CODE:     Modifies the input dict!
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if dry_run:
# REMOVED_UNUSED_CODE:         exchange_config["key"] = ""
# REMOVED_UNUSED_CODE:         exchange_config["apiKey"] = ""
# REMOVED_UNUSED_CODE:         exchange_config["secret"] = ""
# REMOVED_UNUSED_CODE:         exchange_config["password"] = ""
# REMOVED_UNUSED_CODE:         exchange_config["uid"] = ""


def calculate_backoff(retrycount, max_retries):
    """
    Calculate backoff
    """
    return (max_retries - retrycount) ** 2 + 1


# REMOVED_UNUSED_CODE: def retrier_async(f):
# REMOVED_UNUSED_CODE:     async def wrapper(*args, **kwargs):
# REMOVED_UNUSED_CODE:         count = kwargs.pop("count", API_RETRY_COUNT)
# REMOVED_UNUSED_CODE:         kucoin = args[0].name == "KuCoin"  # Check if the exchange is KuCoin.
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             return await f(*args, **kwargs)
# REMOVED_UNUSED_CODE:         except TemporaryError as ex:
# REMOVED_UNUSED_CODE:             msg = f'{f.__name__}() returned exception: "{ex}". '
# REMOVED_UNUSED_CODE:             if count > 0:
# REMOVED_UNUSED_CODE:                 msg += f"Retrying still for {count} times."
# REMOVED_UNUSED_CODE:                 count -= 1
# REMOVED_UNUSED_CODE:                 kwargs["count"] = count
# REMOVED_UNUSED_CODE:                 if isinstance(ex, DDosProtection):
# REMOVED_UNUSED_CODE:                     if kucoin and "429000" in str(ex):
# REMOVED_UNUSED_CODE:                         # Temporary fix for 429000 error on kucoin
# REMOVED_UNUSED_CODE:                         # see https://github.com/freqtrade/freqtrade/issues/5700 for details.
# REMOVED_UNUSED_CODE:                         _get_logging_mixin().log_once(
# REMOVED_UNUSED_CODE:                             f"Kucoin 429 error, avoid triggering DDosProtection backoff delay. "
# REMOVED_UNUSED_CODE:                             f"{count} tries left before giving up",
# REMOVED_UNUSED_CODE:                             logmethod=logger.warning,
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:                         # Reset msg to avoid logging too many times.
# REMOVED_UNUSED_CODE:                         msg = ""
# REMOVED_UNUSED_CODE:                     else:
# REMOVED_UNUSED_CODE:                         backoff_delay = calculate_backoff(count + 1, API_RETRY_COUNT)
# REMOVED_UNUSED_CODE:                         logger.info(f"Applying DDosProtection backoff delay: {backoff_delay}")
# REMOVED_UNUSED_CODE:                         await asyncio.sleep(backoff_delay)
# REMOVED_UNUSED_CODE:                 if msg:
# REMOVED_UNUSED_CODE:                     logger.warning(msg)
# REMOVED_UNUSED_CODE:                 return await wrapper(*args, **kwargs)
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 logger.warning(msg + "Giving up.")
# REMOVED_UNUSED_CODE:                 raise ex
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return wrapper


F = TypeVar("F", bound=Callable[..., Any])


# Type shenanigans
# REMOVED_UNUSED_CODE: @overload
def retrier(_func: F) -> F: ...


# REMOVED_UNUSED_CODE: @overload
def retrier(_func: F, *, retries=API_RETRY_COUNT) -> F: ...


# REMOVED_UNUSED_CODE: @overload
def retrier(*, retries=API_RETRY_COUNT) -> Callable[[F], F]: ...


# REMOVED_UNUSED_CODE: def retrier(_func: F | None = None, *, retries=API_RETRY_COUNT):
# REMOVED_UNUSED_CODE:     def decorator(f: F) -> F:
# REMOVED_UNUSED_CODE:         @wraps(f)
# REMOVED_UNUSED_CODE:         def wrapper(*args, **kwargs):
# REMOVED_UNUSED_CODE:             count = kwargs.pop("count", retries)
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 return f(*args, **kwargs)
# REMOVED_UNUSED_CODE:             except (TemporaryError, RetryableOrderError) as ex:
# REMOVED_UNUSED_CODE:                 msg = f'{f.__name__}() returned exception: "{ex}". '
# REMOVED_UNUSED_CODE:                 if count > 0:
# REMOVED_UNUSED_CODE:                     logger.warning(msg + f"Retrying still for {count} times.")
# REMOVED_UNUSED_CODE:                     count -= 1
# REMOVED_UNUSED_CODE:                     kwargs.update({"count": count})
# REMOVED_UNUSED_CODE:                     if isinstance(ex, DDosProtection | RetryableOrderError):
# REMOVED_UNUSED_CODE:                         # increasing backoff
# REMOVED_UNUSED_CODE:                         backoff_delay = calculate_backoff(count + 1, retries)
# REMOVED_UNUSED_CODE:                         logger.info(f"Applying DDosProtection backoff delay: {backoff_delay}")
# REMOVED_UNUSED_CODE:                         time.sleep(backoff_delay)
# REMOVED_UNUSED_CODE:                     return wrapper(*args, **kwargs)
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     logger.warning(msg + "Giving up.")
# REMOVED_UNUSED_CODE:                     raise ex
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return cast(F, wrapper)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Support both @retrier and @retrier(retries=2) syntax
# REMOVED_UNUSED_CODE:     if _func is None:
# REMOVED_UNUSED_CODE:         return decorator
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         return decorator(_func)
