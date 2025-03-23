# REMOVED_UNUSED_CODE: import re
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import datetime, timezone
# REMOVED_UNUSED_CODE: from time import time

# REMOVED_UNUSED_CODE: import humanize

# REMOVED_UNUSED_CODE: from freqtrade.constants import DATETIME_PRINT_FORMAT


# REMOVED_UNUSED_CODE: def dt_now() -> datetime:
# REMOVED_UNUSED_CODE:     """Return the current datetime in UTC."""
# REMOVED_UNUSED_CODE:     return datetime.now(timezone.utc)


# REMOVED_UNUSED_CODE: def dt_utc(
# REMOVED_UNUSED_CODE:     year: int,
# REMOVED_UNUSED_CODE:     month: int,
# REMOVED_UNUSED_CODE:     day: int,
# REMOVED_UNUSED_CODE:     hour: int = 0,
# REMOVED_UNUSED_CODE:     minute: int = 0,
# REMOVED_UNUSED_CODE:     second: int = 0,
# REMOVED_UNUSED_CODE:     microsecond: int = 0,
# REMOVED_UNUSED_CODE: ) -> datetime:
# REMOVED_UNUSED_CODE:     """Return a datetime in UTC."""
# REMOVED_UNUSED_CODE:     return datetime(year, month, day, hour, minute, second, microsecond, tzinfo=timezone.utc)


# REMOVED_UNUSED_CODE: def dt_ts(dt: datetime | None = None) -> int:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Return dt in ms as a timestamp in UTC.
# REMOVED_UNUSED_CODE:     If dt is None, return the current datetime in UTC.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if dt:
# REMOVED_UNUSED_CODE:         return int(dt.timestamp() * 1000)
# REMOVED_UNUSED_CODE:     return int(time() * 1000)


# REMOVED_UNUSED_CODE: def dt_ts_def(dt: datetime | None, default: int = 0) -> int:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Return dt in ms as a timestamp in UTC.
# REMOVED_UNUSED_CODE:     If dt is None, return the given default.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if dt:
# REMOVED_UNUSED_CODE:         return int(dt.timestamp() * 1000)
# REMOVED_UNUSED_CODE:     return default


# REMOVED_UNUSED_CODE: def dt_ts_none(dt: datetime | None) -> int | None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Return dt in ms as a timestamp in UTC.
# REMOVED_UNUSED_CODE:     If dt is None, return the given default.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if dt:
# REMOVED_UNUSED_CODE:         return int(dt.timestamp() * 1000)
# REMOVED_UNUSED_CODE:     return None


# REMOVED_UNUSED_CODE: def dt_floor_day(dt: datetime) -> datetime:
# REMOVED_UNUSED_CODE:     """Return the floor of the day for the given datetime."""
# REMOVED_UNUSED_CODE:     return dt.replace(hour=0, minute=0, second=0, microsecond=0)


# REMOVED_UNUSED_CODE: def dt_from_ts(timestamp: float) -> datetime:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Return a datetime from a timestamp.
# REMOVED_UNUSED_CODE:     :param timestamp: timestamp in seconds or milliseconds
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if timestamp > 1e10:
# REMOVED_UNUSED_CODE:         # Timezone in ms - convert to seconds
# REMOVED_UNUSED_CODE:         timestamp /= 1000
# REMOVED_UNUSED_CODE:     return datetime.fromtimestamp(timestamp, tz=timezone.utc)


# REMOVED_UNUSED_CODE: def shorten_date(_date: str) -> str:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Trim the date so it fits on small screens
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     new_date = re.sub("seconds?", "sec", _date)
# REMOVED_UNUSED_CODE:     new_date = re.sub("minutes?", "min", new_date)
# REMOVED_UNUSED_CODE:     new_date = re.sub("hours?", "h", new_date)
# REMOVED_UNUSED_CODE:     new_date = re.sub("days?", "d", new_date)
# REMOVED_UNUSED_CODE:     new_date = re.sub("^an?", "1", new_date)
# REMOVED_UNUSED_CODE:     return new_date


# REMOVED_UNUSED_CODE: def dt_humanize_delta(dt: datetime):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Return a humanized string for the given timedelta.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     return humanize.naturaltime(dt)


# REMOVED_UNUSED_CODE: def format_date(date: datetime | None) -> str:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Return a formatted date string.
# REMOVED_UNUSED_CODE:     Returns an empty string if date is None.
# REMOVED_UNUSED_CODE:     :param date: datetime to format
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if date:
# REMOVED_UNUSED_CODE:         return date.strftime(DATETIME_PRINT_FORMAT)
# REMOVED_UNUSED_CODE:     return ""


# REMOVED_UNUSED_CODE: def format_ms_time(date: int | float) -> str:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     convert MS date to readable format.
# REMOVED_UNUSED_CODE:     : epoch-string in ms
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     return dt_from_ts(date).strftime("%Y-%m-%dT%H:%M:%S")


# REMOVED_UNUSED_CODE: def format_ms_time_det(date: int | float) -> str:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     convert MS date to readable format - detailed.
# REMOVED_UNUSED_CODE:     : epoch-string in ms
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     # return dt_from_ts(date).isoformat(timespec="milliseconds")
# REMOVED_UNUSED_CODE:     return dt_from_ts(date).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
