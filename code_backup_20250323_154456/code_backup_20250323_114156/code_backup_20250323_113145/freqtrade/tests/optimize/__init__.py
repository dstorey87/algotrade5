from datetime import timedelta
from typing import NamedTuple

from pandas import DataFrame

from freqtrade.enums import ExitType
from freqtrade.exchange import timeframe_to_minutes
from freqtrade.util.datetime_helpers import dt_utc


tests_start_time = dt_utc(2018, 10, 3)
tests_timeframe = "1h"


class BTrade(NamedTuple):
    """
    Minimalistic Trade result used for functional backtesting
    """

# REMOVED_UNUSED_CODE:     exit_reason: ExitType
# REMOVED_UNUSED_CODE:     open_tick: int
# REMOVED_UNUSED_CODE:     close_tick: int
# REMOVED_UNUSED_CODE:     enter_tag: str | None = None
# REMOVED_UNUSED_CODE:     is_short: bool = False


# REMOVED_UNUSED_CODE: class BTContainer(NamedTuple):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Minimal BacktestContainer defining Backtest inputs and results.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     data: list[list[float]]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stop_loss: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     roi: dict[str, float]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trades: list[BTrade]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_perc: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trailing_stop: bool = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trailing_only_offset_is_reached: bool = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trailing_stop_positive: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trailing_stop_positive_offset: float = 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     use_exit_signal: bool = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     use_custom_stoploss: bool = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     custom_entry_price: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     custom_exit_price: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     leverage: float = 1.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timeout: int | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     adjust_entry_price: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     adjust_trade_position: list[float] | None = None


def _get_frame_time_from_offset(offset):
    minutes = offset * timeframe_to_minutes(tests_timeframe)
    return tests_start_time + timedelta(minutes=minutes)


def _build_backtest_dataframe(data):
    columns = [
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "enter_long",
        "exit_long",
        "enter_short",
        "exit_short",
    ]
    if len(data[0]) == 8:
        # No short columns
        data = [d + [0, 0] for d in data]
    columns = columns + ["enter_tag"] if len(data[0]) == 11 else columns

    frame = DataFrame.from_records(data, columns=columns)
    frame["date"] = frame["date"].apply(_get_frame_time_from_offset)
    # Ensure floats are in place
    for column in ["open", "high", "low", "close", "volume"]:
        frame[column] = frame[column].astype("float64")

    # Ensure all candles make kindof sense
    assert all(frame["low"] <= frame["close"])
    assert all(frame["low"] <= frame["open"])
    assert all(frame["high"] >= frame["close"])
    assert all(frame["high"] >= frame["open"])
    return frame
