# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

from datetime import datetime

from pandas import DataFrame
from strategy_test_v3 import StrategyTestV3

from freqtrade.persistence import Trade


class StrategyTestV3CustomEntryPrice(StrategyTestV3):
    """
    Strategy used by tests freqtrade bot.
    Please do not modify this strategy, it's  intended for internal use only.
    Please look at the SampleStrategy in the user_data/strategy directory
    or strategy repository https://github.com/freqtrade/freqtrade-strategies
    for samples and inspiration.
    """

    new_entry_price: float = 0.001

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe.loc[dataframe["volume"] > 0, "enter_long"] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE:     def custom_entry_price(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade: Trade | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         proposed_rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         entry_tag: str | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         side: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE:         return self.new_entry_price
