import asyncio
import sqlite3
from datetime import datetime
import logging
from ..monitoring.system_monitor import SystemMonitor

logger = logging.getLogger(__name__)

class SystemMetricsService:
    def __init__(self, db_path='data/trading.db', collection_interval=60):
        self.db_path = db_path
        self.collection_interval = collection_interval
        self.monitor = SystemMonitor()
        self.is_running = False
    
    async def start(self):
        """Start the metrics collection service"""
        self.is_running = True
        while self.is_running:
            try:
                metrics = self.monitor.check_system_metrics()
                self._store_metrics(metrics)
                await asyncio.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"Error collecting metrics: {e}")
                await asyncio.sleep(5)  # Brief pause on error
    
    def stop(self):
        """Stop the metrics collection service"""
        self.is_running = False
    
    def _store_metrics(self, metrics):
        """Store metrics in the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO system_metrics (
                    cpu_usage, memory_usage, disk_usage, gpu_utilization,
                    win_rate, drawdown, trading_enabled, quantum_validated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                metrics["cpu_usage"],
                metrics["memory_usage"],
                metrics["disk_usage"],
                metrics["gpu_utilization"],
                metrics["win_rate"],
                metrics["current_drawdown"],
                metrics["trading_enabled"],
                metrics["quantum_validated"]
            ))
            
            conn.commit()
        except Exception as e:
            logger.error(f"Error storing metrics: {e}")
        finally:
            if 'conn' in locals():
                conn.close()