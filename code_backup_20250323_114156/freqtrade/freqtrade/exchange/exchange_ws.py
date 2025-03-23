# REMOVED_UNUSED_CODE: import asyncio
import logging
# REMOVED_UNUSED_CODE: import time
# REMOVED_UNUSED_CODE: from copy import deepcopy
# REMOVED_UNUSED_CODE: from functools import partial
# REMOVED_UNUSED_CODE: from threading import Thread

# REMOVED_UNUSED_CODE: import ccxt

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.constants import Config, PairWithTimeframe
# REMOVED_UNUSED_CODE: from freqtrade.enums.candletype import CandleType
# REMOVED_UNUSED_CODE: from freqtrade.exceptions import TemporaryError
# REMOVED_UNUSED_CODE: from freqtrade.exchange.common import retrier
# REMOVED_UNUSED_CODE: from freqtrade.exchange.exchange import timeframe_to_seconds
# REMOVED_UNUSED_CODE: from freqtrade.exchange.exchange_types import OHLCVResponse
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.util import dt_ts, format_ms_time, format_ms_time_det


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class ExchangeWS:
# REMOVED_UNUSED_CODE:     def __init__(self, config: Config, ccxt_object: ccxt.Exchange) -> None:
# REMOVED_UNUSED_CODE:         self.config = config
# REMOVED_UNUSED_CODE:         self._ccxt_object = ccxt_object
# REMOVED_UNUSED_CODE:         self._background_tasks: set[asyncio.Task] = set()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._klines_watching: set[PairWithTimeframe] = set()
# REMOVED_UNUSED_CODE:         self._klines_scheduled: set[PairWithTimeframe] = set()
# REMOVED_UNUSED_CODE:         self.klines_last_refresh: dict[PairWithTimeframe, float] = {}
# REMOVED_UNUSED_CODE:         self.klines_last_request: dict[PairWithTimeframe, float] = {}
# REMOVED_UNUSED_CODE:         self._thread = Thread(name="ccxt_ws", target=self._start_forever)
# REMOVED_UNUSED_CODE:         self._thread.start()
# REMOVED_UNUSED_CODE:         self.__cleanup_called = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _start_forever(self) -> None:
# REMOVED_UNUSED_CODE:         self._loop = asyncio.new_event_loop()
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             self._loop.run_forever()
# REMOVED_UNUSED_CODE:         finally:
# REMOVED_UNUSED_CODE:             if self._loop.is_running():
# REMOVED_UNUSED_CODE:                 self._loop.stop()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def cleanup(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.debug("Cleanup called - stopping")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._klines_watching.clear()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for task in self._background_tasks:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             task.cancel()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if hasattr(self, "_loop") and not self._loop.is_closed():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.reset_connections()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._loop.call_soon_threadsafe(self._loop.stop)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             time.sleep(0.1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not self._loop.is_closed():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._loop.close()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._thread.join()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.debug("Stopped")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def reset_connections(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Reset all connections - avoids "connection-reset" errors that happen after ~9 days
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if hasattr(self, "_loop") and not self._loop.is_closed():
# REMOVED_UNUSED_CODE:             logger.info("Resetting WS connections.")
# REMOVED_UNUSED_CODE:             asyncio.run_coroutine_threadsafe(self._cleanup_async(), loop=self._loop)
# REMOVED_UNUSED_CODE:             while not self.__cleanup_called:
# REMOVED_UNUSED_CODE:                 time.sleep(0.1)
# REMOVED_UNUSED_CODE:         self.__cleanup_called = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _cleanup_async(self) -> None:
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             await self._ccxt_object.close()
# REMOVED_UNUSED_CODE:             # Clear the cache.
# REMOVED_UNUSED_CODE:             # Not doing this will cause problems on startup with dynamic pairlists
# REMOVED_UNUSED_CODE:             self._ccxt_object.ohlcvs.clear()
# REMOVED_UNUSED_CODE:         except Exception:
# REMOVED_UNUSED_CODE:             logger.exception("Exception in _cleanup_async")
# REMOVED_UNUSED_CODE:         finally:
# REMOVED_UNUSED_CODE:             self.__cleanup_called = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _pop_history(self, paircomb: PairWithTimeframe) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Remove history for a pair/timeframe combination from ccxt cache
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self._ccxt_object.ohlcvs.get(paircomb[0], {}).pop(paircomb[1], None)
# REMOVED_UNUSED_CODE:         self.klines_last_refresh.pop(paircomb, None)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @retrier(retries=3)
# REMOVED_UNUSED_CODE:     def ohlcvs(self, pair: str, timeframe: str) -> list[list]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Returns a copy of the klines for a pair/timeframe combination
# REMOVED_UNUSED_CODE:         Note: this will only contain the data received from the websocket
# REMOVED_UNUSED_CODE:             so the data will build up over time.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             return deepcopy(self._ccxt_object.ohlcvs.get(pair, {}).get(timeframe, []))
# REMOVED_UNUSED_CODE:         except RuntimeError as e:
# REMOVED_UNUSED_CODE:             # Capture runtime errors and retry
# REMOVED_UNUSED_CODE:             # TemporaryError does not cause backoff - so we're essentially retrying immediately
# REMOVED_UNUSED_CODE:             raise TemporaryError(f"Error deepcopying: {e}") from e
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def cleanup_expired(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Remove pairs from watchlist if they've not been requested within
# REMOVED_UNUSED_CODE:         the last timeframe (+ offset)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         changed = False
# REMOVED_UNUSED_CODE:         for p in list(self._klines_watching):
# REMOVED_UNUSED_CODE:             _, timeframe, _ = p
# REMOVED_UNUSED_CODE:             timeframe_s = timeframe_to_seconds(timeframe)
# REMOVED_UNUSED_CODE:             last_refresh = self.klines_last_request.get(p, 0)
# REMOVED_UNUSED_CODE:             if last_refresh > 0 and (dt_ts() - last_refresh) > ((timeframe_s + 20) * 1000):
# REMOVED_UNUSED_CODE:                 logger.info(f"Removing {p} from websocket watchlist.")
# REMOVED_UNUSED_CODE:                 self._klines_watching.discard(p)
# REMOVED_UNUSED_CODE:                 # Pop history to avoid getting stale data
# REMOVED_UNUSED_CODE:                 self._pop_history(p)
# REMOVED_UNUSED_CODE:                 changed = True
# REMOVED_UNUSED_CODE:         if changed:
# REMOVED_UNUSED_CODE:             logger.info(f"Removal done: new watch list ({len(self._klines_watching)})")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _schedule_while_true(self) -> None:
# REMOVED_UNUSED_CODE:         # For the ones we should be watching
# REMOVED_UNUSED_CODE:         for p in self._klines_watching:
# REMOVED_UNUSED_CODE:             # Check if they're already scheduled
# REMOVED_UNUSED_CODE:             if p not in self._klines_scheduled:
# REMOVED_UNUSED_CODE:                 self._klines_scheduled.add(p)
# REMOVED_UNUSED_CODE:                 pair, timeframe, candle_type = p
# REMOVED_UNUSED_CODE:                 task = asyncio.create_task(
# REMOVED_UNUSED_CODE:                     self._continuously_async_watch_ohlcv(pair, timeframe, candle_type)
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 self._background_tasks.add(task)
# REMOVED_UNUSED_CODE:                 task.add_done_callback(
# REMOVED_UNUSED_CODE:                     partial(
# REMOVED_UNUSED_CODE:                         self._continuous_stopped,
# REMOVED_UNUSED_CODE:                         pair=pair,
# REMOVED_UNUSED_CODE:                         timeframe=timeframe,
# REMOVED_UNUSED_CODE:                         candle_type=candle_type,
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _unwatch_ohlcv(self, pair: str, timeframe: str, candle_type: CandleType) -> None:
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             await self._ccxt_object.un_watch_ohlcv_for_symbols([[pair, timeframe]])
# REMOVED_UNUSED_CODE:         except ccxt.NotSupported as e:
# REMOVED_UNUSED_CODE:             logger.debug("un_watch_ohlcv_for_symbols not supported: %s", e)
# REMOVED_UNUSED_CODE:             pass
# REMOVED_UNUSED_CODE:         except Exception:
# REMOVED_UNUSED_CODE:             logger.exception("Exception in _unwatch_ohlcv")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _continuous_stopped(
# REMOVED_UNUSED_CODE:         self, task: asyncio.Task, pair: str, timeframe: str, candle_type: CandleType
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         self._background_tasks.discard(task)
# REMOVED_UNUSED_CODE:         result = "done"
# REMOVED_UNUSED_CODE:         if task.cancelled():
# REMOVED_UNUSED_CODE:             result = "cancelled"
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             if (result1 := task.result()) is not None:
# REMOVED_UNUSED_CODE:                 result = str(result1)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.info(f"{pair}, {timeframe}, {candle_type} - Task finished - {result}")
# REMOVED_UNUSED_CODE:         asyncio.run_coroutine_threadsafe(
# REMOVED_UNUSED_CODE:             self._unwatch_ohlcv(pair, timeframe, candle_type), loop=self._loop
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._klines_scheduled.discard((pair, timeframe, candle_type))
# REMOVED_UNUSED_CODE:         self._pop_history((pair, timeframe, candle_type))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _continuously_async_watch_ohlcv(
# REMOVED_UNUSED_CODE:         self, pair: str, timeframe: str, candle_type: CandleType
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             while (pair, timeframe, candle_type) in self._klines_watching:
# REMOVED_UNUSED_CODE:                 start = dt_ts()
# REMOVED_UNUSED_CODE:                 data = await self._ccxt_object.watch_ohlcv(pair, timeframe)
# REMOVED_UNUSED_CODE:                 self.klines_last_refresh[(pair, timeframe, candle_type)] = dt_ts()
# REMOVED_UNUSED_CODE:                 logger.debug(
# REMOVED_UNUSED_CODE:                     f"watch done {pair}, {timeframe}, data {len(data)} "
# REMOVED_UNUSED_CODE:                     f"in {(dt_ts() - start) / 1000:.3f}s"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:         except ccxt.ExchangeClosedByUser:
# REMOVED_UNUSED_CODE:             logger.debug("Exchange connection closed by user")
# REMOVED_UNUSED_CODE:         except ccxt.BaseError:
# REMOVED_UNUSED_CODE:             logger.exception(f"Exception in continuously_async_watch_ohlcv for {pair}, {timeframe}")
# REMOVED_UNUSED_CODE:         finally:
# REMOVED_UNUSED_CODE:             self._klines_watching.discard((pair, timeframe, candle_type))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def schedule_ohlcv(self, pair: str, timeframe: str, candle_type: CandleType) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Schedule a pair/timeframe combination to be watched
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._klines_watching.add((pair, timeframe, candle_type))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.klines_last_request[(pair, timeframe, candle_type)] = dt_ts()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # asyncio.run_coroutine_threadsafe(self.schedule_schedule(), loop=self._loop)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         asyncio.run_coroutine_threadsafe(self._schedule_while_true(), loop=self._loop)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.cleanup_expired()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     async def get_ohlcv(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         timeframe: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         candle_type: CandleType,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         candle_ts: int,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> OHLCVResponse:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Returns cached klines from ccxt's "watch" cache.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param candle_ts: timestamp of the end-time of the candle we expect.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Deepcopy the response - as it might be modified in the background as new messages arrive
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         candles = self.ohlcvs(pair, timeframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         refresh_date = self.klines_last_refresh[(pair, timeframe, candle_type)]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         received_ts = candles[-1][0] if candles else 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         drop_hint = received_ts >= candle_ts
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if received_ts > refresh_date:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"{pair}, {timeframe} - Candle date > last refresh "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"({format_ms_time(received_ts)} > {format_ms_time_det(refresh_date)}). "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "This usually suggests a problem with time synchronization."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.debug(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"watch result for {pair}, {timeframe} with length {len(candles)}, "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"r_ts={format_ms_time(received_ts)}, "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"lref={format_ms_time_det(refresh_date)}, "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"candle_ts={format_ms_time(candle_ts)}, {drop_hint=}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return pair, timeframe, candle_type, candles, drop_hint
