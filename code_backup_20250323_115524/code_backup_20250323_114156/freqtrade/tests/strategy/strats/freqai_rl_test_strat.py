import logging
# REMOVED_UNUSED_CODE: from functools import reduce

# REMOVED_UNUSED_CODE: import talib.abstract as ta
# REMOVED_UNUSED_CODE: from pandas import DataFrame

from freqtrade.strategy import IStrategy


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


class freqai_rl_test_strat(IStrategy):
    """
    Test strategy - used for testing freqAI functionalities.
    DO not use in production.
    """

# REMOVED_UNUSED_CODE:     minimal_roi = {"0": 0.1, "240": -1}

# REMOVED_UNUSED_CODE:     process_only_new_candles = True
# REMOVED_UNUSED_CODE:     stoploss = -0.05
# REMOVED_UNUSED_CODE:     use_exit_signal = True
# REMOVED_UNUSED_CODE:     startup_candle_count: int = 300
# REMOVED_UNUSED_CODE:     can_short = False

# REMOVED_UNUSED_CODE:     def feature_engineering_expand_all(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, dataframe: DataFrame, period: int, metadata: dict, **kwargs
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         dataframe["%-rsi-period"] = ta.RSI(dataframe, timeperiod=period)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def feature_engineering_expand_basic(self, dataframe: DataFrame, metadata: dict, **kwargs):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-pct-change"] = dataframe["close"].pct_change()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-raw_volume"] = dataframe["volume"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def feature_engineering_standard(self, dataframe: DataFrame, metadata: dict, **kwargs):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-day_of_week"] = dataframe["date"].dt.dayofweek
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-hour_of_day"] = dataframe["date"].dt.hour
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-raw_close"] = dataframe["close"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-raw_open"] = dataframe["open"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-raw_high"] = dataframe["high"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-raw_low"] = dataframe["low"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def set_freqai_targets(self, dataframe: DataFrame, metadata: dict, **kwargs):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["&-action"] = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE:     def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         dataframe = self.freqai.start(dataframe, metadata, self)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE:     def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         enter_long_conditions = [df["do_predict"] == 1, df["&-action"] == 1]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if enter_long_conditions:
# REMOVED_UNUSED_CODE:             df.loc[
# REMOVED_UNUSED_CODE:                 reduce(lambda x, y: x & y, enter_long_conditions), ["enter_long", "enter_tag"]
# REMOVED_UNUSED_CODE:             ] = (1, "long")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         enter_short_conditions = [df["do_predict"] == 1, df["&-action"] == 3]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if enter_short_conditions:
# REMOVED_UNUSED_CODE:             df.loc[
# REMOVED_UNUSED_CODE:                 reduce(lambda x, y: x & y, enter_short_conditions), ["enter_short", "enter_tag"]
# REMOVED_UNUSED_CODE:             ] = (1, "short")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return df

# REMOVED_UNUSED_CODE:     def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         exit_long_conditions = [df["do_predict"] == 1, df["&-action"] == 2]
# REMOVED_UNUSED_CODE:         if exit_long_conditions:
# REMOVED_UNUSED_CODE:             df.loc[reduce(lambda x, y: x & y, exit_long_conditions), "exit_long"] = 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         exit_short_conditions = [df["do_predict"] == 1, df["&-action"] == 4]
# REMOVED_UNUSED_CODE:         if exit_short_conditions:
# REMOVED_UNUSED_CODE:             df.loc[reduce(lambda x, y: x & y, exit_short_conditions), "exit_short"] = 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return df
