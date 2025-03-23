"""
Cache Monitoring Service
=====================

Background service for continuous cache monitoring and maintenance.
"""

import logging
import threading
import time
from datetime import datetime
from pathlib import Path
# REMOVED_UNUSED_CODE: from typing import Dict

from src.core.cache_manager import get_cache_manager
from src.core.config_manager import get_config
from src.core.error_manager import ErrorManager, ErrorSeverity

logger = logging.getLogger(__name__)


class CacheMonitorService(threading.Thread):
    """Background service for cache monitoring"""

    def __init__(self):
        """Initialize monitoring service"""
        super().__init__(daemon=True)
        self.config = get_config()
        self.cache_manager = get_cache_manager()
        self.error_manager = ErrorManager()

        # Get workspace paths with defaults
        workspace_root = Path(self.config.get("paths", "BASE_PATH", str(Path.cwd())))
        self.programdata_dir = workspace_root / "docker" / "programdata"
        self.programdata_dir.mkdir(parents=True, exist_ok=True)

        # Service control
        self._stop_event = threading.Event()
# REMOVED_UNUSED_CODE:         self._last_cleanup = {}
        self._last_check = datetime.now()

        # Alert settings from config with defaults
        self.alert_settings = {
            "check_interval": int(
                self.config.get("resources", "health_check_interval", 300)
            ),
            "cleanup_interval": int(
                self.config.get("resources", "backup_interval", 3600)
            ),
            "alert_enabled": True,
            "alert_cooldown": 1800,  # 30 minutes between repeated alerts
        }

        # Track last alert times
        self._last_alert = {}

        logger.info(
            f"Cache Monitor Service initialized with workspace path: {workspace_root}"
        )

    def run(self) -> None:
        """Main service loop"""
        while not self._stop_event.is_set():
            try:
                # Check cache status
                self._check_cache_status()

                # Run maintenance if needed
                self._run_maintenance()

                # Sleep until next check
                time.sleep(self.alert_settings["check_interval"])

            except Exception as e:
                self.error_manager.log_error(
                    f"Cache monitor service error: {e}",
                    ErrorSeverity.HIGH.value,
                    "CacheMonitorService",
                )
                time.sleep(60)  # Wait before retry

# REMOVED_UNUSED_CODE:     def stop(self) -> None:
# REMOVED_UNUSED_CODE:         """Stop the monitoring service"""
# REMOVED_UNUSED_CODE:         self._stop_event.set()

    def _check_cache_status(self) -> None:
        """Check cache status and generate alerts"""
        try:
            # Get current cache statistics
            cache_stats = self.cache_manager.get_cache_stats()

            for cache_type, stats in cache_stats.items():
                cache_path = self.programdata_dir / f"{cache_type}_cache"
                if not cache_path.exists():
                    logger.warning(f"Cache directory missing: {cache_path}")
                    cache_path.mkdir(parents=True, exist_ok=True)
                    continue

                current_usage = stats.get("usage_percent", 0)
                if current_usage > 90:
                    self._send_alert(
                        cache_type,
                        "CRITICAL",
                        f"Cache usage critical: {current_usage:.1f}%",
                    )
                elif current_usage > 80:
                    self._send_alert(
                        cache_type, "WARNING", f"Cache usage high: {current_usage:.1f}%"
                    )

        except Exception as e:
            self.error_manager.log_error(
                f"Failed to check cache status: {e}",
                ErrorSeverity.MEDIUM.value,
                "CacheMonitorService",
            )

    def _run_maintenance(self) -> None:
        """Run maintenance tasks if needed"""
        try:
            current_time = datetime.now()

            # Check if maintenance is due
            if (current_time - self._last_check).total_seconds() >= self.alert_settings[
                "cleanup_interval"
            ]:
                logger.info("Running scheduled cache maintenance")

                # Clean up caches over 80% usage
                cache_stats = self.cache_manager.get_cache_stats()
                for cache_type, stats in cache_stats.items():
                    if stats.get("usage_percent", 0) > 80:
                        self.cache_manager.cleanup_cache(cache_type)

                self._last_check = current_time

        except Exception as e:
            self.error_manager.log_error(
                f"Failed to run maintenance: {e}",
                ErrorSeverity.MEDIUM.value,
                "CacheMonitorService",
            )

    def _send_alert(self, cache_type: str, severity: str, message: str) -> None:
        """Send alert if cooldown has expired"""
        if not self.alert_settings["alert_enabled"]:
            return

        current_time = datetime.now()
        alert_key = f"{cache_type}_{severity}"

        # Check cooldown
        if (
            alert_key in self._last_alert
            and (current_time - self._last_alert[alert_key]).total_seconds()
            < self.alert_settings["alert_cooldown"]
        ):
            return

        try:
            # Log alert
            if severity == "CRITICAL":
                logger.critical(f"Cache Alert - {message}")
            elif severity == "WARNING":
                logger.warning(f"Cache Alert - {message}")
            else:
                logger.info(f"Cache Alert - {message}")

            # Update last alert time
            self._last_alert[alert_key] = current_time

        except Exception as e:
            self.error_manager.log_error(
                f"Failed to send alert: {e}",
                ErrorSeverity.LOW.value,
                "CacheMonitorService",
            )


# Global instance
_cache_monitor_service = None


# REMOVED_UNUSED_CODE: def get_cache_monitor_service():
# REMOVED_UNUSED_CODE:     """Get global cache monitor service instance"""
# REMOVED_UNUSED_CODE:     global _cache_monitor_service
# REMOVED_UNUSED_CODE:     if _cache_monitor_service is None:
# REMOVED_UNUSED_CODE:         _cache_monitor_service = CacheMonitorService()
# REMOVED_UNUSED_CODE:     return _cache_monitor_service
