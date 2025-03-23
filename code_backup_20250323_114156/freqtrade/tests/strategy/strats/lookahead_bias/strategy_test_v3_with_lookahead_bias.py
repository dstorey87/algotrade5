# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# REMOVED_UNUSED_CODE: from pandas import DataFrame
# REMOVED_UNUSED_CODE: from technical.indicators import ichimoku

from freqtrade.strategy import IStrategy
from freqtrade.strategy.parameters import CategoricalParameter


class strategy_test_v3_with_lookahead_bias(IStrategy):
# REMOVED_UNUSED_CODE:     INTERFACE_VERSION = 3

    # Minimal ROI designed for the strategy
# REMOVED_UNUSED_CODE:     minimal_roi = {"40": 0.0, "30": 0.01, "20": 0.02, "0": 0.04}

    # Optimal stoploss designed for the strategy
# REMOVED_UNUSED_CODE:     stoploss = -0.10

    # Optimal timeframe for the strategy
# REMOVED_UNUSED_CODE:     timeframe = "5m"
# REMOVED_UNUSED_CODE:     scenario = CategoricalParameter(["no_bias", "bias1"], default="bias1", space="buy")

    # Number of candles the strategy requires before producing valid signals
# REMOVED_UNUSED_CODE:     startup_candle_count: int = 20

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # bias is introduced here
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.scenario.value != "no_bias":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ichi = ichimoku(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 dataframe,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 conversion_line_period=20,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 base_line_periods=60,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 laggin_span=120,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 displacement=30,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe["chikou_span"] = ichi["chikou_span"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.scenario.value == "no_bias":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe.loc[dataframe["close"].shift(10) < dataframe["close"], "enter_long"] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe.loc[dataframe["close"].shift(-10) > dataframe["close"], "enter_long"] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.scenario.value == "no_bias":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe.loc[dataframe["close"].shift(10) < dataframe["close"], "exit"] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe.loc[dataframe["close"].shift(-10) > dataframe["close"], "exit"] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
