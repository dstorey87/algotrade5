"""
Various tool function for Freqtrade and scripts
"""

# REMOVED_UNUSED_CODE: import gzip
import logging
# REMOVED_UNUSED_CODE: from collections.abc import Iterator, Mapping
# REMOVED_UNUSED_CODE: from io import StringIO
# REMOVED_UNUSED_CODE: from pathlib import Path
from typing import Any, TextIO
# REMOVED_UNUSED_CODE: from urllib.parse import urlparse

# REMOVED_UNUSED_CODE: import pandas as pd
import rapidjson

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.enums import SignalTagType, SignalType


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: def dump_json_to_file(file_obj: TextIO, data: Any) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Dump JSON data into a file object
# REMOVED_UNUSED_CODE:     :param file_obj: File object to write to
# REMOVED_UNUSED_CODE:     :param data: JSON Data to save
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     rapidjson.dump(data, file_obj, default=str, number_mode=rapidjson.NM_NATIVE)


# REMOVED_UNUSED_CODE: def file_dump_json(filename: Path, data: Any, is_zip: bool = False, log: bool = True) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Dump JSON data into a file
# REMOVED_UNUSED_CODE:     :param filename: file to create
# REMOVED_UNUSED_CODE:     :param is_zip: if file should be zip
# REMOVED_UNUSED_CODE:     :param data: JSON Data to save
# REMOVED_UNUSED_CODE:     :return:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if is_zip:
# REMOVED_UNUSED_CODE:         if filename.suffix != ".gz":
# REMOVED_UNUSED_CODE:             filename = filename.with_suffix(".gz")
# REMOVED_UNUSED_CODE:         if log:
# REMOVED_UNUSED_CODE:             logger.info(f'dumping json to "{filename}"')
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         with gzip.open(filename, "wt", encoding="utf-8") as fpz:
# REMOVED_UNUSED_CODE:             dump_json_to_file(fpz, data)
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         if log:
# REMOVED_UNUSED_CODE:             logger.info(f'dumping json to "{filename}"')
# REMOVED_UNUSED_CODE:         with filename.open("w") as fp:
# REMOVED_UNUSED_CODE:             dump_json_to_file(fp, data)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     logger.debug(f'done json to "{filename}"')


# REMOVED_UNUSED_CODE: def json_load(datafile: TextIO) -> Any:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     load data with rapidjson
# REMOVED_UNUSED_CODE:     Use this to have a consistent experience,
# REMOVED_UNUSED_CODE:     set number_mode to "NM_NATIVE" for greatest speed
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     return rapidjson.load(datafile, number_mode=rapidjson.NM_NATIVE)


# REMOVED_UNUSED_CODE: def file_load_json(file: Path):
# REMOVED_UNUSED_CODE:     if file.suffix != ".gz":
# REMOVED_UNUSED_CODE:         gzipfile = file.with_suffix(file.suffix + ".gz")
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         gzipfile = file
# REMOVED_UNUSED_CODE:     # Try gzip file first, otherwise regular json file.
# REMOVED_UNUSED_CODE:     if gzipfile.is_file():
# REMOVED_UNUSED_CODE:         logger.debug(f"Loading historical data from file {gzipfile}")
# REMOVED_UNUSED_CODE:         with gzip.open(gzipfile, "rt", encoding="utf-8") as datafile:
# REMOVED_UNUSED_CODE:             pairdata = json_load(datafile)
# REMOVED_UNUSED_CODE:     elif file.is_file():
# REMOVED_UNUSED_CODE:         logger.debug(f"Loading historical data from file {file}")
# REMOVED_UNUSED_CODE:         with file.open() as datafile:
# REMOVED_UNUSED_CODE:             pairdata = json_load(datafile)
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE:     return pairdata


# REMOVED_UNUSED_CODE: def is_file_in_dir(file: Path, directory: Path) -> bool:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Helper function to check if file is in directory.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     return file.is_file() and file.parent.samefile(directory)


# REMOVED_UNUSED_CODE: def pair_to_filename(pair: str) -> str:
# REMOVED_UNUSED_CODE:     for ch in ["/", " ", ".", "@", "$", "+", ":"]:
# REMOVED_UNUSED_CODE:         pair = pair.replace(ch, "_")
# REMOVED_UNUSED_CODE:     return pair


