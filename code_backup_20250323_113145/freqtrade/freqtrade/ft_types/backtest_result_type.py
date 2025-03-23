from typing import Any

from typing_extensions import TypedDict


class BacktestMetadataType(TypedDict):
# REMOVED_UNUSED_CODE:     run_id: str
    backtest_start_time: int


class BacktestResultType(TypedDict):
# REMOVED_UNUSED_CODE:     metadata: dict[str, Any]  # BacktestMetadataType
# REMOVED_UNUSED_CODE:     strategy: dict[str, Any]
# REMOVED_UNUSED_CODE:     strategy_comparison: list[Any]


# REMOVED_UNUSED_CODE: def get_BacktestResultType_default() -> BacktestResultType:
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "metadata": {},
# REMOVED_UNUSED_CODE:         "strategy": {},
# REMOVED_UNUSED_CODE:         "strategy_comparison": [],
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: class BacktestHistoryEntryType(BacktestMetadataType):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     filename: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     strategy: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     notes: str
# REMOVED_UNUSED_CODE:     backtest_start_ts: int | None
# REMOVED_UNUSED_CODE:     backtest_end_ts: int | None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timeframe: str | None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timeframe_detail: str | None
