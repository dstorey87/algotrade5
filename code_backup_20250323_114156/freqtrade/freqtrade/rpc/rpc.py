"""
This module contains class to define a RPC communications
"""

import logging
# REMOVED_UNUSED_CODE: from abc import abstractmethod
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from collections.abc import Generator, Sequence
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import date, datetime, timedelta, timezone
# REMOVED_UNUSED_CODE: from math import isnan
from typing import TYPE_CHECKING, Any

# REMOVED_UNUSED_CODE: import psutil
# REMOVED_UNUSED_CODE: from dateutil.relativedelta import relativedelta
# REMOVED_UNUSED_CODE: from dateutil.tz import tzlocal
# REMOVED_UNUSED_CODE: from numpy import inf, int64, mean, nan
from pandas import DataFrame, NaT
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from sqlalchemy import func, select

# REMOVED_UNUSED_CODE: from freqtrade import __version__
# REMOVED_UNUSED_CODE: from freqtrade.configuration.timerange import TimeRange
# REMOVED_UNUSED_CODE: from freqtrade.constants import CANCEL_REASON, DEFAULT_DATAFRAME_COLUMNS, Config
# REMOVED_UNUSED_CODE: from freqtrade.data.history import load_data
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.data.metrics import DrawDownResult, calculate_expectancy, calculate_max_drawdown
# REMOVED_UNUSED_CODE: from freqtrade.enums import (
# REMOVED_UNUSED_CODE:     CandleType,
# REMOVED_UNUSED_CODE:     ExitCheckTuple,
# REMOVED_UNUSED_CODE:     ExitType,
# REMOVED_UNUSED_CODE:     MarketDirection,
# REMOVED_UNUSED_CODE:     SignalDirection,
# REMOVED_UNUSED_CODE:     State,
# REMOVED_UNUSED_CODE:     TradingMode,
# REMOVED_UNUSED_CODE: )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exceptions import ExchangeError, PricingError
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exchange import Exchange, timeframe_to_minutes, timeframe_to_msecs
# REMOVED_UNUSED_CODE: from freqtrade.exchange.exchange_utils import price_to_precision
# REMOVED_UNUSED_CODE: from freqtrade.loggers import bufferHandler
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.persistence import KeyStoreKeys, KeyValueStore, PairLocks, Trade
# REMOVED_UNUSED_CODE: from freqtrade.persistence.models import PairLock
# REMOVED_UNUSED_CODE: from freqtrade.plugins.pairlist.pairlist_helpers import expand_pairlist
from freqtrade.rpc.fiat_convert import CryptoToFiatConverter
# REMOVED_UNUSED_CODE: from freqtrade.rpc.rpc_types import RPCSendMsg
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.util import (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     decimals_per_coin,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     dt_from_ts,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     dt_humanize_delta,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     dt_now,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     dt_ts,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     dt_ts_def,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     format_date,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     shorten_date,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: )
# REMOVED_UNUSED_CODE: from freqtrade.wallets import PositionWallet, Wallet


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class RPCException(Exception):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Should be raised with a rpc-formatted message in an _rpc_* method
# REMOVED_UNUSED_CODE:     if the required state is wrong, i.e.:
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     raise RPCException('*Status:* `no active trade`')
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, message: str) -> None:
# REMOVED_UNUSED_CODE:         super().__init__(self)
# REMOVED_UNUSED_CODE:         self.message = message
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __str__(self):
# REMOVED_UNUSED_CODE:         return self.message
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __json__(self):
# REMOVED_UNUSED_CODE:         return {"msg": self.message}