def deep_merge_dicts(source, destination, allow_null_overrides: bool = True):
    """
    Values from Source override destination, destination is returned (and modified!!)
    Sample:
    >>> a = { 'first' : { 'rows' : { 'pass' : 'dog', 'number' : '1' } } }
    >>> b = { 'first' : { 'rows' : { 'fail' : 'cat', 'number' : '5' } } }
    >>> merge(b, a) == { 'first' : { 'rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
    True
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            deep_merge_dicts(value, node, allow_null_overrides)
        elif value is not None or allow_null_overrides:
            destination[key] = value

    return destination


# REMOVED_UNUSED_CODE: def round_dict(d, n):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Rounds float values in the dict to n digits after the decimal point.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     return {k: (round(v, n) if isinstance(v, float) else v) for k, v in d.items()}


# REMOVED_UNUSED_CODE: DictMap = dict[str, Any] | Mapping[str, Any]


# REMOVED_UNUSED_CODE: def safe_value_fallback(obj: DictMap, key1: str, key2: str | None = None, default_value=None):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Search a value in obj, return this if it's not None.
# REMOVED_UNUSED_CODE:     Then search key2 in obj - return that if it's not none - then use default_value.
# REMOVED_UNUSED_CODE:     Else falls back to None.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if key1 in obj and obj[key1] is not None:
# REMOVED_UNUSED_CODE:         return obj[key1]
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         if key2 and key2 in obj and obj[key2] is not None:
# REMOVED_UNUSED_CODE:             return obj[key2]
# REMOVED_UNUSED_CODE:     return default_value


# REMOVED_UNUSED_CODE: def safe_value_fallback2(dict1: DictMap, dict2: DictMap, key1: str, key2: str, default_value=None):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Search a value in dict1, return this if it's not None.
# REMOVED_UNUSED_CODE:     Fall back to dict2 - return key2 from dict2 if it's not None.
# REMOVED_UNUSED_CODE:     Else falls back to None.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if key1 in dict1 and dict1[key1] is not None:
# REMOVED_UNUSED_CODE:         return dict1[key1]
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         if key2 in dict2 and dict2[key2] is not None:
# REMOVED_UNUSED_CODE:             return dict2[key2]
# REMOVED_UNUSED_CODE:     return default_value


def plural(num: float, singular: str, plural: str | None = None) -> str:
    return singular if (num == 1 or num == -1) else plural or singular + "s"


# REMOVED_UNUSED_CODE: def chunks(lst: list[Any], n: int) -> Iterator[list[Any]]:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Split lst into chunks of the size n.
# REMOVED_UNUSED_CODE:     :param lst: list to split into chunks
# REMOVED_UNUSED_CODE:     :param n: number of max elements per chunk
# REMOVED_UNUSED_CODE:     :return: None
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     for chunk in range(0, len(lst), n):
# REMOVED_UNUSED_CODE:         yield (lst[chunk : chunk + n])


# REMOVED_UNUSED_CODE: def parse_db_uri_for_logging(uri: str):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Helper method to parse the DB URI and return the same DB URI with the password censored
# REMOVED_UNUSED_CODE:     if it contains it. Otherwise, return the DB URI unchanged
# REMOVED_UNUSED_CODE:     :param uri: DB URI to parse for logging
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     parsed_db_uri = urlparse(uri)
# REMOVED_UNUSED_CODE:     if not parsed_db_uri.netloc:  # No need for censoring as no password was provided
# REMOVED_UNUSED_CODE:         return uri
# REMOVED_UNUSED_CODE:     pwd = parsed_db_uri.netloc.split(":")[1].split("@")[0]
# REMOVED_UNUSED_CODE:     return parsed_db_uri.geturl().replace(f":{pwd}@", ":*****@")


# REMOVED_UNUSED_CODE: def dataframe_to_json(dataframe: pd.DataFrame) -> str:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Serialize a DataFrame for transmission over the wire using JSON
# REMOVED_UNUSED_CODE:     :param dataframe: A pandas DataFrame
# REMOVED_UNUSED_CODE:     :returns: A JSON string of the pandas DataFrame
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     return dataframe.to_json(orient="split")


# REMOVED_UNUSED_CODE: def json_to_dataframe(data: str) -> pd.DataFrame:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Deserialize JSON into a DataFrame
# REMOVED_UNUSED_CODE:     :param data: A JSON string
# REMOVED_UNUSED_CODE:     :returns: A pandas DataFrame from the JSON string
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     dataframe = pd.read_json(StringIO(data), orient="split")
# REMOVED_UNUSED_CODE:     if "date" in dataframe.columns:
# REMOVED_UNUSED_CODE:         dataframe["date"] = pd.to_datetime(dataframe["date"], unit="ms", utc=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return dataframe


# REMOVED_UNUSED_CODE: def remove_entry_exit_signals(dataframe: pd.DataFrame):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Remove Entry and Exit signals from a DataFrame
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     :param dataframe: The DataFrame to remove signals from
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     dataframe[SignalType.ENTER_LONG.value] = 0
# REMOVED_UNUSED_CODE:     dataframe[SignalType.EXIT_LONG.value] = 0
# REMOVED_UNUSED_CODE:     dataframe[SignalType.ENTER_SHORT.value] = 0
# REMOVED_UNUSED_CODE:     dataframe[SignalType.EXIT_SHORT.value] = 0
# REMOVED_UNUSED_CODE:     dataframe[SignalTagType.ENTER_TAG.value] = None
# REMOVED_UNUSED_CODE:     dataframe[SignalTagType.EXIT_TAG.value] = None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return dataframe


# REMOVED_UNUSED_CODE: def append_candles_to_dataframe(left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Append the `right` dataframe to the `left` dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     :param left: The full dataframe you want appended to
# REMOVED_UNUSED_CODE:     :param right: The new dataframe containing the data you want appended
# REMOVED_UNUSED_CODE:     :returns: The dataframe with the right data in it
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if left.iloc[-1]["date"] != right.iloc[-1]["date"]:
# REMOVED_UNUSED_CODE:         left = pd.concat([left, right])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Only keep the last 1500 candles in memory
# REMOVED_UNUSED_CODE:     left = left[-1500:] if len(left) > 1500 else left
# REMOVED_UNUSED_CODE:     left.reset_index(drop=True, inplace=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return left
