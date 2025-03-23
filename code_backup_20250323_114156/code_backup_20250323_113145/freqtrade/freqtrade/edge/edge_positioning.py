# pragma pylint: disable=W0603
"""Edge positioning package"""

import logging
# REMOVED_UNUSED_CODE: from collections import defaultdict
# REMOVED_UNUSED_CODE: from copy import deepcopy
# REMOVED_UNUSED_CODE: from datetime import timedelta
# REMOVED_UNUSED_CODE: from typing import Any, NamedTuple

# REMOVED_UNUSED_CODE: import numpy as np
# REMOVED_UNUSED_CODE: import utils_find_1st as utf1st
# REMOVED_UNUSED_CODE: from pandas import DataFrame

# REMOVED_UNUSED_CODE: from freqtrade.configuration import TimeRange
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.constants import DATETIME_PRINT_FORMAT, UNLIMITED_STAKE_AMOUNT, Config
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.data.history import get_timerange, load_data, refresh_data
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.enums import CandleType, ExitType, RunMode
# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException
# REMOVED_UNUSED_CODE: from freqtrade.exchange import timeframe_to_seconds
# REMOVED_UNUSED_CODE: from freqtrade.plugins.pairlist.pairlist_helpers import expand_pairlist
# REMOVED_UNUSED_CODE: from freqtrade.strategy.interface import IStrategy
# REMOVED_UNUSED_CODE: from freqtrade.util import dt_now


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class PairInfo(NamedTuple):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stoploss: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     winrate: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     risk_reward_ratio: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     required_risk_reward: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     expectancy: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     nb_trades: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     avg_trade_duration: float


