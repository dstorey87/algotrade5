"""
Fetch daily-archived OHLCV data from https://data.binance.vision/
"""

import asyncio
import logging
import zipfile
from datetime import date, timedelta
from io import BytesIO
# REMOVED_UNUSED_CODE: from typing import Any

import aiohttp
import pandas as pd
from pandas import DataFrame

from freqtrade.enums import CandleType
# REMOVED_UNUSED_CODE: from freqtrade.misc import chunks
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.util.datetime_helpers import dt_from_ts, dt_now


logger = logging.getLogger(__name__)


class Http404(Exception):
    def __init__(self, msg, date, url):
        super().__init__(msg)
        self.date = date
        self.url = url


class BadHttpStatus(Exception):
    """Not 200/404"""

    pass


# REMOVED_UNUSED_CODE: async def download_archive_ohlcv(
# REMOVED_UNUSED_CODE:     candle_type: CandleType,
# REMOVED_UNUSED_CODE:     pair: str,
# REMOVED_UNUSED_CODE:     timeframe: str,
# REMOVED_UNUSED_CODE:     *,
# REMOVED_UNUSED_CODE:     since_ms: int,
# REMOVED_UNUSED_CODE:     until_ms: int | None,
# REMOVED_UNUSED_CODE:     markets: dict[str, Any],
# REMOVED_UNUSED_CODE:     stop_on_404: bool = True,
# REMOVED_UNUSED_CODE: ) -> DataFrame:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Fetch OHLCV data from https://data.binance.vision
# REMOVED_UNUSED_CODE:     The function makes its best effort to download data within the time range
# REMOVED_UNUSED_CODE:     [`since_ms`, `until_ms`] -- including `since_ms`, but excluding `until_ms`.
# REMOVED_UNUSED_CODE:     If `stop_one_404` is True, this returned DataFrame is guaranteed to start from `since_ms`
# REMOVED_UNUSED_CODE:     with no gaps in the data.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     :candle_type: Currently only spot and futures are supported
# REMOVED_UNUSED_CODE:     :pair: symbol name in CCXT convention
# REMOVED_UNUSED_CODE:     :since_ms: the start timestamp of data, including itself
# REMOVED_UNUSED_CODE:     :until_ms: the end timestamp of data, excluding itself
# REMOVED_UNUSED_CODE:     :param until_ms: `None` indicates the timestamp of the latest available data
# REMOVED_UNUSED_CODE:     :markets: the CCXT markets dict, when it's None, the function will load the markets data
# REMOVED_UNUSED_CODE:         from a new `ccxt.binance` instance
# REMOVED_UNUSED_CODE:     :param stop_on_404: Stop to download the following data when a 404 returned
# REMOVED_UNUSED_CODE:     :return: the date range is between [since_ms, until_ms), return an empty DataFrame if no data
# REMOVED_UNUSED_CODE:         available in the time range
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         symbol = markets[pair]["id"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         start = dt_from_ts(since_ms)
# REMOVED_UNUSED_CODE:         end = dt_from_ts(until_ms) if until_ms else dt_now()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # We use two days ago as the last available day because the daily archives are daily
# REMOVED_UNUSED_CODE:         # uploaded and have several hours delay
# REMOVED_UNUSED_CODE:         last_available_date = dt_now() - timedelta(days=2)
# REMOVED_UNUSED_CODE:         end = min(end, last_available_date)
# REMOVED_UNUSED_CODE:         if start >= end:
# REMOVED_UNUSED_CODE:             return DataFrame()
# REMOVED_UNUSED_CODE:         df = await _download_archive_ohlcv(
# REMOVED_UNUSED_CODE:             symbol, pair, timeframe, candle_type, start, end, stop_on_404
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         logger.debug(
# REMOVED_UNUSED_CODE:             f"Downloaded data for {pair} from https://data.binance.vision with length {len(df)}."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:     except Exception as e:
# REMOVED_UNUSED_CODE:         logger.warning(
# REMOVED_UNUSED_CODE:             "An exception occurred during fast download from Binance, falling back to "
# REMOVED_UNUSED_CODE:             "the slower REST API, this can take more time.",
# REMOVED_UNUSED_CODE:             exc_info=e,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         df = DataFrame()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if not df.empty:
# REMOVED_UNUSED_CODE:         # only return the data within the requested time range
# REMOVED_UNUSED_CODE:         return df.loc[(df["date"] >= start) & (df["date"] < end)]
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         return df


# REMOVED_UNUSED_CODE: def concat_safe(dfs) -> DataFrame:
# REMOVED_UNUSED_CODE:     if all(df is None for df in dfs):
# REMOVED_UNUSED_CODE:         return DataFrame()
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         return pd.concat(dfs)


# REMOVED_UNUSED_CODE: async def _download_archive_ohlcv(
# REMOVED_UNUSED_CODE:     symbol: str,
# REMOVED_UNUSED_CODE:     pair: str,
# REMOVED_UNUSED_CODE:     timeframe: str,
# REMOVED_UNUSED_CODE:     candle_type: CandleType,
# REMOVED_UNUSED_CODE:     start: date,
# REMOVED_UNUSED_CODE:     end: date,
# REMOVED_UNUSED_CODE:     stop_on_404: bool,
# REMOVED_UNUSED_CODE: ) -> DataFrame:
# REMOVED_UNUSED_CODE:     # daily dataframes, `None` indicates missing data in that day (when `stop_on_404` is False)
# REMOVED_UNUSED_CODE:     dfs: list[DataFrame | None] = []
# REMOVED_UNUSED_CODE:     # the current day being processing, starting at 1.
# REMOVED_UNUSED_CODE:     current_day = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     connector = aiohttp.TCPConnector(limit=100)
# REMOVED_UNUSED_CODE:     async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
# REMOVED_UNUSED_CODE:         # the HTTP connections has been throttled by TCPConnector
# REMOVED_UNUSED_CODE:         for dates in chunks(list(date_range(start, end)), 1000):
# REMOVED_UNUSED_CODE:             tasks = [
# REMOVED_UNUSED_CODE:                 asyncio.create_task(get_daily_ohlcv(symbol, timeframe, candle_type, date, session))
# REMOVED_UNUSED_CODE:                 for date in dates
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE:             for task in tasks:
# REMOVED_UNUSED_CODE:                 current_day += 1
# REMOVED_UNUSED_CODE:                 try:
# REMOVED_UNUSED_CODE:                     df = await task
# REMOVED_UNUSED_CODE:                 except Http404 as e:
# REMOVED_UNUSED_CODE:                     if stop_on_404:
# REMOVED_UNUSED_CODE:                         logger.debug(f"Failed to download {e.url} due to 404.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                         # A 404 error on the first day indicates missing data
# REMOVED_UNUSED_CODE:                         # on https://data.binance.vision, we provide the warning and the advice.
# REMOVED_UNUSED_CODE:                         # https://github.com/freqtrade/freqtrade/blob/acc53065e5fa7ab5197073276306dc9dc3adbfa3/tests/exchange_online/test_binance_compare_ohlcv.py#L7
# REMOVED_UNUSED_CODE:                         if current_day == 1:
# REMOVED_UNUSED_CODE:                             logger.warning(
# REMOVED_UNUSED_CODE:                                 f"Fast download is unavailable due to missing data: "
# REMOVED_UNUSED_CODE:                                 f"{e.url}. Falling back to the slower REST API, "
# REMOVED_UNUSED_CODE:                                 "which may take more time."
# REMOVED_UNUSED_CODE:                             )
# REMOVED_UNUSED_CODE:                             if pair in ["BTC/USDT:USDT", "ETH/USDT:USDT", "BCH/USDT:USDT"]:
# REMOVED_UNUSED_CODE:                                 logger.warning(
# REMOVED_UNUSED_CODE:                                     f"To avoid the delay, you can first download {pair} using "
# REMOVED_UNUSED_CODE:                                     "`--timerange <start date>-20200101`, and then download the "
# REMOVED_UNUSED_CODE:                                     "remaining data with `--timerange 20200101-<end date>`."
# REMOVED_UNUSED_CODE:                                 )
# REMOVED_UNUSED_CODE:                         else:
# REMOVED_UNUSED_CODE:                             logger.warning(
# REMOVED_UNUSED_CODE:                                 f"Binance fast download for {pair} stopped at {e.date} due to "
# REMOVED_UNUSED_CODE:                                 f"missing data: {e.url}, falling back to rest API for the "
# REMOVED_UNUSED_CODE:                                 "remaining data, this can take more time."
# REMOVED_UNUSED_CODE:                             )
# REMOVED_UNUSED_CODE:                         await cancel_and_await_tasks(tasks[tasks.index(task) + 1 :])
# REMOVED_UNUSED_CODE:                         return concat_safe(dfs)
# REMOVED_UNUSED_CODE:                     else:
# REMOVED_UNUSED_CODE:                         dfs.append(None)
# REMOVED_UNUSED_CODE:                 except BaseException as e:
# REMOVED_UNUSED_CODE:                     logger.warning(f"An exception raised: : {e}")
# REMOVED_UNUSED_CODE:                     # Directly return the existing data, do not allow the gap within the data
# REMOVED_UNUSED_CODE:                     await cancel_and_await_tasks(tasks[tasks.index(task) + 1 :])
# REMOVED_UNUSED_CODE:                     return concat_safe(dfs)
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     dfs.append(df)
# REMOVED_UNUSED_CODE:     return concat_safe(dfs)


# REMOVED_UNUSED_CODE: async def cancel_and_await_tasks(unawaited_tasks):
# REMOVED_UNUSED_CODE:     """Cancel and await the tasks"""
# REMOVED_UNUSED_CODE:     logger.debug("Try to cancel uncompleted download tasks.")
# REMOVED_UNUSED_CODE:     for task in unawaited_tasks:
# REMOVED_UNUSED_CODE:         task.cancel()
# REMOVED_UNUSED_CODE:     await asyncio.gather(*unawaited_tasks, return_exceptions=True)
# REMOVED_UNUSED_CODE:     logger.debug("All download tasks were awaited.")


# REMOVED_UNUSED_CODE: def date_range(start: date, end: date):
# REMOVED_UNUSED_CODE:     date = start
# REMOVED_UNUSED_CODE:     while date <= end:
# REMOVED_UNUSED_CODE:         yield date
# REMOVED_UNUSED_CODE:         date += timedelta(days=1)


def binance_vision_zip_name(symbol: str, timeframe: str, date: date) -> str:
    return f"{symbol}-{timeframe}-{date.strftime('%Y-%m-%d')}.zip"


def candle_type_to_url_segment(candle_type: CandleType) -> str:
    if candle_type == CandleType.SPOT:
        return "spot"
    elif candle_type == CandleType.FUTURES:
        return "futures/um"
    else:
        raise ValueError(f"Unsupported CandleType: {candle_type}")


def binance_vision_ohlcv_zip_url(
    symbol: str, timeframe: str, candle_type: CandleType, date: date
) -> str:
    """
    example urls:
    https://data.binance.vision/data/spot/daily/klines/BTCUSDT/1s/BTCUSDT-1s-2023-10-27.zip
    https://data.binance.vision/data/futures/um/daily/klines/BTCUSDT/1h/BTCUSDT-1h-2023-10-27.zip
    """
    asset_type_url_segment = candle_type_to_url_segment(candle_type)
    url = (
        f"https://data.binance.vision/data/{asset_type_url_segment}/daily/klines/{symbol}"
        f"/{timeframe}/{binance_vision_zip_name(symbol, timeframe, date)}"
    )
    return url


# REMOVED_UNUSED_CODE: async def get_daily_ohlcv(
# REMOVED_UNUSED_CODE:     symbol: str,
# REMOVED_UNUSED_CODE:     timeframe: str,
# REMOVED_UNUSED_CODE:     candle_type: CandleType,
# REMOVED_UNUSED_CODE:     date: date,
# REMOVED_UNUSED_CODE:     session: aiohttp.ClientSession,
# REMOVED_UNUSED_CODE:     retry_count: int = 3,
# REMOVED_UNUSED_CODE:     retry_delay: float = 0.0,
# REMOVED_UNUSED_CODE: ) -> DataFrame:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Get daily OHLCV from https://data.binance.vision
# REMOVED_UNUSED_CODE:     See https://github.com/binance/binance-public-data
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     :symbol: binance symbol name, e.g. BTCUSDT
# REMOVED_UNUSED_CODE:     :timeframe: e.g. 1m, 1h
# REMOVED_UNUSED_CODE:     :candle_type: SPOT or FUTURES
# REMOVED_UNUSED_CODE:     :date: the returned DataFrame will cover the entire day of `date` in UTC
# REMOVED_UNUSED_CODE:     :session: an aiohttp.ClientSession instance
# REMOVED_UNUSED_CODE:     :retry_count: times to retry before returning the exceptions
# REMOVED_UNUSED_CODE:     :retry_delay: the time to wait before every retry
# REMOVED_UNUSED_CODE:     :return: A dataframe containing columns date,open,high,low,close,volume
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     url = binance_vision_ohlcv_zip_url(symbol, timeframe, candle_type, date)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     logger.debug(f"download data from binance: {url}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     retry = 0
# REMOVED_UNUSED_CODE:     while True:
# REMOVED_UNUSED_CODE:         if retry > 0:
# REMOVED_UNUSED_CODE:             sleep_secs = retry * retry_delay
# REMOVED_UNUSED_CODE:             logger.debug(
# REMOVED_UNUSED_CODE:                 f"[{retry}/{retry_count}] retry to download {url} after {sleep_secs} seconds"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             await asyncio.sleep(sleep_secs)
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             async with session.get(url) as resp:
# REMOVED_UNUSED_CODE:                 if resp.status == 200:
# REMOVED_UNUSED_CODE:                     content = await resp.read()
# REMOVED_UNUSED_CODE:                     logger.debug(f"Successfully downloaded {url}")
# REMOVED_UNUSED_CODE:                     with zipfile.ZipFile(BytesIO(content)) as zipf:
# REMOVED_UNUSED_CODE:                         with zipf.open(zipf.namelist()[0]) as csvf:
# REMOVED_UNUSED_CODE:                             # https://github.com/binance/binance-public-data/issues/283
# REMOVED_UNUSED_CODE:                             first_byte = csvf.read(1)[0]
# REMOVED_UNUSED_CODE:                             if chr(first_byte).isdigit():
# REMOVED_UNUSED_CODE:                                 header = None
# REMOVED_UNUSED_CODE:                             else:
# REMOVED_UNUSED_CODE:                                 header = 0
# REMOVED_UNUSED_CODE:                             csvf.seek(0)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                             df = pd.read_csv(
# REMOVED_UNUSED_CODE:                                 csvf,
# REMOVED_UNUSED_CODE:                                 usecols=[0, 1, 2, 3, 4, 5],
# REMOVED_UNUSED_CODE:                                 names=["date", "open", "high", "low", "close", "volume"],
# REMOVED_UNUSED_CODE:                                 header=header,
# REMOVED_UNUSED_CODE:                             )
# REMOVED_UNUSED_CODE:                             df["date"] = pd.to_datetime(df["date"], unit="ms", utc=True)
# REMOVED_UNUSED_CODE:                             return df
# REMOVED_UNUSED_CODE:                 elif resp.status == 404:
# REMOVED_UNUSED_CODE:                     logger.debug(f"Failed to download {url}")
# REMOVED_UNUSED_CODE:                     raise Http404(f"404: {url}", date, url)
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     raise BadHttpStatus(f"{resp.status} - {resp.reason}")
# REMOVED_UNUSED_CODE:         except Exception as e:
# REMOVED_UNUSED_CODE:             retry += 1
# REMOVED_UNUSED_CODE:             if isinstance(e, Http404) or retry > retry_count:
# REMOVED_UNUSED_CODE:                 logger.debug(f"Failed to get data from {url}: {e}")
# REMOVED_UNUSED_CODE:                 raise
