#!/usr/bin/env python3
"""Utility functions for AlgoTradPro5"""
import logging
import sqlite3
import numpy as np
import pandas as pd
from typing import Dict, Any, Callable
from functools import wraps
import time
from sklearn.preprocessing import StandardScaler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retry_on_exception(retries: int = 3, delay: float = 1.0) -> Callable:
    """Decorator to retry a function on exception"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < retries - 1:
                        logger.warning(f"Attempt {attempt + 1} failed: {e}")
                        time.sleep(delay * (attempt + 1))
            logger.error(f"All {retries} attempts failed. Last error: {last_exception}")
            raise last_exception
        return wrapper
    return decorator

# Utility functions for database operations
class DatabaseUtils:
    @staticmethod
    def connect(db_path: str) -> sqlite3.Connection:
        return sqlite3.connect(db_path)

    @staticmethod
    def execute_query(conn: sqlite3.Connection, query: str, params: tuple = ()) -> Any:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.fetchall()

    @staticmethod
    def retry_query(conn: sqlite3.Connection, query: str, params: tuple = (), retries: int = 3, delay: int = 1) -> Any:
        return retry_on_exception(lambda: DatabaseUtils.execute_query(conn, query, params), retries, delay)

def extract_and_scale_features(market_data: Dict) -> np.ndarray:
    """Extract and scale features from market data"""
    try:
        # Convert market data to DataFrame if needed
        if isinstance(market_data, dict):
            if 'ohlcv' in market_data:
                df = pd.DataFrame(market_data['ohlcv'])
            else:
                df = pd.DataFrame(market_data)
        else:
            df = pd.DataFrame(market_data)

        # Ensure we have expected columns
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing required columns. Found: {df.columns.tolist()}")

        # Calculate basic features
        features = pd.DataFrame()
        
        # Price-based features
        features['close_returns'] = df['close'].pct_change()
        features['high_low_ratio'] = (df['high'] - df['low']) / df['close']
        features['close_to_open'] = (df['close'] - df['open']) / df['open']
        
        # Volume features
        features['volume_change'] = df['volume'].pct_change()
        features['volume_ma_ratio'] = df['volume'] / df['volume'].rolling(20).mean()
        
        # Technical indicators
        features['ma_20'] = df['close'].rolling(window=20).mean()
        features['ma_50'] = df['close'].rolling(window=50).mean()
        features['ma_ratio'] = features['ma_20'] / features['ma_50']
        
        # Volatility
        features['volatility'] = df['close'].rolling(window=20).std()
        features['atr'] = calculate_atr(df)
        
        # Momentum
        features['rsi'] = calculate_rsi(df['close'])
        features['momentum'] = df['close'].diff(10) / df['close'].shift(10)
        
        # Clean and scale features
        features = features.replace([np.inf, -np.inf], np.nan)
        features = features.fillna(method='ffill').fillna(method='bfill')
        
        # Simple standardization
        for col in features.columns:
            mean = features[col].mean()
            std = features[col].std()
            if std > 0:
                features[col] = (features[col] - mean) / std
            else:
                features[col] = 0
        
        return features.values
        
    except Exception as e:
        logger.error(f"Error extracting features: {e}")
        # Return empty feature set that won't break downstream processing
        return np.zeros((1, 10))

def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calculate Average True Range"""
    try:
        high = df['high']
        low = df['low']
        close = df['close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        
        return atr
        
    except Exception as e:
        logger.error(f"Error calculating ATR: {e}")
        return pd.Series(0, index=df.index)

def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index"""
    try:
        delta = prices.diff()
        
        # Separate gains and losses
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        
        # Calculate average gains and losses
        avg_gains = gains.rolling(window=period).mean()
        avg_losses = losses.rolling(window=period).mean()
        
        # Calculate RS and RSI
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
        
    except Exception as e:
        logger.error(f"Error calculating RSI: {e}")
        return pd.Series(50, index=prices.index)
