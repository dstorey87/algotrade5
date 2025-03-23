"""
Main Freqtrade worker class.
"""

import logging
# REMOVED_UNUSED_CODE: import time
# REMOVED_UNUSED_CODE: import traceback
# REMOVED_UNUSED_CODE: from collections.abc import Callable
# REMOVED_UNUSED_CODE: from os import getpid
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: import sdnotify

# REMOVED_UNUSED_CODE: from freqtrade import __version__
# REMOVED_UNUSED_CODE: from freqtrade.configuration import Configuration
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.constants import PROCESS_THROTTLE_SECS, RETRY_TIMEOUT, Config
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.enums import RPCMessageType, State
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException, TemporaryError
# REMOVED_UNUSED_CODE: from freqtrade.exchange import timeframe_to_next_date
# REMOVED_UNUSED_CODE: from freqtrade.freqtradebot import FreqtradeBot


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Worker:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Freqtradebot worker class
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, args: dict[str, Any], config: Config | None = None) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Init all variables and objects the bot needs to work
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         logger.info(f"Starting worker {__version__}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._args = args
# REMOVED_UNUSED_CODE:         self._config = config
# REMOVED_UNUSED_CODE:         self._init(False)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._heartbeat_msg: float = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Tell systemd that we completed initialization phase
# REMOVED_UNUSED_CODE:         self._notify("READY=1")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _init(self, reconfig: bool) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Also called from the _reconfigure() method (with reconfig=True).
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if reconfig or self._config is None:
# REMOVED_UNUSED_CODE:             # Load configuration
# REMOVED_UNUSED_CODE:             self._config = Configuration(self._args, None).get_config()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Init the instance of the bot
# REMOVED_UNUSED_CODE:         self.freqtrade = FreqtradeBot(self._config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         internals_config = self._config.get("internals", {})
# REMOVED_UNUSED_CODE:         self._throttle_secs = internals_config.get("process_throttle_secs", PROCESS_THROTTLE_SECS)
# REMOVED_UNUSED_CODE:         self._heartbeat_interval = internals_config.get("heartbeat_interval", 60)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._sd_notify = (
# REMOVED_UNUSED_CODE:             sdnotify.SystemdNotifier()
# REMOVED_UNUSED_CODE:             if self._config.get("internals", {}).get("sd_notify", False)
# REMOVED_UNUSED_CODE:             else None
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _notify(self, message: str) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Removes the need to verify in all occurrences if sd_notify is enabled
# REMOVED_UNUSED_CODE:         :param message: Message to send to systemd if it's enabled.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self._sd_notify:
# REMOVED_UNUSED_CODE:             logger.debug(f"sd_notify: {message}")
# REMOVED_UNUSED_CODE:             self._sd_notify.notify(message)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def run(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         state = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         while True:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             state = self._worker(old_state=state)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if state == State.RELOAD_CONFIG:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._reconfigure()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _worker(self, old_state: State | None) -> State:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         The main routine that runs each throttling iteration and handles the states.
# REMOVED_UNUSED_CODE:         :param old_state: the previous service state from the previous call
# REMOVED_UNUSED_CODE:         :return: current service state
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         state = self.freqtrade.state
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Log state transition
# REMOVED_UNUSED_CODE:         if state != old_state:
# REMOVED_UNUSED_CODE:             if old_state != State.RELOAD_CONFIG:
# REMOVED_UNUSED_CODE:                 self.freqtrade.notify_status(f"{state.name.lower()}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             logger.info(
# REMOVED_UNUSED_CODE:                 f"Changing state{f' from {old_state.name}' if old_state else ''} to: {state.name}"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             if state == State.RUNNING:
# REMOVED_UNUSED_CODE:                 self.freqtrade.startup()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if state == State.STOPPED:
# REMOVED_UNUSED_CODE:                 self.freqtrade.check_for_open_trades()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Reset heartbeat timestamp to log the heartbeat message at
# REMOVED_UNUSED_CODE:             # first throttling iteration when the state changes
# REMOVED_UNUSED_CODE:             self._heartbeat_msg = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if state == State.STOPPED:
# REMOVED_UNUSED_CODE:             # Ping systemd watchdog before sleeping in the stopped state
# REMOVED_UNUSED_CODE:             self._notify("WATCHDOG=1\nSTATUS=State: STOPPED.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self._throttle(func=self._process_stopped, throttle_secs=self._throttle_secs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         elif state == State.RUNNING:
# REMOVED_UNUSED_CODE:             # Ping systemd watchdog before throttling
# REMOVED_UNUSED_CODE:             self._notify("WATCHDOG=1\nSTATUS=State: RUNNING.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Use an offset of 1s to ensure a new candle has been issued
# REMOVED_UNUSED_CODE:             self._throttle(
# REMOVED_UNUSED_CODE:                 func=self._process_running,
# REMOVED_UNUSED_CODE:                 throttle_secs=self._throttle_secs,
# REMOVED_UNUSED_CODE:                 timeframe=self._config["timeframe"] if self._config else None,
# REMOVED_UNUSED_CODE:                 timeframe_offset=1,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._heartbeat_interval:
# REMOVED_UNUSED_CODE:             now = time.time()
# REMOVED_UNUSED_CODE:             if (now - self._heartbeat_msg) > self._heartbeat_interval:
# REMOVED_UNUSED_CODE:                 version = __version__
# REMOVED_UNUSED_CODE:                 strategy_version = self.freqtrade.strategy.version()
# REMOVED_UNUSED_CODE:                 if strategy_version is not None:
# REMOVED_UNUSED_CODE:                     version += ", strategy_version: " + strategy_version
# REMOVED_UNUSED_CODE:                 logger.info(
# REMOVED_UNUSED_CODE:                     f"Bot heartbeat. PID={getpid()}, version='{version}', state='{state.name}'"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 self._heartbeat_msg = now
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return state
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _throttle(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         func: Callable[..., Any],
# REMOVED_UNUSED_CODE:         throttle_secs: float,
# REMOVED_UNUSED_CODE:         timeframe: str | None = None,
# REMOVED_UNUSED_CODE:         timeframe_offset: float = 1.0,
# REMOVED_UNUSED_CODE:         *args,
# REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ) -> Any:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Throttles the given callable that it
# REMOVED_UNUSED_CODE:         takes at least `min_secs` to finish execution.
# REMOVED_UNUSED_CODE:         :param func: Any callable
# REMOVED_UNUSED_CODE:         :param throttle_secs: throttling iteration execution time limit in seconds
# REMOVED_UNUSED_CODE:         :param timeframe: ensure iteration is executed at the beginning of the next candle.
# REMOVED_UNUSED_CODE:         :param timeframe_offset: offset in seconds to apply to the next candle time.
# REMOVED_UNUSED_CODE:         :return: Any (result of execution of func)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         last_throttle_start_time = time.time()
# REMOVED_UNUSED_CODE:         logger.debug("========================================")
# REMOVED_UNUSED_CODE:         result = func(*args, **kwargs)
# REMOVED_UNUSED_CODE:         time_passed = time.time() - last_throttle_start_time
# REMOVED_UNUSED_CODE:         sleep_duration = throttle_secs - time_passed
# REMOVED_UNUSED_CODE:         if timeframe:
# REMOVED_UNUSED_CODE:             next_tf = timeframe_to_next_date(timeframe)
# REMOVED_UNUSED_CODE:             # Maximum throttling should be until new candle arrives
# REMOVED_UNUSED_CODE:             # Offset is added to ensure a new candle has been issued.
# REMOVED_UNUSED_CODE:             next_tft = next_tf.timestamp() - time.time()
# REMOVED_UNUSED_CODE:             next_tf_with_offset = next_tft + timeframe_offset
# REMOVED_UNUSED_CODE:             if next_tft < sleep_duration and sleep_duration < next_tf_with_offset:
# REMOVED_UNUSED_CODE:                 # Avoid hitting a new loop between the new candle and the candle with offset
# REMOVED_UNUSED_CODE:                 sleep_duration = next_tf_with_offset
# REMOVED_UNUSED_CODE:             sleep_duration = min(sleep_duration, next_tf_with_offset)
# REMOVED_UNUSED_CODE:         sleep_duration = max(sleep_duration, 0.0)
# REMOVED_UNUSED_CODE:         # next_iter = datetime.now(timezone.utc) + timedelta(seconds=sleep_duration)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.debug(
# REMOVED_UNUSED_CODE:             f"Throttling with '{func.__name__}()': sleep for {sleep_duration:.2f} s, "
# REMOVED_UNUSED_CODE:             f"last iteration took {time_passed:.2f} s."
# REMOVED_UNUSED_CODE:             #  f"next: {next_iter}"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         self._sleep(sleep_duration)
# REMOVED_UNUSED_CODE:         return result
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def _sleep(sleep_duration: float) -> None:
# REMOVED_UNUSED_CODE:         """Local sleep method - to improve testability"""
# REMOVED_UNUSED_CODE:         time.sleep(sleep_duration)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _process_stopped(self) -> None:
# REMOVED_UNUSED_CODE:         self.freqtrade.process_stopped()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _process_running(self) -> None:
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             self.freqtrade.process()
# REMOVED_UNUSED_CODE:         except TemporaryError as error:
# REMOVED_UNUSED_CODE:             logger.warning(f"Error: {error}, retrying in {RETRY_TIMEOUT} seconds...")
# REMOVED_UNUSED_CODE:             time.sleep(RETRY_TIMEOUT)
# REMOVED_UNUSED_CODE:         except OperationalException:
# REMOVED_UNUSED_CODE:             tb = traceback.format_exc()
# REMOVED_UNUSED_CODE:             hint = "Issue `/start` if you think it is safe to restart."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.freqtrade.notify_status(
# REMOVED_UNUSED_CODE:                 f"*OperationalException:*\n```\n{tb}```\n {hint}", msg_type=RPCMessageType.EXCEPTION
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             logger.exception("OperationalException. Stopping trader ...")
# REMOVED_UNUSED_CODE:             self.freqtrade.state = State.STOPPED
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _reconfigure(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Cleans up current freqtradebot instance, reloads the configuration and
# REMOVED_UNUSED_CODE:         replaces it with the new instance
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Tell systemd that we initiated reconfiguration
# REMOVED_UNUSED_CODE:         self._notify("RELOADING=1")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Clean up current freqtrade modules
# REMOVED_UNUSED_CODE:         self.freqtrade.cleanup()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Load and validate config and create new instance of the bot
# REMOVED_UNUSED_CODE:         self._init(True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.freqtrade.notify_status("config reloaded")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Tell systemd that we completed reconfiguration
# REMOVED_UNUSED_CODE:         self._notify("READY=1")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def exit(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Tell systemd that we are exiting now
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._notify("STOPPING=1")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.freqtrade:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.freqtrade.notify_status("process died")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.freqtrade.cleanup()
