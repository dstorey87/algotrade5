"""
Market Cap PairList provider

Provides dynamic pair list based on Market Cap
"""

import logging
# REMOVED_UNUSED_CODE: import math

# REMOVED_UNUSED_CODE: from cachetools import TTLCache

# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException
# REMOVED_UNUSED_CODE: from freqtrade.exchange.exchange_types import Tickers
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.plugins.pairlist.IPairList import IPairList, PairlistParameter, SupportsBacktesting
# REMOVED_UNUSED_CODE: from freqtrade.util.coin_gecko import FtCoinGeckoApi


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class MarketCapPairList(IPairList):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     is_pairlist_generator = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     supports_backtesting = SupportsBacktesting.BIASED
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, *args, **kwargs) -> None:
# REMOVED_UNUSED_CODE:         super().__init__(*args, **kwargs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "number_assets" not in self._pairlistconfig:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "`number_assets` not specified. Please check your configuration "
# REMOVED_UNUSED_CODE:                 'for "pairlist.config.number_assets"'
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._stake_currency = self._config["stake_currency"]
# REMOVED_UNUSED_CODE:         self._number_assets = self._pairlistconfig["number_assets"]
# REMOVED_UNUSED_CODE:         self._max_rank = self._pairlistconfig.get("max_rank", 30)
# REMOVED_UNUSED_CODE:         self._refresh_period = self._pairlistconfig.get("refresh_period", 86400)
# REMOVED_UNUSED_CODE:         self._categories = self._pairlistconfig.get("categories", [])
# REMOVED_UNUSED_CODE:         self._marketcap_cache: TTLCache = TTLCache(maxsize=1, ttl=self._refresh_period)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._def_candletype = self._config["candle_type_def"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         _coingecko_config = self._config.get("coingecko", {})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._coingecko: FtCoinGeckoApi = FtCoinGeckoApi(
# REMOVED_UNUSED_CODE:             api_key=_coingecko_config.get("api_key", ""),
# REMOVED_UNUSED_CODE:             is_demo=_coingecko_config.get("is_demo", True),
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._categories:
# REMOVED_UNUSED_CODE:             categories = self._coingecko.get_coins_categories_list()
# REMOVED_UNUSED_CODE:             category_ids = [cat["category_id"] for cat in categories]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             for category in self._categories:
# REMOVED_UNUSED_CODE:                 if category not in category_ids:
# REMOVED_UNUSED_CODE:                     raise OperationalException(
# REMOVED_UNUSED_CODE:                         f"Category {category} not in coingecko category list. "
# REMOVED_UNUSED_CODE:                         f"You can choose from {category_ids}"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._max_rank > 250:
# REMOVED_UNUSED_CODE:             self.logger.warning(
# REMOVED_UNUSED_CODE:                 f"The max rank you have set ({self._max_rank}) is quite high. "
# REMOVED_UNUSED_CODE:                 "This may lead to coingecko API rate limit issues. "
# REMOVED_UNUSED_CODE:                 "Please ensure this value is necessary for your use case.",
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         num = self._number_assets
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         rank = self._max_rank
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         msg = f"{self.name} - {num} pairs placed within top {rank} market cap."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return msg
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def description() -> str:
# REMOVED_UNUSED_CODE:         return "Provides pair list based on CoinGecko's market cap rank."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def available_parameters() -> dict[str, PairlistParameter]:
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "number_assets": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 30,
# REMOVED_UNUSED_CODE:                 "description": "Number of assets",
# REMOVED_UNUSED_CODE:                 "help": "Number of assets to use from the pairlist",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "max_rank": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 30,
# REMOVED_UNUSED_CODE:                 "description": "Max rank of assets",
# REMOVED_UNUSED_CODE:                 "help": "Maximum rank of assets to use from the pairlist",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "categories": {
# REMOVED_UNUSED_CODE:                 "type": "list",
# REMOVED_UNUSED_CODE:                 "default": [],
# REMOVED_UNUSED_CODE:                 "description": "Coin Categories",
# REMOVED_UNUSED_CODE:                 "help": (
# REMOVED_UNUSED_CODE:                     "The Category of the coin e.g layer-1 default [] "
# REMOVED_UNUSED_CODE:                     "(https://www.coingecko.com/en/categories)"
# REMOVED_UNUSED_CODE:                 ),
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "refresh_period": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 86400,
# REMOVED_UNUSED_CODE:                 "description": "Refresh period",
# REMOVED_UNUSED_CODE:                 "help": "Refresh period in seconds",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def gen_pairlist(self, tickers: Tickers) -> list[str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Generate the pairlist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param tickers: Tickers (from exchange.get_tickers). May be cached.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: List of pairs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Generate dynamic whitelist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Must always run if this pairlist is the first in the list.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pairlist = self._marketcap_cache.get("pairlist_mc")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if pairlist:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Item found - no refresh necessary
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return pairlist.copy()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Use fresh pairlist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Check if pair quote currency equals to the stake currency.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             _pairlist = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 k
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 for k in self._exchange.get_markets(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     quote_currencies=[self._stake_currency], tradable_only=True, active_only=True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 ).keys()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # No point in testing for blacklisted pairs...
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             _pairlist = self.verify_blacklist(_pairlist, logger.info)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pairlist = self.filter_pairlist(_pairlist, tickers)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._marketcap_cache["pairlist_mc"] = pairlist.copy()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return pairlist
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def filter_pairlist(self, pairlist: list[str], tickers: dict) -> list[str]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Filters and sorts pairlist and returns the whitelist again.
# REMOVED_UNUSED_CODE:         Called on each bot iteration - please use internal caching if necessary
# REMOVED_UNUSED_CODE:         :param pairlist: pairlist to filter or sort
# REMOVED_UNUSED_CODE:         :param tickers: Tickers (from exchange.get_tickers). May be cached.
# REMOVED_UNUSED_CODE:         :return: new whitelist
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         marketcap_list = self._marketcap_cache.get("marketcap")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         default_kwargs = {
# REMOVED_UNUSED_CODE:             "vs_currency": "usd",
# REMOVED_UNUSED_CODE:             "order": "market_cap_desc",
# REMOVED_UNUSED_CODE:             "per_page": "250",
# REMOVED_UNUSED_CODE:             "page": "1",
# REMOVED_UNUSED_CODE:             "sparkline": "false",
# REMOVED_UNUSED_CODE:             "locale": "en",
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if marketcap_list is None:
# REMOVED_UNUSED_CODE:             data = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if not self._categories:
# REMOVED_UNUSED_CODE:                 pages_required = math.ceil(self._max_rank / 250)
# REMOVED_UNUSED_CODE:                 for page in range(1, pages_required + 1):
# REMOVED_UNUSED_CODE:                     default_kwargs["page"] = str(page)
# REMOVED_UNUSED_CODE:                     page_data = self._coingecko.get_coins_markets(**default_kwargs)
# REMOVED_UNUSED_CODE:                     data.extend(page_data)
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 for category in self._categories:
# REMOVED_UNUSED_CODE:                     category_data = self._coingecko.get_coins_markets(
# REMOVED_UNUSED_CODE:                         **default_kwargs, **({"category": category} if category else {})
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     data += category_data
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             data.sort(key=lambda d: float(d.get("market_cap") or 0.0), reverse=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if data:
# REMOVED_UNUSED_CODE:                 marketcap_list = [row["symbol"] for row in data]
# REMOVED_UNUSED_CODE:                 self._marketcap_cache["marketcap"] = marketcap_list
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if marketcap_list:
# REMOVED_UNUSED_CODE:             filtered_pairlist = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             market = self._config["trading_mode"]
# REMOVED_UNUSED_CODE:             pair_format = f"{self._stake_currency.upper()}"
# REMOVED_UNUSED_CODE:             if market == "futures":
# REMOVED_UNUSED_CODE:                 pair_format += f":{self._stake_currency.upper()}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             top_marketcap = marketcap_list[: self._max_rank :]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             for mc_pair in top_marketcap:
# REMOVED_UNUSED_CODE:                 test_pair = f"{mc_pair.upper()}/{pair_format}"
# REMOVED_UNUSED_CODE:                 if test_pair in pairlist and test_pair not in filtered_pairlist:
# REMOVED_UNUSED_CODE:                     filtered_pairlist.append(test_pair)
# REMOVED_UNUSED_CODE:                     if len(filtered_pairlist) == self._number_assets:
# REMOVED_UNUSED_CODE:                         break
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if len(filtered_pairlist) > 0:
# REMOVED_UNUSED_CODE:                 return filtered_pairlist
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # If no pairs are found, return the original pairlist
# REMOVED_UNUSED_CODE:         return []
