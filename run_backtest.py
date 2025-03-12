#!/usr/bin/env python3
"""Backtesting script for AlgoTradPro5"""
import os
import sys
import logging
import argparse
import subprocess
import torch
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from typing_extensions import TypeAlias

# Type aliases for pandas objects
DataFrame: TypeAlias = 'pd.DataFrame'
Series: TypeAlias = 'pd.Series'

# Setup CUDA environment before any GPU imports
sys.path.append(str(Path(__file__).parent))
from datetime import datetime, timedelta

from config_manager import ConfigManager
from ai_model_manager import AIModelManager
from quantum_optimizer import QuantumOptimizer
from strategy_engine import StrategyEngine
from error_manager import ErrorManager, ErrorCode
from data_manager import DataManager

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Add PyTorch import for GPU verification

def verify_gpu():
    """Verify GPU availability and setup"""
    try:
        if torch.cuda.is_available():
            logger.info(f"GPU detected: {torch.cuda.get_device_name(0)}")
            logger.info(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / (1024**2):.0f}MB")
            return True
        else:
            logger.warning("No GPU detected, using CPU mode")
            return False
            
    except Exception as e:
        logger.error(f"Error checking GPU: {e}")
        return False

def verify_models():
    """Verify AI models are available and load them"""
    try:
        config = ConfigManager()
        ai_manager = AIModelManager(config)
        # Temporarily allow rule-based fallbacks during testing
        ai_manager.set_require_ai(False)
        
        # Test model initialization
        logger.info("Verifying AI models...")
        if ai_manager._initialize_models():
            logger.info("AI models verified successfully")
            return True
            
        logger.info("Running download_models.py to get required models...")
        try:
            subprocess.check_call([sys.executable, "download_models.py"])
            logger.info("Models downloaded successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error downloading models: {e}")
            return False
            
    except Exception as e:
        logger.error(f"Error verifying AI models: {e}")
        return False

