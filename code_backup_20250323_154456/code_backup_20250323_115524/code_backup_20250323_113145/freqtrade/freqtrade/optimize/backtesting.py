# pragma pylint: disable=missing-docstring, W0212, too-many-arguments

"""
This module contains the backtesting logic
"""

import logging
from collections import defaultdict
from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any

from numpy import nan
from pandas import DataFrame

from freqtrade import constants
from freqtrade.configuration import TimeRange, validate_config_consistency
from freqtrade.constants import DATETIME_PRINT_FORMAT, Config, IntOrInf, LongShort
from freqtrade.data import history
from freqtrade.data.btanalysis import find_existing_backtest_stats, trade_list_to_dataframe
from freqtrade.data.converter import trim_dataframe, trim_dataframes
from freqtrade.data.dataprovider import DataProvider
from freqtrade.data.metrics import combined_dataframes_with_rel_mean
from freqtrade.enums import (
    BacktestState,
    CandleType,
    ExitCheckTuple,
    ExitType,
    MarginMode,
    RunMode,
    TradingMode,
)
from freqtrade.exceptions import DependencyException, OperationalException
from freqtrade.exchange import (
    amount_to_contract_precision,
    price_to_precision,
    timeframe_to_seconds,
)
from freqtrade.exchange.exchange import Exchange
from freqtrade.ft_types import BacktestResultType, get_BacktestResultType_default
from freqtrade.leverage.liquidation_price import update_liquidation_prices
from freqtrade.mixins import LoggingMixin
from freqtrade.optimize.backtest_caching import get_strategy_run_id
from freqtrade.optimize.bt_progress import BTProgress
from freqtrade.optimize.optimize_reports import (
    generate_backtest_stats,
    generate_rejected_signals,
    generate_trade_signal_candles,
    show_backtest_results,
    store_backtest_results,
)
from freqtrade.persistence import (
    CustomDataWrapper,
    LocalTrade,
    Order,
    PairLocks,
    Trade,
    disable_database_use,
    enable_database_use,
)
from freqtrade.plugins.pairlistmanager import PairListManager
from freqtrade.plugins.protectionmanager import ProtectionManager
from freqtrade.resolvers import ExchangeResolver, StrategyResolver
from freqtrade.strategy.interface import IStrategy
from freqtrade.strategy.strategy_wrapper import strategy_safe_wrapper
from freqtrade.util import FtPrecise, dt_now
from freqtrade.util.migrations import migrate_data
from freqtrade.wallets import Wallets


logger = logging.getLogger(__name__)

# Indexes for backtest tuples
DATE_IDX = 0
OPEN_IDX = 1
HIGH_IDX = 2
LOW_IDX = 3
CLOSE_IDX = 4
LONG_IDX = 5
ELONG_IDX = 6  # Exit long
SHORT_IDX = 7
ESHORT_IDX = 8  # Exit short
ENTER_TAG_IDX = 9
EXIT_TAG_IDX = 10

# Every change to this headers list must evaluate further usages of the resulting tuple
# and eventually change the constants for indexes at the top
HEADERS = [
    "date",
    "open",
    "high",
    "low",
    "close",
    "enter_long",
    "exit_long",
    "enter_short",
    "exit_short",
    "enter_tag",
    "exit_tag",
]


