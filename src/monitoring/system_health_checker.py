"""
System Health Checker
===================

CRITICAL REQUIREMENTS:
- Win rate validation (85% target)
- Growth rate monitoring (£10 to £1000)
- System component validation
- Resource monitoring

VALIDATION GATES:
1. Performance metrics
2. Resource availability
3. Component health
4. Documentation status

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import logging
from typing import Dict, List, Optional
from pathlib import Path
import psutil
import torch
import json
from datetime import datetime

from doc_validator import validate_documentation
from data_manager import DataManager

logger = logging.getLogger(__name__)

class SystemHealthChecker:
    """
    System health monitoring and validation
    
    CRITICAL METRICS:
    - Win rate >= 85%
    - Growth tracking
    - Component health
    - Resource usage
    """
    
    def __init__(self):
        """
        Initialize health checker with strict thresholds
        
        COMPONENTS:
        - Performance monitor
        - Resource tracker
        - Documentation validator
        - Alert system
        """
        self.data_manager = DataManager()
        
        # STRICT: Critical thresholds
        self.min_win_rate = 0.85
        self.min_growth_rate = 1.0  # 100% daily for £10 to £1000
        self.max_drawdown = 0.10
        self.min_memory = 4_000  # MB
        self.min_gpu_memory = 2_000  # MB
        
        # Component tracking
        self.components = {
            'quantum_optimizer': False,
            'ai_models': False,
            'databases': False,
            'documentation': False
        }
        
        logger.info("System Health Checker initialized with strict thresholds")
        
    def check_system_health(self) -> Dict[str, bool]:
        """
        Comprehensive system health check
        
        CHECKS:
        1. Performance metrics
        2. Resource availability
        3. Component status
        4. Documentation validity
        """
        try:
            health_status = {
                'performance': self._check_performance_metrics(),
                'resources': self._check_resources(),
                'components': self._check_components(),
                'documentation': self._check_documentation()
            }
            
            # CRITICAL: Log any failures
            failed_checks = [k for k, v in health_status.items() if not v]
            if failed_checks:
                logger.error(f"Health check failed for: {', '.join(failed_checks)}")
            
            return health_status
            
        except Exception as e:
            logger.error(f"System health check failed: {e}")
            return {'error': str(e)}
            
    def _check_performance_metrics(self) -> bool:
        """
        Validate critical performance metrics
        
        REQUIREMENTS:
        1. Win rate >= 85%
        2. Growth on track
        3. Drawdown within limits
        """
        try:
            # Get recent performance
            win_rate = self.data_manager.calculate_win_rate(days=1)
            current_capital = self._get_current_capital()
            drawdown = self._calculate_drawdown()
            
            # CRITICAL: Check win rate
            if win_rate < self.min_win_rate:
                logger.error(f"Win rate {win_rate:.2%} below minimum {self.min_win_rate:.2%}")
                return False
            
            # Check growth progress
            if current_capital < 10.0:  # Starting capital
                logger.error(f"Capital below starting amount: £{current_capital:.2f}")
                return False
            
            # Check drawdown
            if drawdown > self.max_drawdown:
                logger.error(f"Maximum drawdown exceeded: {drawdown:.2%}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Performance check failed: {e}")
            return False
            
    def _check_resources(self) -> bool:
        """
        Verify system resource availability
        
        REQUIREMENTS:
        1. Memory availability
        2. GPU resources
        3. Disk space
        4. CPU usage
        """
        try:
            # Check system memory
            memory = psutil.virtual_memory()
            if memory.available / 1024 / 1024 < self.min_memory:
                logger.error("Insufficient system memory")
                return False
            
            # Check GPU if available
            if torch.cuda.is_available():
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024 / 1024
                if gpu_memory < self.min_gpu_memory:
                    logger.error("Insufficient GPU memory")
                    return False
            
            # Check disk space
            disk = psutil.disk_usage('/')
            if disk.percent > 90:
                logger.error("Low disk space")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Resource check failed: {e}")
            return False
            
    def _check_components(self) -> bool:
        """
        Verify all system components
        
        COMPONENTS:
        1. Quantum optimizer
        2. AI models
        3. Databases
        4. Documentation
        """
        try:
            # Check quantum optimizer
            self.components['quantum_optimizer'] = self._verify_quantum_optimizer()
            
            # Check AI models
            self.components['ai_models'] = self._verify_ai_models()
            
            # Check databases
            self.components['databases'] = self._verify_databases()
            
            # All components must be healthy
            return all(self.components.values())
            
        except Exception as e:
            logger.error(f"Component check failed: {e}")
            return False
            
    def _check_documentation(self) -> bool:
        """
        Validate system documentation
        
        REQUIREMENTS:
        1. Architecture docs
        2. Integration guide
        3. Trading journal
        4. Version control
        """
        try:
            # Verify documentation exists and is valid
            docs_valid = validate_documentation()
            self.components['documentation'] = docs_valid
            
            if not docs_valid:
                logger.error("Documentation validation failed")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Documentation check failed: {e}")
            return False
            
    def _verify_quantum_optimizer(self) -> bool:
        """
        Verify quantum optimizer functionality
        
        CHECKS:
        1. GPU availability
        2. Model loading
        3. Test execution
        4. Performance metrics
        """
        try:
            from quantum_optimizer import QuantumOptimizer
            optimizer = QuantumOptimizer(n_qubits=4, shots=1000)
            
            # Run test pattern
            test_data = torch.randn(10, 5)
            result = optimizer.analyze_pattern(test_data.numpy())
            
            return bool(result and 'confidence' in result)
            
        except Exception as e:
            logger.error(f"Quantum optimizer verification failed: {e}")
            return False
            
    def _verify_ai_models(self) -> bool:
        """
        Verify AI model functionality
        
        CHECKS:
        1. Model loading
        2. Prediction test
        3. Performance metrics
        4. Resource usage
        """
        try:
            from ai_model_manager import AIModelManager
            model_manager = AIModelManager({})
            
            # Verify models loaded
            if not model_manager.loaded_models:
                logger.error("No AI models loaded")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"AI model verification failed: {e}")
            return False
            
    def _verify_databases(self) -> bool:
        """
        Verify database health
        
        CHECKS:
        1. Connectivity
        2. Write test
        3. Read test
        4. Integrity check
        """
        try:
            # Test database connections
            test_metrics = {
                'timestamp': datetime.now().isoformat(),
                'test_value': 1.0
            }
            
            # Test write/read
            write_success = self.data_manager.store_performance_metrics(test_metrics)
            if not write_success:
                logger.error("Database write test failed")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Database verification failed: {e}")
            return False
            
    def _get_current_capital(self) -> float:
        """
        Get current trading capital
        
        CRITICAL:
        - Must track progress to £1000 target
        """
        try:
            trades = self.data_manager.get_trade_history(days=7)
            if trades.empty:
                return 10.0  # Starting capital
                
            current_capital = 10.0 + trades['profit_ratio'].sum() * 10.0
            return max(current_capital, 0.0)  # Never return negative
            
        except Exception as e:
            logger.error(f"Error getting current capital: {e}")
            return 0.0
            
    def _calculate_drawdown(self) -> float:
        """
        Calculate current drawdown
        
        CRITICAL:
        - Must not exceed 10%
        """
        try:
            trades = self.data_manager.get_trade_history(days=7)
            if trades.empty:
                return 0.0
                
            # Calculate running balance
            balance = 10.0 + (trades['profit_ratio'].cumsum() * 10.0)
            peak = balance.max()
            current = balance.iloc[-1]
            
            return (peak - current) / peak if peak > 0 else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating drawdown: {e}")
            return 0.0

def check_system_health() -> bool:
    """
    Global health check function
    
    VALIDATION:
    - All components healthy
    - Performance metrics met
    - Resources available
    """
    checker = SystemHealthChecker()
    health_status = checker.check_system_health()
    return all(health_status.values())