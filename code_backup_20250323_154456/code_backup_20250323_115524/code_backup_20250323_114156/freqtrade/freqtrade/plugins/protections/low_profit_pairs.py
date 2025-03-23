import logging
from datetime import datetime, timedelta
from typing import Any

from freqtrade.constants import Config, LongShort
from freqtrade.persistence import Trade
from freqtrade.plugins.protections import IProtection, ProtectionReturn


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class LowProfitPairs(IProtection):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     has_global_stop: bool = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     has_local_stop: bool = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, config: Config, protection_config: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:         super().__init__(config, protection_config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._trade_limit = protection_config.get("trade_limit", 1)
# REMOVED_UNUSED_CODE:         self._required_profit = protection_config.get("required_profit", 0.0)
# REMOVED_UNUSED_CODE:         self._only_per_side = protection_config.get("only_per_side", False)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def short_desc(self) -> str:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Short method description - used for startup-messages
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"{self.name} - Low Profit Protection, locks pairs with "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"profit < {self._required_profit} within {self.lookback_period_str}."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _reason(self, profit: float) -> str:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         LockReason to use
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return (
# REMOVED_UNUSED_CODE:             f"{profit} < {self._required_profit} in {self.lookback_period_str}, "
# REMOVED_UNUSED_CODE:             f"locking {self.unlock_reason_time_element}."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _low_profit(
# REMOVED_UNUSED_CODE:         self, date_now: datetime, pair: str, side: LongShort
# REMOVED_UNUSED_CODE:     ) -> ProtectionReturn | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Evaluate recent trades for pair
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         look_back_until = date_now - timedelta(minutes=self._lookback_period)
# REMOVED_UNUSED_CODE:         # filters = [
# REMOVED_UNUSED_CODE:         #     Trade.is_open.is_(False),
# REMOVED_UNUSED_CODE:         #     Trade.close_date > look_back_until,
# REMOVED_UNUSED_CODE:         # ]
# REMOVED_UNUSED_CODE:         # if pair:
# REMOVED_UNUSED_CODE:         #     filters.append(Trade.pair == pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trades = Trade.get_trades_proxy(pair=pair, is_open=False, close_date=look_back_until)
# REMOVED_UNUSED_CODE:         # trades = Trade.get_trades(filters).all()
# REMOVED_UNUSED_CODE:         if len(trades) < self._trade_limit:
# REMOVED_UNUSED_CODE:             # Not enough trades in the relevant period
# REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         profit = sum(
# REMOVED_UNUSED_CODE:             trade.close_profit
# REMOVED_UNUSED_CODE:             for trade in trades
# REMOVED_UNUSED_CODE:             if trade.close_profit and (not self._only_per_side or trade.trade_direction == side)
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         if profit < self._required_profit:
# REMOVED_UNUSED_CODE:             self.log_once(
# REMOVED_UNUSED_CODE:                 f"Trading for {pair} stopped due to {profit:.2f} < {self._required_profit} "
# REMOVED_UNUSED_CODE:                 f"within {self._lookback_period} minutes.",
# REMOVED_UNUSED_CODE:                 logger.info,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             until = self.calculate_lock_end(trades)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             return ProtectionReturn(
# REMOVED_UNUSED_CODE:                 lock=True,
# REMOVED_UNUSED_CODE:                 until=until,
# REMOVED_UNUSED_CODE:                 reason=self._reason(profit),
# REMOVED_UNUSED_CODE:                 lock_side=(side if self._only_per_side else "*"),
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def global_stop(self, date_now: datetime, side: LongShort) -> ProtectionReturn | None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Stops trading (position entering) for all pairs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This must evaluate to true for the whole period of the "cooldown period".
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: Tuple of [bool, until, reason].
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             If true, all pairs will be locked with <reason> until <until>
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return None
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._low_profit(date_now, pair=pair, side=side)
