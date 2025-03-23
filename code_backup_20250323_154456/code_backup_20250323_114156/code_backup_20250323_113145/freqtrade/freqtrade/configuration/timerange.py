"""
This module contains the argument manager class
"""

import logging
import re
from datetime import datetime, timezone

from typing_extensions import Self

from freqtrade.constants import DATETIME_PRINT_FORMAT
from freqtrade.exceptions import ConfigurationError
from freqtrade.util import dt_from_ts


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class TimeRange:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     object defining timerange inputs.
# REMOVED_UNUSED_CODE:     [start/stop]type defines if [start/stop]ts shall be used.
# REMOVED_UNUSED_CODE:     if *type is None, don't use corresponding startvalue.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         starttype: str | None = None,
# REMOVED_UNUSED_CODE:         stoptype: str | None = None,
# REMOVED_UNUSED_CODE:         startts: int = 0,
# REMOVED_UNUSED_CODE:         stopts: int = 0,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         self.starttype: str | None = starttype
# REMOVED_UNUSED_CODE:         self.stoptype: str | None = stoptype
# REMOVED_UNUSED_CODE:         self.startts: int = startts
# REMOVED_UNUSED_CODE:         self.stopts: int = stopts
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def startdt(self) -> datetime | None:
# REMOVED_UNUSED_CODE:         if self.startts:
# REMOVED_UNUSED_CODE:             return dt_from_ts(self.startts)
# REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def stopdt(self) -> datetime | None:
# REMOVED_UNUSED_CODE:         if self.stopts:
# REMOVED_UNUSED_CODE:             return dt_from_ts(self.stopts)
# REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def timerange_str(self) -> str:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Returns a string representation of the timerange as used by parse_timerange.
# REMOVED_UNUSED_CODE:         Follows the format yyyymmdd-yyyymmdd - leaving out the parts that are not set.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         start = ""
# REMOVED_UNUSED_CODE:         stop = ""
# REMOVED_UNUSED_CODE:         if startdt := self.startdt:
# REMOVED_UNUSED_CODE:             start = startdt.strftime("%Y%m%d")
# REMOVED_UNUSED_CODE:         if stopdt := self.stopdt:
# REMOVED_UNUSED_CODE:             stop = stopdt.strftime("%Y%m%d")
# REMOVED_UNUSED_CODE:         return f"{start}-{stop}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def start_fmt(self) -> str:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Returns a string representation of the start date
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         val = "unbounded"
# REMOVED_UNUSED_CODE:         if (startdt := self.startdt) is not None:
# REMOVED_UNUSED_CODE:             val = startdt.strftime(DATETIME_PRINT_FORMAT)
# REMOVED_UNUSED_CODE:         return val
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def stop_fmt(self) -> str:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Returns a string representation of the stop date
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         val = "unbounded"
# REMOVED_UNUSED_CODE:         if (stopdt := self.stopdt) is not None:
# REMOVED_UNUSED_CODE:             val = stopdt.strftime(DATETIME_PRINT_FORMAT)
# REMOVED_UNUSED_CODE:         return val
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __eq__(self, other):
# REMOVED_UNUSED_CODE:         """Override the default Equals behavior"""
# REMOVED_UNUSED_CODE:         return (
# REMOVED_UNUSED_CODE:             self.starttype == other.starttype
# REMOVED_UNUSED_CODE:             and self.stoptype == other.stoptype
# REMOVED_UNUSED_CODE:             and self.startts == other.startts
# REMOVED_UNUSED_CODE:             and self.stopts == other.stopts
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def subtract_start(self, seconds: int) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Subtracts <seconds> from startts if startts is set.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param seconds: Seconds to subtract from starttime
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: None (Modifies the object in place)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.startts:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.startts = self.startts - seconds
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def adjust_start_if_necessary(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, timeframe_secs: int, startup_candles: int, min_date: datetime
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Adjust startts by <startup_candles> candles.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Applies only if no startup-candles have been available.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param timeframe_secs: Timeframe in seconds e.g. `timeframe_to_seconds('5m')`
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param startup_candles: Number of candles to move start-date forward
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param min_date: Minimum data date loaded. Key kriterium to decide if start-time
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                          has to be moved
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: None (Modifies the object in place)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not self.starttype or (startup_candles and min_date.timestamp() >= self.startts):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # If no startts was defined, or backtest-data starts at the defined backtest-date
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "Moving start-date by %s candles to account for startup time.", startup_candles
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.startts = int(min_date.timestamp() + timeframe_secs * startup_candles)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.starttype = "date"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @classmethod
# REMOVED_UNUSED_CODE:     def parse_timerange(cls, text: str | None) -> Self:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Parse the value of the argument --timerange to determine what is the range desired
# REMOVED_UNUSED_CODE:         :param text: value from --timerange
# REMOVED_UNUSED_CODE:         :return: Start and End range period
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not text:
# REMOVED_UNUSED_CODE:             return cls(None, None, 0, 0)
# REMOVED_UNUSED_CODE:         syntax = [
# REMOVED_UNUSED_CODE:             (r"^-(\d{8})$", (None, "date")),
# REMOVED_UNUSED_CODE:             (r"^(\d{8})-$", ("date", None)),
# REMOVED_UNUSED_CODE:             (r"^(\d{8})-(\d{8})$", ("date", "date")),
# REMOVED_UNUSED_CODE:             (r"^-(\d{10})$", (None, "date")),
# REMOVED_UNUSED_CODE:             (r"^(\d{10})-$", ("date", None)),
# REMOVED_UNUSED_CODE:             (r"^(\d{10})-(\d{10})$", ("date", "date")),
# REMOVED_UNUSED_CODE:             (r"^-(\d{13})$", (None, "date")),
# REMOVED_UNUSED_CODE:             (r"^(\d{13})-$", ("date", None)),
# REMOVED_UNUSED_CODE:             (r"^(\d{13})-(\d{13})$", ("date", "date")),
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         for rex, stype in syntax:
# REMOVED_UNUSED_CODE:             # Apply the regular expression to text
# REMOVED_UNUSED_CODE:             match = re.match(rex, text)
# REMOVED_UNUSED_CODE:             if match:  # Regex has matched
# REMOVED_UNUSED_CODE:                 rvals = match.groups()
# REMOVED_UNUSED_CODE:                 index = 0
# REMOVED_UNUSED_CODE:                 start: int = 0
# REMOVED_UNUSED_CODE:                 stop: int = 0
# REMOVED_UNUSED_CODE:                 if stype[0]:
# REMOVED_UNUSED_CODE:                     starts = rvals[index]
# REMOVED_UNUSED_CODE:                     if stype[0] == "date" and len(starts) == 8:
# REMOVED_UNUSED_CODE:                         start = int(
# REMOVED_UNUSED_CODE:                             datetime.strptime(starts, "%Y%m%d")
# REMOVED_UNUSED_CODE:                             .replace(tzinfo=timezone.utc)
# REMOVED_UNUSED_CODE:                             .timestamp()
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:                     elif len(starts) == 13:
# REMOVED_UNUSED_CODE:                         start = int(starts) // 1000
# REMOVED_UNUSED_CODE:                     else:
# REMOVED_UNUSED_CODE:                         start = int(starts)
# REMOVED_UNUSED_CODE:                     index += 1
# REMOVED_UNUSED_CODE:                 if stype[1]:
# REMOVED_UNUSED_CODE:                     stops = rvals[index]
# REMOVED_UNUSED_CODE:                     if stype[1] == "date" and len(stops) == 8:
# REMOVED_UNUSED_CODE:                         stop = int(
# REMOVED_UNUSED_CODE:                             datetime.strptime(stops, "%Y%m%d")
# REMOVED_UNUSED_CODE:                             .replace(tzinfo=timezone.utc)
# REMOVED_UNUSED_CODE:                             .timestamp()
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:                     elif len(stops) == 13:
# REMOVED_UNUSED_CODE:                         stop = int(stops) // 1000
# REMOVED_UNUSED_CODE:                     else:
# REMOVED_UNUSED_CODE:                         stop = int(stops)
# REMOVED_UNUSED_CODE:                 if start > stop > 0:
# REMOVED_UNUSED_CODE:                     raise ConfigurationError(
# REMOVED_UNUSED_CODE:                         f'Start date is after stop date for timerange "{text}"'
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 return cls(stype[0], stype[1], start, stop)
# REMOVED_UNUSED_CODE:         raise ConfigurationError(f'Incorrect syntax for timerange "{text}"')
