import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from freqtrade.strategy.interface import IStrategy
from freqtrade.freqai.base_models.FreqaiMultiOutputClassifier import FreqaiMultiOutputClassifier
from freqtrade.freqai.base_models.FreqaiRegressorMixin import FreqaiRegressorMixin

logger = logging.getLogger(__name__)

class QuantumFreqAIStrategy(IStrategy):
    """
    QuantumFreqAIStrategy - AI-Driven trading strategy
    
    This strategy uses FreqAI for prediction and applies quantum loop optimization
    with proper risk management techniques including Kelly Criterion and tight
    drawdown controls.
    
    Note: No Talib is used as per project requirements.
    """
    
    # Strategy interface version
    INTERFACE_VERSION: int = 3
    
    # Can this strategy go short?
    can_short: bool = True
    
    # Minimal ROI designed for the strategy
    minimal_roi = {
        "0": 0.03,        # 3% immediate profit target
        "60": 0.02,       # 2% after 60 minutes
        "120": 0.01,      # 1% after 120 minutes
        "240": 0          # No minimum after 4 hours
    }

    # Stoploss
    stoploss = -0.10  # 10% stop loss
    
    # Trailing stop
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True
    
    # Timeframe for the strategy
    timeframe = '5m'
    
    # Run only once at the start of the bot
    startup_candle_count: int = 300
    
    # FreqAI configuration
    freqai_config = {
        "feature_parameters": {
            "include_timeframes": ["5m", "15m", "1h"],
            "include_corr_pairlist": ["BTC/USDT", "ETH/USDT"],
            "label_period_candles": 24,
            "include_shifted_candles": 2,
            "DI_threshold": 0.9,
            "weight_factor": 0.9,
            "principal_component_analysis": False,
            "use_SVM_to_remove_outliers": True,
            "stratify_training_data": 10,
            "indicator_periods_candles": [10, 20, 30, 50],
        },
        "data_split_parameters": {
            "test_size": 0.25,
            "shuffle": False,
        },
        "model_training_parameters": {
            "n_estimators": 100,
            "learning_rate": 0.005,
            "random_state": 42
        },
    }
    
    # Parameters for hyperopt
    buy_rsi = IntParameter(low=10, high=40, default=30, space="buy", optimize=True)
    sell_rsi = IntParameter(low=60, high=90, default=70, space="sell", optimize=True)
    
    # Risk management parameters
    risk_per_trade = DecimalParameter(0.01, 0.02, default=0.01, space="protection", decimals=2, optimize=True)
    max_drawdown = DecimalParameter(0.05, 0.15, default=0.10, space="protection", decimals=2, optimize=True)
    
    def informative_pairs(self) -> List[Tuple[str, str]]:
        """
        Define additional, informative pair/interval combinations to be cached.
        """
        pairs = self.dp.current_whitelist()
        informative_pairs = []
        
        for pair in pairs:
            for timeframe in self.freqai_config["feature_parameters"]["include_timeframes"]:
                if timeframe != self.timeframe:
                    informative_pairs.append((pair, timeframe))
            
            for corr_pair in self.freqai_config["feature_parameters"]["include_corr_pairlist"]:
                if corr_pair != pair:
                    informative_pairs.append((corr_pair, self.timeframe))
                    for timeframe in self.freqai_config["feature_parameters"]["include_timeframes"]:
                        if timeframe != self.timeframe:
                            informative_pairs.append((corr_pair, timeframe))
                
        return informative_pairs
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate all indicators for FreqAI consumption
        Using only Pandas and QTPyLib - No TA-Lib per project requirements
        """
        # Basic price and volume information
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()
        dataframe['price_change'] = dataframe['close'].pct_change()
        
        # Common indicators - using pandas not talib
        for period in self.freqai_config["feature_parameters"]["indicator_periods_candles"]:
            # Trend indicators
            dataframe[f'sma_{period}'] = dataframe['close'].rolling(window=period).mean()
            dataframe[f'ema_{period}'] = dataframe['close'].ewm(span=period, adjust=False).mean()
            
            # Momentum indicators - all custom implementations with pandas
            dataframe[f'rsi_{period}'] = self._calculate_rsi(dataframe, period)
            dataframe[f'mfi_{period}'] = self._calculate_mfi(dataframe, period)
            dataframe[f'cci_{period}'] = self._calculate_cci(dataframe, period)
            
            # Volatility indicators
            dataframe[f'bollinger_upper_{period}'] = (
                dataframe['close'].rolling(period).mean() + 
                dataframe['close'].rolling(period).std() * 2
            )
            dataframe[f'bollinger_lower_{period}'] = (
                dataframe['close'].rolling(period).mean() - 
                dataframe['close'].rolling(period).std() * 2
            )
            dataframe[f'bollinger_width_{period}'] = (
                (dataframe[f'bollinger_upper_{period}'] - dataframe[f'bollinger_lower_{period}']) / 
                dataframe[f'sma_{period}']
            )
            
            # Volume indicators
            dataframe[f'vwap_{period}'] = (
                (dataframe['volume'] * dataframe['close']).rolling(period).sum() / 
                dataframe['volume'].rolling(period).sum()
            )
            
            # Custom indicators
            dataframe[f'fisher_transform_{period}'] = self._calculate_fisher_transform(dataframe, period)
        
        # QTPyLib indicators
        dataframe['rsi'] = qtpylib.rsi(dataframe)
        dataframe['fisher_rsi'] = qtpylib.fisher_rsi(dataframe['rsi'])
        dataframe['sar'] = qtpylib.sar(dataframe)
        
        # Add indicators for different market conditions
        dataframe['market_trend'] = self._calculate_market_trend(dataframe)
        dataframe['volatility'] = self._calculate_volatility(dataframe)
        
        # Label generation for supervised learning
        dataframe['&-future_price'] = dataframe['close'].shift(-self.freqai_config["feature_parameters"]["label_period_candles"])
        dataframe['&-future_price_change'] = (
            (dataframe['&-future_price'] - dataframe['close']) / dataframe['close']
        )
        
        # Classification targets
        dataframe['&-up_or_down'] = np.where(dataframe['&-future_price_change'] > 0, 1, 0)
        
        # Regression targets with thresholds for strong moves
        up_thresh = 0.01  # 1% move up
        down_thresh = -0.01  # 1% move down
        
        dataframe['&-target'] = 0
        dataframe.loc[dataframe['&-future_price_change'] > up_thresh, '&-target'] = 1
        dataframe.loc[dataframe['&-future_price_change'] < down_thresh, '&-target'] = -1
        
        return dataframe
    
    def _calculate_rsi(self, dataframe: DataFrame, window: int) -> pd.Series:
        """Calculate RSI using pandas only (no Talib)"""
        delta = dataframe['close'].diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        
        ma_up = up.rolling(window=window).mean()
        ma_down = down.rolling(window=window).mean()
        
        rsi = 100 - (100 / (1 + ma_up / ma_down))
        return rsi
    
    def _calculate_mfi(self, dataframe: DataFrame, window: int) -> pd.Series:
        """Calculate Money Flow Index using pandas only"""
        typical_price = (dataframe['high'] + dataframe['low'] + dataframe['close']) / 3
        money_flow = typical_price * dataframe['volume']
        
        delta = typical_price.diff()
        positive_flow = (delta > 0) * money_flow
        negative_flow = (delta < 0) * money_flow
        
        pos_mf = positive_flow.rolling(window=window).sum()
        neg_mf = negative_flow.rolling(window=window).sum()
        
        mfi = 100 - (100 / (1 + pos_mf / neg_mf))
        return mfi
    
    def _calculate_cci(self, dataframe: DataFrame, window: int) -> pd.Series:
        """Calculate Commodity Channel Index using pandas only"""
        typical_price = (dataframe['high'] + dataframe['low'] + dataframe['close']) / 3
        ma_tp = typical_price.rolling(window=window).mean()
        mean_deviation = abs(typical_price - ma_tp).rolling(window=window).mean()
        
        cci = (typical_price - ma_tp) / (0.015 * mean_deviation)
        return cci
    
    def _calculate_fisher_transform(self, dataframe: DataFrame, window: int) -> pd.Series:
        """Calculate Fisher Transform using pandas only"""
        high_low_mean = (dataframe['high'] + dataframe['low']) / 2
        normalized = (
            (high_low_mean - high_low_mean.rolling(window=window).min()) / 
            (high_low_mean.rolling(window=window).max() - high_low_mean.rolling(window=window).min())
        )
        normalized = normalized.clip(0.001, 0.999)  # Avoid extreme values
        fisher = 0.5 * np.log((1 + normalized) / (1 - normalized))
        return fisher
    
    def _calculate_market_trend(self, dataframe: DataFrame) -> pd.Series:
        """Calculate overall market trend indicator"""
        short_ema = dataframe['close'].ewm(span=5, adjust=False).mean()
        long_ema = dataframe['close'].ewm(span=50, adjust=False).mean()
        
        # +1 for uptrend, -1 for downtrend, 0 for sideways
        trend = np.where(short_ema > long_ema, 1, np.where(short_ema < long_ema, -1, 0))
        return pd.Series(trend, index=dataframe.index)
    
    def _calculate_volatility(self, dataframe: DataFrame) -> pd.Series:
        """Calculate volatility using standard deviation of returns"""
        returns = dataframe['close'].pct_change()
        volatility = returns.rolling(window=20).std() * np.sqrt(252 * 288)  # Annualized for 5m bars
        return volatility
        
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate buy signals based on FreqAI predictions
        """
        # Default initialization
        dataframe.loc[:, 'enter_long'] = 0
        dataframe.loc[:, 'enter_short'] = 0
        
        if self.freqai and self.dp and "freqaimodel" in self.dp.dataprovider_drivers:
            # Get the model prediction for this pair
            predictions = self.dp.dataprovider_drivers["freqaimodel"].predict(
                dataframe.copy(), metadata["pair"]
            )
            
            # Merge predictions with original dataframe
            dataframe = pd.concat([dataframe, predictions], axis=1)
            
            # Apply Kelly Criterion for position sizing
            dataframe['kelly_coef'] = self._calculate_kelly(dataframe, metadata)
            
            # Long entries
            dataframe.loc[
                (
                    (dataframe['&-target_prediction'] > 0.55) &  # Strong up prediction
                    (dataframe['rsi'] < self.buy_rsi.value) &   # RSI oversold condition
                    (dataframe['volume'] > 0) &
                    (dataframe['kelly_coef'] > 0)               # Kelly criterion is positive
                ),
                'enter_long'
            ] = 1
            
            # Short entries
            dataframe.loc[
                (
                    (dataframe['&-target_prediction'] < -0.55) &  # Strong down prediction
                    (dataframe['rsi'] > self.sell_rsi.value) &   # RSI overbought condition
                    (dataframe['volume'] > 0) &
                    (dataframe['kelly_coef'] < 0)               # Kelly criterion is negative
                ),
                'enter_short'
            ] = 1
        
        return dataframe
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate sell signals based on FreqAI predictions
        """
        # Default initialization
        dataframe.loc[:, 'exit_long'] = 0
        dataframe.loc[:, 'exit_short'] = 0
        
        if self.freqai and self.dp and "freqaimodel" in self.dp.dataprovider_drivers:
            # Get the model prediction
            predictions = self.dp.dataprovider_drivers["freqaimodel"].predict(
                dataframe.copy(), metadata["pair"]
            )
            
            # Merge predictions with original dataframe
            dataframe = pd.concat([dataframe, predictions], axis=1)
            
            # Long exits
            dataframe.loc[
                (
                    (dataframe['&-target_prediction'] < 0) &  # Prediction turns negative
                    (dataframe['rsi'] > self.sell_rsi.value)  # RSI overbought
                ),
                'exit_long'
            ] = 1
            
            # Short exits
            dataframe.loc[
                (
                    (dataframe['&-target_prediction'] > 0) &  # Prediction turns positive
                    (dataframe['rsi'] < self.buy_rsi.value)   # RSI oversold
                ),
                'exit_short'
            ] = 1
        
        return dataframe
    
    def _calculate_kelly(self, dataframe: DataFrame, metadata: dict) -> pd.Series:
        """
        Calculate Kelly Criterion for position sizing
        f* = p - (1 - p) / b
        
        Where:
            f* = fraction of capital to risk
            p = probability of win
            b = win/loss ratio
        """
        # Get the win probability from our model
        win_prob = dataframe['&-target_prediction'].abs()
        
        # Calculate win/loss ratio based on recent trades
        # For safety, we'll use a conservative estimate of 1:1 when we don't have data
        win_loss_ratio = 1.0
        
        # Calculate Kelly fraction
        kelly = win_prob - ((1 - win_prob) / win_loss_ratio)
        
        # Constrain Kelly value to limit risk
        # Apply a factor of 0.5 to the Kelly criterion for safety
        safe_kelly = kelly * 0.5
        
        # Cap max risk per trade at our risk_per_trade parameter
        safe_kelly = safe_kelly.clip(upper=self.risk_per_trade.value)
        
        # Apply sign based on prediction direction
        signed_kelly = safe_kelly * np.sign(dataframe['&-target_prediction'])
        
        return signed_kelly
    
    def custom_stake_amount(self, pair: str, current_time: datetime, current_rate: float,
                           proposed_stake: float, min_stake: Optional[float], max_stake: float,
                           leverage: float, entry_tag: Optional[str], side: str,
                           **kwargs) -> float:
        """
        Adjust stake amount based on Kelly Criterion calculation
        """
        # Get dataframe for this pair
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        
        if dataframe is not None and not dataframe.empty:
            # Get the most recent row
            last_candle = dataframe.iloc[-1].squeeze()
            
            # Check if we have Kelly coefficient
            if 'kelly_coef' in last_candle:
                # Calculate stake based on Kelly
                kelly_stake = max_stake * abs(last_candle['kelly_coef'])
                
                # Apply min/max constraints
                if min_stake and kelly_stake < min_stake:
                    return min_stake
                
                return min(kelly_stake, max_stake)
        
        # Default to 1% of max stake as fallback
        return max_stake * self.risk_per_trade.value
        
    def custom_exit(self, pair: str, trade: 'Trade', current_time: 'datetime', current_rate: float,
                   current_profit: float, **kwargs) -> Optional[str]:
        """
        Implement custom exit logic, including max drawdown protection
        """
        # Maximum drawdown protection
        if current_profit <= -self.max_drawdown.value:
            return "max_drawdown_protection"
            
        # Get dataframe for this pair
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        
        if dataframe is not None and not dataframe.empty:
            # Get the most recent candle
            last_candle = dataframe.iloc[-1].squeeze()
            
            # Exit if prediction significantly changes against our position
            if trade.is_long and '&-target_prediction' in last_candle and last_candle['&-target_prediction'] < -0.6:
                return "prediction_reversed_long"
                
            elif trade.is_short and '&-target_prediction' in last_candle and last_candle['&-target_prediction'] > 0.6:
                return "prediction_reversed_short"
            
        return None
        
    def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float,
                           time_in_force: str, current_time: datetime, entry_tag: Optional[str],
                           side: str, **kwargs) -> bool:
        """
        Confirm we want to enter a trade, checking overall portfolio risk
        """
        # Check our current exposure
        active_trades = len(self.wallets.open_trades)
        max_open_trades = self.config.get('max_open_trades', 1)
        
        # Calculate current portfolio risk
        current_portfolio_risk = sum(
            abs(trade.open_rate - trade.stop_loss) / trade.open_rate * trade.stake_amount / self.wallets.get_total_stake_amount()
            for trade in self.wallets.open_trades if trade.stop_loss
        ) if hasattr(self, 'wallets') and hasattr(self.wallets, 'open_trades') else 0
        
        # Limit max portfolio risk
        max_portfolio_risk = 0.30  # Max 30% portfolio at risk concurrently
        
        # New trade risk
        new_trade_risk = self.risk_per_trade.value
        
        # Portfolio health checks
        if current_portfolio_risk + new_trade_risk > max_portfolio_risk:
            logger.info(f"Rejecting new trade for {pair}: Total portfolio risk would exceed {max_portfolio_risk*100}%")
            return False
            
        # Check if we have buy funds available
        if not self.wallets.check_free_space(self.config['stake_currency'], amount, side):
            logger.info(f"Rejecting new trade for {pair}: Not enough free capital available")
            return False
        
        return True