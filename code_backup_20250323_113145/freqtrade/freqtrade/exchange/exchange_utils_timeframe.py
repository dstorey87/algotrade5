# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import datetime, timezone

# REMOVED_UNUSED_CODE: import ccxt
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from ccxt import ROUND_DOWN, ROUND_UP

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.util.datetime_helpers import dt_from_ts, dt_ts


# REMOVED_UNUSED_CODE: def timeframe_to_seconds(timeframe: str) -> int:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Translates the timeframe interval value written in the human readable
# REMOVED_UNUSED_CODE:     form ('1m', '5m', '1h', '1d', '1w', etc.) to the number
# REMOVED_UNUSED_CODE:     of seconds for one timeframe interval.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     return ccxt.Exchange.parse_timeframe(timeframe)


# REMOVED_UNUSED_CODE: def timeframe_to_minutes(timeframe: str) -> int:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Same as timeframe_to_seconds, but returns minutes.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     return ccxt.Exchange.parse_timeframe(timeframe) // 60


# REMOVED_UNUSED_CODE: def timeframe_to_msecs(timeframe: str) -> int:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Same as timeframe_to_seconds, but returns milliseconds.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     return ccxt.Exchange.parse_timeframe(timeframe) * 1000


# REMOVED_UNUSED_CODE: def timeframe_to_resample_freq(timeframe: str) -> str:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Translates the timeframe interval value written in the human readable
# REMOVED_UNUSED_CODE:     form ('1m', '5m', '1h', '1d', '1w', etc.) to the resample frequency
# REMOVED_UNUSED_CODE:     used by pandas ('1T', '5T', '1H', '1D', '1W', etc.)
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if timeframe == "1y":
# REMOVED_UNUSED_CODE:         return "1YS"
# REMOVED_UNUSED_CODE:     timeframe_seconds = timeframe_to_seconds(timeframe)
# REMOVED_UNUSED_CODE:     timeframe_minutes = timeframe_seconds // 60
# REMOVED_UNUSED_CODE:     resample_interval = f"{timeframe_seconds}s"
# REMOVED_UNUSED_CODE:     if 10000 < timeframe_minutes < 43200:
# REMOVED_UNUSED_CODE:         resample_interval = "1W-MON"
# REMOVED_UNUSED_CODE:     elif timeframe_minutes >= 43200 and timeframe_minutes < 525600:
# REMOVED_UNUSED_CODE:         # Monthly candles need special treatment to stick to the 1st of the month
# REMOVED_UNUSED_CODE:         resample_interval = f"{timeframe}S"
# REMOVED_UNUSED_CODE:     elif timeframe_minutes > 43200:
# REMOVED_UNUSED_CODE:         resample_interval = timeframe
# REMOVED_UNUSED_CODE:     return resample_interval


# REMOVED_UNUSED_CODE: def timeframe_to_prev_date(timeframe: str, date: datetime | None = None) -> datetime:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Use Timeframe and determine the candle start date for this date.
# REMOVED_UNUSED_CODE:     Does not round when given a candle start date.
# REMOVED_UNUSED_CODE:     :param timeframe: timeframe in string format (e.g. "5m")
# REMOVED_UNUSED_CODE:     :param date: date to use. Defaults to now(utc)
# REMOVED_UNUSED_CODE:     :returns: date of previous candle (with utc timezone)
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if not date:
# REMOVED_UNUSED_CODE:         date = datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     new_timestamp = ccxt.Exchange.round_timeframe(timeframe, dt_ts(date), ROUND_DOWN) // 1000
# REMOVED_UNUSED_CODE:     return dt_from_ts(new_timestamp)


# REMOVED_UNUSED_CODE: def timeframe_to_next_date(timeframe: str, date: datetime | None = None) -> datetime:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Use Timeframe and determine next candle.
# REMOVED_UNUSED_CODE:     :param timeframe: timeframe in string format (e.g. "5m")
# REMOVED_UNUSED_CODE:     :param date: date to use. Defaults to now(utc)
# REMOVED_UNUSED_CODE:     :returns: date of next candle (with utc timezone)
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if not date:
# REMOVED_UNUSED_CODE:         date = datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE:     new_timestamp = ccxt.Exchange.round_timeframe(timeframe, dt_ts(date), ROUND_UP) // 1000
# REMOVED_UNUSED_CODE:     return dt_from_ts(new_timestamp)
