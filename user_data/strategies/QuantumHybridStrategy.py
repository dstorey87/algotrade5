from utils.quantum_optimizer import QuantumOptimizer
from freqtrade.strategy import IStrategy, IntParameter
import pandas as pd

class QuantumHybridStrategy(IStrategy):
    """Quantum-enhanced trading strategy combining classical indicators with quantum optimization"""
    
    minimal_roi = {
        "0": 0.05,
        "10": 0.025,
        "20": 0.015,
        "30": 0.01
    }
    stoploss = -0.1
    timeframe = '5m'
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.03
    trailing_only_offset_is_reached = True
    process_only_new_candles = False
    startup_candle_count: int = 30
    
    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """Generate all indicators used by the strategy"""
        qopt = QuantumOptimizer()
        
        dataframe['rsi'] = qopt.quantum_rsi(dataframe['close'])
        dataframe['macd'], dataframe['macdsignal'], dataframe['macdhist'] = qopt.quantum_macd(dataframe['close'])
        dataframe['quantum_trend'] = qopt.get_quantum_trend(dataframe['close'], dataframe['volume'])
        
        return dataframe

    def populate_entry_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """Define entry signals"""
        dataframe.loc[
            (dataframe['rsi'] < 30) &
            (dataframe['macd'] > dataframe['macdsignal']) &
            (dataframe['quantum_trend'] > 0),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """Define exit signals"""
        dataframe.loc[
            (dataframe['rsi'] > 70) |
            (dataframe['macd'] < dataframe['macdsignal']) |
            (dataframe['quantum_trend'] < 0),
            'exit_long'] = 1
        return dataframe