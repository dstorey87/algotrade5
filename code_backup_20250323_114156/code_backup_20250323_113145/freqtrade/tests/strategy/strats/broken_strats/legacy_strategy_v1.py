# type: ignore
from pandas import DataFrame

from freqtrade.strategy import IStrategy


# Dummy strategy - no longer loads but raises an exception.
class TestStrategyLegacyV1(IStrategy):
# REMOVED_UNUSED_CODE:     minimal_roi = {"40": 0.0, "30": 0.01, "20": 0.02, "0": 0.04}
# REMOVED_UNUSED_CODE:     stoploss = -0.10

# REMOVED_UNUSED_CODE:     timeframe = "5m"

# REMOVED_UNUSED_CODE:     def populate_indicators(self, dataframe: DataFrame) -> DataFrame:
# REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE:     def populate_buy_trend(self, dataframe: DataFrame) -> DataFrame:
# REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE:     def populate_sell_trend(self, dataframe: DataFrame) -> DataFrame:
# REMOVED_UNUSED_CODE:         return dataframe
