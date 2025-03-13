"""Quantum-enhanced hybrid trading strategy for FreqTrade"""
from datetime import datetime
from functools import reduce
from typing import Any, Dict, List, Optional, Union
import logging
import numpy as np
import pandas as pd
import talib.abstract as ta
from pandas import DataFrame
from freqtrade.strategy.interface import IStrategy
from freqtrade.strategy import DecimalParameter, IntParameter
import sys
from pathlib import Path

# Add strategy directory to Python path
strategy_dir = Path(__file__).parent
if str(strategy_dir) not in sys.path:
    sys.path.append(str(strategy_dir))

from quantum_optimizer import QuantumOptimizer
from ai_model_manager import AIModelManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuantumHybridStrategy(IStrategy):
    """Quantum-enhanced hybrid trading strategy for FreqTrade"""
    
    # Strategy interface version - required
    INTERFACE_VERSION = 3

    # Minimal ROI designed for the strategy
    minimal_roi = {
        "0": 0.05,   # 5% ROI target
        "30": 0.025, # 2.5% after 30 minutes
        "60": 0.015  # 1.5% after 60 minutes
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.015  # -1.5% stop loss

    # Trailing stoploss
    trailing_stop = True
    trailing_stop_positive = 0.005
    trailing_stop_positive_offset = 0.015

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True

    # Experimental settings
    use_exit_signal = True
    ignore_roi_if_entry_signal = True
    
    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the strategy with AI and quantum components"""
        super().__init__(config)
        
        # Initialize AI Model Manager
        self.ai_manager = AIModelManager(config)
        
        # Initialize quantum optimizer with config settings
        quantum_settings = config.get('quantum_settings', {})
        self.quantum_optimizer = QuantumOptimizer(
            n_qubits=quantum_settings.get('n_qubits', 4),
            shots=quantum_settings.get('shots', 1000),
            optimization_level=quantum_settings.get('optimization_level', 2)
        )

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """Generate all indicators used by the strategy"""
        
        # Calculate basic indicators
        dataframe['rsi'] = ta.RSI(dataframe['close'])
        dataframe['ema_9'] = ta.EMA(dataframe['close'], timeperiod=9)
        dataframe['ema_21'] = ta.EMA(dataframe['close'], timeperiod=21)
        dataframe['macd'], dataframe['macd_signal'], _ = ta.MACD(
            dataframe['close'], 
            fastperiod=12, 
            slowperiod=26, 
            signalperiod=9
        )
        
        # Initialize quantum metrics columns if they don't exist
        for col in ['pattern_score', 'quantum_confidence', 'market_regime']:
            if col not in dataframe.columns:
                dataframe[col] = 0.0
        
        # Quantum pattern analysis on recent price action
        try:
            if len(dataframe) >= 20:  # Ensure we have enough data
                features = dataframe['close'].values[-20:]  # Last 20 candles
                quantum_results = self.quantum_optimizer.analyze_pattern(features)
                
                # Add quantum metrics to the last row
                dataframe.loc[dataframe.index[-1], 'pattern_score'] = quantum_results['pattern_score']
                dataframe.loc[dataframe.index[-1], 'quantum_confidence'] = quantum_results['confidence']
                dataframe.loc[dataframe.index[-1], 'market_regime'] = quantum_results['regime']
            
        except Exception as e:
            logger.error(f"Error in quantum analysis: {e}")
            # Keep previous values or use neutral values if first row
            if len(dataframe) > 0:
                dataframe.loc[dataframe.index[-1], 'pattern_score'] = 0.5
                dataframe.loc[dataframe.index[-1], 'quantum_confidence'] = 0.5
                dataframe.loc[dataframe.index[-1], 'market_regime'] = 0
            
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """Trading logic for entry signals"""
        dataframe.loc[
            (
                # Technical indicators
                (dataframe['rsi'] < 30) &  # Oversold
                (dataframe['macd'] > dataframe['macd_signal']) &  # MACD crossover
                (dataframe['close'] > dataframe['ema_21']) &  # Price above EMA
                
                # Quantum-enhanced signals
                (dataframe['pattern_score'] > 0.6) &  # Strong pattern
                (dataframe['quantum_confidence'] > 0.65) &  # High confidence
                (dataframe['market_regime'] > 0)  # Bullish regime
            ),
            'enter_long'] = 1
            
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """Trading logic for exit signals"""
        dataframe.loc[
            (
                # Technical indicators
                (dataframe['rsi'] > 70) |  # Overbought
                (dataframe['macd'] < dataframe['macd_signal']) |  # MACD crossover
                
                # Quantum-enhanced signals
                (dataframe['pattern_score'] < 0.4) |  # Weak pattern
                (dataframe['quantum_confidence'] < 0.4)  # Low confidence
            ),
            'exit_long'] = 1
            
        return dataframe