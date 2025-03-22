"""FreqAI Interface with continuous learning and pattern analysis"""

import logging
import os
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
# Use proper imports for these modules
from core.data_manager import DataManager
from core.trade_journal import TradeJournal

logger = logging.getLogger(__name__)


class FreqAIInterface:
    """Interface between FreqTrade and AlgoTradPro5's AI components"""

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.trade_journal = TradeJournal()
        self.data_manager = DataManager()
        self.min_pattern_confidence = 0.75
        self.min_success_trades = 10

    def analyze_trade_patterns(self, trades_df: pd.DataFrame) -> Dict:
        """Analyze trade patterns and outcomes"""
        try:
            patterns_analysis = {}

            for pattern in self._extract_patterns(trades_df):
                pattern_trades = trades_df[
                    trades_df["patterns"].str.contains(pattern, na=False)
                ]

                if len(pattern_trades) < self.min_success_trades:
                    continue

                win_rate = len(
                    pattern_trades[pattern_trades["profit_ratio"] > 0]
                ) / len(pattern_trades)

                if win_rate >= self.min_pattern_confidence:
                    patterns_analysis[pattern] = {
                        "pattern_name": pattern,
                        "win_rate": win_rate,
                        "total_trades": len(pattern_trades),
                        "successful_trades": len(
                            pattern_trades[pattern_trades["profit_ratio"] > 0]
                        ),
                        "avg_profit_ratio": pattern_trades["profit_ratio"].mean(),
                        "timestamp": pd.Timestamp.now().isoformat(),
                        "market_regime": self._detect_market_regime(pattern_trades),
                    }

                    # Store successful pattern
                    self.data_manager.catalog_successful_pattern(
                        patterns_analysis[pattern]
                    )

            return patterns_analysis

        except Exception as e:
            logger.error(f"Error analyzing trade patterns: {e}")
            return {}

    def _extract_patterns(self, trades_df: pd.DataFrame) -> List[str]:
        """Extract unique patterns from trades"""
        patterns = set()
        for patterns_str in trades_df["patterns"].dropna():
            patterns.update(patterns_str.split(","))
        return list(patterns)

    def _detect_market_regime(self, trades_df: pd.DataFrame) -> str:
        """Detect market regime from trade data"""
        if trades_df.empty:
            return "unknown"

        # Calculate trend metrics
        returns = trades_df["profit_ratio"]
        volatility = returns.std()
        trend = returns.mean()

        if volatility > 0.02:  # High volatility threshold
            if trend > 0.01:
                return "volatile_bullish"
            elif trend < -0.01:
                return "volatile_bearish"
            return "choppy"
        else:
            if trend > 0.005:
                return "trending_bullish"
            elif trend < -0.005:
                return "trending_bearish"
            return "ranging"

    def get_optimal_patterns(self, market_regime: Optional[str] = None) -> pd.DataFrame:
        """Get optimal trading patterns"""
        return self.data_manager.get_top_patterns(min_trades=self.min_success_trades)

    def recommend_trades(self, current_conditions: Dict) -> List[Dict]:
        """Recommend trades based on pattern analysis"""
        try:
            # Get winning conditions matching current market regime
            winning_conditions = self.data_manager.get_winning_conditions(
                min_trades=self.min_success_trades,
                min_success_rate=self.min_pattern_confidence,
            )

            if winning_conditions.empty:
                return []

            # Match current conditions against historical winners
            recommendations = []
            current_regime = self._detect_market_regime(
                pd.DataFrame([current_conditions])
            )

            for _, condition in winning_conditions.iterrows():
                if condition["market_regime"] == current_regime:
                    recommendations.append(
                        {
                            "pattern": condition["patterns"].split(",")[0],
                            "confidence": condition["success_rate"],
                            "profit_factor": condition["profit_factor"],
                            "regime": current_regime,
                        }
                    )

            return sorted(
                recommendations,
                key=lambda x: (x["confidence"], x["profit_factor"]),
                reverse=True,
            )

        except Exception as e:
            logger.error(f"Error recommending trades: {e}")
            return []

    def update_model(self, new_trades: pd.DataFrame):
        """Update AI model with new trade data"""
        try:
            # Analyze new patterns
            new_patterns = self.analyze_trade_patterns(new_trades)

            # Update pattern performance metrics
            for pattern_name, pattern_data in new_patterns.items():
                performance_data = {
                    "pattern_name": pattern_name,
                    "symbol": new_trades["symbol"].iloc[0],
                    "timeframe": "1h",  # Default timeframe
                    "win_rate": pattern_data["win_rate"],
                    "profit_ratio": pattern_data["avg_profit_ratio"],
                    "trade_count": pattern_data["total_trades"],
                    "market_regime": pattern_data["market_regime"],
                }

                self.data_manager.update_pattern_performance(performance_data)

            # Log model update
            logger.info(
                f"Updated model with {len(new_trades)} trades, "
                f"found {len(new_patterns)} significant patterns"
            )

        except Exception as e:
            logger.error(f"Error updating model: {e}")

    def get_performance_report(self) -> Dict:
        """Generate comprehensive performance report"""
        try:
            report = {
                "recent_performance": self.data_manager.get_recent_performance(
                    days=30, min_trades=self.min_success_trades
                ).to_dict("records"),
                "market_regime_summary": self.data_manager.get_market_regime_summary().to_dict(
                    "records"
                ),
                "top_patterns": self.data_manager.get_top_patterns(
                    min_trades=self.min_success_trades, limit=10
                ).to_dict("records"),
            }

            return report

        except Exception as e:
            logger.error(f"Error generating performance report: {e}")
            return {}
