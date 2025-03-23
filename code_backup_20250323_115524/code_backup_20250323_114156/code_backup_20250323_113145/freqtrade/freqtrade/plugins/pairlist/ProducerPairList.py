"""
External Pair List provider

Provides pair list from Leader data
"""

import logging

from freqtrade.exceptions import OperationalException
from freqtrade.exchange.exchange_types import Tickers
from freqtrade.plugins.pairlist.IPairList import IPairList, PairlistParameter, SupportsBacktesting


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class ProducerPairList(IPairList):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     PairList plugin for use with external_message_consumer.
# REMOVED_UNUSED_CODE:     Will use pairs given from leader data.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Usage:
# REMOVED_UNUSED_CODE:         "pairlists": [
# REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE:                 "method": "ProducerPairList",
# REMOVED_UNUSED_CODE:                 "number_assets": 5,
# REMOVED_UNUSED_CODE:                 "producer_name": "default",
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE:         ],
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     is_pairlist_generator = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     supports_backtesting = SupportsBacktesting.NO
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, *args, **kwargs) -> None:
# REMOVED_UNUSED_CODE:         super().__init__(*args, **kwargs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._num_assets: int = self._pairlistconfig.get("number_assets", 0)
# REMOVED_UNUSED_CODE:         self._producer_name = self._pairlistconfig.get("producer_name", "default")
# REMOVED_UNUSED_CODE:         if not self._config.get("external_message_consumer", {}).get("enabled"):
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "ProducerPairList requires external_message_consumer to be enabled."
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         -> Please overwrite in subclasses
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return f"{self.name} - {self._producer_name}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def description() -> str:
# REMOVED_UNUSED_CODE:         return "Get a pairlist from an upstream bot."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def available_parameters() -> dict[str, PairlistParameter]:
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "number_assets": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 0,
# REMOVED_UNUSED_CODE:                 "description": "Number of assets",
# REMOVED_UNUSED_CODE:                 "help": "Number of assets to use from the pairlist",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "producer_name": {
# REMOVED_UNUSED_CODE:                 "type": "string",
# REMOVED_UNUSED_CODE:                 "default": "default",
# REMOVED_UNUSED_CODE:                 "description": "Producer name",
# REMOVED_UNUSED_CODE:                 "help": (
# REMOVED_UNUSED_CODE:                     "Name of the producer to use. Requires additional "
# REMOVED_UNUSED_CODE:                     "external_message_consumer configuration."
# REMOVED_UNUSED_CODE:                 ),
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _filter_pairlist(self, pairlist: list[str] | None):
# REMOVED_UNUSED_CODE:         upstream_pairlist = self._pairlistmanager._dataprovider.get_producer_pairs(
# REMOVED_UNUSED_CODE:             self._producer_name
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if pairlist is None:
# REMOVED_UNUSED_CODE:             pairlist = self._pairlistmanager._dataprovider.get_producer_pairs(self._producer_name)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         pairs = list(dict.fromkeys(pairlist + upstream_pairlist))
# REMOVED_UNUSED_CODE:         if self._num_assets:
# REMOVED_UNUSED_CODE:             pairs = pairs[: self._num_assets]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return pairs
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def gen_pairlist(self, tickers: Tickers) -> list[str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Generate the pairlist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param tickers: Tickers (from exchange.get_tickers). May be cached.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: List of pairs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pairs = self._filter_pairlist(None)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.log_once(f"Received pairs: {pairs}", logger.debug)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pairs = self._whitelist_for_active_markets(self.verify_whitelist(pairs, logger.info))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return pairs
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def filter_pairlist(self, pairlist: list[str], tickers: Tickers) -> list[str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Filters and sorts pairlist and returns the whitelist again.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Called on each bot iteration - please use internal caching if necessary
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pairlist: pairlist to filter or sort
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param tickers: Tickers (from exchange.get_tickers). May be cached.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: new whitelist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._filter_pairlist(pairlist)
