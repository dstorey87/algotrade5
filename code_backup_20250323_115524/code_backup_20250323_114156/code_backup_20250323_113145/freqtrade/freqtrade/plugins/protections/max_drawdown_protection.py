import logging
from datetime import datetime, timedelta
from typing import Any

import pandas as pd

from freqtrade.constants import Config, LongShort
from freqtrade.data.metrics import calculate_max_drawdown
from freqtrade.persistence import Trade
from freqtrade.plugins.protections import IProtection, ProtectionReturn


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class MaxDrawdown(IProtection):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     has_global_stop: bool = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     has_local_stop: bool = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, config: Config, protection_config: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:         super().__init__(config, protection_config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._trade_limit = protection_config.get("trade_limit", 1)
# REMOVED_UNUSED_CODE:         self._max_allowed_drawdown = protection_config.get("max_allowed_drawdown", 0.0)
# REMOVED_UNUSED_CODE:         # TODO: Implement checks to limit max_drawdown to sensible values
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def short_desc(self) -> str:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Short method description - used for startup-messages
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"{self.name} - Max drawdown protection, stop trading if drawdown is > "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"{self._max_allowed_drawdown} within {self.lookback_period_str}."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _reason(self, drawdown: float) -> str:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         LockReason to use
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return (
# REMOVED_UNUSED_CODE:             f"{drawdown} passed {self._max_allowed_drawdown} in {self.lookback_period_str}, "
# REMOVED_UNUSED_CODE:             f"locking {self.unlock_reason_time_element}."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _max_drawdown(self, date_now: datetime) -> ProtectionReturn | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Evaluate recent trades for drawdown ...
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         look_back_until = date_now - timedelta(minutes=self._lookback_period)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trades = Trade.get_trades_proxy(is_open=False, close_date=look_back_until)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trades_df = pd.DataFrame([trade.to_json() for trade in trades])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if len(trades) < self._trade_limit:
# REMOVED_UNUSED_CODE:             # Not enough trades in the relevant period
# REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Drawdown is always positive
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             # TODO: This should use absolute profit calculation, considering account balance.
# REMOVED_UNUSED_CODE:             drawdown_obj = calculate_max_drawdown(trades_df, value_col="close_profit")
# REMOVED_UNUSED_CODE:             drawdown = drawdown_obj.drawdown_abs
# REMOVED_UNUSED_CODE:         except ValueError:
# REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if drawdown > self._max_allowed_drawdown:
# REMOVED_UNUSED_CODE:             self.log_once(
# REMOVED_UNUSED_CODE:                 f"Trading stopped due to Max Drawdown {drawdown:.2f} > {self._max_allowed_drawdown}"
# REMOVED_UNUSED_CODE:                 f" within {self.lookback_period_str}.",
# REMOVED_UNUSED_CODE:                 logger.info,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             until = self.calculate_lock_end(trades)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             return ProtectionReturn(
# REMOVED_UNUSED_CODE:                 lock=True,
# REMOVED_UNUSED_CODE:                 until=until,
# REMOVED_UNUSED_CODE:                 reason=self._reason(drawdown),
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._max_drawdown(date_now)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def stop_per_pair(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pair: str, date_now: datetime, side: LongShort
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> ProtectionReturn | None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Stops trading (position entering) for this pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This must evaluate to true for the whole period of the "cooldown period".
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: Tuple of [bool, until, reason].
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             If true, this pair will be locked with <reason> until <until>
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return None
