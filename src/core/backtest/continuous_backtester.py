"""
Continuous Backtester
==================

Real-time strategy validation system.

CRITICAL REQUIREMENTS:
- Quantum validation integration
- LLM feedback loop
- Multi-timeframe testing
- Forward/reverse testing
"""

import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from ..llm.feedback_learner import LLMFeedbackLearner
from ..quantum.quantum_optimizer import QuantumOptimizer
from ..risk.risk_manager import RiskManager

logger = logging.getLogger(__name__)


class ContinuousBacktester:
    def __init__(self, config: Dict):
        """Initialize continuous backtester"""
        self.config = config
        self.base_path = Path(config.get("base_path", "C:/AlgoTradPro5"))

        # Initialize components
        self.quantum_optimizer = QuantumOptimizer(
            n_qubits=config["model_params"]["quantum"]["n_qubits"],
            shots=config["model_params"]["quantum"]["shots"],
            use_gpu=config["model_params"]["quantum"]["use_gpu"],
        )

        self.llm_feedback = LLMFeedbackLearner(config)
        self.risk_manager = RiskManager(config)

        # Backtesting parameters
        self.min_trades = 100  # Minimum trades for validation
        self.validation_threshold = 0.85  # 85% minimum win rate
        self.max_drawdown = 0.10  # 10% maximum drawdown
        self.min_profit_factor = 2.0  # Minimum 2:1 reward/risk

        # Performance tracking
        self.backtest_results: List[Dict] = []
        self.validated_strategies: List[Dict] = []
        self.max_history = 1000

    async def validate_strategy(
        self, strategy_data: Dict, market_data: pd.DataFrame
    ) -> Dict:
        """
        Validate trading strategy

        Args:
            strategy_data: Strategy configuration
            market_data: Historical market data

        Returns:
            Validation results
        """
        try:
            # Run initial backtest
            backtest_results = await self._run_backtest(strategy_data, market_data)

            # Check if strategy meets requirements
            if self._validate_performance(backtest_results):
                logger.info("Strategy meets performance requirements")
                self.validated_strategies.append(
                    {
                        "strategy": strategy_data,
                        "results": backtest_results,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
                return backtest_results

            # Strategy needs improvement
            improvements = self.llm_feedback.generate_improvements(
                strategy_data, backtest_results
            )

            # Apply improvements and revalidate
            improved_results = None
            for improvement in improvements:
                improved_strategy = self._apply_improvement(strategy_data, improvement)

                # Validate improved strategy
                new_results = await self._run_backtest(improved_strategy, market_data)

                if self._validate_performance(new_results):
                    logger.info(
                        f"Strategy improved after applying {improvement['type']}"
                    )
                    improved_results = new_results
                    break

            # Return final results
            final_results = improved_results or backtest_results
            self._update_history(final_results)

            return final_results

        except Exception as e:
            logger.error(f"Strategy validation failed: {e}")
            return {}

    async def _run_backtest(self, strategy: Dict, market_data: pd.DataFrame) -> Dict:
        """Run strategy backtest"""
        try:
            results = {
                "trades": [],
                "equity_curve": [],
                "drawdowns": [],
                "win_rate": 0.0,
                "profit_factor": 0.0,
                "max_drawdown": 0.0,
                "total_trades": 0,
            }

            # Initialize metrics
            equity = self.config["trading_params"]["initial_capital"]
            peak_equity = equity
            current_drawdown = 0.0
            winning_trades = 0
            losing_trades = 0
            gross_profit = 0.0
            gross_loss = 0.0

            # Process each timeframe
            for timeframe in strategy["timeframes"]:
                # Resample data to timeframe
                tf_data = self._resample_data(market_data, timeframe)

                # Scan for patterns
                patterns = self._scan_patterns(tf_data, strategy["patterns"])

                # Validate patterns with quantum circuit
                valid_patterns = []
                for pattern in patterns:
                    validation = self.quantum_optimizer.analyze_pattern(pattern["data"])
                    if validation["confidence"] >= self.validation_threshold:
                        valid_patterns.append(pattern)

                # Execute trades
                for pattern in valid_patterns:
                    # Calculate position size
                    position_size = self.risk_manager.calculate_position_size(
                        pattern["pair"],
                        pattern["entry_price"],
                        equity * 0.2,  # Max 20% per trade
                    )

                    # Simulate trade
                    trade_result = self._simulate_trade(pattern, position_size, tf_data)

                    # Update metrics
                    equity += trade_result["profit"]
                    peak_equity = max(peak_equity, equity)
                    current_drawdown = (peak_equity - equity) / peak_equity
                    results["max_drawdown"] = max(
                        results["max_drawdown"], current_drawdown
                    )

                    if trade_result["profit"] > 0:
                        winning_trades += 1
                        gross_profit += trade_result["profit"]
                    else:
                        losing_trades += 1
                        gross_loss += abs(trade_result["profit"])

                    # Record trade
                    results["trades"].append(
                        {
                            "timestamp": trade_result["exit_time"],
                            "pair": pattern["pair"],
                            "profit": trade_result["profit"],
                            "profit_ratio": trade_result["profit"] / position_size,
                            "drawdown": current_drawdown,
                        }
                    )

                    # Record equity curve
                    results["equity_curve"].append(
                        {"timestamp": trade_result["exit_time"], "equity": equity}
                    )

                    # Record drawdown
                    results["drawdowns"].append(
                        {
                            "timestamp": trade_result["exit_time"],
                            "drawdown": current_drawdown,
                        }
                    )

            # Calculate final metrics
            total_trades = winning_trades + losing_trades
            results.update(
                {
                    "win_rate": winning_trades / total_trades
                    if total_trades > 0
                    else 0,
                    "profit_factor": gross_profit / gross_loss
                    if gross_loss > 0
                    else float("inf"),
                    "total_trades": total_trades,
                    "winning_trades": winning_trades,
                    "losing_trades": losing_trades,
                    "gross_profit": gross_profit,
                    "gross_loss": gross_loss,
                    "final_equity": equity,
                    "return_ratio": (
                        equity - self.config["trading_params"]["initial_capital"]
                    )
                    / self.config["trading_params"]["initial_capital"],
                }
            )

            return results

        except Exception as e:
            logger.error(f"Backtest failed: {e}")
            return {}

    def _validate_performance(self, results: Dict) -> bool:
        """Validate strategy performance"""
        try:
            if not results:
                return False

            # Check minimum trades
            if results["total_trades"] < self.min_trades:
                logger.warning(
                    f"Insufficient trades: {results['total_trades']} < {self.min_trades}"
                )
                return False

            # Check win rate
            if results["win_rate"] < self.validation_threshold:
                logger.warning(
                    f"Win rate too low: {results['win_rate']:.1%} < {self.validation_threshold:.1%}"
                )
                return False

            # Check drawdown
            if results["max_drawdown"] > self.max_drawdown:
                logger.warning(
                    f"Drawdown too high: {results['max_drawdown']:.1%} > {self.max_drawdown:.1%}"
                )
                return False

            # Check profit factor
            if results["profit_factor"] < self.min_profit_factor:
                logger.warning(
                    f"Profit factor too low: {results['profit_factor']:.1f} < {self.min_profit_factor:.1f}"
                )
                return False

            return True

        except Exception as e:
            logger.error(f"Performance validation failed: {e}")
            return False

    def _apply_improvement(self, strategy: Dict, improvement: Dict) -> Dict:
        """Apply strategy improvement"""
        try:
            improved_strategy = strategy.copy()

            if improvement["type"] == "pattern":
                # Modify pattern recognition parameters
                for pattern in improved_strategy["patterns"]:
                    if improvement["confidence"] > pattern.get("confidence", 0):
                        pattern.update(self._parse_pattern_improvement(improvement))

            elif improvement["type"] == "entry":
                # Update entry rules
                new_rules = self._parse_rule_improvement(
                    improvement, improved_strategy["entry_rules"]
                )
                improved_strategy["entry_rules"] = new_rules

            elif improvement["type"] == "exit":
                # Update exit rules
                new_rules = self._parse_rule_improvement(
                    improvement, improved_strategy["exit_rules"]
                )
                improved_strategy["exit_rules"] = new_rules

            elif improvement["type"] == "risk":
                # Update risk parameters
                risk_updates = self._parse_risk_improvement(improvement)
                improved_strategy["risk_params"].update(risk_updates)

            elif improvement["type"] == "timeframe":
                # Update timeframes
                new_timeframes = self._parse_timeframe_improvement(
                    improvement, improved_strategy["timeframes"]
                )
                improved_strategy["timeframes"] = new_timeframes

            return improved_strategy

        except Exception as e:
            logger.error(f"Failed to apply improvement: {e}")
            return strategy

    def _resample_data(self, data: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        """Resample market data to timeframe"""
        try:
            return data.resample(timeframe).agg(
                {
                    "open": "first",
                    "high": "max",
                    "low": "min",
                    "close": "last",
                    "volume": "sum",
                }
            )
        except Exception as e:
            logger.error(f"Data resampling failed: {e}")
            return data

    def _scan_patterns(self, data: pd.DataFrame, patterns: List[Dict]) -> List[Dict]:
        """Scan for trading patterns"""
        try:
            found_patterns = []

            for pattern in patterns:
                # Extract pattern window
                window_size = pattern["window"]
                for i in range(len(data) - window_size):
                    window = data.iloc[i : i + window_size]

                    # Check if window matches pattern
                    if self._match_pattern(window, pattern):
                        found_patterns.append(
                            {
                                "pair": pattern["pair"],
                                "data": window.values,
                                "entry_price": window.iloc[-1]["close"],
                                "timestamp": window.index[-1],
                                "pattern_type": pattern["type"],
                            }
                        )

            return found_patterns

        except Exception as e:
            logger.error(f"Pattern scanning failed: {e}")
            return []

    def _match_pattern(self, window: pd.DataFrame, pattern: Dict) -> bool:
        """Check if window matches pattern"""
        try:
            # Calculate pattern features
            features = self._calculate_features(window)

            # Compare with pattern definition
            for condition in pattern["conditions"]:
                feature = condition["feature"]
                operator = condition["operator"]
                value = condition["value"]

                if not self._evaluate_condition(features.get(feature), operator, value):
                    return False

            return True

        except Exception as e:
            logger.error(f"Pattern matching failed: {e}")
            return False

    def _calculate_features(self, data: pd.DataFrame) -> Dict:
        """Calculate technical features"""
        try:
            return {
                "trend": self._calculate_trend(data),
                "momentum": self._calculate_momentum(data),
                "volatility": self._calculate_volatility(data),
                "volume_profile": self._calculate_volume_profile(data),
            }
        except Exception as e:
            logger.error(f"Feature calculation failed: {e}")
            return {}

    def _evaluate_condition(
        self, feature_value: float, operator: str, threshold: float
    ) -> bool:
        """Evaluate pattern condition"""
        try:
            if operator == ">":
                return feature_value > threshold
            elif operator == "<":
                return feature_value < threshold
            elif operator == ">=":
                return feature_value >= threshold
            elif operator == "<=":
                return feature_value <= threshold
            elif operator == "==":
                return abs(feature_value - threshold) < 1e-6
            else:
                return False

        except Exception:
            return False

    def _simulate_trade(
        self, pattern: Dict, position_size: float, market_data: pd.DataFrame
    ) -> Dict:
        """Simulate trade execution"""
        try:
            entry_time = pattern["timestamp"]
            entry_price = pattern["entry_price"]

            # Find exit point
            exit_data = market_data[market_data.index > entry_time]
            exit_time = None
            exit_price = None

            for idx, row in exit_data.iterrows():
                # Check stop loss
                if row["low"] <= entry_price * (
                    1 - self.config["trading_params"]["stop_loss"]
                ):
                    exit_time = idx
                    exit_price = entry_price * (
                        1 - self.config["trading_params"]["stop_loss"]
                    )
                    break

                # Check take profit
                if row["high"] >= entry_price * (
                    1 + self.config["trading_params"]["take_profit"]
                ):
                    exit_time = idx
                    exit_price = entry_price * (
                        1 + self.config["trading_params"]["take_profit"]
                    )
                    break

            if exit_time is None or exit_price is None:
                # Use last available price if no exit triggered
                exit_time = exit_data.index[-1]
                exit_price = exit_data.iloc[-1]["close"]

            # Calculate profit
            profit = (exit_price - entry_price) * position_size

            return {"entry_time": entry_time, "exit_time": exit_time, "profit": profit}

        except Exception as e:
            logger.error(f"Trade simulation failed: {e}")
            return {
                "entry_time": pattern["timestamp"],
                "exit_time": pattern["timestamp"],
                "profit": 0.0,
            }

    def _calculate_trend(self, data: pd.DataFrame) -> float:
        """Calculate trend strength"""
        try:
            close_prices = data["close"].values
            x = np.arange(len(close_prices))
            slope, _ = np.polyfit(x, close_prices, 1)
            return slope / np.mean(close_prices)
        except Exception:
            return 0.0

    def _calculate_momentum(self, data: pd.DataFrame) -> float:
        """Calculate price momentum"""
        try:
            close_prices = data["close"].values
            return (close_prices[-1] - close_prices[0]) / close_prices[0]
        except Exception:
            return 0.0

    def _calculate_volatility(self, data: pd.DataFrame) -> float:
        """Calculate price volatility"""
        try:
            close_prices = data["close"].values
            returns = np.diff(close_prices) / close_prices[:-1]
            return np.std(returns)
        except Exception:
            return 0.0

    def _calculate_volume_profile(self, data: pd.DataFrame) -> float:
        """Calculate volume profile"""
        try:
            if "volume" not in data.columns:
                return 0.0
            return np.corrcoef(data["close"].values, data["volume"].values)[0, 1]
        except Exception:
            return 0.0

    def _update_history(self, results: Dict) -> None:
        """Update backtest history"""
        try:
            self.backtest_results.append(
                {"timestamp": datetime.now().isoformat(), "results": results}
            )

            # Maintain maximum history length
            if len(self.backtest_results) > self.max_history:
                self.backtest_results = self.backtest_results[-self.max_history :]

        except Exception as e:
            logger.error(f"History update failed: {e}")

    def _parse_pattern_improvement(self, improvement: Dict) -> Dict:
        """Parse pattern improvement suggestion"""
        try:
            # Extract parameters from suggestion
            params = {}

            if "window" in improvement["suggestion"].lower():
                params["window"] = int(re.findall(r"\d+", improvement["suggestion"])[0])

            if "threshold" in improvement["suggestion"].lower():
                params["threshold"] = float(
                    re.findall(r"[\d.]+", improvement["suggestion"])[0]
                )

            return params

        except Exception as e:
            logger.error(f"Pattern improvement parsing failed: {e}")
            return {}

    def _parse_rule_improvement(
        self, improvement: Dict, current_rules: List[str]
    ) -> List[str]:
        """Parse trading rule improvement"""
        try:
            rules = current_rules.copy()

            if "add" in improvement["suggestion"].lower():
                new_rule = improvement["suggestion"].split("add")[-1].strip()
                rules.append(new_rule)

            elif "remove" in improvement["suggestion"].lower():
                target = improvement["suggestion"].split("remove")[-1].strip()
                rules = [r for r in rules if target not in r.lower()]

            elif "modify" in improvement["suggestion"].lower():
                target = improvement["suggestion"].split("modify")[-1].strip()
                for i, rule in enumerate(rules):
                    if target in rule.lower():
                        rules[i] = target

            return rules

        except Exception as e:
            logger.error(f"Rule improvement parsing failed: {e}")
            return current_rules

    def _parse_risk_improvement(self, improvement: Dict) -> Dict:
        """Parse risk parameter improvement"""
        try:
            params = {}

            if "stop loss" in improvement["suggestion"].lower():
                params["stop_loss"] = float(
                    re.findall(r"[\d.]+", improvement["suggestion"])[0]
                )

            if "take profit" in improvement["suggestion"].lower():
                params["take_profit"] = float(
                    re.findall(r"[\d.]+", improvement["suggestion"])[0]
                )

            if "position size" in improvement["suggestion"].lower():
                params["position_size"] = float(
                    re.findall(r"[\d.]+", improvement["suggestion"])[0]
                )

            return params

        except Exception as e:
            logger.error(f"Risk improvement parsing failed: {e}")
            return {}

    def _parse_timeframe_improvement(
        self, improvement: Dict, current_timeframes: List[str]
    ) -> List[str]:
        """Parse timeframe improvement"""
        try:
            timeframes = current_timeframes.copy()

            if "add" in improvement["suggestion"].lower():
                new_tf = improvement["suggestion"].split("add")[-1].strip()
                timeframes.append(new_tf)

            elif "remove" in improvement["suggestion"].lower():
                target = improvement["suggestion"].split("remove")[-1].strip()
                timeframes = [tf for tf in timeframes if target not in tf.lower()]

            return list(set(timeframes))  # Remove duplicates

        except Exception as e:
            logger.error(f"Timeframe improvement parsing failed: {e}")
            return current_timeframes
