import logging
from datetime import datetime, timedelta

from freqtrade.constants import LongShort
from freqtrade.persistence import Trade
from freqtrade.plugins.protections import IProtection, ProtectionReturn


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class CooldownPeriod(IProtection):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     has_global_stop: bool = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     has_local_stop: bool = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _reason(self) -> str:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         LockReason to use
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return f"Cooldown period for {self.unlock_reason_time_element}."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def short_desc(self) -> str:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Short method description - used for startup messages
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return f"{self.name} - Cooldown period {self.unlock_reason_time_element}."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _cooldown_period(self, pair: str, date_now: datetime) -> ProtectionReturn | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get last trade for this pair
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         look_back_until = date_now - timedelta(minutes=self._lookback_period)
# REMOVED_UNUSED_CODE:         # filters = [
# REMOVED_UNUSED_CODE:         #     Trade.is_open.is_(False),
# REMOVED_UNUSED_CODE:         #     Trade.close_date > look_back_until,
# REMOVED_UNUSED_CODE:         #     Trade.pair == pair,
# REMOVED_UNUSED_CODE:         # ]
# REMOVED_UNUSED_CODE:         # trade = Trade.get_trades(filters).first()
# REMOVED_UNUSED_CODE:         trades = Trade.get_trades_proxy(pair=pair, is_open=False, close_date=look_back_until)
# REMOVED_UNUSED_CODE:         if trades:
# REMOVED_UNUSED_CODE:             # Get latest trade
# REMOVED_UNUSED_CODE:             # Ignore type error as we know we only get closed trades.
# REMOVED_UNUSED_CODE:             trade = sorted(trades, key=lambda t: t.close_date)[-1]  # type: ignore
# REMOVED_UNUSED_CODE:             self.log_once(f"Cooldown for {pair} {self.unlock_reason_time_element}.", logger.info)
# REMOVED_UNUSED_CODE:             until = self.calculate_lock_end([trade])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             return ProtectionReturn(
# REMOVED_UNUSED_CODE:                 lock=True,
# REMOVED_UNUSED_CODE:                 until=until,
# REMOVED_UNUSED_CODE:                 reason=self._reason(),
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def global_stop(self, date_now: datetime, side: LongShort) -> ProtectionReturn | None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Stops trading (position entering) for all pairs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This must evaluate to true for the whole period of the "cooldown period".
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: Tuple of [bool, until, reason].
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             If true, all pairs will be locked with <reason> until <until>
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Not implemented for cooldown period.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def stop_per_pair(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pair: str, date_now: datetime, side: LongShort
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> ProtectionReturn | None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Stops trading (position entering) for this pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This must evaluate to true for the whole period of the "cooldown period".
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: Tuple of [bool, until, reason].
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             If true, this pair will be locked with <reason> until <until>
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._cooldown_period(pair, date_now)
