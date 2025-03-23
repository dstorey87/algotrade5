"""
Spread pair list filter
"""

import logging

from freqtrade.exceptions import OperationalException
from freqtrade.exchange.exchange_types import Ticker
from freqtrade.plugins.pairlist.IPairList import IPairList, PairlistParameter, SupportsBacktesting


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class SpreadFilter(IPairList):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     supports_backtesting = SupportsBacktesting.NO
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, *args, **kwargs) -> None:
# REMOVED_UNUSED_CODE:         super().__init__(*args, **kwargs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._max_spread_ratio = self._pairlistconfig.get("max_spread_ratio", 0.005)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._enabled = self._max_spread_ratio != 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not self._exchange.get_option("tickers_have_bid_ask"):
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 f"{self.name} requires exchange to have bid/ask data for tickers, "
# REMOVED_UNUSED_CODE:                 "which is not available for the selected exchange / trading mode."
# REMOVED_UNUSED_CODE:             )
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"{self.name} - Filtering pairs with ask/bid diff above {self._max_spread_ratio:.2%}."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def description() -> str:
# REMOVED_UNUSED_CODE:         return "Filter by bid/ask difference."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def available_parameters() -> dict[str, PairlistParameter]:
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "max_spread_ratio": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 0.005,
# REMOVED_UNUSED_CODE:                 "description": "Max spread ratio",
# REMOVED_UNUSED_CODE:                 "help": "Max spread ratio for a pair to be considered.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _validate_pair(self, pair: str, ticker: Ticker | None) -> bool:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Validate spread for the ticker
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair that's currently validated
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param ticker: ticker dict as returned from ccxt.fetch_ticker
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: True if the pair can stay, false if it should be removed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if ticker and "bid" in ticker and "ask" in ticker and ticker["ask"] and ticker["bid"]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             spread = 1 - ticker["bid"] / ticker["ask"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if spread > self._max_spread_ratio:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.log_once(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"Removed {pair} from whitelist, because spread "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"{spread:.3%} > {self._max_spread_ratio:.3%}",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     logger.info,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.log_once(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"Removed {pair} from whitelist due to invalid ticker data: {ticker}", logger.info
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return False
