"""
Data Preprocessing Module
=====================

CRITICAL REQUIREMENTS:
- Missing data imputation
- Outlier detection
- Feature scaling
- Validation checks
- Error tracking

PREPROCESSING STEPS:
1. Data validation
2. Missing value imputation
3. Outlier detection
4. Feature scaling
5. Sequence generation

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import logging
from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.impute import SimpleImputer
import torch
from datetime import datetime

from config_manager import get_config
from error_manager import ErrorManager, ErrorSeverity

logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Handles all data preprocessing and validation"""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize preprocessor with configuration"""
        self.config = config or get_config()
        self.error_manager = ErrorManager()
        
        # Feature scaling configuration
        self.scaler_type = self.config.get('scaler', 'standard')
        self.scaler = self._initialize_scaler()
        
        # Missing data imputation
        self.imputer = SimpleImputer(
            strategy=self.config.get('impute_strategy', 'mean'),
            missing_values=np.nan
        )
        
        # Outlier detection parameters
        self.outlier_std_threshold = self.config.get('outlier_std_threshold', 3.0)
        self.min_samples = self.config.get('min_samples', 30)
        
        # Sequence parameters
        self.sequence_length = self.config.get('sequence_length', 10)
        self.prediction_horizon = self.config.get('prediction_horizon', 1)
        
        # Feature configuration
        self.feature_columns = self.config.get('feature_columns', [])
        self.target_columns = self.config.get('target_columns', [])
        
        # State tracking
        self.is_fitted = False
        self.last_validation = None
        
        logger.info("Data Preprocessor initialized with validation")
        
    def _initialize_scaler(self) -> Union[StandardScaler, RobustScaler]:
        """Initialize feature scaler based on configuration"""
        if self.scaler_type == 'standard':
            return StandardScaler()
        elif self.scaler_type == 'robust':
            return RobustScaler()
        else:
            error_msg = f"Unknown scaler type: {self.scaler_type}"
            self.error_manager.log_error(
                error_msg,
                ErrorSeverity.HIGH.value,
                "Preprocessing"
            )
            raise ValueError(error_msg)
            
    def fit(self, data: np.ndarray) -> None:
        """Fit preprocessor to training data"""
        try:
            self._validate_input(data)
            
            # Fit imputer
            self.imputer.fit(data)
            
            # Remove outliers for fitting scaler
            clean_data = self._detect_outliers(data)
            
            # Fit scaler
            self.scaler.fit(clean_data)
            
            self.is_fitted = True
            self.last_validation = datetime.now().isoformat()
            
        except Exception as e:
            self.error_manager.log_error(
                f"Error fitting preprocessor: {e}",
                ErrorSeverity.HIGH.value,
                "Preprocessing"
            )
            raise
            
    def transform(self, data: np.ndarray) -> np.ndarray:
        """Transform data with validation"""
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transform")
            
        try:
            self._validate_input(data)
            
            # Handle missing values
            imputed_data = self.imputer.transform(data)
            
            # Handle outliers
            clean_data = self._detect_outliers(imputed_data)
            
            # Scale features
            scaled_data = self.scaler.transform(clean_data)
            
            return scaled_data
            
        except Exception as e:
            self.error_manager.log_error(
                f"Error transforming data: {e}",
                ErrorSeverity.HIGH.value,
                "Preprocessing"
            )
            raise
            
    def create_sequences(self, 
                        data: np.ndarray,
                        shuffle: bool = True) -> Tuple[torch.Tensor, torch.Tensor]:
        """Create input sequences for model training"""
        try:
            n_samples = data.shape[0]
            
            # Ensure enough samples for sequence
            if n_samples < self.sequence_length + self.prediction_horizon:
                raise ValueError(
                    f"Not enough samples ({n_samples}) for sequence length "
                    f"({self.sequence_length}) and horizon ({self.prediction_horizon})"
                )
                
            # Create sequences
            sequences = []
            targets = []
            
            for i in range(n_samples - self.sequence_length - self.prediction_horizon + 1):
                seq = data[i:(i + self.sequence_length)]
                target = data[i + self.sequence_length + self.prediction_horizon - 1]
                sequences.append(seq)
                targets.append(target)
                
            # Convert to tensors
            X = torch.FloatTensor(np.array(sequences))
            y = torch.FloatTensor(np.array(targets))
            
            # Shuffle if requested
            if shuffle:
                indices = torch.randperm(X.shape[0])
                X = X[indices]
                y = y[indices]
                
            return X, y
            
        except Exception as e:
            self.error_manager.log_error(
                f"Error creating sequences: {e}",
                ErrorSeverity.MEDIUM.value,
                "Preprocessing"
            )
            raise
            
    def _validate_input(self, data: np.ndarray) -> None:
        """Validate input data"""
        if not isinstance(data, np.ndarray):
            raise TypeError(f"Expected numpy array, got {type(data)}")
            
        if data.size == 0:
            raise ValueError("Empty input data")
            
        if len(data.shape) != 2:
            raise ValueError(f"Expected 2D array, got {len(data.shape)}D")
            
        if data.shape[0] < self.min_samples:
            raise ValueError(
                f"Not enough samples ({data.shape[0]}) for minimum requirement "
                f"({self.min_samples})"
            )
            
    def _detect_outliers(self, data: np.ndarray) -> np.ndarray:
        """Detect outliers using z-score method"""
        z_scores = np.abs((data - np.mean(data, axis=0)) / np.std(data, axis=0))
        outlier_mask = z_scores < self.outlier_std_threshold
        clean_data = data.copy()
        clean_data[~outlier_mask] = np.nan
        
        # Impute removed outliers
        clean_data = self.imputer.transform(clean_data)
        return clean_data
        
    def inverse_transform(self, data: np.ndarray) -> np.ndarray:
        """Inverse transform predictions"""
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before inverse transform")
            
        try:
            return self.scaler.inverse_transform(data)
            
        except Exception as e:
            self.error_manager.log_error(
                f"Error in inverse transform: {e}",
                ErrorSeverity.MEDIUM.value,
                "Preprocessing"
            )
            raise
            
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores"""
        if not self.feature_columns:
            return {}
            
        importance = {}
        for i, feature in enumerate(self.feature_columns):
            # Use scaler scale_ as crude importance measure
            if hasattr(self.scaler, 'scale_'):
                importance[feature] = abs(self.scaler.scale_[i])
            else:
                importance[feature] = 1.0
                
        return importance
        
    def cleanup(self) -> None:
        """Reset preprocessor state"""
        self.is_fitted = False
        if hasattr(self.scaler, 'n_samples_seen_'):
            self.scaler.n_samples_seen_ = 0

# Create global instance
_preprocessor = DataPreprocessor()

def get_preprocessor() -> DataPreprocessor:
    """Global function to get preprocessor instance"""
    return _preprocessor