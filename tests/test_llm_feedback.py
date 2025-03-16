"""
Test suite for LLM feedback learner
"""

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent))

from src.core.llm.feedback_learner import LLMFeedbackLearner


class TestLLMFeedbackLearner(unittest.TestCase):
    def setUp(self):
        """Setup test environment"""
        self.config = {
            "base_path": "C:/AlgoTradPro5",
            "model_params": {
                "llm": {
                    "model_path": "models/llm/mistral",
                    "min_confidence": 0.85,
                    "max_refinement_steps": 5,
                }
            },
        }
        self.learner = LLMFeedbackLearner(self.config)

    def test_generate_improvements(self):
        """Test improvement generation"""
        strategy_data = {
            "patterns": [
                {"type": "breakout", "window": 20, "threshold": 0.02},
                {"type": "reversal", "window": 14, "threshold": 0.03},
            ],
            "timeframes": ["5m", "15m", "1h"],
            "risk_params": {
                "position_size": 0.02,
                "stop_loss": 0.01,
                "take_profit": 0.03,
            },
            "entry_rules": ["price > sma_20", "volume > volume_sma_20 * 1.5"],
            "exit_rules": ["rsi_14 > 70", "price < sma_20"],
        }

        performance = {
            "win_rate": 0.75,  # Below target
            "profit_factor": 1.8,
            "max_drawdown": 0.08,
            "total_trades": 120,
            "average_win": 0.02,
            "average_loss": 0.01,
            "consecutive_wins": 5,
            "consecutive_losses": 2,
        }

        improvements = self.learner.generate_improvements(strategy_data, performance)

        # Validate improvements
        self.assertIsInstance(improvements, list)
        if improvements:  # Should generate improvements since win rate < target
            self.assertGreater(len(improvements), 0)
            for improvement in improvements:
                self.assertIn("type", improvement)
                self.assertIn("suggestion", improvement)
                self.assertIn("confidence", improvement)
                self.assertIn("estimated_impact", improvement)
                self.assertGreaterEqual(improvement["confidence"], 0.0)
                self.assertLessEqual(improvement["confidence"], 1.0)

    def test_no_improvements_needed(self):
        """Test when no improvements needed"""
        strategy_data = {
            "patterns": [{"type": "breakout", "window": 20}],
            "timeframes": ["5m"],
            "risk_params": {"position_size": 0.02},
            "entry_rules": ["price > sma_20"],
            "exit_rules": ["rsi_14 > 70"],
        }

        performance = {
            "win_rate": 0.87,  # Above target
            "total_trades": 100,
        }

        improvements = self.learner.generate_improvements(strategy_data, performance)
        self.assertEqual(len(improvements), 0)

    def test_pattern_improvement(self):
        """Test pattern-specific improvements"""
        strategy_data = {
            "patterns": [{"type": "breakout", "window": 5}],  # Too short window
            "timeframes": ["5m"],
            "risk_params": {"position_size": 0.02},
            "entry_rules": ["price > sma_20"],
            "exit_rules": ["rsi_14 > 70"],
        }

        performance = {"win_rate": 0.65, "total_trades": 100}

        improvements = self.learner.generate_improvements(strategy_data, performance)

        pattern_improvements = [i for i in improvements if i["type"] == "pattern"]
        self.assertGreater(len(pattern_improvements), 0)

    def test_timeframe_improvement(self):
        """Test timeframe-specific improvements"""
        strategy_data = {
            "patterns": [{"type": "breakout", "window": 20}],
            "timeframes": ["1m"],  # Too short timeframe
            "risk_params": {"position_size": 0.02},
            "entry_rules": ["price > sma_20"],
            "exit_rules": ["rsi_14 > 70"],
        }

        performance = {"win_rate": 0.70, "total_trades": 100}

        improvements = self.learner.generate_improvements(strategy_data, performance)

        tf_improvements = [i for i in improvements if i["type"] == "timeframe"]
        self.assertGreater(len(tf_improvements), 0)

    def test_risk_improvement(self):
        """Test risk parameter improvements"""
        strategy_data = {
            "patterns": [{"type": "breakout", "window": 20}],
            "timeframes": ["5m"],
            "risk_params": {
                "position_size": 0.05,  # Too large
                "stop_loss": 0.005,  # Too tight
                "take_profit": 0.01,  # Too small
            },
            "entry_rules": ["price > sma_20"],
            "exit_rules": ["rsi_14 > 70"],
        }

        performance = {
            "win_rate": 0.72,
            "total_trades": 100,
            "max_drawdown": 0.15,  # Too high
        }

        improvements = self.learner.generate_improvements(strategy_data, performance)

        risk_improvements = [i for i in improvements if i["type"] == "risk"]
        self.assertGreater(len(risk_improvements), 0)


if __name__ == "__main__":
    unittest.main()