# REMOVED_UNUSED_CODE: class Backtesting:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Backtesting class, this class contains all the logic to run a backtest
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     To run a backtest:
# REMOVED_UNUSED_CODE:     backtesting = Backtesting(config)
# REMOVED_UNUSED_CODE:     backtesting.start()
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, config: Config, exchange: Exchange | None = None) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         LoggingMixin.show_output = False
# REMOVED_UNUSED_CODE:         self.config = config
# REMOVED_UNUSED_CODE:         self.results: BacktestResultType = get_BacktestResultType_default()
# REMOVED_UNUSED_CODE:         self.trade_id_counter: int = 0
# REMOVED_UNUSED_CODE:         self.order_id_counter: int = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         config["dry_run"] = True
# REMOVED_UNUSED_CODE:         self.run_ids: dict[str, str] = {}
# REMOVED_UNUSED_CODE:         self.strategylist: list[IStrategy] = []
# REMOVED_UNUSED_CODE:         self.all_results: dict[str, dict] = {}
# REMOVED_UNUSED_CODE:         self.analysis_results: dict[str, dict[str, DataFrame]] = {
# REMOVED_UNUSED_CODE:             "signals": {},
# REMOVED_UNUSED_CODE:             "rejected": {},
# REMOVED_UNUSED_CODE:             "exited": {},
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:         self.rejected_dict: dict[str, list] = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._exchange_name = self.config["exchange"]["name"]
# REMOVED_UNUSED_CODE:         if not exchange:
# REMOVED_UNUSED_CODE:             exchange = ExchangeResolver.load_exchange(self.config, load_leverage_tiers=True)
# REMOVED_UNUSED_CODE:         self.exchange = exchange
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.dataprovider = DataProvider(self.config, self.exchange)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.config.get("strategy_list"):
# REMOVED_UNUSED_CODE:             if self.config.get("freqai", {}).get("enabled", False):
# REMOVED_UNUSED_CODE:                 logger.warning(
# REMOVED_UNUSED_CODE:                     "Using --strategy-list with FreqAI REQUIRES all strategies "
# REMOVED_UNUSED_CODE:                     "to have identical feature_engineering_* functions."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             for strat in list(self.config["strategy_list"]):
# REMOVED_UNUSED_CODE:                 stratconf = deepcopy(self.config)
# REMOVED_UNUSED_CODE:                 stratconf["strategy"] = strat
# REMOVED_UNUSED_CODE:                 self.strategylist.append(StrategyResolver.load_strategy(stratconf))
# REMOVED_UNUSED_CODE:                 validate_config_consistency(stratconf)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # No strategy list specified, only one strategy
# REMOVED_UNUSED_CODE:             self.strategylist.append(StrategyResolver.load_strategy(self.config))
# REMOVED_UNUSED_CODE:             validate_config_consistency(self.config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "timeframe" not in self.config:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "Timeframe needs to be set in either "
# REMOVED_UNUSED_CODE:                 "configuration or as cli argument `--timeframe 5m`"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         self.timeframe = str(self.config.get("timeframe"))
# REMOVED_UNUSED_CODE:         self.timeframe_secs = timeframe_to_seconds(self.timeframe)
# REMOVED_UNUSED_CODE:         self.timeframe_min = self.timeframe_secs // 60
# REMOVED_UNUSED_CODE:         self.timeframe_td = timedelta(seconds=self.timeframe_secs)
# REMOVED_UNUSED_CODE:         self.disable_database_use()
# REMOVED_UNUSED_CODE:         self.init_backtest_detail()
# REMOVED_UNUSED_CODE:         self.pairlists = PairListManager(self.exchange, self.config, self.dataprovider)
# REMOVED_UNUSED_CODE:         self._validate_pairlists_for_backtesting()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.dataprovider.add_pairlisthandler(self.pairlists)
# REMOVED_UNUSED_CODE:         self.pairlists.refresh_pairlist()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if len(self.pairlists.whitelist) == 0:
# REMOVED_UNUSED_CODE:             raise OperationalException("No pair in whitelist.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if config.get("fee", None) is not None:
# REMOVED_UNUSED_CODE:             self.fee = config["fee"]
# REMOVED_UNUSED_CODE:             logger.info(f"Using fee {self.fee:.4%} from config.")
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             fees = [
# REMOVED_UNUSED_CODE:                 self.exchange.get_fee(
# REMOVED_UNUSED_CODE:                     symbol=self.pairlists.whitelist[0],
# REMOVED_UNUSED_CODE:                     taker_or_maker=mt,  # type: ignore
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 for mt in ("taker", "maker")
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE:             self.fee = max(fee for fee in fees if fee is not None)
# REMOVED_UNUSED_CODE:             logger.info(f"Using fee {self.fee:.4%} - worst case fee from exchange (lowest tier).")
# REMOVED_UNUSED_CODE:         self.precision_mode = self.exchange.precisionMode
# REMOVED_UNUSED_CODE:         self.precision_mode_price = self.exchange.precision_mode_price
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.config.get("freqai_backtest_live_models", False):
# REMOVED_UNUSED_CODE:             from freqtrade.freqai.utils import get_timerange_backtest_live_models
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.config["timerange"] = get_timerange_backtest_live_models(self.config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.timerange = TimeRange.parse_timerange(
# REMOVED_UNUSED_CODE:             None if self.config.get("timerange") is None else str(self.config.get("timerange"))
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Get maximum required startup period
# REMOVED_UNUSED_CODE:         self.required_startup = max([strat.startup_candle_count for strat in self.strategylist])
# REMOVED_UNUSED_CODE:         self.exchange.validate_required_startup_candles(self.required_startup, self.timeframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add maximum startup candle count to configuration for informative pairs support
# REMOVED_UNUSED_CODE:         self.config["startup_candle_count"] = self.required_startup
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.config.get("freqai", {}).get("enabled", False):
# REMOVED_UNUSED_CODE:             # For FreqAI, increase the required_startup to includes the training data
# REMOVED_UNUSED_CODE:             # This value should NOT be written to startup_candle_count
# REMOVED_UNUSED_CODE:             self.required_startup = self.dataprovider.get_required_startup(self.timeframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.trading_mode: TradingMode = config.get("trading_mode", TradingMode.SPOT)
# REMOVED_UNUSED_CODE:         self.margin_mode: MarginMode = config.get("margin_mode", MarginMode.ISOLATED)
# REMOVED_UNUSED_CODE:         # strategies which define "can_short=True" will fail to load in Spot mode.
# REMOVED_UNUSED_CODE:         self._can_short = self.trading_mode != TradingMode.SPOT
# REMOVED_UNUSED_CODE:         self._position_stacking: bool = self.config.get("position_stacking", False)
# REMOVED_UNUSED_CODE:         self.enable_protections: bool = self.config.get("enable_protections", False)
# REMOVED_UNUSED_CODE:         migrate_data(config, self.exchange)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.init_backtest()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _validate_pairlists_for_backtesting(self):
# REMOVED_UNUSED_CODE:         if "VolumePairList" in self.pairlists.name_list:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "VolumePairList not allowed for backtesting. Please use StaticPairList instead."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if len(self.strategylist) > 1 and "PrecisionFilter" in self.pairlists.name_list:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "PrecisionFilter not allowed for backtesting multiple strategies."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def cleanup():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         LoggingMixin.show_output = True
# REMOVED_UNUSED_CODE:         enable_database_use()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def init_backtest_detail(self) -> None:
# REMOVED_UNUSED_CODE:         # Load detail timeframe if specified
# REMOVED_UNUSED_CODE:         self.timeframe_detail = str(self.config.get("timeframe_detail", ""))
# REMOVED_UNUSED_CODE:         if self.timeframe_detail:
# REMOVED_UNUSED_CODE:             timeframe_detail_secs = timeframe_to_seconds(self.timeframe_detail)
# REMOVED_UNUSED_CODE:             self.timeframe_detail_td = timedelta(seconds=timeframe_detail_secs)
# REMOVED_UNUSED_CODE:             if self.timeframe_secs <= timeframe_detail_secs:
# REMOVED_UNUSED_CODE:                 raise OperationalException(
# REMOVED_UNUSED_CODE:                     "Detail timeframe must be smaller than strategy timeframe."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             self.timeframe_detail_td = timedelta(seconds=0)
# REMOVED_UNUSED_CODE:         self.detail_data: dict[str, DataFrame] = {}
# REMOVED_UNUSED_CODE:         self.futures_data: dict[str, DataFrame] = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def init_backtest(self):
# REMOVED_UNUSED_CODE:         self.prepare_backtest(False)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.wallets = Wallets(self.config, self.exchange, is_backtest=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.progress = BTProgress()
# REMOVED_UNUSED_CODE:         self.abort = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _set_strategy(self, strategy: IStrategy):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Load strategy into backtesting
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.strategy: IStrategy = strategy
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         strategy.dp = self.dataprovider
# REMOVED_UNUSED_CODE:         # Attach Wallets to Strategy baseclass
# REMOVED_UNUSED_CODE:         strategy.wallets = self.wallets
# REMOVED_UNUSED_CODE:         # Set stoploss_on_exchange to false for backtesting,
# REMOVED_UNUSED_CODE:         # since a "perfect" stoploss-exit is assumed anyway
# REMOVED_UNUSED_CODE:         # And the regular "stoploss" function would not apply to that case
# REMOVED_UNUSED_CODE:         self.strategy.order_types["stoploss_on_exchange"] = False
# REMOVED_UNUSED_CODE:         # Update can_short flag
# REMOVED_UNUSED_CODE:         self._can_short = self.trading_mode != TradingMode.SPOT and strategy.can_short
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.strategy.ft_bot_start()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _load_protections(self, strategy: IStrategy):
# REMOVED_UNUSED_CODE:         if self.config.get("enable_protections", False):
# REMOVED_UNUSED_CODE:             self.protections = ProtectionManager(self.config, strategy.protections)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def load_bt_data(self) -> tuple[dict[str, DataFrame], TimeRange]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Loads backtest data and returns the data combined with the timerange
# REMOVED_UNUSED_CODE:         as tuple.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.progress.init_step(BacktestState.DATALOAD, 1)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         data = history.load_data(
# REMOVED_UNUSED_CODE:             datadir=self.config["datadir"],
# REMOVED_UNUSED_CODE:             pairs=self.pairlists.whitelist,
# REMOVED_UNUSED_CODE:             timeframe=self.timeframe,
# REMOVED_UNUSED_CODE:             timerange=self.timerange,
# REMOVED_UNUSED_CODE:             startup_candles=self.required_startup,
# REMOVED_UNUSED_CODE:             fail_without_data=True,
# REMOVED_UNUSED_CODE:             data_format=self.config["dataformat_ohlcv"],
# REMOVED_UNUSED_CODE:             candle_type=self.config.get("candle_type_def", CandleType.SPOT),
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         min_date, max_date = history.get_timerange(data)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.info(
# REMOVED_UNUSED_CODE:             f"Loading data from {min_date.strftime(DATETIME_PRINT_FORMAT)} "
# REMOVED_UNUSED_CODE:             f"up to {max_date.strftime(DATETIME_PRINT_FORMAT)} "
# REMOVED_UNUSED_CODE:             f"({(max_date - min_date).days} days)."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Adjust startts forward if not enough data is available
# REMOVED_UNUSED_CODE:         self.timerange.adjust_start_if_necessary(
# REMOVED_UNUSED_CODE:             timeframe_to_seconds(self.timeframe), self.required_startup, min_date
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.progress.set_new_value(1)
# REMOVED_UNUSED_CODE:         return data, self.timerange
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def load_bt_data_detail(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Loads backtest detail data (smaller timeframe) if necessary.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self.timeframe_detail:
# REMOVED_UNUSED_CODE:             self.detail_data = history.load_data(
# REMOVED_UNUSED_CODE:                 datadir=self.config["datadir"],
# REMOVED_UNUSED_CODE:                 pairs=self.pairlists.whitelist,
# REMOVED_UNUSED_CODE:                 timeframe=self.timeframe_detail,
# REMOVED_UNUSED_CODE:                 timerange=self.timerange,
# REMOVED_UNUSED_CODE:                 startup_candles=0,
# REMOVED_UNUSED_CODE:                 fail_without_data=True,
# REMOVED_UNUSED_CODE:                 data_format=self.config["dataformat_ohlcv"],
# REMOVED_UNUSED_CODE:                 candle_type=self.config.get("candle_type_def", CandleType.SPOT),
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             self.detail_data = {}
# REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES:
# REMOVED_UNUSED_CODE:             funding_fee_timeframe: str = self.exchange.get_option("funding_fee_timeframe")
# REMOVED_UNUSED_CODE:             self.funding_fee_timeframe_secs: int = timeframe_to_seconds(funding_fee_timeframe)
# REMOVED_UNUSED_CODE:             mark_timeframe: str = self.exchange.get_option("mark_ohlcv_timeframe")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Load additional futures data.
# REMOVED_UNUSED_CODE:             funding_rates_dict = history.load_data(
# REMOVED_UNUSED_CODE:                 datadir=self.config["datadir"],
# REMOVED_UNUSED_CODE:                 pairs=self.pairlists.whitelist,
# REMOVED_UNUSED_CODE:                 timeframe=funding_fee_timeframe,
# REMOVED_UNUSED_CODE:                 timerange=self.timerange,
# REMOVED_UNUSED_CODE:                 startup_candles=0,
# REMOVED_UNUSED_CODE:                 fail_without_data=True,
# REMOVED_UNUSED_CODE:                 data_format=self.config["dataformat_ohlcv"],
# REMOVED_UNUSED_CODE:                 candle_type=CandleType.FUNDING_RATE,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # For simplicity, assign to CandleType.Mark (might contain index candles!)
# REMOVED_UNUSED_CODE:             mark_rates_dict = history.load_data(
# REMOVED_UNUSED_CODE:                 datadir=self.config["datadir"],
# REMOVED_UNUSED_CODE:                 pairs=self.pairlists.whitelist,
# REMOVED_UNUSED_CODE:                 timeframe=mark_timeframe,
# REMOVED_UNUSED_CODE:                 timerange=self.timerange,
# REMOVED_UNUSED_CODE:                 startup_candles=0,
# REMOVED_UNUSED_CODE:                 fail_without_data=True,
# REMOVED_UNUSED_CODE:                 data_format=self.config["dataformat_ohlcv"],
# REMOVED_UNUSED_CODE:                 candle_type=CandleType.from_string(self.exchange.get_option("mark_ohlcv_price")),
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             # Combine data to avoid combining the data per trade.
# REMOVED_UNUSED_CODE:             unavailable_pairs = []
# REMOVED_UNUSED_CODE:             for pair in self.pairlists.whitelist:
# REMOVED_UNUSED_CODE:                 if pair not in self.exchange._leverage_tiers:
# REMOVED_UNUSED_CODE:                     unavailable_pairs.append(pair)
# REMOVED_UNUSED_CODE:                     continue
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 self.futures_data[pair] = self.exchange.combine_funding_and_mark(
# REMOVED_UNUSED_CODE:                     funding_rates=funding_rates_dict[pair],
# REMOVED_UNUSED_CODE:                     mark_rates=mark_rates_dict[pair],
# REMOVED_UNUSED_CODE:                     futures_funding_rate=self.config.get("futures_funding_rate", None),
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if unavailable_pairs:
# REMOVED_UNUSED_CODE:                 raise OperationalException(
# REMOVED_UNUSED_CODE:                     f"Pairs {', '.join(unavailable_pairs)} got no leverage tiers available. "
# REMOVED_UNUSED_CODE:                     "It is therefore impossible to backtest with this pair at the moment."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             self.futures_data = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def disable_database_use(self):
# REMOVED_UNUSED_CODE:         disable_database_use(self.timeframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def prepare_backtest(self, enable_protections):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Backtesting setup method - called once for every call to "backtest()".
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.disable_database_use()
# REMOVED_UNUSED_CODE:         PairLocks.reset_locks()
# REMOVED_UNUSED_CODE:         Trade.reset_trades()
# REMOVED_UNUSED_CODE:         CustomDataWrapper.reset_custom_data()
# REMOVED_UNUSED_CODE:         self.rejected_trades = 0
# REMOVED_UNUSED_CODE:         self.timedout_entry_orders = 0
# REMOVED_UNUSED_CODE:         self.timedout_exit_orders = 0
# REMOVED_UNUSED_CODE:         self.canceled_trade_entries = 0
# REMOVED_UNUSED_CODE:         self.canceled_entry_orders = 0
# REMOVED_UNUSED_CODE:         self.replaced_entry_orders = 0
# REMOVED_UNUSED_CODE:         self.dataprovider.clear_cache()
# REMOVED_UNUSED_CODE:         if enable_protections:
# REMOVED_UNUSED_CODE:             self._load_protections(self.strategy)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def check_abort(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check if abort was requested, raise DependencyException if that's the case
# REMOVED_UNUSED_CODE:         Only applies to Interactive backtest mode (webserver mode)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self.abort:
# REMOVED_UNUSED_CODE:             self.abort = False
# REMOVED_UNUSED_CODE:             raise DependencyException("Stop requested")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _get_ohlcv_as_lists(self, processed: dict[str, DataFrame]) -> dict[str, tuple]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Helper function to convert a processed dataframes into lists for performance reasons.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         Used by backtest() - so keep this optimized for performance.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param processed: a processed dictionary with format {pair, data}, which gets cleared to
# REMOVED_UNUSED_CODE:         optimize memory usage!
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         data: dict = {}
# REMOVED_UNUSED_CODE:         self.progress.init_step(BacktestState.CONVERT, len(processed))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Create dict with data
# REMOVED_UNUSED_CODE:         for pair in processed.keys():
# REMOVED_UNUSED_CODE:             pair_data = processed[pair]
# REMOVED_UNUSED_CODE:             self.check_abort()
# REMOVED_UNUSED_CODE:             self.progress.increment()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if not pair_data.empty:
# REMOVED_UNUSED_CODE:                 # Cleanup from prior runs
# REMOVED_UNUSED_CODE:                 pair_data.drop(HEADERS[5:] + ["buy", "sell"], axis=1, errors="ignore")
# REMOVED_UNUSED_CODE:             df_analyzed = self.strategy.ft_advise_signals(pair_data, {"pair": pair})
# REMOVED_UNUSED_CODE:             # Update dataprovider cache
# REMOVED_UNUSED_CODE:             self.dataprovider._set_cached_df(
# REMOVED_UNUSED_CODE:                 pair, self.timeframe, df_analyzed, self.config["candle_type_def"]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Trim startup period from analyzed dataframe
# REMOVED_UNUSED_CODE:             df_analyzed = processed[pair] = pair_data = trim_dataframe(
# REMOVED_UNUSED_CODE:                 df_analyzed, self.timerange, startup_candles=self.required_startup
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Create a copy of the dataframe before shifting, that way the entry signal/tag
# REMOVED_UNUSED_CODE:             # remains on the correct candle for callbacks.
# REMOVED_UNUSED_CODE:             df_analyzed = df_analyzed.copy()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # To avoid using data from future, we use entry/exit signals shifted
# REMOVED_UNUSED_CODE:             # from the previous candle
# REMOVED_UNUSED_CODE:             for col in HEADERS[5:]:
# REMOVED_UNUSED_CODE:                 tag_col = col in ("enter_tag", "exit_tag")
# REMOVED_UNUSED_CODE:                 if col in df_analyzed.columns:
# REMOVED_UNUSED_CODE:                     df_analyzed[col] = (
# REMOVED_UNUSED_CODE:                         df_analyzed.loc[:, col]
# REMOVED_UNUSED_CODE:                         .replace([nan], [0 if not tag_col else None])
# REMOVED_UNUSED_CODE:                         .shift(1)
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 elif not df_analyzed.empty:
# REMOVED_UNUSED_CODE:                     df_analyzed[col] = 0 if not tag_col else None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             df_analyzed = df_analyzed.drop(df_analyzed.head(1).index)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Convert from Pandas to list for performance reasons
# REMOVED_UNUSED_CODE:             # (Looping Pandas is slow.)
# REMOVED_UNUSED_CODE:             data[pair] = df_analyzed[HEADERS].values.tolist() if not df_analyzed.empty else []
# REMOVED_UNUSED_CODE:         return data
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _get_close_rate(
# REMOVED_UNUSED_CODE:         self, row: tuple, trade: LocalTrade, exit_: ExitCheckTuple, trade_dur: int
# REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get close rate for backtesting result
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Special handling if high or low hit STOP_LOSS or ROI
# REMOVED_UNUSED_CODE:         if exit_.exit_type in (
# REMOVED_UNUSED_CODE:             ExitType.STOP_LOSS,
# REMOVED_UNUSED_CODE:             ExitType.TRAILING_STOP_LOSS,
# REMOVED_UNUSED_CODE:             ExitType.LIQUIDATION,
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             return self._get_close_rate_for_stoploss(row, trade, exit_, trade_dur)
# REMOVED_UNUSED_CODE:         elif exit_.exit_type == (ExitType.ROI):
# REMOVED_UNUSED_CODE:             return self._get_close_rate_for_roi(row, trade, exit_, trade_dur)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return row[OPEN_IDX]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _get_close_rate_for_stoploss(
# REMOVED_UNUSED_CODE:         self, row: tuple, trade: LocalTrade, exit_: ExitCheckTuple, trade_dur: int
# REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE:         # our stoploss was already lower than candle high,
# REMOVED_UNUSED_CODE:         # possibly due to a cancelled trade exit.
# REMOVED_UNUSED_CODE:         # exit at open price.
# REMOVED_UNUSED_CODE:         is_short = trade.is_short or False
# REMOVED_UNUSED_CODE:         leverage = trade.leverage or 1.0
# REMOVED_UNUSED_CODE:         side_1 = -1 if is_short else 1
# REMOVED_UNUSED_CODE:         if exit_.exit_type == ExitType.LIQUIDATION and trade.liquidation_price:
# REMOVED_UNUSED_CODE:             stoploss_value = trade.liquidation_price
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             stoploss_value = trade.stop_loss
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if is_short:
# REMOVED_UNUSED_CODE:             if stoploss_value < row[LOW_IDX]:
# REMOVED_UNUSED_CODE:                 return row[OPEN_IDX]
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             if stoploss_value > row[HIGH_IDX]:
# REMOVED_UNUSED_CODE:                 return row[OPEN_IDX]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Special case: trailing triggers within same candle as trade opened. Assume most
# REMOVED_UNUSED_CODE:         # pessimistic price movement, which is moving just enough to arm stoploss and
# REMOVED_UNUSED_CODE:         # immediately going down to stop price.
# REMOVED_UNUSED_CODE:         if exit_.exit_type == ExitType.TRAILING_STOP_LOSS and trade_dur == 0:
# REMOVED_UNUSED_CODE:             if (
# REMOVED_UNUSED_CODE:                 not self.strategy.use_custom_stoploss
# REMOVED_UNUSED_CODE:                 and self.strategy.trailing_stop
# REMOVED_UNUSED_CODE:                 and self.strategy.trailing_only_offset_is_reached
# REMOVED_UNUSED_CODE:                 and self.strategy.trailing_stop_positive_offset is not None
# REMOVED_UNUSED_CODE:                 and self.strategy.trailing_stop_positive
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 # Worst case: price reaches stop_positive_offset and dives down.
# REMOVED_UNUSED_CODE:                 stop_rate = row[OPEN_IDX] * (
# REMOVED_UNUSED_CODE:                     1
# REMOVED_UNUSED_CODE:                     + side_1 * abs(self.strategy.trailing_stop_positive_offset)
# REMOVED_UNUSED_CODE:                     - side_1 * abs(self.strategy.trailing_stop_positive / leverage)
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 # Worst case: price ticks tiny bit above open and dives down.
# REMOVED_UNUSED_CODE:                 stop_rate = row[OPEN_IDX] * (
# REMOVED_UNUSED_CODE:                     1 - side_1 * abs((trade.stop_loss_pct or 0.0) / leverage)
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Limit lower-end to candle low to avoid exits below the low.
# REMOVED_UNUSED_CODE:             # This still remains "worst case" - but "worst realistic case".
# REMOVED_UNUSED_CODE:             if is_short:
# REMOVED_UNUSED_CODE:                 return min(row[HIGH_IDX], stop_rate)
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 return max(row[LOW_IDX], stop_rate)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Set close_rate to stoploss
# REMOVED_UNUSED_CODE:         return stoploss_value
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _get_close_rate_for_roi(
# REMOVED_UNUSED_CODE:         self, row: tuple, trade: LocalTrade, exit_: ExitCheckTuple, trade_dur: int
# REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE:         is_short = trade.is_short or False
# REMOVED_UNUSED_CODE:         leverage = trade.leverage or 1.0
# REMOVED_UNUSED_CODE:         side_1 = -1 if is_short else 1
# REMOVED_UNUSED_CODE:         roi_entry, roi = self.strategy.min_roi_reached_entry(trade_dur)
# REMOVED_UNUSED_CODE:         if roi is not None and roi_entry is not None:
# REMOVED_UNUSED_CODE:             if roi == -1 and roi_entry % self.timeframe_min == 0:
# REMOVED_UNUSED_CODE:                 # When force_exiting with ROI=-1, the roi time will always be equal to trade_dur.
# REMOVED_UNUSED_CODE:                 # If that entry is a multiple of the timeframe (so on candle open)
# REMOVED_UNUSED_CODE:                 # - we'll use open instead of close
# REMOVED_UNUSED_CODE:                 return row[OPEN_IDX]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # - (Expected abs profit - open_rate - open_fee) / (fee_close -1)
# REMOVED_UNUSED_CODE:             roi_rate = trade.open_rate * roi / leverage
# REMOVED_UNUSED_CODE:             open_fee_rate = side_1 * trade.open_rate * (1 + side_1 * trade.fee_open)
# REMOVED_UNUSED_CODE:             close_rate = -(roi_rate + open_fee_rate) / ((trade.fee_close or 0.0) - side_1 * 1)
# REMOVED_UNUSED_CODE:             if is_short:
# REMOVED_UNUSED_CODE:                 is_new_roi = row[OPEN_IDX] < close_rate
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 is_new_roi = row[OPEN_IDX] > close_rate
# REMOVED_UNUSED_CODE:             if (
# REMOVED_UNUSED_CODE:                 trade_dur > 0
# REMOVED_UNUSED_CODE:                 and trade_dur == roi_entry
# REMOVED_UNUSED_CODE:                 and roi_entry % self.timeframe_min == 0
# REMOVED_UNUSED_CODE:                 and is_new_roi
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 # new ROI entry came into effect.
# REMOVED_UNUSED_CODE:                 # use Open rate if open_rate > calculated exit rate
# REMOVED_UNUSED_CODE:                 return row[OPEN_IDX]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if trade_dur == 0 and (
# REMOVED_UNUSED_CODE:                 (
# REMOVED_UNUSED_CODE:                     is_short
# REMOVED_UNUSED_CODE:                     # Red candle (for longs)
# REMOVED_UNUSED_CODE:                     and row[OPEN_IDX] < row[CLOSE_IDX]  # Red candle
# REMOVED_UNUSED_CODE:                     and trade.open_rate > row[OPEN_IDX]  # trade-open above open_rate
# REMOVED_UNUSED_CODE:                     and close_rate < row[CLOSE_IDX]  # closes below close
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 or (
# REMOVED_UNUSED_CODE:                     not is_short
# REMOVED_UNUSED_CODE:                     # green candle (for shorts)
# REMOVED_UNUSED_CODE:                     and row[OPEN_IDX] > row[CLOSE_IDX]  # green candle
# REMOVED_UNUSED_CODE:                     and trade.open_rate < row[OPEN_IDX]  # trade-open below open_rate
# REMOVED_UNUSED_CODE:                     and close_rate > row[CLOSE_IDX]  # closes above close
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 # ROI on opening candles with custom pricing can only
# REMOVED_UNUSED_CODE:                 # trigger if the entry was at Open or lower wick.
# REMOVED_UNUSED_CODE:                 # details: https: // github.com/freqtrade/freqtrade/issues/6261
# REMOVED_UNUSED_CODE:                 # If open_rate is < open, only allow exits below the close on red candles.
# REMOVED_UNUSED_CODE:                 raise ValueError("Opening candle ROI on red candles.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Use the maximum between close_rate and low as we
# REMOVED_UNUSED_CODE:             # cannot exit outside of a candle.
# REMOVED_UNUSED_CODE:             # Applies when a new ROI setting comes in place and the whole candle is above that.
# REMOVED_UNUSED_CODE:             return min(max(close_rate, row[LOW_IDX]), row[HIGH_IDX])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # This should not be reached...
# REMOVED_UNUSED_CODE:             return row[OPEN_IDX]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _get_adjust_trade_entry_for_candle(
# REMOVED_UNUSED_CODE:         self, trade: LocalTrade, row: tuple, current_time: datetime
# REMOVED_UNUSED_CODE:     ) -> LocalTrade:
# REMOVED_UNUSED_CODE:         current_rate: float = row[OPEN_IDX]
# REMOVED_UNUSED_CODE:         current_profit = trade.calc_profit_ratio(current_rate)
# REMOVED_UNUSED_CODE:         min_stake = self.exchange.get_min_pair_stake_amount(trade.pair, current_rate, -0.1)
# REMOVED_UNUSED_CODE:         max_stake = self.exchange.get_max_pair_stake_amount(trade.pair, current_rate)
# REMOVED_UNUSED_CODE:         stake_available = self.wallets.get_available_stake_amount()
# REMOVED_UNUSED_CODE:         stake_amount, order_tag = self.strategy._adjust_trade_position_internal(
# REMOVED_UNUSED_CODE:             trade=trade,  # type: ignore[arg-type]
# REMOVED_UNUSED_CODE:             current_time=current_time,
# REMOVED_UNUSED_CODE:             current_rate=current_rate,
# REMOVED_UNUSED_CODE:             current_profit=current_profit,
# REMOVED_UNUSED_CODE:             min_stake=min_stake,
# REMOVED_UNUSED_CODE:             max_stake=min(max_stake, stake_available),
# REMOVED_UNUSED_CODE:             current_entry_rate=current_rate,
# REMOVED_UNUSED_CODE:             current_exit_rate=current_rate,
# REMOVED_UNUSED_CODE:             current_entry_profit=current_profit,
# REMOVED_UNUSED_CODE:             current_exit_profit=current_profit,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Check if we should increase our position
# REMOVED_UNUSED_CODE:         if stake_amount is not None and stake_amount > 0.0:
# REMOVED_UNUSED_CODE:             check_adjust_entry = True
# REMOVED_UNUSED_CODE:             if self.strategy.max_entry_position_adjustment > -1:
# REMOVED_UNUSED_CODE:                 entry_count = trade.nr_of_successful_entries
# REMOVED_UNUSED_CODE:                 check_adjust_entry = entry_count <= self.strategy.max_entry_position_adjustment
# REMOVED_UNUSED_CODE:             if check_adjust_entry:
# REMOVED_UNUSED_CODE:                 pos_trade = self._enter_trade(
# REMOVED_UNUSED_CODE:                     trade.pair,
# REMOVED_UNUSED_CODE:                     row,
# REMOVED_UNUSED_CODE:                     "short" if trade.is_short else "long",
# REMOVED_UNUSED_CODE:                     stake_amount,
# REMOVED_UNUSED_CODE:                     trade,
# REMOVED_UNUSED_CODE:                     entry_tag1=order_tag,
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 if pos_trade is not None:
# REMOVED_UNUSED_CODE:                     self.wallets.update()
# REMOVED_UNUSED_CODE:                     return pos_trade
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if stake_amount is not None and stake_amount < 0.0:
# REMOVED_UNUSED_CODE:             amount = amount_to_contract_precision(
# REMOVED_UNUSED_CODE:                 abs(
# REMOVED_UNUSED_CODE:                     float(
# REMOVED_UNUSED_CODE:                         FtPrecise(stake_amount)
# REMOVED_UNUSED_CODE:                         * FtPrecise(trade.amount)
# REMOVED_UNUSED_CODE:                         / FtPrecise(trade.stake_amount)
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 ),
# REMOVED_UNUSED_CODE:                 trade.amount_precision,
# REMOVED_UNUSED_CODE:                 self.precision_mode,
# REMOVED_UNUSED_CODE:                 trade.contract_size,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             if amount == 0.0:
# REMOVED_UNUSED_CODE:                 return trade
# REMOVED_UNUSED_CODE:             remaining = (trade.amount - amount) * current_rate
# REMOVED_UNUSED_CODE:             if min_stake and remaining != 0 and remaining < min_stake:
# REMOVED_UNUSED_CODE:                 # Remaining stake is too low to be sold.
# REMOVED_UNUSED_CODE:                 return trade
# REMOVED_UNUSED_CODE:             exit_ = ExitCheckTuple(ExitType.PARTIAL_EXIT, order_tag)
# REMOVED_UNUSED_CODE:             pos_trade = self._get_exit_for_signal(trade, row, exit_, current_time, amount)
# REMOVED_UNUSED_CODE:             if pos_trade is not None:
# REMOVED_UNUSED_CODE:                 order = pos_trade.orders[-1]
# REMOVED_UNUSED_CODE:                 # If the order was filled and for the full trade amount, we need to close the trade.
# REMOVED_UNUSED_CODE:                 self._process_exit_order(order, pos_trade, current_time, row, trade.pair)
# REMOVED_UNUSED_CODE:                 return pos_trade
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return trade
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _get_order_filled(self, rate: float, row: tuple) -> bool:
# REMOVED_UNUSED_CODE:         """Rate is within candle, therefore filled"""
# REMOVED_UNUSED_CODE:         return row[LOW_IDX] <= rate <= row[HIGH_IDX]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _call_adjust_stop(self, current_date: datetime, trade: LocalTrade, current_rate: float):
# REMOVED_UNUSED_CODE:         profit = trade.calc_profit_ratio(current_rate)
# REMOVED_UNUSED_CODE:         self.strategy.ft_stoploss_adjust(
# REMOVED_UNUSED_CODE:             current_rate,
# REMOVED_UNUSED_CODE:             trade,  # type: ignore
# REMOVED_UNUSED_CODE:             current_date,
# REMOVED_UNUSED_CODE:             profit,
# REMOVED_UNUSED_CODE:             0,
# REMOVED_UNUSED_CODE:             after_fill=True,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _try_close_open_order(
# REMOVED_UNUSED_CODE:         self, order: Order | None, trade: LocalTrade, current_date: datetime, row: tuple
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check if an order is open and if it should've filled.
# REMOVED_UNUSED_CODE:         :return:  True if the order filled.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if order and self._get_order_filled(order.ft_price, row):
# REMOVED_UNUSED_CODE:             order.close_bt_order(current_date, trade)
# REMOVED_UNUSED_CODE:             self._run_funding_fees(trade, current_date, force=True)
# REMOVED_UNUSED_CODE:             strategy_safe_wrapper(self.strategy.order_filled, default_retval=None)(
# REMOVED_UNUSED_CODE:                 pair=trade.pair,
# REMOVED_UNUSED_CODE:                 trade=trade,  # type: ignore[arg-type]
# REMOVED_UNUSED_CODE:                 order=order,
# REMOVED_UNUSED_CODE:                 current_time=current_date,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if self.margin_mode == MarginMode.CROSS or not (
# REMOVED_UNUSED_CODE:                 order.ft_order_side == trade.exit_side and order.safe_amount == trade.amount
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 # trade is still open or we are in cross margin mode and
# REMOVED_UNUSED_CODE:                 # must update all liquidation prices
# REMOVED_UNUSED_CODE:                 update_liquidation_prices(
# REMOVED_UNUSED_CODE:                     trade,
# REMOVED_UNUSED_CODE:                     exchange=self.exchange,
# REMOVED_UNUSED_CODE:                     wallets=self.wallets,
# REMOVED_UNUSED_CODE:                     stake_currency=self.config["stake_currency"],
# REMOVED_UNUSED_CODE:                     dry_run=self.config["dry_run"],
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             if not (order.ft_order_side == trade.exit_side and order.safe_amount == trade.amount):
# REMOVED_UNUSED_CODE:                 self._call_adjust_stop(current_date, trade, order.ft_price)
# REMOVED_UNUSED_CODE:             return True
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _process_exit_order(
# REMOVED_UNUSED_CODE:         self, order: Order, trade: LocalTrade, current_time: datetime, row: tuple, pair: str
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Takes an exit order and processes it, potentially closing the trade.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self._try_close_open_order(order, trade, current_time, row):
# REMOVED_UNUSED_CODE:             sub_trade = order.safe_amount_after_fee != trade.amount
# REMOVED_UNUSED_CODE:             if sub_trade:
# REMOVED_UNUSED_CODE:                 trade.recalc_trade_from_orders()
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade.close_date = current_time
# REMOVED_UNUSED_CODE:                 trade.close(order.ft_price, show_msg=False)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 LocalTrade.close_bt_trade(trade)
# REMOVED_UNUSED_CODE:             self.wallets.update()
# REMOVED_UNUSED_CODE:             self.run_protections(pair, current_time, trade.trade_direction)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _get_exit_for_signal(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         trade: LocalTrade,
# REMOVED_UNUSED_CODE:         row: tuple,
# REMOVED_UNUSED_CODE:         exit_: ExitCheckTuple,
# REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE:         amount: float | None = None,
# REMOVED_UNUSED_CODE:     ) -> LocalTrade | None:
# REMOVED_UNUSED_CODE:         if exit_.exit_flag:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade.close_date = current_time
# REMOVED_UNUSED_CODE:             exit_reason = exit_.exit_reason
# REMOVED_UNUSED_CODE:             amount_ = amount if amount is not None else trade.amount
# REMOVED_UNUSED_CODE:             trade_dur = int((trade.close_date_utc - trade.open_date_utc).total_seconds() // 60)
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 close_rate = self._get_close_rate(row, trade, exit_, trade_dur)
# REMOVED_UNUSED_CODE:             except ValueError:
# REMOVED_UNUSED_CODE:                 return None
# REMOVED_UNUSED_CODE:             # call the custom exit price,with default value as previous close_rate
# REMOVED_UNUSED_CODE:             current_profit = trade.calc_profit_ratio(close_rate)
# REMOVED_UNUSED_CODE:             order_type = self.strategy.order_types["exit"]
# REMOVED_UNUSED_CODE:             if exit_.exit_type in (
# REMOVED_UNUSED_CODE:                 ExitType.EXIT_SIGNAL,
# REMOVED_UNUSED_CODE:                 ExitType.CUSTOM_EXIT,
# REMOVED_UNUSED_CODE:                 ExitType.PARTIAL_EXIT,
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 # Checks and adds an exit tag, after checking that the length of the
# REMOVED_UNUSED_CODE:                 # row has the length for an exit tag column
# REMOVED_UNUSED_CODE:                 if (
# REMOVED_UNUSED_CODE:                     len(row) > EXIT_TAG_IDX
# REMOVED_UNUSED_CODE:                     and row[EXIT_TAG_IDX] is not None
# REMOVED_UNUSED_CODE:                     and len(row[EXIT_TAG_IDX]) > 0
# REMOVED_UNUSED_CODE:                     and exit_.exit_type in (ExitType.EXIT_SIGNAL,)
# REMOVED_UNUSED_CODE:                 ):
# REMOVED_UNUSED_CODE:                     exit_reason = row[EXIT_TAG_IDX]
# REMOVED_UNUSED_CODE:                 # Custom exit pricing only for exit-signals
# REMOVED_UNUSED_CODE:                 if order_type == "limit":
# REMOVED_UNUSED_CODE:                     rate = strategy_safe_wrapper(
# REMOVED_UNUSED_CODE:                         self.strategy.custom_exit_price, default_retval=close_rate
# REMOVED_UNUSED_CODE:                     )(
# REMOVED_UNUSED_CODE:                         pair=trade.pair,
# REMOVED_UNUSED_CODE:                         trade=trade,  # type: ignore[arg-type]
# REMOVED_UNUSED_CODE:                         current_time=current_time,
# REMOVED_UNUSED_CODE:                         proposed_rate=close_rate,
# REMOVED_UNUSED_CODE:                         current_profit=current_profit,
# REMOVED_UNUSED_CODE:                         exit_tag=exit_reason,
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     if rate is not None and rate != close_rate:
# REMOVED_UNUSED_CODE:                         close_rate = price_to_precision(
# REMOVED_UNUSED_CODE:                             rate, trade.price_precision, self.precision_mode_price
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:                     # We can't place orders lower than current low.
# REMOVED_UNUSED_CODE:                     # freqtrade does not support this in live, and the order would fill immediately
# REMOVED_UNUSED_CODE:                     if trade.is_short:
# REMOVED_UNUSED_CODE:                         close_rate = min(close_rate, row[HIGH_IDX])
# REMOVED_UNUSED_CODE:                     else:
# REMOVED_UNUSED_CODE:                         close_rate = max(close_rate, row[LOW_IDX])
# REMOVED_UNUSED_CODE:             # Confirm trade exit:
# REMOVED_UNUSED_CODE:             time_in_force = self.strategy.order_time_in_force["exit"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if exit_.exit_type not in (
# REMOVED_UNUSED_CODE:                 ExitType.LIQUIDATION,
# REMOVED_UNUSED_CODE:                 ExitType.PARTIAL_EXIT,
# REMOVED_UNUSED_CODE:             ) and not strategy_safe_wrapper(self.strategy.confirm_trade_exit, default_retval=True)(
# REMOVED_UNUSED_CODE:                 pair=trade.pair,
# REMOVED_UNUSED_CODE:                 trade=trade,  # type: ignore[arg-type]
# REMOVED_UNUSED_CODE:                 order_type=order_type,
# REMOVED_UNUSED_CODE:                 amount=amount_,
# REMOVED_UNUSED_CODE:                 rate=close_rate,
# REMOVED_UNUSED_CODE:                 time_in_force=time_in_force,
# REMOVED_UNUSED_CODE:                 sell_reason=exit_reason,  # deprecated
# REMOVED_UNUSED_CODE:                 exit_reason=exit_reason,
# REMOVED_UNUSED_CODE:                 current_time=current_time,
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             trade.exit_reason = exit_reason
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             return self._exit_trade(trade, row, close_rate, amount_, exit_reason)
# REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _exit_trade(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         trade: LocalTrade,
# REMOVED_UNUSED_CODE:         sell_row: tuple,
# REMOVED_UNUSED_CODE:         close_rate: float,
# REMOVED_UNUSED_CODE:         amount: float,
# REMOVED_UNUSED_CODE:         exit_reason: str | None,
# REMOVED_UNUSED_CODE:     ) -> LocalTrade | None:
# REMOVED_UNUSED_CODE:         self.order_id_counter += 1
# REMOVED_UNUSED_CODE:         exit_candle_time = sell_row[DATE_IDX].to_pydatetime()
# REMOVED_UNUSED_CODE:         order_type = self.strategy.order_types["exit"]
# REMOVED_UNUSED_CODE:         # amount = amount or trade.amount
# REMOVED_UNUSED_CODE:         amount = amount_to_contract_precision(
# REMOVED_UNUSED_CODE:             amount or trade.amount, trade.amount_precision, self.precision_mode, trade.contract_size
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.handle_similar_order(trade, close_rate, amount, trade.exit_side, exit_candle_time):
# REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         order = Order(
# REMOVED_UNUSED_CODE:             id=self.order_id_counter,
# REMOVED_UNUSED_CODE:             ft_trade_id=trade.id,
# REMOVED_UNUSED_CODE:             order_date=exit_candle_time,
# REMOVED_UNUSED_CODE:             order_update_date=exit_candle_time,
# REMOVED_UNUSED_CODE:             ft_is_open=True,
# REMOVED_UNUSED_CODE:             ft_pair=trade.pair,
# REMOVED_UNUSED_CODE:             order_id=str(self.order_id_counter),
# REMOVED_UNUSED_CODE:             symbol=trade.pair,
# REMOVED_UNUSED_CODE:             ft_order_side=trade.exit_side,
# REMOVED_UNUSED_CODE:             side=trade.exit_side,
# REMOVED_UNUSED_CODE:             order_type=order_type,
# REMOVED_UNUSED_CODE:             status="open",
# REMOVED_UNUSED_CODE:             ft_price=close_rate,
# REMOVED_UNUSED_CODE:             price=close_rate,
# REMOVED_UNUSED_CODE:             average=close_rate,
# REMOVED_UNUSED_CODE:             amount=amount,
# REMOVED_UNUSED_CODE:             filled=0,
# REMOVED_UNUSED_CODE:             remaining=amount,
# REMOVED_UNUSED_CODE:             cost=amount * close_rate * (1 + self.fee),
# REMOVED_UNUSED_CODE:             ft_order_tag=exit_reason,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         order._trade_bt = trade
# REMOVED_UNUSED_CODE:         trade.orders.append(order)
# REMOVED_UNUSED_CODE:         return trade
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _check_trade_exit(
# REMOVED_UNUSED_CODE:         self, trade: LocalTrade, row: tuple, current_time: datetime
# REMOVED_UNUSED_CODE:     ) -> LocalTrade | None:
# REMOVED_UNUSED_CODE:         self._run_funding_fees(trade, current_time)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Check if we need to adjust our current positions
# REMOVED_UNUSED_CODE:         if self.strategy.position_adjustment_enable:
# REMOVED_UNUSED_CODE:             trade = self._get_adjust_trade_entry_for_candle(trade, row, current_time)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if trade.is_open:
# REMOVED_UNUSED_CODE:             enter = row[SHORT_IDX] if trade.is_short else row[LONG_IDX]
# REMOVED_UNUSED_CODE:             exit_sig = row[ESHORT_IDX] if trade.is_short else row[ELONG_IDX]
# REMOVED_UNUSED_CODE:             exits = self.strategy.should_exit(
# REMOVED_UNUSED_CODE:                 trade,  # type: ignore
# REMOVED_UNUSED_CODE:                 row[OPEN_IDX],
# REMOVED_UNUSED_CODE:                 row[DATE_IDX].to_pydatetime(),
# REMOVED_UNUSED_CODE:                 enter=enter,
# REMOVED_UNUSED_CODE:                 exit_=exit_sig,
# REMOVED_UNUSED_CODE:                 low=row[LOW_IDX],
# REMOVED_UNUSED_CODE:                 high=row[HIGH_IDX],
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             for exit_ in exits:
# REMOVED_UNUSED_CODE:                 t = self._get_exit_for_signal(trade, row, exit_, current_time)
# REMOVED_UNUSED_CODE:                 if t:
# REMOVED_UNUSED_CODE:                     return t
# REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _run_funding_fees(self, trade: LocalTrade, current_time: datetime, force: bool = False):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Calculate funding fees if necessary and add them to the trade.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES:
# REMOVED_UNUSED_CODE:             if force or (current_time.timestamp() % self.funding_fee_timeframe_secs) == 0:
# REMOVED_UNUSED_CODE:                 # Funding fee interval.
# REMOVED_UNUSED_CODE:                 trade.set_funding_fees(
# REMOVED_UNUSED_CODE:                     self.exchange.calculate_funding_fees(
# REMOVED_UNUSED_CODE:                         self.futures_data[trade.pair],
# REMOVED_UNUSED_CODE:                         amount=trade.amount,
# REMOVED_UNUSED_CODE:                         is_short=trade.is_short,
# REMOVED_UNUSED_CODE:                         open_date=trade.date_last_filled_utc,
# REMOVED_UNUSED_CODE:                         close_date=current_time,
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_valid_price_and_stake(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         row: tuple,
# REMOVED_UNUSED_CODE:         propose_rate: float,
# REMOVED_UNUSED_CODE:         stake_amount: float,
# REMOVED_UNUSED_CODE:         direction: LongShort,
# REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE:         entry_tag: str | None,
# REMOVED_UNUSED_CODE:         trade: LocalTrade | None,
# REMOVED_UNUSED_CODE:         order_type: str,
# REMOVED_UNUSED_CODE:         price_precision: float | None,
# REMOVED_UNUSED_CODE:     ) -> tuple[float, float, float, float]:
# REMOVED_UNUSED_CODE:         if order_type == "limit":
# REMOVED_UNUSED_CODE:             new_rate = strategy_safe_wrapper(
# REMOVED_UNUSED_CODE:                 self.strategy.custom_entry_price, default_retval=propose_rate
# REMOVED_UNUSED_CODE:             )(
# REMOVED_UNUSED_CODE:                 pair=pair,
# REMOVED_UNUSED_CODE:                 trade=trade,  # type: ignore[arg-type]
# REMOVED_UNUSED_CODE:                 current_time=current_time,
# REMOVED_UNUSED_CODE:                 proposed_rate=propose_rate,
# REMOVED_UNUSED_CODE:                 entry_tag=entry_tag,
# REMOVED_UNUSED_CODE:                 side=direction,
# REMOVED_UNUSED_CODE:             )  # default value is the open rate
# REMOVED_UNUSED_CODE:             # We can't place orders higher than current high (otherwise it'd be a stop limit entry)
# REMOVED_UNUSED_CODE:             # which freqtrade does not support in live.
# REMOVED_UNUSED_CODE:             if new_rate is not None and new_rate != propose_rate:
# REMOVED_UNUSED_CODE:                 propose_rate = price_to_precision(
# REMOVED_UNUSED_CODE:                     new_rate, price_precision, self.precision_mode_price
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             if direction == "short":
# REMOVED_UNUSED_CODE:                 propose_rate = max(propose_rate, row[LOW_IDX])
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 propose_rate = min(propose_rate, row[HIGH_IDX])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         pos_adjust = trade is not None
# REMOVED_UNUSED_CODE:         leverage = trade.leverage if trade else 1.0
# REMOVED_UNUSED_CODE:         if not pos_adjust:
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 stake_amount = self.wallets.get_trade_stake_amount(
# REMOVED_UNUSED_CODE:                     pair, self.strategy.max_open_trades, update=False
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             except DependencyException:
# REMOVED_UNUSED_CODE:                 return 0, 0, 0, 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             max_leverage = self.exchange.get_max_leverage(pair, stake_amount)
# REMOVED_UNUSED_CODE:             leverage = (
# REMOVED_UNUSED_CODE:                 strategy_safe_wrapper(self.strategy.leverage, default_retval=1.0)(
# REMOVED_UNUSED_CODE:                     pair=pair,
# REMOVED_UNUSED_CODE:                     current_time=current_time,
# REMOVED_UNUSED_CODE:                     current_rate=row[OPEN_IDX],
# REMOVED_UNUSED_CODE:                     proposed_leverage=1.0,
# REMOVED_UNUSED_CODE:                     max_leverage=max_leverage,
# REMOVED_UNUSED_CODE:                     side=direction,
# REMOVED_UNUSED_CODE:                     entry_tag=entry_tag,
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 if self.trading_mode != TradingMode.SPOT
# REMOVED_UNUSED_CODE:                 else 1.0
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             # Cap leverage between 1.0 and max_leverage.
# REMOVED_UNUSED_CODE:             leverage = min(max(leverage, 1.0), max_leverage)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         min_stake_amount = (
# REMOVED_UNUSED_CODE:             self.exchange.get_min_pair_stake_amount(
# REMOVED_UNUSED_CODE:                 pair, propose_rate, -0.05 if not pos_adjust else 0.0, leverage=leverage
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             or 0
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         max_stake_amount = self.exchange.get_max_pair_stake_amount(
# REMOVED_UNUSED_CODE:             pair, propose_rate, leverage=leverage
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         stake_available = self.wallets.get_available_stake_amount()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not pos_adjust:
# REMOVED_UNUSED_CODE:             stake_amount = strategy_safe_wrapper(
# REMOVED_UNUSED_CODE:                 self.strategy.custom_stake_amount, default_retval=stake_amount
# REMOVED_UNUSED_CODE:             )(
# REMOVED_UNUSED_CODE:                 pair=pair,
# REMOVED_UNUSED_CODE:                 current_time=current_time,
# REMOVED_UNUSED_CODE:                 current_rate=propose_rate,
# REMOVED_UNUSED_CODE:                 proposed_stake=stake_amount,
# REMOVED_UNUSED_CODE:                 min_stake=min_stake_amount,
# REMOVED_UNUSED_CODE:                 max_stake=min(stake_available, max_stake_amount),
# REMOVED_UNUSED_CODE:                 leverage=leverage,
# REMOVED_UNUSED_CODE:                 entry_tag=entry_tag,
# REMOVED_UNUSED_CODE:                 side=direction,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         stake_amount_val = self.wallets.validate_stake_amount(
# REMOVED_UNUSED_CODE:             pair=pair,
# REMOVED_UNUSED_CODE:             stake_amount=stake_amount,
# REMOVED_UNUSED_CODE:             min_stake_amount=min_stake_amount,
# REMOVED_UNUSED_CODE:             max_stake_amount=max_stake_amount,
# REMOVED_UNUSED_CODE:             trade_amount=trade.stake_amount if trade else None,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return propose_rate, stake_amount_val, leverage, min_stake_amount
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _enter_trade(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         row: tuple,
# REMOVED_UNUSED_CODE:         direction: LongShort,
# REMOVED_UNUSED_CODE:         stake_amount: float | None = None,
# REMOVED_UNUSED_CODE:         trade: LocalTrade | None = None,
# REMOVED_UNUSED_CODE:         requested_rate: float | None = None,
# REMOVED_UNUSED_CODE:         requested_stake: float | None = None,
# REMOVED_UNUSED_CODE:         entry_tag1: str | None = None,
# REMOVED_UNUSED_CODE:     ) -> LocalTrade | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         :param trade: Trade to adjust - initial entry if None
# REMOVED_UNUSED_CODE:         :param requested_rate: Adjusted entry rate
# REMOVED_UNUSED_CODE:         :param requested_stake: Stake amount for adjusted orders (`adjust_entry_price`).
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         current_time = row[DATE_IDX].to_pydatetime()
# REMOVED_UNUSED_CODE:         entry_tag = entry_tag1 or (row[ENTER_TAG_IDX] if len(row) >= ENTER_TAG_IDX + 1 else None)
# REMOVED_UNUSED_CODE:         # let's call the custom entry price, using the open price as default price
# REMOVED_UNUSED_CODE:         order_type = self.strategy.order_types["entry"]
# REMOVED_UNUSED_CODE:         pos_adjust = trade is not None and requested_rate is None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         stake_amount_ = stake_amount or (trade.stake_amount if trade else 0.0)
# REMOVED_UNUSED_CODE:         precision_price = self.exchange.get_precision_price(pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         propose_rate, stake_amount, leverage, min_stake_amount = self.get_valid_price_and_stake(
# REMOVED_UNUSED_CODE:             pair,
# REMOVED_UNUSED_CODE:             row,
# REMOVED_UNUSED_CODE:             row[OPEN_IDX],
# REMOVED_UNUSED_CODE:             stake_amount_,
# REMOVED_UNUSED_CODE:             direction,
# REMOVED_UNUSED_CODE:             current_time,
# REMOVED_UNUSED_CODE:             entry_tag,
# REMOVED_UNUSED_CODE:             trade,
# REMOVED_UNUSED_CODE:             order_type,
# REMOVED_UNUSED_CODE:             precision_price,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # replace proposed rate if another rate was requested
# REMOVED_UNUSED_CODE:         propose_rate = requested_rate if requested_rate else propose_rate
# REMOVED_UNUSED_CODE:         stake_amount = requested_stake if requested_stake else stake_amount
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not stake_amount:
# REMOVED_UNUSED_CODE:             # In case of pos adjust, still return the original trade
# REMOVED_UNUSED_CODE:             # If not pos adjust, trade is None
# REMOVED_UNUSED_CODE:             return trade
# REMOVED_UNUSED_CODE:         time_in_force = self.strategy.order_time_in_force["entry"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if stake_amount and (not min_stake_amount or stake_amount >= min_stake_amount):
# REMOVED_UNUSED_CODE:             self.order_id_counter += 1
# REMOVED_UNUSED_CODE:             base_currency = self.exchange.get_pair_base_currency(pair)
# REMOVED_UNUSED_CODE:             amount_p = (stake_amount / propose_rate) * leverage
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             contract_size = self.exchange.get_contract_size(pair)
# REMOVED_UNUSED_CODE:             precision_amount = self.exchange.get_precision_amount(pair)
# REMOVED_UNUSED_CODE:             amount = amount_to_contract_precision(
# REMOVED_UNUSED_CODE:                 amount_p, precision_amount, self.precision_mode, contract_size
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             if not amount:
# REMOVED_UNUSED_CODE:                 # No amount left after truncating to precision.
# REMOVED_UNUSED_CODE:                 return trade
# REMOVED_UNUSED_CODE:             # Backcalculate actual stake amount.
# REMOVED_UNUSED_CODE:             stake_amount = amount * propose_rate / leverage
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if not pos_adjust:
# REMOVED_UNUSED_CODE:                 # Confirm trade entry:
# REMOVED_UNUSED_CODE:                 if not strategy_safe_wrapper(
# REMOVED_UNUSED_CODE:                     self.strategy.confirm_trade_entry, default_retval=True
# REMOVED_UNUSED_CODE:                 )(
# REMOVED_UNUSED_CODE:                     pair=pair,
# REMOVED_UNUSED_CODE:                     order_type=order_type,
# REMOVED_UNUSED_CODE:                     amount=amount,
# REMOVED_UNUSED_CODE:                     rate=propose_rate,
# REMOVED_UNUSED_CODE:                     time_in_force=time_in_force,
# REMOVED_UNUSED_CODE:                     current_time=current_time,
# REMOVED_UNUSED_CODE:                     entry_tag=entry_tag,
# REMOVED_UNUSED_CODE:                     side=direction,
# REMOVED_UNUSED_CODE:                 ):
# REMOVED_UNUSED_CODE:                     return trade
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             is_short = direction == "short"
# REMOVED_UNUSED_CODE:             # Necessary for Margin trading. Disabled until support is enabled.
# REMOVED_UNUSED_CODE:             # interest_rate = self.exchange.get_interest_rate()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if trade is None:
# REMOVED_UNUSED_CODE:                 # Enter trade
# REMOVED_UNUSED_CODE:                 self.trade_id_counter += 1
# REMOVED_UNUSED_CODE:                 trade = LocalTrade(
# REMOVED_UNUSED_CODE:                     id=self.trade_id_counter,
# REMOVED_UNUSED_CODE:                     pair=pair,
# REMOVED_UNUSED_CODE:                     base_currency=base_currency,
# REMOVED_UNUSED_CODE:                     stake_currency=self.config["stake_currency"],
# REMOVED_UNUSED_CODE:                     open_rate=propose_rate,
# REMOVED_UNUSED_CODE:                     open_rate_requested=propose_rate,
# REMOVED_UNUSED_CODE:                     open_date=current_time,
# REMOVED_UNUSED_CODE:                     stake_amount=stake_amount,
# REMOVED_UNUSED_CODE:                     amount=0,
# REMOVED_UNUSED_CODE:                     amount_requested=amount,
# REMOVED_UNUSED_CODE:                     fee_open=self.fee,
# REMOVED_UNUSED_CODE:                     fee_close=self.fee,
# REMOVED_UNUSED_CODE:                     is_open=True,
# REMOVED_UNUSED_CODE:                     enter_tag=entry_tag,
# REMOVED_UNUSED_CODE:                     timeframe=self.timeframe_min,
# REMOVED_UNUSED_CODE:                     exchange=self._exchange_name,
# REMOVED_UNUSED_CODE:                     is_short=is_short,
# REMOVED_UNUSED_CODE:                     trading_mode=self.trading_mode,
# REMOVED_UNUSED_CODE:                     leverage=leverage,
# REMOVED_UNUSED_CODE:                     # interest_rate=interest_rate,
# REMOVED_UNUSED_CODE:                     amount_precision=precision_amount,
# REMOVED_UNUSED_CODE:                     price_precision=precision_price,
# REMOVED_UNUSED_CODE:                     precision_mode=self.precision_mode,
# REMOVED_UNUSED_CODE:                     precision_mode_price=self.precision_mode_price,
# REMOVED_UNUSED_CODE:                     contract_size=contract_size,
# REMOVED_UNUSED_CODE:                     orders=[],
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 LocalTrade.add_bt_trade(trade)
# REMOVED_UNUSED_CODE:             elif self.handle_similar_order(
# REMOVED_UNUSED_CODE:                 trade, propose_rate, amount, trade.entry_side, current_time
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             trade.adjust_stop_loss(trade.open_rate, self.strategy.stoploss, initial=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             order = Order(
# REMOVED_UNUSED_CODE:                 id=self.order_id_counter,
# REMOVED_UNUSED_CODE:                 ft_trade_id=trade.id,
# REMOVED_UNUSED_CODE:                 ft_is_open=True,
# REMOVED_UNUSED_CODE:                 ft_pair=trade.pair,
# REMOVED_UNUSED_CODE:                 order_id=str(self.order_id_counter),
# REMOVED_UNUSED_CODE:                 symbol=trade.pair,
# REMOVED_UNUSED_CODE:                 ft_order_side=trade.entry_side,
# REMOVED_UNUSED_CODE:                 side=trade.entry_side,
# REMOVED_UNUSED_CODE:                 order_type=order_type,
# REMOVED_UNUSED_CODE:                 status="open",
# REMOVED_UNUSED_CODE:                 order_date=current_time,
# REMOVED_UNUSED_CODE:                 order_filled_date=current_time,
# REMOVED_UNUSED_CODE:                 order_update_date=current_time,
# REMOVED_UNUSED_CODE:                 ft_price=propose_rate,
# REMOVED_UNUSED_CODE:                 price=propose_rate,
# REMOVED_UNUSED_CODE:                 average=propose_rate,
# REMOVED_UNUSED_CODE:                 amount=amount,
# REMOVED_UNUSED_CODE:                 filled=0,
# REMOVED_UNUSED_CODE:                 remaining=amount,
# REMOVED_UNUSED_CODE:                 cost=amount * propose_rate * (1 + self.fee),
# REMOVED_UNUSED_CODE:                 ft_order_tag=entry_tag,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             order._trade_bt = trade
# REMOVED_UNUSED_CODE:             trade.orders.append(order)
# REMOVED_UNUSED_CODE:             self._try_close_open_order(order, trade, current_time, row)
# REMOVED_UNUSED_CODE:             trade.recalc_trade_from_orders()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return trade
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def handle_left_open(
# REMOVED_UNUSED_CODE:         self, open_trades: dict[str, list[LocalTrade]], data: dict[str, list[tuple]]
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handling of left open trades at the end of backtesting
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         for pair in open_trades.keys():
# REMOVED_UNUSED_CODE:             for trade in list(open_trades[pair]):
# REMOVED_UNUSED_CODE:                 if (
# REMOVED_UNUSED_CODE:                     trade.has_open_orders and trade.nr_of_successful_entries == 0
# REMOVED_UNUSED_CODE:                 ) or not trade.has_open_position:
# REMOVED_UNUSED_CODE:                     # Ignore trade if entry-order did not fill yet
# REMOVED_UNUSED_CODE:                     LocalTrade.remove_bt_trade(trade)
# REMOVED_UNUSED_CODE:                     continue
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 exit_row = data[pair][-1]
# REMOVED_UNUSED_CODE:                 self._exit_trade(
# REMOVED_UNUSED_CODE:                     trade, exit_row, exit_row[OPEN_IDX], trade.amount, ExitType.FORCE_EXIT.value
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 trade.exit_reason = ExitType.FORCE_EXIT.value
# REMOVED_UNUSED_CODE:                 self._process_exit_order(
# REMOVED_UNUSED_CODE:                     trade.orders[-1], trade, exit_row[DATE_IDX].to_pydatetime(), exit_row, pair
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def trade_slot_available(self, open_trade_count: int) -> bool:
# REMOVED_UNUSED_CODE:         # Always allow trades when max_open_trades is enabled.
# REMOVED_UNUSED_CODE:         max_open_trades: IntOrInf = self.strategy.max_open_trades
# REMOVED_UNUSED_CODE:         if max_open_trades <= 0 or open_trade_count < max_open_trades:
# REMOVED_UNUSED_CODE:             return True
# REMOVED_UNUSED_CODE:         # Rejected trade
# REMOVED_UNUSED_CODE:         self.rejected_trades += 1
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def check_for_trade_entry(self, row) -> LongShort | None:
# REMOVED_UNUSED_CODE:         enter_long = row[LONG_IDX] == 1
# REMOVED_UNUSED_CODE:         exit_long = row[ELONG_IDX] == 1
# REMOVED_UNUSED_CODE:         enter_short = self._can_short and row[SHORT_IDX] == 1
# REMOVED_UNUSED_CODE:         exit_short = self._can_short and row[ESHORT_IDX] == 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if enter_long == 1 and not any([exit_long, enter_short]):
# REMOVED_UNUSED_CODE:             # Long
# REMOVED_UNUSED_CODE:             return "long"
# REMOVED_UNUSED_CODE:         if enter_short == 1 and not any([exit_short, enter_long]):
# REMOVED_UNUSED_CODE:             # Short
# REMOVED_UNUSED_CODE:             return "short"
# REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def run_protections(self, pair: str, current_time: datetime, side: LongShort):
# REMOVED_UNUSED_CODE:         if self.enable_protections:
# REMOVED_UNUSED_CODE:             self.protections.stop_per_pair(pair, current_time, side)
# REMOVED_UNUSED_CODE:             self.protections.global_stop(current_time, side)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def manage_open_orders(self, trade: LocalTrade, current_time: datetime, row: tuple) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check if any open order needs to be cancelled or replaced.
# REMOVED_UNUSED_CODE:         Returns True if the trade should be deleted.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         for order in [o for o in trade.orders if o.ft_is_open]:
# REMOVED_UNUSED_CODE:             oc = self.check_order_cancel(trade, order, current_time)
# REMOVED_UNUSED_CODE:             if oc:
# REMOVED_UNUSED_CODE:                 # delete trade due to order timeout
# REMOVED_UNUSED_CODE:                 return True
# REMOVED_UNUSED_CODE:             elif oc is None and self.check_order_replace(trade, order, current_time, row):
# REMOVED_UNUSED_CODE:                 # delete trade due to user request
# REMOVED_UNUSED_CODE:                 self.canceled_trade_entries += 1
# REMOVED_UNUSED_CODE:                 return True
# REMOVED_UNUSED_CODE:         # default maintain trade
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def cancel_open_orders(self, trade: LocalTrade, current_time: datetime):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Cancel all open orders for the given trade.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         for order in [o for o in trade.orders if o.ft_is_open]:
# REMOVED_UNUSED_CODE:             if order.side == trade.entry_side:
# REMOVED_UNUSED_CODE:                 self.canceled_entry_orders += 1
# REMOVED_UNUSED_CODE:             # elif order.side == trade.exit_side:
# REMOVED_UNUSED_CODE:             #     self.canceled_exit_orders += 1
# REMOVED_UNUSED_CODE:             # canceled orders are removed from the trade
# REMOVED_UNUSED_CODE:             del trade.orders[trade.orders.index(order)]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def handle_similar_order(
# REMOVED_UNUSED_CODE:         self, trade: LocalTrade, price: float, amount: float, side: str, current_time: datetime
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handle similar order for the given trade.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if trade.has_open_orders:
# REMOVED_UNUSED_CODE:             oo = trade.select_order(side, True)
# REMOVED_UNUSED_CODE:             if oo:
# REMOVED_UNUSED_CODE:                 if (price == oo.price) and (side == oo.side) and (amount == oo.amount):
# REMOVED_UNUSED_CODE:                     # logger.info(
# REMOVED_UNUSED_CODE:                     #     f"A similar open order was found for {trade.pair}. "
# REMOVED_UNUSED_CODE:                     #     f"Keeping existing {trade.exit_side} order. {price=},  {amount=}"
# REMOVED_UNUSED_CODE:                     # )
# REMOVED_UNUSED_CODE:                     return True
# REMOVED_UNUSED_CODE:             self.cancel_open_orders(trade, current_time)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def check_order_cancel(
# REMOVED_UNUSED_CODE:         self, trade: LocalTrade, order: Order, current_time: datetime
# REMOVED_UNUSED_CODE:     ) -> bool | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check if current analyzed order has to be canceled.
# REMOVED_UNUSED_CODE:         Returns True if the trade should be Deleted (initial order was canceled),
# REMOVED_UNUSED_CODE:                 False if it's Canceled
# REMOVED_UNUSED_CODE:                 None if the order is still active.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         timedout = self.strategy.ft_check_timed_out(
# REMOVED_UNUSED_CODE:             trade,  # type: ignore[arg-type]
# REMOVED_UNUSED_CODE:             order,
# REMOVED_UNUSED_CODE:             current_time,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         if timedout:
# REMOVED_UNUSED_CODE:             if order.side == trade.entry_side:
# REMOVED_UNUSED_CODE:                 self.timedout_entry_orders += 1
# REMOVED_UNUSED_CODE:                 if trade.nr_of_successful_entries == 0:
# REMOVED_UNUSED_CODE:                     # Remove trade due to entry timeout expiration.
# REMOVED_UNUSED_CODE:                     return True
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     # Close additional entry order
# REMOVED_UNUSED_CODE:                     del trade.orders[trade.orders.index(order)]
# REMOVED_UNUSED_CODE:                     return False
# REMOVED_UNUSED_CODE:             if order.side == trade.exit_side:
# REMOVED_UNUSED_CODE:                 self.timedout_exit_orders += 1
# REMOVED_UNUSED_CODE:                 # Close exit order and retry exiting on next signal.
# REMOVED_UNUSED_CODE:                 del trade.orders[trade.orders.index(order)]
# REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def check_order_replace(
# REMOVED_UNUSED_CODE:         self, trade: LocalTrade, order: Order, current_time, row: tuple
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check if current analyzed entry order has to be replaced and do so.
# REMOVED_UNUSED_CODE:         If user requested cancellation and there are no filled orders in the trade will
# REMOVED_UNUSED_CODE:         instruct caller to delete the trade.
# REMOVED_UNUSED_CODE:         Returns True if the trade should be deleted.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # only check on new candles for open entry orders
# REMOVED_UNUSED_CODE:         if order.side == trade.entry_side and current_time > order.order_date_utc:
# REMOVED_UNUSED_CODE:             requested_rate = strategy_safe_wrapper(
# REMOVED_UNUSED_CODE:                 self.strategy.adjust_entry_price, default_retval=order.ft_price
# REMOVED_UNUSED_CODE:             )(
# REMOVED_UNUSED_CODE:                 trade=trade,  # type: ignore[arg-type]
# REMOVED_UNUSED_CODE:                 order=order,
# REMOVED_UNUSED_CODE:                 pair=trade.pair,
# REMOVED_UNUSED_CODE:                 current_time=current_time,
# REMOVED_UNUSED_CODE:                 proposed_rate=row[OPEN_IDX],
# REMOVED_UNUSED_CODE:                 current_order_rate=order.ft_price,
# REMOVED_UNUSED_CODE:                 entry_tag=trade.enter_tag,
# REMOVED_UNUSED_CODE:                 side=trade.trade_direction,
# REMOVED_UNUSED_CODE:             )  # default value is current order price
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # cancel existing order whenever a new rate is requested (or None)
# REMOVED_UNUSED_CODE:             if requested_rate == order.ft_price:
# REMOVED_UNUSED_CODE:                 # assumption: there can't be multiple open entry orders at any given time
# REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 del trade.orders[trade.orders.index(order)]
# REMOVED_UNUSED_CODE:                 self.canceled_entry_orders += 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # place new order if result was not None
# REMOVED_UNUSED_CODE:             if requested_rate:
# REMOVED_UNUSED_CODE:                 self._enter_trade(
# REMOVED_UNUSED_CODE:                     pair=trade.pair,
# REMOVED_UNUSED_CODE:                     row=row,
# REMOVED_UNUSED_CODE:                     trade=trade,
# REMOVED_UNUSED_CODE:                     requested_rate=requested_rate,
# REMOVED_UNUSED_CODE:                     requested_stake=(order.safe_remaining * order.ft_price / trade.leverage),
# REMOVED_UNUSED_CODE:                     direction="short" if trade.is_short else "long",
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 # Delete trade if no successful entries happened (if placing the new order failed)
# REMOVED_UNUSED_CODE:                 if not trade.has_open_orders and trade.nr_of_successful_entries == 0:
# REMOVED_UNUSED_CODE:                     return True
# REMOVED_UNUSED_CODE:                 self.replaced_entry_orders += 1
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 # assumption: there can't be multiple open entry orders at any given time
# REMOVED_UNUSED_CODE:                 return trade.nr_of_successful_entries == 0
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def validate_row(
# REMOVED_UNUSED_CODE:         self, data: dict, pair: str, row_index: int, current_time: datetime
# REMOVED_UNUSED_CODE:     ) -> tuple | None:
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             # Row is treated as "current incomplete candle".
# REMOVED_UNUSED_CODE:             # entry / exit signals are shifted by 1 to compensate for this.
# REMOVED_UNUSED_CODE:             row = data[pair][row_index]
# REMOVED_UNUSED_CODE:         except IndexError:
# REMOVED_UNUSED_CODE:             # missing Data for one pair at the end.
# REMOVED_UNUSED_CODE:             # Warnings for this are shown during data loading
# REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Waits until the time-counter reaches the start of the data for this pair.
# REMOVED_UNUSED_CODE:         if row[DATE_IDX] > current_time:
# REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE:         return row
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _collate_rejected(self, pair, row):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Temporarily store rejected signal information for downstream use in backtesting_analysis
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # It could be fun to enable hyperopt mode to write
# REMOVED_UNUSED_CODE:         # a loss function to reduce rejected signals
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             self.config.get("export", "none") == "signals"
# REMOVED_UNUSED_CODE:             and self.dataprovider.runmode == RunMode.BACKTEST
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             if pair not in self.rejected_dict:
# REMOVED_UNUSED_CODE:                 self.rejected_dict[pair] = []
# REMOVED_UNUSED_CODE:             self.rejected_dict[pair].append([row[DATE_IDX], row[ENTER_TAG_IDX]])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def backtest_loop(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         row: tuple,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE:         trade_dir: LongShort | None,
# REMOVED_UNUSED_CODE:         can_enter: bool,
# REMOVED_UNUSED_CODE:     ) -> LongShort | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         NOTE: This method is used by Hyperopt at each iteration. Please keep it optimized.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         Backtesting processing for one candle/pair.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         exiting_dir: LongShort | None = None
# REMOVED_UNUSED_CODE:         if not self._position_stacking and len(LocalTrade.bt_trades_open_pp[pair]) > 0:
# REMOVED_UNUSED_CODE:             # position_stacking not supported for now.
# REMOVED_UNUSED_CODE:             exiting_dir = "short" if LocalTrade.bt_trades_open_pp[pair][0].is_short else "long"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for t in list(LocalTrade.bt_trades_open_pp[pair]):
# REMOVED_UNUSED_CODE:             # 1. Manage currently open orders of active trades
# REMOVED_UNUSED_CODE:             if self.manage_open_orders(t, current_time, row):
# REMOVED_UNUSED_CODE:                 # Remove trade (initial open order never filled)
# REMOVED_UNUSED_CODE:                 LocalTrade.remove_bt_trade(t)
# REMOVED_UNUSED_CODE:                 self.wallets.update()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # 2. Process entries.
# REMOVED_UNUSED_CODE:         # without positionstacking, we can only have one open trade per pair.
# REMOVED_UNUSED_CODE:         # max_open_trades must be respected
# REMOVED_UNUSED_CODE:         # don't open on the last row
# REMOVED_UNUSED_CODE:         # We only open trades on the main candle, not on detail candles
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             can_enter
# REMOVED_UNUSED_CODE:             and trade_dir is not None
# REMOVED_UNUSED_CODE:             and (self._position_stacking or len(LocalTrade.bt_trades_open_pp[pair]) == 0)
# REMOVED_UNUSED_CODE:             and not PairLocks.is_pair_locked(pair, row[DATE_IDX], trade_dir)
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             if self.trade_slot_available(LocalTrade.bt_open_open_trade_count):
# REMOVED_UNUSED_CODE:                 trade = self._enter_trade(pair, row, trade_dir)
# REMOVED_UNUSED_CODE:                 if trade:
# REMOVED_UNUSED_CODE:                     self.wallets.update()
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 self._collate_rejected(pair, row)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for trade in list(LocalTrade.bt_trades_open_pp[pair]):
# REMOVED_UNUSED_CODE:             # 3. Process entry orders.
# REMOVED_UNUSED_CODE:             order = trade.select_order(trade.entry_side, is_open=True)
# REMOVED_UNUSED_CODE:             if self._try_close_open_order(order, trade, current_time, row):
# REMOVED_UNUSED_CODE:                 self.wallets.update()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # 4. Create exit orders (if any)
# REMOVED_UNUSED_CODE:             if trade.has_open_position:
# REMOVED_UNUSED_CODE:                 self._check_trade_exit(trade, row, current_time)  # Place exit order if necessary
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # 5. Process exit orders.
# REMOVED_UNUSED_CODE:             order = trade.select_order(trade.exit_side, is_open=True)
# REMOVED_UNUSED_CODE:             if order:
# REMOVED_UNUSED_CODE:                 self._process_exit_order(order, trade, current_time, row, pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if exiting_dir and len(LocalTrade.bt_trades_open_pp[pair]) == 0:
# REMOVED_UNUSED_CODE:             return exiting_dir
# REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_detail_data(self, pair: str, row: tuple) -> list[tuple] | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Spread into detail data
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         current_detail_time: datetime = row[DATE_IDX].to_pydatetime()
# REMOVED_UNUSED_CODE:         exit_candle_end = current_detail_time + self.timeframe_td
# REMOVED_UNUSED_CODE:         detail_data = self.detail_data[pair]
# REMOVED_UNUSED_CODE:         detail_data = detail_data.loc[
# REMOVED_UNUSED_CODE:             (detail_data["date"] >= current_detail_time) & (detail_data["date"] < exit_candle_end)
# REMOVED_UNUSED_CODE:         ].copy()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if len(detail_data) == 0:
# REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE:         detail_data.loc[:, "enter_long"] = row[LONG_IDX]
# REMOVED_UNUSED_CODE:         detail_data.loc[:, "exit_long"] = row[ELONG_IDX]
# REMOVED_UNUSED_CODE:         detail_data.loc[:, "enter_short"] = row[SHORT_IDX]
# REMOVED_UNUSED_CODE:         detail_data.loc[:, "exit_short"] = row[ESHORT_IDX]
# REMOVED_UNUSED_CODE:         detail_data.loc[:, "enter_tag"] = row[ENTER_TAG_IDX]
# REMOVED_UNUSED_CODE:         detail_data.loc[:, "exit_tag"] = row[EXIT_TAG_IDX]
# REMOVED_UNUSED_CODE:         return detail_data[HEADERS].values.tolist()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _time_generator(self, start_date: datetime, end_date: datetime):
# REMOVED_UNUSED_CODE:         current_time = start_date + self.timeframe_td
# REMOVED_UNUSED_CODE:         while current_time <= end_date:
# REMOVED_UNUSED_CODE:             yield current_time
# REMOVED_UNUSED_CODE:             current_time += self.timeframe_td
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _time_generator_det(self, start_date: datetime, end_date: datetime):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Loop for each detail candle.
# REMOVED_UNUSED_CODE:         Yields only the start date if no detail timeframe is set.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not self.timeframe_detail_td:
# REMOVED_UNUSED_CODE:             yield start_date, True, False, 0
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         current_time = start_date
# REMOVED_UNUSED_CODE:         i = 0
# REMOVED_UNUSED_CODE:         while current_time <= end_date:
# REMOVED_UNUSED_CODE:             yield current_time, i == 0, True, i
# REMOVED_UNUSED_CODE:             i += 1
# REMOVED_UNUSED_CODE:             current_time += self.timeframe_detail_td
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _time_pair_generator_det(self, current_time: datetime, pairs: list[str]):
# REMOVED_UNUSED_CODE:         for current_time_det, is_first, has_detail, idx in self._time_generator_det(
# REMOVED_UNUSED_CODE:             current_time, current_time + self.timeframe_td
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             # Pairs that have open trades should be processed first
# REMOVED_UNUSED_CODE:             new_pairlist = list(dict.fromkeys([t.pair for t in LocalTrade.bt_trades_open] + pairs))
# REMOVED_UNUSED_CODE:             for pair in new_pairlist:
# REMOVED_UNUSED_CODE:                 yield current_time_det, is_first, has_detail, idx, pair
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def time_pair_generator(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         start_date: datetime,
# REMOVED_UNUSED_CODE:         end_date: datetime,
# REMOVED_UNUSED_CODE:         pairs: list[str],
# REMOVED_UNUSED_CODE:         data: dict[str, list[tuple]],
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Backtest time and pair generator
# REMOVED_UNUSED_CODE:         :returns: generator of (current_time, pair, row, is_last_row, trade_dir)
# REMOVED_UNUSED_CODE:             where is_last_row is a boolean indicating if this is the data end date.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         current_time = start_date + self.timeframe_td
# REMOVED_UNUSED_CODE:         self.progress.init_step(
# REMOVED_UNUSED_CODE:             BacktestState.BACKTEST, int((end_date - start_date) / self.timeframe_td)
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         # Indexes per pair, so some pairs are allowed to have a missing start.
# REMOVED_UNUSED_CODE:         indexes: dict = defaultdict(int)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for current_time in self._time_generator(start_date, end_date):
# REMOVED_UNUSED_CODE:             # Loop for each main candle.
# REMOVED_UNUSED_CODE:             self.check_abort()
# REMOVED_UNUSED_CODE:             # Reset open trade count for this candle
# REMOVED_UNUSED_CODE:             # Critical to avoid exceeding max_open_trades in backtesting
# REMOVED_UNUSED_CODE:             # when timeframe-detail is used and trades close within the opening candle.
# REMOVED_UNUSED_CODE:             strategy_safe_wrapper(self.strategy.bot_loop_start, supress_error=True)(
# REMOVED_UNUSED_CODE:                 current_time=current_time
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             pair_detail_cache: dict[str, list[tuple]] = {}
# REMOVED_UNUSED_CODE:             pair_tradedir_cache: dict[str, LongShort | None] = {}
# REMOVED_UNUSED_CODE:             pairs_with_open_trades = [t.pair for t in LocalTrade.bt_trades_open]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             for current_time_det, is_first, has_detail, idx, pair in self._time_pair_generator_det(
# REMOVED_UNUSED_CODE:                 current_time, pairs
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 # Loop for each detail candle (if necessary) and pair
# REMOVED_UNUSED_CODE:                 # Yields only the main date if no detail timeframe is set.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 # Pairs that have open trades should be processed first
# REMOVED_UNUSED_CODE:                 trade_dir: LongShort | None = None
# REMOVED_UNUSED_CODE:                 if is_first:
# REMOVED_UNUSED_CODE:                     # Main candle
# REMOVED_UNUSED_CODE:                     row_index = indexes[pair]
# REMOVED_UNUSED_CODE:                     row = self.validate_row(data, pair, row_index, current_time)
# REMOVED_UNUSED_CODE:                     if not row:
# REMOVED_UNUSED_CODE:                         continue
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                     row_index += 1
# REMOVED_UNUSED_CODE:                     indexes[pair] = row_index
# REMOVED_UNUSED_CODE:                     is_last_row = current_time == end_date
# REMOVED_UNUSED_CODE:                     self.dataprovider._set_dataframe_max_index(self.required_startup + row_index)
# REMOVED_UNUSED_CODE:                     trade_dir = self.check_for_trade_entry(row)
# REMOVED_UNUSED_CODE:                     pair_tradedir_cache[pair] = trade_dir
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     # Detail candle - from cache.
# REMOVED_UNUSED_CODE:                     detail_data = pair_detail_cache.get(pair)
# REMOVED_UNUSED_CODE:                     if detail_data is None or len(detail_data) <= idx:
# REMOVED_UNUSED_CODE:                         # logger.info(f"skipping {pair}, {current_time_det}, {trade_dir}")
# REMOVED_UNUSED_CODE:                         continue
# REMOVED_UNUSED_CODE:                     row = detail_data[idx]
# REMOVED_UNUSED_CODE:                     trade_dir = pair_tradedir_cache.get(pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                     if self.strategy.ignore_expired_candle(
# REMOVED_UNUSED_CODE:                         current_time - self.timeframe_td,  # last closed candle is 1 timeframe away.
# REMOVED_UNUSED_CODE:                         current_time_det,
# REMOVED_UNUSED_CODE:                         self.timeframe_secs,
# REMOVED_UNUSED_CODE:                         trade_dir is not None,
# REMOVED_UNUSED_CODE:                     ):
# REMOVED_UNUSED_CODE:                         # Ignore late entries eventually
# REMOVED_UNUSED_CODE:                         trade_dir = None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 self.dataprovider._set_dataframe_max_date(current_time_det)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 pair_has_open_trades = len(LocalTrade.bt_trades_open_pp[pair]) > 0
# REMOVED_UNUSED_CODE:                 if pair in pairs_with_open_trades and not pair_has_open_trades:
# REMOVED_UNUSED_CODE:                     # Pair has had open trades which closed in the current main candle.
# REMOVED_UNUSED_CODE:                     # Skip this pair for this timeframe
# REMOVED_UNUSED_CODE:                     continue
# REMOVED_UNUSED_CODE:                 if pair_has_open_trades and pair not in pairs_with_open_trades:
# REMOVED_UNUSED_CODE:                     # auto-lock for pairs that have open trades
# REMOVED_UNUSED_CODE:                     # Necessary for detail - to capture trades that open and close within
# REMOVED_UNUSED_CODE:                     # the same main candle
# REMOVED_UNUSED_CODE:                     pairs_with_open_trades.append(pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 if (
# REMOVED_UNUSED_CODE:                     is_first
# REMOVED_UNUSED_CODE:                     and (trade_dir is not None or pair_has_open_trades)
# REMOVED_UNUSED_CODE:                     and has_detail
# REMOVED_UNUSED_CODE:                     and pair not in pair_detail_cache
# REMOVED_UNUSED_CODE:                     and pair in self.detail_data
# REMOVED_UNUSED_CODE:                     and row
# REMOVED_UNUSED_CODE:                 ):
# REMOVED_UNUSED_CODE:                     # Spread candle into detail timeframe and cache that -
# REMOVED_UNUSED_CODE:                     # only once per main candle
# REMOVED_UNUSED_CODE:                     # and only if we can expect activity.
# REMOVED_UNUSED_CODE:                     pair_detail = self.get_detail_data(pair, row)
# REMOVED_UNUSED_CODE:                     if pair_detail is not None:
# REMOVED_UNUSED_CODE:                         pair_detail_cache[pair] = pair_detail
# REMOVED_UNUSED_CODE:                     row = pair_detail_cache[pair][idx]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 is_last_row = current_time_det == end_date
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 yield current_time_det, pair, row, is_last_row, trade_dir
# REMOVED_UNUSED_CODE:             self.progress.increment()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def backtest(self, processed: dict, start_date: datetime, end_date: datetime) -> dict[str, Any]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Implement backtesting functionality
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         NOTE: This method is used by Hyperopt at each iteration. Please keep it optimized.
# REMOVED_UNUSED_CODE:         Of course try to not have ugly code. By some accessor are sometime slower than functions.
# REMOVED_UNUSED_CODE:         Avoid extensive logging in this method and functions it calls.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param processed: a processed dictionary with format {pair, data}, which gets cleared to
# REMOVED_UNUSED_CODE:         optimize memory usage!
# REMOVED_UNUSED_CODE:         :param start_date: backtesting timerange start datetime
# REMOVED_UNUSED_CODE:         :param end_date: backtesting timerange end datetime
# REMOVED_UNUSED_CODE:         :return: DataFrame with trades (results of backtesting)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.prepare_backtest(self.enable_protections)
# REMOVED_UNUSED_CODE:         # Ensure wallets are up-to-date (important for --strategy-list)
# REMOVED_UNUSED_CODE:         self.wallets.update()
# REMOVED_UNUSED_CODE:         # Use dict of lists with data for performance
# REMOVED_UNUSED_CODE:         # (looping lists is a lot faster than pandas DataFrames)
# REMOVED_UNUSED_CODE:         data: dict = self._get_ohlcv_as_lists(processed)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Loop timerange and get candle for each pair at that point in time
# REMOVED_UNUSED_CODE:         for (
# REMOVED_UNUSED_CODE:             current_time,
# REMOVED_UNUSED_CODE:             pair,
# REMOVED_UNUSED_CODE:             row,
# REMOVED_UNUSED_CODE:             is_last_row,
# REMOVED_UNUSED_CODE:             trade_dir,
# REMOVED_UNUSED_CODE:         ) in self.time_pair_generator(start_date, end_date, list(data.keys()), data):
# REMOVED_UNUSED_CODE:             if not self._can_short or trade_dir is None:
# REMOVED_UNUSED_CODE:                 # No need to reverse position if shorting is disabled or there's no new signal
# REMOVED_UNUSED_CODE:                 self.backtest_loop(row, pair, current_time, trade_dir, not is_last_row)
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 # Conditionally call backtest_loop a 2nd time if shorting is enabled,
# REMOVED_UNUSED_CODE:                 # a position closed and a new signal in the other direction is available.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 for _ in (0, 1):
# REMOVED_UNUSED_CODE:                     a = self.backtest_loop(row, pair, current_time, trade_dir, not is_last_row)
# REMOVED_UNUSED_CODE:                     if not a or a == trade_dir:
# REMOVED_UNUSED_CODE:                         # the trade didn't close or position change is in the same direction
# REMOVED_UNUSED_CODE:                         break
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.handle_left_open(LocalTrade.bt_trades_open_pp, data=data)
# REMOVED_UNUSED_CODE:         self.wallets.update()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         results = trade_list_to_dataframe(LocalTrade.bt_trades)
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "results": results,
# REMOVED_UNUSED_CODE:             "config": self.strategy.config,
# REMOVED_UNUSED_CODE:             "locks": PairLocks.get_all_locks(),
# REMOVED_UNUSED_CODE:             "rejected_signals": self.rejected_trades,
# REMOVED_UNUSED_CODE:             "timedout_entry_orders": self.timedout_entry_orders,
# REMOVED_UNUSED_CODE:             "timedout_exit_orders": self.timedout_exit_orders,
# REMOVED_UNUSED_CODE:             "canceled_trade_entries": self.canceled_trade_entries,
# REMOVED_UNUSED_CODE:             "canceled_entry_orders": self.canceled_entry_orders,
# REMOVED_UNUSED_CODE:             "replaced_entry_orders": self.replaced_entry_orders,
# REMOVED_UNUSED_CODE:             "final_balance": self.wallets.get_total(self.strategy.config["stake_currency"]),
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def backtest_one_strategy(
# REMOVED_UNUSED_CODE:         self, strat: IStrategy, data: dict[str, DataFrame], timerange: TimeRange
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         self.progress.init_step(BacktestState.ANALYZE, 0)
# REMOVED_UNUSED_CODE:         strategy_name = strat.get_strategy_name()
# REMOVED_UNUSED_CODE:         logger.info(f"Running backtesting for Strategy {strategy_name}")
# REMOVED_UNUSED_CODE:         backtest_start_time = dt_now()
# REMOVED_UNUSED_CODE:         self._set_strategy(strat)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # need to reprocess data every time to populate signals
# REMOVED_UNUSED_CODE:         preprocessed = self.strategy.advise_all_indicators(data)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Trim startup period from analyzed dataframe
# REMOVED_UNUSED_CODE:         # This only used to determine if trimming would result in an empty dataframe
# REMOVED_UNUSED_CODE:         preprocessed_tmp = trim_dataframes(preprocessed, timerange, self.required_startup)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not preprocessed_tmp:
# REMOVED_UNUSED_CODE:             raise OperationalException("No data left after adjusting for startup candles.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Use preprocessed_tmp for date generation (the trimmed dataframe).
# REMOVED_UNUSED_CODE:         # Backtesting will re-trim the dataframes after entry/exit signal generation.
# REMOVED_UNUSED_CODE:         min_date, max_date = history.get_timerange(preprocessed_tmp)
# REMOVED_UNUSED_CODE:         logger.info(
# REMOVED_UNUSED_CODE:             f"Backtesting with data from {min_date.strftime(DATETIME_PRINT_FORMAT)} "
# REMOVED_UNUSED_CODE:             f"up to {max_date.strftime(DATETIME_PRINT_FORMAT)} "
# REMOVED_UNUSED_CODE:             f"({(max_date - min_date).days} days)."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         # Execute backtest and store results
# REMOVED_UNUSED_CODE:         results = self.backtest(
# REMOVED_UNUSED_CODE:             processed=preprocessed,
# REMOVED_UNUSED_CODE:             start_date=min_date,
# REMOVED_UNUSED_CODE:             end_date=max_date,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         backtest_end_time = dt_now()
# REMOVED_UNUSED_CODE:         results.update(
# REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE:                 "run_id": self.run_ids.get(strategy_name, ""),
# REMOVED_UNUSED_CODE:                 "backtest_start_time": int(backtest_start_time.timestamp()),
# REMOVED_UNUSED_CODE:                 "backtest_end_time": int(backtest_end_time.timestamp()),
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         self.all_results[strategy_name] = results
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             self.config.get("export", "none") == "signals"
# REMOVED_UNUSED_CODE:             and self.dataprovider.runmode == RunMode.BACKTEST
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             signals = generate_trade_signal_candles(preprocessed_tmp, results, "open_date")
# REMOVED_UNUSED_CODE:             rejected = generate_rejected_signals(preprocessed_tmp, self.rejected_dict)
# REMOVED_UNUSED_CODE:             exited = generate_trade_signal_candles(preprocessed_tmp, results, "close_date")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.analysis_results["signals"][strategy_name] = signals
# REMOVED_UNUSED_CODE:             self.analysis_results["rejected"][strategy_name] = rejected
# REMOVED_UNUSED_CODE:             self.analysis_results["exited"][strategy_name] = exited
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return min_date, max_date
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _get_min_cached_backtest_date(self):
# REMOVED_UNUSED_CODE:         min_backtest_date = None
# REMOVED_UNUSED_CODE:         backtest_cache_age = self.config.get("backtest_cache", constants.BACKTEST_CACHE_DEFAULT)
# REMOVED_UNUSED_CODE:         if self.timerange.stopts == 0 or self.timerange.stopdt > dt_now():
# REMOVED_UNUSED_CODE:             logger.warning("Backtest result caching disabled due to use of open-ended timerange.")
# REMOVED_UNUSED_CODE:         elif backtest_cache_age == "day":
# REMOVED_UNUSED_CODE:             min_backtest_date = dt_now() - timedelta(days=1)
# REMOVED_UNUSED_CODE:         elif backtest_cache_age == "week":
# REMOVED_UNUSED_CODE:             min_backtest_date = dt_now() - timedelta(weeks=1)
# REMOVED_UNUSED_CODE:         elif backtest_cache_age == "month":
# REMOVED_UNUSED_CODE:             min_backtest_date = dt_now() - timedelta(weeks=4)
# REMOVED_UNUSED_CODE:         return min_backtest_date
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def load_prior_backtest(self):
# REMOVED_UNUSED_CODE:         self.run_ids = {
# REMOVED_UNUSED_CODE:             strategy.get_strategy_name(): get_strategy_run_id(strategy)
# REMOVED_UNUSED_CODE:             for strategy in self.strategylist
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Load previous result that will be updated incrementally.
# REMOVED_UNUSED_CODE:         # This can be circumvented in certain instances in combination with downloading more data
# REMOVED_UNUSED_CODE:         min_backtest_date = self._get_min_cached_backtest_date()
# REMOVED_UNUSED_CODE:         if min_backtest_date is not None:
# REMOVED_UNUSED_CODE:             self.results = find_existing_backtest_stats(
# REMOVED_UNUSED_CODE:                 self.config["user_data_dir"] / "backtest_results", self.run_ids, min_backtest_date
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def start(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Run backtesting end-to-end
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         data: dict[str, DataFrame] = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         data, timerange = self.load_bt_data()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.load_bt_data_detail()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info("Dataload complete. Calculating indicators")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.load_prior_backtest()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for strat in self.strategylist:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self.results and strat.get_strategy_name() in self.results["strategy"]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # When previous result hash matches - reuse that result and skip backtesting.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.info(f"Reusing result of previous backtest for {strat.get_strategy_name()}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             min_date, max_date = self.backtest_one_strategy(strat, data, timerange)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Update old results with new ones.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if len(self.all_results) > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             results = generate_backtest_stats(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 data, self.all_results, min_date=min_date, max_date=max_date
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self.results:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.results["metadata"].update(results["metadata"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.results["strategy"].update(results["strategy"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.results["strategy_comparison"].extend(results["strategy_comparison"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.results = results
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dt_appendix = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self.config.get("export", "none") in ("trades", "signals"):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 combined_res = combined_dataframes_with_rel_mean(data, min_date, max_date)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 store_backtest_results(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     self.config,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     self.results,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     dt_appendix,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     market_change_data=combined_res,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     analysis_results=self.analysis_results,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Results may be mixed up now. Sort them so they follow --strategy-list order.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if "strategy_list" in self.config and len(self.results) > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.results["strategy_comparison"] = sorted(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.results["strategy_comparison"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 key=lambda c: self.config["strategy_list"].index(c["key"]),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.results["strategy"] = dict(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 sorted(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     self.results["strategy"].items(),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     key=lambda kv: self.config["strategy_list"].index(kv[0]),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if len(self.strategylist) > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Show backtest results
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             show_backtest_results(self.config, self.results)
