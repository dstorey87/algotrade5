from typing import Dict, List, Optional, Tuple

import pandas as pd

from freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqai.prediction_models.LightGBMRegressor import LightGBMRegressor


class QuantumLoopOptimizer:
    def __init__(self, config: dict):
        self.config = config
        self.current_best_winrate = 0.0
        self.current_best_strategy = None
        self.model_performance_history = []
        
    def optimize_strategy(self, strategy_params: dict, historical_data: pd.DataFrame) -> Tuple[dict, float]:
        """
        Continuously optimize strategy parameters using quantum-inspired optimization
        """
        model = LightGBMRegressor(config=self.config)
        
        # Split data into training and validation sets
        train_data, val_data = self._prepare_datasets(historical_data)
        
        # Train model on historical data
        trained_model = model.fit(train_data, strategy_params)
        
        # Evaluate strategy performance
        winrate, drawdown = self._evaluate_strategy(trained_model, val_data)
        
        # Store performance metrics
        self.model_performance_history.append({
            'winrate': winrate,
            'drawdown': drawdown,
            'params': strategy_params
        })
        
        # Update if this is the best performing strategy
        if winrate > self.current_best_winrate:
            self.current_best_winrate = winrate
            self.current_best_strategy = strategy_params
            
        return strategy_params, winrate

    def _prepare_datasets(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Prepare training and validation datasets"""
        split_idx = int(len(data) * 0.8)
        return data[:split_idx], data[split_idx:]

    def _evaluate_strategy(self, model, validation_data: pd.DataFrame) -> Tuple[float, float]:
        """Evaluate strategy performance on validation data"""
        predictions = model.predict(validation_data)
        
        # Calculate win rate and drawdown
        trades = self._simulate_trades(validation_data, predictions)
        winrate = len([t for t in trades if t['profit'] > 0]) / len(trades)
        drawdown = self._calculate_max_drawdown(trades)
        
        return winrate, drawdown

    def _simulate_trades(self, data: pd.DataFrame, predictions: np.ndarray) -> List[Dict]:
        """Simulate trades based on predictions"""
        trades = []
        position = None
        
        for i, pred in enumerate(predictions):
            if pred > 0.5 and position is None:  # Enter long
                position = {'entry_price': data.iloc[i]['close'],
                          'entry_time': data.iloc[i].name}
            elif pred < 0.5 and position:  # Exit long
                profit = (data.iloc[i]['close'] - position['entry_price']) / position['entry_price']
                trades.append({
                    'entry_time': position['entry_time'],
                    'exit_time': data.iloc[i].name,
                    'profit': profit
                })
                position = None
                
        return trades

    def _calculate_max_drawdown(self, trades: List[Dict]) -> float:
        """Calculate maximum drawdown from trade history"""
        equity_curve = [1.0]
        for trade in trades:
            equity_curve.append(equity_curve[-1] * (1 + trade['profit']))
        
        max_dd = 0
        peak = equity_curve[0]
        
        for value in equity_curve:
            if value > peak:
                peak = value
            dd = (peak - value) / peak
            if dd > max_dd:
                max_dd = dd
                
        return max_dd

    def get_best_strategy(self) -> Optional[dict]:
        """Return the best performing strategy parameters"""
        return self.current_best_strategy

    def get_performance_history(self) -> List[Dict]:
        """Return the history of strategy performances"""
        return self.model_performance_history