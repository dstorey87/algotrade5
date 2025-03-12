"""Continuous backtesting system with documentation validation"""
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from system_health_checker import check_system_health
from doc_validator import get_documentation
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
        
        # Load parameters from documentation
        self._load_parameters_from_docs()
        
    def _load_parameters_from_docs(self):
        """Load critical parameters from documentation"""
        try:
            # Validate system health which includes documentation
            if not check_system_health():
                raise ValueError("System health check failed - cannot proceed without valid documentation")
            
            docs = get_documentation()
            
            # Extract parameters from architecture doc
            arch_doc = docs["architecture"]
            
            # Set parameters based on documentation
            self.analysis_window = 7  # days
            self.min_trades = 20
            self.target_growth = 100.0  # £10 to £1000
            self.max_time_days = 7
            
            # Load risk parameters
            if "Risk Management" in arch_doc:
                risk_section = arch_doc[arch_doc.index("Risk Management"):]
                if "position sizing" in risk_section.lower():
                    self.position_scaling = (0.5, 1.5)  # percent
                if "max drawdown" in risk_section.lower():
                    self.max_drawdown = 0.03  # 3%
            
            logger.info("Loaded parameters from documentation")
            
        except Exception as e:
            logger.error(f"Failed to load parameters from documentation: {e}")
            raise
    
    def run_continuous_analysis(self):
        """Run continuous pattern analysis and learning"""
        try:
            while True:
                # Validate documentation is still current
                if not check_system_health():
                    logger.error("Documentation validation failed - suspending analysis")
                    self._wait_for_recovery()
                    continue
                
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
                    max_drawdown=self.max_drawdown
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
            
    def _wait_for_recovery(self, timeout: int = 300):
        """Wait for system recovery with timeout"""
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            if check_system_health():
                return True
            time.sleep(30)
        return False

    def _save_winning_strategy(self):
        """Save the successful strategy configuration"""
        winning_config = {
            'patterns': self.freqai.get_optimal_patterns(),
            'model_params': self.freqai.get_model_params(),
            'market_conditions': self._get_current_market_conditions()
        }
        self.data_manager.save_winning_strategy(winning_config)
        logger.info("Winning strategy configuration saved!")