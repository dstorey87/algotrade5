"""
Cache Monitoring System
===================

Monitors and analyzes cache usage patterns for AlgoTradePro5.

CRITICAL REQUIREMENTS:
- Historical usage tracking
- Performance analysis
- Usage prediction
- Alert generation
"""

import json
import logging
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

from src.core.cache_manager import get_cache_manager
from src.core.config_manager import get_config
from src.core.error_manager import ErrorManager, ErrorSeverity

logger = logging.getLogger(__name__)


@dataclass
class CacheMetric:
    """Cache usage metric data structure"""

    timestamp: datetime
    cache_type: str
    size_mb: float
    usage_percent: float
    total_files: int
    performance_score: float


class CacheMonitor:
    """Monitors and analyzes cache usage patterns"""

    def __init__(self):
        """Initialize cache monitoring system"""
        self.cache_manager = get_cache_manager()
        self.config = get_config()
        self.error_manager = ErrorManager()

        # Database setup
        data_dir = Path(self.config.get("paths", "data_dir"))
        self.db_path = data_dir / "cache_metrics.db"

        # Initialize database
        self._init_database()

        # Monitoring settings
        self.check_interval = 300  # 5 minutes
        self.retention_days = 30
        self.alert_thresholds = {"critical": 90, "warning": 80, "notice": 70}

        logger.info("Cache Monitor initialized")

    def _init_database(self) -> None:
        """Initialize SQLite database for cache metrics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS cache_metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        cache_type TEXT NOT NULL,
                        size_mb REAL NOT NULL,
                        usage_percent REAL NOT NULL,
                        total_files INTEGER NOT NULL,
                        performance_score REAL NOT NULL
                    )
                """)
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_cache_metrics_timestamp
                    ON cache_metrics(timestamp)
                """)

        except Exception as e:
            self.error_manager.log_error(
                f"Failed to initialize cache metrics database: {e}",
                ErrorSeverity.HIGH.value,
                "CacheMonitor",
            )

    def record_metrics(self) -> None:
        """Record current cache metrics to database"""
        try:
            current_stats = self.cache_manager.get_cache_stats()
            timestamp = datetime.now().isoformat()

            metrics = []
            for cache_type, stats in current_stats.items():
                performance_score = self._calculate_performance_score(stats)

                metrics.append(
                    (
                        timestamp,
                        cache_type,
                        stats["size_mb"],
                        stats["usage_percent"],
                        stats["total_files"],
                        performance_score,
                    )
                )

            with sqlite3.connect(self.db_path) as conn:
                conn.executemany(
                    """
                    INSERT INTO cache_metrics
                    (timestamp, cache_type, size_mb, usage_percent, total_files, performance_score)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    metrics,
                )

        except Exception as e:
            self.error_manager.log_error(
                f"Failed to record cache metrics: {e}",
                ErrorSeverity.MEDIUM.value,
                "CacheMonitor",
            )

    def _calculate_performance_score(self, stats: Dict) -> float:
        """Calculate cache performance score"""
        # Factors: usage %, file count, and access patterns
        usage_score = (
            max(0, 100 - stats["usage_percent"]) / 100
        )  # Lower usage is better
        file_score = min(
            1.0, 1000 / max(1, stats["total_files"])
        )  # Fewer files is better

        # Weighted average
        weights = {"usage": 0.7, "files": 0.3}
        return usage_score * weights["usage"] + file_score * weights["files"]

    def analyze_trends(self, days: int = 7) -> Dict:
        """Analyze cache usage trends"""
        try:
            cutoff = (datetime.now() - timedelta(days=days)).isoformat()

            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    """
                    SELECT cache_type,
                           AVG(size_mb) as avg_size,
                           AVG(usage_percent) as avg_usage,
                           AVG(performance_score) as avg_performance,
                           MAX(usage_percent) as max_usage,
                           COUNT(*) as sample_count
                    FROM cache_metrics
                    WHERE timestamp > ?
                    GROUP BY cache_type
                """,
                    (cutoff,),
                ).fetchall()

            trends = {}
            for row in rows:
                trends[row["cache_type"]] = {
                    "avg_size_mb": row["avg_size"],
                    "avg_usage_percent": row["avg_usage"],
                    "avg_performance": row["avg_performance"],
                    "max_usage_percent": row["max_usage"],
                    "sample_count": row["sample_count"],
                }

            return trends

        except Exception as e:
            self.error_manager.log_error(
                f"Failed to analyze cache trends: {e}",
                ErrorSeverity.MEDIUM.value,
                "CacheMonitor",
            )
            return {}

    def predict_cleanup_needed(self, cache_type: str, hours_ahead: int = 24) -> bool:
        """Predict if cache cleanup will be needed"""
        try:
            cutoff = (datetime.now() - timedelta(days=7)).isoformat()

            with sqlite3.connect(self.db_path) as conn:
                # Get recent usage pattern
                data = conn.execute(
                    """
                    SELECT usage_percent
                    FROM cache_metrics
                    WHERE cache_type = ? AND timestamp > ?
                    ORDER BY timestamp ASC
                """,
                    (cache_type, cutoff),
                ).fetchall()

            if not data:
                return False

            # Calculate growth rate
            usage_values = [row[0] for row in data]
            growth_rate = np.polyfit(range(len(usage_values)), usage_values, 1)[0]

            # Current usage
            current_usage = self.cache_manager.get_cache_stats()[cache_type][
                "usage_percent"
            ]

            # Predict future usage
            predicted_usage = current_usage + (growth_rate * hours_ahead)

            return predicted_usage > self.alert_thresholds["warning"]

        except Exception as e:
            self.error_manager.log_error(
                f"Failed to predict cache cleanup needs: {e}",
                ErrorSeverity.LOW.value,
                "CacheMonitor",
            )
            return False

    def cleanup_old_metrics(self) -> None:
        """Clean up old metrics from database"""
        try:
            cutoff = (datetime.now() - timedelta(days=self.retention_days)).isoformat()

            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM cache_metrics WHERE timestamp < ?", (cutoff,))
                conn.execute("VACUUM")

        except Exception as e:
            self.error_manager.log_error(
                f"Failed to clean up old metrics: {e}",
                ErrorSeverity.LOW.value,
                "CacheMonitor",
            )


# Global instance
_cache_monitor = None


def get_cache_monitor():
    """Get global cache monitor instance"""
    global _cache_monitor
    if _cache_monitor is None:
        _cache_monitor = CacheMonitor()
    return _cache_monitor
