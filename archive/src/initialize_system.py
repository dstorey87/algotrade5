import asyncio
import logging
from pathlib import Path
from typing import Optional

from .services.system_metrics_service import SystemMetricsService

logger = logging.getLogger(__name__)


class SystemInitializer:
    def __init__(self):
        self.metrics_service: Optional[SystemMetricsService] = None

    async def initialize(self):
        """Initialize all system components"""
        try:
            # Ensure data directory exists
            Path("data").mkdir(exist_ok=True)

            # Initialize database if needed
            await self._init_database()

            # Start metrics collection service
            self.metrics_service = SystemMetricsService()
            asyncio.create_task(self.metrics_service.start())

            logger.info("System initialization complete")

        except Exception as e:
            logger.error(f"Error during system initialization: {e}")
            raise

    async def _init_database(self):
        """Initialize database with schema"""
        try:
            import sqlite3

            conn = sqlite3.connect("data/trading.db")
            cursor = conn.cursor()

            # Read and execute schema
            with open("data/schema.sql", "r") as schema_file:
                schema = schema_file.read()
                cursor.executescript(schema)

            conn.commit()
            logger.info("Database initialization complete")

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
        finally:
            if "conn" in locals():
                conn.close()

    async def shutdown(self):
        """Graceful system shutdown"""
        if self.metrics_service:
            self.metrics_service.stop()
        logger.info("System shutdown complete")
