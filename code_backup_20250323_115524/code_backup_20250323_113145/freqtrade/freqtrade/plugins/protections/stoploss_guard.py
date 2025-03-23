import logging
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import datetime, timedelta
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.constants import Config, LongShort
# REMOVED_UNUSED_CODE: from freqtrade.enums import ExitType
# REMOVED_UNUSED_CODE: from freqtrade.persistence import Trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.plugins.protections import IProtection, ProtectionReturn


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class StoplossGuard(IProtection):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     has_global_stop: bool = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     has_local_stop: bool = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, config: Config, protection_config: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:         super().__init__(config, protection_config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._trade_limit = protection_config.get("trade_limit", 10)
# REMOVED_UNUSED_CODE:         self._disable_global_stop = protection_config.get("only_per_pair", False)
# REMOVED_UNUSED_CODE:         self._only_per_side = protection_config.get("only_per_side", False)
# REMOVED_UNUSED_CODE:         self._profit_limit = protection_config.get("required_profit", 0.0)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def short_desc(self) -> str:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Short method description - used for startup-messages
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"{self.name} - Frequent Stoploss Guard, {self._trade_limit} stoplosses "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"with profit < {self._profit_limit:.2%} within {self.lookback_period_str}."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _reason(self) -> str:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         LockReason to use
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return (
# REMOVED_UNUSED_CODE:             f"{self._trade_limit} stoplosses in {self._lookback_period} min, "
# REMOVED_UNUSED_CODE:             f"locking {self.unlock_reason_time_element}."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _stoploss_guard(
# REMOVED_UNUSED_CODE:         self, date_now: datetime, pair: str | None, side: LongShort
# REMOVED_UNUSED_CODE:     ) -> ProtectionReturn | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Evaluate recent trades
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         look_back_until = date_now - timedelta(minutes=self._lookback_period)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trades1 = Trade.get_trades_proxy(pair=pair, is_open=False, close_date=look_back_until)
# REMOVED_UNUSED_CODE:         trades = [
# REMOVED_UNUSED_CODE:             trade
# REMOVED_UNUSED_CODE:             for trade in trades1
# REMOVED_UNUSED_CODE:             if (
# REMOVED_UNUSED_CODE:                 str(trade.exit_reason)
# REMOVED_UNUSED_CODE:                 in (
# REMOVED_UNUSED_CODE:                     ExitType.TRAILING_STOP_LOSS.value,
# REMOVED_UNUSED_CODE:                     ExitType.STOP_LOSS.value,
# REMOVED_UNUSED_CODE:                     ExitType.STOPLOSS_ON_EXCHANGE.value,
# REMOVED_UNUSED_CODE:                     ExitType.LIQUIDATION.value,
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 and trade.close_profit
# REMOVED_UNUSED_CODE:                 and trade.close_profit < self._profit_limit
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._only_per_side:
# REMOVED_UNUSED_CODE:             # Long or short trades only
# REMOVED_UNUSED_CODE:             trades = [trade for trade in trades if trade.trade_direction == side]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if len(trades) < self._trade_limit:
# REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.log_once(
# REMOVED_UNUSED_CODE:             f"Trading stopped due to {self._trade_limit} "
# REMOVED_UNUSED_CODE:             f"stoplosses within {self._lookback_period} minutes.",
# REMOVED_UNUSED_CODE:             logger.info,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         until = self.calculate_lock_end(trades)
# REMOVED_UNUSED_CODE:         return ProtectionReturn(
# REMOVED_UNUSED_CODE:             lock=True,
# REMOVED_UNUSED_CODE:             until=until,
# REMOVED_UNUSED_CODE:             reason=self._reason(),
# REMOVED_UNUSED_CODE:             lock_side=(side if self._only_per_side else "*"),
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def global_stop(self, date_now: datetime, side: LongShort) -> ProtectionReturn | None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Stops trading (position entering) for all pairs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This must evaluate to true for the whole period of the "cooldown period".
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: Tuple of [bool, until, reason].
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             If true, all pairs will be locked with <reason> until <until>
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._disable_global_stop:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._stoploss_guard(date_now, None, side)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def stop_per_pair(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pair: str, date_now: datetime, side: LongShort
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> ProtectionReturn | None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Stops trading (position entering) for this pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This must evaluate to true for the whole period of the "cooldown period".
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: Tuple of [bool, until, reason].
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             If true, this pair will be locked with <reason> until <until>
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._stoploss_guard(date_now, pair, side)
