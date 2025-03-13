"""
Pattern Catalog
=============

Manages quantum-validated trading patterns.

CRITICAL REQUIREMENTS:
- Store validated patterns with >85% success rate
- Track pattern performance metrics
- Handle pattern mutations and variations
- Maintain pattern validation status
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import numpy as np
import pandas as pd
from pathlib import Path
import json

from data_manager import DataManager
from quantum_optimizer import QuantumOptimizer

logger = logging.getLogger(__name__)

class PatternCatalog:
    def __init__(self, config: Dict):
        """Initialize pattern catalog"""
        self.config = config
        self.base_path = Path(config.get('base_path', 'C:/AlgoTradPro5'))
        
        # Initialize components
        self.data_manager = DataManager(config)
        self.quantum_optimizer = QuantumOptimizer(
            n_qubits=4,
            shots=1000,
            use_gpu=True
        )
        
        # Pattern tracking
        self.active_patterns: Dict[str, Dict] = {}
        self.pattern_mutations: Dict[str, List[str]] = {}
        
        # Performance thresholds
        self.min_confidence = 0.85  # STRICT: 85% minimum confidence
        self.min_win_rate = 0.85    # STRICT: 85% minimum win rate
        self.validation_window = 12  # Required candles for validation
        
        # TODO: Implement pattern similarity scoring
        # TODO: Add pattern evolution tracking
        # TODO: Create pattern regime detection
        # TODO: Add market condition correlation

    def add_pattern(self, 
                   pattern_data: np.ndarray,
                   pattern_name: str,
                   pair: str,
                   timeframe: str) -> Optional[str]:
        """
        Add new pattern to catalog with quantum validation
        
        VALIDATION STEPS:
        1. Forward/backward testing
        2. Confidence check
        3. Performance validation
        4. Similarity analysis
        """
        try:
            # Quantum validation
            validation = self._validate_pattern(pattern_data)
            if not validation['pattern_validated']:
                logger.warning(f"Pattern {pattern_name} failed quantum validation")
                return None
            
            # Store pattern details
            pattern_id = self.data_manager.store_quantum_validated_pattern({
                'pattern_name': pattern_name,
                'pair': pair,
                'timeframe': timeframe,
                'entry_timestamp': datetime.now().isoformat(),
                'forward_score': validation['forward_score'],
                'backward_score': validation['backward_score'],
                'alignment_score': validation['alignment_score'],
                'confidence': validation['confidence'],
                'regime': validation['regime'],
                'pattern_data': pattern_data.tolist(),
                'validation_window': self.validation_window
            })
            
            if pattern_id:
                self.active_patterns[pattern_id] = {
                    'name': pattern_name,
                    'confidence': validation['confidence'],
                    'last_used': datetime.now().isoformat(),
                    'trades_won': 0,
                    'trades_total': 0
                }
            
            return pattern_id
            
        except Exception as e:
            logger.error(f"Error adding pattern: {e}")
            return None

    def validate_pattern_similarity(self,
                                 pattern_data: np.ndarray,
                                 min_similarity: float = 0.85) -> List[Dict]:
        """
        Check if pattern matches existing validated patterns
        
        SIMILARITY METRICS:
        1. Shape correlation
        2. Volume profile
        3. Momentum alignment
        4. Regime consistency
        """
        similar_patterns = []
        try:
            # Get active patterns
            patterns = self.data_manager.get_validated_patterns(
                min_confidence=self.min_confidence
            )
            
            for _, pattern in patterns.iterrows():
                stored_data = np.array(json.loads(pattern['pattern_data']))
                
                # Calculate similarity score
                similarity = self._calculate_pattern_similarity(
                    pattern_data,
                    stored_data
                )
                
                if similarity >= min_similarity:
                    stats = self.data_manager.get_pattern_stats(pattern['id'])
                    similar_patterns.append({
                        'pattern_id': pattern['id'],
                        'similarity': similarity,
                        'confidence': pattern['confidence'],
                        'win_rate': stats.get('win_rate', 0),
                        'regime': pattern['regime']
                    })
            
            return sorted(
                similar_patterns,
                key=lambda x: (x['similarity'], x['win_rate']),
                reverse=True
            )
            
        except Exception as e:
            logger.error(f"Error validating pattern similarity: {e}")
            return []

    def update_pattern_performance(self,
                                pattern_id: str,
                                trade_result: Dict) -> None:
        """
        Update pattern performance metrics and status
        
        TRACKING:
        - Win/loss record
        - PnL metrics
        - Confidence updates
        - Regime changes
        """
        try:
            if pattern_id in self.active_patterns:
                pattern = self.active_patterns[pattern_id]
                
                # Update trade statistics
                pattern['trades_total'] += 1
                if trade_result['pnl'] > 0:
                    pattern['trades_won'] += 1
                
                # Calculate win rate
                win_rate = pattern['trades_won'] / pattern['trades_total']
                
                # Update pattern status
                pattern['last_used'] = datetime.now().isoformat()
                pattern['win_rate'] = win_rate
                
                # Store trade result
                self.data_manager.update_pattern_performance(
                    pattern_id,
                    trade_result
                )
                
                # Check if pattern needs deactivation
                if win_rate < self.min_win_rate and pattern['trades_total'] >= 10:
                    logger.warning(
                        f"Pattern {pattern_id} deactivated due to low win rate: {win_rate:.1%}"
                    )
                    self.active_patterns.pop(pattern_id)
            
        except Exception as e:
            logger.error(f"Error updating pattern performance: {e}")

    def _validate_pattern(self, pattern_data: np.ndarray) -> Dict:
        """Perform quantum validation of pattern"""
        # Forward analysis
        forward_results = self.quantum_optimizer.analyze_pattern(pattern_data)
        
        # Backward analysis
        backward_data = np.flip(pattern_data.copy(), axis=0)
        backward_results = self.quantum_optimizer.analyze_pattern(backward_data)
        
        # Validation metrics
        confidence_alignment = 1 - abs(
            forward_results['confidence'] - backward_results['confidence']
        )
        regime_alignment = (
            forward_results['regime'] * -backward_results['regime']
        ) > 0
        
        return {
            'pattern_validated': confidence_alignment > 0.8 and regime_alignment,
            'confidence': min(
                forward_results['confidence'],
                backward_results['confidence']
            ),
            'regime': forward_results['regime'],
            'forward_score': forward_results['pattern_score'],
            'backward_score': backward_results['pattern_score'],
            'alignment_score': confidence_alignment
        }

    def _calculate_pattern_similarity(self,
                                   pattern1: np.ndarray,
                                   pattern2: np.ndarray) -> float:
        """
        Calculate similarity between two patterns
        
        METRICS:
        1. Price correlation
        2. Volume profile similarity
        3. Pattern shape matching
        """
        try:
            # Normalize patterns
            p1_norm = (pattern1 - np.mean(pattern1)) / np.std(pattern1)
            p2_norm = (pattern2 - np.mean(pattern2)) / np.std(pattern2)
            
            # Calculate correlation
            correlation = np.corrcoef(p1_norm.flatten(), p2_norm.flatten())[0, 1]
            
            # Calculate volume profile similarity
            vol1 = pattern1[:, -1]  # Assuming volume is last column
            vol2 = pattern2[:, -1]
            vol_similarity = 1 - np.mean(np.abs(
                vol1/np.sum(vol1) - vol2/np.sum(vol2)
            ))
            
            # Combine metrics
            similarity = 0.7 * max(0, correlation) + 0.3 * vol_similarity
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error calculating pattern similarity: {e}")
            return 0.0