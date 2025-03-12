"""
Training Orchestrator
==================

Manages model training, validation, and updates.

REQUIREMENTS:
- Integration with FreqTrade API
- Continuous training pipeline
- Performance monitoring
- Model persistence
"""

import torch
import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging
from datetime import datetime
import json
from .model_factory import ModelFactory
from .data_preprocessor import DataPreprocessor
from .prediction_validator import PredictionValidator

logger = logging.getLogger(__name__)

class TrainingOrchestrator:
    def __init__(self, config: Dict):
        """Initialize training orchestrator"""
        self.config = config
        self.base_path = Path(config.get('base_path', 'C:/AlgoTradPro5'))
        
        # Initialize components
        self.model_factory = ModelFactory(
            base_path=self.base_path / 'models'
        )
        
        self.preprocessor = DataPreprocessor(
            config=config.get('preprocessor', {})
        )
        
        self.validator = PredictionValidator(
            config=config.get('validator', {})
        )
        
        # Training parameters
        self.batch_size = config.get('batch_size', 32)
        self.learning_rate = config.get('learning_rate', 1e-4)
        self.max_epochs = config.get('max_epochs', 100)
        self.patience = config.get('patience', 10)
        self.validation_split = config.get('validation_split', 0.2)
        
        # Performance tracking
        self.best_metrics = None
        self.best_model_path = None
        self.current_epoch = 0
        self.early_stop_counter = 0
        
        # CUDA setup
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu'
        )
        
        # TODO: Add multi-GPU support
        # TODO: Implement model checkpointing
        # TODO: Add distributed training
        
    def train(self,
              train_data: np.ndarray,
              model_type: str = 'ensemble',
              model_config: Optional[Dict] = None) -> Dict[str, float]:
        """
        Train model with validation
        
        Args:
            train_data: Training data
            model_type: Type of model to train
            model_config: Optional model configuration
            
        Returns:
            Dictionary of training metrics
        """
        # Preprocess data
        self.preprocessor.fit(train_data)
        processed_data = self.preprocessor.transform(train_data)
        
        # Create sequences
        X, y = self.preprocessor.create_sequences(
            processed_data,
            shuffle=True
        )
        
        # Split validation
        val_size = int(len(X) * self.validation_split)
        X_train, X_val = X[val_size:], X[:val_size]
        y_train, y_val = y[val_size:], y[:val_size]
        
        # Create model
        model = self.model_factory.create_model(
            model_type,
            config=model_config
        )
        model = model.to(self.device)
        
        # Initialize optimizer
        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=self.learning_rate
        )
        
        # Training loop
        best_val_loss = float('inf')
        training_metrics = []
        
        for epoch in range(self.max_epochs):
            self.current_epoch = epoch
            
            # Training phase
            model.train()
            train_losses = []
            
            for i in range(0, len(X_train), self.batch_size):
                batch_X = X_train[i:i + self.batch_size].to(self.device)
                batch_y = y_train[i:i + self.batch_size].to(self.device)
                
                optimizer.zero_grad()
                
                if model_type == 'ensemble':
                    predictions = model.predict(batch_X)
                    loss = self._calculate_ensemble_loss(predictions, batch_y)
                else:
                    predictions = model(batch_X)
                    loss = torch.nn.functional.mse_loss(predictions, batch_y)
                
                loss.backward()
                optimizer.step()
                train_losses.append(loss.item())
                
            # Validation phase
            model.eval()
            val_losses = []
            val_predictions = []
            
            with torch.no_grad():
                for i in range(0, len(X_val), self.batch_size):
                    batch_X = X_val[i:i + self.batch_size].to(self.device)
                    batch_y = y_val[i:i + self.batch_size].to(self.device)
                    
                    if model_type == 'ensemble':
                        predictions = model.predict(batch_X)
                        loss = self._calculate_ensemble_loss(predictions, batch_y)
                    else:
                        predictions = model(batch_X)
                        loss = torch.nn.functional.mse_loss(predictions, batch_y)
                        
                    val_losses.append(loss.item())
                    val_predictions.extend(predictions.cpu().numpy())
                    
            # Calculate metrics
            train_loss = np.mean(train_losses)
            val_loss = np.mean(val_losses)
            
            # Validate predictions
            validation_results = []
            for pred, actual in zip(val_predictions, y_val.numpy()):
                metrics = self.validator.validate_prediction(
                    {'value': float(pred), 'confidence': 0.9},  # TODO: Add real confidence
                    float(actual)
                )
                validation_results.append(metrics)
                
            validation_rate = np.mean([
                m.validation_passed for m in validation_results
            ])
            
            metrics = {
                'epoch': epoch,
                'train_loss': train_loss,
                'val_loss': val_loss,
                'validation_rate': validation_rate
            }
            training_metrics.append(metrics)
            
            logger.info(
                f"Epoch {epoch}: train_loss={train_loss:.4f}, "
                f"val_loss={val_loss:.4f}, validation_rate={validation_rate:.2%}"
            )
            
            # Check for improvement
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                self.best_metrics = metrics
                self.early_stop_counter = 0
                
                # Save best model
                self.best_model_path = (
                    self.base_path / 'models' / 
                    f'{model_type}_best_{datetime.now():%Y%m%d_%H%M}.pth'
                )
                self.model_factory.save_model_weights(
                    model,
                    self.best_model_path.stem,
                    overwrite=True
                )
            else:
                self.early_stop_counter += 1
                
            # Early stopping check
            if self.early_stop_counter >= self.patience:
                logger.info(f"Early stopping triggered after {epoch + 1} epochs")
                break
                
        return self.best_metrics
        
    def _calculate_ensemble_loss(self,
                               predictions: Dict[str, torch.Tensor],
                               targets: torch.Tensor) -> torch.Tensor:
        """Calculate weighted loss for ensemble predictions"""
        total_loss = 0.0
        
        # ROI prediction loss
        if 'roi' in predictions:
            roi_loss = torch.nn.functional.mse_loss(
                predictions['roi'],
                targets
            )
            total_loss += 0.5 * roi_loss  # 50% weight
            
        # Volatility prediction loss
        if 'volatility' in predictions:
            vol_loss = torch.nn.functional.mse_loss(
                predictions['volatility'],
                targets
            )
            total_loss += 0.3 * vol_loss  # 30% weight
            
        # Trend prediction loss
        if 'trend' in predictions:
            trend_loss = torch.nn.functional.cross_entropy(
                predictions['trend'],
                targets.long()
            )
            total_loss += 0.2 * trend_loss  # 20% weight
            
        return total_loss
        
    def save_training_state(self):
        """Save training state and metrics"""
        if not self.best_metrics:
            return
            
        state_path = self.base_path / 'models' / 'training_state.json'
        
        state = {
            'best_metrics': self.best_metrics,
            'best_model_path': str(self.best_model_path),
            'last_epoch': self.current_epoch,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(state_path, 'w') as f:
            json.dump(state, f, indent=2)
            
    def load_training_state(self) -> Optional[Dict]:
        """Load previous training state"""
        state_path = self.base_path / 'models' / 'training_state.json'
        
        if not state_path.exists():
            return None
            
        with open(state_path) as f:
            return json.load(f)