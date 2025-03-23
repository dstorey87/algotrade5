import json
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from pandas import DataFrame

from freqtrade.strategy import DecimalParameter, IntParameter, IStrategy
from freqtrade.strategy.interface import IStrategy

# Add custom path for our utilities
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'utils'))
from db_manager import DatabaseManager
from llm_integrator import LLMIntegrator
from quantum_loop import QuantumLoop
from risk_manager import RiskManager

logger = logging.getLogger(__name__)

class QuantumLoopStrategy(IStrategy):
    """
    AlgoTradePro5 Quantum Loop Strategy
    
    This strategy integrates ML models with FreqAI to dynamically adapt to market conditions
    while maintaining strict risk management guidelines.
    """
    # Strategy parameters
    max_risk_per_trade = DecimalParameter(0.5, 5.0, default=2.0, space="buy", optimize=True)
    hard_drawdown_cap = DecimalParameter(5.0, 15.0, default=10.0, space="buy", optimize=True)
    
    # Buy hyperparameters
    buy_rsi_window = IntParameter(10, 50, default=14, space="buy", optimize=True)
    buy_rsi_threshold = IntParameter(10, 40, default=30, space="buy", optimize=True)
    
    # Sell hyperparameters
    sell_rsi_window = IntParameter(10, 50, default=14, space="sell", optimize=True)
    sell_rsi_threshold = IntParameter(60, 90, default=70, space="sell", optimize=True)
    
    # Trailing stop parameters
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True
    
    # Stoploss and ROI
    stoploss = -0.05
    minimal_roi = {
        "0": 0.05,
        "30": 0.03,
        "60": 0.02,
        "120": 0.01
    }
    
    # General settings
    ticker_interval = '5m'
    timeframe = '5m'
    process_only_new_candles = True
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False
    
    # Initialization
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.risk_manager = RiskManager(
            max_risk_per_trade=float(self.max_risk_per_trade.value),
            hard_drawdown_cap=float(self.hard_drawdown_cap.value)
        )
        
        # Initialize LLM integrator for strategy refinement
        self.llm_integrator = LLMIntegrator(os.environ.get('LLM_MODELS_PATH'))
        
        # Initialize Quantum Loop for strategy validation
        self.quantum_loop = QuantumLoop()
        
        # Initialize Database Manager for logging and metrics
        self.db_manager = DatabaseManager(
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD')
        )
        
        # Track trades and performance
        self.trades_log = []
        self.strategy_performance = {
            'win_rate': 0,
            'total_trades': 0,
            'successful_trades': 0,
            'failed_trades': 0,
            'current_drawdown': 0,
            'max_drawdown': 0
        }
        
        logger.info("QuantumLoopStrategy initialized with risk parameters: "
                    f"max_risk_per_trade={self.max_risk_per_trade.value}, "
                    f"hard_drawdown_cap={self.hard_drawdown_cap.value}")
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate indicators for the given dataframe
        """
        # RSI
        dataframe['rsi'] = self.calculate_rsi(dataframe, self.buy_rsi_window.value)
        
        # MACD
        macd_fast = 12
        macd_slow = 26
        macd_signal = 9
        dataframe['macd'], dataframe['macdsignal'], dataframe['macdhist'] = self.calculate_macd(
            dataframe, macd_fast, macd_slow, macd_signal
        )
        
        # Bollinger Bands
        bollinger_window = 20
        bollinger_std_dev = 2
        bollinger = self.calculate_bollinger_bands(dataframe, bollinger_window, bollinger_std_dev)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']
        
        # Volume indicators
        dataframe['volume_mean_slow'] = dataframe['volume'].rolling(window=30).mean()
        dataframe['volume_mean_fast'] = dataframe['volume'].rolling(window=10).mean()
        
        # Trend indicators
        dataframe['ema_50'] = self.calculate_ema(dataframe, 50)
        dataframe['ema_200'] = self.calculate_ema(dataframe, 200)
        dataframe['sma_50'] = self.calculate_sma(dataframe, 50)
        dataframe['sma_200'] = self.calculate_sma(dataframe, 200)
        
        # ADX
        dataframe['adx'] = self.calculate_adx(dataframe)
        
        # Log the completion of indicator calculation
        logger.debug(f"Indicators calculated for {metadata['pair']}")
        
        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate buy signals
        """
        conditions = []
        
        # Basic RSI condition
        conditions.append(dataframe['rsi'] < self.buy_rsi_threshold.value)
        
        # Price below lower Bollinger Band
        conditions.append(dataframe['close'] < dataframe['bb_lowerband'])
        
        # Upward momentum with MACD
        conditions.append(dataframe['macdhist'] > dataframe['macdhist'].shift(1))
        
        # Volume confirmation
        conditions.append(dataframe['volume'] > 0)
        conditions.append(dataframe['volume_mean_fast'] > dataframe['volume_mean_slow'])
        
        # Apply risk management constraints
        if not self.risk_manager.can_enter_new_trade():
            logger.warning(f"Risk management prevented new entry for {metadata['pair']}")
            return dataframe
        
        # Quantum Loop validation
        if not self.quantum_loop.validate_entry(dataframe.iloc[-1].to_dict(), metadata['pair']):
            logger.info(f"Quantum Loop rejected entry for {metadata['pair']}")
            return dataframe
        
        # Combine all conditions
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'enter_long'
            ] = 1
        
        # Log entry signals
        entry_signals = dataframe[dataframe['enter_long'] == 1]
        if not entry_signals.empty:
            logger.info(f"Generated entry signals for {metadata['pair']}: {len(entry_signals)}")
            
            # Log to database
            for idx, signal in entry_signals.iterrows():
                self.db_manager.log_signal('entry', metadata['pair'], idx, signal.to_dict())
        
        return dataframe
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate sell signals
        """
        conditions = []
        
        # RSI overbought condition
        conditions.append(dataframe['rsi'] > self.sell_rsi_threshold.value)
        
        # Price above upper Bollinger Band
        conditions.append(dataframe['close'] > dataframe['bb_upperband'])
        
        # Downward momentum with MACD
        conditions.append(dataframe['macdhist'] < dataframe['macdhist'].shift(1))
        
        # Combine all conditions
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'exit_long'
            ] = 1
        
        # Log exit signals
        exit_signals = dataframe[dataframe['exit_long'] == 1]
        if not exit_signals.empty:
            logger.info(f"Generated exit signals for {metadata['pair']}: {len(exit_signals)}")
            
            # Log to database
            for idx, signal in exit_signals.iterrows():
                self.db_manager.log_signal('exit', metadata['pair'], idx, signal.to_dict())
        
        return dataframe
    
    def calculate_rsi(self, dataframe: DataFrame, window: int) -> pd.Series:
        """
        Calculate RSI using pandas
        """
        diff = dataframe['close'].diff()
        gain = diff.where(diff > 0, 0)
        loss = -diff.where(diff < 0, 0)
        
        avg_gain = gain.rolling(window=window, min_periods=1).mean()
        avg_loss = loss.rolling(window=window, min_periods=1).mean()
        
        rs = avg_gain / avg_loss.replace(0, np.finfo(float).eps)
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def calculate_macd(self, dataframe: DataFrame, fast: int, slow: int, signal: int) -> tuple:
        """
        Calculate MACD using pandas
        """
        ema_fast = dataframe['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = dataframe['close'].ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        macdsignal = macd.ewm(span=signal, adjust=False).mean()
        macdhist = macd - macdsignal
        
        return macd, macdsignal, macdhist
    
    def calculate_bollinger_bands(self, dataframe: DataFrame, window: int, std_dev: int) -> dict:
        """
        Calculate Bollinger Bands using pandas
        """
        rolling_mean = dataframe['close'].rolling(window=window).mean()
        rolling_std = dataframe['close'].rolling(window=window).std(ddof=0)
        
        upper_band = rolling_mean + (rolling_std * std_dev)
        lower_band = rolling_mean - (rolling_std * std_dev)
        
        return {
            'upper': upper_band,
            'mid': rolling_mean,
            'lower': lower_band
        }
    
    def calculate_ema(self, dataframe: DataFrame, window: int) -> pd.Series:
        """
        Calculate EMA using pandas
        """
        return dataframe['close'].ewm(span=window, adjust=False).mean()
    
    def calculate_sma(self, dataframe: DataFrame, window: int) -> pd.Series:
        """
        Calculate SMA using pandas
        """
        return dataframe['close'].rolling(window=window).mean()
    
    def calculate_adx(self, dataframe: DataFrame, window: int = 14) -> pd.Series:
        """
        Calculate ADX using pandas
        """
        high = dataframe['high']
        low = dataframe['low']
        close = dataframe['close']
        
        plus_dm = high.diff()
        minus_dm = low.diff(-1)
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm > 0] = 0
        
        tr1 = pd.DataFrame(high - low)
        tr2 = pd.DataFrame(abs(high - close.shift(1)))
        tr3 = pd.DataFrame(abs(low - close.shift(1)))
        frames = [tr1, tr2, tr3]
        tr = pd.concat(frames, axis=1, join='inner').max(axis=1)
        atr = tr.rolling(window).mean()
        
        plus_di = 100 * (plus_dm.ewm(alpha=1/window).mean() / atr)
        minus_di = abs(100 * (minus_dm.ewm(alpha=1/window).mean() / atr))
        dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
        adx = dx.ewm(alpha=1/window).mean()
        
        return adx
    
    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                      current_rate: float, current_profit: float, **kwargs) -> float:
        """
        Custom stoploss logic, using profit threshold
        """
        if current_profit >= 0.05:
            return self.stoploss
        return self.stoploss
    
    def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float,
                          time_in_force: str, current_time: datetime, **kwargs) -> bool:
        """
        Called before placing a buy order.
        """
        # Get dataframe from kwargs
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        
        # Check risk management
        if not self.risk_manager.confirm_trade_entry(pair, amount, rate):
            logger.warning(f"Risk management rejected trade entry for {pair}")
            return False
        
        # Use LLM to analyze entry
        llm_analysis = self.llm_integrator.analyze_entry(
            pair, 
            last_candle.to_dict(),
            {
                'order_type': order_type,
                'amount': amount,
                'rate': rate,
                'time_in_force': time_in_force
            }
        )
        
        # Log the trade to database
        self.db_manager.log_trade_entry(
            pair, 
            amount, 
            rate, 
            current_time,
            llm_analysis
        )
        
        # Quantum loop final validation
        return self.quantum_loop.confirm_entry(pair, amount, rate, last_candle.to_dict())
    
    def confirm_trade_exit(self, pair: str, trade: 'Trade', order_type: str, amount: float,
                          rate: float, time_in_force: str, exit_reason: str,
                          current_time: datetime, **kwargs) -> bool:
        """
        Called before placing a sell order.
        """
        # Log the exit to database
        self.db_manager.log_trade_exit(
            pair,
            trade.stake_amount,
            rate,
            current_time,
            exit_reason,
            trade.calc_profit_ratio(rate)
        )
        
        # Update performance metrics
        profit_ratio = trade.calc_profit_ratio(rate)
        self.strategy_performance['total_trades'] += 1
        
        if profit_ratio > 0:
            self.strategy_performance['successful_trades'] += 1
        else:
            self.strategy_performance['failed_trades'] += 1
        
        self.strategy_performance['win_rate'] = (
            self.strategy_performance['successful_trades'] / 
            self.strategy_performance['total_trades']
        ) * 100
        
        # Calculate current drawdown
        current_drawdown = self.risk_manager.calculate_drawdown()
        self.strategy_performance['current_drawdown'] = current_drawdown
        
        if current_drawdown > self.strategy_performance['max_drawdown']:
            self.strategy_performance['max_drawdown'] = current_drawdown
        
        # Get quantum loop feedback for strategy improvement
        self.quantum_loop.process_trade_result(
            pair, 
            profit_ratio,
            trade.trade_duration,
            self.strategy_performance
        )
        
        # Always allow exits
        return True

# Import utilities
from functools import reduce
