# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these imports ---
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from pandas import DataFrame
from typing import Optional, Union
import talib.abstract as ta
from technical import qtpylib

from freqtrade.strategy import (
    IStrategy,
    Trade,
    Order,
    PairLocks,
    informative,  # @informative decorator
    # Hyperopt Parameters
    BooleanParameter,
    CategoricalParameter,
    DecimalParameter,
    IntParameter,
    RealParameter,
    # timeframe helpers
    timeframe_to_minutes,
    timeframe_to_next_date,
    timeframe_to_prev_date,
    # Strategy helper functions
    merge_informative_pair,
    stoploss_from_absolute,
    stoploss_from_open,
)

# --------------------------------


class SampleStrategy(IStrategy):
    """
    This is a sample strategy integrating FreqAI with LLM models.
    """

    INTERFACE_VERSION = 3
    can_short: bool = False

    minimal_roi = {
        "60": 0.05,
        "30": 0.10,
        "0": 0.20,
    }

    stoploss = -0.05
    trailing_stop = False
    timeframe = "5m"
    process_only_new_candles = True
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Hyperoptable parameters
    buy_rsi = IntParameter(low=1, high=50, default=30, space="buy", optimize=True, load=True)
    sell_rsi = IntParameter(low=50, high=100, default=70, space="sell", optimize=True, load=True)
    short_rsi = IntParameter(low=51, high=100, default=70, space="sell", optimize=True, load=True)
    exit_short_rsi = IntParameter(low=1, high=50, default=30, space="buy", optimize=True, load=True)

    startup_candle_count: int = 200

    order_types = {
        "entry": "limit",
        "exit": "limit",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }

    order_time_in_force = {"entry": "GTC", "exit": "GTC"}

    plot_config = {
        "main_plot": {
            "tema": {},
            "sar": {"color": "white"},
        },
        "subplots": {
            "MACD": {
                "macd": {"color": "blue"},
                "macdsignal": {"color": "orange"},
            },
            "RSI": {
                "rsi": {"color": "red"},
            },
        },
    }

    def feature_engineering_expand_all(self, dataframe: DataFrame, period: int, 
                                    metadata: dict, **kwargs) -> DataFrame:
        """
        Create features needed for FreqAI training
        """
        dataframe["%-change"] = dataframe["close"].pct_change()
        dataframe["volume-change"] = dataframe["volume"].pct_change()
        
        # Basic features
        dataframe["%-high"] = (dataframe["high"] - dataframe["close"]) / dataframe["close"]
        dataframe["%-low"] = (dataframe["low"] - dataframe["close"]) / dataframe["close"]
        
        return dataframe

    def set_freqai_targets(self, dataframe: DataFrame, metadata: dict, **kwargs) -> DataFrame:
        """
        Set targets for FreqAI training
        """
        dataframe["&-target"] = dataframe["close"].pct_change().shift(-1)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame
        """
        dataframe["adx"] = ta.ADX(dataframe)
        dataframe["rsi"] = ta.RSI(dataframe)

        stoch_fast = ta.STOCHF(dataframe)
        dataframe["fastd"] = stoch_fast["fastd"]
        dataframe["fastk"] = stoch_fast["fastk"]

        macd = ta.MACD(dataframe)
        dataframe["macd"] = macd["macd"]
        dataframe["macdsignal"] = macd["macdsignal"]
        dataframe["macdhist"] = macd["macdhist"]

        dataframe["mfi"] = ta.MFI(dataframe)

        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe["bb_lowerband"] = bollinger["lower"]
        dataframe["bb_middleband"] = bollinger["mid"]
        dataframe["bb_upperband"] = bollinger["upper"]
        dataframe["bb_percent"] = (dataframe["close"] - dataframe["bb_lowerband"]) / (
            dataframe["bb_upperband"] - dataframe["bb_lowerband"]
        )
        dataframe["bb_width"] = (dataframe["bb_upperband"] - dataframe["bb_lowerband"]) / dataframe[
            "bb_middleband"
        ]

        dataframe["sar"] = ta.SAR(dataframe)
        dataframe["tema"] = ta.TEMA(dataframe, timeperiod=9)

        hilbert = ta.HT_SINE(dataframe)
        dataframe["htsine"] = hilbert["sine"]
        dataframe["htleadsine"] = hilbert["leadsine"]

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators and FreqAI predictions, populates the entry signals
        """
        trade_predictions = self.dp.get_pair_dataframe(
            metadata["pair"], self.freqai_info["feature_parameters"]["include_timeframes"][0]
        )

        conditions = []
        if trade_predictions is not None and len(trade_predictions) > 0:
            dataframe = self.freqai.return_dataframe_predict(dataframe)
            conditions.append(dataframe["do_predict"] == 1)
            conditions.append(dataframe["&-prediction"] > 0.7)  # High probability threshold

        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe["rsi"], self.buy_rsi.value))
                & (dataframe["tema"] <= dataframe["bb_middleband"])
                & (dataframe["tema"] > dataframe["tema"].shift(1))
                & (dataframe["volume"] > 0)
                & (all(conditions) if conditions else True)
            ),
            "enter_long",
        ] = 1

        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe["rsi"], self.short_rsi.value))
                & (dataframe["tema"] > dataframe["bb_middleband"])
                & (dataframe["tema"] < dataframe["tema"].shift(1))
                & (dataframe["volume"] > 0)
            ),
            "enter_short",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators and FreqAI predictions, populates the exit signals
        """
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe["rsi"], self.sell_rsi.value))
                & (dataframe["tema"] > dataframe["bb_middleband"])
                & (dataframe["tema"] < dataframe["tema"].shift(1))
                & (dataframe["volume"] > 0)
            ),
            "exit_long",
        ] = 1

        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe["rsi"], self.exit_short_rsi.value))
                & (dataframe["tema"] <= dataframe["bb_middleband"])
                & (dataframe["tema"] > dataframe["tema"].shift(1))
                & (dataframe["volume"] > 0)
            ),
            "exit_short",
        ] = 1

        return dataframe
