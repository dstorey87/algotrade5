"""
IStrategy interface
This module defines the interface to apply for strategies
"""

import logging
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from abc import ABC, abstractmethod
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import datetime, timedelta, timezone
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from math import isinf, isnan

# REMOVED_UNUSED_CODE: from pandas import DataFrame

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.constants import CUSTOM_TAG_MAX_LENGTH, Config, IntOrInf, ListPairsWithTimeframes
# REMOVED_UNUSED_CODE: from freqtrade.data.converter import populate_dataframe_with_trades
# REMOVED_UNUSED_CODE: from freqtrade.data.dataprovider import DataProvider
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.enums import (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     CandleType,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ExitCheckTuple,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ExitType,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     MarketDirection,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     RunMode,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     SignalDirection,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     SignalTagType,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     SignalType,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     TradingMode,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException, StrategyError
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exchange import timeframe_to_minutes, timeframe_to_next_date, timeframe_to_seconds
# REMOVED_UNUSED_CODE: from freqtrade.misc import remove_entry_exit_signals
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.persistence import Order, PairLocks, Trade
# REMOVED_UNUSED_CODE: from freqtrade.strategy.hyper import HyperStrategyMixin
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.strategy.informative_decorator import (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     InformativeData,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     PopulateIndicators,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     _create_and_merge_informative_pair,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     _format_pair_name,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: )
# REMOVED_UNUSED_CODE: from freqtrade.strategy.strategy_wrapper import strategy_safe_wrapper
# REMOVED_UNUSED_CODE: from freqtrade.util import dt_now
# REMOVED_UNUSED_CODE: from freqtrade.wallets import Wallets


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class IStrategy(ABC, HyperStrategyMixin):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Interface for freqtrade strategies
# REMOVED_UNUSED_CODE:     Defines the mandatory structure must follow any custom strategies
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Attributes you can use:
# REMOVED_UNUSED_CODE:         minimal_roi -> Dict: Minimal ROI designed for the strategy
# REMOVED_UNUSED_CODE:         stoploss -> float: optimal stoploss designed for the strategy
# REMOVED_UNUSED_CODE:         timeframe -> str: value of the timeframe to use with the strategy
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Strategy interface version
# REMOVED_UNUSED_CODE:     # Default to version 2
# REMOVED_UNUSED_CODE:     # Version 1 is the initial interface without metadata dict - deprecated and no longer supported.
# REMOVED_UNUSED_CODE:     # Version 2 populate_* include metadata dict
# REMOVED_UNUSED_CODE:     # Version 3 - First version with short and leverage support
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     INTERFACE_VERSION: int = 3
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _ft_params_from_file: dict
# REMOVED_UNUSED_CODE:     # associated minimal roi
# REMOVED_UNUSED_CODE:     minimal_roi: dict = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # associated stoploss
# REMOVED_UNUSED_CODE:     stoploss: float
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # max open trades for the strategy
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     max_open_trades: IntOrInf
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # trailing stoploss
# REMOVED_UNUSED_CODE:     trailing_stop: bool = False
# REMOVED_UNUSED_CODE:     trailing_stop_positive: float | None = None
# REMOVED_UNUSED_CODE:     trailing_stop_positive_offset: float = 0.0
# REMOVED_UNUSED_CODE:     trailing_only_offset_is_reached = False
# REMOVED_UNUSED_CODE:     use_custom_stoploss: bool = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Can this strategy go short?
# REMOVED_UNUSED_CODE:     can_short: bool = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # associated timeframe
# REMOVED_UNUSED_CODE:     timeframe: str
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Optional order types
# REMOVED_UNUSED_CODE:     order_types: dict = {
# REMOVED_UNUSED_CODE:         "entry": "limit",
# REMOVED_UNUSED_CODE:         "exit": "limit",
# REMOVED_UNUSED_CODE:         "stoploss": "limit",
# REMOVED_UNUSED_CODE:         "stoploss_on_exchange": False,
# REMOVED_UNUSED_CODE:         "stoploss_on_exchange_interval": 60,
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Optional time in force
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     order_time_in_force: dict = {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         "entry": "GTC",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         "exit": "GTC",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # run "populate_indicators" only for new candle
# REMOVED_UNUSED_CODE:     process_only_new_candles: bool = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     use_exit_signal: bool
# REMOVED_UNUSED_CODE:     exit_profit_only: bool
# REMOVED_UNUSED_CODE:     exit_profit_offset: float
# REMOVED_UNUSED_CODE:     ignore_roi_if_entry_signal: bool
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Position adjustment is disabled by default
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     position_adjustment_enable: bool = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     max_entry_position_adjustment: int = -1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Number of seconds after which the candle will no longer result in a buy on expired candles
# REMOVED_UNUSED_CODE:     ignore_buying_expired_candle_after: int = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Disable checking the dataframe (converts the error into a warning message)
# REMOVED_UNUSED_CODE:     disable_dataframe_checks: bool = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Count of candles the strategy requires before producing valid signals
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     startup_candle_count: int = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Protections
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     protections: list = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Class level variables (intentional) containing
# REMOVED_UNUSED_CODE:     # the dataprovider (dp) (access to other candles, historic data, ...)
# REMOVED_UNUSED_CODE:     # and wallets - access to the current balance.
# REMOVED_UNUSED_CODE:     dp: DataProvider
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     wallets: Wallets | None = None
# REMOVED_UNUSED_CODE:     # Filled from configuration
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stake_currency: str
# REMOVED_UNUSED_CODE:     # container variable for strategy source code
# REMOVED_UNUSED_CODE:     __source__: str = ""
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Definition of plot_config. See plotting documentation for more details.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     plot_config: dict = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # A self set parameter that represents the market direction. filled from configuration
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     market_direction: MarketDirection = MarketDirection.NONE
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Global cache dictionary
# REMOVED_UNUSED_CODE:     _cached_grouped_trades_per_pair: dict[str, DataFrame] = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         self.config = config
# REMOVED_UNUSED_CODE:         # Dict to determine if analysis is necessary
# REMOVED_UNUSED_CODE:         self._last_candle_seen_per_pair: dict[str, datetime] = {}
# REMOVED_UNUSED_CODE:         super().__init__(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Gather informative pairs from @informative-decorated methods.
# REMOVED_UNUSED_CODE:         self._ft_informative: list[tuple[InformativeData, PopulateIndicators]] = []
# REMOVED_UNUSED_CODE:         for attr_name in dir(self.__class__):
# REMOVED_UNUSED_CODE:             cls_method = getattr(self.__class__, attr_name)
# REMOVED_UNUSED_CODE:             if not callable(cls_method):
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE:             informative_data_list = getattr(cls_method, "_ft_informative", None)
# REMOVED_UNUSED_CODE:             if not isinstance(informative_data_list, list):
# REMOVED_UNUSED_CODE:                 # Type check is required because mocker would return a mock object that evaluates to
# REMOVED_UNUSED_CODE:                 # True, confusing this code.
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE:             strategy_timeframe_minutes = timeframe_to_minutes(self.timeframe)
# REMOVED_UNUSED_CODE:             for informative_data in informative_data_list:
# REMOVED_UNUSED_CODE:                 if timeframe_to_minutes(informative_data.timeframe) < strategy_timeframe_minutes:
# REMOVED_UNUSED_CODE:                     raise OperationalException(
# REMOVED_UNUSED_CODE:                         "Informative timeframe must be equal or higher than strategy timeframe!"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 if not informative_data.candle_type:
# REMOVED_UNUSED_CODE:                     informative_data.candle_type = config["candle_type_def"]
# REMOVED_UNUSED_CODE:                 self._ft_informative.append((informative_data, cls_method))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def load_freqAI_model(self) -> None:
# REMOVED_UNUSED_CODE:         if self.config.get("freqai", {}).get("enabled", False):
# REMOVED_UNUSED_CODE:             # Import here to avoid importing this if freqAI is disabled
# REMOVED_UNUSED_CODE:             from freqtrade.freqai.utils import download_all_data_for_training
# REMOVED_UNUSED_CODE:             from freqtrade.resolvers.freqaimodel_resolver import FreqaiModelResolver
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.freqai = FreqaiModelResolver.load_freqaimodel(self.config)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.freqai_info = self.config["freqai"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # download the desired data in dry/live
# REMOVED_UNUSED_CODE:             if self.config.get("runmode") in (RunMode.DRY_RUN, RunMode.LIVE):
# REMOVED_UNUSED_CODE:                 logger.info(
# REMOVED_UNUSED_CODE:                     "Downloading all training data for all pairs in whitelist and "
# REMOVED_UNUSED_CODE:                     "corr_pairlist, this may take a while if the data is not "
# REMOVED_UNUSED_CODE:                     "already on disk."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 download_all_data_for_training(self.dp, self.config)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # Gracious failures if freqAI is disabled but "start" is called.
# REMOVED_UNUSED_CODE:             class DummyClass:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 def start(self, *args, **kwargs):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     raise OperationalException(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         "freqAI is not enabled. "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         "Please enable it in your config to use this strategy."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 def shutdown(self, *args, **kwargs):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     pass
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.freqai = DummyClass()  # type: ignore
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def ft_bot_start(self, **kwargs) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Strategy init - runs after dataprovider has been added.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Must call bot_start()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.load_freqAI_model()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         strategy_safe_wrapper(self.bot_start)()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.ft_load_hyper_params(self.config.get("runmode") == RunMode.HYPEROPT)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def ft_bot_cleanup(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Clean up FreqAI and child threads
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.freqai.shutdown()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Populate indicators that will be used in the Buy, Sell, Short, Exit_short strategy
# REMOVED_UNUSED_CODE:         :param dataframe: DataFrame with data from the exchange
# REMOVED_UNUSED_CODE:         :param metadata: Additional information, like the currently traded pair
# REMOVED_UNUSED_CODE:         :return: a Dataframe with all mandatory indicators for the strategies
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         DEPRECATED - please migrate to populate_entry_trend
# REMOVED_UNUSED_CODE:         :param dataframe: DataFrame
# REMOVED_UNUSED_CODE:         :param metadata: Additional information, like the currently traded pair
# REMOVED_UNUSED_CODE:         :return: DataFrame with buy column
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Based on TA indicators, populates the entry signal for the given dataframe
# REMOVED_UNUSED_CODE:         :param dataframe: DataFrame
# REMOVED_UNUSED_CODE:         :param metadata: Additional information, like the currently traded pair
# REMOVED_UNUSED_CODE:         :return: DataFrame with entry columns populated
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return self.populate_buy_trend(dataframe, metadata)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         DEPRECATED - please migrate to populate_exit_trend
# REMOVED_UNUSED_CODE:         Based on TA indicators, populates the sell signal for the given dataframe
# REMOVED_UNUSED_CODE:         :param dataframe: DataFrame
# REMOVED_UNUSED_CODE:         :param metadata: Additional information, like the currently traded pair
# REMOVED_UNUSED_CODE:         :return: DataFrame with sell column
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Based on TA indicators, populates the exit signal for the given dataframe
# REMOVED_UNUSED_CODE:         :param dataframe: DataFrame
# REMOVED_UNUSED_CODE:         :param metadata: Additional information, like the currently traded pair
# REMOVED_UNUSED_CODE:         :return: DataFrame with exit columns populated
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return self.populate_sell_trend(dataframe, metadata)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def bot_start(self, **kwargs) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Called only once after bot instantiation.
# REMOVED_UNUSED_CODE:         :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         pass
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def bot_loop_start(self, current_time: datetime, **kwargs) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Called at the start of the bot iteration (one loop).
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Might be used to perform pair-independent tasks
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         (e.g. gather some remote resource for comparison)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param current_time: datetime object, containing the current datetime
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pass
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def check_buy_timeout(
# REMOVED_UNUSED_CODE:         self, pair: str, trade: Trade, order: Order, current_time: datetime, **kwargs
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         DEPRECATED: Please use `check_entry_timeout` instead.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def check_entry_timeout(
# REMOVED_UNUSED_CODE:         self, pair: str, trade: Trade, order: Order, current_time: datetime, **kwargs
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check entry timeout function callback.
# REMOVED_UNUSED_CODE:         This method can be used to override the entry-timeout.
# REMOVED_UNUSED_CODE:         It is called whenever a limit entry order has been created,
# REMOVED_UNUSED_CODE:         and is not yet fully filled.
# REMOVED_UNUSED_CODE:         Configuration options in `unfilledtimeout` will be verified before this,
# REMOVED_UNUSED_CODE:         so ensure to set these timeouts high enough.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         When not implemented by a strategy, this simply returns False.
# REMOVED_UNUSED_CODE:         :param pair: Pair the trade is for
# REMOVED_UNUSED_CODE:         :param trade: Trade object.
# REMOVED_UNUSED_CODE:         :param order: Order object.
# REMOVED_UNUSED_CODE:         :param current_time: datetime object, containing the current datetime
# REMOVED_UNUSED_CODE:         :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
# REMOVED_UNUSED_CODE:         :return bool: When True is returned, then the entry order is cancelled.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return self.check_buy_timeout(
# REMOVED_UNUSED_CODE:             pair=pair, trade=trade, order=order, current_time=current_time
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def check_sell_timeout(
# REMOVED_UNUSED_CODE:         self, pair: str, trade: Trade, order: Order, current_time: datetime, **kwargs
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         DEPRECATED: Please use `check_exit_timeout` instead.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def check_exit_timeout(
# REMOVED_UNUSED_CODE:         self, pair: str, trade: Trade, order: Order, current_time: datetime, **kwargs
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check exit timeout function callback.
# REMOVED_UNUSED_CODE:         This method can be used to override the exit-timeout.
# REMOVED_UNUSED_CODE:         It is called whenever a limit exit order has been created,
# REMOVED_UNUSED_CODE:         and is not yet fully filled.
# REMOVED_UNUSED_CODE:         Configuration options in `unfilledtimeout` will be verified before this,
# REMOVED_UNUSED_CODE:         so ensure to set these timeouts high enough.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         When not implemented by a strategy, this simply returns False.
# REMOVED_UNUSED_CODE:         :param pair: Pair the trade is for
# REMOVED_UNUSED_CODE:         :param trade: Trade object.
# REMOVED_UNUSED_CODE:         :param order: Order object
# REMOVED_UNUSED_CODE:         :param current_time: datetime object, containing the current datetime
# REMOVED_UNUSED_CODE:         :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
# REMOVED_UNUSED_CODE:         :return bool: When True is returned, then the exit-order is cancelled.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return self.check_sell_timeout(
# REMOVED_UNUSED_CODE:             pair=pair, trade=trade, order=order, current_time=current_time
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def confirm_trade_entry(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         order_type: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         amount: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         time_in_force: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         entry_tag: str | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         side: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Called right before placing a entry order.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Timing for this function is critical, so avoid doing heavy computations or
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         network requests in this method.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         For full documentation please go to https://www.freqtrade.io/en/latest/strategy-advanced/
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         When not implemented by a strategy, returns True (always confirming).
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair that's about to be bought/shorted.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param order_type: Order type (as configured in order_types). usually limit or market.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param amount: Amount in target (base) currency that's going to be traded.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param rate: Rate that's going to be used when using limit orders
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                      or current rate for market orders.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param time_in_force: Time in force. Defaults to GTC (Good-til-cancelled).
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param current_time: datetime object, containing the current datetime
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param side: 'long' or 'short' - indicating the direction of the proposed trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return bool: When True is returned, then the buy-order is placed on the exchange.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             False aborts the process
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def confirm_trade_exit(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         order_type: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         amount: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         time_in_force: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         exit_reason: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Called right before placing a regular exit order.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Timing for this function is critical, so avoid doing heavy computations or
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         network requests in this method.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         For full documentation please go to https://www.freqtrade.io/en/latest/strategy-advanced/
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         When not implemented by a strategy, returns True (always confirming).
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair for trade that's about to be exited.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param trade: trade object.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param order_type: Order type (as configured in order_types). usually limit or market.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param amount: Amount in base currency.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param rate: Rate that's going to be used when using limit orders
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                      or current rate for market orders.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param time_in_force: Time in force. Defaults to GTC (Good-til-cancelled).
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param exit_reason: Exit reason.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             Can be any of ['roi', 'stop_loss', 'stoploss_on_exchange', 'trailing_stop_loss',
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                            'exit_signal', 'force_exit', 'emergency_exit']
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param current_time: datetime object, containing the current datetime
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return bool: When True, then the exit-order is placed on the exchange.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             False aborts the process
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def order_filled(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pair: str, trade: Trade, order: Order, current_time: datetime, **kwargs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Called right after an order fills.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Will be called for all order types (entry, exit, stoploss, position adjustment).
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair for trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param trade: trade object.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param order: Order object.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param current_time: datetime object, containing the current datetime
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pass
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def custom_stoploss(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE:         current_rate: float,
# REMOVED_UNUSED_CODE:         current_profit: float,
# REMOVED_UNUSED_CODE:         after_fill: bool,
# REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ) -> float | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Custom stoploss logic, returning the new distance relative to current_rate (as ratio).
# REMOVED_UNUSED_CODE:         e.g. returning -0.05 would create a stoploss 5% below current_rate.
# REMOVED_UNUSED_CODE:         The custom stoploss can never be below self.stoploss, which serves as a hard maximum loss.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         For full documentation please go to https://www.freqtrade.io/en/latest/strategy-advanced/
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         When not implemented by a strategy, returns the initial stoploss value.
# REMOVED_UNUSED_CODE:         Only called when use_custom_stoploss is set to True.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param pair: Pair that's currently analyzed
# REMOVED_UNUSED_CODE:         :param trade: trade object.
# REMOVED_UNUSED_CODE:         :param current_time: datetime object, containing the current datetime
# REMOVED_UNUSED_CODE:         :param current_rate: Rate, calculated based on pricing settings in exit_pricing.
# REMOVED_UNUSED_CODE:         :param current_profit: Current profit (as ratio), calculated based on current_rate.
# REMOVED_UNUSED_CODE:         :param after_fill: True if the stoploss is called after the order was filled.
# REMOVED_UNUSED_CODE:         :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
# REMOVED_UNUSED_CODE:         :return float: New stoploss value, relative to the current_rate
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return self.stoploss
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def custom_entry_price(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade: Trade | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         proposed_rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         entry_tag: str | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         side: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Custom entry price logic, returning the new entry price.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         For full documentation please go to https://www.freqtrade.io/en/latest/strategy-advanced/
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         When not implemented by a strategy, returns None, orderbook is used to set entry price
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair that's currently analyzed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param trade: trade object (None for initial entries).
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param current_time: datetime object, containing the current datetime
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param proposed_rate: Rate, calculated based on pricing settings in exit_pricing.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param side: 'long' or 'short' - indicating the direction of the proposed trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return float: New entry price value if provided
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return proposed_rate
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def custom_exit_price(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         proposed_rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_profit: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         exit_tag: str | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Custom exit price logic, returning the new exit price.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         For full documentation please go to https://www.freqtrade.io/en/latest/strategy-advanced/
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         When not implemented by a strategy, returns None, orderbook is used to set exit price
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair that's currently analyzed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param trade: trade object.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param current_time: datetime object, containing the current datetime
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param proposed_rate: Rate, calculated based on pricing settings in exit_pricing.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param current_profit: Current profit (as ratio), calculated based on current_rate.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param exit_tag: Exit reason.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return float: New exit price value if provided
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return proposed_rate
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def custom_sell(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE:         current_rate: float,
# REMOVED_UNUSED_CODE:         current_profit: float,
# REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ) -> str | bool | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         DEPRECATED - please use custom_exit instead.
# REMOVED_UNUSED_CODE:         Custom exit signal logic indicating that specified position should be sold. Returning a
# REMOVED_UNUSED_CODE:         string or True from this method is equal to setting exit signal on a candle at specified
# REMOVED_UNUSED_CODE:         time. This method is not called when exit signal is set.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         This method should be overridden to create exit signals that depend on trade parameters. For
# REMOVED_UNUSED_CODE:         example you could implement an exit relative to the candle when the trade was opened,
# REMOVED_UNUSED_CODE:         or a custom 1:2 risk-reward ROI.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         Custom exit reason max length is 64. Exceeding characters will be removed.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param pair: Pair that's currently analyzed
# REMOVED_UNUSED_CODE:         :param trade: trade object.
# REMOVED_UNUSED_CODE:         :param current_time: datetime object, containing the current datetime
# REMOVED_UNUSED_CODE:         :param current_rate: Rate, calculated based on pricing settings in exit_pricing.
# REMOVED_UNUSED_CODE:         :param current_profit: Current profit (as ratio), calculated based on current_rate.
# REMOVED_UNUSED_CODE:         :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
# REMOVED_UNUSED_CODE:         :return: To execute exit, return a string with custom exit reason or True. Otherwise return
# REMOVED_UNUSED_CODE:         None or False.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def custom_exit(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE:         current_rate: float,
# REMOVED_UNUSED_CODE:         current_profit: float,
# REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ) -> str | bool | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Custom exit signal logic indicating that specified position should be sold. Returning a
# REMOVED_UNUSED_CODE:         string or True from this method is equal to setting exit signal on a candle at specified
# REMOVED_UNUSED_CODE:         time. This method is not called when exit signal is set.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         This method should be overridden to create exit signals that depend on trade parameters. For
# REMOVED_UNUSED_CODE:         example you could implement an exit relative to the candle when the trade was opened,
# REMOVED_UNUSED_CODE:         or a custom 1:2 risk-reward ROI.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         Custom exit reason max length is 64. Exceeding characters will be removed.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param pair: Pair that's currently analyzed
# REMOVED_UNUSED_CODE:         :param trade: trade object.
# REMOVED_UNUSED_CODE:         :param current_time: datetime object, containing the current datetime
# REMOVED_UNUSED_CODE:         :param current_rate: Rate, calculated based on pricing settings in exit_pricing.
# REMOVED_UNUSED_CODE:         :param current_profit: Current profit (as ratio), calculated based on current_rate.
# REMOVED_UNUSED_CODE:         :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
# REMOVED_UNUSED_CODE:         :return: To execute exit, return a string with custom exit reason or True. Otherwise return
# REMOVED_UNUSED_CODE:         None or False.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return self.custom_sell(pair, trade, current_time, current_rate, current_profit, **kwargs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def custom_stake_amount(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         proposed_stake: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         min_stake: float | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         max_stake: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         leverage: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         entry_tag: str | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         side: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Customize stake size for each new trade.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair that's currently analyzed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param current_time: datetime object, containing the current datetime
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param current_rate: Rate, calculated based on pricing settings in exit_pricing.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param proposed_stake: A stake amount proposed by the bot.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param min_stake: Minimal stake size allowed by exchange.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param max_stake: Balance available for trading.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param leverage: Leverage selected for this trade.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param side: 'long' or 'short' - indicating the direction of the proposed trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: A stake size, which is between min_stake and max_stake.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return proposed_stake
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def adjust_trade_position(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE:         current_rate: float,
# REMOVED_UNUSED_CODE:         current_profit: float,
# REMOVED_UNUSED_CODE:         min_stake: float | None,
# REMOVED_UNUSED_CODE:         max_stake: float,
# REMOVED_UNUSED_CODE:         current_entry_rate: float,
# REMOVED_UNUSED_CODE:         current_exit_rate: float,
# REMOVED_UNUSED_CODE:         current_entry_profit: float,
# REMOVED_UNUSED_CODE:         current_exit_profit: float,
# REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ) -> float | None | tuple[float | None, str | None]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Custom trade adjustment logic, returning the stake amount that a trade should be
# REMOVED_UNUSED_CODE:         increased or decreased.
# REMOVED_UNUSED_CODE:         This means extra entry or exit orders with additional fees.
# REMOVED_UNUSED_CODE:         Only called when `position_adjustment_enable` is set to True.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         For full documentation please go to https://www.freqtrade.io/en/latest/strategy-advanced/
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         When not implemented by a strategy, returns None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param trade: trade object.
# REMOVED_UNUSED_CODE:         :param current_time: datetime object, containing the current datetime
# REMOVED_UNUSED_CODE:         :param current_rate: Current entry rate (same as current_entry_profit)
# REMOVED_UNUSED_CODE:         :param current_profit: Current profit (as ratio), calculated based on current_rate
# REMOVED_UNUSED_CODE:                                (same as current_entry_profit).
# REMOVED_UNUSED_CODE:         :param min_stake: Minimal stake size allowed by exchange (for both entries and exits)
# REMOVED_UNUSED_CODE:         :param max_stake: Maximum stake allowed (either through balance, or by exchange limits).
# REMOVED_UNUSED_CODE:         :param current_entry_rate: Current rate using entry pricing.
# REMOVED_UNUSED_CODE:         :param current_exit_rate: Current rate using exit pricing.
# REMOVED_UNUSED_CODE:         :param current_entry_profit: Current profit using entry pricing.
# REMOVED_UNUSED_CODE:         :param current_exit_profit: Current profit using exit pricing.
# REMOVED_UNUSED_CODE:         :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
# REMOVED_UNUSED_CODE:         :return float: Stake amount to adjust your trade,
# REMOVED_UNUSED_CODE:                        Positive values to increase position, Negative values to decrease position.
# REMOVED_UNUSED_CODE:                        Return None for no action.
# REMOVED_UNUSED_CODE:                        Optionally, return a tuple with a 2nd element with an order reason
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def adjust_entry_price(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         order: Order | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         proposed_rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_order_rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         entry_tag: str | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         side: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Entry price re-adjustment logic, returning the user desired limit price.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This only executes when a order was already placed, still open (unfilled fully or partially)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         and not timed out on subsequent candles after entry trigger.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         For full documentation please go to https://www.freqtrade.io/en/latest/strategy-callbacks/
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         When not implemented by a strategy, returns current_order_rate as default.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         If current_order_rate is returned then the existing order is maintained.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         If None is returned then order gets canceled but not replaced by a new one.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair that's currently analyzed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param trade: Trade object.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param order: Order object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param current_time: datetime object, containing the current datetime
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param proposed_rate: Rate, calculated based on pricing settings in entry_pricing.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param current_order_rate: Rate of the existing order in place.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param side: 'long' or 'short' - indicating the direction of the proposed trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return float: New entry price value if provided
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return current_order_rate
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def leverage(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         proposed_leverage: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         max_leverage: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         entry_tag: str | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         side: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Customize leverage for each new trade. This method is only called in futures mode.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair that's currently analyzed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param current_time: datetime object, containing the current datetime
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param current_rate: Rate, calculated based on pricing settings in exit_pricing.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param proposed_leverage: A leverage proposed by the bot.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param max_leverage: Max leverage allowed on this pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param side: 'long' or 'short' - indicating the direction of the proposed trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: A leverage amount, which is between 1.0 and max_leverage.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return 1.0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def informative_pairs(self) -> ListPairsWithTimeframes:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Define additional, informative pair/interval combinations to be cached from the exchange.
# REMOVED_UNUSED_CODE:         These pair/interval combinations are non-tradable, unless they are part
# REMOVED_UNUSED_CODE:         of the whitelist as well.
# REMOVED_UNUSED_CODE:         For more information, please consult the documentation
# REMOVED_UNUSED_CODE:         :return: List of tuples in the format (pair, interval)
# REMOVED_UNUSED_CODE:             Sample: return [("ETH/USDT", "5m"),
# REMOVED_UNUSED_CODE:                             ("BTC/USDT", "15m"),
# REMOVED_UNUSED_CODE:                             ]
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def version(self) -> str | None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Returns version of the strategy.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_any_indicators(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         df: DataFrame,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         tf: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         informative: DataFrame | None = None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         set_generalized_indicators: bool = False,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         DEPRECATED - USE FEATURE ENGINEERING FUNCTIONS INSTEAD
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Function designed to automatically generate, name and merge features
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         from user indicated timeframes in the configuration file. User can add
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         additional features here, but must follow the naming convention.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This method is *only* used in FreqaiDataKitchen class and therefore
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         it is only called if FreqAI is active.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: pair to be used as informative
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param df: strategy dataframe which will receive merges from informatives
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param tf: timeframe of the dataframe which will modify the feature names
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param informative: the dataframe associated with the informative pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return df
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def feature_engineering_expand_all(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, dataframe: DataFrame, period: int, metadata: dict, **kwargs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         *Only functional with FreqAI enabled strategies*
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This function will automatically expand the defined features on the config defined
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         `indicator_periods_candles`, `include_timeframes`, `include_shifted_candles`, and
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         `include_corr_pairs`. In other words, a single feature defined in this function
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         will automatically expand to a total of
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         `indicator_periods_candles` * `include_timeframes` * `include_shifted_candles` *
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         `include_corr_pairs` numbers of features added to the model.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         All features must be prepended with `%` to be recognized by FreqAI internals.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         More details on how these config defined parameters accelerate feature engineering
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         in the documentation at:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         https://www.freqtrade.io/en/latest/freqai-parameter-table/#feature-parameters
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         https://www.freqtrade.io/en/latest/freqai-feature-engineering/#defining-the-features
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: strategy dataframe which will receive the features
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param period: period of the indicator - usage example:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metadata: metadata of current pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-ema-period"] = ta.EMA(dataframe, timeperiod=period)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def feature_engineering_expand_basic(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, dataframe: DataFrame, metadata: dict, **kwargs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         *Only functional with FreqAI enabled strategies*
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This function will automatically expand the defined features on the config defined
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         `include_timeframes`, `include_shifted_candles`, and `include_corr_pairs`.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         In other words, a single feature defined in this function
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         will automatically expand to a total of
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         `include_timeframes` * `include_shifted_candles` * `include_corr_pairs`
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         numbers of features added to the model.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Features defined here will *not* be automatically duplicated on user defined
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         `indicator_periods_candles`
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         All features must be prepended with `%` to be recognized by FreqAI internals.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         More details on how these config defined parameters accelerate feature engineering
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         in the documentation at:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         https://www.freqtrade.io/en/latest/freqai-parameter-table/#feature-parameters
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         https://www.freqtrade.io/en/latest/freqai-feature-engineering/#defining-the-features
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: strategy dataframe which will receive the features
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metadata: metadata of current pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-pct-change"] = dataframe["close"].pct_change()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-ema-200"] = ta.EMA(dataframe, timeperiod=200)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def feature_engineering_standard(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, dataframe: DataFrame, metadata: dict, **kwargs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         *Only functional with FreqAI enabled strategies*
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This optional function will be called once with the dataframe of the base timeframe.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This is the final function to be called, which means that the dataframe entering this
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         function will contain all the features and columns created by all other
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         freqai_feature_engineering_* functions.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This function is a good place to do custom exotic feature extractions (e.g. tsfresh).
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This function is a good place for any feature that should not be auto-expanded upon
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         (e.g. day of the week).
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         All features must be prepended with `%` to be recognized by FreqAI internals.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         More details about feature engineering available:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         https://www.freqtrade.io/en/latest/freqai-feature-engineering
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: strategy dataframe which will receive the features
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metadata: metadata of current pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         usage example: dataframe["%-day_of_week"] = (dataframe["date"].dt.dayofweek + 1) / 7
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def set_freqai_targets(self, dataframe: DataFrame, metadata: dict, **kwargs) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         *Only functional with FreqAI enabled strategies*
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Required function to set the targets for the model.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         All targets must be prepended with `&` to be recognized by the FreqAI internals.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         More details about feature engineering available:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         https://www.freqtrade.io/en/latest/freqai-feature-engineering
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: strategy dataframe which will receive the targets
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metadata: metadata of current pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         usage example: dataframe["&-target"] = dataframe["close"].shift(-1) / dataframe["close"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     ###
# REMOVED_UNUSED_CODE:     # END - Intended to be overridden by strategy
# REMOVED_UNUSED_CODE:     ###
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _ft_stop_uses_after_fill = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _adjust_trade_position_internal(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_profit: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         min_stake: float | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         max_stake: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_entry_rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_exit_rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_entry_profit: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_exit_profit: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> tuple[float | None, str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         wrapper around adjust_trade_position to handle the return value
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         resp = strategy_safe_wrapper(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.adjust_trade_position, default_retval=(None, ""), supress_error=True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade=trade,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_time=current_time,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_rate=current_rate,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_profit=current_profit,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             min_stake=min_stake,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             max_stake=max_stake,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_entry_rate=current_entry_rate,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_exit_rate=current_exit_rate,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_entry_profit=current_entry_profit,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_exit_profit=current_exit_profit,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             **kwargs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         order_tag = ""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if isinstance(resp, tuple):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if len(resp) >= 1:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 stake_amount = resp[0]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if len(resp) > 1:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 order_tag = resp[1] or ""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             stake_amount = resp
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return stake_amount, order_tag
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __informative_pairs_freqai(self) -> ListPairsWithTimeframes:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Create informative-pairs needed for FreqAI
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self.config.get("freqai", {}).get("enabled", False):
# REMOVED_UNUSED_CODE:             whitelist_pairs = self.dp.current_whitelist()
# REMOVED_UNUSED_CODE:             candle_type = self.config.get("candle_type_def", CandleType.SPOT)
# REMOVED_UNUSED_CODE:             corr_pairs = self.config["freqai"]["feature_parameters"]["include_corr_pairlist"]
# REMOVED_UNUSED_CODE:             informative_pairs = []
# REMOVED_UNUSED_CODE:             for tf in self.config["freqai"]["feature_parameters"]["include_timeframes"]:
# REMOVED_UNUSED_CODE:                 for pair in set(whitelist_pairs + corr_pairs):
# REMOVED_UNUSED_CODE:                     informative_pairs.append((pair, tf, candle_type))
# REMOVED_UNUSED_CODE:             return informative_pairs
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def gather_informative_pairs(self) -> ListPairsWithTimeframes:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Internal method which gathers all informative pairs (user or automatically defined).
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         informative_pairs = self.informative_pairs()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Compatibility code for 2 tuple informative pairs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         informative_pairs = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 p[0],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 p[1],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     CandleType.from_string(p[2])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     if len(p) > 2 and p[2] != ""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     else self.config.get("candle_type_def", CandleType.SPOT)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 ),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for p in informative_pairs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for inf_data, _ in self._ft_informative:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Get default candle type if not provided explicitly.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             candle_type = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 inf_data.candle_type
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if inf_data.candle_type
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 else self.config.get("candle_type_def", CandleType.SPOT)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if inf_data.asset:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if any(s in inf_data.asset for s in ("{BASE}", "{base}")):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     for pair in self.dp.current_whitelist():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         pair_tf = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             _format_pair_name(self.config, inf_data.asset, self.dp.market(pair)),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             inf_data.timeframe,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             candle_type,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         informative_pairs.append(pair_tf)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     pair_tf = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         _format_pair_name(self.config, inf_data.asset),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         inf_data.timeframe,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         candle_type,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     informative_pairs.append(pair_tf)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 for pair in self.dp.current_whitelist():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     informative_pairs.append((pair, inf_data.timeframe, candle_type))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         informative_pairs.extend(self.__informative_pairs_freqai())
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return list(set(informative_pairs))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_strategy_name(self) -> str:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Returns strategy class name
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self.__class__.__name__
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def lock_pair(
# REMOVED_UNUSED_CODE:         self, pair: str, until: datetime, reason: str | None = None, side: str = "*"
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Locks pair until a given timestamp happens.
# REMOVED_UNUSED_CODE:         Locked pairs are not analyzed, and are prevented from opening new trades.
# REMOVED_UNUSED_CODE:         Locks can only count up (allowing users to lock pairs for a longer period of time).
# REMOVED_UNUSED_CODE:         To remove a lock from a pair, use `unlock_pair()`
# REMOVED_UNUSED_CODE:         :param pair: Pair to lock
# REMOVED_UNUSED_CODE:         :param until: datetime in UTC until the pair should be blocked from opening new trades.
# REMOVED_UNUSED_CODE:                 Needs to be timezone aware `datetime.now(timezone.utc)`
# REMOVED_UNUSED_CODE:         :param reason: Optional string explaining why the pair was locked.
# REMOVED_UNUSED_CODE:         :param side: Side to check, can be long, short or '*'
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         PairLocks.lock_pair(pair, until, reason, side=side)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def unlock_pair(self, pair: str) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Unlocks a pair previously locked using lock_pair.
# REMOVED_UNUSED_CODE:         Not used by freqtrade itself, but intended to be used if users lock pairs
# REMOVED_UNUSED_CODE:         manually from within the strategy, to allow an easy way to unlock pairs.
# REMOVED_UNUSED_CODE:         :param pair: Unlock pair to allow trading again
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         PairLocks.unlock_pair(pair, datetime.now(timezone.utc))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def unlock_reason(self, reason: str) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Unlocks all pairs previously locked using lock_pair with specified reason.
# REMOVED_UNUSED_CODE:         Not used by freqtrade itself, but intended to be used if users lock pairs
# REMOVED_UNUSED_CODE:         manually from within the strategy, to allow an easy way to unlock pairs.
# REMOVED_UNUSED_CODE:         :param reason: Unlock pairs to allow trading again
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         PairLocks.unlock_reason(reason, datetime.now(timezone.utc))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def is_pair_locked(
# REMOVED_UNUSED_CODE:         self, pair: str, *, candle_date: datetime | None = None, side: str = "*"
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Checks if a pair is currently locked
# REMOVED_UNUSED_CODE:         The 2nd, optional parameter ensures that locks are applied until the new candle arrives,
# REMOVED_UNUSED_CODE:         and not stop at 14:00:00 - while the next candle arrives at 14:00:02 leaving a gap
# REMOVED_UNUSED_CODE:         of 2 seconds for an entry order to happen on an old signal.
# REMOVED_UNUSED_CODE:         :param pair: "Pair to check"
# REMOVED_UNUSED_CODE:         :param candle_date: Date of the last candle. Optional, defaults to current date
# REMOVED_UNUSED_CODE:         :param side: Side to check, can be long, short or '*'
# REMOVED_UNUSED_CODE:         :returns: locking state of the pair in question.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not candle_date:
# REMOVED_UNUSED_CODE:             # Simple call ...
# REMOVED_UNUSED_CODE:             return PairLocks.is_pair_locked(pair, side=side)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             lock_time = timeframe_to_next_date(self.timeframe, candle_date)
# REMOVED_UNUSED_CODE:             return PairLocks.is_pair_locked(pair, lock_time, side=side)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def analyze_ticker(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Parses the given candle (OHLCV) data and returns a populated DataFrame
# REMOVED_UNUSED_CODE:         add several TA indicators and entry order signal to it
# REMOVED_UNUSED_CODE:         Should only be used in live.
# REMOVED_UNUSED_CODE:         :param dataframe: Dataframe containing data from exchange
# REMOVED_UNUSED_CODE:         :param metadata: Metadata dictionary with additional data (e.g. 'pair')
# REMOVED_UNUSED_CODE:         :return: DataFrame of candle (OHLCV) data with indicator data and signals added
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         logger.debug("TA Analysis Launched")
# REMOVED_UNUSED_CODE:         dataframe = self.advise_indicators(dataframe, metadata)
# REMOVED_UNUSED_CODE:         dataframe = self.advise_entry(dataframe, metadata)
# REMOVED_UNUSED_CODE:         dataframe = self.advise_exit(dataframe, metadata)
# REMOVED_UNUSED_CODE:         logger.debug("TA Analysis Ended")
# REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _analyze_ticker_internal(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Parses the given candle (OHLCV) data and returns a populated DataFrame
# REMOVED_UNUSED_CODE:         add several TA indicators and buy signal to it
# REMOVED_UNUSED_CODE:         WARNING: Used internally only, may skip analysis if `process_only_new_candles` is set.
# REMOVED_UNUSED_CODE:         :param dataframe: Dataframe containing data from exchange
# REMOVED_UNUSED_CODE:         :param metadata: Metadata dictionary with additional data (e.g. 'pair')
# REMOVED_UNUSED_CODE:         :return: DataFrame of candle (OHLCV) data with indicator data and signals added
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         pair = str(metadata.get("pair"))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         new_candle = self._last_candle_seen_per_pair.get(pair, None) != dataframe.iloc[-1]["date"]
# REMOVED_UNUSED_CODE:         # Test if seen this pair and last candle before.
# REMOVED_UNUSED_CODE:         # always run if process_only_new_candles is set to false
# REMOVED_UNUSED_CODE:         if not self.process_only_new_candles or new_candle:
# REMOVED_UNUSED_CODE:             # Defs that only make change on new candle data.
# REMOVED_UNUSED_CODE:             dataframe = self.analyze_ticker(dataframe, metadata)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self._last_candle_seen_per_pair[pair] = dataframe.iloc[-1]["date"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             candle_type = self.config.get("candle_type_def", CandleType.SPOT)
# REMOVED_UNUSED_CODE:             self.dp._set_cached_df(pair, self.timeframe, dataframe, candle_type=candle_type)
# REMOVED_UNUSED_CODE:             self.dp._emit_df((pair, self.timeframe, candle_type), dataframe, new_candle)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.debug("Skipping TA Analysis for already analyzed candle")
# REMOVED_UNUSED_CODE:             dataframe = remove_entry_exit_signals(dataframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.debug("Loop Analysis Launched")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def analyze_pair(self, pair: str) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Fetch data for this pair from dataprovider and analyze.
# REMOVED_UNUSED_CODE:         Stores the dataframe into the dataprovider.
# REMOVED_UNUSED_CODE:         The analyzed dataframe is then accessible via `dp.get_analyzed_dataframe()`.
# REMOVED_UNUSED_CODE:         :param pair: Pair to analyze.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         dataframe = self.dp.ohlcv(
# REMOVED_UNUSED_CODE:             pair, self.timeframe, candle_type=self.config.get("candle_type_def", CandleType.SPOT)
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         if not isinstance(dataframe, DataFrame) or dataframe.empty:
# REMOVED_UNUSED_CODE:             logger.warning("Empty candle (OHLCV) data for pair %s", pair)
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             df_len, df_close, df_date = self.preserve_df(dataframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             dataframe = strategy_safe_wrapper(self._analyze_ticker_internal, message="")(
# REMOVED_UNUSED_CODE:                 dataframe, {"pair": pair}
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.assert_df(dataframe, df_len, df_close, df_date)
# REMOVED_UNUSED_CODE:         except StrategyError as error:
# REMOVED_UNUSED_CODE:             logger.warning(f"Unable to analyze candle (OHLCV) data for pair {pair}: {error}")
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if dataframe.empty:
# REMOVED_UNUSED_CODE:             logger.warning("Empty dataframe for pair %s", pair)
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def analyze(self, pairs: list[str]) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Analyze all pairs using analyze_pair().
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pairs: List of pairs to analyze
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for pair in pairs:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.analyze_pair(pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def preserve_df(dataframe: DataFrame) -> tuple[int, float, datetime]:
# REMOVED_UNUSED_CODE:         """keep some data for dataframes"""
# REMOVED_UNUSED_CODE:         return len(dataframe), dataframe["close"].iloc[-1], dataframe["date"].iloc[-1]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def assert_df(self, dataframe: DataFrame, df_len: int, df_close: float, df_date: datetime):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Ensure dataframe (length, last candle) was not modified, and has all elements we need.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         message_template = "Dataframe returned from strategy has mismatching {}."
# REMOVED_UNUSED_CODE:         message = ""
# REMOVED_UNUSED_CODE:         if dataframe is None:
# REMOVED_UNUSED_CODE:             message = "No dataframe returned (return statement missing?)."
# REMOVED_UNUSED_CODE:         elif df_len != len(dataframe):
# REMOVED_UNUSED_CODE:             message = message_template.format("length")
# REMOVED_UNUSED_CODE:         elif df_close != dataframe["close"].iloc[-1]:
# REMOVED_UNUSED_CODE:             message = message_template.format("last close price")
# REMOVED_UNUSED_CODE:         elif df_date != dataframe["date"].iloc[-1]:
# REMOVED_UNUSED_CODE:             message = message_template.format("last date")
# REMOVED_UNUSED_CODE:         if message:
# REMOVED_UNUSED_CODE:             if self.disable_dataframe_checks:
# REMOVED_UNUSED_CODE:                 logger.warning(message)
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 raise StrategyError(message)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_latest_candle(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         timeframe: str,
# REMOVED_UNUSED_CODE:         dataframe: DataFrame,
# REMOVED_UNUSED_CODE:     ) -> tuple[DataFrame | None, datetime | None]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Calculates current signal based based on the entry order or exit order
# REMOVED_UNUSED_CODE:         columns of the dataframe.
# REMOVED_UNUSED_CODE:         Used by Bot to get the signal to enter, or exit
# REMOVED_UNUSED_CODE:         :param pair: pair in format ANT/BTC
# REMOVED_UNUSED_CODE:         :param timeframe: timeframe to use
# REMOVED_UNUSED_CODE:         :param dataframe: Analyzed dataframe to get signal from.
# REMOVED_UNUSED_CODE:         :return: (None, None) or (Dataframe, latest_date) - corresponding to the last candle
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not isinstance(dataframe, DataFrame) or dataframe.empty:
# REMOVED_UNUSED_CODE:             logger.warning(f"Empty candle (OHLCV) data for pair {pair}")
# REMOVED_UNUSED_CODE:             return None, None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             latest_date_pd = dataframe["date"].max()
# REMOVED_UNUSED_CODE:             latest = dataframe.loc[dataframe["date"] == latest_date_pd].iloc[-1]
# REMOVED_UNUSED_CODE:         except Exception as e:
# REMOVED_UNUSED_CODE:             logger.warning(f"Unable to get latest candle (OHLCV) data for pair {pair} - {e}")
# REMOVED_UNUSED_CODE:             return None, None
# REMOVED_UNUSED_CODE:         # Explicitly convert to datetime object to ensure the below comparison does not fail
# REMOVED_UNUSED_CODE:         latest_date: datetime = latest_date_pd.to_pydatetime()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Check if dataframe is out of date
# REMOVED_UNUSED_CODE:         timeframe_minutes = timeframe_to_minutes(timeframe)
# REMOVED_UNUSED_CODE:         offset = self.config.get("exchange", {}).get("outdated_offset", 5)
# REMOVED_UNUSED_CODE:         if latest_date < (dt_now() - timedelta(minutes=timeframe_minutes * 2 + offset)):
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 "Outdated history for pair %s. Last tick is %s minutes old",
# REMOVED_UNUSED_CODE:                 pair,
# REMOVED_UNUSED_CODE:                 int((dt_now() - latest_date).total_seconds() // 60),
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             return None, None
# REMOVED_UNUSED_CODE:         return latest, latest_date
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_exit_signal(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pair: str, timeframe: str, dataframe: DataFrame, is_short: bool | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> tuple[bool, bool, str | None]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Calculates current exit signal based based on the dataframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         columns of the dataframe.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Used by Bot to get the signal to exit.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         depending on is_short, looks at "short" or "long" columns.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: pair in format ANT/BTC
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param timeframe: timeframe to use
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: Analyzed dataframe to get signal from.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param is_short: Indicating existing trade direction.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: (enter, exit) A bool-tuple with enter / exit values.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         latest, _latest_date = self.get_latest_candle(pair, timeframe, dataframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if latest is None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return False, False, None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if is_short:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             enter = latest.get(SignalType.ENTER_SHORT.value, 0) == 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             exit_ = latest.get(SignalType.EXIT_SHORT.value, 0) == 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             enter = latest.get(SignalType.ENTER_LONG.value, 0) == 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             exit_ = latest.get(SignalType.EXIT_LONG.value, 0) == 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         exit_tag = latest.get(SignalTagType.EXIT_TAG.value, None)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Tags can be None, which does not resolve to False.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         exit_tag = exit_tag if isinstance(exit_tag, str) and exit_tag != "nan" else None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.debug(f"exit-trigger: {latest['date']} (pair={pair}) enter={enter} exit={exit_}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return enter, exit_, exit_tag
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_entry_signal(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         timeframe: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe: DataFrame,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> tuple[SignalDirection | None, str | None]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Calculates current entry signal based based on the dataframe signals
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         columns of the dataframe.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Used by Bot to get the signal to enter trades.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: pair in format ANT/BTC
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param timeframe: timeframe to use
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: Analyzed dataframe to get signal from.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: (SignalDirection, entry_tag)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         latest, latest_date = self.get_latest_candle(pair, timeframe, dataframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if latest is None or latest_date is None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return None, None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         enter_long = latest.get(SignalType.ENTER_LONG.value, 0) == 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         exit_long = latest.get(SignalType.EXIT_LONG.value, 0) == 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         enter_short = latest.get(SignalType.ENTER_SHORT.value, 0) == 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         exit_short = latest.get(SignalType.EXIT_SHORT.value, 0) == 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         enter_signal: SignalDirection | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         enter_tag: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if enter_long == 1 and not any([exit_long, enter_short]):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             enter_signal = SignalDirection.LONG
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             enter_tag = latest.get(SignalTagType.ENTER_TAG.value, None)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.config.get("trading_mode", TradingMode.SPOT) != TradingMode.SPOT
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             and self.can_short
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             and enter_short == 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             and not any([exit_short, enter_long])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             enter_signal = SignalDirection.SHORT
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             enter_tag = latest.get(SignalTagType.ENTER_TAG.value, None)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         enter_tag = enter_tag if isinstance(enter_tag, str) and enter_tag != "nan" else None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         timeframe_seconds = timeframe_to_seconds(timeframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.ignore_expired_candle(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             latest_date=latest_date,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_time=dt_now(),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             timeframe_seconds=timeframe_seconds,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             enter=bool(enter_signal),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return None, enter_tag
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.debug(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"entry trigger: {latest['date']} (pair={pair}) "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"enter={enter_long} enter_tag_value={enter_tag}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return enter_signal, enter_tag
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def ignore_expired_candle(
# REMOVED_UNUSED_CODE:         self, latest_date: datetime, current_time: datetime, timeframe_seconds: int, enter: bool
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         if self.ignore_buying_expired_candle_after and enter:
# REMOVED_UNUSED_CODE:             time_delta = current_time - (latest_date + timedelta(seconds=timeframe_seconds))
# REMOVED_UNUSED_CODE:             return time_delta.total_seconds() > self.ignore_buying_expired_candle_after
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def should_exit(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         enter: bool,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         exit_: bool,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         low: float | None = None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         high: float | None = None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         force_stoploss: float = 0,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> list[ExitCheckTuple]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This function evaluates if one of the conditions required to trigger an exit order
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         has been reached, which can either be a stop-loss, ROI or exit-signal.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param low: Only used during backtesting to simulate (long)stoploss/(short)ROI
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param high: Only used during backtesting, to simulate (short)stoploss/(long)ROI
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param force_stoploss: Externally provided stoploss
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: List of exit reasons - or empty list.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         exits: list[ExitCheckTuple] = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_rate = rate
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_profit = trade.calc_profit_ratio(current_rate)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_profit_best = current_profit
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if low is not None or high is not None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Set current rate to high for backtesting ROI exits
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_rate_best = (low if trade.is_short else high) or rate
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_profit_best = trade.calc_profit_ratio(current_rate_best)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade.adjust_min_max_rates(high or current_rate, low or current_rate)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stoplossflag = self.ft_stoploss_reached(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_rate=current_rate,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade=trade,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_time=current_time,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_profit=current_profit,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             force_stoploss=force_stoploss,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             low=low,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             high=high,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # if enter signal and ignore_roi is set, we don't need to evaluate min_roi.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         roi_reached = not (enter and self.ignore_roi_if_entry_signal) and self.min_roi_reached(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade=trade, current_profit=current_profit_best, current_time=current_time
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         exit_signal = ExitType.NONE
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         custom_reason = ""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.use_exit_signal:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if exit_ and not enter:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 exit_signal = ExitType.EXIT_SIGNAL
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 reason_cust = strategy_safe_wrapper(self.custom_exit, default_retval=False)(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     pair=trade.pair,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     trade=trade,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     current_time=current_time,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     current_rate=current_rate,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     current_profit=current_profit,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if reason_cust:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     exit_signal = ExitType.CUSTOM_EXIT
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     if isinstance(reason_cust, str):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         custom_reason = reason_cust
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         if len(reason_cust) > CUSTOM_TAG_MAX_LENGTH:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             logger.warning(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 f"Custom exit reason returned from "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 f"custom_exit is too long and was trimmed"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 f"to {CUSTOM_TAG_MAX_LENGTH} characters."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             custom_reason = reason_cust[:CUSTOM_TAG_MAX_LENGTH]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         custom_reason = ""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if exit_signal == ExitType.CUSTOM_EXIT or (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 exit_signal == ExitType.EXIT_SIGNAL
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 and (not self.exit_profit_only or current_profit > self.exit_profit_offset)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.debug(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"{trade.pair} - Sell signal received. "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"exit_type=ExitType.{exit_signal.name}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     + (f", custom_reason={custom_reason}" if custom_reason else "")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 exits.append(ExitCheckTuple(exit_type=exit_signal, exit_reason=custom_reason))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Sequence:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Exit-signal
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Stoploss
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # ROI
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Trailing stoploss
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if stoplossflag.exit_type in (ExitType.STOP_LOSS, ExitType.LIQUIDATION):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.debug(f"{trade.pair} - Stoploss hit. exit_type={stoplossflag.exit_type}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             exits.append(stoplossflag)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if roi_reached:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.debug(f"{trade.pair} - Required profit reached. exit_type=ExitType.ROI")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             exits.append(ExitCheckTuple(exit_type=ExitType.ROI))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if stoplossflag.exit_type == ExitType.TRAILING_STOP_LOSS:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.debug(f"{trade.pair} - Trailing stoploss hit.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             exits.append(stoplossflag)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return exits
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def ft_stoploss_adjust(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         current_rate: float,
# REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE:         current_profit: float,
# REMOVED_UNUSED_CODE:         force_stoploss: float,
# REMOVED_UNUSED_CODE:         low: float | None = None,
# REMOVED_UNUSED_CODE:         high: float | None = None,
# REMOVED_UNUSED_CODE:         after_fill: bool = False,
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Adjust stop-loss dynamically if configured to do so.
# REMOVED_UNUSED_CODE:         :param current_profit: current profit as ratio
# REMOVED_UNUSED_CODE:         :param low: Low value of this candle, only set in backtesting
# REMOVED_UNUSED_CODE:         :param high: High value of this candle, only set in backtesting
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if after_fill and not self._ft_stop_uses_after_fill:
# REMOVED_UNUSED_CODE:             # Skip if the strategy doesn't support after fill.
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         stop_loss_value = force_stoploss if force_stoploss else self.stoploss
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Initiate stoploss with open_rate. Does nothing if stoploss is already set.
# REMOVED_UNUSED_CODE:         trade.adjust_stop_loss(trade.open_rate, stop_loss_value, initial=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         dir_correct = (
# REMOVED_UNUSED_CODE:             trade.stop_loss < (low or current_rate)
# REMOVED_UNUSED_CODE:             if not trade.is_short
# REMOVED_UNUSED_CODE:             else trade.stop_loss > (high or current_rate)
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Make sure current_profit is calculated using high for backtesting.
# REMOVED_UNUSED_CODE:         bound = low if trade.is_short else high
# REMOVED_UNUSED_CODE:         bound_profit = current_profit if not bound else trade.calc_profit_ratio(bound)
# REMOVED_UNUSED_CODE:         if self.use_custom_stoploss and dir_correct:
# REMOVED_UNUSED_CODE:             stop_loss_value_custom = strategy_safe_wrapper(
# REMOVED_UNUSED_CODE:                 self.custom_stoploss, default_retval=None, supress_error=True
# REMOVED_UNUSED_CODE:             )(
# REMOVED_UNUSED_CODE:                 pair=trade.pair,
# REMOVED_UNUSED_CODE:                 trade=trade,
# REMOVED_UNUSED_CODE:                 current_time=current_time,
# REMOVED_UNUSED_CODE:                 current_rate=(bound or current_rate),
# REMOVED_UNUSED_CODE:                 current_profit=bound_profit,
# REMOVED_UNUSED_CODE:                 after_fill=after_fill,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             # Sanity check - error cases will return None
# REMOVED_UNUSED_CODE:             if stop_loss_value_custom and not (
# REMOVED_UNUSED_CODE:                 isnan(stop_loss_value_custom) or isinf(stop_loss_value_custom)
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 stop_loss_value = stop_loss_value_custom
# REMOVED_UNUSED_CODE:                 trade.adjust_stop_loss(
# REMOVED_UNUSED_CODE:                     bound or current_rate, stop_loss_value, allow_refresh=after_fill
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 logger.debug("CustomStoploss function did not return valid stoploss")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.trailing_stop and dir_correct:
# REMOVED_UNUSED_CODE:             # trailing stoploss handling
# REMOVED_UNUSED_CODE:             sl_offset = self.trailing_stop_positive_offset
# REMOVED_UNUSED_CODE:             # Make sure current_profit is calculated using high for backtesting.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Don't update stoploss if trailing_only_offset_is_reached is true.
# REMOVED_UNUSED_CODE:             if not (self.trailing_only_offset_is_reached and bound_profit < sl_offset):
# REMOVED_UNUSED_CODE:                 # Specific handling for trailing_stop_positive
# REMOVED_UNUSED_CODE:                 if self.trailing_stop_positive is not None and bound_profit > sl_offset:
# REMOVED_UNUSED_CODE:                     stop_loss_value = self.trailing_stop_positive
# REMOVED_UNUSED_CODE:                     logger.debug(
# REMOVED_UNUSED_CODE:                         f"{trade.pair} - Using positive stoploss: {stop_loss_value} "
# REMOVED_UNUSED_CODE:                         f"offset: {sl_offset:.4g} profit: {bound_profit:.2%}"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 trade.adjust_stop_loss(bound or current_rate, stop_loss_value)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def ft_stoploss_reached(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         current_rate: float,
# REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE:         current_profit: float,
# REMOVED_UNUSED_CODE:         force_stoploss: float,
# REMOVED_UNUSED_CODE:         low: float | None = None,
# REMOVED_UNUSED_CODE:         high: float | None = None,
# REMOVED_UNUSED_CODE:     ) -> ExitCheckTuple:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Based on current profit of the trade and configured (trailing) stoploss,
# REMOVED_UNUSED_CODE:         decides to exit or not
# REMOVED_UNUSED_CODE:         :param current_profit: current profit as ratio
# REMOVED_UNUSED_CODE:         :param low: Low value of this candle, only set in backtesting
# REMOVED_UNUSED_CODE:         :param high: High value of this candle, only set in backtesting
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.ft_stoploss_adjust(
# REMOVED_UNUSED_CODE:             current_rate, trade, current_time, current_profit, force_stoploss, low, high
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         sl_higher_long = trade.stop_loss >= (low or current_rate) and not trade.is_short
# REMOVED_UNUSED_CODE:         sl_lower_short = trade.stop_loss <= (high or current_rate) and trade.is_short
# REMOVED_UNUSED_CODE:         liq_higher_long = (
# REMOVED_UNUSED_CODE:             trade.liquidation_price
# REMOVED_UNUSED_CODE:             and trade.liquidation_price >= (low or current_rate)
# REMOVED_UNUSED_CODE:             and not trade.is_short
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         liq_lower_short = (
# REMOVED_UNUSED_CODE:             trade.liquidation_price
# REMOVED_UNUSED_CODE:             and trade.liquidation_price <= (high or current_rate)
# REMOVED_UNUSED_CODE:             and trade.is_short
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # evaluate if the stoploss was hit if stoploss is not on exchange
# REMOVED_UNUSED_CODE:         # in Dry-Run, this handles stoploss logic as well, as the logic will not be different to
# REMOVED_UNUSED_CODE:         # regular stoploss handling.
# REMOVED_UNUSED_CODE:         if (sl_higher_long or sl_lower_short) and (
# REMOVED_UNUSED_CODE:             not self.order_types.get("stoploss_on_exchange") or self.config["dry_run"]
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             exit_type = ExitType.STOP_LOSS
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # If initial stoploss is not the same as current one then it is trailing.
# REMOVED_UNUSED_CODE:             if trade.is_stop_loss_trailing:
# REMOVED_UNUSED_CODE:                 exit_type = ExitType.TRAILING_STOP_LOSS
# REMOVED_UNUSED_CODE:                 logger.debug(
# REMOVED_UNUSED_CODE:                     f"{trade.pair} - HIT STOP: current price at "
# REMOVED_UNUSED_CODE:                     f"{((high if trade.is_short else low) or current_rate):.6f}, "
# REMOVED_UNUSED_CODE:                     f"stoploss is {trade.stop_loss:.6f}, "
# REMOVED_UNUSED_CODE:                     f"initial stoploss was at {trade.initial_stop_loss:.6f}, "
# REMOVED_UNUSED_CODE:                     f"trade opened at {trade.open_rate:.6f}"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             return ExitCheckTuple(exit_type=exit_type)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if liq_higher_long or liq_lower_short:
# REMOVED_UNUSED_CODE:             logger.debug(f"{trade.pair} - Liquidation price hit. exit_type=ExitType.LIQUIDATION")
# REMOVED_UNUSED_CODE:             return ExitCheckTuple(exit_type=ExitType.LIQUIDATION)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return ExitCheckTuple(exit_type=ExitType.NONE)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def min_roi_reached_entry(self, trade_dur: int) -> tuple[int | None, float | None]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Based on trade duration defines the ROI entry that may have been reached.
# REMOVED_UNUSED_CODE:         :param trade_dur: trade duration in minutes
# REMOVED_UNUSED_CODE:         :return: minimal ROI entry value or None if none proper ROI entry was found.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Get highest entry in ROI dict where key <= trade-duration
# REMOVED_UNUSED_CODE:         roi_list = [x for x in self.minimal_roi.keys() if x <= trade_dur]
# REMOVED_UNUSED_CODE:         if not roi_list:
# REMOVED_UNUSED_CODE:             return None, None
# REMOVED_UNUSED_CODE:         roi_entry = max(roi_list)
# REMOVED_UNUSED_CODE:         return roi_entry, self.minimal_roi[roi_entry]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def min_roi_reached(self, trade: Trade, current_profit: float, current_time: datetime) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Based on trade duration, current profit of the trade and ROI configuration,
# REMOVED_UNUSED_CODE:         decides whether bot should exit.
# REMOVED_UNUSED_CODE:         :param current_profit: current profit as ratio
# REMOVED_UNUSED_CODE:         :return: True if bot should exit at current rate
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Check if time matches and current rate is above threshold
# REMOVED_UNUSED_CODE:         trade_dur = int((current_time.timestamp() - trade.open_date_utc.timestamp()) // 60)
# REMOVED_UNUSED_CODE:         _, roi = self.min_roi_reached_entry(trade_dur)
# REMOVED_UNUSED_CODE:         if roi is None:
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return current_profit > roi
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def ft_check_timed_out(self, trade: Trade, order: Order, current_time: datetime) -> bool:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         FT Internal method.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Check if timeout is active, and if the order is still open and timed out
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         side = "entry" if order.ft_order_side == trade.entry_side else "exit"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         timeout = self.config.get("unfilledtimeout", {}).get(side)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if timeout is not None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             timeout_unit = self.config.get("unfilledtimeout", {}).get("unit", "minutes")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             timeout_kwargs = {timeout_unit: -timeout}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             timeout_threshold = current_time + timedelta(**timeout_kwargs)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             timedout = order.status == "open" and order.order_date_utc < timeout_threshold
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if timedout:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         time_method = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.check_exit_timeout
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if order.ft_order_side == trade.exit_side
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else self.check_entry_timeout
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return strategy_safe_wrapper(time_method, default_retval=False)(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pair=trade.pair, trade=trade, order=order, current_time=current_time
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def advise_all_indicators(self, data: dict[str, DataFrame]) -> dict[str, DataFrame]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Populates indicators for given candle (OHLCV) data (for multiple pairs)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Does not run advise_entry or advise_exit!
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Used by optimize operations only, not during dry / live runs.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Using .copy() to get a fresh copy of the dataframe for every strategy run.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Also copy on output to avoid PerformanceWarnings pandas 1.3.0 started to show.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Has positive effects on memory usage for whatever reason - also when
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         using only one strategy.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pair: self.advise_indicators(pair_data.copy(), {"pair": pair}).copy()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for pair, pair_data in data.items()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def ft_advise_signals(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Call advise_entry and advise_exit and return the resulting dataframe.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: Dataframe containing data from exchange, as well as pre-calculated
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                           indicators
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metadata: Metadata dictionary with additional data (e.g. 'pair')
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: DataFrame of candle (OHLCV) data with indicator data and signals added
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe = self.advise_entry(dataframe, metadata)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe = self.advise_exit(dataframe, metadata)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _if_enabled_populate_trades(self, dataframe: DataFrame, metadata: dict):
# REMOVED_UNUSED_CODE:         use_public_trades = self.config.get("exchange", {}).get("use_public_trades", False)
# REMOVED_UNUSED_CODE:         if use_public_trades:
# REMOVED_UNUSED_CODE:             trades = self.dp.trades(pair=metadata["pair"], copy=False)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             pair = metadata["pair"]
# REMOVED_UNUSED_CODE:             # TODO: slice trades to size of dataframe for faster backtesting
# REMOVED_UNUSED_CODE:             cached_grouped_trades: DataFrame | None = self._cached_grouped_trades_per_pair.get(pair)
# REMOVED_UNUSED_CODE:             dataframe, cached_grouped_trades = populate_dataframe_with_trades(
# REMOVED_UNUSED_CODE:                 cached_grouped_trades, self.config, dataframe, trades
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # dereference old cache
# REMOVED_UNUSED_CODE:             if pair in self._cached_grouped_trades_per_pair:
# REMOVED_UNUSED_CODE:                 del self._cached_grouped_trades_per_pair[pair]
# REMOVED_UNUSED_CODE:             self._cached_grouped_trades_per_pair[pair] = cached_grouped_trades
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             logger.debug("Populated dataframe with trades.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def advise_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Populate indicators that will be used in the Buy, Sell, short, exit_short strategy
# REMOVED_UNUSED_CODE:         This method should not be overridden.
# REMOVED_UNUSED_CODE:         :param dataframe: Dataframe with data from the exchange
# REMOVED_UNUSED_CODE:         :param metadata: Additional information, like the currently traded pair
# REMOVED_UNUSED_CODE:         :return: a Dataframe with all mandatory indicators for the strategies
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         logger.debug(f"Populating indicators for pair {metadata.get('pair')}.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # call populate_indicators_Nm() which were tagged with @informative decorator.
# REMOVED_UNUSED_CODE:         for inf_data, populate_fn in self._ft_informative:
# REMOVED_UNUSED_CODE:             dataframe = _create_and_merge_informative_pair(
# REMOVED_UNUSED_CODE:                 self, dataframe, metadata, inf_data, populate_fn
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._if_enabled_populate_trades(dataframe, metadata)
# REMOVED_UNUSED_CODE:         return self.populate_indicators(dataframe, metadata)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def advise_entry(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Based on TA indicators, populates the entry order signal for the given dataframe
# REMOVED_UNUSED_CODE:         This method should not be overridden.
# REMOVED_UNUSED_CODE:         :param dataframe: DataFrame
# REMOVED_UNUSED_CODE:         :param metadata: Additional information dictionary, with details like the
# REMOVED_UNUSED_CODE:             currently traded pair
# REMOVED_UNUSED_CODE:         :return: DataFrame with buy column
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.debug(f"Populating enter signals for pair {metadata.get('pair')}.")
# REMOVED_UNUSED_CODE:         # Initialize column to work around Pandas bug #56503.
# REMOVED_UNUSED_CODE:         dataframe.loc[:, "enter_tag"] = ""
# REMOVED_UNUSED_CODE:         df = self.populate_entry_trend(dataframe, metadata)
# REMOVED_UNUSED_CODE:         if "enter_long" not in df.columns:
# REMOVED_UNUSED_CODE:             df = df.rename({"buy": "enter_long", "buy_tag": "enter_tag"}, axis="columns")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return df
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def advise_exit(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Based on TA indicators, populates the exit order signal for the given dataframe
# REMOVED_UNUSED_CODE:         This method should not be overridden.
# REMOVED_UNUSED_CODE:         :param dataframe: DataFrame
# REMOVED_UNUSED_CODE:         :param metadata: Additional information dictionary, with details like the
# REMOVED_UNUSED_CODE:             currently traded pair
# REMOVED_UNUSED_CODE:         :return: DataFrame with exit column
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Initialize column to work around Pandas bug #56503.
# REMOVED_UNUSED_CODE:         dataframe.loc[:, "exit_tag"] = ""
# REMOVED_UNUSED_CODE:         logger.debug(f"Populating exit signals for pair {metadata.get('pair')}.")
# REMOVED_UNUSED_CODE:         df = self.populate_exit_trend(dataframe, metadata)
# REMOVED_UNUSED_CODE:         if "exit_long" not in df.columns:
# REMOVED_UNUSED_CODE:             df = df.rename({"sell": "exit_long"}, axis="columns")
# REMOVED_UNUSED_CODE:         return df
