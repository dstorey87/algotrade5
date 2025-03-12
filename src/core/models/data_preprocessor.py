"""
Data Preprocessor
==============

Data preprocessing pipeline for AI models.

REQUIREMENTS:
- Input validation
- Feature scaling
- Missing data handling
- Outlier detection
"""

import numpy as np
import torch
from typing import Dict, List, Tuple, Optional, Union
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.impute import SimpleImputer
import logging

logger = logging.getLogger(__name__)

class DataPreprocessor:
    def __init__(self, config: Dict):
        """Initialize preprocessor with configuration"""
        self.config = config
        
        # Feature scaling
        self.scaler_type = config.get('scaler', 'standard')
        if self.scaler_type == 'standard':
            self.scaler = StandardScaler()
        elif self.scaler_type == 'robust':
            self.scaler = RobustScaler()
        else:
            raise ValueError(f"Unknown scaler type: {self.scaler_type}")
            
        # Missing data imputation
        self.imputer = SimpleImputer(
            strategy=config.get('impute_strategy', 'mean'),
            missing_values=np.nan
        )
        
        # Outlier detection thresholds
        self.outlier_std_threshold = config.get('outlier_std_threshold', 3.0)
        self.min_samples = config.get('min_samples', 30)
        
        # Sequence parameters
        self.sequence_length = config.get('sequence_length', 10)
        self.prediction_horizon = config.get('prediction_horizon', 1)
        
        # Feature configuration
        self.feature_columns = config.get('feature_columns', [])
        self.target_columns = config.get('target_columns', [])
        
        # State tracking
        self.is_fitted = False
        
        # TODO: Add feature selection
        # TODO: Implement dimension reduction
        # TODO: Add data augmentation
        
    def fit(self, data: np.ndarray):
        """Fit preprocessor to training data"""
        if len(data) < self.min_samples:
            raise ValueError(
                f"Insufficient samples: {len(data)} < {self.min_samples}"
            )
            
        # Fit imputer
        self.imputer.fit(data)
        
        # Fit scaler
        clean_data = self.imputer.transform(data)
        self.scaler.fit(clean_data)
        
        self.is_fitted = True
        
    def transform(self, data: np.ndarray) -> np.ndarray:
        """Transform data with validation"""
        if not self.is_fitted:
            raise RuntimeError("Preprocessor must be fitted before transform")
            
        # Basic validation
        self._validate_input(data)
        
        # Handle missing data
        clean_data = self.imputer.transform(data)
        
        # Scale features
        scaled_data = self.scaler.transform(clean_data)
        
        # Detect outliers
        outliers = self._detect_outliers(scaled_data)
        if outliers.any():
            logger.warning(f"Detected {outliers.sum()} outliers in data")
            
        return scaled_data
        
    def create_sequences(self, 
                        data: np.ndarray,
                        shuffle: bool = True) -> Tuple[torch.Tensor, torch.Tensor]:
        """Create input sequences for model training"""
        # Validate data
        if len(data) < self.sequence_length + self.prediction_horizon:
            raise ValueError("Insufficient data for sequence creation")
            
        # Create sequences
        sequences = []
        targets = []
        
        for i in range(len(data) - self.sequence_length - self.prediction_horizon + 1):
            seq = data[i:(i + self.sequence_length)]
            target = data[i + self.sequence_length:
                         i + self.sequence_length + self.prediction_horizon]
            
            sequences.append(seq)
            targets.append(target)
            
        # Convert to tensors
        X = torch.FloatTensor(np.array(sequences))
        y = torch.FloatTensor(np.array(targets))
        
        # Shuffle if requested
        if shuffle:
            indices = torch.randperm(len(X))
            X = X[indices]
            y = y[indices]
            
        return X, y
        
    def _validate_input(self, data: np.ndarray):
        """Validate input data"""
        if data.ndim != 2:
            raise ValueError(f"Expected 2D array, got {data.ndim}D")
            
        if len(data) == 0:
            raise ValueError("Empty input data")
            
        if np.any(np.isinf(data)):
            raise ValueError("Input contains infinity values")
            
        expected_features = len(self.feature_columns)
        if expected_features > 0 and data.shape[1] != expected_features:
            raise ValueError(
                f"Expected {expected_features} features, got {data.shape[1]}"
            )
            
    def _detect_outliers(self, data: np.ndarray) -> np.ndarray:
        """Detect outliers using z-score method"""
        z_scores = np.abs((data - np.mean(data, axis=0)) / np.std(data, axis=0))
        return z_scores > self.outlier_std_threshold
        
    def inverse_transform(self, data: np.ndarray) -> np.ndarray:
        """Inverse transform predictions"""
        if not self.is_fitted:
            raise RuntimeError("Preprocessor must be fitted before inverse_transform")
            
        return self.scaler.inverse_transform(data)
        
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores"""
        if not self.feature_columns:
            return {}
            
        # Use variance as basic importance metric
        if not self.is_fitted:
            raise RuntimeError("Preprocessor must be fitted to get feature importance")
            
        variances = np.var(self.scaler.transform(self.imputer.transform(
            self._latest_data)), axis=0)
            
        return dict(zip(self.feature_columns, variances))