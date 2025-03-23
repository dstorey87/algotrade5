import logging
# REMOVED_UNUSED_CODE: import numbers
# REMOVED_UNUSED_CODE: import shutil
# REMOVED_UNUSED_CODE: from copy import deepcopy
# REMOVED_UNUSED_CODE: from datetime import timedelta
# REMOVED_UNUSED_CODE: from pathlib import Path
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: from pandas import DataFrame

# REMOVED_UNUSED_CODE: from freqtrade.exchange import timeframe_to_minutes
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.loggers.set_log_levels import (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     reduce_verbosity_for_bias_tester,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     restore_verbosity_for_bias_tester,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: )
# REMOVED_UNUSED_CODE: from freqtrade.optimize.backtesting import Backtesting
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.optimize.base_analysis import BaseAnalysis, VarHolder
# REMOVED_UNUSED_CODE: from freqtrade.resolvers import StrategyResolver


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: def is_number(variable):
# REMOVED_UNUSED_CODE:     return isinstance(variable, numbers.Number) and not isinstance(variable, bool)


# REMOVED_UNUSED_CODE: class RecursiveAnalysis(BaseAnalysis):
# REMOVED_UNUSED_CODE:     def __init__(self, config: dict[str, Any], strategy_obj: dict):
# REMOVED_UNUSED_CODE:         self._startup_candle = list(
# REMOVED_UNUSED_CODE:             map(int, config.get("startup_candle", [199, 399, 499, 999, 1999]))
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         super().__init__(config, strategy_obj)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         strat = StrategyResolver.load_strategy(config)
# REMOVED_UNUSED_CODE:         self._strat_scc = strat.startup_candle_count
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._strat_scc not in self._startup_candle:
# REMOVED_UNUSED_CODE:             self._startup_candle.append(self._strat_scc)
# REMOVED_UNUSED_CODE:         self._startup_candle.sort()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.partial_varHolder_array: list[VarHolder] = []
# REMOVED_UNUSED_CODE:         self.partial_varHolder_lookahead_array: list[VarHolder] = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.dict_recursive: dict[str, Any] = dict()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # For recursive bias check
# REMOVED_UNUSED_CODE:     # analyzes two data frames with processed indicators and shows differences between them.
# REMOVED_UNUSED_CODE:     def analyze_indicators(self):
# REMOVED_UNUSED_CODE:         pair_to_check = self.local_config["pairs"][0]
# REMOVED_UNUSED_CODE:         logger.info("Start checking for recursive bias")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # check and report signals
# REMOVED_UNUSED_CODE:         base_last_row = self.full_varHolder.indicators[pair_to_check].iloc[-1]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for part in self.partial_varHolder_array:
# REMOVED_UNUSED_CODE:             part_last_row = part.indicators[pair_to_check].iloc[-1]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             compare_df = base_last_row.compare(part_last_row)
# REMOVED_UNUSED_CODE:             if compare_df.shape[0] > 0:
# REMOVED_UNUSED_CODE:                 # print(compare_df)
# REMOVED_UNUSED_CODE:                 for col_name, values in compare_df.items():
# REMOVED_UNUSED_CODE:                     # print(col_name)
# REMOVED_UNUSED_CODE:                     if "other" == col_name:
# REMOVED_UNUSED_CODE:                         continue
# REMOVED_UNUSED_CODE:                     indicators = values.index
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                     for indicator in indicators:
# REMOVED_UNUSED_CODE:                         if indicator not in self.dict_recursive:
# REMOVED_UNUSED_CODE:                             self.dict_recursive[indicator] = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                         values_diff = compare_df.loc[indicator]
# REMOVED_UNUSED_CODE:                         values_diff_self = values_diff.loc["self"]
# REMOVED_UNUSED_CODE:                         values_diff_other = values_diff.loc["other"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                         if (
# REMOVED_UNUSED_CODE:                             values_diff_self
# REMOVED_UNUSED_CODE:                             and values_diff_other
# REMOVED_UNUSED_CODE:                             and is_number(values_diff_self)
# REMOVED_UNUSED_CODE:                             and is_number(values_diff_other)
# REMOVED_UNUSED_CODE:                         ):
# REMOVED_UNUSED_CODE:                             diff = (values_diff_other - values_diff_self) / values_diff_self * 100
# REMOVED_UNUSED_CODE:                             str_diff = f"{diff:.3f}%"
# REMOVED_UNUSED_CODE:                         else:
# REMOVED_UNUSED_CODE:                             str_diff = "NaN"
# REMOVED_UNUSED_CODE:                         self.dict_recursive[indicator][part.startup_candle] = str_diff
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 logger.info("No variance on indicator(s) found due to recursive formula.")
# REMOVED_UNUSED_CODE:                 break
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # For lookahead bias check
# REMOVED_UNUSED_CODE:     # analyzes two data frames with processed indicators and shows differences between them.
# REMOVED_UNUSED_CODE:     def analyze_indicators_lookahead(self):
# REMOVED_UNUSED_CODE:         pair_to_check = self.local_config["pairs"][0]
# REMOVED_UNUSED_CODE:         logger.info("Start checking for lookahead bias on indicators only")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         part = self.partial_varHolder_lookahead_array[0]
# REMOVED_UNUSED_CODE:         part_last_row = part.indicators[pair_to_check].iloc[-1]
# REMOVED_UNUSED_CODE:         date_to_check = part_last_row["date"]
# REMOVED_UNUSED_CODE:         index_to_get = self.full_varHolder.indicators[pair_to_check]["date"] == date_to_check
# REMOVED_UNUSED_CODE:         base_row_check = self.full_varHolder.indicators[pair_to_check].loc[index_to_get].iloc[-1]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         check_time = part.to_dt.strftime("%Y-%m-%dT%H:%M:%S")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.info(f"Check indicators at {check_time}")
# REMOVED_UNUSED_CODE:         # logger.info(f"vs {part_timerange} with {part.startup_candle} startup candle")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         compare_df = base_row_check.compare(part_last_row)
# REMOVED_UNUSED_CODE:         if compare_df.shape[0] > 0:
# REMOVED_UNUSED_CODE:             # print(compare_df)
# REMOVED_UNUSED_CODE:             for col_name, values in compare_df.items():
# REMOVED_UNUSED_CODE:                 # print(col_name)
# REMOVED_UNUSED_CODE:                 if "other" == col_name:
# REMOVED_UNUSED_CODE:                     continue
# REMOVED_UNUSED_CODE:                 indicators = values.index
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 for indicator in indicators:
# REMOVED_UNUSED_CODE:                     logger.info(f"=> found lookahead in indicator {indicator}")
# REMOVED_UNUSED_CODE:                     # logger.info("base value {:.5f}".format(values_diff_self))
# REMOVED_UNUSED_CODE:                     # logger.info("part value {:.5f}".format(values_diff_other))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.info("No lookahead bias on indicators found.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def prepare_data(self, varholder: VarHolder, pairs_to_load: list[DataFrame]):
# REMOVED_UNUSED_CODE:         if "freqai" in self.local_config and "identifier" in self.local_config["freqai"]:
# REMOVED_UNUSED_CODE:             # purge previous data if the freqai model is defined
# REMOVED_UNUSED_CODE:             # (to be sure nothing is carried over from older backtests)
# REMOVED_UNUSED_CODE:             path_to_current_identifier = Path(
# REMOVED_UNUSED_CODE:                 f"{self.local_config['user_data_dir']}/models/"
# REMOVED_UNUSED_CODE:                 f"{self.local_config['freqai']['identifier']}"
# REMOVED_UNUSED_CODE:             ).resolve()
# REMOVED_UNUSED_CODE:             # remove folder and its contents
# REMOVED_UNUSED_CODE:             if Path.exists(path_to_current_identifier):
# REMOVED_UNUSED_CODE:                 shutil.rmtree(path_to_current_identifier)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         prepare_data_config = deepcopy(self.local_config)
# REMOVED_UNUSED_CODE:         prepare_data_config["timerange"] = (
# REMOVED_UNUSED_CODE:             str(self.dt_to_timestamp(varholder.from_dt))
# REMOVED_UNUSED_CODE:             + "-"
# REMOVED_UNUSED_CODE:             + str(self.dt_to_timestamp(varholder.to_dt))
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         prepare_data_config["exchange"]["pair_whitelist"] = pairs_to_load
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         backtesting = Backtesting(prepare_data_config, self.exchange)
# REMOVED_UNUSED_CODE:         self.exchange = backtesting.exchange
# REMOVED_UNUSED_CODE:         backtesting._set_strategy(backtesting.strategylist[0])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         varholder.data, varholder.timerange = backtesting.load_bt_data()
# REMOVED_UNUSED_CODE:         backtesting.load_bt_data_detail()
# REMOVED_UNUSED_CODE:         varholder.timeframe = backtesting.timeframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         varholder.indicators = backtesting.strategy.advise_all_indicators(varholder.data)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fill_partial_varholder(self, start_date, startup_candle):
# REMOVED_UNUSED_CODE:         logger.info(f"Calculating indicators using startup candle of {startup_candle}.")
# REMOVED_UNUSED_CODE:         partial_varHolder = VarHolder()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         partial_varHolder.from_dt = start_date
# REMOVED_UNUSED_CODE:         partial_varHolder.to_dt = self.full_varHolder.to_dt
# REMOVED_UNUSED_CODE:         partial_varHolder.startup_candle = startup_candle
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.local_config["startup_candle_count"] = startup_candle
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.prepare_data(partial_varHolder, self.local_config["pairs"])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.partial_varHolder_array.append(partial_varHolder)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fill_partial_varholder_lookahead(self, end_date):
# REMOVED_UNUSED_CODE:         logger.info("Calculating indicators to test lookahead on indicators.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         partial_varHolder = VarHolder()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         partial_varHolder.from_dt = self.full_varHolder.from_dt
# REMOVED_UNUSED_CODE:         partial_varHolder.to_dt = end_date
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.prepare_data(partial_varHolder, self.local_config["pairs"])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.partial_varHolder_lookahead_array.append(partial_varHolder)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def start(self) -> None:
# REMOVED_UNUSED_CODE:         super().start()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         reduce_verbosity_for_bias_tester()
# REMOVED_UNUSED_CODE:         start_date_full = self.full_varHolder.from_dt
# REMOVED_UNUSED_CODE:         end_date_full = self.full_varHolder.to_dt
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         timeframe_minutes = timeframe_to_minutes(self.full_varHolder.timeframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         end_date_partial = start_date_full + timedelta(minutes=int(timeframe_minutes * 10))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.fill_partial_varholder_lookahead(end_date_partial)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # restore_verbosity_for_bias_tester()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         start_date_partial = end_date_full - timedelta(minutes=int(timeframe_minutes))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for startup_candle in self._startup_candle:
# REMOVED_UNUSED_CODE:             self.fill_partial_varholder(start_date_partial, startup_candle)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Restore verbosity, so it's not too quiet for the next strategy
# REMOVED_UNUSED_CODE:         restore_verbosity_for_bias_tester()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.analyze_indicators()
# REMOVED_UNUSED_CODE:         self.analyze_indicators_lookahead()