# REMOVED_UNUSED_CODE: class RPCHandler:
# REMOVED_UNUSED_CODE:     def __init__(self, rpc: "RPC", config: Config) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Initializes RPCHandlers
# REMOVED_UNUSED_CODE:         :param rpc: instance of RPC Helper class
# REMOVED_UNUSED_CODE:         :param config: Configuration object
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._rpc = rpc
# REMOVED_UNUSED_CODE:         self._config: Config = config
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def name(self) -> str:
# REMOVED_UNUSED_CODE:         """Returns the lowercase name of the implementation"""
# REMOVED_UNUSED_CODE:         return self.__class__.__name__.lower()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def cleanup(self) -> None:
# REMOVED_UNUSED_CODE:         """Cleanup pending module resources"""
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def send_msg(self, msg: RPCSendMsg) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Sends a message to all registered rpc modules"""


# REMOVED_UNUSED_CODE: class RPC:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     RPC class can be used to have extra feature, like bot data, and access to DB data
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Bind _fiat_converter if needed
# REMOVED_UNUSED_CODE:     _fiat_converter: CryptoToFiatConverter | None = None
# REMOVED_UNUSED_CODE:     if TYPE_CHECKING:
# REMOVED_UNUSED_CODE:         from freqtrade.freqtradebot import FreqtradeBot
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         _freqtrade: FreqtradeBot
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, freqtrade) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Initializes all enabled rpc modules
# REMOVED_UNUSED_CODE:         :param freqtrade: Instance of a freqtrade bot
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self._freqtrade = freqtrade
# REMOVED_UNUSED_CODE:         self._config: Config = freqtrade.config
# REMOVED_UNUSED_CODE:         if self._config.get("fiat_display_currency"):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._fiat_converter = CryptoToFiatConverter(self._config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_show_config(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         config, botstate: State | str, strategy_version: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> dict[str, Any]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Return a dict of config options.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Explicitly does NOT return the full config to avoid leakage of sensitive
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         information via rpc.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         val = {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "version": __version__,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "strategy_version": strategy_version,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "dry_run": config["dry_run"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "trading_mode": config.get("trading_mode", "spot"),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "short_allowed": config.get("trading_mode", "spot") != "spot",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "stake_currency": config["stake_currency"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "stake_currency_decimals": decimals_per_coin(config["stake_currency"]),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "stake_amount": str(config["stake_amount"]),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "available_capital": config.get("available_capital"),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "max_open_trades": (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 config.get("max_open_trades", 0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if config.get("max_open_trades", 0) != float("inf")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 else -1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "minimal_roi": config["minimal_roi"].copy() if "minimal_roi" in config else {},
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "stoploss": config.get("stoploss"),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "stoploss_on_exchange": config.get("order_types", {}).get(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "stoploss_on_exchange", False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "trailing_stop": config.get("trailing_stop"),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "trailing_stop_positive": config.get("trailing_stop_positive"),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "trailing_stop_positive_offset": config.get("trailing_stop_positive_offset"),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "trailing_only_offset_is_reached": config.get("trailing_only_offset_is_reached"),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "unfilledtimeout": config.get("unfilledtimeout"),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "use_custom_stoploss": config.get("use_custom_stoploss"),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "order_types": config.get("order_types"),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "bot_name": config.get("bot_name", "freqtrade"),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "timeframe": config.get("timeframe"),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "timeframe_ms": timeframe_to_msecs(config["timeframe"]) if "timeframe" in config else 0,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "timeframe_min": (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 timeframe_to_minutes(config["timeframe"]) if "timeframe" in config else 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "exchange": config["exchange"]["name"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "strategy": config["strategy"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "force_entry_enable": config.get("force_entry_enable", False),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "exit_pricing": config.get("exit_pricing", {}),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "entry_pricing": config.get("entry_pricing", {}),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "state": str(botstate),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "runmode": config["runmode"].value,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "position_adjustment_enable": config.get("position_adjustment_enable", False),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "max_entry_position_adjustment": (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 config.get("max_entry_position_adjustment", -1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if config.get("max_entry_position_adjustment") != float("inf")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 else -1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return val
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_trade_status(self, trade_ids: list[int] | None = None) -> list[dict[str, Any]]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Below follows the RPC backend it is prefixed with rpc_ to raise awareness that it is
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         a remotely exposed function
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Fetch open trades
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if trade_ids:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trades: Sequence[Trade] = Trade.get_trades(trade_filter=Trade.id.in_(trade_ids)).all()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trades = Trade.get_open_trades()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not trades:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise RPCException("no active trade")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             results = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for trade in trades:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 current_profit_fiat: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 total_profit_fiat: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # prepare open orders details
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 oo_details: str | None = ""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 oo_details_lst = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"({oo.order_type} {oo.side} rem={oo.safe_remaining:.8f})"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     for oo in trade.open_orders
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     if oo.ft_order_side not in ["stoploss"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 oo_details = ", ".join(oo_details_lst)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 total_profit_abs = 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 total_profit_ratio: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # calculate profit and send message to user
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if trade.is_open:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         current_rate: float = self._freqtrade.exchange.get_rate(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             trade.pair, side="exit", is_short=trade.is_short, refresh=False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     except (ExchangeError, PricingError):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         current_rate = nan
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     if len(trade.select_filled_orders(trade.entry_side)) > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         current_profit = current_profit_abs = current_profit_fiat = nan
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         if not isnan(current_rate):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             prof = trade.calculate_profit(current_rate)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             current_profit = prof.profit_ratio
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             current_profit_abs = prof.profit_abs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             total_profit_abs = prof.total_profit
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             total_profit_ratio = prof.total_profit_ratio
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         current_profit = current_profit_abs = current_profit_fiat = 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     # Closed trade ...
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     current_rate = trade.close_rate or 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     current_profit = trade.close_profit or 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     current_profit_abs = trade.close_profit_abs or 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Calculate fiat profit
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if not isnan(current_profit_abs) and self._fiat_converter:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     current_profit_fiat = self._fiat_converter.convert_amount(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         current_profit_abs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         self._freqtrade.config["stake_currency"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         self._freqtrade.config["fiat_display_currency"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     total_profit_fiat = self._fiat_converter.convert_amount(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         total_profit_abs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         self._freqtrade.config["stake_currency"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         self._freqtrade.config["fiat_display_currency"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Calculate guaranteed profit (in case of trailing stop)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 stop_entry = trade.calculate_profit(trade.stop_loss)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 stoploss_entry_dist = stop_entry.profit_abs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 stoploss_entry_dist_ratio = stop_entry.profit_ratio
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # calculate distance to stoploss
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 stoploss_current_dist = price_to_precision(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     trade.stop_loss - current_rate,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     trade.price_precision,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     trade.precision_mode_price,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 stoploss_current_dist_ratio = stoploss_current_dist / current_rate
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade_dict = trade.to_json()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade_dict.update(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     dict(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         close_profit=trade.close_profit if not trade.is_open else None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         current_rate=current_rate,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         profit_ratio=current_profit,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         profit_pct=round(current_profit * 100, 2),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         profit_abs=current_profit_abs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         profit_fiat=current_profit_fiat,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         total_profit_abs=total_profit_abs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         total_profit_fiat=total_profit_fiat,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         total_profit_ratio=total_profit_ratio,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         stoploss_current_dist=stoploss_current_dist,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         stoploss_current_dist_ratio=round(stoploss_current_dist_ratio, 8),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         stoploss_current_dist_pct=round(stoploss_current_dist_ratio * 100, 2),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         stoploss_entry_dist=stoploss_entry_dist,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         stoploss_entry_dist_ratio=round(stoploss_entry_dist_ratio, 8),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         open_orders=oo_details,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         nr_of_successful_entries=trade.nr_of_successful_entries,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 results.append(trade_dict)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return results
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_status_table(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, stake_currency: str, fiat_display_currency: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> tuple[list, list, float, float]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: list of trades, list of columns, sum of fiat profit
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         nonspot = self._config.get("trading_mode", TradingMode.SPOT) != TradingMode.SPOT
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not Trade.get_open_trades():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise RPCException("no active trade")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trades_list = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         fiat_profit_sum = nan
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         fiat_total_profit_sum = nan
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for trade in self._rpc_trade_status():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Format profit as a string with the right sign
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             profit = f"{trade['profit_ratio']:.2%}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             fiat_profit = trade.get("profit_fiat", None)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if fiat_profit is None or isnan(fiat_profit):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 fiat_profit = trade.get("profit_abs", 0.0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not isnan(fiat_profit):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 profit += f" ({fiat_profit:.2f})"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 fiat_profit_sum = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     fiat_profit if isnan(fiat_profit_sum) else fiat_profit_sum + fiat_profit
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             total_profit = trade.get("total_profit_fiat", None)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if total_profit is None or isnan(total_profit):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 total_profit = trade.get("total_profit_abs", 0.0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not isnan(total_profit):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 fiat_total_profit_sum = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     total_profit
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     if isnan(fiat_total_profit_sum)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     else fiat_total_profit_sum + total_profit
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Format the active order side symbols
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             active_order_side = ""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             orders = trade.get("orders", [])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if orders:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 active_order_side = ".".join(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "*" if (o.get("is_open") and o.get("ft_is_entry")) else "**"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     for o in orders
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     if o.get("is_open") and o.get("ft_order_side") != "stoploss"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Direction string for non-spot
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             direction_str = ""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if nonspot:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 leverage = trade.get("leverage", 1.0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 direction_str = f"{'S' if trade.get('is_short') else 'L'} {leverage:.3g}x"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             detail_trade = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"{trade['trade_id']} {direction_str}",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"{trade['pair']}{active_order_side}",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 shorten_date(dt_humanize_delta(dt_from_ts(trade["open_timestamp"]))),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 profit,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Add number of entries if position adjustment is enabled
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self._config.get("position_adjustment_enable", False):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 max_entry_str = ""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if self._config.get("max_entry_position_adjustment", -1) > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     max_entry_str = f"/{self._config['max_entry_position_adjustment'] + 1}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 filled_entries = trade.get("nr_of_successful_entries", 0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 detail_trade.append(f"{filled_entries}{max_entry_str}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trades_list.append(detail_trade)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         columns = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "ID L/S" if nonspot else "ID",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "Pair",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "Since",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"Profit ({fiat_display_currency if self._fiat_converter else stake_currency})",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._config.get("position_adjustment_enable", False):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             columns.append("# Entries")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return trades_list, columns, fiat_profit_sum, fiat_total_profit_sum
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_timeunit_profit(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         timescale: int,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stake_currency: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         fiat_display_currency: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         timeunit: str = "days",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> dict[str, Any]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param timeunit: Valid entries are 'days', 'weeks', 'months'
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         start_date = datetime.now(timezone.utc).date()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if timeunit == "weeks":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # weekly
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             start_date = start_date - timedelta(days=start_date.weekday())  # Monday
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if timeunit == "months":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             start_date = start_date.replace(day=1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         def time_offset(step: int):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if timeunit == "months":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return relativedelta(months=step)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return timedelta(**{timeunit: step})
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not (isinstance(timescale, int) and timescale > 0):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise RPCException("timescale must be an integer greater than 0")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         profit_units: dict[date, dict] = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         daily_stake = self._freqtrade.wallets.get_total_stake_amount()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for day in range(0, timescale):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             profitday = start_date - time_offset(day)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Only query for necessary columns for performance reasons.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trades = Trade.session.execute(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 select(Trade.close_profit_abs)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 .filter(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     Trade.is_open.is_(False),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     Trade.close_date >= profitday,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     Trade.close_date < (profitday + time_offset(1)),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 .order_by(Trade.close_date)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ).all()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             curdayprofit = sum(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade.close_profit_abs for trade in trades if trade.close_profit_abs is not None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Calculate this periods starting balance
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             daily_stake = daily_stake - curdayprofit
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             profit_units[profitday] = {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "amount": curdayprofit,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "daily_stake": daily_stake,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "rel_profit": round(curdayprofit / daily_stake, 8) if daily_stake > 0 else 0,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "trades": len(trades),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         data = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "date": key,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "abs_profit": value["amount"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "starting_balance": value["daily_stake"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "rel_profit": value["rel_profit"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "fiat_value": (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     self._fiat_converter.convert_amount(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         value["amount"], stake_currency, fiat_display_currency
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     if self._fiat_converter
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     else 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 ),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "trade_count": value["trades"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for key, value in profit_units.items()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "stake_currency": stake_currency,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "fiat_display_currency": fiat_display_currency,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "data": data,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_trade_history(self, limit: int, offset: int = 0, order_by_id: bool = False) -> dict:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Returns the X last trades"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         order_by: Any = Trade.id if order_by_id else Trade.close_date.desc()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if limit:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trades = Trade.session.scalars(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 Trade.get_trades_query([Trade.is_open.is_(False)])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 .order_by(order_by)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 .limit(limit)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 .offset(offset)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trades = Trade.session.scalars(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 Trade.get_trades_query([Trade.is_open.is_(False)]).order_by(Trade.close_date.desc())
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         output = [trade.to_json() for trade in trades]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         total_trades = Trade.session.scalar(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             select(func.count(Trade.id)).filter(Trade.is_open.is_(False))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "trades": output,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "trades_count": len(output),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "offset": offset,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "total_trades": total_trades,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_stats(self) -> dict[str, Any]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Generate generic stats for trades in database
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         def trade_win_loss(trade):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if trade.close_profit > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return "wins"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             elif trade.close_profit < 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return "losses"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return "draws"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trades = Trade.get_trades([Trade.is_open.is_(False)], include_orders=False)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Duration
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dur: dict[str, list[float]] = {"wins": [], "draws": [], "losses": []}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Exit reason
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         exit_reasons = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for trade in trades:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if trade.exit_reason not in exit_reasons:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 exit_reasons[trade.exit_reason] = {"wins": 0, "losses": 0, "draws": 0}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             exit_reasons[trade.exit_reason][trade_win_loss(trade)] += 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if trade.close_date is not None and trade.open_date is not None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade_dur = (trade.close_date - trade.open_date).total_seconds()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 dur[trade_win_loss(trade)].append(trade_dur)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         wins_dur = sum(dur["wins"]) / len(dur["wins"]) if len(dur["wins"]) > 0 else None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         draws_dur = sum(dur["draws"]) / len(dur["draws"]) if len(dur["draws"]) > 0 else None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         losses_dur = sum(dur["losses"]) / len(dur["losses"]) if len(dur["losses"]) > 0 else None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         durations = {"wins": wins_dur, "draws": draws_dur, "losses": losses_dur}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return {"exit_reasons": exit_reasons, "durations": durations}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_trade_statistics(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, stake_currency: str, fiat_display_currency: str, start_date: datetime | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> dict[str, Any]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Returns cumulative profit statistics"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         start_date = datetime.fromtimestamp(0) if start_date is None else start_date
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade_filter = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             Trade.is_open.is_(False) & (Trade.close_date >= start_date)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ) | Trade.is_open.is_(True)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trades: Sequence[Trade] = Trade.session.scalars(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             Trade.get_trades_query(trade_filter, include_orders=False).order_by(Trade.id)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ).all()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         profit_all_coin = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         profit_all_ratio = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         profit_closed_coin = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         profit_closed_ratio = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         durations = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         winning_trades = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         losing_trades = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         winning_profit = 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         losing_profit = 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for trade in trades:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_rate: float = 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if trade.close_date:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 durations.append((trade.close_date - trade.open_date).total_seconds())
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not trade.is_open:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 profit_ratio = trade.close_profit or 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 profit_abs = trade.close_profit_abs or 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 profit_closed_coin.append(profit_abs)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 profit_closed_ratio.append(profit_ratio)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if profit_ratio >= 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     winning_trades += 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     winning_profit += profit_abs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     losing_trades += 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     losing_profit += profit_abs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Get current rate
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if len(trade.select_filled_orders(trade.entry_side)) == 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     # Skip trades with no filled orders
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     current_rate = self._freqtrade.exchange.get_rate(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         trade.pair, side="exit", is_short=trade.is_short, refresh=False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 except (PricingError, ExchangeError):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     current_rate = nan
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     profit_ratio = nan
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     profit_abs = nan
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     _profit = trade.calculate_profit(trade.close_rate or current_rate)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     profit_ratio = _profit.profit_ratio
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     profit_abs = _profit.total_profit
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             profit_all_coin.append(profit_abs)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             profit_all_ratio.append(profit_ratio)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         closed_trade_count = len([t for t in trades if not t.is_open])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         best_pair = Trade.get_best_pair(start_date)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trading_volume = Trade.get_trading_volume(start_date)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Prepare data to display
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         profit_closed_coin_sum = round(sum(profit_closed_coin), 8)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         profit_closed_ratio_mean = float(mean(profit_closed_ratio) if profit_closed_ratio else 0.0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         profit_closed_ratio_sum = sum(profit_closed_ratio) if profit_closed_ratio else 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         profit_closed_fiat = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._fiat_converter.convert_amount(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 profit_closed_coin_sum, stake_currency, fiat_display_currency
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self._fiat_converter
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         profit_all_coin_sum = round(sum(profit_all_coin), 8)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         profit_all_ratio_mean = float(mean(profit_all_ratio) if profit_all_ratio else 0.0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Doing the sum is not right - overall profit needs to be based on initial capital
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         profit_all_ratio_sum = sum(profit_all_ratio) if profit_all_ratio else 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         starting_balance = self._freqtrade.wallets.get_starting_balance()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         profit_closed_ratio_fromstart = 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         profit_all_ratio_fromstart = 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if starting_balance:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             profit_closed_ratio_fromstart = profit_closed_coin_sum / starting_balance
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             profit_all_ratio_fromstart = profit_all_coin_sum / starting_balance
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         profit_factor = winning_profit / abs(losing_profit) if losing_profit else float("inf")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         winrate = (winning_trades / closed_trade_count) if closed_trade_count > 0 else 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trades_df = DataFrame(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "close_date": format_date(trade.close_date),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "close_date_dt": trade.close_date,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "profit_abs": trade.close_profit_abs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 for trade in trades
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if not trade.is_open and trade.close_date
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         expectancy, expectancy_ratio = calculate_expectancy(trades_df)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         drawdown = DrawDownResult()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if len(trades_df) > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 drawdown = calculate_max_drawdown(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     trades_df,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     value_col="profit_abs",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     date_col="close_date_dt",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     starting_balance=starting_balance,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             except ValueError:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # ValueError if no losing trade.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 pass
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         profit_all_fiat = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._fiat_converter.convert_amount(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 profit_all_coin_sum, stake_currency, fiat_display_currency
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self._fiat_converter
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         first_date = trades[0].open_date_utc if trades else None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         last_date = trades[-1].open_date_utc if trades else None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         num = float(len(durations) or 1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         bot_start = KeyValueStore.get_datetime_value(KeyStoreKeys.BOT_START_TIME)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_closed_coin": profit_closed_coin_sum,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_closed_percent_mean": round(profit_closed_ratio_mean * 100, 2),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_closed_ratio_mean": profit_closed_ratio_mean,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_closed_percent_sum": round(profit_closed_ratio_sum * 100, 2),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_closed_ratio_sum": profit_closed_ratio_sum,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_closed_ratio": profit_closed_ratio_fromstart,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_closed_percent": round(profit_closed_ratio_fromstart * 100, 2),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_closed_fiat": profit_closed_fiat,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_all_coin": profit_all_coin_sum,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_all_percent_mean": round(profit_all_ratio_mean * 100, 2),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_all_ratio_mean": profit_all_ratio_mean,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_all_percent_sum": round(profit_all_ratio_sum * 100, 2),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_all_ratio_sum": profit_all_ratio_sum,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_all_ratio": profit_all_ratio_fromstart,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_all_percent": round(profit_all_ratio_fromstart * 100, 2),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_all_fiat": profit_all_fiat,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "trade_count": len(trades),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "closed_trade_count": closed_trade_count,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "first_trade_date": format_date(first_date),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "first_trade_humanized": dt_humanize_delta(first_date) if first_date else "",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "first_trade_timestamp": dt_ts_def(first_date, 0),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "latest_trade_date": format_date(last_date),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "latest_trade_humanized": dt_humanize_delta(last_date) if last_date else "",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "latest_trade_timestamp": dt_ts_def(last_date, 0),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "avg_duration": str(timedelta(seconds=sum(durations) / num)).split(".")[0],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "best_pair": best_pair[0] if best_pair else "",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "best_rate": round(best_pair[1] * 100, 2) if best_pair else 0,  # Deprecated
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "best_pair_profit_ratio": best_pair[1] if best_pair else 0,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "best_pair_profit_abs": best_pair[2] if best_pair else 0,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "winning_trades": winning_trades,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "losing_trades": losing_trades,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "profit_factor": profit_factor,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "winrate": winrate,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "expectancy": expectancy,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "expectancy_ratio": expectancy_ratio,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "max_drawdown": drawdown.relative_account_drawdown,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "max_drawdown_abs": drawdown.drawdown_abs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "max_drawdown_start": format_date(drawdown.high_date),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "max_drawdown_start_timestamp": dt_ts_def(drawdown.high_date),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "max_drawdown_end": format_date(drawdown.low_date),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "max_drawdown_end_timestamp": dt_ts_def(drawdown.low_date),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "drawdown_high": drawdown.high_value,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "drawdown_low": drawdown.low_value,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "trading_volume": trading_volume,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "bot_start_timestamp": dt_ts_def(bot_start, 0),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "bot_start_date": format_date(bot_start),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def __balance_get_est_stake(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, coin: str, stake_currency: str, amount: float, balance: Wallet
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> tuple[float, float]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         est_stake = 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         est_bot_stake = 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         is_futures = self._config.get("trading_mode", TradingMode.SPOT) == TradingMode.FUTURES
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if coin == self._freqtrade.exchange.get_proxy_coin():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             est_stake = balance.total
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if is_futures:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # in Futures, "total" includes the locked stake, and therefore all positions
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 est_stake = balance.free
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             est_bot_stake = amount
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 rate: float | None = self._freqtrade.exchange.get_conversion_rate(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     coin, stake_currency
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if rate:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     est_stake = rate * (balance.free if is_futures else balance.total)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     est_bot_stake = rate * amount
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return est_stake, est_bot_stake
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             except (ExchangeError, PricingError) as e:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.warning(f"Error {e} getting rate for {coin}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 pass
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return est_stake, est_bot_stake
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_balance(self, stake_currency: str, fiat_display_currency: str) -> dict:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Returns current account balance per crypto"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         currencies: list[dict] = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         total = 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         total_bot = 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         open_trades: list[Trade] = Trade.get_open_trades()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         open_assets: dict[str, Trade] = {t.safe_base_currency: t for t in open_trades}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._freqtrade.wallets.update(require_update=False)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         starting_capital = self._freqtrade.wallets.get_starting_balance()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         starting_cap_fiat = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._fiat_converter.convert_amount(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 starting_capital, stake_currency, fiat_display_currency
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self._fiat_converter
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         coin: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         balance: Wallet
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for coin, balance in self._freqtrade.wallets.get_all_balances().items():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not balance.total and not balance.free:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 open_assets.get(coin, None)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if self._freqtrade.trading_mode != TradingMode.FUTURES
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 else None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             is_stake_currency = coin == self._freqtrade.exchange.get_proxy_coin()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             is_bot_managed = is_stake_currency or trade is not None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade_amount = trade.amount if trade else 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if is_stake_currency:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade_amount = self._freqtrade.wallets.get_available_stake_amount()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 est_stake, est_stake_bot = self.__balance_get_est_stake(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     coin, stake_currency, trade_amount, balance
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             except ValueError:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             total += est_stake
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if is_bot_managed:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 total_bot += est_stake_bot
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             currencies.append(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "currency": coin,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "free": balance.free,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "balance": balance.total,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "used": balance.used,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "bot_owned": trade_amount,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "est_stake": est_stake or 0,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "est_stake_bot": est_stake_bot if is_bot_managed else 0,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "stake": stake_currency,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "side": "long",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "position": 0,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "is_bot_managed": is_bot_managed,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "is_position": False,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         symbol: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         position: PositionWallet
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for symbol, position in self._freqtrade.wallets.get_all_positions().items():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             total += position.collateral
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             total_bot += position.collateral
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             currencies.append(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "currency": symbol,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "free": 0,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "balance": 0,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "used": 0,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "position": position.position,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "est_stake": position.collateral,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "est_stake_bot": position.collateral,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "stake": stake_currency,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "side": position.side,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "is_bot_managed": True,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "is_position": True,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         value = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._fiat_converter.convert_amount(total, stake_currency, fiat_display_currency)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self._fiat_converter
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         value_bot = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._fiat_converter.convert_amount(total_bot, stake_currency, fiat_display_currency)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self._fiat_converter
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade_count = len(Trade.get_trades_proxy())
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         starting_capital_ratio = (total_bot / starting_capital) - 1 if starting_capital else 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         starting_cap_fiat_ratio = (value_bot / starting_cap_fiat) - 1 if starting_cap_fiat else 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "currencies": currencies,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "total": total,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "total_bot": total_bot,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "symbol": fiat_display_currency,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "value": value,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "value_bot": value_bot,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "stake": stake_currency,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "starting_capital": starting_capital,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "starting_capital_ratio": starting_capital_ratio,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "starting_capital_pct": round(starting_capital_ratio * 100, 2),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "starting_capital_fiat": starting_cap_fiat,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "starting_capital_fiat_ratio": starting_cap_fiat_ratio,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "starting_capital_fiat_pct": round(starting_cap_fiat_ratio * 100, 2),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "trade_count": trade_count,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "note": "Simulated balances" if self._freqtrade.config["dry_run"] else "",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_start(self) -> dict[str, str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Handler for start"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._freqtrade.state == State.RUNNING:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return {"status": "already running"}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._freqtrade.state = State.RUNNING
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return {"status": "starting trader ..."}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_stop(self) -> dict[str, str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Handler for stop"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._freqtrade.state == State.RUNNING:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._freqtrade.state = State.STOPPED
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return {"status": "stopping trader ..."}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return {"status": "already stopped"}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_reload_config(self) -> dict[str, str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Handler for reload_config."""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._freqtrade.state = State.RELOAD_CONFIG
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return {"status": "Reloading config ..."}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_stopentry(self) -> dict[str, str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Handler to stop buying, but handle open trades gracefully.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._freqtrade.state == State.RUNNING:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Set 'max_open_trades' to 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._freqtrade.config["max_open_trades"] = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._freqtrade.strategy.max_open_trades = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return {"status": "No more entries will occur from now. Run /reload_config to reset."}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_reload_trade_from_exchange(self, trade_id: int) -> dict[str, str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Handler for reload_trade_from_exchange.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Reloads a trade from it's orders, should manual interaction have happened.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade = Trade.get_trades(trade_filter=[Trade.id == trade_id]).first()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not trade:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise RPCException(f"Could not find trade with id {trade_id}.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._freqtrade.handle_onexchange_order(trade)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return {"status": "Reloaded from orders from exchange"}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def __exec_force_exit(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, trade: Trade, ordertype: str | None, amount: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Check if there is there are open orders
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade_entry_cancelation_registry = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for oo in trade.open_orders:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade_entry_cancelation_res = {"order_id": oo.order_id, "cancel_state": False}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             order = self._freqtrade.exchange.fetch_order(oo.order_id, trade.pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if order["side"] == trade.entry_side:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 fully_canceled = self._freqtrade.handle_cancel_enter(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     trade, order, oo, CANCEL_REASON["FORCE_EXIT"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade_entry_cancelation_res["cancel_state"] = fully_canceled
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade_entry_cancelation_registry.append(trade_entry_cancelation_res)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if order["side"] == trade.exit_side:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Cancel order - so it is placed anew with a fresh price.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._freqtrade.handle_cancel_exit(trade, order, oo, CANCEL_REASON["FORCE_EXIT"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if all(tocr["cancel_state"] is False for tocr in trade_entry_cancelation_registry):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if trade.has_open_orders:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Order cancellation failed, so we can't exit.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Get current rate and execute sell
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_rate = self._freqtrade.exchange.get_rate(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade.pair, side="exit", is_short=trade.is_short, refresh=True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             exit_check = ExitCheckTuple(exit_type=ExitType.FORCE_EXIT)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             order_type = ordertype or self._freqtrade.strategy.order_types.get(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "force_exit", self._freqtrade.strategy.order_types["exit"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             sub_amount: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if amount and amount < trade.amount:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Partial exit ...
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 min_exit_stake = self._freqtrade.exchange.get_min_pair_stake_amount(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     trade.pair, current_rate, trade.stop_loss_pct or 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 remaining = (trade.amount - amount) * current_rate
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if min_exit_stake and remaining < min_exit_stake:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     raise RPCException(f"Remaining amount of {remaining} would be too small.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 sub_amount = amount
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._freqtrade.execute_trade_exit(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade, current_rate, exit_check, ordertype=order_type, sub_trade_amt=sub_amount
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_force_exit(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, trade_id: str, ordertype: str | None = None, *, amount: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> dict[str, str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Handler for forceexit <id>.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Sells the given trade at current price
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._freqtrade.state != State.RUNNING:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise RPCException("trader is not running")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with self._freqtrade._exit_lock:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if trade_id == "all":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Execute exit for all open orders
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 for trade in Trade.get_open_trades():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     self.__exec_force_exit(trade, ordertype)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 Trade.commit()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._freqtrade.wallets.update()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return {"result": "Created exit orders for all open trades."}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Query for trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade = Trade.get_trades(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade_filter=[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     Trade.id == trade_id,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     Trade.is_open.is_(True),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ).first()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not trade:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.warning("force_exit: Invalid argument received")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 raise RPCException("invalid argument")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             result = self.__exec_force_exit(trade, ordertype, amount)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             Trade.commit()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._freqtrade.wallets.update()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not result:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 raise RPCException("Failed to exit trade.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return {"result": f"Created exit order for trade {trade_id}."}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _force_entry_validations(self, pair: str, order_side: SignalDirection):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not self._freqtrade.config.get("force_entry_enable", False):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise RPCException("Force_entry not enabled.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._freqtrade.state != State.RUNNING:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise RPCException("trader is not running")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if order_side == SignalDirection.SHORT and self._freqtrade.trading_mode == TradingMode.SPOT:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise RPCException("Can't go short on Spot markets.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if pair not in self._freqtrade.exchange.get_markets(tradable_only=True):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise RPCException("Symbol does not exist or market is not active.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Check if pair quote currency equals to the stake currency.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stake_currency = self._freqtrade.config.get("stake_currency")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not self._freqtrade.exchange.get_pair_quote_currency(pair) == stake_currency:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise RPCException(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"Wrong pair selected. Only pairs with stake-currency {stake_currency} allowed."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_force_entry(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         price: float | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         order_type: str | None = None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         order_side: SignalDirection = SignalDirection.LONG,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stake_amount: float | None = None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         enter_tag: str | None = "force_entry",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         leverage: float | None = None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> Trade | None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Handler for forcebuy <asset> <price>
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Buys a pair trade at the given or current price
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._force_entry_validations(pair, order_side)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # check if valid pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # check if pair already has an open pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade: Trade | None = Trade.get_trades(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             [Trade.is_open.is_(True), Trade.pair == pair]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ).first()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         is_short = order_side == SignalDirection.SHORT
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if trade:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             is_short = trade.is_short
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not self._freqtrade.strategy.position_adjustment_enable:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 raise RPCException(f"position for {pair} already open - id: {trade.id}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if trade.has_open_orders:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 raise RPCException(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"position for {pair} already open - id: {trade.id} "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"and has open order {','.join(trade.open_orders_ids)}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if Trade.get_open_trade_count() >= self._config["max_open_trades"]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 raise RPCException("Maximum number of trades is reached.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not stake_amount:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # gen stake amount
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             stake_amount = self._freqtrade.wallets.get_trade_stake_amount(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 pair, self._config["max_open_trades"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # execute buy
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not order_type:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             order_type = self._freqtrade.strategy.order_types.get(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "force_entry", self._freqtrade.strategy.order_types["entry"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with self._freqtrade._exit_lock:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self._freqtrade.execute_entry(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 pair,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 stake_amount,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 price,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 ordertype=order_type,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade=trade,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 is_short=is_short,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 enter_tag=enter_tag,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 leverage_=leverage,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 mode="pos_adjust" if trade else "initial",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 Trade.commit()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade = Trade.get_trades([Trade.is_open.is_(True), Trade.pair == pair]).first()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 raise RPCException(f"Failed to enter position for {pair}.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_cancel_open_order(self, trade_id: int):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._freqtrade.state != State.RUNNING:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise RPCException("trader is not running")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with self._freqtrade._exit_lock:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Query for trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade = Trade.get_trades(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade_filter=[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     Trade.id == trade_id,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     Trade.is_open.is_(True),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ).first()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not trade:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.warning("cancel_open_order: Invalid trade_id received.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 raise RPCException("Invalid trade_id.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not trade.has_open_orders:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.warning("cancel_open_order: No open order for trade_id.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 raise RPCException("No open order for trade_id.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for open_order in trade.open_orders:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     order = self._freqtrade.exchange.fetch_order(open_order.order_id, trade.pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 except ExchangeError as e:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     logger.info(f"Cannot query order for {trade} due to {e}.", exc_info=True)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     raise RPCException("Order not found.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._freqtrade.handle_cancel_order(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     order, open_order, trade, CANCEL_REASON["USER_CANCEL"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             Trade.commit()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_delete(self, trade_id: int) -> dict[str, str | int]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Handler for delete <id>.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Delete the given trade and close eventually existing open orders.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with self._freqtrade._exit_lock:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             c_count = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade = Trade.get_trades(trade_filter=[Trade.id == trade_id]).first()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not trade:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.warning("delete trade: Invalid argument received")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 raise RPCException("invalid argument")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Try cancelling regular order if that exists
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for open_order in trade.open_orders:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     self._freqtrade.exchange.cancel_order(open_order.order_id, trade.pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     c_count += 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 except ExchangeError:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     pass
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # cancel stoploss on exchange orders ...
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._freqtrade.strategy.order_types.get("stoploss_on_exchange")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 and trade.has_open_sl_orders
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 for oslo in trade.open_sl_orders:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         self._freqtrade.exchange.cancel_stoploss_order(oslo.order_id, trade.pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         c_count += 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     except ExchangeError:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         pass
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade.delete()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._freqtrade.wallets.update()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "result": "success",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "trade_id": trade_id,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "result_msg": f"Deleted trade {trade_id}. Closed {c_count} open orders.",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "cancel_order_count": c_count,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_list_custom_data(self, trade_id: int, key: str | None) -> list[dict[str, Any]]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Query for trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade = Trade.get_trades(trade_filter=[Trade.id == trade_id]).first()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if trade is None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Query custom_data
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         custom_data = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if key:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             data = trade.get_custom_data(key=key)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if data:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 custom_data = [data]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             custom_data = trade.get_all_custom_data()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "id": data_entry.id,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "ft_trade_id": data_entry.ft_trade_id,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "cd_key": data_entry.cd_key,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "cd_type": data_entry.cd_type,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "cd_value": data_entry.cd_value,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "created_at": data_entry.created_at,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "updated_at": data_entry.updated_at,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for data_entry in custom_data
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_performance(self) -> list[dict[str, Any]]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Handler for performance.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Shows a performance statistic from finished trades
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair_rates = Trade.get_overall_performance()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return pair_rates
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_enter_tag_performance(self, pair: str | None) -> list[dict[str, Any]]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Handler for buy tag performance.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Shows a performance statistic from finished trades
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return Trade.get_enter_tag_performance(pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_exit_reason_performance(self, pair: str | None) -> list[dict[str, Any]]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Handler for exit reason performance.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Shows a performance statistic from finished trades
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return Trade.get_exit_reason_performance(pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_mix_tag_performance(self, pair: str | None) -> list[dict[str, Any]]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Handler for mix tag (enter_tag + exit_reason) performance.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Shows a performance statistic from finished trades
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         mix_tags = Trade.get_mix_tag_performance(pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return mix_tags
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_count(self) -> dict[str, float]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Returns the number of trades running"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._freqtrade.state != State.RUNNING:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise RPCException("trader is not running")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trades = Trade.get_open_trades()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "current": len(trades),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "max": (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 int(self._freqtrade.config["max_open_trades"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if self._freqtrade.config["max_open_trades"] != float("inf")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 else -1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "total_stake": sum((trade.open_rate * trade.amount) for trade in trades),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_locks(self) -> dict[str, Any]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Returns the  current locks"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         locks = PairLocks.get_pair_locks(None)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return {"lock_count": len(locks), "locks": [lock.to_json() for lock in locks]}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_delete_lock(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, lockid: int | None = None, pair: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> dict[str, Any]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Delete specific lock(s)"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         locks: Sequence[PairLock] = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if pair:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             locks = PairLocks.get_pair_locks(pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if lockid:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             locks = PairLock.session.scalars(select(PairLock).filter(PairLock.id == lockid)).all()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for lock in locks:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             lock.active = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             lock.lock_end_time = datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Trade.commit()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._rpc_locks()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_add_lock(self, pair: str, until: datetime, reason: str | None, side: str) -> PairLock:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         lock = PairLocks.lock_pair(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pair=pair,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             until=until,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             reason=reason,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             side=side,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return lock
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_whitelist(self) -> dict:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Returns the currently active whitelist"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         res = {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "method": self._freqtrade.pairlists.name_list,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "length": len(self._freqtrade.active_pair_whitelist),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "whitelist": self._freqtrade.active_pair_whitelist,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return res
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_blacklist_delete(self, delete: list[str]) -> dict:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Removes pairs from currently active blacklist"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         errors = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for pair in delete:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if pair in self._freqtrade.pairlists.blacklist:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._freqtrade.pairlists.blacklist.remove(pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 errors[pair] = {"error_msg": f"Pair {pair} is not in the current blacklist."}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         resp = self._rpc_blacklist()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         resp["errors"] = errors
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return resp
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_blacklist(self, add: list[str] | None = None) -> dict:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Returns the currently active blacklist"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         errors = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if add:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for pair in add:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if pair not in self._freqtrade.pairlists.blacklist:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         expand_pairlist([pair], list(self._freqtrade.exchange.get_markets().keys()))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         self._freqtrade.pairlists.blacklist.append(pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     except ValueError:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         errors[pair] = {"error_msg": f"Pair {pair} is not a valid wildcard."}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     errors[pair] = {"error_msg": f"Pair {pair} already in pairlist."}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         res = {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "method": self._freqtrade.pairlists.name_list,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "length": len(self._freqtrade.pairlists.blacklist),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "blacklist": self._freqtrade.pairlists.blacklist,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "blacklist_expanded": self._freqtrade.pairlists.expanded_blacklist,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "errors": errors,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return res
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_get_logs(limit: int | None) -> dict[str, Any]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Returns the last X logs"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if limit:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             buffer = bufferHandler.buffer[-limit:]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             buffer = bufferHandler.buffer
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         records = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 format_date(datetime.fromtimestamp(r.created)),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 r.created * 1000,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 r.name,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 r.levelname,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 r.message + ("\n" + r.exc_text if r.exc_text else ""),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for r in buffer
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if hasattr(r, "message")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Log format:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # [logtime-formatted, logepoch, logger-name, loglevel, message \n + exception]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # e.g. ["2020-08-27 11:35:01", 1598520901097.9397,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #       "freqtrade.worker", "INFO", "Starting worker develop"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return {"log_count": len(records), "logs": records}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_edge(self) -> list[dict[str, Any]]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Returns information related to Edge"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not self._freqtrade.edge:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise RPCException("Edge is not enabled.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._freqtrade.edge.accepted_pairs()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def _convert_dataframe_to_dict(
# REMOVED_UNUSED_CODE:         strategy: str,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         timeframe: str,
# REMOVED_UNUSED_CODE:         dataframe: DataFrame,
# REMOVED_UNUSED_CODE:         last_analyzed: datetime,
# REMOVED_UNUSED_CODE:         selected_cols: list[str] | None,
# REMOVED_UNUSED_CODE:     ) -> dict[str, Any]:
# REMOVED_UNUSED_CODE:         has_content = len(dataframe) != 0
# REMOVED_UNUSED_CODE:         dataframe_columns = list(dataframe.columns)
# REMOVED_UNUSED_CODE:         signals = {
# REMOVED_UNUSED_CODE:             "enter_long": 0,
# REMOVED_UNUSED_CODE:             "exit_long": 0,
# REMOVED_UNUSED_CODE:             "enter_short": 0,
# REMOVED_UNUSED_CODE:             "exit_short": 0,
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:         if has_content:
# REMOVED_UNUSED_CODE:             if selected_cols is not None:
# REMOVED_UNUSED_CODE:                 # Ensure OHLCV columns are always present
# REMOVED_UNUSED_CODE:                 cols_set = set(DEFAULT_DATAFRAME_COLUMNS + list(signals.keys()) + selected_cols)
# REMOVED_UNUSED_CODE:                 df_cols = [col for col in dataframe_columns if col in cols_set]
# REMOVED_UNUSED_CODE:                 dataframe = dataframe.loc[:, df_cols]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             dataframe.loc[:, "__date_ts"] = dataframe.loc[:, "date"].astype(int64) // 1000 // 1000
# REMOVED_UNUSED_CODE:             # Move signal close to separate column when signal for easy plotting
# REMOVED_UNUSED_CODE:             for sig_type in signals.keys():
# REMOVED_UNUSED_CODE:                 if sig_type in dataframe.columns:
# REMOVED_UNUSED_CODE:                     mask = dataframe[sig_type] == 1
# REMOVED_UNUSED_CODE:                     signals[sig_type] = int(mask.sum())
# REMOVED_UNUSED_CODE:                     dataframe.loc[mask, f"_{sig_type}_signal_close"] = dataframe.loc[mask, "close"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # band-aid until this is fixed:
# REMOVED_UNUSED_CODE:             # https://github.com/pandas-dev/pandas/issues/45836
# REMOVED_UNUSED_CODE:             datetime_types = ["datetime", "datetime64", "datetime64[ns, UTC]"]
# REMOVED_UNUSED_CODE:             date_columns = dataframe.select_dtypes(include=datetime_types)
# REMOVED_UNUSED_CODE:             for date_column in date_columns:
# REMOVED_UNUSED_CODE:                 # replace NaT with `None`
# REMOVED_UNUSED_CODE:                 dataframe[date_column] = dataframe[date_column].astype(object).replace({NaT: None})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             dataframe = dataframe.replace({inf: None, -inf: None, nan: None})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         res = {
# REMOVED_UNUSED_CODE:             "pair": pair,
# REMOVED_UNUSED_CODE:             "timeframe": timeframe,
# REMOVED_UNUSED_CODE:             "timeframe_ms": timeframe_to_msecs(timeframe),
# REMOVED_UNUSED_CODE:             "strategy": strategy,
# REMOVED_UNUSED_CODE:             "all_columns": dataframe_columns,
# REMOVED_UNUSED_CODE:             "columns": list(dataframe.columns),
# REMOVED_UNUSED_CODE:             "data": dataframe.values.tolist(),
# REMOVED_UNUSED_CODE:             "length": len(dataframe),
# REMOVED_UNUSED_CODE:             "buy_signals": signals["enter_long"],  # Deprecated
# REMOVED_UNUSED_CODE:             "sell_signals": signals["exit_long"],  # Deprecated
# REMOVED_UNUSED_CODE:             "enter_long_signals": signals["enter_long"],
# REMOVED_UNUSED_CODE:             "exit_long_signals": signals["exit_long"],
# REMOVED_UNUSED_CODE:             "enter_short_signals": signals["enter_short"],
# REMOVED_UNUSED_CODE:             "exit_short_signals": signals["exit_short"],
# REMOVED_UNUSED_CODE:             "last_analyzed": last_analyzed,
# REMOVED_UNUSED_CODE:             "last_analyzed_ts": int(last_analyzed.timestamp()),
# REMOVED_UNUSED_CODE:             "data_start": "",
# REMOVED_UNUSED_CODE:             "data_start_ts": 0,
# REMOVED_UNUSED_CODE:             "data_stop": "",
# REMOVED_UNUSED_CODE:             "data_stop_ts": 0,
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:         if has_content:
# REMOVED_UNUSED_CODE:             res.update(
# REMOVED_UNUSED_CODE:                 {
# REMOVED_UNUSED_CODE:                     "data_start": str(dataframe.iloc[0]["date"]),
# REMOVED_UNUSED_CODE:                     "data_start_ts": int(dataframe.iloc[0]["__date_ts"]),
# REMOVED_UNUSED_CODE:                     "data_stop": str(dataframe.iloc[-1]["date"]),
# REMOVED_UNUSED_CODE:                     "data_stop_ts": int(dataframe.iloc[-1]["__date_ts"]),
# REMOVED_UNUSED_CODE:                 }
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         return res
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _rpc_analysed_dataframe(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pair: str, timeframe: str, limit: int | None, selected_cols: list[str] | None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> dict[str, Any]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Analyzed dataframe in Dict form"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         _data, last_analyzed = self.__rpc_analysed_dataframe_raw(pair, timeframe, limit)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return RPC._convert_dataframe_to_dict(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._freqtrade.config["strategy"], pair, timeframe, _data, last_analyzed, selected_cols
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def __rpc_analysed_dataframe_raw(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pair: str, timeframe: str, limit: int | None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> tuple[DataFrame, datetime]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Get the dataframe and last analyze from the dataprovider
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: The pair to get
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param timeframe: The timeframe of data to get
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param limit: The amount of candles in the dataframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         _data, last_analyzed = self._freqtrade.dataprovider.get_analyzed_dataframe(pair, timeframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         _data = _data.copy()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if limit:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             _data = _data.iloc[-limit:]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return _data, last_analyzed

# REMOVED_UNUSED_CODE:     def _ws_all_analysed_dataframes(
# REMOVED_UNUSED_CODE:         self, pairlist: list[str], limit: int | None
# REMOVED_UNUSED_CODE:     ) -> Generator[dict[str, Any], None, None]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get the analysed dataframes of each pair in the pairlist.
# REMOVED_UNUSED_CODE:         If specified, only return the most recent `limit` candles for
# REMOVED_UNUSED_CODE:         each dataframe.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param pairlist: A list of pairs to get
# REMOVED_UNUSED_CODE:         :param limit: If an integer, limits the size of dataframe
# REMOVED_UNUSED_CODE:                       If a list of string date times, only returns those candles
# REMOVED_UNUSED_CODE:         :returns: A generator of dictionaries with the key, dataframe, and last analyzed timestamp
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         timeframe = self._freqtrade.config["timeframe"]
# REMOVED_UNUSED_CODE:         candle_type = self._freqtrade.config.get("candle_type_def", CandleType.SPOT)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for pair in pairlist:
# REMOVED_UNUSED_CODE:             dataframe, last_analyzed = self.__rpc_analysed_dataframe_raw(pair, timeframe, limit)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             yield {"key": (pair, timeframe, candle_type), "df": dataframe, "la": last_analyzed}

# REMOVED_UNUSED_CODE:     def _ws_request_analyzed_df(self, limit: int | None = None, pair: str | None = None):
# REMOVED_UNUSED_CODE:         """Historical Analyzed Dataframes for WebSocket"""
# REMOVED_UNUSED_CODE:         pairlist = [pair] if pair else self._freqtrade.active_pair_whitelist
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return self._ws_all_analysed_dataframes(pairlist, limit)

# REMOVED_UNUSED_CODE:     def _ws_request_whitelist(self):
# REMOVED_UNUSED_CODE:         """Whitelist data for WebSocket"""
# REMOVED_UNUSED_CODE:         return self._freqtrade.active_pair_whitelist

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def _rpc_analysed_history_full(
# REMOVED_UNUSED_CODE:         config: Config,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         timeframe: str,
# REMOVED_UNUSED_CODE:         exchange: Exchange,
# REMOVED_UNUSED_CODE:         selected_cols: list[str] | None,
# REMOVED_UNUSED_CODE:         live: bool,
# REMOVED_UNUSED_CODE:     ) -> dict[str, Any]:
# REMOVED_UNUSED_CODE:         timerange_parsed = TimeRange.parse_timerange(config.get("timerange"))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         from freqtrade.data.converter import trim_dataframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         from freqtrade.data.dataprovider import DataProvider
# REMOVED_UNUSED_CODE:         from freqtrade.resolvers.strategy_resolver import StrategyResolver
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         strategy_name = ""
# REMOVED_UNUSED_CODE:         startup_candles = 0
# REMOVED_UNUSED_CODE:         if config.get("strategy"):
# REMOVED_UNUSED_CODE:             strategy = StrategyResolver.load_strategy(config)
# REMOVED_UNUSED_CODE:             startup_candles = strategy.startup_candle_count
# REMOVED_UNUSED_CODE:             strategy_name = strategy.get_strategy_name()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if live:
# REMOVED_UNUSED_CODE:             data = exchange.get_historic_ohlcv(
# REMOVED_UNUSED_CODE:                 pair=pair,
# REMOVED_UNUSED_CODE:                 timeframe=timeframe,
# REMOVED_UNUSED_CODE:                 since_ms=timerange_parsed.startts * 1000
# REMOVED_UNUSED_CODE:                 if timerange_parsed.startts
# REMOVED_UNUSED_CODE:                 else dt_ts(dt_now() - timedelta(days=30)),
# REMOVED_UNUSED_CODE:                 is_new_pair=True,  # history is never available - so always treat as new pair
# REMOVED_UNUSED_CODE:                 candle_type=config.get("candle_type_def", CandleType.SPOT),
# REMOVED_UNUSED_CODE:                 until_ms=timerange_parsed.stopts,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             _data = load_data(
# REMOVED_UNUSED_CODE:                 datadir=config["datadir"],
# REMOVED_UNUSED_CODE:                 pairs=[pair],
# REMOVED_UNUSED_CODE:                 timeframe=timeframe,
# REMOVED_UNUSED_CODE:                 timerange=timerange_parsed,
# REMOVED_UNUSED_CODE:                 data_format=config["dataformat_ohlcv"],
# REMOVED_UNUSED_CODE:                 candle_type=config.get("candle_type_def", CandleType.SPOT),
# REMOVED_UNUSED_CODE:                 startup_candles=startup_candles,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             if pair not in _data:
# REMOVED_UNUSED_CODE:                 raise RPCException(
# REMOVED_UNUSED_CODE:                     f"No data for {pair}, {timeframe} in {config.get('timerange')} found."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             data = _data[pair]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if config.get("strategy"):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             strategy.dp = DataProvider(config, exchange=exchange, pairlists=None)
# REMOVED_UNUSED_CODE:             strategy.ft_bot_start()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             df_analyzed = strategy.analyze_ticker(data, {"pair": pair})
# REMOVED_UNUSED_CODE:             df_analyzed = trim_dataframe(
# REMOVED_UNUSED_CODE:                 df_analyzed, timerange_parsed, startup_candles=startup_candles
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             df_analyzed = data
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return RPC._convert_dataframe_to_dict(
# REMOVED_UNUSED_CODE:             strategy_name,
# REMOVED_UNUSED_CODE:             pair,
# REMOVED_UNUSED_CODE:             timeframe,
# REMOVED_UNUSED_CODE:             df_analyzed.copy(),
# REMOVED_UNUSED_CODE:             dt_now(),
# REMOVED_UNUSED_CODE:             selected_cols,
# REMOVED_UNUSED_CODE:         )

# REMOVED_UNUSED_CODE:     def _rpc_plot_config(self) -> dict[str, Any]:
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             self._freqtrade.strategy.plot_config
# REMOVED_UNUSED_CODE:             and "subplots" not in self._freqtrade.strategy.plot_config
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             self._freqtrade.strategy.plot_config["subplots"] = {}
# REMOVED_UNUSED_CODE:         return self._freqtrade.strategy.plot_config

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def _rpc_plot_config_with_strategy(config: Config) -> dict[str, Any]:
# REMOVED_UNUSED_CODE:         from freqtrade.resolvers.strategy_resolver import StrategyResolver
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         strategy = StrategyResolver.load_strategy(config)
# REMOVED_UNUSED_CODE:         # Manually load hyperparameters, as we don't call the bot-start callback.
# REMOVED_UNUSED_CODE:         strategy.ft_load_hyper_params(False)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if strategy.plot_config and "subplots" not in strategy.plot_config:
# REMOVED_UNUSED_CODE:             strategy.plot_config["subplots"] = {}
# REMOVED_UNUSED_CODE:         return strategy.plot_config

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def _rpc_sysinfo() -> dict[str, Any]:
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "cpu_pct": psutil.cpu_percent(interval=1, percpu=True),
# REMOVED_UNUSED_CODE:             "ram_pct": psutil.virtual_memory().percent,
# REMOVED_UNUSED_CODE:         }

# REMOVED_UNUSED_CODE:     def health(self) -> dict[str, str | int | None]:
# REMOVED_UNUSED_CODE:         last_p = self._freqtrade.last_process
# REMOVED_UNUSED_CODE:         res: dict[str, None | str | int] = {
# REMOVED_UNUSED_CODE:             "last_process": None,
# REMOVED_UNUSED_CODE:             "last_process_loc": None,
# REMOVED_UNUSED_CODE:             "last_process_ts": None,
# REMOVED_UNUSED_CODE:             "bot_start": None,
# REMOVED_UNUSED_CODE:             "bot_start_loc": None,
# REMOVED_UNUSED_CODE:             "bot_start_ts": None,
# REMOVED_UNUSED_CODE:             "bot_startup": None,
# REMOVED_UNUSED_CODE:             "bot_startup_loc": None,
# REMOVED_UNUSED_CODE:             "bot_startup_ts": None,
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if last_p is not None:
# REMOVED_UNUSED_CODE:             res.update(
# REMOVED_UNUSED_CODE:                 {
# REMOVED_UNUSED_CODE:                     "last_process": str(last_p),
# REMOVED_UNUSED_CODE:                     "last_process_loc": format_date(last_p.astimezone(tzlocal())),
# REMOVED_UNUSED_CODE:                     "last_process_ts": int(last_p.timestamp()),
# REMOVED_UNUSED_CODE:                 }
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if bot_start := KeyValueStore.get_datetime_value(KeyStoreKeys.BOT_START_TIME):
# REMOVED_UNUSED_CODE:             res.update(
# REMOVED_UNUSED_CODE:                 {
# REMOVED_UNUSED_CODE:                     "bot_start": str(bot_start),
# REMOVED_UNUSED_CODE:                     "bot_start_loc": format_date(bot_start.astimezone(tzlocal())),
# REMOVED_UNUSED_CODE:                     "bot_start_ts": int(bot_start.timestamp()),
# REMOVED_UNUSED_CODE:                 }
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         if bot_startup := KeyValueStore.get_datetime_value(KeyStoreKeys.STARTUP_TIME):
# REMOVED_UNUSED_CODE:             res.update(
# REMOVED_UNUSED_CODE:                 {
# REMOVED_UNUSED_CODE:                     "bot_startup": str(bot_startup),
# REMOVED_UNUSED_CODE:                     "bot_startup_loc": format_date(bot_startup.astimezone(tzlocal())),
# REMOVED_UNUSED_CODE:                     "bot_startup_ts": int(bot_startup.timestamp()),
# REMOVED_UNUSED_CODE:                 }
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return res

# REMOVED_UNUSED_CODE:     def _update_market_direction(self, direction: MarketDirection) -> None:
# REMOVED_UNUSED_CODE:         self._freqtrade.strategy.market_direction = direction

# REMOVED_UNUSED_CODE:     def _get_market_direction(self) -> MarketDirection:
# REMOVED_UNUSED_CODE:         return self._freqtrade.strategy.market_direction
