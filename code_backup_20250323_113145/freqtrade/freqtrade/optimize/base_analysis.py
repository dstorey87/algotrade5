import logging
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from pandas import DataFrame

from freqtrade.configuration import TimeRange


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


class VarHolder:
# REMOVED_UNUSED_CODE:     timerange: TimeRange
# REMOVED_UNUSED_CODE:     data: DataFrame
# REMOVED_UNUSED_CODE:     indicators: dict[str, DataFrame]
# REMOVED_UNUSED_CODE:     result: DataFrame
# REMOVED_UNUSED_CODE:     compared: DataFrame
# REMOVED_UNUSED_CODE:     from_dt: datetime
# REMOVED_UNUSED_CODE:     to_dt: datetime
# REMOVED_UNUSED_CODE:     compared_dt: datetime
# REMOVED_UNUSED_CODE:     timeframe: str
# REMOVED_UNUSED_CODE:     startup_candle: int


# REMOVED_UNUSED_CODE: class BaseAnalysis:
# REMOVED_UNUSED_CODE:     def __init__(self, config: dict[str, Any], strategy_obj: dict):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.failed_bias_check = True
# REMOVED_UNUSED_CODE:         self.full_varHolder = VarHolder()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.exchange: Any | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._fee = None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # pull variables the scope of the lookahead_analysis-instance
# REMOVED_UNUSED_CODE:         self.local_config = deepcopy(config)
# REMOVED_UNUSED_CODE:         self.local_config["strategy"] = strategy_obj["name"]
# REMOVED_UNUSED_CODE:         self.strategy_obj = strategy_obj
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def dt_to_timestamp(dt: datetime):
# REMOVED_UNUSED_CODE:         timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())
# REMOVED_UNUSED_CODE:         return timestamp
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fill_full_varholder(self):
# REMOVED_UNUSED_CODE:         self.full_varHolder = VarHolder()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # define datetime in human-readable format
# REMOVED_UNUSED_CODE:         parsed_timerange = TimeRange.parse_timerange(self.local_config["timerange"])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if parsed_timerange.startdt is None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.full_varHolder.from_dt = datetime.fromtimestamp(0, tz=timezone.utc)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.full_varHolder.from_dt = parsed_timerange.startdt
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if parsed_timerange.stopdt is None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.full_varHolder.to_dt = datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.full_varHolder.to_dt = parsed_timerange.stopdt
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.prepare_data(self.full_varHolder, self.local_config["pairs"])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def start(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # first make a single backtest
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.fill_full_varholder()
