"""
ML Model Manager
=============

Manages ML models for the quantum hybrid strategy.

CRITICAL REQUIREMENTS:
- Model versioning
- Performance tracking
- Quantum validation
- Real-time optimization
"""

import logging
from typing import Dict, List, Optional, Union
from datetime import datetime
from pathlib import Path
import torch
import numpy as np
from torch.cuda.amp import autocast
import json

from .lstm_model import LSTMModel
from ..quantum.quantum_optimizer import QuantumOptimizer
from ..data.data_manager import DataManager

logger = logging.getLogger(__name__)

class MLModelManager:
    def __init__(self, config: Dict):
        """Initialize ML model manager"""
        self.config = config
        self.base_path = Path(config.get('base_path', 'C:/AlgoTradPro5'))
        self.models_path = self.base_path / 'models' / 'ml'
        
        # Initialize components
        self.quantum_optimizer = QuantumOptimizer(
            n_qubits=4,
            shots=1000,
            use_gpu=True
        )
        self.data_manager = DataManager(config)
        
        # Load models
        self.models: Dict[str, torch.nn.Module] = {}
        self.model_configs: Dict[str, Dict] = {}
        self._load_models()
        
        # Performance tracking
        self.model_metrics: Dict[str, List[Dict]] = {}
        self.min_confidence = 0.85
        
        # GPU setup
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
    def predict(self,
               model_name: str,
               data: np.ndarray,
               validate: bool = True) -> Dict[str, Union[np.ndarray, float]]:
        """
        Make prediction with optional quantum validation
        
        Args:
            model_name: Name of model to use
            data: Input data array
            validate: Whether to validate with quantum circuit
            
        Returns:
            Dictionary with predictions and confidence scores
        """
        try:
            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")
                
            # Convert to tensor
            x = torch.tensor(data, dtype=torch.float32).to(self.device)
            
            # Make prediction
            model = self.models[model_name]
            model.eval()
            
            with torch.no_grad(), autocast(device_type='cuda'):
                predictions = model(x)
                
            # Convert to numpy
            predictions = predictions.cpu().numpy()
            
            # Quantum validation if requested
            confidence = 0.0
            if validate:
                validation = self.quantum_optimizer.analyze_pattern(data)
                confidence = validation['confidence']
                
                # Skip predictions with low confidence
                if confidence < self.min_confidence:
                    logger.warning(
                        f"Low confidence prediction ({confidence:.2%})"
                    )
                    return {
                        'predictions': np.zeros_like(predictions),
                        'confidence': confidence
                    }
            
            return {
                'predictions': predictions,
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {
                'predictions': np.array([]),
                'confidence': 0.0
            }
            
    def update_model(self,
                    model_name: str,
                    train_data: np.ndarray,
                    train_labels: np.ndarray) -> Dict[str, float]:
        """
        Update model with new training data
        
        Args:
            model_name: Name of model to update
            train_data: Training data array
            train_labels: Training labels array
            
        Returns:
            Dictionary with training metrics
        """
        try:
            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")
                
            # Convert to tensors
            x = torch.tensor(train_data, dtype=torch.float32).to(self.device)
            y = torch.tensor(train_labels, dtype=torch.float32).to(self.device)
            
            # Train model
            model = self.models[model_name]
            model.train()
            
            optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
            criterion = torch.nn.MSELoss()
            
            # Single update step
            optimizer.zero_grad()
            with autocast(device_type='cuda'):
                predictions = model(x)
                loss = criterion(predictions, y)
            
            loss.backward()
            optimizer.step()
            
            # Calculate metrics
            metrics = {
                'loss': loss.item(),
                'samples': len(train_data)
            }
            
            # Update tracking
            self._update_metrics(model_name, metrics)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Model update failed: {e}")
            return {'loss': float('inf'), 'samples': 0}
            
    def validate_model(self,
                      model_name: str,
                      val_data: np.ndarray,
                      val_labels: np.ndarray) -> Dict[str, float]:
        """
        Validate model performance
        
        Args:
            model_name: Name of model to validate
            val_data: Validation data array
            val_labels: Validation labels array
            
        Returns:
            Dictionary with validation metrics
        """
        try:
            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")
                
            # Convert to tensors
            x = torch.tensor(val_data, dtype=torch.float32).to(self.device)
            y = torch.tensor(val_labels, dtype=torch.float32).to(self.device)
            
            # Validate model
            model = self.models[model_name]
            model.eval()
            
            with torch.no_grad(), autocast(device_type='cuda'):
                predictions = model(x)
                mse = torch.nn.functional.mse_loss(predictions, y)
                mae = torch.nn.functional.l1_loss(predictions, y)
            
            # Calculate metrics
            metrics = {
                'mse': mse.item(),
                'mae': mae.item(),
                'samples': len(val_data)
            }
            
            # Quantum validation of critical predictions
            validation_results = []
            for i, pred in enumerate(predictions):
                if abs(pred.item()) > 0.5:  # Validate significant signals
                    validation = self.quantum_optimizer.analyze_pattern(
                        val_data[i]
                    )
                    validation_results.append(validation['confidence'])
            
            if validation_results:
                metrics['quantum_confidence'] = np.mean(validation_results)
            
            # Update tracking
            self._update_metrics(model_name, metrics)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Model validation failed: {e}")
            return {
                'mse': float('inf'),
                'mae': float('inf'),
                'samples': 0
            }
            
    def save_model(self, model_name: str) -> bool:
        """Save model to disk"""
        try:
            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")
                
            # Save model weights
            model = self.models[model_name]
            save_path = self.models_path / model_name
            save_path.mkdir(parents=True, exist_ok=True)
            
            torch.save(model.state_dict(), save_path / 'model.pt')
            
            # Save config
            if model_name in self.model_configs:
                with open(save_path / 'config.json', 'w') as f:
                    json.dump(self.model_configs[model_name], f)
            
            # Save metrics
            if model_name in self.model_metrics:
                with open(save_path / 'metrics.json', 'w') as f:
                    json.dump(self.model_metrics[model_name], f)
                    
            return True
            
        except Exception as e:
            logger.error(f"Model save failed: {e}")
            return False
            
    def load_model(self, model_name: str) -> bool:
        """Load model from disk"""
        try:
            model_path = self.models_path / model_name
            
            # Load config
            with open(model_path / 'config.json', 'r') as f:
                config = json.load(f)
                
            # Initialize model
            model = self._create_model(config)
            
            # Load weights
            model.load_state_dict(
                torch.load(model_path / 'model.pt')
            )
            
            # Move to device
            model = model.to(self.device)
            
            # Store model
            self.models[model_name] = model
            self.model_configs[model_name] = config
            
            # Load metrics if available
            if (model_path / 'metrics.json').exists():
                with open(model_path / 'metrics.json', 'r') as f:
                    self.model_metrics[model_name] = json.load(f)
                    
            return True
            
        except Exception as e:
            logger.error(f"Model load failed: {e}")
            return False
            
    def _load_models(self) -> None:
        """Load all available models"""
        try:
            for model_dir in self.models_path.iterdir():
                if model_dir.is_dir():
                    self.load_model(model_dir.name)
                    
        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            
    def _create_model(self, config: Dict) -> torch.nn.Module:
        """Create model instance from config"""
        model_type = config.get('type', 'lstm')
        
        if model_type == 'lstm':
            return LSTMModel(
                input_size=config.get('input_size', 5),
                hidden_size=config.get('hidden_size', 128),
                num_layers=config.get('num_layers', 3),
                dropout=config.get('dropout', 0.2)
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
            
    def _update_metrics(self, model_name: str, metrics: Dict) -> None:
        """Update model metrics tracking"""
        if model_name not in self.model_metrics:
            self.model_metrics[model_name] = []
            
        metrics['timestamp'] = datetime.now().isoformat()
        self.model_metrics[model_name].append(metrics)
        
        # Keep only recent metrics
        max_history = 1000
        if len(self.model_metrics[model_name]) > max_history:
            self.model_metrics[model_name] = self.model_metrics[model_name][-max_history:]