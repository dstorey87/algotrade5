import numpy as np
import pandas as pd
from typing import Dict, List
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.strategy import IStrategy, merge_informative_pair
from freqtrade.freqai.prediction_models.LightGBMRegressor import LightGBMRegressor

class BasicTestStrategy(IStrategy):
    """
    A basic strategy using RSI and Bollinger Bands with FreqAI LightGBM model
    """
    minimal_roi = {
        "0": 0.05
    }
    
    stoploss = -0.10
    trailing_stop = False
    process_only_new_candles = True
    use_custom_stoploss = False
    timeframe = '1h'
    
    # FreqAI model settings
    freqai: Dict = {
        "model_name": "LightGBMRegressor",
        "model_save_path": "user_data/models",
        "data_path": "user_data/data",
    }
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame
        """
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']
        
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Entry signals based on RSI and BB
        """
        dataframe.loc[
            (
                (dataframe['rsi'] < 30) &
                (dataframe['close'] < dataframe['bb_lowerband'])
            ),
            'enter_long'] = 1
            
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Exit signals based on RSI and BB
        """
        dataframe.loc[
            (
                (dataframe['rsi'] > 70) &
                (dataframe['close'] > dataframe['bb_upperband'])
            ),
            'exit_long'] = 1
            
        return dataframe