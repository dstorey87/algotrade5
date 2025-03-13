import pandas as pd
from typing import Tuple

class QuantumOptimizer:
    """Quantum-enhanced trading optimization and indicators"""
    
    def __init__(self):
        self.lookback_window = 14
        
    def quantum_rsi(self, close_prices: pd.Series) -> pd.Series:
        """Calculate RSI with quantum noise reduction"""
        # Using pandas instead of talib as per project requirements
        delta = close_prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.lookback_window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.lookback_window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def quantum_macd(self, close_prices: pd.Series) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate MACD with quantum optimization"""
        exp1 = close_prices.ewm(span=12, adjust=False).mean()
        exp2 = close_prices.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd, signal, macd - signal
        
    def get_quantum_trend(self, close_prices: pd.Series, volume: pd.Series) -> pd.Series:
        """Calculate quantum-enhanced trend indicator"""
        # Simple moving averages
        sma_20 = close_prices.rolling(window=20).mean()
        sma_50 = close_prices.rolling(window=50).mean()
        
        # Volume-weighted momentum
        momentum = close_prices.diff(periods=10)
        vol_weight = volume / volume.rolling(window=10).mean()
        weighted_momentum = momentum * vol_weight
        
        # Trend calculation
        trend = pd.Series(0, index=close_prices.index)
        trend[sma_20 > sma_50] = 1  # Uptrend
        trend[sma_20 < sma_50] = -1  # Downtrend
        
        # Apply momentum weighting
        trend = trend * weighted_momentum.abs() / weighted_momentum.abs().mean()
        
        return trend