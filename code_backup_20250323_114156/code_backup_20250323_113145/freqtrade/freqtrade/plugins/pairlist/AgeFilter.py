"""
Minimum age (days listed) pair list filter
"""

import logging
# REMOVED_UNUSED_CODE: from copy import deepcopy
# REMOVED_UNUSED_CODE: from datetime import timedelta

# REMOVED_UNUSED_CODE: from pandas import DataFrame

# REMOVED_UNUSED_CODE: from freqtrade.constants import ListPairsWithTimeframes
# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException
# REMOVED_UNUSED_CODE: from freqtrade.exchange.exchange_types import Tickers
# REMOVED_UNUSED_CODE: from freqtrade.misc import plural
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.plugins.pairlist.IPairList import IPairList, PairlistParameter, SupportsBacktesting
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.util import PeriodicCache, dt_floor_day, dt_now, dt_ts


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class AgeFilter(IPairList):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     supports_backtesting = SupportsBacktesting.NO
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, *args, **kwargs) -> None:
# REMOVED_UNUSED_CODE:         super().__init__(*args, **kwargs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Checked symbols cache (dictionary of ticker symbol => timestamp)
# REMOVED_UNUSED_CODE:         self._symbolsChecked: dict[str, int] = {}
# REMOVED_UNUSED_CODE:         self._symbolsCheckFailed = PeriodicCache(maxsize=1000, ttl=86_400)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._min_days_listed = self._pairlistconfig.get("min_days_listed", 10)
# REMOVED_UNUSED_CODE:         self._max_days_listed = self._pairlistconfig.get("max_days_listed")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         candle_limit = self._exchange.ohlcv_candle_limit("1d", self._config["candle_type_def"])
# REMOVED_UNUSED_CODE:         if self._min_days_listed < 1:
# REMOVED_UNUSED_CODE:             raise OperationalException("AgeFilter requires min_days_listed to be >= 1")
# REMOVED_UNUSED_CODE:         if self._min_days_listed > candle_limit:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "AgeFilter requires min_days_listed to not exceed "
# REMOVED_UNUSED_CODE:                 "exchange max request size "
# REMOVED_UNUSED_CODE:                 f"({candle_limit})"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         if self._max_days_listed and self._max_days_listed <= self._min_days_listed:
# REMOVED_UNUSED_CODE:             raise OperationalException("AgeFilter max_days_listed <= min_days_listed not permitted")
# REMOVED_UNUSED_CODE:         if self._max_days_listed and self._max_days_listed > candle_limit:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "AgeFilter requires max_days_listed to not exceed "
# REMOVED_UNUSED_CODE:                 "exchange max request size "
# REMOVED_UNUSED_CODE:                 f"({candle_limit})"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def needstickers(self) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Boolean property defining if tickers are necessary.
# REMOVED_UNUSED_CODE:         If no Pairlist requires tickers, an empty Dict is passed
# REMOVED_UNUSED_CODE:         as tickers argument to filter_pairlist
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def short_desc(self) -> str:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Short whitelist method description - used for startup-messages
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"{self.name} - Filtering pairs with age less than "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"{self._min_days_listed} {plural(self._min_days_listed, 'day')}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ) + (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (" or more than {self._max_days_listed} {plural(self._max_days_listed, 'day')}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self._max_days_listed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else ""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def description() -> str:
# REMOVED_UNUSED_CODE:         return "Filter pairs by age (days listed)."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def available_parameters() -> dict[str, PairlistParameter]:
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "min_days_listed": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 10,
# REMOVED_UNUSED_CODE:                 "description": "Minimum Days Listed",
# REMOVED_UNUSED_CODE:                 "help": "Minimum number of days a pair must have been listed on the exchange.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "max_days_listed": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": None,
# REMOVED_UNUSED_CODE:                 "description": "Maximum Days Listed",
# REMOVED_UNUSED_CODE:                 "help": "Maximum number of days a pair must have been listed on the exchange.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def filter_pairlist(self, pairlist: list[str], tickers: Tickers) -> list[str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pairlist: pairlist to filter or sort
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param tickers: Tickers (from exchange.get_tickers). May be cached.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: new allowlist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         needed_pairs: ListPairsWithTimeframes = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (p, "1d", self._config["candle_type_def"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for p in pairlist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if p not in self._symbolsChecked and p not in self._symbolsCheckFailed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not needed_pairs:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Remove pairs that have been removed before
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return [p for p in pairlist if p not in self._symbolsCheckFailed]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         since_days = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             -(self._max_days_listed if self._max_days_listed else self._min_days_listed) - 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         since_ms = dt_ts(dt_floor_day(dt_now()) + timedelta(days=since_days))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         candles = self._exchange.refresh_latest_ohlcv(needed_pairs, since_ms=since_ms, cache=False)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._enabled:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for p in deepcopy(pairlist):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 daily_candles = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     candles[(p, "1d", self._config["candle_type_def"])]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     if (p, "1d", self._config["candle_type_def"]) in candles
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     else None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if not self._validate_pair_loc(p, daily_candles):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     pairlist.remove(p)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.log_once(f"Validated {len(pairlist)} pairs.", logger.info)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return pairlist
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _validate_pair_loc(self, pair: str, daily_candles: DataFrame | None) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Validate age for the ticker
# REMOVED_UNUSED_CODE:         :param pair: Pair that's currently validated
# REMOVED_UNUSED_CODE:         :param daily_candles: Downloaded daily candles
# REMOVED_UNUSED_CODE:         :return: True if the pair can stay, false if it should be removed
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Check symbol in cache
# REMOVED_UNUSED_CODE:         if pair in self._symbolsChecked:
# REMOVED_UNUSED_CODE:             return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if daily_candles is not None:
# REMOVED_UNUSED_CODE:             if len(daily_candles) >= self._min_days_listed and (
# REMOVED_UNUSED_CODE:                 not self._max_days_listed or len(daily_candles) <= self._max_days_listed
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 # We have fetched at least the minimum required number of daily candles
# REMOVED_UNUSED_CODE:                 # Add to cache, store the time we last checked this symbol
# REMOVED_UNUSED_CODE:                 self._symbolsChecked[pair] = dt_ts()
# REMOVED_UNUSED_CODE:                 return True
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 self.log_once(
# REMOVED_UNUSED_CODE:                     (
# REMOVED_UNUSED_CODE:                         f"Removed {pair} from whitelist, because age "
# REMOVED_UNUSED_CODE:                         f"{len(daily_candles)} is less than {self._min_days_listed} "
# REMOVED_UNUSED_CODE:                         f"{plural(self._min_days_listed, 'day')}"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     + (
# REMOVED_UNUSED_CODE:                         (
# REMOVED_UNUSED_CODE:                             " or more than "
# REMOVED_UNUSED_CODE:                             f"{self._max_days_listed} {plural(self._max_days_listed, 'day')}"
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:                         if self._max_days_listed
# REMOVED_UNUSED_CODE:                         else ""
# REMOVED_UNUSED_CODE:                     ),
# REMOVED_UNUSED_CODE:                     logger.info,
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 self._symbolsCheckFailed[pair] = dt_ts()
# REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE:         return False
