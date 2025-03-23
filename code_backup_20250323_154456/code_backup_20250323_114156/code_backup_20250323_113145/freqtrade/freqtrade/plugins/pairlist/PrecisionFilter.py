"""
Precision pair list filter
"""

import logging

from freqtrade.exceptions import OperationalException
from freqtrade.exchange import ROUND_UP
from freqtrade.exchange.exchange_types import Ticker
from freqtrade.plugins.pairlist.IPairList import IPairList, SupportsBacktesting


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class PrecisionFilter(IPairList):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     supports_backtesting = SupportsBacktesting.BIASED
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, *args, **kwargs) -> None:
# REMOVED_UNUSED_CODE:         super().__init__(*args, **kwargs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "stoploss" not in self._config:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "PrecisionFilter can only work with stoploss defined. Please add the "
# REMOVED_UNUSED_CODE:                 "stoploss key to your configuration (overwrites eventual strategy settings)."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         self._stoploss = self._config["stoploss"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._enabled = self._stoploss != 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Precalculate sanitized stoploss value to avoid recalculation for every pair
# REMOVED_UNUSED_CODE:         self._stoploss = 1 - abs(self._stoploss)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def needstickers(self) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Boolean property defining if tickers are necessary.
# REMOVED_UNUSED_CODE:         If no Pairlist requires tickers, an empty Dict is passed
# REMOVED_UNUSED_CODE:         as tickers argument to filter_pairlist
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def short_desc(self) -> str:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Short whitelist method description - used for startup-messages
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return f"{self.name} - Filtering untradable pairs."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def description() -> str:
# REMOVED_UNUSED_CODE:         return "Filters low-value coins which would not allow setting stoplosses."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _validate_pair(self, pair: str, ticker: Ticker | None) -> bool:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Check if pair has enough room to add a stoploss to avoid "unsellable" buys of very
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         low value pairs.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair that's currently validated
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param ticker: ticker dict as returned from ccxt.fetch_ticker
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: True if the pair can stay, false if it should be removed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not ticker or ticker.get("last", None) is None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.log_once(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"Removed {pair} from whitelist, because "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "ticker['last'] is empty (Usually no trade in the last 24h).",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.info,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stop_price = ticker["last"] * self._stoploss
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Adjust stop-prices to precision
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         sp = self._exchange.price_to_precision(pair, stop_price, rounding_mode=ROUND_UP)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stop_gap_price = self._exchange.price_to_precision(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pair, stop_price * 0.99, rounding_mode=ROUND_UP
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.debug(f"{pair} - {sp} : {stop_gap_price}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if sp <= stop_gap_price:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.log_once(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"Removed {pair} from whitelist, because "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"stop price {sp} would be <= stop limit {stop_gap_price}",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.info,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return True
