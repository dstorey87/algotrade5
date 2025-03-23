import logging

import numpy as np  # noqa
import pandas as pd  # noqa
# REMOVED_UNUSED_CODE: import talib.abstract as ta
# REMOVED_UNUSED_CODE: from pandas import DataFrame
# REMOVED_UNUSED_CODE: from technical import qtpylib

from freqtrade.strategy import IntParameter, IStrategy, merge_informative_pair  # noqa


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class FreqaiExampleHybridStrategy(IStrategy):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Example of a hybrid FreqAI strat, designed to illustrate how a user may employ
# REMOVED_UNUSED_CODE:     FreqAI to bolster a typical Freqtrade strategy.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Launching this strategy would be:
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     freqtrade trade --strategy FreqaiExampleHybridStrategy --strategy-path freqtrade/templates
# REMOVED_UNUSED_CODE:     --freqaimodel CatboostClassifier --config config_examples/config_freqai.example.json
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     or the user simply adds this to their config:
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     "freqai": {
# REMOVED_UNUSED_CODE:         "enabled": true,
# REMOVED_UNUSED_CODE:         "purge_old_models": 2,
# REMOVED_UNUSED_CODE:         "train_period_days": 15,
# REMOVED_UNUSED_CODE:         "identifier": "unique-id",
# REMOVED_UNUSED_CODE:         "feature_parameters": {
# REMOVED_UNUSED_CODE:             "include_timeframes": [
# REMOVED_UNUSED_CODE:                 "3m",
# REMOVED_UNUSED_CODE:                 "15m",
# REMOVED_UNUSED_CODE:                 "1h"
# REMOVED_UNUSED_CODE:             ],
# REMOVED_UNUSED_CODE:             "include_corr_pairlist": [
# REMOVED_UNUSED_CODE:                 "BTC/USDT",
# REMOVED_UNUSED_CODE:                 "ETH/USDT"
# REMOVED_UNUSED_CODE:             ],
# REMOVED_UNUSED_CODE:             "label_period_candles": 20,
# REMOVED_UNUSED_CODE:             "include_shifted_candles": 2,
# REMOVED_UNUSED_CODE:             "DI_threshold": 0.9,
# REMOVED_UNUSED_CODE:             "weight_factor": 0.9,
# REMOVED_UNUSED_CODE:             "principal_component_analysis": false,
# REMOVED_UNUSED_CODE:             "use_SVM_to_remove_outliers": true,
# REMOVED_UNUSED_CODE:             "indicator_periods_candles": [10, 20]
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "data_split_parameters": {
# REMOVED_UNUSED_CODE:             "test_size": 0,
# REMOVED_UNUSED_CODE:             "random_state": 1
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "model_training_parameters": {
# REMOVED_UNUSED_CODE:             "n_estimators": 800
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:     },
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Thanks to @smarmau and @johanvulgt for developing and sharing the strategy.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     minimal_roi = {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # "120": 0.0,  # exit after 120 minutes at break even
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         "60": 0.01,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         "30": 0.02,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         "0": 0.04,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     plot_config = {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         "main_plot": {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "tema": {},
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         "subplots": {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "MACD": {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "macd": {"color": "blue"},
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "macdsignal": {"color": "orange"},
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "RSI": {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "rsi": {"color": "red"},
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "Up_or_down": {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "&s-up_or_down": {"color": "green"},
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     process_only_new_candles = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stoploss = -0.05
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     use_exit_signal = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     startup_candle_count: int = 30
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     can_short = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Hyperoptable parameters
# REMOVED_UNUSED_CODE:     buy_rsi = IntParameter(low=1, high=50, default=30, space="buy", optimize=True, load=True)
# REMOVED_UNUSED_CODE:     sell_rsi = IntParameter(low=50, high=100, default=70, space="sell", optimize=True, load=True)
# REMOVED_UNUSED_CODE:     short_rsi = IntParameter(low=51, high=100, default=70, space="sell", optimize=True, load=True)
# REMOVED_UNUSED_CODE:     exit_short_rsi = IntParameter(low=1, high=50, default=30, space="buy", optimize=True, load=True)
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         More details about feature engineering available:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         https://www.freqtrade.io/en/latest/freqai-feature-engineering
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: strategy dataframe which will receive the targets
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metadata: metadata of current pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         usage example: dataframe["&-target"] = dataframe["close"].shift(-1) / dataframe["close"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.freqai.class_names = ["down", "up"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["&s-up_or_down"] = np.where(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe["close"].shift(-50) > dataframe["close"], "up", "down"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:  # noqa: C901
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # User creates their own custom strat here. Present example is a supertrend
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # based strategy.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe = self.freqai.start(dataframe, metadata, self)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # TA indicators to combine with the Freqai targets
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # RSI
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["rsi"] = ta.RSI(dataframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Bollinger Bands
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["bb_lowerband"] = bollinger["lower"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["bb_middleband"] = bollinger["mid"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["bb_upperband"] = bollinger["upper"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["bb_percent"] = (dataframe["close"] - dataframe["bb_lowerband"]) / (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe["bb_upperband"] - dataframe["bb_lowerband"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["bb_width"] = (dataframe["bb_upperband"] - dataframe["bb_lowerband"]) / dataframe[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "bb_middleband"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # TEMA - Triple Exponential Moving Average
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["tema"] = ta.TEMA(dataframe, timeperiod=9)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         df.loc[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Signal: RSI crosses above 30
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (qtpylib.crossed_above(df["rsi"], self.buy_rsi.value))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (df["tema"] <= df["bb_middleband"])  # Guard: tema below BB middle
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (df["tema"] > df["tema"].shift(1))  # Guard: tema is raising
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (df["volume"] > 0)  # Make sure Volume is not 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (df["do_predict"] == 1)  # Make sure Freqai is confident in the prediction
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 &
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Only enter trade if Freqai thinks the trend is in this direction
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (df["&s-up_or_down"] == "up")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "enter_long",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         df.loc[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Signal: RSI crosses above 70
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (qtpylib.crossed_above(df["rsi"], self.short_rsi.value))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (df["tema"] > df["bb_middleband"])  # Guard: tema above BB middle
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (df["tema"] < df["tema"].shift(1))  # Guard: tema is falling
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (df["volume"] > 0)  # Make sure Volume is not 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (df["do_predict"] == 1)  # Make sure Freqai is confident in the prediction
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 &
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Only enter trade if Freqai thinks the trend is in this direction
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (df["&s-up_or_down"] == "down")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "enter_short",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return df
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         df.loc[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Signal: RSI crosses above 70
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (qtpylib.crossed_above(df["rsi"], self.sell_rsi.value))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (df["tema"] > df["bb_middleband"])  # Guard: tema above BB middle
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (df["tema"] < df["tema"].shift(1))  # Guard: tema is falling
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (df["volume"] > 0)  # Make sure Volume is not 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "exit_long",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         df.loc[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Signal: RSI crosses above 30
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (qtpylib.crossed_above(df["rsi"], self.exit_short_rsi.value))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 &
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Guard: tema below BB middle
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (df["tema"] <= df["bb_middleband"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (df["tema"] > df["tema"].shift(1))  # Guard: tema is raising
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (df["volume"] > 0)  # Make sure Volume is not 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "exit_short",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return df
