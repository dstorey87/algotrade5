"""
Fetch daily-archived OHLCV data from https://data.binance.vision/
"""

import asyncio
import logging
import zipfile
from datetime import date, timedelta
from io import BytesIO
from typing import Any

import aiohttp
import pandas as pd
from pandas import DataFrame

from freqtrade.enums import CandleType
from freqtrade.misc import chunks
from freqtrade.util.datetime_helpers import dt_from_ts, dt_now


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


def concat_safe(dfs) -> DataFrame:
    if all(df is None for df in dfs):
        return DataFrame()
    else:
        return pd.concat(dfs)


async def _download_archive_ohlcv(
    symbol: str,
    pair: str,
    timeframe: str,
    candle_type: CandleType,
    start: date,
    end: date,
    stop_on_404: bool,
) -> DataFrame:
    # daily dataframes, `None` indicates missing data in that day (when `stop_on_404` is False)
    dfs: list[DataFrame | None] = []
    # the current day being processing, starting at 1.
    current_day = 0

    connector = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
        # the HTTP connections has been throttled by TCPConnector
        for dates in chunks(list(date_range(start, end)), 1000):
            tasks = [
                asyncio.create_task(get_daily_ohlcv(symbol, timeframe, candle_type, date, session))
                for date in dates
            ]
            for task in tasks:
                current_day += 1
                try:
                    df = await task
                except Http404 as e:
                    if stop_on_404:
                        logger.debug(f"Failed to download {e.url} due to 404.")

                        # A 404 error on the first day indicates missing data
                        # on https://data.binance.vision, we provide the warning and the advice.
                        # https://github.com/freqtrade/freqtrade/blob/acc53065e5fa7ab5197073276306dc9dc3adbfa3/tests/exchange_online/test_binance_compare_ohlcv.py#L7
                        if current_day == 1:
                            logger.warning(
                                f"Fast download is unavailable due to missing data: "
                                f"{e.url}. Falling back to the slower REST API, "
                                "which may take more time."
                            )
                            if pair in ["BTC/USDT:USDT", "ETH/USDT:USDT", "BCH/USDT:USDT"]:
                                logger.warning(
                                    f"To avoid the delay, you can first download {pair} using "
                                    "`--timerange <start date>-20200101`, and then download the "
                                    "remaining data with `--timerange 20200101-<end date>`."
                                )
                        else:
                            logger.warning(
                                f"Binance fast download for {pair} stopped at {e.date} due to "
                                f"missing data: {e.url}, falling back to rest API for the "
                                "remaining data, this can take more time."
                            )
                        await cancel_and_await_tasks(tasks[tasks.index(task) + 1 :])
                        return concat_safe(dfs)
                    else:
                        dfs.append(None)
                except BaseException as e:
                    logger.warning(f"An exception raised: : {e}")
                    # Directly return the existing data, do not allow the gap within the data
                    await cancel_and_await_tasks(tasks[tasks.index(task) + 1 :])
                    return concat_safe(dfs)
                else:
                    dfs.append(df)
    return concat_safe(dfs)


async def cancel_and_await_tasks(unawaited_tasks):
    """Cancel and await the tasks"""
    logger.debug("Try to cancel uncompleted download tasks.")
    for task in unawaited_tasks:
        task.cancel()
    await asyncio.gather(*unawaited_tasks, return_exceptions=True)
    logger.debug("All download tasks were awaited.")


def date_range(start: date, end: date):
    date = start
    while date <= end:
        yield date
        date += timedelta(days=1)


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


async def get_daily_ohlcv(
    symbol: str,
    timeframe: str,
    candle_type: CandleType,
    date: date,
    session: aiohttp.ClientSession,
    retry_count: int = 3,
    retry_delay: float = 0.0,
) -> DataFrame:
    """
    Get daily OHLCV from https://data.binance.vision
    See https://github.com/binance/binance-public-data

    :symbol: binance symbol name, e.g. BTCUSDT
    :timeframe: e.g. 1m, 1h
    :candle_type: SPOT or FUTURES
    :date: the returned DataFrame will cover the entire day of `date` in UTC
    :session: an aiohttp.ClientSession instance
    :retry_count: times to retry before returning the exceptions
    :retry_delay: the time to wait before every retry
    :return: A dataframe containing columns date,open,high,low,close,volume
    """

    url = binance_vision_ohlcv_zip_url(symbol, timeframe, candle_type, date)

    logger.debug(f"download data from binance: {url}")

    retry = 0
    while True:
        if retry > 0:
            sleep_secs = retry * retry_delay
            logger.debug(
                f"[{retry}/{retry_count}] retry to download {url} after {sleep_secs} seconds"
            )
            await asyncio.sleep(sleep_secs)
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    content = await resp.read()
                    logger.debug(f"Successfully downloaded {url}")
                    with zipfile.ZipFile(BytesIO(content)) as zipf:
                        with zipf.open(zipf.namelist()[0]) as csvf:
                            # https://github.com/binance/binance-public-data/issues/283
                            first_byte = csvf.read(1)[0]
                            if chr(first_byte).isdigit():
                                header = None
                            else:
                                header = 0
                            csvf.seek(0)

                            df = pd.read_csv(
                                csvf,
                                usecols=[0, 1, 2, 3, 4, 5],
                                names=["date", "open", "high", "low", "close", "volume"],
                                header=header,
                            )
                            df["date"] = pd.to_datetime(df["date"], unit="ms", utc=True)
                            return df
                elif resp.status == 404:
                    logger.debug(f"Failed to download {url}")
                    raise Http404(f"404: {url}", date, url)
                else:
                    raise BadHttpStatus(f"{resp.status} - {resp.reason}")
        except Exception as e:
            retry += 1
            if isinstance(e, Http404) or retry > retry_count:
                logger.debug(f"Failed to get data from {url}: {e}")
                raise
