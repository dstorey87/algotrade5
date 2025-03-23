# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

from datetime import datetime

import talib.abstract as ta
from pandas import DataFrame

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.persistence import Trade
from freqtrade.strategy import (
    BooleanParameter,
    DecimalParameter,
    IntParameter,
    IStrategy,
    RealParameter,
)


class StrategyTestV3(IStrategy):
    """
    Strategy used by tests freqtrade bot.
    Please do not modify this strategy, it's  intended for internal use only.
    Please look at the SampleStrategy in the user_data/strategy directory
    or strategy repository https://github.com/freqtrade/freqtrade-strategies
    for samples and inspiration.
    """

# REMOVED_UNUSED_CODE:     INTERFACE_VERSION = 3

    # Minimal ROI designed for the strategy
# REMOVED_UNUSED_CODE:     minimal_roi = {"40": 0.0, "30": 0.01, "20": 0.02, "0": 0.04}

    # Optimal max_open_trades for the strategy
# REMOVED_UNUSED_CODE:     max_open_trades = -1

    # Optimal stoploss designed for the strategy
# REMOVED_UNUSED_CODE:     stoploss = -0.10

    # Optimal timeframe for the strategy
# REMOVED_UNUSED_CODE:     timeframe = "5m"

    # Optional order type mapping
# REMOVED_UNUSED_CODE:     order_types = {
# REMOVED_UNUSED_CODE:         "entry": "limit",
# REMOVED_UNUSED_CODE:         "exit": "limit",
# REMOVED_UNUSED_CODE:         "stoploss": "limit",
# REMOVED_UNUSED_CODE:         "stoploss_on_exchange": False,
# REMOVED_UNUSED_CODE:     }

    # Number of candles the strategy requires before producing valid signals
# REMOVED_UNUSED_CODE:     startup_candle_count: int = 20

    # Optional time in force for orders
# REMOVED_UNUSED_CODE:     order_time_in_force = {
# REMOVED_UNUSED_CODE:         "entry": "gtc",
# REMOVED_UNUSED_CODE:         "exit": "gtc",
# REMOVED_UNUSED_CODE:     }

# REMOVED_UNUSED_CODE:     buy_params = {
# REMOVED_UNUSED_CODE:         "buy_rsi": 35,
# REMOVED_UNUSED_CODE:         # Intentionally not specified, so "default" is tested
# REMOVED_UNUSED_CODE:         # 'buy_plusdi': 0.4
# REMOVED_UNUSED_CODE:     }

# REMOVED_UNUSED_CODE:     sell_params = {"sell_rsi": 74, "sell_minusdi": 0.4}

    buy_rsi = IntParameter([0, 50], default=30, space="buy")
    buy_plusdi = RealParameter(low=0, high=1, default=0.5, space="buy")
    sell_rsi = IntParameter(low=50, high=100, default=70, space="sell")
    sell_minusdi = DecimalParameter(
        low=0, high=1, default=0.5001, decimals=3, space="sell", load=False
    )
    protection_enabled = BooleanParameter(default=True)
# REMOVED_UNUSED_CODE:     protection_cooldown_lookback = IntParameter([0, 50], default=30)

    # TODO: Can this work with protection tests? (replace HyperoptableStrategy implicitly ... )
# REMOVED_UNUSED_CODE:     @property
    def protections(self):
        prot = []
        if self.protection_enabled.value:
            # Workaround to simplify tests. This will not work in real scenarios.
            prot = self.config.get("_strategy_protections", {})
        return prot

# REMOVED_UNUSED_CODE:     bot_started = False

# REMOVED_UNUSED_CODE:     def bot_start(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.bot_started = True

# REMOVED_UNUSED_CODE:     def informative_pairs(self):
# REMOVED_UNUSED_CODE:         return []

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Momentum Indicator
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # ------------------------------------
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # ADX
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["adx"] = ta.ADX(dataframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # MACD
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         macd = ta.MACD(dataframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["macd"] = macd["macd"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["macdsignal"] = macd["macdsignal"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["macdhist"] = macd["macdhist"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Minus Directional Indicator / Movement
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["minus_di"] = ta.MINUS_DI(dataframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Plus Directional Indicator / Movement
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["plus_di"] = ta.PLUS_DI(dataframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # RSI
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["rsi"] = ta.RSI(dataframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Stoch fast
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stoch_fast = ta.STOCHF(dataframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["fastd"] = stoch_fast["fastd"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["fastk"] = stoch_fast["fastk"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Bollinger bands
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["bb_lowerband"] = bollinger["lower"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["bb_middleband"] = bollinger["mid"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["bb_upperband"] = bollinger["upper"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # EMA - Exponential Moving Average
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["ema10"] = ta.EMA(dataframe, timeperiod=10)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe.loc[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (dataframe["rsi"] < self.buy_rsi.value)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (dataframe["fastd"] < 35)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (dataframe["adx"] > 30)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (dataframe["plus_di"] > self.buy_plusdi.value)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             | ((dataframe["adx"] > 65) & (dataframe["plus_di"] > self.buy_plusdi.value)),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "enter_long",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe.loc[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (qtpylib.crossed_below(dataframe["rsi"], self.sell_rsi.value)),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ("enter_short", "enter_tag"),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ] = (1, "short_Tag")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe.loc[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     (qtpylib.crossed_above(dataframe["rsi"], self.sell_rsi.value))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     | (qtpylib.crossed_above(dataframe["fastd"], 70))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (dataframe["adx"] > 10)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (dataframe["minus_di"] > 0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             | ((dataframe["adx"] > 70) & (dataframe["minus_di"] > self.sell_minusdi.value)),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "exit_long",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe.loc[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (qtpylib.crossed_above(dataframe["rsi"], self.buy_rsi.value)),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ("exit_short", "exit_tag"),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ] = (1, "short_Tag")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE:     def leverage(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         proposed_leverage: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         max_leverage: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         entry_tag: str | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         side: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE:         # Return 3.0 in all cases.
# REMOVED_UNUSED_CODE:         # Bot-logic must make sure it's an allowed leverage and eventually adjust accordingly.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return 3.0

# REMOVED_UNUSED_CODE:     def adjust_trade_position(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_time: datetime,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_rate: float,
# REMOVED_UNUSED_CODE:         current_profit: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         min_stake: float | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         max_stake: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_entry_rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_exit_rate: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_entry_profit: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_exit_profit: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ) -> float | None:
# REMOVED_UNUSED_CODE:         if current_profit < -0.0075:
# REMOVED_UNUSED_CODE:             orders = trade.select_filled_orders(trade.entry_side)
# REMOVED_UNUSED_CODE:             return round(orders[0].stake_amount, 0)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return None


class StrategyTestV3Futures(StrategyTestV3):
# REMOVED_UNUSED_CODE:     can_short = True
