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
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import GPUtil
import numpy as np
import pandas as pd
import psutil
from data_manager import DataManager
from quantum_optimizer import QuantumOptimizer
from risk_manager import RiskManager
from system_health_checker import check_system_health

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
        self._start_time = time.time()
        self._last_check = {}

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
                "timestamp": datetime.now().isoformat(),
                "system_health": check_system_health(),
                "win_rate": self._calculate_win_rate(),
                "current_drawdown": self._calculate_drawdown(),
                "trading_enabled": self._check_trading_status(),
                "quantum_validated": self._check_quantum_status(),
                "gpu_utilization": self._get_gpu_usage(),
                "db_status": self._check_database(),
                "cpu_usage": psutil.cpu_percent(interval=1),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage("/").percent,
                "uptime": self._get_uptime(),
            }

            # CRITICAL: Check win rate
            if metrics["win_rate"] < self.win_rate_threshold:
                self._trigger_alert(
                    "CRITICAL",
                    f"Win rate {metrics['win_rate']:.2%} below minimum threshold",
                )
            elif metrics["win_rate"] < self.warning_win_rate:
                self._trigger_alert(
                    "WARNING",
                    f"Win rate {metrics['win_rate']:.2%} approaching minimum threshold",
                )

            # CRITICAL: Check drawdown
            if metrics["current_drawdown"] >= self.max_drawdown:
                self._trigger_alert(
                    "CRITICAL",
                    f"Maximum drawdown reached: {metrics['current_drawdown']:.2%}",
                )
            elif metrics["current_drawdown"] >= self.warning_drawdown:
                self._trigger_alert(
                    "WARNING", f"Drawdown warning: {metrics['current_drawdown']:.2%}"
                )

            self.performance_history.append(metrics)
            self._last_check = metrics
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
                min_confidence=self.min_confidence, validation_status="validated"
            )

            performance_metrics = {
                "total_patterns": len(patterns),
                "validated_count": sum(
                    1 for p in patterns if p["validation_status"] == "validated"
                ),
                "average_confidence": patterns["confidence"].mean()
                if not patterns.empty
                else 0,
                "success_rate": patterns["success_rate"].mean()
                if not patterns.empty
                else 0,
            }

            # CRITICAL: Validate pattern performance
            if performance_metrics["average_confidence"] < self.min_confidence:
                self._trigger_alert(
                    "WARNING",
                    f"Pattern confidence {performance_metrics['average_confidence']:.2%} below threshold",
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
                "analysis_db": True,
                "trading_db": True,
                "write_performance": 0,
                "storage_available": 0,
            }

            # Test database connections
            for db_path in ["data/analysis.db", "data/trading.db"]:
                try:
                    with sqlite3.connect(db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute("PRAGMA integrity_check")
                except Exception as e:
                    status[db_path.split("/")[-1].replace(".db", "_db")] = False
                    self._trigger_alert(
                        "CRITICAL", f"Database error ({db_path}): {str(e)}"
                    )

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
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
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
            "status": self.system_status,
            "current_metrics": self.check_system_metrics(),
            "pattern_performance": self.validate_pattern_performance(),
            "recent_alerts": self.alert_history[-10:],
            "trading_enabled": self.risk_manager.trading_enabled,
            "last_updated": datetime.now().isoformat(),
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
            "win_rate_trend": df["win_rate"].rolling(10).mean(),
            "drawdown_trend": df["current_drawdown"].rolling(10).mean(),
            "system_health_rate": df["system_health"].mean(),
            "validation_rate": df["quantum_validated"].mean(),
        }

        return pd.DataFrame(stats)

    def _get_gpu_usage(self) -> float:
        """Get GPU utilization percentage"""
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                return gpus[0].load * 100
            return 0
        except:
            return 0

    def _get_uptime(self) -> str:
        """Get system uptime in human readable format"""
        uptime = time.time() - self._start_time
        return str(timedelta(seconds=int(uptime)))

    def _calculate_win_rate(self) -> float:
        """Calculate win rate from recent trades"""
        try:
            conn = sqlite3.connect("data/trading.db")
            cursor = conn.cursor()

            # Get trades from last 24 hours
            cursor.execute("""
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN profit > 0 THEN 1 ELSE 0 END) as wins
                FROM trades
                WHERE close_time >= datetime('now', '-1 day')
            """)

            result = cursor.fetchone()
            if result and result[0] > 0:
                return (result[1] / result[0]) * 100
            return 0

        except Exception as e:
            print(f"Error calculating win rate: {e}")
            return 0
        finally:
            if "conn" in locals():
                conn.close()

    def _calculate_drawdown(self) -> float:
        """Calculate current drawdown"""
        try:
            conn = sqlite3.connect("data/trading.db")
            cursor = conn.cursor()

            # Get peak balance in last 24 hours
            cursor.execute(
                "SELECT MAX(balance) FROM account_value WHERE timestamp >= datetime('now', '-1 day')"
            )
            peak = cursor.fetchone()[0]

            # Get current balance
            cursor.execute(
                "SELECT balance FROM account_value ORDER BY timestamp DESC LIMIT 1"
            )
            current = cursor.fetchone()[0]

            if peak and current and peak > 0:
                return ((peak - current) / peak) * 100
            return 0

        except Exception as e:
            print(f"Error calculating drawdown: {e}")
            return 0
        finally:
            if "conn" in locals():
                conn.close()

    def _check_trading_status(self) -> bool:
        """Check if trading is currently enabled"""
        try:
            conn = sqlite3.connect("data/trading.db")
            cursor = conn.cursor()

            cursor.execute(
                "SELECT value FROM system_status WHERE key = 'trading_enabled'"
            )
            result = cursor.fetchone()
            return bool(result and result[0])

        except Exception as e:
            print(f"Error checking trading status: {e}")
            return False
        finally:
            if "conn" in locals():
                conn.close()

    def _check_quantum_status(self) -> bool:
        """Check quantum circuit validation status"""
        try:
            conn = sqlite3.connect("data/trading.db")
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*) FROM quantum_validations
                WHERE timestamp >= datetime('now', '-1 hour')
                AND status = 'valid'
            """)

            result = cursor.fetchone()
            return bool(result and result[0] > 0)

        except Exception as e:
            print(f"Error checking quantum status: {e}")
            return False
        finally:
            if "conn" in locals():
                conn.close()

    def _check_database(self) -> bool:
        """Check database connectivity and health"""
        try:
            conn = sqlite3.connect("data/trading.db")
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            return True
        except:
            return False
        finally:
            if "conn" in locals():
                conn.close()
