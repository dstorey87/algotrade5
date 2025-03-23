#!/usr/bin/env python
import os
import sys
import logging
import psutil
import numpy as np
import pandas as pd
import torch
from datetime import datetime, timedelta
# REMOVED_UNUSED_CODE: from typing import Dict, List
# REMOVED_UNUSED_CODE: import ccxt
import json

# Add FreqTrade modules to path
freqtrade_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(freqtrade_path)

# REMOVED_UNUSED_CODE: from freqtrade.persistence import Trade
from freqtrade.configuration import Configuration
from freqtrade.resolvers import StrategyResolver
from freqtrade.exchange import Exchange
# REMOVED_UNUSED_CODE: from freqtrade.data.history import load_pair_history
from pathlib import Path

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class ModelTester:
    def __init__(self):
        try:
            # Load config
            config_path = Path('user_data/config.json')
            if not config_path.exists():
                raise FileNotFoundError(f"Config file not found at {config_path}")
            
            self.config = Configuration.from_files([str(config_path)])
            
            # Initialize exchange
            self.exchange = Exchange(self.config)
            
            # Initialize strategy
            strategy_name = self.config.get('strategy', 'FreqAIStrategy')
            self.strategy = StrategyResolver.load_strategy(self.config)
            logger.info(f"Successfully loaded strategy: {strategy_name}")
            
            # Setup trade models
# REMOVED_UNUSED_CODE:             Trade.use_db = False
            
            # Initialize resource tracking
            self.resource_logs = []
            logger.info("Successfully initialized test environment")
            
        except Exception as e:
            logger.error(f"Error in initialization: {e}")
            raise
        
        self.resource_logs = []
        
    def load_test_data(self) -> pd.DataFrame:
        """Load test dataset directly from exchange"""
        try:
            timeframe = "5m"
            pairs = ["BTC/USDT"]
            
            candles = self.exchange.refresh_latest_ohlcv(
                pair_list=pairs,
                timeframe=timeframe,
                since_ms=int((datetime.now() - timedelta(days=1)).timestamp() * 1000)
            )
            
            if not candles or "BTC/USDT" not in candles:
                raise ValueError("Failed to fetch candle data")
                
            df = candles["BTC/USDT"].copy()
            logger.info(f"Loaded {len(df)} candles of test data")
            return df
            
        except Exception as e:
            logger.error(f"Error loading test data: {e}")
            raise

    def monitor_resources(self) -> Dict:
        """Monitor system resources"""
        process = psutil.Process(os.getpid())
        resources = {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': process.cpu_percent(),
            'memory_mb': process.memory_info().rss / 1024 / 1024,
            'gpu_memory_mb': 0
        }
        
        if torch.cuda.is_available():
            resources['gpu_memory_mb'] = torch.cuda.memory_allocated() / 1024 / 1024
            
        self.resource_logs.append(resources)
        return resources

    def test_strategy_predictions(self, df: pd.DataFrame) -> Dict:
        """Test strategy's FreqAI predictions"""
        try:
            logger.info("Testing FreqAI predictions...")
            
            # Prepare dataframe using strategy's methods
            df = self.strategy.freqai_info["feature_pipeline"]["include_shifted_candles"](df)
            df = self.strategy.set_freqai_targets(df, {"pair": "BTC/USDT"})
            
            resources_start = self.monitor_resources()
            start_time = datetime.now()
            
            # Get predictions using strategy's methods
            predictions = self.strategy.predict(df)
            
            end_time = datetime.now()
            resources_end = self.monitor_resources()
            
            performance = {
                'model_type': 'FreqAI Strategy',
                'training_time': (end_time - start_time).total_seconds(),
                'memory_impact': resources_end['memory_mb'] - resources_start['memory_mb'],
                'gpu_memory_impact': resources_end['gpu_memory_mb'] - resources_start['gpu_memory_mb'],
                'prediction_count': len(predictions) if predictions is not None else 0
            }
            
            if predictions is not None:
                performance.update({
                    'mean_prediction': float(np.mean(predictions)),
                    'std_prediction': float(np.std(predictions))
                })
            
            logger.info(f"Strategy test results: {performance}")
            return performance
            
        except Exception as e:
            logger.error(f"Error testing strategy predictions: {e}")
            return {'error': str(e)}

    def analyze_thresholds(self, predictions: np.ndarray) -> Dict:
        """Analyze prediction thresholds"""
        try:
            percentiles = np.percentile(predictions, [10, 25, 50, 75, 90])
            return {
                'thresholds': {
                    'conservative': float(percentiles[1]),    # 25th percentile
                    'moderate': float(percentiles[2]),        # 50th percentile
                    'aggressive': float(percentiles[3])       # 75th percentile
                },
                'distribution': {
                    'mean': float(np.mean(predictions)),
                    'std': float(np.std(predictions)),
                    'min': float(np.min(predictions)),
                    'max': float(np.max(predictions))
                }
            }
        except Exception as e:
            logger.error(f"Error analyzing thresholds: {e}")
            return {'error': str(e)}

    def run_tests(self):
        """Run complete test suite"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'strategy_performance': None,
            'threshold_analysis': None,
            'resource_usage': []
        }
        
        try:
            # Load and prepare test data
            df = self.load_test_data()
            
            # Test strategy predictions
            perf = self.test_strategy_predictions(df)
            results['strategy_performance'] = perf
            
            # Analyze prediction thresholds if available
            if 'error' not in perf and 'predictions' in perf:
                results['threshold_analysis'] = self.analyze_thresholds(perf['predictions'])
            
            # Add resource logs
            results['resource_usage'] = [
                {k: v for k, v in log.items() if k != 'timestamp'}
                for log in self.resource_logs
            ]
            
            # Save results
            output_file = "model_test_results.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=4)
            
            logger.info(f"Test results saved to {output_file}")
            return results
            
        except Exception as e:
            logger.error(f"Error running tests: {e}")
            results['error'] = str(e)
            
            # Save error results
            with open("model_test_error.json", 'w') as f:
                json.dump(results, f, indent=4)
            raise

if __name__ == "__main__":
    try:
        logger.info("Starting model tests...")
        tester = ModelTester()
        results = tester.run_tests()
        logger.info("Tests completed successfully")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Test run failed: {e}")
        sys.exit(1)
