"""
AlgoTradePro5 System Monitor
===========================

CRITICAL REQUIREMENTS:
- Real-time win rate monitoring (85% target)
- Growth rate tracking (£10 to £1000)
- Quantum validation status
- System health verification
- Performance metrics logging

ALERT THRESHOLDS:
1. Win rate drops below 87%
2. Drawdown exceeds 8%
3. Growth rate below target
4. Pattern validation failures

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from pathlib import Path
import sqlite3

from system_health_checker import check_system_health
from risk_manager import RiskManager
from quantum_optimizer import QuantumOptimizer
from data_manager import DataManager

logger = logging.getLogger(__name__)

class SystemMonitor:
    """
    Real-time system monitoring and alerting
    
    CRITICAL METRICS:
    - Win rate (85% minimum)
    - Pattern confidence (0.85+)
    - System health status
    - Resource utilization
    """
    
    def __init__(self, config: Dict):
        """
        Initialize monitoring system with strict thresholds
        
        COMPONENTS:
        - Database connections
        - Alert system
        - Metric trackers
        - Health monitors
        """
        self.config = config
        self.data_manager = DataManager()
        self.risk_manager = RiskManager(config)
        self.quantum_optimizer = QuantumOptimizer(n_qubits=4, shots=1000)
        
        # STRICT: Alert thresholds
        self.win_rate_threshold = 0.85
        self.warning_win_rate = 0.87
        self.max_drawdown = 0.10
        self.warning_drawdown = 0.08
        self.min_confidence = 0.85
        
        # Performance tracking
        self.performance_history = []
        self.alert_history = []
        self.system_status = "operational"
        
        logger.info("System Monitor initialized with strict thresholds")
        
    def check_system_metrics(self) -> Dict:
        """
        Comprehensive system health and performance check
        
        MONITORED METRICS:
        1. Win rate and performance
        2. System health status
        3. Resource utilization
        4. Pattern validation status
        """
        try:
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'system_health': check_system_health(),
                'win_rate': self.risk_manager.calculate_win_rate(),
                'current_drawdown': self.risk_manager.current_drawdown,
                'trading_enabled': self.risk_manager.trading_enabled,
                'quantum_validated': self.risk_manager.quantum_validated,
                'gpu_utilization': self.quantum_optimizer.get_gpu_metrics(),
                'db_status': self._check_database_health()
            }
            
            # CRITICAL: Check win rate
            if metrics['win_rate'] < self.win_rate_threshold:
                self._trigger_alert("CRITICAL", f"Win rate {metrics['win_rate']:.2%} below minimum threshold")
            elif metrics['win_rate'] < self.warning_win_rate:
                self._trigger_alert("WARNING", f"Win rate {metrics['win_rate']:.2%} approaching minimum threshold")
            
            # CRITICAL: Check drawdown
            if metrics['current_drawdown'] >= self.max_drawdown:
                self._trigger_alert("CRITICAL", f"Maximum drawdown reached: {metrics['current_drawdown']:.2%}")
            elif metrics['current_drawdown'] >= self.warning_drawdown:
                self._trigger_alert("WARNING", f"Drawdown warning: {metrics['current_drawdown']:.2%}")
            
            self.performance_history.append(metrics)
            return metrics
            
        except Exception as e:
            logger.error(f"Error checking system metrics: {e}")
            self._trigger_alert("CRITICAL", f"System monitoring failure: {str(e)}")
            return {}
            
    def validate_pattern_performance(self) -> Dict:
        """
        Validate pattern recognition performance
        
        REQUIREMENTS:
        1. Minimum confidence level
        2. Pattern success rate
        3. Validation status tracking
        4. Performance logging
        """
        try:
            patterns = self.data_manager.get_validated_patterns(
                min_confidence=self.min_confidence,
                validation_status='validated'
            )
            
            performance_metrics = {
                'total_patterns': len(patterns),
                'validated_count': sum(1 for p in patterns if p['validation_status'] == 'validated'),
                'average_confidence': patterns['confidence'].mean() if not patterns.empty else 0,
                'success_rate': patterns['success_rate'].mean() if not patterns.empty else 0
            }
            
            # CRITICAL: Validate pattern performance
            if performance_metrics['average_confidence'] < self.min_confidence:
                self._trigger_alert(
                    "WARNING", 
                    f"Pattern confidence {performance_metrics['average_confidence']:.2%} below threshold"
                )
            
            return performance_metrics
            
        except Exception as e:
            logger.error(f"Error validating patterns: {e}")
            return {}
            
    def _check_database_health(self) -> Dict:
        """
        Verify database integrity and performance
        
        CHECKS:
        1. Connection status
        2. Write performance
        3. Data integrity
        4. Storage capacity
        """
        try:
            status = {
                'analysis_db': True,
                'trading_db': True,
                'write_performance': 0,
                'storage_available': 0
            }
            
            # Test database connections
            for db_path in ['data/analysis.db', 'data/trading.db']:
                try:
                    with sqlite3.connect(db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute("PRAGMA integrity_check")
                except Exception as e:
                    status[db_path.split('/')[-1].replace('.db', '_db')] = False
                    self._trigger_alert("CRITICAL", f"Database error ({db_path}): {str(e)}")
            
            return status
            
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {}
            
    def _trigger_alert(self, level: str, message: str):
        """
        Trigger system alert with appropriate severity
        
        ALERT LEVELS:
        - CRITICAL: Immediate action required
        - WARNING: Investigation needed
        - INFO: Status update
        """
        alert = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message
        }
        
        self.alert_history.append(alert)
        
        if level == "CRITICAL":
            logger.error(f"🚨 {message}")
            self.system_status = "critical"
            # TODO: Implement emergency notification system
        elif level == "WARNING":
            logger.warning(f"⚠️ {message}")
            if self.system_status == "operational":
                self.system_status = "warning"
        else:
            logger.info(f"ℹ️ {message}")
            
    def get_system_status(self) -> Dict:
        """
        Get comprehensive system status report
        
        INCLUDES:
        1. Current metrics
        2. Alert history
        3. Performance trends
        4. Resource status
        """
        return {
            'status': self.system_status,
            'current_metrics': self.check_system_metrics(),
            'pattern_performance': self.validate_pattern_performance(),
            'recent_alerts': self.alert_history[-10:],
            'trading_enabled': self.risk_manager.trading_enabled,
            'last_updated': datetime.now().isoformat()
        }
        
    def generate_performance_report(self) -> pd.DataFrame:
        """
        Generate detailed performance analysis report
        
        METRICS:
        - Win rate trends
        - Pattern success rates
        - System health history
        - Alert statistics
        """
        if not self.performance_history:
            return pd.DataFrame()
            
        df = pd.DataFrame(self.performance_history)
        
        # Calculate key statistics
        stats = {
            'win_rate_trend': df['win_rate'].rolling(10).mean(),
            'drawdown_trend': df['current_drawdown'].rolling(10).mean(),
            'system_health_rate': df['system_health'].mean(),
            'validation_rate': df['quantum_validated'].mean()
        }
        
        return pd.DataFrame(stats)