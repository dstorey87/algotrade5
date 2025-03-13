"""
Strategy Optimizer
================

Combines quantum validation with LLM feedback learning.

CRITICAL REQUIREMENTS:
- Maintain 85% win rate target
- Real-time pattern optimization
- Continuous strategy refinement
- Risk limit enforcement
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
import numpy as np
from pathlib import Path

# Local imports
from .llm.feedback_learner import LLMFeedbackLearner
from .quantum.quantum_optimizer import QuantumOptimizer
from .data.data_manager import DataManager
from .trade.trade_journal import TradeJournal

logger = logging.getLogger(__name__)

class StrategyOptimizer:
    def __init__(self, config: Dict):
        """Initialize strategy optimizer"""
        self.config = config
        self.base_path = Path(config.get('base_path', 'C:/AlgoTradPro5'))
        
        # Initialize components
        self.feedback_learner = LLMFeedbackLearner(config)
        self.quantum_optimizer = QuantumOptimizer(
            n_qubits=4,
            shots=1000,
            use_gpu=True
        )
        self.data_manager = DataManager(config)
        self.trade_journal = TradeJournal()
        
        # Performance thresholds
        self.min_win_rate = 0.85  # STRICT: 85% minimum
        self.min_confidence = 0.85  # STRICT: 85% minimum
        self.improvement_threshold = 0.02  # 2% minimum improvement
        
        # Strategy tracking
        self.active_strategies: Dict[str, Dict] = {}
        self.strategy_history: List[Dict] = []
        
        # TODO: Add dynamic threshold adjustment
        # TODO: Implement strategy evolution tracking
        # TODO: Create pattern mutation analysis
        # TODO: Add market regime optimization

    def optimize_strategy(self, 
                        strategy_id: str,
                        strategy_data: Dict) -> Dict:
        """
        Optimize trading strategy with quantum validation and LLM feedback
        
        Args:
            strategy_id: Strategy identifier
            strategy_data: Current strategy configuration
            
        Returns:
            Optimized strategy configuration
        """
        try:
            # Validate strategy data
            if not self._validate_strategy_data(strategy_data):
                logger.error("Invalid strategy data")
                return {}
            
            # Get current performance metrics
            performance = self._get_performance_metrics(strategy_id)
            
            # Check if optimization needed
            if performance['win_rate'] >= self.min_win_rate:
                logger.info(f"Strategy {strategy_id} already meeting targets")
                return strategy_data
            
            # Generate improvements with LLM
            improvements = self.feedback_learner.generate_improvements(
                strategy_data,
                performance
            )
            
            if not improvements:
                logger.warning("No valid improvements generated")
                return strategy_data
            
            # Apply and validate improvements
            optimized_strategy = self._apply_improvements(
                strategy_data,
                improvements
            )
            
            # Quantum validation of optimized strategy
            validation = self._validate_quantum_patterns(
                optimized_strategy
            )
            
            if not validation['validated']:
                logger.warning("Optimized strategy failed quantum validation")
                return strategy_data
            
            # Update strategy tracking
            self._update_strategy_tracking(
                strategy_id,
                optimized_strategy,
                validation
            )
            
            return optimized_strategy
            
        except Exception as e:
            logger.error(f"Strategy optimization failed: {e}")
            return strategy_data

    def _validate_strategy_data(self, strategy_data: Dict) -> bool:
        """Validate strategy data completeness"""
        required_fields = [
            'patterns',
            'timeframes',
            'risk_params',
            'entry_rules',
            'exit_rules'
        ]
        
        return all(field in strategy_data for field in required_fields)

    def _get_performance_metrics(self, strategy_id: str) -> Dict:
        """Get current strategy performance metrics"""
        try:
            # Get recent trades
            trades = self.trade_journal.get_strategy_trades(
                strategy_id,
                days=7  # Focus on recent performance
            )
            
            if trades.empty:
                return {'win_rate': 0.0, 'profit_factor': 0.0}
            
            # Calculate metrics
            winning_trades = len(trades[trades['profit_ratio'] > 0])
            total_trades = len(trades)
            
            # Calculate profit factor
            gross_profit = trades[trades['profit_ratio'] > 0]['profit_ratio'].sum()
            gross_loss = abs(trades[trades['profit_ratio'] < 0]['profit_ratio'].sum())
            
            win_rate = winning_trades / total_trades if total_trades > 0 else 0
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
            
            return {
                'win_rate': win_rate,
                'profit_factor': profit_factor,
                'total_trades': total_trades,
                'winning_trades': winning_trades
            }
            
        except Exception as e:
            logger.error(f"Error getting performance metrics: {e}")
            return {'win_rate': 0.0, 'profit_factor': 0.0}

    def _apply_improvements(self,
                          strategy_data: Dict,
                          improvements: List[Dict]) -> Dict:
        """Apply strategy improvements with validation"""
        try:
            optimized_strategy = strategy_data.copy()
            
            for improvement in improvements:
                # Skip low confidence improvements
                if improvement['confidence'] < self.min_confidence:
                    continue
                # Apply improvement if impact is sufficient
                if improvement['estimated_impact'] >= self.improvement_threshold:
                    self._apply_single_improvement(
                        optimized_strategy,
                        improvement
                    )
            return optimized_strategy
            
        except Exception as e:
            logger.error(f"Error applying improvements: {e}")
            return strategy_data

    def _validate_quantum_patterns(self, strategy_data: Dict) -> Dict:
        """Validate strategy patterns with quantum circuit"""
        try:
            validation_results = []
            
            for pattern in strategy_data['patterns']:
                # Extract pattern features
                pattern_data = np.array([
                    pattern['open_prices'],
                    pattern['high_prices'],
                    pattern['low_prices'],
                    pattern['close_prices'],
                    pattern['volumes']
                ]).T
                
                # Quantum validation
                result = self.quantum_optimizer.analyze_pattern(pattern_data)
                validation_results.append(result)
            
            # Calculate aggregate validation metrics
            confidence = np.mean([r['confidence'] for r in validation_results])
            validated = confidence >= self.min_confidence
            
            return {
                'validated': validated,
                'confidence': confidence,
                'results': validation_results
            }
            
        except Exception as e:
            logger.error(f"Quantum validation failed: {e}")
            return {'validated': False, 'confidence': 0.0, 'results': []}

    def _update_strategy_tracking(self,
                                strategy_id: str,
                                strategy_data: Dict,
                                validation: Dict) -> None:
        """Update strategy tracking and history"""
        try:
            # Update active strategies
            self.active_strategies[strategy_id] = {
                'strategy_data': strategy_data,
                'last_updated': datetime.now().isoformat(),
                'validation_metrics': validation,
                'performance_metrics': self._get_performance_metrics(strategy_id)
            }
            
            # Add to history
            self.strategy_history.append({
                'strategy_id': strategy_id,
                'timestamp': datetime.now().isoformat(),
                'strategy_data': strategy_data,
                'validation_metrics': validation,
                'performance_metrics': self._get_performance_metrics(strategy_id)
            })
            # Store in database
            self.data_manager.store_strategy_update({
                'strategy_id': strategy_id,
                'strategy_data': strategy_data,
                'validation_metrics': validation,
                'performance_metrics': self._get_performance_metrics(strategy_id),
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error updating strategy tracking: {e}")

    def _apply_single_improvement(self,
                                strategy: Dict,
                                improvement: Dict) -> None:
        """Apply single strategy improvement"""
        try:
            suggestion = improvement['suggestion']
            
            # Parse suggestion and apply changes
            if 'entry rules' in suggestion.lower():
                self._update_entry_rules(strategy, suggestion)
            elif 'exit rules' in suggestion.lower():
                self._update_exit_rules(strategy, suggestion)
            elif 'risk parameters' in suggestion.lower():
                self._update_risk_params(strategy, suggestion)
            elif 'timeframes' in suggestion.lower():
                self._update_timeframes(strategy, suggestion)
                
        except Exception as e:
            logger.error(f"Error applying improvement: {e}")

    def _update_entry_rules(self, strategy: Dict, suggestion: str) -> None:
        """Update strategy entry rules"""
        try:
            # Extract rule changes from suggestion
            if 'add rule' in suggestion.lower():
                new_rule = self._parse_rule(suggestion)
                strategy['entry_rules'].append(new_rule)
            elif 'modify rule' in suggestion.lower():
                rule_index = self._find_rule_index(strategy['entry_rules'], suggestion)
                if rule_index >= 0:
                    strategy['entry_rules'][rule_index] = self._parse_rule(suggestion)
            elif 'remove rule' in suggestion.lower():
                rule_index = self._find_rule_index(strategy['entry_rules'], suggestion)
                if rule_index >= 0:
                    strategy['entry_rules'].pop(rule_index)
                    
        except Exception as e:
            logger.error(f"Error updating entry rules: {e}")

    def _update_exit_rules(self, strategy: Dict, suggestion: str) -> None:
        """Update strategy exit rules"""
        try:
            # Extract rule changes from suggestion
            if 'add rule' in suggestion.lower():
                new_rule = self._parse_rule(suggestion)
                strategy['exit_rules'].append(new_rule)
            elif 'modify rule' in suggestion.lower():
                rule_index = self._find_rule_index(strategy['exit_rules'], suggestion)
                if rule_index >= 0:
                    strategy['exit_rules'][rule_index] = self._parse_rule(suggestion)
            elif 'remove rule' in suggestion.lower():
                rule_index = self._find_rule_index(strategy['exit_rules'], suggestion)
                if rule_index >= 0:
                    strategy['exit_rules'].pop(rule_index)
                    
        except Exception as e:
            logger.error(f"Error updating exit rules: {e}")

    def _update_risk_params(self, strategy: Dict, suggestion: str) -> None:
        """Update strategy risk parameters"""
        try:
            risk_params = strategy['risk_params']
            
            if 'position size' in suggestion.lower():
                new_size = self._extract_numeric_value(suggestion)
                if 0 < new_size <= 0.02:  # Max 2% position size
                    risk_params['position_size'] = new_size
                    
            if 'stop loss' in suggestion.lower():
                new_stop = self._extract_numeric_value(suggestion)
                if 0.01 <= new_stop <= 0.03:  # 1-3% stop loss
                    risk_params['stop_loss'] = new_stop
                    
            if 'take profit' in suggestion.lower():
                new_tp = self._extract_numeric_value(suggestion)
                if new_tp > risk_params['stop_loss'] * 2:  # Min 2:1 reward ratio
                    risk_params['take_profit'] = new_tp
                    
        except Exception as e:
            logger.error(f"Error updating risk parameters: {e}")

    def _update_timeframes(self, strategy: Dict, suggestion: str) -> None:
        """Update strategy timeframes"""
        try:
            # Extract timeframe changes
            if 'add timeframe' in suggestion.lower():
                new_tf = self._extract_timeframe(suggestion)
                if new_tf and new_tf not in strategy['timeframes']:
                    strategy['timeframes'].append(new_tf)
            elif 'remove timeframe' in suggestion.lower():
                tf = self._extract_timeframe(suggestion)
                if tf in strategy['timeframes']:
                    strategy['timeframes'].remove(tf)
                    
        except Exception as e:
            logger.error(f"Error updating timeframes: {e}")

    def _parse_rule(self, suggestion: str) -> Dict:
        """Parse trading rule from suggestion text"""
        # TODO: Implement more sophisticated rule parsing
        return {
            'type': 'basic',
            'condition': suggestion,
            'parameters': {}
        }

    def _find_rule_index(self, rules: List[Dict], suggestion: str) -> int:
        """Find index of rule to modify/remove"""
        # TODO: Implement rule matching logic
        return -1

    def _extract_numeric_value(self, text: str) -> float:
        """Extract numeric value from text"""
        try:
            # Find numbers in text
            import re
            numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
            if numbers:
                return float(numbers[0])
            return 0.0
            
        except Exception:
            return 0.0

    def _extract_timeframe(self, text: str) -> Optional[str]:
        """Extract timeframe from text"""
        valid_timeframes = ['1m', '5m', '15m', '1h', '4h', '1d']
        for tf in valid_timeframes:
            if tf in text:
                return tf
        return None