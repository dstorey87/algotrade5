"""
Cache Cleanup Scheduler
====================

Manages automated cache maintenance and cleanup schedules.

CRITICAL REQUIREMENTS:
- Scheduled cleanups
- Resource-aware scheduling
- Priority-based cleanup
- Cleanup verification
"""

import heapq
import logging
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from src.core.cache_manager import get_cache_manager
from src.core.config_manager import get_config
from src.core.error_manager import ErrorManager, ErrorSeverity
from src.monitoring.cache_monitor import get_cache_monitor

logger = logging.getLogger(__name__)


@dataclass(order=True)
class CleanupTask:
    """Represents a scheduled cache cleanup task"""

    priority: int
    cache_type: str
    scheduled_time: datetime
    force: bool = False

    def __lt__(self, other):
        return (self.priority, self.scheduled_time) < (
            other.priority,
            other.scheduled_time,
        )


class CacheCleanupScheduler(threading.Thread):
    """Manages cache cleanup scheduling and execution"""

    def __init__(self):
        """Initialize cleanup scheduler"""
        super().__init__(daemon=True)
        self.config = get_config()
        self.cache_manager = get_cache_manager()
        self.cache_monitor = get_cache_monitor()
        self.error_manager = ErrorManager()

        # Task queue and control
        self._task_queue = []  # Priority queue
        self._task_lock = threading.Lock()
        self._stop_event = threading.Event()

        # Cleanup thresholds
        self.cleanup_thresholds = {
            "critical": 90,  # Immediate cleanup
            "high": 80,  # Schedule within 1 hour
            "medium": 70,  # Schedule within 4 hours
            "low": 60,  # Schedule within 12 hours
        }

        # Default scheduling windows (in hours)
        self.schedule_windows = {
            "critical": 0,  # Immediate
            "high": 1,
            "medium": 4,
            "low": 12,
        }

        logger.info("Cache Cleanup Scheduler initialized")

    def run(self) -> None:
        """Main scheduler loop"""
        while not self._stop_event.is_set():
            try:
                # Process due tasks
                self._process_due_tasks()

                # Check for new tasks
                self._check_cache_status()

                # Sleep briefly
                time.sleep(60)  # Check every minute

            except Exception as e:
                self.error_manager.log_error(
                    f"Cache cleanup scheduler error: {e}",
                    ErrorSeverity.HIGH.value,
                    "CacheCleanupScheduler",
                )
                time.sleep(60)  # Wait before retry

    def stop(self) -> None:
        """Stop the scheduler"""
        self._stop_event.set()

    def schedule_cleanup(
        self,
        cache_type: str,
        priority: int,
        scheduled_time: Optional[datetime] = None,
        force: bool = False,
    ) -> bool:
        """Schedule a cache cleanup task"""
        try:
            if scheduled_time is None:
                scheduled_time = datetime.now()

            task = CleanupTask(
                priority=priority,
                cache_type=cache_type,
                scheduled_time=scheduled_time,
                force=force,
            )

            with self._task_lock:
                heapq.heappush(self._task_queue, task)

            logger.info(f"Scheduled cleanup for {cache_type} at {scheduled_time}")
            return True

        except Exception as e:
            self.error_manager.log_error(
                f"Failed to schedule cleanup task: {e}",
                ErrorSeverity.MEDIUM.value,
                "CacheCleanupScheduler",
            )
            return False

    def _process_due_tasks(self) -> None:
        """Process any due cleanup tasks"""
        current_time = datetime.now()

        with self._task_lock:
            # Process tasks that are due
            while (
                self._task_queue and self._task_queue[0].scheduled_time <= current_time
            ):
                task = heapq.heappop(self._task_queue)

                try:
                    logger.info(f"Executing cleanup task for {task.cache_type}")
                    self.cache_manager.cleanup_cache(task.cache_type, task.force)

                    # Verify cleanup
                    self._verify_cleanup(task.cache_type)

                except Exception as e:
                    self.error_manager.log_error(
                        f"Failed to execute cleanup task: {e}",
                        ErrorSeverity.MEDIUM.value,
                        "CacheCleanupScheduler",
                    )

    def _check_cache_status(self) -> None:
        """Check cache status and schedule cleanups if needed"""
        try:
            cache_stats = self.cache_monitor.get_cache_stats()
            current_time = datetime.now()

            for cache_type, stats in cache_stats.items():
                usage = stats["usage_percent"]

                # Determine cleanup priority and schedule
                if usage >= self.cleanup_thresholds["critical"]:
                    self.schedule_cleanup(
                        cache_type,
                        priority=0,  # Highest priority
                        scheduled_time=current_time,
                        force=True,
                    )
                elif usage >= self.cleanup_thresholds["high"]:
                    self.schedule_cleanup(
                        cache_type,
                        priority=1,
                        scheduled_time=current_time
                        + timedelta(hours=self.schedule_windows["high"]),
                    )
                elif usage >= self.cleanup_thresholds["medium"]:
                    self.schedule_cleanup(
                        cache_type,
                        priority=2,
                        scheduled_time=current_time
                        + timedelta(hours=self.schedule_windows["medium"]),
                    )
                elif usage >= self.cleanup_thresholds["low"]:
                    self.schedule_cleanup(
                        cache_type,
                        priority=3,
                        scheduled_time=current_time
                        + timedelta(hours=self.schedule_windows["low"]),
                    )

        except Exception as e:
            self.error_manager.log_error(
                f"Failed to check cache status: {e}",
                ErrorSeverity.MEDIUM.value,
                "CacheCleanupScheduler",
            )

    def _verify_cleanup(self, cache_type: str) -> None:
        """Verify cleanup was successful"""
        try:
            # Get updated stats
            stats = self.cache_monitor.get_cache_stats()
            if cache_type not in stats:
                logger.warning(
                    f"Could not verify cleanup for {cache_type} - cache not found"
                )
                return

            usage = stats[cache_type]["usage_percent"]

            # Check if usage is still high
            if usage >= self.cleanup_thresholds["high"]:
                logger.warning(
                    f"Cleanup may not have been effective for {cache_type} - usage still at {usage:.1f}%"
                )

                # Schedule emergency cleanup if critical
                if usage >= self.cleanup_thresholds["critical"]:
                    self.schedule_cleanup(
                        cache_type,
                        priority=0,
                        scheduled_time=datetime.now(),
                        force=True,
                    )

        except Exception as e:
            self.error_manager.log_error(
                f"Failed to verify cleanup: {e}",
                ErrorSeverity.LOW.value,
                "CacheCleanupScheduler",
            )


# Global instance
_cleanup_scheduler = None


def get_cleanup_scheduler():
    """Get global cleanup scheduler instance"""
    global _cleanup_scheduler
    if _cleanup_scheduler is None:
        _cleanup_scheduler = CacheCleanupScheduler()
    return _cleanup_scheduler
