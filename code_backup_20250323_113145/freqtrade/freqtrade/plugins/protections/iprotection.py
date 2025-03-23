import logging
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from abc import ABC, abstractmethod
from dataclasses import dataclass
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import datetime, timedelta, timezone
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.constants import Config, LongShort
# REMOVED_UNUSED_CODE: from freqtrade.exchange import timeframe_to_minutes
# REMOVED_UNUSED_CODE: from freqtrade.misc import plural
# REMOVED_UNUSED_CODE: from freqtrade.mixins import LoggingMixin
# REMOVED_UNUSED_CODE: from freqtrade.persistence import LocalTrade


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: @dataclass
class ProtectionReturn:
# REMOVED_UNUSED_CODE:     lock: bool
# REMOVED_UNUSED_CODE:     until: datetime
# REMOVED_UNUSED_CODE:     reason: str | None
# REMOVED_UNUSED_CODE:     lock_side: str = "*"


# REMOVED_UNUSED_CODE: class IProtection(LoggingMixin, ABC):
# REMOVED_UNUSED_CODE:     # Can globally stop the bot
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     has_global_stop: bool = False
# REMOVED_UNUSED_CODE:     # Can stop trading for one pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     has_local_stop: bool = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, config: Config, protection_config: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._config = config
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._protection_config = protection_config
# REMOVED_UNUSED_CODE:         self._stop_duration_candles: int | None = None
# REMOVED_UNUSED_CODE:         self._stop_duration: int = 0
# REMOVED_UNUSED_CODE:         self._lookback_period_candles: int | None = None
# REMOVED_UNUSED_CODE:         self._unlock_at: str | None = None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         tf_in_min = timeframe_to_minutes(config["timeframe"])
# REMOVED_UNUSED_CODE:         if "stop_duration_candles" in protection_config:
# REMOVED_UNUSED_CODE:             self._stop_duration_candles = int(protection_config.get("stop_duration_candles", 1))
# REMOVED_UNUSED_CODE:             self._stop_duration = tf_in_min * self._stop_duration_candles
# REMOVED_UNUSED_CODE:         elif "unlock_at" in protection_config:
# REMOVED_UNUSED_CODE:             self._unlock_at = protection_config.get("unlock_at")
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             self._stop_duration = int(protection_config.get("stop_duration", 60))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "lookback_period_candles" in protection_config:
# REMOVED_UNUSED_CODE:             self._lookback_period_candles = int(protection_config.get("lookback_period_candles", 1))
# REMOVED_UNUSED_CODE:             self._lookback_period = tf_in_min * self._lookback_period_candles
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             self._lookback_period_candles = None
# REMOVED_UNUSED_CODE:             self._lookback_period = int(protection_config.get("lookback_period", 60))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         LoggingMixin.__init__(self, logger)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def name(self) -> str:
# REMOVED_UNUSED_CODE:         return self.__class__.__name__
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def stop_duration_str(self) -> str:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Output configured stop duration in either candles or minutes
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self._stop_duration_candles:
# REMOVED_UNUSED_CODE:             return (
# REMOVED_UNUSED_CODE:                 f"{self._stop_duration_candles} "
# REMOVED_UNUSED_CODE:                 f"{plural(self._stop_duration_candles, 'candle', 'candles')}"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return f"{self._stop_duration} {plural(self._stop_duration, 'minute', 'minutes')}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def lookback_period_str(self) -> str:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Output configured lookback period in either candles or minutes
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self._lookback_period_candles:
# REMOVED_UNUSED_CODE:             return (
# REMOVED_UNUSED_CODE:                 f"{self._lookback_period_candles} "
# REMOVED_UNUSED_CODE:                 f"{plural(self._lookback_period_candles, 'candle', 'candles')}"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return f"{self._lookback_period} {plural(self._lookback_period, 'minute', 'minutes')}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def unlock_reason_time_element(self) -> str:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Output configured unlock time or stop duration
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self._unlock_at is not None:
# REMOVED_UNUSED_CODE:             return f"until {self._unlock_at}"
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return f"for {self.stop_duration_str}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def short_desc(self) -> str:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Short method description - used for startup-messages
# REMOVED_UNUSED_CODE:         -> Please overwrite in subclasses
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def global_stop(self, date_now: datetime, side: LongShort) -> ProtectionReturn | None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Stops trading (position entering) for all pairs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This must evaluate to true for the whole period of the "cooldown period".
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def stop_per_pair(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pair: str, date_now: datetime, side: LongShort
# REMOVED_UNUSED_CODE:     ) -> ProtectionReturn | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Stops trading (position entering) for this pair
# REMOVED_UNUSED_CODE:         This must evaluate to true for the whole period of the "cooldown period".
# REMOVED_UNUSED_CODE:         :return: Tuple of [bool, until, reason].
# REMOVED_UNUSED_CODE:             If true, this pair will be locked with <reason> until <until>
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def calculate_lock_end(self, trades: list[LocalTrade]) -> datetime:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Get lock end time
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Implicitly uses `self._stop_duration` or `self._unlock_at` depending on the configuration.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         max_date: datetime = max([trade.close_date for trade in trades if trade.close_date])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # coming from Database, tzinfo is not set.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if max_date.tzinfo is None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             max_date = max_date.replace(tzinfo=timezone.utc)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._unlock_at is not None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # unlock_at case with fixed hour of the day
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             hour, minutes = self._unlock_at.split(":")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             unlock_at = max_date.replace(hour=int(hour), minute=int(minutes))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if unlock_at < max_date:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 unlock_at += timedelta(days=1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return unlock_at
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         until = max_date + timedelta(minutes=self._stop_duration)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return until
