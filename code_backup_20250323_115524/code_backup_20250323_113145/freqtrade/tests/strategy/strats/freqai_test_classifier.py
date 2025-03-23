import logging
# REMOVED_UNUSED_CODE: from functools import reduce

# REMOVED_UNUSED_CODE: import numpy as np
# REMOVED_UNUSED_CODE: import talib.abstract as ta
# REMOVED_UNUSED_CODE: from pandas import DataFrame

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.strategy import DecimalParameter, IntParameter, IStrategy


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


class freqai_test_classifier(IStrategy):
    """
    Test strategy - used for testing freqAI functionalities.
    DO not use in production.
    """

# REMOVED_UNUSED_CODE:     minimal_roi = {"0": 0.1, "240": -1}

# REMOVED_UNUSED_CODE:     plot_config = {
# REMOVED_UNUSED_CODE:         "main_plot": {},
# REMOVED_UNUSED_CODE:         "subplots": {
# REMOVED_UNUSED_CODE:             "prediction": {"prediction": {"color": "blue"}},
# REMOVED_UNUSED_CODE:             "target_roi": {
# REMOVED_UNUSED_CODE:                 "target_roi": {"color": "brown"},
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "do_predict": {
# REMOVED_UNUSED_CODE:                 "do_predict": {"color": "brown"},
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:     }

# REMOVED_UNUSED_CODE:     process_only_new_candles = True
# REMOVED_UNUSED_CODE:     stoploss = -0.05
# REMOVED_UNUSED_CODE:     use_exit_signal = True
# REMOVED_UNUSED_CODE:     startup_candle_count: int = 300
# REMOVED_UNUSED_CODE:     can_short = False

# REMOVED_UNUSED_CODE:     linear_roi_offset = DecimalParameter(
# REMOVED_UNUSED_CODE:         0.00, 0.02, default=0.005, space="sell", optimize=False, load=True
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     max_roi_time_long = IntParameter(0, 800, default=400, space="sell", optimize=False, load=True)

    def informative_pairs(self):
        whitelist_pairs = self.dp.current_whitelist()
        corr_pairs = self.config["freqai"]["feature_parameters"]["include_corr_pairlist"]
        informative_pairs = []
        for tf in self.config["freqai"]["feature_parameters"]["include_timeframes"]:
            for pair in whitelist_pairs:
                informative_pairs.append((pair, tf))
            for pair in corr_pairs:
                if pair in whitelist_pairs:
                    continue  # avoid duplication
                informative_pairs.append((pair, tf))
        return informative_pairs

# REMOVED_UNUSED_CODE:     def feature_engineering_expand_all(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, dataframe: DataFrame, period: int, metadata: dict, **kwargs
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         dataframe["%-rsi-period"] = ta.RSI(dataframe, timeperiod=period)
# REMOVED_UNUSED_CODE:         dataframe["%-mfi-period"] = ta.MFI(dataframe, timeperiod=period)
# REMOVED_UNUSED_CODE:         dataframe["%-adx-period"] = ta.ADX(dataframe, timeperiod=period)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def feature_engineering_expand_basic(self, dataframe: DataFrame, metadata: dict, **kwargs):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-pct-change"] = dataframe["close"].pct_change()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-raw_volume"] = dataframe["volume"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-raw_price"] = dataframe["close"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def feature_engineering_standard(self, dataframe: DataFrame, metadata: dict, **kwargs):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-day_of_week"] = dataframe["date"].dt.dayofweek
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-hour_of_day"] = dataframe["date"].dt.hour
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def set_freqai_targets(self, dataframe: DataFrame, metadata: dict, **kwargs):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.freqai.class_names = ["down", "up"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["&s-up_or_down"] = np.where(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe["close"].shift(-100) > dataframe["close"], "up", "down"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE:     def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.freqai_info = self.config["freqai"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         dataframe = self.freqai.start(dataframe, metadata, self)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE:     def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         enter_long_conditions = [df["&s-up_or_down"] == "up"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if enter_long_conditions:
# REMOVED_UNUSED_CODE:             df.loc[
# REMOVED_UNUSED_CODE:                 reduce(lambda x, y: x & y, enter_long_conditions), ["enter_long", "enter_tag"]
# REMOVED_UNUSED_CODE:             ] = (1, "long")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         enter_short_conditions = [df["&s-up_or_down"] == "down"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if enter_short_conditions:
# REMOVED_UNUSED_CODE:             df.loc[
# REMOVED_UNUSED_CODE:                 reduce(lambda x, y: x & y, enter_short_conditions), ["enter_short", "enter_tag"]
# REMOVED_UNUSED_CODE:             ] = (1, "short")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return df

# REMOVED_UNUSED_CODE:     def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         return df
