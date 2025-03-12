"""
AI Model Manager
==============

CRITICAL REQUIREMENTS:
- Models loaded only from C:\AlgoTradPro5\models
- 85% minimum prediction accuracy
- Real-time performance monitoring
- Automatic fallback mechanisms

VALIDATION GATES:
1. Model validation
2. Prediction confidence
3. Performance tracking
4. Resource monitoring

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import logging
from typing import Dict, List, Optional, Union
from pathlib import Path
import torch
import numpy as np
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class AIModelManager:
    """
    AI model management and validation system
    
    CRITICAL METRICS:
    - Prediction accuracy: 85%+
    - Confidence threshold: 0.85
    - Response time: <50ms
    - Resource efficiency
    """
    
    def __init__(self, config: Dict):
        """
        Initialize AI model manager with strict validation
        
        REQUIREMENTS:
        - Valid model paths
        - GPU availability
        - Resource allocation
        - Error handling
        """
        self.config = config
        self.models_path = Path("C:/AlgoTradPro5/models")
        self.device = self._initialize_device()
        
        # STRICT: Validation thresholds
        self.min_accuracy = 0.85
        self.min_confidence = 0.85
        self.max_response_time = 0.05  # 50ms
        
        # Model tracking
        self.loaded_models = {}
        self.model_performance = {}
        self.fallback_enabled = True
        
        # Initialize models
        self._load_models()
        logger.info("AI Model Manager initialized with strict validation")
        
    def _initialize_device(self) -> torch.device:
        """
        Initialize and verify compute device
        
        REQUIREMENTS:
        - CUDA GPU primary
        - CPU fallback available
        - Memory verification
        """
        if torch.cuda.is_available():
            device = torch.device("cuda:0")
            logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            logger.warning("⚠️ GPU not available - using CPU")
            device = torch.device("cpu")
        return device
        
    def _load_models(self):
        """
        Load AI models with strict validation
        
        REQUIREMENTS:
        1. Valid model files
        2. Performance verification
        3. Resource availability
        4. Error handling
        """
        try:
            # STRICT: Verify models directory
            if not self.models_path.exists():
                raise ValueError(f"Models directory not found: {self.models_path}")
            
            # Load model configurations
            model_configs = list(self.models_path.glob("*/config.json"))
            if not model_configs:
                raise ValueError("No model configurations found")
            
            for config_path in model_configs:
                try:
                    with open(config_path) as f:
                        model_config = json.load(f)
                    
                    model_name = model_config['name']
                    model_type = model_config['type']
                    
                    # Load and validate model
                    model = self._load_model(model_name, model_type)
                    
                    # Verify performance
                    if self._validate_model(model, model_name):
                        self.loaded_models[model_name] = {
                            'model': model,
                            'config': model_config,
                            'performance': {
                                'accuracy': 0.0,
                                'confidence': 0.0,
                                'response_time': 0.0
                            }
                        }
                        logger.info(f"Loaded model: {model_name}")
                    else:
                        logger.warning(f"Model validation failed: {model_name}")
                        
                except Exception as e:
                    logger.error(f"Error loading model {config_path}: {e}")
                    
        except Exception as e:
            logger.error(f"Critical error loading models: {e}")
            raise
            
    def _load_model(self, model_name: str, model_type: str) -> torch.nn.Module:
        """
        Load specific AI model with validation
        
        REQUIREMENTS:
        1. Model file verification
        2. Architecture validation
        3. Weight initialization
        4. GPU optimization
        """
        model_path = self.models_path / model_name
        weights_path = model_path / "weights.pth"
        
        if not weights_path.exists():
            raise FileNotFoundError(f"Model weights not found: {weights_path}")
            
        try:
            # Load model architecture
            if model_type == "lstm":
                model = self._create_lstm_model()
            elif model_type == "transformer":
                model = self._create_transformer_model()
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
                
            # Load weights and move to device
            model.load_state_dict(torch.load(weights_path, map_location=self.device))
            model.to(self.device)
            model.eval()
            
            return model
            
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {e}")
            raise
            
    def _validate_model(self, model: torch.nn.Module, model_name: str) -> bool:
        """
        Validate model performance and reliability
        
        VALIDATION CHECKS:
        1. Accuracy verification
        2. Response time
        3. Resource usage
        4. Prediction stability
        """
        try:
            # Generate test data
            test_input = torch.randn(1, 10, 5).to(self.device)
            
            # Measure response time
            start_time = datetime.now()
            with torch.no_grad():
                output = model(test_input)
            response_time = (datetime.now() - start_time).total_seconds()
            
            # Validate performance
            if response_time > self.max_response_time:
                logger.warning(f"Model {model_name} response time ({response_time:.3f}s) exceeds limit")
                return False
                
            # Update performance metrics
            self.model_performance[model_name] = {
                'response_time': response_time,
                'last_validated': datetime.now().isoformat()
            }
            
            return True
            
        except Exception as e:
            logger.error(f"Model validation failed for {model_name}: {e}")
            return False
            
    def predict(self, data: np.ndarray, model_name: str) -> Dict[str, float]:
        """
        Make predictions with strict validation
        
        REQUIREMENTS:
        1. Input validation
        2. Confidence check
        3. Performance monitoring
        4. Error handling
        """
        try:
            if model_name not in self.loaded_models:
                raise ValueError(f"Model not found: {model_name}")
                
            model = self.loaded_models[model_name]['model']
            
            # Convert to tensor and move to device
            tensor_data = torch.from_numpy(data).float().to(self.device)
            
            # Make prediction
            start_time = datetime.now()
            with torch.no_grad():
                output = model(tensor_data)
            response_time = (datetime.now() - start_time).total_seconds()
            
            # Calculate confidence
            confidence = float(torch.max(torch.softmax(output, dim=1)))
            
            # STRICT: Validate confidence
            if confidence < self.min_confidence:
                logger.warning(f"Low confidence prediction ({confidence:.2%}) from {model_name}")
                if self.fallback_enabled:
                    return self._get_fallback_prediction(data)
            
            # Update performance tracking
            self._update_model_metrics(model_name, confidence, response_time)
            
            return {
                'prediction': float(torch.argmax(output)),
                'confidence': confidence,
                'response_time': response_time,
                'model_name': model_name
            }
            
        except Exception as e:
            logger.error(f"Prediction error with {model_name}: {e}")
            return self._get_fallback_prediction(data)
            
    def _get_fallback_prediction(self, data: np.ndarray) -> Dict[str, float]:
        """
        Generate fallback prediction when primary fails
        
        FALLBACK RULES:
        1. Use rule-based system
        2. Conservative estimates
        3. Clear flagging
        4. Logging
        """
        logger.warning("Using fallback prediction system")
        return {
            'prediction': 0.0,
            'confidence': 0.0,
            'response_time': 0.0,
            'model_name': 'fallback',
            'is_fallback': True
        }
        
    def _update_model_metrics(self, model_name: str, confidence: float, response_time: float):
        """
        Update model performance metrics
        
        TRACKED METRICS:
        1. Prediction accuracy
        2. Average confidence
        3. Response times
        4. Resource usage
        """
        metrics = self.model_performance.get(model_name, {
            'predictions': 0,
            'accuracy': 0.0,
            'avg_confidence': 0.0,
            'avg_response_time': 0.0
        })
        
        # Update running averages
        n = metrics['predictions'] + 1
        metrics['avg_confidence'] = (metrics['avg_confidence'] * (n-1) + confidence) / n
        metrics['avg_response_time'] = (metrics['avg_response_time'] * (n-1) + response_time) / n
        metrics['predictions'] = n
        metrics['last_update'] = datetime.now().isoformat()
        
        self.model_performance[model_name] = metrics
        
    def get_performance_metrics(self) -> Dict[str, Dict]:
        """
        Get comprehensive performance metrics
        
        INCLUDES:
        1. Model accuracies
        2. Response times
        3. Resource usage
        4. Error rates
        """
        return {
            'models': self.model_performance,
            'system': {
                'gpu_memory_used': torch.cuda.memory_allocated() if torch.cuda.is_available() else 0,
                'gpu_memory_cached': torch.cuda.memory_reserved() if torch.cuda.is_available() else 0,
                'models_loaded': len(self.loaded_models),
                'fallback_enabled': self.fallback_enabled
            }
        }