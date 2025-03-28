import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime

# Add the parent directory to the path to import the strategy
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import the strategy
from strategies.QuantumFreqAIStrategy import QuantumFreqAIStrategy

class TestQuantumFreqAIStrategy(unittest.TestCase):
    """
    Unit tests for QuantumFreqAIStrategy
    
    This test suite validates:
    1. Custom indicator calculations (no Talib)
    2. Strategy core functionality
    3. Risk management logic
    4. FreqAI integration
    """
    
    def setUp(self):
        """Setup test environment before each test method."""
        self.strategy = QuantumFreqAIStrategy({})
        
        # Create a sample dataframe for testing
        date_range = pd.date_range(start='2023-01-01', periods=100, freq='5min')
        self.sample_df = pd.DataFrame({
            'date': date_range,
            'open': np.random.normal(100, 5, 100),
            'high': np.random.normal(102, 5, 100),
            'low': np.random.normal(98, 5, 100),
            'close': np.random.normal(101, 5, 100),
            'volume': np.random.normal(1000, 200, 100).astype(int)
        })
        
        # Make sure high is always >= close >= low
        for i in range(len(self.sample_df)):
            self.sample_df.at[i, 'high'] = max(self.sample_df.at[i, 'high'], 
                                              self.sample_df.at[i, 'open'], 
                                              self.sample_df.at[i, 'close'])
            self.sample_df.at[i, 'low'] = min(self.sample_df.at[i, 'low'], 
                                             self.sample_df.at[i, 'open'], 
                                             self.sample_df.at[i, 'close'])
        
        self.sample_df.set_index('date', inplace=True)
        
        # Setup mock metadata
        self.metadata = {'pair': 'BTC/USDT'}
    
    def test_strategy_interface(self):
        """Test that the strategy implements the required interface."""
        self.assertEqual(self.strategy.INTERFACE_VERSION, 3)
        self.assertTrue(hasattr(self.strategy, 'populate_indicators'))
        self.assertTrue(hasattr(self.strategy, 'populate_entry_trend'))
        self.assertTrue(hasattr(self.strategy, 'populate_exit_trend'))
        self.assertTrue(hasattr(self.strategy, 'informative_pairs'))
    
    def test_rsi_calculation(self):
        """Test custom RSI calculation (no Talib)."""
        # Calculate RSI with our strategy
        rsi = self.strategy._calculate_rsi(self.sample_df, 14)
        
        # Basic validation
        self.assertIsInstance(rsi, pd.Series)
        self.assertEqual(len(rsi), len(self.sample_df))
        
        # Check that values are within expected range (0-100)
        self.assertTrue(rsi.dropna().between(0, 100).all())
    
    def test_mfi_calculation(self):
        """Test custom MFI calculation (no Talib)."""
        # Calculate MFI with our strategy
        mfi = self.strategy._calculate_mfi(self.sample_df, 14)
        
        # Basic validation
        self.assertIsInstance(mfi, pd.Series)
        self.assertEqual(len(mfi), len(self.sample_df))
        
        # Check that values are within expected range (0-100)
        self.assertTrue(mfi.dropna().between(0, 100).all())
    
    def test_cci_calculation(self):
        """Test custom CCI calculation (no Talib)."""
        # Calculate CCI with our strategy
        cci = self.strategy._calculate_cci(self.sample_df, 20)
        
        # Basic validation
        self.assertIsInstance(cci, pd.Series)
        self.assertEqual(len(cci), len(self.sample_df))
        
        # CCI can be any value but typically in range (-200, 200)
        # Just check it's not all NaN
        self.assertTrue(cci.notna().any())
    
    def test_fisher_transform(self):
        """Test Fisher Transform calculation."""
        # Calculate Fisher Transform with our strategy
        fisher = self.strategy._calculate_fisher_transform(self.sample_df, 10)
        
        # Basic validation
        self.assertIsInstance(fisher, pd.Series)
        self.assertEqual(len(fisher), len(self.sample_df))
        
        # Fisher transform values should be finite
        self.assertFalse(np.isinf(fisher.dropna()).any())
    
    def test_market_trend(self):
        """Test market trend calculation."""
        # Calculate market trend
        trend = self.strategy._calculate_market_trend(self.sample_df)
        
        # Basic validation
        self.assertIsInstance(trend, pd.Series)
        self.assertEqual(len(trend), len(self.sample_df))
        
        # Should only have -1, 0, or 1 values
        unique_values = trend.dropna().unique()
        self.assertTrue(all(val in [-1, 0, 1] for val in unique_values))
    
    def test_volatility(self):
        """Test volatility calculation."""
        # Calculate volatility
        vol = self.strategy._calculate_volatility(self.sample_df)
        
        # Basic validation
        self.assertIsInstance(vol, pd.Series)
        self.assertEqual(len(vol), len(self.sample_df))
        
        # Volatility should be non-negative
        self.assertTrue((vol.dropna() >= 0).all())
    
    def test_populate_indicators(self):
        """Test the indicator population method."""
        # Patch the freqai_config to avoid issues in testing
        original_config = self.strategy.freqai_config
        self.strategy.freqai_config = {
            "feature_parameters": {
                "indicator_periods_candles": [10],
                "label_period_candles": 10,
                "include_timeframes": ["5m", "15m"],
                "include_corr_pairlist": ["BTC/USDT"]
            }
        }
        
        # Run populate_indicators
        result_df = self.strategy.populate_indicators(self.sample_df.copy(), self.metadata)
        
        # Restore original config
        self.strategy.freqai_config = original_config
        
        # Check that all expected columns are present
        expected_columns = [
            'volume_mean', 'price_change', 'sma_10', 'ema_10', 'rsi_10', 
            'mfi_10', 'cci_10', 'bollinger_upper_10', 'bollinger_lower_10',
            'bollinger_width_10', 'vwap_10', 'fisher_transform_10', 
            'rsi', 'fisher_rsi', 'sar', 'market_trend', 'volatility',
            '&-future_price', '&-future_price_change', '&-up_or_down', '&-target'
        ]
        
        for col in expected_columns:
            self.assertIn(col, result_df.columns, f"Missing column: {col}")
        
        # Check that label columns start with '&-' as per FreqAI requirements
        label_cols = [col for col in result_df.columns if col.startswith('&-')]
        self.assertGreater(len(label_cols), 0)
    
    @patch('strategies.QuantumFreqAIStrategy.QuantumFreqAIStrategy._calculate_kelly')
    @patch('freqtrade.strategy.interface.IStrategy.dp')
    def test_populate_entry_trend(self, mock_dp, mock_calculate_kelly):
        """Test entry signal generation with mock FreqAI predictions."""
        # Setup mock FreqAI prediction
        mock_predictions = pd.DataFrame({
            'prediction': np.random.uniform(0, 1, len(self.sample_df)),
            'prediction_probability': np.random.uniform(0.5, 1, len(self.sample_df)),
            'target_prediction': np.random.choice([-1, 0, 1], len(self.sample_df)),
            'do_predict': np.ones(len(self.sample_df))
        }, index=self.sample_df.index)
        
        # Mock the FreqAI model
        mock_freqai_model = MagicMock()
        mock_freqai_model.predict.return_value = mock_predictions
        
        # Mock the dataprovider
        mock_dp.dataprovider_drivers = {"freqaimodel": mock_freqai_model}
        
        # Set up the Kelly coefficient mock
        mock_calculate_kelly.return_value = pd.Series(0.5, index=self.sample_df.index)
        
        # Set the mocked DP on the strategy
        self.strategy.dp = mock_dp
        self.strategy.freqai = True
        
        # Test with the sample dataframe
        result_df = self.strategy.populate_entry_trend(self.sample_df.copy(), self.metadata)
        
        # Verify that entry signals are present
        self.assertIn('enter_long', result_df.columns)
        self.assertIn('enter_short', result_df.columns)
        
        # Call count verification
        mock_freqai_model.predict.assert_called_once()
        mock_calculate_kelly.assert_called_once()
    
    def test_freqai_config(self):
        """Test that the FreqAI configuration is correctly structured."""
        required_keys = [
            "feature_parameters", 
            "data_split_parameters", 
            "model_training_parameters"
        ]
        
        for key in required_keys:
            self.assertIn(key, self.strategy.freqai_config)
        
        # Check essential feature parameters
        feature_params = self.strategy.freqai_config["feature_parameters"]
        self.assertIn("include_timeframes", feature_params)
        self.assertIn("include_corr_pairlist", feature_params)
        self.assertIn("label_period_candles", feature_params)
        self.assertIn("indicator_periods_candles", feature_params)
    
    def test_risk_management_parameters(self):
        """Test that risk management parameters are properly configured."""
        # Check risk per trade parameter
        self.assertTrue(hasattr(self.strategy, 'risk_per_trade'))
        self.assertEqual(self.strategy.risk_per_trade.default, 0.01)  # Default 1%
        self.assertEqual(self.strategy.risk_per_trade.low, 0.01)      # Min 1% 
        self.assertEqual(self.strategy.risk_per_trade.high, 0.02)     # Max 2%
        
        # Check max drawdown parameter
        self.assertTrue(hasattr(self.strategy, 'max_drawdown'))
        self.assertEqual(self.strategy.max_drawdown.default, 0.10)    # Default 10%
        self.assertEqual(self.strategy.max_drawdown.low, 0.05)        # Min 5%
        self.assertEqual(self.strategy.max_drawdown.high, 0.15)       # Max 15%

if __name__ == '__main__':
    unittest.main()