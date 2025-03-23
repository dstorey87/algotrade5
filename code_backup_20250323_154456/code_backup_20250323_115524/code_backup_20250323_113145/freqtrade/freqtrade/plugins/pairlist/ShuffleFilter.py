"""
Shuffle pair list filter
"""

import logging
import random
from typing import Literal

from freqtrade.enums import RunMode
from freqtrade.exchange import timeframe_to_seconds
from freqtrade.exchange.exchange_types import Tickers
from freqtrade.plugins.pairlist.IPairList import IPairList, PairlistParameter, SupportsBacktesting
from freqtrade.util.periodic_cache import PeriodicCache


logger = logging.getLogger(__name__)

ShuffleValues = Literal["candle", "iteration"]


# REMOVED_UNUSED_CODE: class ShuffleFilter(IPairList):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     supports_backtesting = SupportsBacktesting.YES
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, *args, **kwargs) -> None:
# REMOVED_UNUSED_CODE:         super().__init__(*args, **kwargs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Apply seed in backtesting mode to get comparable results,
# REMOVED_UNUSED_CODE:         # but not in live modes to get a non-repeating order of pairs during live modes.
# REMOVED_UNUSED_CODE:         if self._config.get("runmode") in (RunMode.LIVE, RunMode.DRY_RUN):
# REMOVED_UNUSED_CODE:             self._seed = None
# REMOVED_UNUSED_CODE:             logger.info("Live mode detected, not applying seed.")
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             self._seed = self._pairlistconfig.get("seed")
# REMOVED_UNUSED_CODE:             logger.info(f"Backtesting mode detected, applying seed value: {self._seed}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._random = random.Random(self._seed)  # noqa: S311
# REMOVED_UNUSED_CODE:         self._shuffle_freq: ShuffleValues = self._pairlistconfig.get("shuffle_frequency", "candle")
# REMOVED_UNUSED_CODE:         self.__pairlist_cache = PeriodicCache(
# REMOVED_UNUSED_CODE:             maxsize=1000, ttl=timeframe_to_seconds(self._config["timeframe"])
# REMOVED_UNUSED_CODE:         )
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return f"{self.name} - Shuffling pairs every {self._shuffle_freq}" + (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f", seed = {self._seed}." if self._seed is not None else "."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def description() -> str:
# REMOVED_UNUSED_CODE:         return "Randomize pairlist order."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def available_parameters() -> dict[str, PairlistParameter]:
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "shuffle_frequency": {
# REMOVED_UNUSED_CODE:                 "type": "option",
# REMOVED_UNUSED_CODE:                 "default": "candle",
# REMOVED_UNUSED_CODE:                 "options": ["candle", "iteration"],
# REMOVED_UNUSED_CODE:                 "description": "Shuffle frequency",
# REMOVED_UNUSED_CODE:                 "help": "Shuffle frequency. Can be either 'candle' or 'iteration'.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "seed": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": None,
# REMOVED_UNUSED_CODE:                 "description": "Random Seed",
# REMOVED_UNUSED_CODE:                 "help": "Seed for random number generator. Not used in live mode.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def filter_pairlist(self, pairlist: list[str], tickers: Tickers) -> list[str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Filters and sorts pairlist and returns the whitelist again.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Called on each bot iteration - please use internal caching if necessary
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pairlist: pairlist to filter or sort
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param tickers: Tickers (from exchange.get_tickers). May be cached.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: new whitelist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pairlist_bef = tuple(pairlist)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pairlist_new = self.__pairlist_cache.get(pairlist_bef)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if pairlist_new and self._shuffle_freq == "candle":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Use cached pairlist.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return pairlist_new
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Shuffle is done inplace
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._random.shuffle(pairlist)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.__pairlist_cache[pairlist_bef] = pairlist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return pairlist
