import unittest
from pathlib import Path
import sys

class SystemReadinessTest(unittest.TestCase):
    def setUp(self):
        self.base_path = Path("C:/AlgoTradPro5")
        self.required_paths = [
            "models/llm",
            "models/ml",
            "src/core",
            "data",
            "trade_logs"
        ]
        
    def test_directory_structure(self):
        for path in self.required_paths:
            full_path = self.base_path / path
            self.assertTrue(full_path.exists(), f"Required directory missing: {path}")
            
    def test_model_availability(self):
        model_path = self.base_path / "models"
        required_models = ["deepseek", "mistral", "mixtral", "qwen"]
        for model in required_models:
            self.assertTrue(any((model_path / "llm").glob(f"{model}*")))

if __name__ == "__main__":
    unittest.main()
