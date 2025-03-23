"""
Volume PairList provider

Provides dynamic pair list based on trade volumes
"""

import logging
# REMOVED_UNUSED_CODE: from datetime import timedelta
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from typing import Any, Literal

# REMOVED_UNUSED_CODE: from cachetools import TTLCache

# REMOVED_UNUSED_CODE: from freqtrade.constants import ListPairsWithTimeframes
# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exchange import timeframe_to_minutes, timeframe_to_prev_date
# REMOVED_UNUSED_CODE: from freqtrade.exchange.exchange_types import Tickers
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.plugins.pairlist.IPairList import IPairList, PairlistParameter, SupportsBacktesting
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.util import dt_now, format_ms_time


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: SORT_VALUES = ["quoteVolume"]


# REMOVED_UNUSED_CODE: class VolumePairList(IPairList):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     is_pairlist_generator = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     supports_backtesting = SupportsBacktesting.NO
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
# REMOVED_UNUSED_CODE:         self._number_pairs = self._pairlistconfig["number_assets"]
# REMOVED_UNUSED_CODE:         self._sort_key: Literal["quoteVolume"] = self._pairlistconfig.get("sort_key", "quoteVolume")
# REMOVED_UNUSED_CODE:         self._min_value = self._pairlistconfig.get("min_value", 0)
# REMOVED_UNUSED_CODE:         self._max_value = self._pairlistconfig.get("max_value", None)
# REMOVED_UNUSED_CODE:         self._refresh_period = self._pairlistconfig.get("refresh_period", 1800)
# REMOVED_UNUSED_CODE:         self._pair_cache: TTLCache = TTLCache(maxsize=1, ttl=self._refresh_period)
# REMOVED_UNUSED_CODE:         self._lookback_days = self._pairlistconfig.get("lookback_days", 0)
# REMOVED_UNUSED_CODE:         self._lookback_timeframe = self._pairlistconfig.get("lookback_timeframe", "1d")
# REMOVED_UNUSED_CODE:         self._lookback_period = self._pairlistconfig.get("lookback_period", 0)
# REMOVED_UNUSED_CODE:         self._def_candletype = self._config["candle_type_def"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if (self._lookback_days > 0) & (self._lookback_period > 0):
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "Ambiguous configuration: lookback_days and lookback_period both set in pairlist "
# REMOVED_UNUSED_CODE:                 "config. Please set lookback_days only or lookback_period and lookback_timeframe "
# REMOVED_UNUSED_CODE:                 "and restart the bot."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # overwrite lookback timeframe and days when lookback_days is set
# REMOVED_UNUSED_CODE:         if self._lookback_days > 0:
# REMOVED_UNUSED_CODE:             self._lookback_timeframe = "1d"
# REMOVED_UNUSED_CODE:             self._lookback_period = self._lookback_days
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # get timeframe in minutes and seconds
# REMOVED_UNUSED_CODE:         self._tf_in_min = timeframe_to_minutes(self._lookback_timeframe)
# REMOVED_UNUSED_CODE:         _tf_in_sec = self._tf_in_min * 60
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # whether to use range lookback or not
# REMOVED_UNUSED_CODE:         self._use_range = (self._tf_in_min > 0) & (self._lookback_period > 0)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._use_range & (self._refresh_period < _tf_in_sec):
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 f"Refresh period of {self._refresh_period} seconds is smaller than one "
# REMOVED_UNUSED_CODE:                 f"timeframe of {self._lookback_timeframe}. Please adjust refresh_period "
# REMOVED_UNUSED_CODE:                 f"to at least {_tf_in_sec} and restart the bot."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not self._use_range and not (
# REMOVED_UNUSED_CODE:             self._exchange.exchange_has("fetchTickers")
# REMOVED_UNUSED_CODE:             and self._exchange.get_option("tickers_have_quoteVolume")
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "Exchange does not support dynamic whitelist in this configuration. "
# REMOVED_UNUSED_CODE:                 "Please edit your config and either remove Volumepairlist, "
# REMOVED_UNUSED_CODE:                 "or switch to using candles. and restart the bot."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not self._validate_keys(self._sort_key):
# REMOVED_UNUSED_CODE:             raise OperationalException(f"key {self._sort_key} not in {SORT_VALUES}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         candle_limit = self._exchange.ohlcv_candle_limit(
# REMOVED_UNUSED_CODE:             self._lookback_timeframe, self._config["candle_type_def"]
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         if self._lookback_period < 0:
# REMOVED_UNUSED_CODE:             raise OperationalException("VolumeFilter requires lookback_period to be >= 0")
# REMOVED_UNUSED_CODE:         if self._lookback_period > candle_limit:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "VolumeFilter requires lookback_period to not "
# REMOVED_UNUSED_CODE:                 f"exceed exchange max request size ({candle_limit})"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def needstickers(self) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Boolean property defining if tickers are necessary.
# REMOVED_UNUSED_CODE:         If no Pairlist requires tickers, an empty Dict is passed
# REMOVED_UNUSED_CODE:         as tickers argument to filter_pairlist
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return not self._use_range
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _validate_keys(self, key):
# REMOVED_UNUSED_CODE:         return key in SORT_VALUES
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def short_desc(self) -> str:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Short whitelist method description - used for startup-messages
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return f"{self.name} - top {self._pairlistconfig['number_assets']} volume pairs."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def description() -> str:
# REMOVED_UNUSED_CODE:         return "Provides dynamic pair list based on trade volumes."
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
# REMOVED_UNUSED_CODE:             "sort_key": {
# REMOVED_UNUSED_CODE:                 "type": "option",
# REMOVED_UNUSED_CODE:                 "default": "quoteVolume",
# REMOVED_UNUSED_CODE:                 "options": SORT_VALUES,
# REMOVED_UNUSED_CODE:                 "description": "Sort key",
# REMOVED_UNUSED_CODE:                 "help": "Sort key to use for sorting the pairlist.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "min_value": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 0,
# REMOVED_UNUSED_CODE:                 "description": "Minimum value",
# REMOVED_UNUSED_CODE:                 "help": "Minimum value to use for filtering the pairlist.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "max_value": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": None,
# REMOVED_UNUSED_CODE:                 "description": "Maximum value",
# REMOVED_UNUSED_CODE:                 "help": "Maximum value to use for filtering the pairlist.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             **IPairList.refresh_period_parameter(),
# REMOVED_UNUSED_CODE:             "lookback_days": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 0,
# REMOVED_UNUSED_CODE:                 "description": "Lookback Days",
# REMOVED_UNUSED_CODE:                 "help": "Number of days to look back at.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "lookback_timeframe": {
# REMOVED_UNUSED_CODE:                 "type": "string",
# REMOVED_UNUSED_CODE:                 "default": "",
# REMOVED_UNUSED_CODE:                 "description": "Lookback Timeframe",
# REMOVED_UNUSED_CODE:                 "help": "Timeframe to use for lookback.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "lookback_period": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 0,
# REMOVED_UNUSED_CODE:                 "description": "Lookback Period",
# REMOVED_UNUSED_CODE:                 "help": "Number of periods to look back at.",
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Must always run if this pairlist is not the first in the list.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pairlist = self._pair_cache.get("pairlist")
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not self._use_range:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 filtered_tickers = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     v
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     for k, v in tickers.items()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     if (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         self._exchange.get_pair_quote_currency(k) == self._stake_currency
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         and (self._use_range or v.get(self._sort_key) is not None)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         and v["symbol"] in _pairlist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 pairlist = [s["symbol"] for s in filtered_tickers]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 pairlist = _pairlist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pairlist = self.filter_pairlist(pairlist, tickers)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._pair_cache["pairlist"] = pairlist.copy()
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
# REMOVED_UNUSED_CODE:         if self._use_range:
# REMOVED_UNUSED_CODE:             # Create bare minimum from tickers structure.
# REMOVED_UNUSED_CODE:             filtered_tickers: list[dict[str, Any]] = [{"symbol": k} for k in pairlist]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # get lookback period in ms, for exchange ohlcv fetch
# REMOVED_UNUSED_CODE:             since_ms = (
# REMOVED_UNUSED_CODE:                 int(
# REMOVED_UNUSED_CODE:                     timeframe_to_prev_date(
# REMOVED_UNUSED_CODE:                         self._lookback_timeframe,
# REMOVED_UNUSED_CODE:                         dt_now()
# REMOVED_UNUSED_CODE:                         + timedelta(
# REMOVED_UNUSED_CODE:                             minutes=-(self._lookback_period * self._tf_in_min) - self._tf_in_min
# REMOVED_UNUSED_CODE:                         ),
# REMOVED_UNUSED_CODE:                     ).timestamp()
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 * 1000
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             to_ms = (
# REMOVED_UNUSED_CODE:                 int(
# REMOVED_UNUSED_CODE:                     timeframe_to_prev_date(
# REMOVED_UNUSED_CODE:                         self._lookback_timeframe, dt_now() - timedelta(minutes=self._tf_in_min)
# REMOVED_UNUSED_CODE:                     ).timestamp()
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 * 1000
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # todo: utc date output for starting date
# REMOVED_UNUSED_CODE:             self.log_once(
# REMOVED_UNUSED_CODE:                 f"Using volume range of {self._lookback_period} candles, timeframe: "
# REMOVED_UNUSED_CODE:                 f"{self._lookback_timeframe}, starting from {format_ms_time(since_ms)} "
# REMOVED_UNUSED_CODE:                 f"till {format_ms_time(to_ms)}",
# REMOVED_UNUSED_CODE:                 logger.info,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             needed_pairs: ListPairsWithTimeframes = [
# REMOVED_UNUSED_CODE:                 (p, self._lookback_timeframe, self._def_candletype)
# REMOVED_UNUSED_CODE:                 for p in [s["symbol"] for s in filtered_tickers]
# REMOVED_UNUSED_CODE:                 if p not in self._pair_cache
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             candles = self._exchange.refresh_ohlcv_with_cache(needed_pairs, since_ms)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             for i, p in enumerate(filtered_tickers):
# REMOVED_UNUSED_CODE:                 contract_size = self._exchange.markets[p["symbol"]].get("contractSize", 1.0) or 1.0
# REMOVED_UNUSED_CODE:                 pair_candles = (
# REMOVED_UNUSED_CODE:                     candles[(p["symbol"], self._lookback_timeframe, self._def_candletype)]
# REMOVED_UNUSED_CODE:                     if (p["symbol"], self._lookback_timeframe, self._def_candletype) in candles
# REMOVED_UNUSED_CODE:                     else None
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 # in case of candle data calculate typical price and quoteVolume for candle
# REMOVED_UNUSED_CODE:                 if pair_candles is not None and not pair_candles.empty:
# REMOVED_UNUSED_CODE:                     if self._exchange.get_option("ohlcv_volume_currency") == "base":
# REMOVED_UNUSED_CODE:                         pair_candles["typical_price"] = (
# REMOVED_UNUSED_CODE:                             pair_candles["high"] + pair_candles["low"] + pair_candles["close"]
# REMOVED_UNUSED_CODE:                         ) / 3
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                         pair_candles["quoteVolume"] = (
# REMOVED_UNUSED_CODE:                             pair_candles["volume"] * pair_candles["typical_price"] * contract_size
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:                     else:
# REMOVED_UNUSED_CODE:                         # Exchange ohlcv data is in quote volume already.
# REMOVED_UNUSED_CODE:                         pair_candles["quoteVolume"] = pair_candles["volume"]
# REMOVED_UNUSED_CODE:                     # ensure that a rolling sum over the lookback_period is built
# REMOVED_UNUSED_CODE:                     # if pair_candles contains more candles than lookback_period
# REMOVED_UNUSED_CODE:                     quoteVolume = (
# REMOVED_UNUSED_CODE:                         pair_candles["quoteVolume"]
# REMOVED_UNUSED_CODE:                         .rolling(self._lookback_period)
# REMOVED_UNUSED_CODE:                         .sum()
# REMOVED_UNUSED_CODE:                         .fillna(0)
# REMOVED_UNUSED_CODE:                         .iloc[-1]
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                     # replace quoteVolume with range quoteVolume sum calculated above
# REMOVED_UNUSED_CODE:                     filtered_tickers[i]["quoteVolume"] = quoteVolume
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     filtered_tickers[i]["quoteVolume"] = 0
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # Tickers mode - filter based on incoming pairlist.
# REMOVED_UNUSED_CODE:             filtered_tickers = [v for k, v in tickers.items() if k in pairlist]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._min_value > 0:
# REMOVED_UNUSED_CODE:             filtered_tickers = [v for v in filtered_tickers if v[self._sort_key] > self._min_value]
# REMOVED_UNUSED_CODE:         if self._max_value is not None:
# REMOVED_UNUSED_CODE:             filtered_tickers = [v for v in filtered_tickers if v[self._sort_key] < self._max_value]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         sorted_tickers = sorted(filtered_tickers, reverse=True, key=lambda t: t[self._sort_key])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Validate whitelist to only have active market pairs
# REMOVED_UNUSED_CODE:         pairs = self._whitelist_for_active_markets([s["symbol"] for s in sorted_tickers])
# REMOVED_UNUSED_CODE:         pairs = self.verify_blacklist(pairs, logmethod=logger.info)
# REMOVED_UNUSED_CODE:         # Limit pairlist to the requested number of pairs
# REMOVED_UNUSED_CODE:         pairs = pairs[: self._number_pairs]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return pairs
