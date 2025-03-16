"""Continuous backtesting system with documentation validation"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from data_manager import DataManager
from doc_validator import get_documentation
from freqai_interface import FreqAIInterface
from quantum_optimizer import QuantumOptimizer
from system_health_checker import check_system_health
from trade_journal import TradeJournal

logger = logging.getLogger(__name__)


class ContinuousBacktester:
    """Continuously backtest and analyze trading patterns"""

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.freqai = FreqAIInterface(config)
        self.data_manager = DataManager()
        self.trade_journal = TradeJournal()

        # Initialize quantum optimizer
        self.quantum_optimizer = QuantumOptimizer(n_qubits=4, shots=1000, use_gpu=True)

        # Load parameters from documentation
        self._load_parameters_from_docs()

    def _load_parameters_from_docs(self):
        """Load critical parameters from documentation"""
        try:
            # Validate system health which includes documentation
            if not check_system_health():
                raise ValueError(
                    "System health check failed - cannot proceed without valid documentation"
                )

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
                risk_section = arch_doc[arch_doc.index("Risk Management") :]
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
                    logger.error(
                        "Documentation validation failed - suspending analysis"
                    )
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
                    max_drawdown=self.max_drawdown,
                )

                # Update AI model with emphasis on growth
                self.freqai.update_model(
                    recent_trades,
                    target_metric="profit_ratio",
                    optimization_goal="maximize",
                )

                # Get winning patterns
                winning_patterns = self.freqai.get_optimal_patterns(
                    min_win_rate=0.75, min_profit_factor=2.0
                )

                # Run quantum loop validation on winning patterns
                validated_patterns = []
                for pattern in winning_patterns.itertuples():
                    # Extract pattern data and prepare for quantum validation
                    pattern_data = self._extract_pattern_data(pattern)

                    # Perform quantum loop validation
                    validation_results = self._validate_pattern_quantum_loop(
                        pattern_data,
                        pattern_name=pattern.pattern_name,
                        pair=pattern.pair,
                        timeframe=pattern.timeframe,
                    )

                    if validation_results["validation_status"] == "validated":
                        validated_patterns.append(validation_results)
                        # Store validated pattern
                        self.data_manager.store_quantum_validated_pattern(
                            validation_results
                        )

                # Store backtest conditions with quantum validation results
                for pattern in winning_patterns.itertuples():
                    is_validated = any(
                        p["pattern_name"] == pattern.pattern_name
                        for p in validated_patterns
                    )
                    condition = {
                        "timestamp": datetime.now().isoformat(),
                        "timerange": f"{self.analysis_window}d",
                        "success_rate": pattern.win_rate,
                        "total_trades": pattern.total_trades,
                        "profit_factor": pattern.avg_profit_ratio,
                        "market_regime": pattern.market_regime,
                        "patterns": pattern.pattern_name,
                        "growth_contribution": pattern.profit_ratio * pattern.win_rate,
                        "quantum_validated": is_validated,
                    }
                    self.data_manager.catalog_backtest_condition(condition)

                # Generate and log performance report
                report = self.freqai.get_performance_report()
                self._log_performance(report)

                # Check if we've hit our target
                if growth_rate >= self.target_growth:
                    logger.info(
                        f"🎯 Target growth achieved! Current capital: £{current_capital:.2f}"
                    )
                    self._save_winning_strategy()

                # Sleep for shorter interval during active trading
                self._wait_for_next_analysis()

        except Exception as e:
            logger.error(f"Error in continuous analysis: {e}")
            raise

    def _validate_pattern_quantum_loop(
        self, pattern_data: np.ndarray, pattern_name: str, pair: str, timeframe: str
    ) -> Dict:
        """
        Perform quantum loop validation of a pattern
        Returns validation metrics including confidence and regime prediction
        """
        # Forward pass - analyze pattern as is
        forward_results = self.quantum_optimizer.analyze_pattern(pattern_data)

        # Backward pass - analyze pattern in reverse to verify robustness
        backward_data = np.flip(pattern_data.copy(), axis=0)
        backward_results = self.quantum_optimizer.analyze_pattern(backward_data)

        # Cross-validation - compare forward and backward analysis
        confidence_alignment = 1 - abs(
            forward_results["confidence"] - backward_results["confidence"]
        )
        regime_alignment = (forward_results["regime"] * -backward_results["regime"]) > 0

        # Prepare validation results
        validation_results = {
            "pattern_name": pattern_name,
            "pair": pair,
            "timeframe": timeframe,
            "entry_timestamp": datetime.now().isoformat(),
            "forward_score": forward_results["pattern_score"],
            "backward_score": backward_results["pattern_score"],
            "alignment_score": confidence_alignment,
            "confidence": min(
                forward_results["confidence"], backward_results["confidence"]
            ),
            "regime": forward_results["regime"],
            "market_conditions": self._get_current_market_conditions(),
            "pattern_data": pattern_data.tolist(),
            "validation_status": "validated"
            if confidence_alignment > 0.8 and regime_alignment
            else "failed",
            "validation_window": len(pattern_data),
        }

        return validation_results

    def _wait_for_recovery(self, timeout: int = 300):
        """Wait for system recovery with timeout"""
        import time

        start_time = time.time()
        while time.time() - start_time < timeout:
            if check_system_health():
                return True
            time.sleep(30)
        return False

    def _extract_pattern_data(self, pattern) -> np.ndarray:
        """Extract pattern data in the correct format for quantum analysis"""
        try:
            # Convert pattern features to numpy array
            pattern_features = [
                pattern.open_prices,
                pattern.high_prices,
                pattern.low_prices,
                pattern.close_prices,
                pattern.volumes,
            ]
            return np.array(pattern_features).T

        except Exception as e:
            logger.error(f"Error extracting pattern data: {e}")
            return np.array([])

    def _get_current_market_conditions(self) -> Dict:
        """Get current market conditions"""
        try:
            return {
                "volatility": self.freqai.get_market_volatility(),
                "trend": self.freqai.get_market_trend(),
                "volume_profile": self.freqai.get_volume_profile(),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error getting market conditions: {e}")
            return {}

    def _save_winning_strategy(self):
        """Save the successful strategy configuration"""
        winning_config = {
            "patterns": self.freqai.get_optimal_patterns(),
            "model_params": self.freqai.get_model_params(),
            "market_conditions": self._get_current_market_conditions(),
            "quantum_validated_patterns": self.data_manager.get_validated_patterns(
                min_confidence=0.85, validation_status="validated"
            ).to_dict("records"),
        }
        self.data_manager.save_winning_strategy(winning_config)
        logger.info("Winning strategy configuration saved!")
