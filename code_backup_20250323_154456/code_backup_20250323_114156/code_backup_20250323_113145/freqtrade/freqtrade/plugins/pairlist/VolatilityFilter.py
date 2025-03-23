"""
Volatility pairlist filter
"""

import logging
import sys
from datetime import timedelta

import numpy as np
from cachetools import TTLCache
from pandas import DataFrame

from freqtrade.constants import ListPairsWithTimeframes
from freqtrade.exceptions import OperationalException
from freqtrade.exchange.exchange_types import Tickers
from freqtrade.misc import plural
from freqtrade.plugins.pairlist.IPairList import IPairList, PairlistParameter, SupportsBacktesting
from freqtrade.util import dt_floor_day, dt_now, dt_ts


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class VolatilityFilter(IPairList):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Filters pairs by volatility
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     supports_backtesting = SupportsBacktesting.NO
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, *args, **kwargs) -> None:
# REMOVED_UNUSED_CODE:         super().__init__(*args, **kwargs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._days = self._pairlistconfig.get("lookback_days", 10)
# REMOVED_UNUSED_CODE:         self._min_volatility = self._pairlistconfig.get("min_volatility", 0)
# REMOVED_UNUSED_CODE:         self._max_volatility = self._pairlistconfig.get("max_volatility", sys.maxsize)
# REMOVED_UNUSED_CODE:         self._refresh_period = self._pairlistconfig.get("refresh_period", 1440)
# REMOVED_UNUSED_CODE:         self._def_candletype = self._config["candle_type_def"]
# REMOVED_UNUSED_CODE:         self._sort_direction: str | None = self._pairlistconfig.get("sort_direction", None)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._pair_cache: TTLCache = TTLCache(maxsize=1000, ttl=self._refresh_period)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         candle_limit = self._exchange.ohlcv_candle_limit("1d", self._config["candle_type_def"])
# REMOVED_UNUSED_CODE:         if self._days < 1:
# REMOVED_UNUSED_CODE:             raise OperationalException("VolatilityFilter requires lookback_days to be >= 1")
# REMOVED_UNUSED_CODE:         if self._days > candle_limit:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "VolatilityFilter requires lookback_days to not "
# REMOVED_UNUSED_CODE:                 f"exceed exchange max request size ({candle_limit})"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         if self._sort_direction not in [None, "asc", "desc"]:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "VolatilityFilter requires sort_direction to be "
# REMOVED_UNUSED_CODE:                 "either None (undefined), 'asc' or 'desc'"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def needstickers(self) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Boolean property defining if tickers are necessary.
# REMOVED_UNUSED_CODE:         If no Pairlist requires tickers, an empty List is passed
# REMOVED_UNUSED_CODE:         as tickers argument to filter_pairlist
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def short_desc(self) -> str:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Short whitelist method description - used for startup-messages
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"{self.name} - Filtering pairs with volatility range "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"{self._min_volatility}-{self._max_volatility} "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f" the last {self._days} {plural(self._days, 'day')}."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def description() -> str:
# REMOVED_UNUSED_CODE:         return "Filter pairs by their recent volatility."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def available_parameters() -> dict[str, PairlistParameter]:
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "lookback_days": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 10,
# REMOVED_UNUSED_CODE:                 "description": "Lookback Days",
# REMOVED_UNUSED_CODE:                 "help": "Number of days to look back at.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "min_volatility": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 0,
# REMOVED_UNUSED_CODE:                 "description": "Minimum Volatility",
# REMOVED_UNUSED_CODE:                 "help": "Minimum volatility a pair must have to be considered.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "max_volatility": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": None,
# REMOVED_UNUSED_CODE:                 "description": "Maximum Volatility",
# REMOVED_UNUSED_CODE:                 "help": "Maximum volatility a pair must have to be considered.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "sort_direction": {
# REMOVED_UNUSED_CODE:                 "type": "option",
# REMOVED_UNUSED_CODE:                 "default": None,
# REMOVED_UNUSED_CODE:                 "options": ["", "asc", "desc"],
# REMOVED_UNUSED_CODE:                 "description": "Sort pairlist",
# REMOVED_UNUSED_CODE:                 "help": "Sort Pairlist ascending or descending by volatility.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             **IPairList.refresh_period_parameter(),
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def filter_pairlist(self, pairlist: list[str], tickers: Tickers) -> list[str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Validate trading range
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pairlist: pairlist to filter or sort
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param tickers: Tickers (from exchange.get_tickers). May be cached.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: new allowlist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         needed_pairs: ListPairsWithTimeframes = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (p, "1d", self._def_candletype) for p in pairlist if p not in self._pair_cache
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         since_ms = dt_ts(dt_floor_day(dt_now()) - timedelta(days=self._days))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         candles = self._exchange.refresh_ohlcv_with_cache(needed_pairs, since_ms=since_ms)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         resulting_pairlist: list[str] = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         volatilitys: dict[str, float] = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for p in pairlist:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             daily_candles = candles.get((p, "1d", self._def_candletype), None)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             volatility_avg = self._calculate_volatility(p, daily_candles)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if volatility_avg is not None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if self._validate_pair_loc(p, volatility_avg):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     resulting_pairlist.append(p)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     volatilitys[p] = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         volatility_avg if volatility_avg and not np.isnan(volatility_avg) else 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.log_once(f"Removed {p} from whitelist, no candles found.", logger.info)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._sort_direction:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             resulting_pairlist = sorted(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 resulting_pairlist,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 key=lambda p: volatilitys[p],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 reverse=self._sort_direction == "desc",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return resulting_pairlist
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _calculate_volatility(self, pair: str, daily_candles: DataFrame) -> float | None:
# REMOVED_UNUSED_CODE:         # Check symbol in cache
# REMOVED_UNUSED_CODE:         if (volatility_avg := self._pair_cache.get(pair, None)) is not None:
# REMOVED_UNUSED_CODE:             return volatility_avg
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if daily_candles is not None and not daily_candles.empty:
# REMOVED_UNUSED_CODE:             returns = np.log(daily_candles["close"].shift(1) / daily_candles["close"])
# REMOVED_UNUSED_CODE:             returns.fillna(0, inplace=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             volatility_series = returns.rolling(window=self._days).std() * np.sqrt(self._days)
# REMOVED_UNUSED_CODE:             volatility_avg = volatility_series.mean()
# REMOVED_UNUSED_CODE:             self._pair_cache[pair] = volatility_avg
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             return volatility_avg
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _validate_pair_loc(self, pair: str, volatility_avg: float) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Validate trading range
# REMOVED_UNUSED_CODE:         :param pair: Pair that's currently validated
# REMOVED_UNUSED_CODE:         :param volatility_avg: Average volatility
# REMOVED_UNUSED_CODE:         :return: True if the pair can stay, false if it should be removed
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._min_volatility <= volatility_avg <= self._max_volatility:
# REMOVED_UNUSED_CODE:             result = True
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             self.log_once(
# REMOVED_UNUSED_CODE:                 f"Removed {pair} from whitelist, because volatility "
# REMOVED_UNUSED_CODE:                 f"over {self._days} {plural(self._days, 'day')} "
# REMOVED_UNUSED_CODE:                 f"is: {volatility_avg:.3f} "
# REMOVED_UNUSED_CODE:                 f"which is not in the configured range of "
# REMOVED_UNUSED_CODE:                 f"{self._min_volatility}-{self._max_volatility}.",
# REMOVED_UNUSED_CODE:                 logger.info,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             result = False
# REMOVED_UNUSED_CODE:         return result
