"""
Percent Change PairList provider

Provides dynamic pair list based on trade change
sorted based on percentage change in price over a
defined period or as coming from ticker
"""

import logging
from datetime import timedelta
from typing import TypedDict

from cachetools import TTLCache
from pandas import DataFrame

from freqtrade.constants import ListPairsWithTimeframes, PairWithTimeframe
from freqtrade.exceptions import OperationalException
from freqtrade.exchange import timeframe_to_minutes, timeframe_to_prev_date
from freqtrade.exchange.exchange_types import Ticker, Tickers
from freqtrade.plugins.pairlist.IPairList import IPairList, PairlistParameter, SupportsBacktesting
from freqtrade.util import dt_now, format_ms_time


logger = logging.getLogger(__name__)


class SymbolWithPercentage(TypedDict):
# REMOVED_UNUSED_CODE:     symbol: str
# REMOVED_UNUSED_CODE:     percentage: float | None


# REMOVED_UNUSED_CODE: class PercentChangePairList(IPairList):
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
# REMOVED_UNUSED_CODE:         self._min_value = self._pairlistconfig.get("min_value", None)
# REMOVED_UNUSED_CODE:         self._max_value = self._pairlistconfig.get("max_value", None)
# REMOVED_UNUSED_CODE:         self._refresh_period = self._pairlistconfig.get("refresh_period", 1800)
# REMOVED_UNUSED_CODE:         self._pair_cache: TTLCache = TTLCache(maxsize=1, ttl=self._refresh_period)
# REMOVED_UNUSED_CODE:         self._lookback_days = self._pairlistconfig.get("lookback_days", 0)
# REMOVED_UNUSED_CODE:         self._lookback_timeframe = self._pairlistconfig.get("lookback_timeframe", "1d")
# REMOVED_UNUSED_CODE:         self._lookback_period = self._pairlistconfig.get("lookback_period", 0)
# REMOVED_UNUSED_CODE:         self._sort_direction: str | None = self._pairlistconfig.get("sort_direction", "desc")
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
# REMOVED_UNUSED_CODE:             and self._exchange.get_option("tickers_have_percentage")
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "Exchange does not support dynamic whitelist in this configuration. "
# REMOVED_UNUSED_CODE:                 "Please edit your config and either remove PercentChangePairList, "
# REMOVED_UNUSED_CODE:                 "or switch to using candles. and restart the bot."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         candle_limit = self._exchange.ohlcv_candle_limit(
# REMOVED_UNUSED_CODE:             self._lookback_timeframe, self._config["candle_type_def"]
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._lookback_period > candle_limit:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "ChangeFilter requires lookback_period to not "
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def short_desc(self) -> str:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Short whitelist method description - used for startup-messages
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return f"{self.name} - top {self._pairlistconfig['number_assets']} percent change pairs."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def description() -> str:
# REMOVED_UNUSED_CODE:         return "Provides dynamic pair list based on percentage change."
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
# REMOVED_UNUSED_CODE:             "min_value": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": None,
# REMOVED_UNUSED_CODE:                 "description": "Minimum value",
# REMOVED_UNUSED_CODE:                 "help": "Minimum value to use for filtering the pairlist.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "max_value": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": None,
# REMOVED_UNUSED_CODE:                 "description": "Maximum value",
# REMOVED_UNUSED_CODE:                 "help": "Maximum value to use for filtering the pairlist.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "sort_direction": {
# REMOVED_UNUSED_CODE:                 "type": "option",
# REMOVED_UNUSED_CODE:                 "default": "desc",
# REMOVED_UNUSED_CODE:                 "options": ["", "asc", "desc"],
# REMOVED_UNUSED_CODE:                 "description": "Sort pairlist",
# REMOVED_UNUSED_CODE:                 "help": "Sort Pairlist ascending or descending by rate of change.",
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
# REMOVED_UNUSED_CODE:                 "default": "1d",
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # No point in testing for blacklisted pairs...
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             _pairlist = self.verify_blacklist(_pairlist, logger.info)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not self._use_range:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 filtered_tickers = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     v
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     for k, v in tickers.items()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     if (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         self._exchange.get_pair_quote_currency(k) == self._stake_currency
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
# REMOVED_UNUSED_CODE:         filtered_tickers: list[SymbolWithPercentage] = [
# REMOVED_UNUSED_CODE:             {"symbol": k, "percentage": None} for k in pairlist
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         if self._use_range:
# REMOVED_UNUSED_CODE:             # calculating using lookback_period
# REMOVED_UNUSED_CODE:             filtered_tickers = self.fetch_percent_change_from_lookback_period(filtered_tickers)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # Fetching 24h change by default from supported exchange tickers
# REMOVED_UNUSED_CODE:             filtered_tickers = self.fetch_percent_change_from_tickers(filtered_tickers, tickers)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._min_value is not None:
# REMOVED_UNUSED_CODE:             filtered_tickers = [v for v in filtered_tickers if v["percentage"] > self._min_value]
# REMOVED_UNUSED_CODE:         if self._max_value is not None:
# REMOVED_UNUSED_CODE:             filtered_tickers = [v for v in filtered_tickers if v["percentage"] < self._max_value]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         sorted_tickers = sorted(
# REMOVED_UNUSED_CODE:             filtered_tickers,
# REMOVED_UNUSED_CODE:             reverse=self._sort_direction == "desc",
# REMOVED_UNUSED_CODE:             key=lambda t: t["percentage"],  # type: ignore
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Validate whitelist to only have active market pairs
# REMOVED_UNUSED_CODE:         pairs = self._whitelist_for_active_markets([s["symbol"] for s in sorted_tickers])
# REMOVED_UNUSED_CODE:         pairs = self.verify_blacklist(pairs, logmethod=logger.info)
# REMOVED_UNUSED_CODE:         # Limit pairlist to the requested number of pairs
# REMOVED_UNUSED_CODE:         pairs = pairs[: self._number_pairs]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return pairs
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fetch_candles_for_lookback_period(
# REMOVED_UNUSED_CODE:         self, filtered_tickers: list[SymbolWithPercentage]
# REMOVED_UNUSED_CODE:     ) -> dict[PairWithTimeframe, DataFrame]:
# REMOVED_UNUSED_CODE:         since_ms = (
# REMOVED_UNUSED_CODE:             int(
# REMOVED_UNUSED_CODE:                 timeframe_to_prev_date(
# REMOVED_UNUSED_CODE:                     self._lookback_timeframe,
# REMOVED_UNUSED_CODE:                     dt_now()
# REMOVED_UNUSED_CODE:                     + timedelta(
# REMOVED_UNUSED_CODE:                         minutes=-(self._lookback_period * self._tf_in_min) - self._tf_in_min
# REMOVED_UNUSED_CODE:                     ),
# REMOVED_UNUSED_CODE:                 ).timestamp()
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             * 1000
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         to_ms = (
# REMOVED_UNUSED_CODE:             int(
# REMOVED_UNUSED_CODE:                 timeframe_to_prev_date(
# REMOVED_UNUSED_CODE:                     self._lookback_timeframe, dt_now() - timedelta(minutes=self._tf_in_min)
# REMOVED_UNUSED_CODE:                 ).timestamp()
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             * 1000
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         self.log_once(
# REMOVED_UNUSED_CODE:             f"Using change range of {self._lookback_period} candles, timeframe: "
# REMOVED_UNUSED_CODE:             f"{self._lookback_timeframe}, starting from {format_ms_time(since_ms)} "
# REMOVED_UNUSED_CODE:             f"till {format_ms_time(to_ms)}",
# REMOVED_UNUSED_CODE:             logger.info,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         needed_pairs: ListPairsWithTimeframes = [
# REMOVED_UNUSED_CODE:             (p, self._lookback_timeframe, self._def_candletype)
# REMOVED_UNUSED_CODE:             for p in [s["symbol"] for s in filtered_tickers]
# REMOVED_UNUSED_CODE:             if p not in self._pair_cache
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         candles = self._exchange.refresh_ohlcv_with_cache(needed_pairs, since_ms)
# REMOVED_UNUSED_CODE:         return candles
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fetch_percent_change_from_lookback_period(
# REMOVED_UNUSED_CODE:         self, filtered_tickers: list[SymbolWithPercentage]
# REMOVED_UNUSED_CODE:     ) -> list[SymbolWithPercentage]:
# REMOVED_UNUSED_CODE:         # get lookback period in ms, for exchange ohlcv fetch
# REMOVED_UNUSED_CODE:         candles = self.fetch_candles_for_lookback_period(filtered_tickers)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for i, p in enumerate(filtered_tickers):
# REMOVED_UNUSED_CODE:             pair_candles = (
# REMOVED_UNUSED_CODE:                 candles[(p["symbol"], self._lookback_timeframe, self._def_candletype)]
# REMOVED_UNUSED_CODE:                 if (p["symbol"], self._lookback_timeframe, self._def_candletype) in candles
# REMOVED_UNUSED_CODE:                 else None
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # in case of candle data calculate typical price and change for candle
# REMOVED_UNUSED_CODE:             if pair_candles is not None and not pair_candles.empty:
# REMOVED_UNUSED_CODE:                 current_close = pair_candles["close"].iloc[-1]
# REMOVED_UNUSED_CODE:                 previous_close = pair_candles["close"].shift(self._lookback_period).iloc[-1]
# REMOVED_UNUSED_CODE:                 pct_change = (
# REMOVED_UNUSED_CODE:                     ((current_close - previous_close) / previous_close) * 100
# REMOVED_UNUSED_CODE:                     if previous_close > 0
# REMOVED_UNUSED_CODE:                     else 0
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 # replace change with a range change sum calculated above
# REMOVED_UNUSED_CODE:                 filtered_tickers[i]["percentage"] = pct_change
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 filtered_tickers[i]["percentage"] = 0
# REMOVED_UNUSED_CODE:         return filtered_tickers
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fetch_percent_change_from_tickers(
# REMOVED_UNUSED_CODE:         self, filtered_tickers: list[SymbolWithPercentage], tickers
# REMOVED_UNUSED_CODE:     ) -> list[SymbolWithPercentage]:
# REMOVED_UNUSED_CODE:         valid_tickers: list[SymbolWithPercentage] = []
# REMOVED_UNUSED_CODE:         for p in filtered_tickers:
# REMOVED_UNUSED_CODE:             # Filter out assets
# REMOVED_UNUSED_CODE:             if (
# REMOVED_UNUSED_CODE:                 self._validate_pair(
# REMOVED_UNUSED_CODE:                     p["symbol"], tickers[p["symbol"]] if p["symbol"] in tickers else None
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 and p["symbol"] != "UNI/USDT"
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 p["percentage"] = tickers[p["symbol"]]["percentage"]
# REMOVED_UNUSED_CODE:                 valid_tickers.append(p)
# REMOVED_UNUSED_CODE:         return valid_tickers
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _validate_pair(self, pair: str, ticker: Ticker | None) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check if one price-step (pip) is > than a certain barrier.
# REMOVED_UNUSED_CODE:         :param pair: Pair that's currently validated
# REMOVED_UNUSED_CODE:         :param ticker: ticker dict as returned from ccxt.fetch_ticker
# REMOVED_UNUSED_CODE:         :return: True if the pair can stay, false if it should be removed
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not ticker or "percentage" not in ticker or ticker["percentage"] is None:
# REMOVED_UNUSED_CODE:             self.log_once(
# REMOVED_UNUSED_CODE:                 f"Removed {pair} from whitelist, because "
# REMOVED_UNUSED_CODE:                 "ticker['percentage'] is empty (Usually no trade in the last 24h).",
# REMOVED_UNUSED_CODE:                 logger.info,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return True
