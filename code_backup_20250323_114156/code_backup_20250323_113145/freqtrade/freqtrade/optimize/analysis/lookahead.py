import logging
# REMOVED_UNUSED_CODE: import shutil
# REMOVED_UNUSED_CODE: from copy import deepcopy
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import datetime, timedelta
# REMOVED_UNUSED_CODE: from pathlib import Path
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: from pandas import DataFrame

# REMOVED_UNUSED_CODE: from freqtrade.data.history import get_timerange
# REMOVED_UNUSED_CODE: from freqtrade.exchange import timeframe_to_minutes
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.loggers.set_log_levels import (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     reduce_verbosity_for_bias_tester,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     restore_verbosity_for_bias_tester,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: )
# REMOVED_UNUSED_CODE: from freqtrade.optimize.backtesting import Backtesting
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.optimize.base_analysis import BaseAnalysis, VarHolder


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Analysis:
# REMOVED_UNUSED_CODE:     def __init__(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.total_signals = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.false_entry_signals = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.false_exit_signals = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.false_indicators: list[str] = []
# REMOVED_UNUSED_CODE:         self.has_bias = False


# REMOVED_UNUSED_CODE: class LookaheadAnalysis(BaseAnalysis):
# REMOVED_UNUSED_CODE:     def __init__(self, config: dict[str, Any], strategy_obj: dict):
# REMOVED_UNUSED_CODE:         super().__init__(config, strategy_obj)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.entry_varHolders: list[VarHolder] = []
# REMOVED_UNUSED_CODE:         self.exit_varHolders: list[VarHolder] = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.current_analysis = Analysis()
# REMOVED_UNUSED_CODE:         self.minimum_trade_amount = config["minimum_trade_amount"]
# REMOVED_UNUSED_CODE:         self.targeted_trade_amount = config["targeted_trade_amount"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def get_result(backtesting: Backtesting, processed: DataFrame):
# REMOVED_UNUSED_CODE:         min_date, max_date = get_timerange(processed)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         result = backtesting.backtest(
# REMOVED_UNUSED_CODE:             processed=deepcopy(processed), start_date=min_date, end_date=max_date
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         return result
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def report_signal(result: dict, column_name: str, checked_timestamp: datetime):
# REMOVED_UNUSED_CODE:         df = result["results"]
# REMOVED_UNUSED_CODE:         row_count = df[column_name].shape[0]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if row_count == 0:
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             df_cut = df[(df[column_name] == checked_timestamp)]
# REMOVED_UNUSED_CODE:             if df_cut[column_name].shape[0] == 0:
# REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 return True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # analyzes two data frames with processed indicators and shows differences between them.
# REMOVED_UNUSED_CODE:     def analyze_indicators(self, full_vars: VarHolder, cut_vars: VarHolder, current_pair: str):
# REMOVED_UNUSED_CODE:         # extract dataframes
# REMOVED_UNUSED_CODE:         cut_df: DataFrame = cut_vars.indicators[current_pair]
# REMOVED_UNUSED_CODE:         full_df: DataFrame = full_vars.indicators[current_pair]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # cut longer dataframe to length of the shorter
# REMOVED_UNUSED_CODE:         full_df_cut = full_df[(full_df.date == cut_vars.compared_dt)].reset_index(drop=True)
# REMOVED_UNUSED_CODE:         cut_df_cut = cut_df[(cut_df.date == cut_vars.compared_dt)].reset_index(drop=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # check if dataframes are not empty
# REMOVED_UNUSED_CODE:         if full_df_cut.shape[0] != 0 and cut_df_cut.shape[0] != 0:
# REMOVED_UNUSED_CODE:             # compare dataframes
# REMOVED_UNUSED_CODE:             compare_df = full_df_cut.compare(cut_df_cut)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if compare_df.shape[0] > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 for col_name, values in compare_df.items():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     col_idx = compare_df.columns.get_loc(col_name)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     compare_df_row = compare_df.iloc[0]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     # compare_df now comprises tuples with [1] having either 'self' or 'other'
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     if "other" in col_name[1]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     self_value = compare_df_row.iloc[col_idx]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     other_value = compare_df_row.iloc[col_idx + 1]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     # output differences
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     if self_value != other_value:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         if not self.current_analysis.false_indicators.__contains__(col_name[0]):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             self.current_analysis.false_indicators.append(col_name[0])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             logger.info(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 f"=> found look ahead bias in indicator "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 f"{col_name[0]}. "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 f"{str(self_value)} != {str(other_value)}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             )
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
# REMOVED_UNUSED_CODE:         if self._fee is not None:
# REMOVED_UNUSED_CODE:             # Don't re-calculate fee per pair, as fee might differ per pair.
# REMOVED_UNUSED_CODE:             prepare_data_config["fee"] = self._fee
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         backtesting = Backtesting(prepare_data_config, self.exchange)
# REMOVED_UNUSED_CODE:         self.exchange = backtesting.exchange
# REMOVED_UNUSED_CODE:         self._fee = backtesting.fee
# REMOVED_UNUSED_CODE:         backtesting._set_strategy(backtesting.strategylist[0])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         varholder.data, varholder.timerange = backtesting.load_bt_data()
# REMOVED_UNUSED_CODE:         backtesting.load_bt_data_detail()
# REMOVED_UNUSED_CODE:         varholder.timeframe = backtesting.timeframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         varholder.indicators = backtesting.strategy.advise_all_indicators(varholder.data)
# REMOVED_UNUSED_CODE:         varholder.result = self.get_result(backtesting, varholder.indicators)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fill_entry_and_exit_varHolders(self, result_row):
# REMOVED_UNUSED_CODE:         # entry_varHolder
# REMOVED_UNUSED_CODE:         entry_varHolder = VarHolder()
# REMOVED_UNUSED_CODE:         self.entry_varHolders.append(entry_varHolder)
# REMOVED_UNUSED_CODE:         entry_varHolder.from_dt = self.full_varHolder.from_dt
# REMOVED_UNUSED_CODE:         entry_varHolder.compared_dt = result_row["open_date"]
# REMOVED_UNUSED_CODE:         # to_dt needs +1 candle since it won't buy on the last candle
# REMOVED_UNUSED_CODE:         entry_varHolder.to_dt = result_row["open_date"] + timedelta(
# REMOVED_UNUSED_CODE:             minutes=timeframe_to_minutes(self.full_varHolder.timeframe)
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         self.prepare_data(entry_varHolder, [result_row["pair"]])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # exit_varHolder
# REMOVED_UNUSED_CODE:         exit_varHolder = VarHolder()
# REMOVED_UNUSED_CODE:         self.exit_varHolders.append(exit_varHolder)
# REMOVED_UNUSED_CODE:         # to_dt needs +1 candle since it will always exit/force-exit trades on the last candle
# REMOVED_UNUSED_CODE:         exit_varHolder.from_dt = self.full_varHolder.from_dt
# REMOVED_UNUSED_CODE:         exit_varHolder.to_dt = result_row["close_date"] + timedelta(
# REMOVED_UNUSED_CODE:             minutes=timeframe_to_minutes(self.full_varHolder.timeframe)
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         exit_varHolder.compared_dt = result_row["close_date"]
# REMOVED_UNUSED_CODE:         self.prepare_data(exit_varHolder, [result_row["pair"]])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # now we analyze a full trade of full_varholder and look for analyze its bias
# REMOVED_UNUSED_CODE:     def analyze_row(self, idx: int, result_row):
# REMOVED_UNUSED_CODE:         # if force-sold, ignore this signal since here it will unconditionally exit.
# REMOVED_UNUSED_CODE:         if result_row.close_date == self.dt_to_timestamp(self.full_varHolder.to_dt):
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # keep track of how many signals are processed at total
# REMOVED_UNUSED_CODE:         self.current_analysis.total_signals += 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # fill entry_varHolder and exit_varHolder
# REMOVED_UNUSED_CODE:         self.fill_entry_and_exit_varHolders(result_row)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # this will trigger a logger-message
# REMOVED_UNUSED_CODE:         buy_or_sell_biased: bool = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # register if buy signal is broken
# REMOVED_UNUSED_CODE:         if not self.report_signal(
# REMOVED_UNUSED_CODE:             self.entry_varHolders[idx].result, "open_date", self.entry_varHolders[idx].compared_dt
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             self.current_analysis.false_entry_signals += 1
# REMOVED_UNUSED_CODE:             buy_or_sell_biased = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # register if buy or sell signal is broken
# REMOVED_UNUSED_CODE:         if not self.report_signal(
# REMOVED_UNUSED_CODE:             self.exit_varHolders[idx].result, "close_date", self.exit_varHolders[idx].compared_dt
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             self.current_analysis.false_exit_signals += 1
# REMOVED_UNUSED_CODE:             buy_or_sell_biased = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if buy_or_sell_biased:
# REMOVED_UNUSED_CODE:             logger.info(
# REMOVED_UNUSED_CODE:                 f"found lookahead-bias in trade "
# REMOVED_UNUSED_CODE:                 f"pair: {result_row['pair']}, "
# REMOVED_UNUSED_CODE:                 f"timerange:{result_row['open_date']} - {result_row['close_date']}, "
# REMOVED_UNUSED_CODE:                 f"idx: {idx}"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # check if the indicators themselves contain biased data
# REMOVED_UNUSED_CODE:         self.analyze_indicators(self.full_varHolder, self.entry_varHolders[idx], result_row["pair"])
# REMOVED_UNUSED_CODE:         self.analyze_indicators(self.full_varHolder, self.exit_varHolders[idx], result_row["pair"])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def start(self) -> None:
# REMOVED_UNUSED_CODE:         super().start()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         reduce_verbosity_for_bias_tester()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # check if requirements have been met of full_varholder
# REMOVED_UNUSED_CODE:         found_signals: int = self.full_varHolder.result["results"].shape[0] + 1
# REMOVED_UNUSED_CODE:         if found_signals >= self.targeted_trade_amount:
# REMOVED_UNUSED_CODE:             logger.info(
# REMOVED_UNUSED_CODE:                 f"Found {found_signals} trades, calculating {self.targeted_trade_amount} trades."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         elif self.targeted_trade_amount >= found_signals >= self.minimum_trade_amount:
# REMOVED_UNUSED_CODE:             logger.info(f"Only found {found_signals} trades. Calculating all available trades.")
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.info(
# REMOVED_UNUSED_CODE:                 f"found {found_signals} trades "
# REMOVED_UNUSED_CODE:                 f"which is less than minimum_trade_amount {self.minimum_trade_amount}. "
# REMOVED_UNUSED_CODE:                 f"Cancelling this backtest lookahead bias test."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # now we loop through all signals
# REMOVED_UNUSED_CODE:         # starting from the same datetime to avoid miss-reports of bias
# REMOVED_UNUSED_CODE:         for idx, result_row in self.full_varHolder.result["results"].iterrows():
# REMOVED_UNUSED_CODE:             if self.current_analysis.total_signals == self.targeted_trade_amount:
# REMOVED_UNUSED_CODE:                 logger.info(f"Found targeted trade amount = {self.targeted_trade_amount} signals.")
# REMOVED_UNUSED_CODE:                 break
# REMOVED_UNUSED_CODE:             if found_signals < self.minimum_trade_amount:
# REMOVED_UNUSED_CODE:                 logger.info(
# REMOVED_UNUSED_CODE:                     f"only found {found_signals} "
# REMOVED_UNUSED_CODE:                     f"which is smaller than "
# REMOVED_UNUSED_CODE:                     f"minimum trade amount = {self.minimum_trade_amount}. "
# REMOVED_UNUSED_CODE:                     f"Exiting this lookahead-analysis"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 return None
# REMOVED_UNUSED_CODE:             if "force_exit" in result_row["exit_reason"]:
# REMOVED_UNUSED_CODE:                 logger.info(
# REMOVED_UNUSED_CODE:                     "found force-exit in pair: {result_row['pair']}, "
# REMOVED_UNUSED_CODE:                     f"timerange:{result_row['open_date']}-{result_row['close_date']}, "
# REMOVED_UNUSED_CODE:                     f"idx: {idx}, skipping this one to avoid a false-positive."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 # just to keep the IDs of both full, entry and exit varholders the same
# REMOVED_UNUSED_CODE:                 # to achieve a better debugging experience
# REMOVED_UNUSED_CODE:                 self.entry_varHolders.append(VarHolder())
# REMOVED_UNUSED_CODE:                 self.exit_varHolders.append(VarHolder())
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.analyze_row(idx, result_row)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if len(self.entry_varHolders) < self.minimum_trade_amount:
# REMOVED_UNUSED_CODE:             logger.info(
# REMOVED_UNUSED_CODE:                 f"only found {found_signals} after skipping forced exits "
# REMOVED_UNUSED_CODE:                 f"which is smaller than "
# REMOVED_UNUSED_CODE:                 f"minimum trade amount = {self.minimum_trade_amount}. "
# REMOVED_UNUSED_CODE:                 f"Exiting this lookahead-analysis"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Restore verbosity, so it's not too quiet for the next strategy
# REMOVED_UNUSED_CODE:         restore_verbosity_for_bias_tester()
# REMOVED_UNUSED_CODE:         # check and report signals
# REMOVED_UNUSED_CODE:         if self.current_analysis.total_signals < self.local_config["minimum_trade_amount"]:
# REMOVED_UNUSED_CODE:             logger.info(
# REMOVED_UNUSED_CODE:                 f" -> {self.local_config['strategy']} : too few trades. "
# REMOVED_UNUSED_CODE:                 f"We only found {self.current_analysis.total_signals} trades. "
# REMOVED_UNUSED_CODE:                 f"Hint: Extend the timerange "
# REMOVED_UNUSED_CODE:                 f"to get at least {self.local_config['minimum_trade_amount']} "
# REMOVED_UNUSED_CODE:                 f"or lower the value of minimum_trade_amount."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.failed_bias_check = True
# REMOVED_UNUSED_CODE:         elif (
# REMOVED_UNUSED_CODE:             self.current_analysis.false_entry_signals > 0
# REMOVED_UNUSED_CODE:             or self.current_analysis.false_exit_signals > 0
# REMOVED_UNUSED_CODE:             or len(self.current_analysis.false_indicators) > 0
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             logger.info(f" => {self.local_config['strategy']} : bias detected!")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.current_analysis.has_bias = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.failed_bias_check = False
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.info(self.local_config["strategy"] + ": no bias detected")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.failed_bias_check = False