# REMOVED_UNUSED_CODE: class Edge:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Calculates Win Rate, Risk Reward Ratio, Expectancy
# REMOVED_UNUSED_CODE:     against historical data for a give set of markets and a strategy
# REMOVED_UNUSED_CODE:     it then adjusts stoploss and position size accordingly
# REMOVED_UNUSED_CODE:     and force it into the strategy
# REMOVED_UNUSED_CODE:     Author: https://github.com/mishaker
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _cached_pairs: dict[str, Any] = {}  # Keeps a list of pairs
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, config: Config, exchange, strategy) -> None:
# REMOVED_UNUSED_CODE:         self.config = config
# REMOVED_UNUSED_CODE:         self.exchange = exchange
# REMOVED_UNUSED_CODE:         self.strategy: IStrategy = strategy
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.edge_config = self.config.get("edge", {})
# REMOVED_UNUSED_CODE:         self._cached_pairs: dict[str, Any] = {}  # Keeps a list of pairs
# REMOVED_UNUSED_CODE:         self._final_pairs: list = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # checking max_open_trades. it should be -1 as with Edge
# REMOVED_UNUSED_CODE:         # the number of trades is determined by position size
# REMOVED_UNUSED_CODE:         if self.config["max_open_trades"] != float("inf"):
# REMOVED_UNUSED_CODE:             logger.critical("max_open_trades should be -1 in config !")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.config["stake_amount"] != UNLIMITED_STAKE_AMOUNT:
# REMOVED_UNUSED_CODE:             raise OperationalException("Edge works only with unlimited stake amount")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._capital_ratio: float = self.config["tradable_balance_ratio"]
# REMOVED_UNUSED_CODE:         self._allowed_risk: float = self.edge_config.get("allowed_risk")
# REMOVED_UNUSED_CODE:         self._since_number_of_days: int = self.edge_config.get("calculate_since_number_of_days", 14)
# REMOVED_UNUSED_CODE:         self._last_updated: int = 0  # Timestamp of pairs last updated time
# REMOVED_UNUSED_CODE:         self._refresh_pairs = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._stoploss_range_min = float(self.edge_config.get("stoploss_range_min", -0.01))
# REMOVED_UNUSED_CODE:         self._stoploss_range_max = float(self.edge_config.get("stoploss_range_max", -0.05))
# REMOVED_UNUSED_CODE:         self._stoploss_range_step = float(self.edge_config.get("stoploss_range_step", -0.001))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # calculating stoploss range
# REMOVED_UNUSED_CODE:         self._stoploss_range = np.arange(
# REMOVED_UNUSED_CODE:             self._stoploss_range_min, self._stoploss_range_max, self._stoploss_range_step
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._timerange: TimeRange = TimeRange.parse_timerange(
# REMOVED_UNUSED_CODE:             f"{(dt_now() - timedelta(days=self._since_number_of_days)).strftime('%Y%m%d')}-"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         if config.get("fee"):
# REMOVED_UNUSED_CODE:             self.fee = config["fee"]
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 self.fee = self.exchange.get_fee(
# REMOVED_UNUSED_CODE:                     symbol=expand_pairlist(
# REMOVED_UNUSED_CODE:                         self.config["exchange"]["pair_whitelist"], list(self.exchange.markets)
# REMOVED_UNUSED_CODE:                     )[0]
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             except IndexError:
# REMOVED_UNUSED_CODE:                 self.fee = None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def calculate(self, pairs: list[str]) -> bool:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.fee is None and pairs:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.fee = self.exchange.get_fee(pairs[0])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         heartbeat = self.edge_config.get("process_throttle_secs")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if (self._last_updated > 0) and (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._last_updated + heartbeat > int(dt_now().timestamp())
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         data: dict[str, Any] = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info("Using stake_currency: %s ...", self.config["stake_currency"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info("Using local backtesting data (using whitelist in given config) ...")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._refresh_pairs:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             timerange_startup = deepcopy(self._timerange)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             timerange_startup.subtract_start(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 timeframe_to_seconds(self.strategy.timeframe) * self.strategy.startup_candle_count
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             refresh_data(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 datadir=self.config["datadir"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 pairs=pairs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 exchange=self.exchange,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 timeframe=self.strategy.timeframe,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 timerange=timerange_startup,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 data_format=self.config["dataformat_ohlcv"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 candle_type=self.config.get("candle_type_def", CandleType.SPOT),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Download informative pairs too
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             res = defaultdict(list)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for pair, timeframe, _ in self.strategy.gather_informative_pairs():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 res[timeframe].append(pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for timeframe, inf_pairs in res.items():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 timerange_startup = deepcopy(self._timerange)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 timerange_startup.subtract_start(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     timeframe_to_seconds(timeframe) * self.strategy.startup_candle_count
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 refresh_data(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     datadir=self.config["datadir"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     pairs=inf_pairs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     exchange=self.exchange,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     timeframe=timeframe,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     timerange=timerange_startup,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     data_format=self.config["dataformat_ohlcv"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     candle_type=self.config.get("candle_type_def", CandleType.SPOT),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         data = load_data(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             datadir=self.config["datadir"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pairs=pairs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             timeframe=self.strategy.timeframe,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             timerange=self._timerange,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             startup_candles=self.strategy.startup_candle_count,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             data_format=self.config["dataformat_ohlcv"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             candle_type=self.config.get("candle_type_def", CandleType.SPOT),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not data:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Reinitializing cached pairs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._cached_pairs = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.critical("No data found. Edge is stopped ...")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Fake run-mode to Edge
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         prior_rm = self.config["runmode"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.config["runmode"] = RunMode.EDGE
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         preprocessed = self.strategy.advise_all_indicators(data)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.config["runmode"] = prior_rm
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Print timeframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         min_date, max_date = get_timerange(preprocessed)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"Measuring data from {min_date.strftime(DATETIME_PRINT_FORMAT)} "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"up to {max_date.strftime(DATETIME_PRINT_FORMAT)} "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"({(max_date - min_date).days} days).."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # TODO: Should edge support shorts? needs to be investigated further
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # * (add enter_short exit_short)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         headers = ["date", "open", "high", "low", "close", "enter_long", "exit_long"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trades: list = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for pair, pair_data in preprocessed.items():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Sorting dataframe by date and reset index
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pair_data = pair_data.sort_values(by=["date"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pair_data = pair_data.reset_index(drop=True)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df_analyzed = self.strategy.ft_advise_signals(pair_data, {"pair": pair})[headers].copy()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trades += self._find_trades_for_stoploss_range(df_analyzed, pair, self._stoploss_range)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # If no trade found then exit
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if len(trades) == 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.info("No trades found.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Fill missing, calculable columns, profit, duration , abs etc.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trades_df = self._fill_calculable_fields(DataFrame(trades))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._cached_pairs = self._process_expectancy(trades_df)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._last_updated = int(dt_now().timestamp())
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def stake_amount(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pair: str, free_capital: float, total_capital: float, capital_in_trade: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stoploss = self.get_stoploss(pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         available_capital = (total_capital + capital_in_trade) * self._capital_ratio
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         allowed_capital_at_risk = available_capital * self._allowed_risk
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         max_position_size = abs(allowed_capital_at_risk / stoploss)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Position size must be below available capital.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         position_size = min(min(max_position_size, free_capital), available_capital)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if pair in self._cached_pairs:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.info(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "winrate: %s, expectancy: %s, position size: %s, pair: %s,"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 " capital in trade: %s, free capital: %s, total capital: %s,"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 " stoploss: %s, available capital: %s.",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._cached_pairs[pair].winrate,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._cached_pairs[pair].expectancy,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 position_size,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 pair,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 capital_in_trade,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 free_capital,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 total_capital,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 stoploss,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 available_capital,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return round(position_size, 15)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_stoploss(self, pair: str) -> float:
# REMOVED_UNUSED_CODE:         if pair in self._cached_pairs:
# REMOVED_UNUSED_CODE:             return self._cached_pairs[pair].stoploss
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 f"Tried to access stoploss of non-existing pair {pair}, "
# REMOVED_UNUSED_CODE:                 "strategy stoploss is returned instead."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             return self.strategy.stoploss
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def adjust(self, pairs: list[str]) -> list:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Filters out and sorts "pairs" according to Edge calculated pairs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         final = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for pair, info in self._cached_pairs.items():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 info.expectancy > float(self.edge_config.get("minimum_expectancy", 0.2))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 and info.winrate > float(self.edge_config.get("minimum_winrate", 0.60))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 and pair in pairs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 final.append(pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._final_pairs != final:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._final_pairs = final
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self._final_pairs:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.info(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "Minimum expectancy and minimum winrate are met only for %s,"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     " so other pairs are filtered out.",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     self._final_pairs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.info(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "Edge removed all pairs as no pair with minimum expectancy "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "and minimum winrate was found !"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._final_pairs
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def accepted_pairs(self) -> list[dict[str, Any]]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return a list of accepted pairs along with their winrate, expectancy and stoploss
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         final = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for pair, info in self._cached_pairs.items():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if info.expectancy > float(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.edge_config.get("minimum_expectancy", 0.2)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ) and info.winrate > float(self.edge_config.get("minimum_winrate", 0.60)):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 final.append(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         "Pair": pair,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         "Winrate": info.winrate,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         "Expectancy": info.expectancy,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         "Stoploss": info.stoploss,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return final
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _fill_calculable_fields(self, result: DataFrame) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         The result frame contains a number of columns that are calculable
# REMOVED_UNUSED_CODE:         from other columns. These are left blank till all rows are added,
# REMOVED_UNUSED_CODE:         to be populated in single vector calls.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         Columns to be populated are:
# REMOVED_UNUSED_CODE:         - Profit
# REMOVED_UNUSED_CODE:         - trade duration
# REMOVED_UNUSED_CODE:         - profit abs
# REMOVED_UNUSED_CODE:         :param result Dataframe
# REMOVED_UNUSED_CODE:         :return: result Dataframe
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # We set stake amount to an arbitrary amount, as it doesn't change the calculation.
# REMOVED_UNUSED_CODE:         # All returned values are relative, they are defined as ratios.
# REMOVED_UNUSED_CODE:         stake = 0.015
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         result["trade_duration"] = result["close_date"] - result["open_date"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         result["trade_duration"] = result["trade_duration"].map(
# REMOVED_UNUSED_CODE:             lambda x: int(x.total_seconds() / 60)
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Spends, Takes, Profit, Absolute Profit
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Buy Price
# REMOVED_UNUSED_CODE:         result["buy_vol"] = stake / result["open_rate"]  # How many target are we buying
# REMOVED_UNUSED_CODE:         result["buy_fee"] = stake * self.fee
# REMOVED_UNUSED_CODE:         result["buy_spend"] = stake + result["buy_fee"]  # How much we're spending
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Sell price
# REMOVED_UNUSED_CODE:         result["sell_sum"] = result["buy_vol"] * result["close_rate"]
# REMOVED_UNUSED_CODE:         result["sell_fee"] = result["sell_sum"] * self.fee
# REMOVED_UNUSED_CODE:         result["sell_take"] = result["sell_sum"] - result["sell_fee"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # profit_ratio
# REMOVED_UNUSED_CODE:         result["profit_ratio"] = (result["sell_take"] - result["buy_spend"]) / result["buy_spend"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Absolute profit
# REMOVED_UNUSED_CODE:         result["profit_abs"] = result["sell_take"] - result["buy_spend"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return result
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _process_expectancy(self, results: DataFrame) -> dict[str, Any]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         This calculates WinRate, Required Risk Reward, Risk Reward and Expectancy of all pairs
# REMOVED_UNUSED_CODE:         The calculation will be done per pair and per strategy.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Removing pairs having less than min_trades_number
# REMOVED_UNUSED_CODE:         min_trades_number = self.edge_config.get("min_trade_number", 10)
# REMOVED_UNUSED_CODE:         results = results.groupby(["pair", "stoploss"]).filter(lambda x: len(x) > min_trades_number)
# REMOVED_UNUSED_CODE:         ###################################
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Removing outliers (Only Pumps) from the dataset
# REMOVED_UNUSED_CODE:         # The method to detect outliers is to calculate standard deviation
# REMOVED_UNUSED_CODE:         # Then every value more than (standard deviation + 2*average) is out (pump)
# REMOVED_UNUSED_CODE:         #
# REMOVED_UNUSED_CODE:         # Removing Pumps
# REMOVED_UNUSED_CODE:         if self.edge_config.get("remove_pumps", False):
# REMOVED_UNUSED_CODE:             results = results[
# REMOVED_UNUSED_CODE:                 results["profit_abs"]
# REMOVED_UNUSED_CODE:                 < 2 * results["profit_abs"].std() + results["profit_abs"].mean()
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE:         ##########################################################################
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Removing trades having a duration more than X minutes (set in config)
# REMOVED_UNUSED_CODE:         max_trade_duration = self.edge_config.get("max_trade_duration_minute", 1440)
# REMOVED_UNUSED_CODE:         results = results[results.trade_duration < max_trade_duration]
# REMOVED_UNUSED_CODE:         #######################################################################
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if results.empty:
# REMOVED_UNUSED_CODE:             return {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         groupby_aggregator = {
# REMOVED_UNUSED_CODE:             "profit_abs": [
# REMOVED_UNUSED_CODE:                 ("nb_trades", "count"),  # number of all trades
# REMOVED_UNUSED_CODE:                 ("profit_sum", lambda x: x[x > 0].sum()),  # cumulative profit of all winning trades
# REMOVED_UNUSED_CODE:                 ("loss_sum", lambda x: abs(x[x < 0].sum())),  # cumulative loss of all losing trades
# REMOVED_UNUSED_CODE:                 ("nb_win_trades", lambda x: x[x > 0].count()),  # number of winning trades
# REMOVED_UNUSED_CODE:             ],
# REMOVED_UNUSED_CODE:             "trade_duration": [("avg_trade_duration", "mean")],
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Group by (pair and stoploss) by applying above aggregator
# REMOVED_UNUSED_CODE:         df = (
# REMOVED_UNUSED_CODE:             results.groupby(["pair", "stoploss"])[["profit_abs", "trade_duration"]]
# REMOVED_UNUSED_CODE:             .agg(groupby_aggregator)
# REMOVED_UNUSED_CODE:             .reset_index(col_level=1)
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Dropping level 0 as we don't need it
# REMOVED_UNUSED_CODE:         df.columns = df.columns.droplevel(0)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Calculating number of losing trades, average win and average loss
# REMOVED_UNUSED_CODE:         df["nb_loss_trades"] = df["nb_trades"] - df["nb_win_trades"]
# REMOVED_UNUSED_CODE:         df["average_win"] = np.where(
# REMOVED_UNUSED_CODE:             df["nb_win_trades"] == 0, 0.0, df["profit_sum"] / df["nb_win_trades"]
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         df["average_loss"] = np.where(
# REMOVED_UNUSED_CODE:             df["nb_loss_trades"] == 0, 0.0, df["loss_sum"] / df["nb_loss_trades"]
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Win rate = number of profitable trades / number of trades
# REMOVED_UNUSED_CODE:         df["winrate"] = df["nb_win_trades"] / df["nb_trades"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # risk_reward_ratio = average win / average loss
# REMOVED_UNUSED_CODE:         df["risk_reward_ratio"] = df["average_win"] / df["average_loss"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # required_risk_reward = (1 / winrate) - 1
# REMOVED_UNUSED_CODE:         df["required_risk_reward"] = (1 / df["winrate"]) - 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # expectancy = (risk_reward_ratio * winrate) - (lossrate)
# REMOVED_UNUSED_CODE:         df["expectancy"] = (df["risk_reward_ratio"] * df["winrate"]) - (1 - df["winrate"])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # sort by expectancy and stoploss
# REMOVED_UNUSED_CODE:         df = (
# REMOVED_UNUSED_CODE:             df.sort_values(by=["expectancy", "stoploss"], ascending=False)
# REMOVED_UNUSED_CODE:             .groupby("pair")
# REMOVED_UNUSED_CODE:             .first()
# REMOVED_UNUSED_CODE:             .sort_values(by=["expectancy"], ascending=False)
# REMOVED_UNUSED_CODE:             .reset_index()
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         final = {}
# REMOVED_UNUSED_CODE:         for x in df.itertuples():
# REMOVED_UNUSED_CODE:             final[x.pair] = PairInfo(
# REMOVED_UNUSED_CODE:                 x.stoploss,
# REMOVED_UNUSED_CODE:                 x.winrate,
# REMOVED_UNUSED_CODE:                 x.risk_reward_ratio,
# REMOVED_UNUSED_CODE:                 x.required_risk_reward,
# REMOVED_UNUSED_CODE:                 x.expectancy,
# REMOVED_UNUSED_CODE:                 x.nb_trades,
# REMOVED_UNUSED_CODE:                 x.avg_trade_duration,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Returning a list of pairs in order of "expectancy"
# REMOVED_UNUSED_CODE:         return final
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _find_trades_for_stoploss_range(self, df, pair: str, stoploss_range) -> list:
# REMOVED_UNUSED_CODE:         buy_column = df["enter_long"].values
# REMOVED_UNUSED_CODE:         sell_column = df["exit_long"].values
# REMOVED_UNUSED_CODE:         date_column = df["date"].values
# REMOVED_UNUSED_CODE:         ohlc_columns = df[["open", "high", "low", "close"]].values
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         result: list = []
# REMOVED_UNUSED_CODE:         for stoploss in stoploss_range:
# REMOVED_UNUSED_CODE:             result += self._detect_next_stop_or_sell_point(
# REMOVED_UNUSED_CODE:                 buy_column, sell_column, date_column, ohlc_columns, round(stoploss, 6), pair
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return result
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _detect_next_stop_or_sell_point(
# REMOVED_UNUSED_CODE:         self, buy_column, sell_column, date_column, ohlc_columns, stoploss, pair: str
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Iterate through ohlc_columns in order to find the next trade
# REMOVED_UNUSED_CODE:         Next trade opens from the first buy signal noticed to
# REMOVED_UNUSED_CODE:         The sell or stoploss signal after it.
# REMOVED_UNUSED_CODE:         It then cuts OHLC, buy_column, sell_column and date_column.
# REMOVED_UNUSED_CODE:         Cut from (the exit trade index) + 1.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         Author: https://github.com/mishaker
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         result: list = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         start_point = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         while True:
# REMOVED_UNUSED_CODE:             open_trade_index = utf1st.find_1st(buy_column, 1, utf1st.cmp_equal)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Return empty if we don't find trade entry (i.e. buy==1) or
# REMOVED_UNUSED_CODE:             # we find a buy but at the end of array
# REMOVED_UNUSED_CODE:             if open_trade_index == -1 or open_trade_index == len(buy_column) - 1:
# REMOVED_UNUSED_CODE:                 break
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 # When a buy signal is seen,
# REMOVED_UNUSED_CODE:                 # trade opens in reality on the next candle
# REMOVED_UNUSED_CODE:                 open_trade_index += 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             open_price = ohlc_columns[open_trade_index, 0]
# REMOVED_UNUSED_CODE:             stop_price = open_price * (stoploss + 1)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Searching for the index where stoploss is hit
# REMOVED_UNUSED_CODE:             stop_index = utf1st.find_1st(
# REMOVED_UNUSED_CODE:                 ohlc_columns[open_trade_index:, 2], stop_price, utf1st.cmp_smaller
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # If we don't find it then we assume stop_index will be far in future (infinite number)
# REMOVED_UNUSED_CODE:             if stop_index == -1:
# REMOVED_UNUSED_CODE:                 stop_index = float("inf")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Searching for the index where sell is hit
# REMOVED_UNUSED_CODE:             sell_index = utf1st.find_1st(sell_column[open_trade_index:], 1, utf1st.cmp_equal)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # If we don't find it then we assume sell_index will be far in future (infinite number)
# REMOVED_UNUSED_CODE:             if sell_index == -1:
# REMOVED_UNUSED_CODE:                 sell_index = float("inf")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Check if we don't find any stop or sell point (in that case trade remains open)
# REMOVED_UNUSED_CODE:             # It is not interesting for Edge to consider it so we simply ignore the trade
# REMOVED_UNUSED_CODE:             # And stop iterating there is no more entry
# REMOVED_UNUSED_CODE:             if stop_index == sell_index == float("inf"):
# REMOVED_UNUSED_CODE:                 break
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if stop_index <= sell_index:
# REMOVED_UNUSED_CODE:                 exit_index = open_trade_index + stop_index
# REMOVED_UNUSED_CODE:                 exit_type = ExitType.STOP_LOSS
# REMOVED_UNUSED_CODE:                 exit_price = stop_price
# REMOVED_UNUSED_CODE:             elif stop_index > sell_index:
# REMOVED_UNUSED_CODE:                 # If exit is SELL then we exit at the next candle
# REMOVED_UNUSED_CODE:                 exit_index = open_trade_index + sell_index + 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 # Check if we have the next candle
# REMOVED_UNUSED_CODE:                 if len(ohlc_columns) - 1 < exit_index:
# REMOVED_UNUSED_CODE:                     break
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 exit_type = ExitType.EXIT_SIGNAL
# REMOVED_UNUSED_CODE:                 exit_price = ohlc_columns[exit_index, 0]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             trade = {
# REMOVED_UNUSED_CODE:                 "pair": pair,
# REMOVED_UNUSED_CODE:                 "stoploss": stoploss,
# REMOVED_UNUSED_CODE:                 "profit_ratio": "",
# REMOVED_UNUSED_CODE:                 "profit_abs": "",
# REMOVED_UNUSED_CODE:                 "open_date": date_column[open_trade_index],
# REMOVED_UNUSED_CODE:                 "close_date": date_column[exit_index],
# REMOVED_UNUSED_CODE:                 "trade_duration": "",
# REMOVED_UNUSED_CODE:                 "open_rate": round(open_price, 15),
# REMOVED_UNUSED_CODE:                 "close_rate": round(exit_price, 15),
# REMOVED_UNUSED_CODE:                 "exit_type": exit_type,
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             result.append(trade)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Giving a view of exit_index till the end of array
# REMOVED_UNUSED_CODE:             buy_column = buy_column[exit_index:]
# REMOVED_UNUSED_CODE:             sell_column = sell_column[exit_index:]
# REMOVED_UNUSED_CODE:             date_column = date_column[exit_index:]
# REMOVED_UNUSED_CODE:             ohlc_columns = ohlc_columns[exit_index:]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             start_point += exit_index
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return result
