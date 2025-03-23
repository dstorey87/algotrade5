import numpy as np
import pandas as pd
import pytest

from src.quantum_loop_optimizer import QuantumLoopOptimizer


@pytest.fixture
def sample_data():
    dates = pd.date_range(start='2024-01-01', periods=100, freq='1H')
    data = pd.DataFrame({
        'open': np.random.random(100) * 100,
        'high': np.random.random(100) * 100,
        'low': np.random.random(100) * 100,
        'close': np.random.random(100) * 100,
        'volume': np.random.random(100) * 1000
    }, index=dates)
    
    # Ensure high is always highest and low is always lowest
    data['high'] = data[['open', 'close', 'high']].max(axis=1)
    data['low'] = data[['open', 'close', 'low']].min(axis=1)
    return data

@pytest.fixture
def test_config():
    return {
        'max_drawdown': 0.1,
        'target_winrate': 0.85,
        'model_params': {
            'n_estimators': 100,
            'learning_rate': 0.1
        }
    }

def test_optimizer_initialization(test_config):
    optimizer = QuantumLoopOptimizer(test_config)
    assert optimizer.current_best_winrate == 0.0
    assert optimizer.current_best_strategy is None
    assert len(optimizer.model_performance_history) == 0

def test_strategy_optimization(test_config, sample_data):
    optimizer = QuantumLoopOptimizer(test_config)
    strategy_params = {
        'rsi_period': 14,
        'ma_period': 20,
        'profit_target': 0.02
    }
    
    new_params, winrate = optimizer.optimize_strategy(strategy_params, sample_data)
    
    assert isinstance(new_params, dict)
    assert isinstance(winrate, float)
    assert winrate >= 0.0 and winrate <= 1.0
    assert len(optimizer.get_performance_history()) > 0

def test_drawdown_calculation(test_config):
    optimizer = QuantumLoopOptimizer(test_config)
    trades = [
        {'profit': 0.01},
        {'profit': -0.02},
        {'profit': 0.015},
        {'profit': -0.01}
    ]
    
    max_dd = optimizer._calculate_max_drawdown(trades)
    assert isinstance(max_dd, float)
    assert max_dd >= 0.0 and max_dd <= 1.0

def test_dataset_preparation(test_config, sample_data):
    optimizer = QuantumLoopOptimizer(test_config)
    train, val = optimizer._prepare_datasets(sample_data)
    
    assert len(train) + len(val) == len(sample_data)
    assert len(train) > len(val)  # 80-20 split
    assert isinstance(train, pd.DataFrame)
    assert isinstance(val, pd.DataFrame)