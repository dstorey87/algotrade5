"""
The strategies here are minimal strategies designed to fail loading in certain conditions.
They are not operational, and don't aim to be.
"""

from datetime import datetime

from pandas import DataFrame

from freqtrade.persistence.trade_model import Order
from freqtrade.strategy.interface import IStrategy


class TestStrategyNoImplements(IStrategy):
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return super().populate_indicators(dataframe, metadata)


class TestStrategyNoImplementSell(TestStrategyNoImplements):
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return super().populate_entry_trend(dataframe, metadata)


class TestStrategyImplementCustomSell(TestStrategyNoImplementSell):
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return super().populate_exit_trend(dataframe, metadata)

# REMOVED_UNUSED_CODE:     def custom_sell(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_profit: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         return False


class TestStrategyImplementBuyTimeout(TestStrategyNoImplementSell):
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return super().populate_exit_trend(dataframe, metadata)

# REMOVED_UNUSED_CODE:     def check_buy_timeout(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pair: str, trade, order: Order, current_time: datetime, **kwargs
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         return False


class TestStrategyImplementSellTimeout(TestStrategyNoImplementSell):
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return super().populate_exit_trend(dataframe, metadata)

# REMOVED_UNUSED_CODE:     def check_sell_timeout(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pair: str, trade, order: Order, current_time: datetime, **kwargs
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         return False
