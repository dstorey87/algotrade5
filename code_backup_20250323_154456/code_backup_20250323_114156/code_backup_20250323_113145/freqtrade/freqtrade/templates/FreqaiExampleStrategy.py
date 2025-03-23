import logging
from functools import reduce

import talib.abstract as ta
from pandas import DataFrame
from technical import qtpylib

from freqtrade.strategy import IStrategy


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class FreqaiExampleStrategy(IStrategy):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Example strategy showing how the user connects their own
# REMOVED_UNUSED_CODE:     IFreqaiModel to the strategy.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Warning! This is a showcase of functionality,
# REMOVED_UNUSED_CODE:     which means that it is designed to show various functions of FreqAI
# REMOVED_UNUSED_CODE:     and it runs on all computers. We use this showcase to help users
# REMOVED_UNUSED_CODE:     understand how to build a strategy, and we use it as a benchmark
# REMOVED_UNUSED_CODE:     to help debug possible problems.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     This means this is *not* meant to be run live in production.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     minimal_roi = {"0": 0.1, "240": -1}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     plot_config = {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         "main_plot": {},
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         "subplots": {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "&-s_close": {"&-s_close": {"color": "blue"}},
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "do_predict": {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "do_predict": {"color": "brown"},
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     process_only_new_candles = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stoploss = -0.05
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     use_exit_signal = True
# REMOVED_UNUSED_CODE:     # this is the maximum period fed to talib (timeframe independent)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     startup_candle_count: int = 40
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     can_short = True
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Access metadata such as the current pair/timeframe with:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         `metadata["pair"]` `metadata["tf"]`
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-rsi-period"] = ta.RSI(dataframe, timeperiod=period)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-mfi-period"] = ta.MFI(dataframe, timeperiod=period)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-adx-period"] = ta.ADX(dataframe, timeperiod=period)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-sma-period"] = ta.SMA(dataframe, timeperiod=period)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-ema-period"] = ta.EMA(dataframe, timeperiod=period)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         bollinger = qtpylib.bollinger_bands(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             qtpylib.typical_price(dataframe), window=period, stds=2.2
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["bb_lowerband-period"] = bollinger["lower"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["bb_middleband-period"] = bollinger["mid"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["bb_upperband-period"] = bollinger["upper"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-bb_width-period"] = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe["bb_upperband-period"] - dataframe["bb_lowerband-period"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ) / dataframe["bb_middleband-period"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-close-bb_lower-period"] = dataframe["close"] / dataframe["bb_lowerband-period"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-roc-period"] = ta.ROC(dataframe, timeperiod=period)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-relative_volume-period"] = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe["volume"] / dataframe["volume"].rolling(period).mean()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def feature_engineering_expand_basic(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, dataframe: DataFrame, metadata: dict, **kwargs
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Access metadata such as the current pair/timeframe with:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         `metadata["pair"]` `metadata["tf"]`
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-pct-change"] = dataframe["close"].pct_change()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-raw_volume"] = dataframe["volume"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-raw_price"] = dataframe["close"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def feature_engineering_standard(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, dataframe: DataFrame, metadata: dict, **kwargs
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Access metadata such as the current pair with:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         `metadata["pair"]`
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         More details about feature engineering available:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         https://www.freqtrade.io/en/latest/freqai-feature-engineering
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: strategy dataframe which will receive the features
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metadata: metadata of current pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         usage example: dataframe["%-day_of_week"] = (dataframe["date"].dt.dayofweek + 1) / 7
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-day_of_week"] = dataframe["date"].dt.dayofweek
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["%-hour_of_day"] = dataframe["date"].dt.hour
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def set_freqai_targets(self, dataframe: DataFrame, metadata: dict, **kwargs) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         *Only functional with FreqAI enabled strategies*
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Required function to set the targets for the model.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         All targets must be prepended with `&` to be recognized by the FreqAI internals.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Access metadata such as the current pair with:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         `metadata["pair"]`
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         More details about feature engineering available:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         https://www.freqtrade.io/en/latest/freqai-feature-engineering
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: strategy dataframe which will receive the targets
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metadata: metadata of current pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         usage example: dataframe["&-target"] = dataframe["close"].shift(-1) / dataframe["close"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["&-s_close"] = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe["close"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             .shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             .rolling(self.freqai_info["feature_parameters"]["label_period_candles"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             .mean()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             / dataframe["close"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             - 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Classifiers are typically set up with strings as targets:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # df['&s-up_or_down'] = np.where( df["close"].shift(-100) >
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #                                 df["close"], 'up', 'down')
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # If user wishes to use multiple targets, they can add more by
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # appending more columns with '&'. User should keep in mind that multi targets
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # requires a multioutput prediction model such as
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # freqai/prediction_models/CatboostRegressorMultiTarget.py,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # freqtrade trade --freqaimodel CatboostRegressorMultiTarget
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # df["&-s_range"] = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #     df["close"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #     .shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #     .rolling(self.freqai_info["feature_parameters"]["label_period_candles"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #     .max()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #     -
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #     df["close"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #     .shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #     .rolling(self.freqai_info["feature_parameters"]["label_period_candles"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #     .min()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # All indicators must be populated by feature_engineering_*() functions
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # the model will return all labels created by user in `set_freqai_targets()`
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # (& appended targets), an indication of whether or not the prediction should be accepted,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # the target mean/std values for each of the labels created by user in
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # `set_freqai_targets()` for each training period.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe = self.freqai.start(dataframe, metadata, self)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         enter_long_conditions = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df["do_predict"] == 1,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df["&-s_close"] > 0.01,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if enter_long_conditions:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df.loc[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 reduce(lambda x, y: x & y, enter_long_conditions), ["enter_long", "enter_tag"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ] = (1, "long")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         enter_short_conditions = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df["do_predict"] == 1,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df["&-s_close"] < -0.01,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if enter_short_conditions:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df.loc[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 reduce(lambda x, y: x & y, enter_short_conditions), ["enter_short", "enter_tag"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ] = (1, "short")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return df
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         exit_long_conditions = [df["do_predict"] == 1, df["&-s_close"] < 0]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if exit_long_conditions:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df.loc[reduce(lambda x, y: x & y, exit_long_conditions), "exit_long"] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         exit_short_conditions = [df["do_predict"] == 1, df["&-s_close"] > 0]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if exit_short_conditions:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df.loc[reduce(lambda x, y: x & y, exit_short_conditions), "exit_short"] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return df
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def confirm_trade_entry(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         order_type: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         amount: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         time_in_force: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_time,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         entry_tag,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         side: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         df, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         last_candle = df.iloc[-1].squeeze()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if side == "long":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if rate > (last_candle["close"] * (1 + 0.0025)):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if rate < (last_candle["close"] * (1 - 0.0025)):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return True
