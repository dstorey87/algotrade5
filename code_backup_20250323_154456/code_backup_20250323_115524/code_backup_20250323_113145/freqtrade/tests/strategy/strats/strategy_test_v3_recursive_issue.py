# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
import talib.abstract as ta
from pandas import DataFrame

from freqtrade.strategy import IStrategy
from freqtrade.strategy.parameters import CategoricalParameter


class strategy_test_v3_recursive_issue(IStrategy):
# REMOVED_UNUSED_CODE:     INTERFACE_VERSION = 3

    # Minimal ROI designed for the strategy
# REMOVED_UNUSED_CODE:     minimal_roi = {"0": 0.04}

    # Optimal stoploss designed for the strategy
# REMOVED_UNUSED_CODE:     stoploss = -0.10

    # Optimal timeframe for the strategy
# REMOVED_UNUSED_CODE:     timeframe = "5m"
    scenario = CategoricalParameter(["no_bias", "bias1", "bias2"], default="bias1", space="buy")

    # Number of candles the strategy requires before producing valid signals
# REMOVED_UNUSED_CODE:     startup_candle_count: int = 100

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # bias is introduced here
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.scenario.value == "no_bias":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe["rsi"] = ta.RSI(dataframe, timeperiod=50)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.scenario.value == "bias2":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Has both bias1 and bias2
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe["rsi_lookahead"] = ta.RSI(dataframe, timeperiod=50).shift(-1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # String columns shouldn't cause issues
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["test_string_column"] = f"a{len(dataframe)}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
