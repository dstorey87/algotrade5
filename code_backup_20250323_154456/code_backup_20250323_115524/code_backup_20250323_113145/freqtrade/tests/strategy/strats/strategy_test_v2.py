# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

import talib.abstract as ta
from pandas import DataFrame

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.strategy import IStrategy


class StrategyTestV2(IStrategy):
    """
    Strategy used by tests freqtrade bot.
    Please do not modify this strategy, it's  intended for internal use only.
    Please look at the SampleStrategy in the user_data/strategy directory
    or strategy repository https://github.com/freqtrade/freqtrade-strategies
    for samples and inspiration.
    """

# REMOVED_UNUSED_CODE:     INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy
# REMOVED_UNUSED_CODE:     minimal_roi = {"40": 0.0, "30": 0.01, "20": 0.02, "0": 0.04}

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
    # Test legacy use_sell_signal definition
# REMOVED_UNUSED_CODE:     use_sell_signal = False

    # By default this strategy does not use Position Adjustments
# REMOVED_UNUSED_CODE:     position_adjustment_enable = False

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Adds several different TA indicators to the given DataFrame
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Performance Note: For the best performance be frugal on the number of indicators
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         you are using. Let uncomment only the indicator you are using in your strategies
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: Dataframe with data from the exchange
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metadata: Additional information, like the currently traded pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: a Dataframe with all mandatory indicators for the strategies
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
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

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Based on TA indicators, populates the buy signal for the given dataframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: DataFrame
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metadata: Additional information, like the currently traded pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: DataFrame with buy column
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe.loc[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (dataframe["rsi"] < 35)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (dataframe["fastd"] < 35)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (dataframe["adx"] > 30)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (dataframe["plus_di"] > 0.5)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             | ((dataframe["adx"] > 65) & (dataframe["plus_di"] > 0.5)),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "buy",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Based on TA indicators, populates the sell signal for the given dataframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: DataFrame
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metadata: Additional information, like the currently traded pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: DataFrame with buy column
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe.loc[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     (qtpylib.crossed_above(dataframe["rsi"], 70))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     | (qtpylib.crossed_above(dataframe["fastd"], 70))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (dataframe["adx"] > 10)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 & (dataframe["minus_di"] > 0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             | ((dataframe["adx"] > 70) & (dataframe["minus_di"] > 0.5)),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "sell",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
