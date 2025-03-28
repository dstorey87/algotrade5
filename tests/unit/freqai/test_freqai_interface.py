import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import json
import shutil
from pathlib import Path
import numpy as np

# Add the src directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# Import the freqai_interface module
from src.freqai_interface import ModelLoader, PredictionRequest, ModelMetrics

class TestFreqAIInterface(unittest.TestCase):
    """Test cases for the FreqAI interface"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a temporary test directory
        self.test_dir = Path("test_models")
        self.test_dir.mkdir(exist_ok=True)
        
        # Set environment variables for testing
        os.environ["MODEL_DIR"] = str(self.test_dir)
        os.environ["ML_MODELS_PATH"] = str(self.test_dir)
        
        # Create a mock freqai_config.json
        self.config = {
            "freqai": {
                "enabled": True,
                "identifier": "test"
            },
            "predictors": {
                "test_model": {
                    "model_path": "${ML_MODELS_PATH}/test_model",
                    "model_type": "LightGBMRegressor"
                }
            }
        }
        
        # Create metrics file
        self.metrics = {
            "test_model": {
                "accuracy": 0.85,
                "precision": 0.85,
                "recall": 0.85,
                "f1_score": 0.85,
                "win_rate": 0.85,
                "drawdown": 0.1
            }
        }
        
        # Create test model directory
        self.model_dir = self.test_dir / "test_model"
        self.model_dir.mkdir(exist_ok=True)
        
        # Write metrics file
        with open(self.test_dir / "metrics.json", "w") as f:
            json.dump(self.metrics, f)
            
    def tearDown(self):
        """Clean up after tests"""
        # Remove test directory
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    @patch("src.freqai_interface.ModelLoader._load_freqai_config")
    def test_model_loader_initialization(self, mock_load_config):
        """Test that the ModelLoader initializes correctly"""
        # Configure the mock
        mock_load_config.return_value = self.config
        
        # Create model loader
        loader = ModelLoader()
        
        # Verify it loads the config
        mock_load_config.assert_called_once()
        
        # Verify it has the expected attributes
        self.assertEqual(loader.model_dir, Path(os.environ["MODEL_DIR"]))
        self.assertEqual(loader.config, self.config)
        
        # Verify metrics loaded
        self.assertIn("test_model", loader.metrics)
        
    @patch("src.freqai_interface.ModelLoader._load_freqai_config")
    def test_get_model_metrics(self, mock_load_config):
        """Test getting model metrics"""
        # Configure the mock
        mock_load_config.return_value = self.config
        
        # Create model loader
        loader = ModelLoader()
        
        # Get metrics for existing model
        metrics = loader.get_model_metrics("test_model")
        self.assertIsInstance(metrics, ModelMetrics)
        self.assertEqual(metrics.accuracy, 0.85)
        
        # Get metrics for non-existent model (should return default metrics)
        metrics = loader.get_model_metrics("non_existent_model")
        self.assertIsInstance(metrics, ModelMetrics)
        self.assertEqual(metrics.accuracy, 0.85)  # Default value
        
    @patch("src.freqai_interface.ModelLoader._load_freqai_config")
    def test_resolve_model_path(self, mock_load_config):
        """Test resolving model paths with environment variables"""
        # Configure the mock
        mock_load_config.return_value = self.config
        
        # Create model loader
        loader = ModelLoader()
        
        # Resolve path for model in config
        path = loader._resolve_model_path("test_model")
        expected_path = Path(os.environ["ML_MODELS_PATH"]) / "test_model"
        self.assertEqual(path, expected_path)
        
        # Resolve path for model not in config
        path = loader._resolve_model_path("unknown_model")
        expected_path = Path(os.environ["MODEL_DIR"]) / "unknown_model"
        self.assertEqual(path, expected_path)
        
    @patch("src.freqai_interface.ModelLoader._load_freqai_config")
    def test_get_model_type(self, mock_load_config):
        """Test getting model type from config"""
        # Configure the mock
        mock_load_config.return_value = self.config
        
        # Create model loader
        loader = ModelLoader()
        
        # Get type for model in config
        model_type = loader._get_model_type("test_model")
        self.assertEqual(model_type, "LightGBMRegressor")
        
        # Get type for model not in config (should return default)
        model_type = loader._get_model_type("unknown_model")
        self.assertEqual(model_type, "LightGBMRegressor")  # Default value

    @patch("src.freqai_interface.ModelLoader._load_freqai_config")
    @patch("src.freqai_interface.ModelLoader._load_ml_model")
    def test_predict_with_ml_model(self, mock_load_ml_model, mock_load_config):
        """Test prediction with ML model"""
        # Configure the mocks
        mock_load_config.return_value = self.config
        
        # Mock the ML model
        mock_model = MagicMock()
        mock_model.predict.return_value = np.array([0.75])
        mock_load_ml_model.return_value = mock_model
        
        # Create model loader
        loader = ModelLoader()
        
        # Create features
        features = {
            "close": 50000.0,
            "volume": 1000.0,
            "rsi": 65.0,
            "feature1": 0.5,
            "feature2": -0.3
        }
        
        # Make prediction
        with patch.object(loader, "load_model", return_value=(mock_model, None)):
            prediction, confidence = loader._predict_with_ml_model(
                mock_model, "LightGBMRegressor", features
            )
        
        # Verify prediction is normalized to -1 or 1
        self.assertTrue(prediction in [1.0, -1.0])
        
        # Verify confidence is between 0 and 1
        self.assertTrue(0 <= confidence <= 1)

if __name__ == "__main__":
    unittest.main()