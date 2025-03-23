"""
Protection manager class
"""

import logging
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import datetime, timezone
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.constants import Config, LongShort
# REMOVED_UNUSED_CODE: from freqtrade.exceptions import ConfigurationError
# REMOVED_UNUSED_CODE: from freqtrade.persistence import PairLocks
# REMOVED_UNUSED_CODE: from freqtrade.persistence.models import PairLock
# REMOVED_UNUSED_CODE: from freqtrade.plugins.protections import IProtection
# REMOVED_UNUSED_CODE: from freqtrade.resolvers import ProtectionResolver


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class ProtectionManager:
# REMOVED_UNUSED_CODE:     def __init__(self, config: Config, protections: list) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._config = config
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._protection_handlers: list[IProtection] = []
# REMOVED_UNUSED_CODE:         self.validate_protections(protections)
# REMOVED_UNUSED_CODE:         for protection_handler_config in protections:
# REMOVED_UNUSED_CODE:             protection_handler = ProtectionResolver.load_protection(
# REMOVED_UNUSED_CODE:                 protection_handler_config["method"],
# REMOVED_UNUSED_CODE:                 config=config,
# REMOVED_UNUSED_CODE:                 protection_config=protection_handler_config,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             self._protection_handlers.append(protection_handler)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not self._protection_handlers:
# REMOVED_UNUSED_CODE:             logger.info("No protection Handlers defined.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def name_list(self) -> list[str]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get list of loaded Protection Handler names
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return [p.name for p in self._protection_handlers]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def short_desc(self) -> list[dict]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         List of short_desc for each Pairlist Handler
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return [{p.name: p.short_desc()} for p in self._protection_handlers]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def global_stop(self, now: datetime | None = None, side: LongShort = "long") -> PairLock | None:
# REMOVED_UNUSED_CODE:         if not now:
# REMOVED_UNUSED_CODE:             now = datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE:         result = None
# REMOVED_UNUSED_CODE:         for protection_handler in self._protection_handlers:
# REMOVED_UNUSED_CODE:             if protection_handler.has_global_stop:
# REMOVED_UNUSED_CODE:                 lock = protection_handler.global_stop(date_now=now, side=side)
# REMOVED_UNUSED_CODE:                 if lock and lock.until:
# REMOVED_UNUSED_CODE:                     if not PairLocks.is_global_lock(lock.until, side=lock.lock_side):
# REMOVED_UNUSED_CODE:                         result = PairLocks.lock_pair(
# REMOVED_UNUSED_CODE:                             "*", lock.until, lock.reason, now=now, side=lock.lock_side
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:         return result
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def stop_per_pair(
# REMOVED_UNUSED_CODE:         self, pair, now: datetime | None = None, side: LongShort = "long"
# REMOVED_UNUSED_CODE:     ) -> PairLock | None:
# REMOVED_UNUSED_CODE:         if not now:
# REMOVED_UNUSED_CODE:             now = datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE:         result = None
# REMOVED_UNUSED_CODE:         for protection_handler in self._protection_handlers:
# REMOVED_UNUSED_CODE:             if protection_handler.has_local_stop:
# REMOVED_UNUSED_CODE:                 lock = protection_handler.stop_per_pair(pair=pair, date_now=now, side=side)
# REMOVED_UNUSED_CODE:                 if lock and lock.until:
# REMOVED_UNUSED_CODE:                     if not PairLocks.is_pair_locked(pair, lock.until, lock.lock_side):
# REMOVED_UNUSED_CODE:                         result = PairLocks.lock_pair(
# REMOVED_UNUSED_CODE:                             pair, lock.until, lock.reason, now=now, side=lock.lock_side
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:         return result
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def validate_protections(protections: list[dict[str, Any]]) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Validate protection setup validity
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for prot in protections:
# REMOVED_UNUSED_CODE:             parsed_unlock_at = None
# REMOVED_UNUSED_CODE:             if (config_unlock_at := prot.get("unlock_at")) is not None:
# REMOVED_UNUSED_CODE:                 try:
# REMOVED_UNUSED_CODE:                     parsed_unlock_at = datetime.strptime(config_unlock_at, "%H:%M")
# REMOVED_UNUSED_CODE:                 except ValueError:
# REMOVED_UNUSED_CODE:                     raise ConfigurationError(
# REMOVED_UNUSED_CODE:                         f"Invalid date format for unlock_at: {config_unlock_at}."
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if "stop_duration" in prot and "stop_duration_candles" in prot:
# REMOVED_UNUSED_CODE:                 raise ConfigurationError(
# REMOVED_UNUSED_CODE:                     "Protections must specify either `stop_duration` or `stop_duration_candles`.\n"
# REMOVED_UNUSED_CODE:                     f"Please fix the protection {prot.get('method')}."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if "lookback_period" in prot and "lookback_period_candles" in prot:
# REMOVED_UNUSED_CODE:                 raise ConfigurationError(
# REMOVED_UNUSED_CODE:                     "Protections must specify either `lookback_period` or "
# REMOVED_UNUSED_CODE:                     f"`lookback_period_candles`.\n Please fix the protection {prot.get('method')}."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if parsed_unlock_at is not None and (
# REMOVED_UNUSED_CODE:                 "stop_duration" in prot or "stop_duration_candles" in prot
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 raise ConfigurationError(
# REMOVED_UNUSED_CODE:                     "Protections must specify either `unlock_at`, `stop_duration` or "
# REMOVED_UNUSED_CODE:                     "`stop_duration_candles`.\n"
# REMOVED_UNUSED_CODE:                     f"Please fix the protection {prot.get('method')}."
# REMOVED_UNUSED_CODE:                 )