def import_or_install(package: str) -> any:
    """Import a package, installing it if necessary"""
    try:
        return __import__(package)
    except ImportError:
        logger.info(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return __import__(package)

# Import dependencies with auto-installation
pd = import_or_install('pandas')
np = import_or_install('numpy')
ccxt = import_or_install('ccxt')
ta = import_or_install('pandas_ta')  # Changed from pandas-ta to pandas_ta

# Import our risk management and trade journal
from risk_manager import RiskManager
from trade_journal import TradeJournal

class TradingStrategy:
    def __init__(self, params: Optional[Dict[str, Any]] = None):
        """Initialize strategy with parameters"""
        self.params = params or {}
        self.ai_manager = None
        self.quantum_optimizer = None
        self.risk_manager = None
        
        # Initialize components if specified
        if self.params.get('use_ai', True):
            config = ConfigManager()
            self.ai_manager = AIModelManager(config)
            self.ai_manager.set_require_ai(False)  # Allow fallback rules
            
        if self.params.get('use_quantum', True):
            self.quantum_optimizer = QuantumOptimizer(
                n_qubits=4, 
                shots=1000,
                use_gpu=verify_gpu()
            )
        
        # Initialize with sensible defaults
        self.risk_manager = RiskManager(
            initial_capital=self.params.get('initial_capital', 10_000),
            max_risk_per_trade=self.params.get('max_risk_per_trade', 0.01)
        )

    def calculate_indicators(self, df: DataFrame) -> DataFrame:
        """Calculate technical indicators for the dataframe"""
        if df.empty:
            return df
            
        try:
            # Calculate basic indicators
            # RSI
            df['rsi'] = ta.rsi(df['close'], length=14)
            
            # MACD
            macd = ta.macd(df['close'])
            df['macd'] = macd['MACD_12_26_9']
            df['macd_signal'] = macd['MACDs_12_26_9']
            df['macd_hist'] = macd['MACDh_12_26_9']
            
            # Bollinger Bands
            bb = ta.bbands(df['close'])
            df['bb_upper'] = bb['BBU_5_2.0']
            df['bb_middle'] = bb['BBM_5_2.0']
            df['bb_lower'] = bb['BBL_5_2.0']
            
            # Moving averages
            df['ema_9'] = ta.ema(df['close'], length=9)
            df['ema_21'] = ta.ema(df['close'], length=21)
            df['sma_50'] = ta.sma(df['close'], length=50)
            df['sma_200'] = ta.sma(df['close'], length=200)
            
            # ATR for volatility
            df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
            
            # Momentum
            df['mom'] = ta.mom(df['close'], length=10)
            
            # Fill NaN values
            df = df.bfill().ffill()
            
            return df
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return df
        
    def analyze_pattern(self, df: DataFrame, row_idx: int) -> Dict[str, Union[float, None]]:
        """Analyze price patterns at the given row index"""
        try:
            # Extract the relevant price data (lookback window)
            lookback = 20
            start_idx = max(0, row_idx - lookback)
            price_window = df.iloc[start_idx:row_idx + 1]
            
            # Use AI models if available
            ai_analysis = {}
            quantum_analysis = {}
            
            if self.ai_manager and row_idx >= lookback:
                features = self.ai_manager.extract_features(price_window)
                if features is not None:
                    ai_analysis = self.ai_manager.analyze_market(features)
            
            if self.quantum_optimizer and row_idx >= lookback:
                features = price_window[['open', 'high', 'low', 'close', 'volume']].values
                quantum_analysis = self.quantum_optimizer.analyze_pattern(features)
                
            # Combine AI and quantum analysis
            pattern_results = {
                'ai_confidence': ai_analysis.get('confidence', 0.5),
                'market_regime': ai_analysis.get('market_regime', 'unknown'),
                'trend': ai_analysis.get('trend', 'neutral'),
                'patterns': ai_analysis.get('patterns', []),
                'quantum_score': quantum_analysis.get('pattern_score', 0.5),
                'quantum_confidence': quantum_analysis.get('confidence', 0.5),
                'regime': quantum_analysis.get('regime', 0)
            }
            
            return pattern_results
            
        except Exception as e:
            logger.error(f"Error in pattern analysis: {e}")
            return {
                'ai_confidence': 0.5,
                'market_regime': 'unknown',
                'trend': 'neutral',
                'patterns': [],
                'quantum_score': 0.5,
                'quantum_confidence': 0.5,
                'regime': 0
            }
        
    def generate_signals(self, df: DataFrame, ai_analysis: Dict[str, Any], 
                        quantum_results: Dict[str, Any]) -> DataFrame:
        """Generate trading signals based on indicators and AI analysis"""
        try:
            # Initialize signal columns
            df['signal'] = 0       # 1 for buy, -1 for sell, 0 for hold
            df['stop_loss'] = None
            df['take_profit'] = None
            
            for i in range(1, len(df)):
                # Skip the first few candles for indicator warmup
                if i < 50:
                    continue
                    
                # Get current price and indicators
                current = df.iloc[i]
                prev = df.iloc[i-1]
                
                # Basic technical signals
                rsi_buy = current['rsi'] < 30 and prev['rsi'] < 30
                rsi_sell = current['rsi'] > 70 and prev['rsi'] > 70
                
                macd_buy = current['macd'] > current['macd_signal'] and prev['macd'] <= prev['macd_signal']
                macd_sell = current['macd'] < current['macd_signal'] and prev['macd'] >= prev['macd_signal']
                
                ma_buy = current['ema_9'] > current['ema_21'] and prev['ema_9'] <= prev['ema_21']
                ma_sell = current['ema_9'] < current['ema_21'] and prev['ema_9'] >= prev['ema_21']
                
                # Combine with AI signals if available
                ai_signal = 0
                if ai_analysis:
                    trend = ai_analysis.get('trend', 'neutral')
                    confidence = ai_analysis.get('confidence', 0.5)
                    
                    if trend in ['bullish', 'strongly_bullish'] and confidence > 0.65:
                        ai_signal = 1
                    elif trend in ['bearish', 'strongly_bearish'] and confidence > 0.65:
                        ai_signal = -1
                
                # Combine with quantum signals
                quantum_signal = 0
                if quantum_results:
                    score = quantum_results.get('pattern_score', 0.5)
                    regime = quantum_results.get('regime', 0)
                    
                    if score > 0.65 and regime > 0:
                        quantum_signal = 1
                    elif score > 0.65 and regime < 0:
                        quantum_signal = -1
                
                # Final signal logic
                if (rsi_buy or macd_buy or ma_buy) and (ai_signal >= 0 and quantum_signal >= 0):
                    df.at[df.index[i], 'signal'] = 1
                    
                    # Set stop loss and take profit
                    stop_price = current['close'] * 0.97  # 3% stop loss
                    tp_price = current['close'] * 1.06    # 6% take profit
                    df.at[df.index[i], 'stop_loss'] = stop_price
                    df.at[df.index[i], 'take_profit'] = tp_price
                    
                elif (rsi_sell or macd_sell or ma_sell) and (ai_signal <= 0 and quantum_signal <= 0):
                    df.at[df.index[i], 'signal'] = -1
            
            return df
            
        except Exception as e:
            logger.error(f"Error generating signals: {e}")
            return df
            
    def _find_local_minima(self, prices: Series) -> List[float]:
        """Find local minima in price series"""
        minima = []
        for i in range(1, len(prices) - 1):
            if prices[i-1] > prices[i] < prices[i+1]:
                minima.append(i)
        return minima
        
    def _find_local_maxima(self, prices: Series) -> List[float]:
        """Find local maxima in price series"""
        maxima = []
        for i in range(1, len(prices) - 1):
            if prices[i-1] < prices[i] > prices[i+1]:
                maxima.append(i)
        return maxima

class Backtester:
    def __init__(self, exchange_id: str = 'binance', timeframe: str = '1h'):
        """Initialize backtester with exchange and timeframe"""
        self.exchange_id = exchange_id
        self.timeframe = timeframe
        self.exchange = ccxt.exchange(exchange_id)
        self.data_manager = DataManager()
        
    def fetch_data(self, symbol: str, since: str, limit: int = 1000) -> DataFrame:
        """Fetch OHLCV data from exchange"""
        try:
            # Parse since date
            since_date = datetime.strptime(since, '%Y%m%d')
            since_timestamp = int(since_date.timestamp() * 1000)
            
            logger.info(f"Fetching {symbol} data from {since_date.strftime('%Y-%m-%d')}...")
            
            # Fetch data in chunks to handle large requests
            all_ohlcv = []
            current_since = since_timestamp
            
            while True:
                ohlcv = self.exchange.fetch_ohlcv(
                    symbol=symbol,
                    timeframe=self.timeframe,
                    since=current_since,
                    limit=limit
                )
                
                if not ohlcv or len(ohlcv) == 0:
                    break
                    
                all_ohlcv.extend(ohlcv)
                
                if len(ohlcv) < limit:
                    break
                    
                # Update since for next iteration
                current_since = ohlcv[-1][0] + 1
                
            # Convert to DataFrame
            df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            logger.info(f"Fetched {len(df)} candles for {symbol}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return pd.DataFrame()

    def run(self, symbol: str, since: str, strategy: TradingStrategy) -> Dict[str, Any]:
        """Run backtest for the given symbol and strategy"""
        try:
            # Fetch historical data
            data = self.fetch_data(symbol, since)
            if data.empty:
                return self._get_empty_results()
                
            # Calculate indicators
            data = strategy.calculate_indicators(data)
            
            # Analyze market using AI and quantum optimizer
            ai_analysis = {}
            quantum_results = {}
            
            if strategy.ai_manager:
                features = strategy.ai_manager.extract_features(data)
                if features is not None:
                    ai_analysis = strategy.ai_manager.analyze_market(features)
            
            if strategy.quantum_optimizer:
                features = data[['open', 'high', 'low', 'close', 'volume']].values
                quantum_results = strategy.quantum_optimizer.analyze_pattern(features)
                
            # Generate signals
            data = strategy.generate_signals(data, ai_analysis, quantum_results)
            
            # Simulate trades
            trades = []
            position = {
                'is_open': False,
                'entry_price': None,
                'entry_time': None,
                'stop_loss': None,
                'take_profit': None,
                'size': 0
            }
            
            initial_capital = strategy.risk_manager.initial_capital
            current_capital = initial_capital
            
            for i in range(1, len(data)):
                current = data.iloc[i]
                
                # Check if we need to close position based on stop loss or take profit
                if position['is_open']:
                    # Check for stop loss hit
                    if position['stop_loss'] and current['low'] <= position['stop_loss']:
                        # Close position at stop loss
                        exit_price = position['stop_loss']
                        profit_loss = (exit_price - position['entry_price']) * position['size']
                        
                        trades.append({
                            'entry_time': position['entry_time'],
                            'exit_time': current.name,
                            'entry_price': position['entry_price'],
                            'exit_price': exit_price,
                            'size': position['size'],
                            'pnl': profit_loss,
                            'pnl_pct': profit_loss / (position['entry_price'] * position['size']),
                            'exit_type': 'stop_loss'
                        })
                        
                        # Update capital
                        current_capital += profit_loss
                        position['is_open'] = False
                        
                    # Check for take profit hit
                    elif position['take_profit'] and current['high'] >= position['take_profit']:
                        # Close position at take profit
                        exit_price = position['take_profit']
                        profit_loss = (exit_price - position['entry_price']) * position['size']
                        
                        trades.append({
                            'entry_time': position['entry_time'],
                            'exit_time': current.name,
                            'entry_price': position['entry_price'],
                            'exit_price': exit_price,
                            'size': position['size'],
                            'pnl': profit_loss,
                            'pnl_pct': profit_loss / (position['entry_price'] * position['size']),
                            'exit_type': 'take_profit'
                        })
                        
                        # Update capital
                        current_capital += profit_loss
                        position['is_open'] = False
                        
                    # Check for exit signal
                    elif current['signal'] == -1:
                        # Close position at current price
                        exit_price = current['close']
                        profit_loss = (exit_price - position['entry_price']) * position['size']
                        
                        trades.append({
                            'entry_time': position['entry_time'],
                            'exit_time': current.name,
                            'entry_price': position['entry_price'],
                            'exit_price': exit_price,
                            'size': position['size'],
                            'pnl': profit_loss,
                            'pnl_pct': profit_loss / (position['entry_price'] * position['size']),
                            'exit_type': 'signal'
                        })
                        
                        # Update capital
                        current_capital += profit_loss
                        position['is_open'] = False
                
                # Check for entry signal if no open position
                if not position['is_open'] and current['signal'] == 1:
                    # Calculate position size based on risk
                    entry_price = current['close']
                    stop_loss = current['stop_loss']
                    
                    if strategy.risk_manager and stop_loss is not None:
                        position_size = strategy.risk_manager.calculate_position_size(
                            entry_price=entry_price,
                            stop_loss=stop_loss,
                            confidence_score=ai_analysis.get('confidence', 0.5)
                        )
                    else:
                        # Default to 5% of capital if no risk manager
                        position_size = current_capital * 0.05 / entry_price
                    
                    # Open position
                    position['is_open'] = True
                    position['entry_price'] = entry_price
                    position['entry_time'] = current.name
                    position['stop_loss'] = stop_loss
                    position['take_profit'] = current['take_profit']
                    position['size'] = position_size
            
            # Close any remaining open position at the end of the backtest
            if position['is_open']:
                exit_price = data.iloc[-1]['close']
                profit_loss = (exit_price - position['entry_price']) * position['size']
                
                trades.append({
                    'entry_time': position['entry_time'],
                    'exit_time': data.index[-1],
                    'entry_price': position['entry_price'],
                    'exit_price': exit_price,
                    'size': position['size'],
                    'pnl': profit_loss,
                    'pnl_pct': profit_loss / (position['entry_price'] * position['size']),
                    'exit_type': 'end_of_period'
                })
                
                # Update capital
                current_capital += profit_loss
            
            # Calculate backtest metrics
            metrics = self._calculate_backtest_metrics(trades, data)
            metrics['final_capital'] = current_capital
            metrics['total_return'] = (current_capital / initial_capital - 1) * 100
            metrics['symbol'] = symbol
            metrics['timeframe'] = self.timeframe
            metrics['start_date'] = data.index[0].strftime('%Y-%m-%d')
            metrics['end_date'] = data.index[-1].strftime('%Y-%m-%d')
            
            # Store results
            results = {
                'trades': trades,
                'metrics': metrics,
                'ai_analysis': ai_analysis,
                'quantum_results': quantum_results
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Error running backtest: {e}")
            return self._get_empty_results()

    def _calculate_backtest_metrics(self, trades: List[Dict[str, Any]], 
                                  data: DataFrame) -> Dict[str, Any]:
        """Calculate performance metrics for backtest"""
        if not trades:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'max_drawdown': 0,
                'sharpe_ratio': 0
            }
            
        # Extract PnL
        pnls = [trade['pnl'] for trade in trades]
        win_trades = [pnl for pnl in pnls if pnl > 0]
        loss_trades = [pnl for pnl in pnls if pnl <= 0]
        
        # Calculate metrics
        total_trades = len(trades)
        winning_trades = len(win_trades)
        losing_trades = len(loss_trades)
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        
        total_profit = sum(win_trades) if win_trades else 0
        total_loss = abs(sum(loss_trades)) if loss_trades else 0
        profit_factor = total_profit / total_loss if total_loss > 0 else float('inf')
        
        # Calculate drawdown
        balance_curve = []
        peak = 0
        drawdowns = []
        
        for trade in trades:
            pnl = trade['pnl']
            balance = balance_curve[-1] + pnl if balance_curve else pnl
            balance_curve.append(balance)
            
            # Update peak
            peak = max(peak, balance)
            
            # Calculate drawdown
            drawdown = (peak - balance) / peak if peak > 0 else 0
            drawdowns.append(drawdown)
        
        max_drawdown = max(drawdowns) if drawdowns else 0
        
        # Calculate Sharpe ratio (annualized)
        if len(pnls) > 1:
            returns = pd.Series(pnls)
            sharpe_ratio = returns.mean() / returns.std() * (252 ** 0.5) if returns.std() > 0 else 0
        else:
            sharpe_ratio = 0
            
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'avg_profit': sum(pnls) / len(pnls) if pnls else 0,
            'avg_win': sum(win_trades) / len(win_trades) if win_trades else 0,
            'avg_loss': sum(loss_trades) / len(loss_trades) if loss_trades else 0,
            'largest_win': max(win_trades) if win_trades else 0,
            'largest_loss': min(loss_trades) if loss_trades else 0
        }
        
    def _get_empty_results(self) -> Dict[str, Any]:
        """Return empty results structure"""
        return {
            'trades': [],
            'metrics': {
                'total_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'max_drawdown': 0,
                'sharpe_ratio': 0
            },
            'ai_analysis': {},
            'quantum_results': {}
        }

def main():
    parser = argparse.ArgumentParser(description='AlgoTradPro5 Safe Backtesting')
    
    parser.add_argument('--pairs', type=str, 
                      help='Trading pairs to backtest (comma-separated)',
                      default='BTC/USDT')
    parser.add_argument('--timeframe', type=str,
                      help='Timeframe for analysis (1m, 5m, 15m, 1h, 4h, 1d)',
                      default='15m')
    parser.add_argument('--timerange', type=str,
                      help='Timerange for backtesting (format: YYYYMMDD-YYYYMMDD)',
                      default='20230101-20240101')
    parser.add_argument('--exchange', type=str,
                      help='Exchange to use (default: binance)',
                      default='binance')
    
    args = parser.parse_args()
    
    try:
        # Verify GPU and models
        gpu_available = verify_gpu()
        models_available = verify_models()
        
        logger.info(f"GPU available: {gpu_available}, Models available: {models_available}")
        
        # Parse pairs
        pairs = args.pairs.split(',')
        start_date = args.timerange.split('-')[0]
        
        # Initialize strategy
        strategy = TradingStrategy({
            'use_ai': models_available,
            'use_quantum': gpu_available,
            'initial_capital': 10_000
        })
        
        # Initialize backtester
        backtester = Backtester(exchange_id=args.exchange, timeframe=args.timeframe)
        
        # Run backtest for each pair
        all_results = {}
        for pair in pairs:
            pair = pair.strip()
            logger.info(f"Running backtest for {pair} on {args.timeframe} timeframe")
            
            results = backtester.run(pair, start_date, strategy)
            all_results[pair] = results
            
            # Log results
            metrics = results['metrics']
            logger.info(f"Backtest completed for {pair}:")
            logger.info(f"  Total trades: {metrics.get('total_trades', 0)}")
            logger.info(f"  Win rate: {metrics.get('win_rate', 0):.2%}")
            logger.info(f"  Profit factor: {metrics.get('profit_factor', 0):.2f}")
            logger.info(f"  Max drawdown: {metrics.get('max_drawdown', 0):.2%}")
            logger.info(f"  Total return: {metrics.get('total_return', 0):.2f}%")
            logger.info(f"  Final capital: {metrics.get('final_capital', 0):.2f}")
        
        # Save results to file
        results_file = Path(f"backtest_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(results_file, 'w') as f:
            import json
            json.dump(all_results, f, default=str, indent=2)
            
        logger.info(f"Backtest results saved to {results_file}")
        
    except KeyboardInterrupt:
        logger.info("Backtest interrupted by user")
    except Exception as e:
        logger.error(f"Error running backtest: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Backtest interrupted by user")
    except Exception as e:
        logger.error(f"Error in main: {e}")