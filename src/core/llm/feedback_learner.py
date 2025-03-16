"""
LLM-based feedback learning system for strategy improvement
"""

import json
import os
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class LLMFeedbackLearner:
    def __init__(self, config):
        """Initialize the LLM feedback learner"""
        self.config = config
        self.model_path = (
            Path(config["base_path"]) / config["model_params"]["llm"]["model_path"]
        )
        self.min_confidence = config["model_params"]["llm"]["min_confidence"]
        self.max_steps = config["model_params"]["llm"]["max_refinement_steps"]

        # Load model and tokenizer
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            torch_dtype=torch.float16 if self.device.type == "cuda" else torch.float32,
        ).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)

    def generate_improvements(self, strategy_data, performance):
        """Generate strategy improvements based on performance metrics"""
        if performance["win_rate"] >= 0.85:  # Target achieved
            return []

        improvements = []

        # Pattern improvements
        pattern_suggestions = self._analyze_patterns(
            strategy_data["patterns"], performance
        )
        improvements.extend(pattern_suggestions)

        # Timeframe improvements
        tf_suggestions = self._analyze_timeframes(
            strategy_data["timeframes"], performance
        )
        improvements.extend(tf_suggestions)

        # Risk management improvements
        risk_suggestions = self._analyze_risk_params(
            strategy_data["risk_params"], performance
        )
        improvements.extend(risk_suggestions)

        # Sort by confidence and estimated impact
        improvements.sort(
            key=lambda x: (x["confidence"], x["estimated_impact"]), reverse=True
        )

        return improvements

    def _analyze_patterns(self, patterns, performance):
        """Analyze trading patterns for potential improvements"""
        suggestions = []

        prompt = self._create_pattern_prompt(patterns, performance)
        response = self._get_llm_response(prompt)

        for improvement in response:
            if improvement["confidence"] >= self.min_confidence:
                suggestions.append(
                    {
                        "type": "pattern",
                        "suggestion": improvement["suggestion"],
                        "confidence": improvement["confidence"],
                        "estimated_impact": improvement["impact"],
                    }
                )

        return suggestions

    def _analyze_timeframes(self, timeframes, performance):
        """Analyze timeframes for potential improvements"""
        suggestions = []

        # Check for very short timeframes
        if "1m" in timeframes and performance["win_rate"] < 0.75:
            suggestions.append(
                {
                    "type": "timeframe",
                    "suggestion": "Consider removing 1m timeframe due to noise",
                    "confidence": 0.9,
                    "estimated_impact": 0.1,
                }
            )

        # Check for missing higher timeframes
        if not any(tf in timeframes for tf in ["4h", "1d"]):
            suggestions.append(
                {
                    "type": "timeframe",
                    "suggestion": "Add higher timeframes (4h/1d) for trend context",
                    "confidence": 0.85,
                    "estimated_impact": 0.08,
                }
            )

        return suggestions

    def _analyze_risk_params(self, risk_params, performance):
        """Analyze risk parameters for potential improvements"""
        suggestions = []

        # Check position sizing
        if risk_params.get("position_size", 0) > 0.02:
            suggestions.append(
                {
                    "type": "risk",
                    "suggestion": "Reduce position size to 2% maximum",
                    "confidence": 0.95,
                    "estimated_impact": 0.15,
                }
            )

        # Check stop loss
        if risk_params.get("stop_loss", 0) < 0.01:
            suggestions.append(
                {
                    "type": "risk",
                    "suggestion": "Increase stop loss to minimum 1%",
                    "confidence": 0.9,
                    "estimated_impact": 0.12,
                }
            )

        return suggestions

    def _create_pattern_prompt(self, patterns, performance):
        """Create prompt for pattern analysis"""
        prompt = {
            "instruction": "Analyze trading patterns and suggest improvements",
            "patterns": patterns,
            "performance": {
                k: v
                for k, v in performance.items()
                if k in ["win_rate", "profit_factor", "max_drawdown"]
            },
            "target_win_rate": 0.85,
        }
        return json.dumps(prompt)

    def _get_llm_response(self, prompt):
        """Get response from LLM model"""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=512,
                temperature=0.7,
                top_p=0.9,
                num_return_sequences=3,
            )

        responses = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)

        # Parse responses into improvements
        improvements = []
        for response in responses:
            try:
                improvement = json.loads(response)
                improvements.append(improvement)
            except json.JSONDecodeError:
                continue

        return improvements

    def save_feedback(self, strategy_id, improvements, success_rate):
        """Save feedback and success rate for future learning"""
        feedback_path = Path(self.config["base_path"]) / "data" / "feedback"
        feedback_path.mkdir(exist_ok=True)

        feedback_file = feedback_path / f"{strategy_id}_feedback.json"
        feedback_data = {
            "improvements": improvements,
            "success_rate": success_rate,
            "timestamp": str(pd.Timestamp.now()),
        }

        with open(feedback_file, "w") as f:
            json.dump(feedback_data, f, indent=2)
