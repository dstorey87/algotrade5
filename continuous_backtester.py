"""Continuous Backtester with Pattern Analysis"""
import logging
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Optional
from freqai_interface import FreqAIInterface
from data_manager import DataManager
from trade_journal import TradeJournal

logger = logging.getLogger(__name__)

class ContinuousBacktester:
    """Continuously backtest and analyze trading patterns"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.freqai = FreqAIInterface(config)
        self.data_manager = DataManager()
        self.trade_journal = TradeJournal()
        self.analysis_window = 7  # Reduced to 7 days for faster learning
        self.min_trades = 20  # Reduced minimum trades for faster adaptation
        self.target_growth = 100.0  # Target 100x growth (£10 to £1000)
        self.max_time_days = 7  # Maximum time window for target
        
    def run_continuous_analysis(self):
        """Run continuous pattern analysis and learning"""
        try:
            while True:
                # Get recent trades
                recent_trades = self.trade_journal.get_recent_trades(
                    days=self.analysis_window
                )
                
                if len(recent_trades) < self.min_trades:
                    logger.info(
                        f"Not enough trades ({len(recent_trades)}) "
                        f"for analysis. Minimum required: {self.min_trades}"
                    )
                    self._wait_for_next_analysis()
                    continue
                
                # Calculate current growth rate
                current_capital = self.get_current_capital()
                growth_rate = (current_capital / 10.0) - 1  # Starting from £10
                
                # Analyze patterns with focus on high-growth opportunities
                pattern_analysis = self.freqai.analyze_trade_patterns(
                    recent_trades,
                    min_profit_ratio=0.06,  # Focus on 6%+ profit trades
                    max_drawdown=0.03  # Limit risk to 3% per trade
                )
                
                # Update AI model with emphasis on growth
                self.freqai.update_model(
                    recent_trades,
                    target_metric='profit_ratio',
                    optimization_goal='maximize'
                )
                
                # Get winning patterns
                winning_patterns = self.freqai.get_optimal_patterns(
                    min_win_rate=0.75,
                    min_profit_factor=2.0
                )
                
                # Store backtest conditions
                for pattern in winning_patterns.itertuples():
                    condition = {
                        'timestamp': datetime.now().isoformat(),
                        'timerange': f"{self.analysis_window}d",
                        'success_rate': pattern.win_rate,
                        'total_trades': pattern.total_trades,
                        'profit_factor': pattern.avg_profit_ratio,
                        'market_regime': pattern.market_regime,
                        'patterns': pattern.pattern_name,
                        'growth_contribution': pattern.profit_ratio * pattern.win_rate
                    }
                    self.data_manager.catalog_backtest_condition(condition)
                
                # Generate and log performance report
                report = self.freqai.get_performance_report()
                self._log_performance(report)
                
                # Check if we've hit our target
                if growth_rate >= self.target_growth:
                    logger.info(f"🎯 Target growth achieved! Current capital: £{current_capital:.2f}")
                    self._save_winning_strategy()
                
                # Sleep for shorter interval during active trading
                self._wait_for_next_analysis()
                
        except Exception as e:
            logger.error(f"Error in continuous analysis: {e}")
            raise

    def _save_winning_strategy(self):
        """Save the successful strategy configuration"""
        winning_config = {
            'patterns': self.freqai.get_optimal_patterns(),
            'model_params': self.freqai.get_model_params(),
            'market_conditions': self._get_current_market_conditions()
        }
        self.data_manager.save_winning_strategy(winning_config)
        logger.info("Winning strategy configuration saved!")