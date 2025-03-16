# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these imports ---
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from pandas import DataFrame
from typing import Dict, Optional, Union, Tuple

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
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
from technical import qtpylib

"""
Quantum-Enhanced Hybrid Strategy
======================================
Uses quantum-inspired pattern recognition with strict risk management
"""
import logging
from functools import reduce

logger = logging.getLogger(__name__)


class QuantumHybrid(IStrategy):
    """
    Quantum-enhanced hybrid trading strategy.
    Implements both buy and sell signals based on quantum-validated patterns.
    """

    INTERFACE_VERSION = 3

    # Minimal ROI designed for the strategy.
    minimal_roi = {
        "0": 0.06,  # Take profit at 6%
        "10": 0.04,  # After 10 minutes
        "20": 0.02,  # After 20 minutes
        "30": 0.01,  # After 30 minutes
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.03  # 3% maximum loss

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True

    # Run "populate_indicators" only for new candle.
    process_only_new_candles = True

    # These values can be overridden in the config.
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = True

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30

    # Strategy parameters
    timeframe = "5m"

    # Hyperopt parameters
    buy_rsi = IntParameter(low=20, high=35, default=30, space="buy", optimize=True)
    sell_rsi = IntParameter(low=65, high=80, default=70, space="sell", optimize=True)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """Generate strategy indicators."""
        # EMA
        dataframe["ema_8"] = dataframe["close"].ewm(span=8, adjust=False).mean()
        dataframe["ema_13"] = dataframe["close"].ewm(span=13, adjust=False).mean()
        dataframe["ema_21"] = dataframe["close"].ewm(span=21, adjust=False).mean()

        # Volume
        dataframe["volume_mean"] = dataframe["volume"].rolling(window=5).mean()
        dataframe["volume_ratio"] = dataframe["volume"] / dataframe["volume_mean"]

        # RSI
        close_diff = dataframe["close"].diff()
        gain = close_diff.where(close_diff > 0, 0).rolling(window=14).mean()
        loss = -close_diff.where(close_diff < 0, 0).rolling(window=14).mean()
        rs = gain / loss
        dataframe["rsi"] = 100 - (100 / (1 + rs))

        # Custom momentum
        dataframe["growth_momentum"] = (
            (dataframe["close"] - dataframe["open"])
            / dataframe["open"]
            * 100
            * dataframe["volume_ratio"]
        )

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """Generate buy signals."""
        conditions = []

        # Momentum check
        momentum_up = (dataframe["growth_momentum"] > 1.0) & (
            dataframe["volume"] > dataframe["volume_mean"] * 1.5
        )

        # EMA cross
        ema_cross_up = (dataframe["ema_8"] > dataframe["ema_13"]) & (
            dataframe["ema_13"] > dataframe["ema_21"]
        )

        # RSI not overbought - using hyperopt parameter
        rsi_ok = dataframe["rsi"] < self.sell_rsi.value

        # Risk check
        risk_check = dataframe["close"] > dataframe["ema_21"]

        conditions.append(momentum_up)
        conditions.append(ema_cross_up)
        conditions.append(rsi_ok)
        conditions.append(risk_check)

        if conditions:
            dataframe.loc[reduce(lambda x, y: x & y, conditions), "buy"] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """Generate sell signals."""
        conditions = []

        # Momentum down
        momentum_down = dataframe["growth_momentum"] < -1.0

        # EMA cross down
        ema_cross_down = (dataframe["ema_8"] < dataframe["ema_13"]) & (
            dataframe["volume"] > dataframe["volume_mean"]
        )

        # RSI overbought - using hyperopt parameter
        rsi_high = dataframe["rsi"] > self.sell_rsi.value

        conditions.append(momentum_down)
        conditions.append(ema_cross_down)
        conditions.append(rsi_high)

        if conditions:
            dataframe.loc[reduce(lambda x, y: x | y, conditions), "sell"] = 1

        return dataframe
