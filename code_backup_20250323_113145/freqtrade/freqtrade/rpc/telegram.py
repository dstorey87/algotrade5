# pragma pylint: disable=unused-argument, unused-variable, protected-access, invalid-name

"""
This module manage Telegram communication
"""

# REMOVED_UNUSED_CODE: import asyncio
# REMOVED_UNUSED_CODE: import json
import logging
# REMOVED_UNUSED_CODE: import re
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from collections.abc import Callable, Coroutine
# REMOVED_UNUSED_CODE: from copy import deepcopy
# REMOVED_UNUSED_CODE: from dataclasses import dataclass
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import date, datetime, timedelta
# REMOVED_UNUSED_CODE: from functools import partial, wraps
# REMOVED_UNUSED_CODE: from html import escape
# REMOVED_UNUSED_CODE: from itertools import chain
# REMOVED_UNUSED_CODE: from math import isnan
# REMOVED_UNUSED_CODE: from threading import Thread
# REMOVED_UNUSED_CODE: from typing import Any, Literal

# REMOVED_UNUSED_CODE: from tabulate import tabulate
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from telegram import (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     CallbackQuery,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     InlineKeyboardButton,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     InlineKeyboardMarkup,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     KeyboardButton,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ReplyKeyboardMarkup,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     Update,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: )
# REMOVED_UNUSED_CODE: from telegram.constants import MessageLimit, ParseMode
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from telegram.error import BadRequest, NetworkError, TelegramError
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from telegram.ext import Application, CallbackContext, CallbackQueryHandler, CommandHandler
# REMOVED_UNUSED_CODE: from telegram.helpers import escape_markdown

# REMOVED_UNUSED_CODE: from freqtrade.__init__ import __version__
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.constants import DUST_PER_COIN, Config
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.enums import MarketDirection, RPCMessageType, SignalDirection, TradingMode
# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.misc import chunks, plural
# REMOVED_UNUSED_CODE: from freqtrade.persistence import Trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.rpc import RPC, RPCException, RPCHandler
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.rpc.rpc_types import RPCEntryMsg, RPCExitMsg, RPCOrderMsg, RPCSendMsg
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.util import (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     dt_from_ts,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     dt_humanize_delta,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     fmt_coin,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     fmt_coin2,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     format_date,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     round_value,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: )


# REMOVED_UNUSED_CODE: MAX_MESSAGE_LENGTH = MessageLimit.MAX_TEXT_LENGTH


logger = logging.getLogger(__name__)

logger.debug("Included module rpc.telegram ...")


# REMOVED_UNUSED_CODE: def safe_async_db(func: Callable[..., Any]):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Decorator to safely handle sessions when switching async context
# REMOVED_UNUSED_CODE:     :param func: function to decorate
# REMOVED_UNUSED_CODE:     :return: decorated function
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @wraps(func)
# REMOVED_UNUSED_CODE:     def wrapper(*args, **kwargs):
# REMOVED_UNUSED_CODE:         """Decorator logic"""
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             return func(*args, **kwargs)
# REMOVED_UNUSED_CODE:         finally:
# REMOVED_UNUSED_CODE:             Trade.session.remove()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return wrapper


# REMOVED_UNUSED_CODE: @dataclass
# REMOVED_UNUSED_CODE: class TimeunitMappings:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     header: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     message: str
# REMOVED_UNUSED_CODE:     message2: str
# REMOVED_UNUSED_CODE:     callback: str
# REMOVED_UNUSED_CODE:     default: int
# REMOVED_UNUSED_CODE:     dateformat: str


# REMOVED_UNUSED_CODE: def authorized_only(command_handler: Callable[..., Coroutine[Any, Any, None]]):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Decorator to check if the message comes from the correct chat_id
# REMOVED_UNUSED_CODE:     can only be used with Telegram Class to decorate instance methods.
# REMOVED_UNUSED_CODE:     :param command_handler: Telegram CommandHandler
# REMOVED_UNUSED_CODE:     :return: decorated function
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @wraps(command_handler)
# REMOVED_UNUSED_CODE:     async def wrapper(self, *args, **kwargs):
# REMOVED_UNUSED_CODE:         """Decorator logic"""
# REMOVED_UNUSED_CODE:         update = kwargs.get("update") or args[0]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Reject unauthorized messages
# REMOVED_UNUSED_CODE:         if update.callback_query:
# REMOVED_UNUSED_CODE:             cchat_id = int(update.callback_query.message.chat.id)
# REMOVED_UNUSED_CODE:             ctopic_id = update.callback_query.message.message_thread_id
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             cchat_id = int(update.message.chat_id)
# REMOVED_UNUSED_CODE:             ctopic_id = update.message.message_thread_id
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         chat_id = int(self._config["telegram"]["chat_id"])
# REMOVED_UNUSED_CODE:         if cchat_id != chat_id:
# REMOVED_UNUSED_CODE:             logger.info(f"Rejected unauthorized message from: {cchat_id}")
# REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE:         if (topic_id := self._config["telegram"].get("topic_id")) is not None:
# REMOVED_UNUSED_CODE:             if str(ctopic_id) != topic_id:
# REMOVED_UNUSED_CODE:                 # This can be quite common in multi-topic environments.
# REMOVED_UNUSED_CODE:                 logger.debug(f"Rejected message from wrong channel: {cchat_id}, {ctopic_id}")
# REMOVED_UNUSED_CODE:                 return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Rollback session to avoid getting data stored in a transaction.
# REMOVED_UNUSED_CODE:         Trade.rollback()
# REMOVED_UNUSED_CODE:         logger.debug("Executing handler: %s for chat_id: %s", command_handler.__name__, chat_id)
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             return await command_handler(self, *args, **kwargs)
# REMOVED_UNUSED_CODE:         except RPCException as e:
# REMOVED_UNUSED_CODE:             await self._send_msg(str(e))
# REMOVED_UNUSED_CODE:         except BaseException:
# REMOVED_UNUSED_CODE:             logger.exception("Exception occurred within Telegram module")
# REMOVED_UNUSED_CODE:         finally:
# REMOVED_UNUSED_CODE:             Trade.session.remove()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return wrapper


# REMOVED_UNUSED_CODE: class Telegram(RPCHandler):
# REMOVED_UNUSED_CODE:     """This class handles all telegram communication"""
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, rpc: RPC, config: Config) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Init the Telegram call, and init the super class RPCHandler
# REMOVED_UNUSED_CODE:         :param rpc: instance of RPC Helper class
# REMOVED_UNUSED_CODE:         :param config: Configuration object
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         super().__init__(rpc, config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._app: Application
# REMOVED_UNUSED_CODE:         self._loop: asyncio.AbstractEventLoop
# REMOVED_UNUSED_CODE:         self._init_keyboard()
# REMOVED_UNUSED_CODE:         self._start_thread()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _start_thread(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Creates and starts the polling thread
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self._thread = Thread(target=self._init, name="FTTelegram")
# REMOVED_UNUSED_CODE:         self._thread.start()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _init_keyboard(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Validates the keyboard configuration from telegram config
# REMOVED_UNUSED_CODE:         section.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self._keyboard: list[list[str | KeyboardButton]] = [
# REMOVED_UNUSED_CODE:             ["/daily", "/profit", "/balance"],
# REMOVED_UNUSED_CODE:             ["/status", "/status table", "/performance"],
# REMOVED_UNUSED_CODE:             ["/count", "/start", "/stop", "/help"],
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         # do not allow commands with mandatory arguments and critical cmds
# REMOVED_UNUSED_CODE:         # TODO: DRY! - its not good to list all valid cmds here. But otherwise
# REMOVED_UNUSED_CODE:         #       this needs refactoring of the whole telegram module (same
# REMOVED_UNUSED_CODE:         #       problem in _help()).
# REMOVED_UNUSED_CODE:         valid_keys: list[str] = [
# REMOVED_UNUSED_CODE:             r"/start$",
# REMOVED_UNUSED_CODE:             r"/stop$",
# REMOVED_UNUSED_CODE:             r"/status$",
# REMOVED_UNUSED_CODE:             r"/status table$",
# REMOVED_UNUSED_CODE:             r"/trades$",
# REMOVED_UNUSED_CODE:             r"/performance$",
# REMOVED_UNUSED_CODE:             r"/buys",
# REMOVED_UNUSED_CODE:             r"/entries",
# REMOVED_UNUSED_CODE:             r"/sells",
# REMOVED_UNUSED_CODE:             r"/exits",
# REMOVED_UNUSED_CODE:             r"/mix_tags",
# REMOVED_UNUSED_CODE:             r"/daily$",
# REMOVED_UNUSED_CODE:             r"/daily \d+$",
# REMOVED_UNUSED_CODE:             r"/profit$",
# REMOVED_UNUSED_CODE:             r"/profit \d+",
# REMOVED_UNUSED_CODE:             r"/stats$",
# REMOVED_UNUSED_CODE:             r"/count$",
# REMOVED_UNUSED_CODE:             r"/locks$",
# REMOVED_UNUSED_CODE:             r"/balance$",
# REMOVED_UNUSED_CODE:             r"/stopbuy$",
# REMOVED_UNUSED_CODE:             r"/stopentry$",
# REMOVED_UNUSED_CODE:             r"/reload_config$",
# REMOVED_UNUSED_CODE:             r"/show_config$",
# REMOVED_UNUSED_CODE:             r"/logs$",
# REMOVED_UNUSED_CODE:             r"/whitelist$",
# REMOVED_UNUSED_CODE:             r"/whitelist(\ssorted|\sbaseonly)+$",
# REMOVED_UNUSED_CODE:             r"/blacklist$",
# REMOVED_UNUSED_CODE:             r"/bl_delete$",
# REMOVED_UNUSED_CODE:             r"/weekly$",
# REMOVED_UNUSED_CODE:             r"/weekly \d+$",
# REMOVED_UNUSED_CODE:             r"/monthly$",
# REMOVED_UNUSED_CODE:             r"/monthly \d+$",
# REMOVED_UNUSED_CODE:             r"/forcebuy$",
# REMOVED_UNUSED_CODE:             r"/forcelong$",
# REMOVED_UNUSED_CODE:             r"/forceshort$",
# REMOVED_UNUSED_CODE:             r"/forcesell$",
# REMOVED_UNUSED_CODE:             r"/forceexit$",
# REMOVED_UNUSED_CODE:             r"/edge$",
# REMOVED_UNUSED_CODE:             r"/health$",
# REMOVED_UNUSED_CODE:             r"/help$",
# REMOVED_UNUSED_CODE:             r"/version$",
# REMOVED_UNUSED_CODE:             r"/marketdir (long|short|even|none)$",
# REMOVED_UNUSED_CODE:             r"/marketdir$",
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         # Create keys for generation
# REMOVED_UNUSED_CODE:         valid_keys_print = [k.replace("$", "") for k in valid_keys]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # custom keyboard specified in config.json
# REMOVED_UNUSED_CODE:         cust_keyboard = self._config["telegram"].get("keyboard", [])
# REMOVED_UNUSED_CODE:         if cust_keyboard:
# REMOVED_UNUSED_CODE:             combined = "(" + ")|(".join(valid_keys) + ")"
# REMOVED_UNUSED_CODE:             # check for valid shortcuts
# REMOVED_UNUSED_CODE:             invalid_keys = [
# REMOVED_UNUSED_CODE:                 b for b in chain.from_iterable(cust_keyboard) if not re.match(combined, b)
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE:             if len(invalid_keys):
# REMOVED_UNUSED_CODE:                 err_msg = (
# REMOVED_UNUSED_CODE:                     "config.telegram.keyboard: Invalid commands for "
# REMOVED_UNUSED_CODE:                     f"custom Telegram keyboard: {invalid_keys}"
# REMOVED_UNUSED_CODE:                     f"\nvalid commands are: {valid_keys_print}"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 raise OperationalException(err_msg)
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 self._keyboard = cust_keyboard
# REMOVED_UNUSED_CODE:                 logger.info(f"using custom keyboard from config.json: {self._keyboard}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _init_telegram_app(self):
# REMOVED_UNUSED_CODE:         return Application.builder().token(self._config["telegram"]["token"]).build()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _init(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Initializes this module with the given config,
# REMOVED_UNUSED_CODE:         registers all known command handlers
# REMOVED_UNUSED_CODE:         and starts polling for message updates
# REMOVED_UNUSED_CODE:         Runs in a separate thread.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             self._loop = asyncio.get_running_loop()
# REMOVED_UNUSED_CODE:         except RuntimeError:
# REMOVED_UNUSED_CODE:             self._loop = asyncio.new_event_loop()
# REMOVED_UNUSED_CODE:             asyncio.set_event_loop(self._loop)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._app = self._init_telegram_app()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Register command handler and start telegram message polling
# REMOVED_UNUSED_CODE:         handles = [
# REMOVED_UNUSED_CODE:             CommandHandler("status", self._status),
# REMOVED_UNUSED_CODE:             CommandHandler("profit", self._profit),
# REMOVED_UNUSED_CODE:             CommandHandler("balance", self._balance),
# REMOVED_UNUSED_CODE:             CommandHandler("start", self._start),
# REMOVED_UNUSED_CODE:             CommandHandler("stop", self._stop),
# REMOVED_UNUSED_CODE:             CommandHandler(["forcesell", "forceexit", "fx"], self._force_exit),
# REMOVED_UNUSED_CODE:             CommandHandler(
# REMOVED_UNUSED_CODE:                 ["forcebuy", "forcelong"],
# REMOVED_UNUSED_CODE:                 partial(self._force_enter, order_side=SignalDirection.LONG),
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:             CommandHandler(
# REMOVED_UNUSED_CODE:                 "forceshort", partial(self._force_enter, order_side=SignalDirection.SHORT)
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:             CommandHandler("reload_trade", self._reload_trade_from_exchange),
# REMOVED_UNUSED_CODE:             CommandHandler("trades", self._trades),
# REMOVED_UNUSED_CODE:             CommandHandler("delete", self._delete_trade),
# REMOVED_UNUSED_CODE:             CommandHandler(["coo", "cancel_open_order"], self._cancel_open_order),
# REMOVED_UNUSED_CODE:             CommandHandler("performance", self._performance),
# REMOVED_UNUSED_CODE:             CommandHandler(["buys", "entries"], self._enter_tag_performance),
# REMOVED_UNUSED_CODE:             CommandHandler(["sells", "exits"], self._exit_reason_performance),
# REMOVED_UNUSED_CODE:             CommandHandler("mix_tags", self._mix_tag_performance),
# REMOVED_UNUSED_CODE:             CommandHandler("stats", self._stats),
# REMOVED_UNUSED_CODE:             CommandHandler("daily", self._daily),
# REMOVED_UNUSED_CODE:             CommandHandler("weekly", self._weekly),
# REMOVED_UNUSED_CODE:             CommandHandler("monthly", self._monthly),
# REMOVED_UNUSED_CODE:             CommandHandler("count", self._count),
# REMOVED_UNUSED_CODE:             CommandHandler("locks", self._locks),
# REMOVED_UNUSED_CODE:             CommandHandler(["unlock", "delete_locks"], self._delete_locks),
# REMOVED_UNUSED_CODE:             CommandHandler(["reload_config", "reload_conf"], self._reload_config),
# REMOVED_UNUSED_CODE:             CommandHandler(["show_config", "show_conf"], self._show_config),
# REMOVED_UNUSED_CODE:             CommandHandler(["stopbuy", "stopentry"], self._stopentry),
# REMOVED_UNUSED_CODE:             CommandHandler("whitelist", self._whitelist),
# REMOVED_UNUSED_CODE:             CommandHandler("blacklist", self._blacklist),
# REMOVED_UNUSED_CODE:             CommandHandler(["blacklist_delete", "bl_delete"], self._blacklist_delete),
# REMOVED_UNUSED_CODE:             CommandHandler("logs", self._logs),
# REMOVED_UNUSED_CODE:             CommandHandler("edge", self._edge),
# REMOVED_UNUSED_CODE:             CommandHandler("health", self._health),
# REMOVED_UNUSED_CODE:             CommandHandler("help", self._help),
# REMOVED_UNUSED_CODE:             CommandHandler("version", self._version),
# REMOVED_UNUSED_CODE:             CommandHandler("marketdir", self._changemarketdir),
# REMOVED_UNUSED_CODE:             CommandHandler("order", self._order),
# REMOVED_UNUSED_CODE:             CommandHandler("list_custom_data", self._list_custom_data),
# REMOVED_UNUSED_CODE:             CommandHandler("tg_info", self._tg_info),
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         callbacks = [
# REMOVED_UNUSED_CODE:             CallbackQueryHandler(self._status_table, pattern="update_status_table"),
# REMOVED_UNUSED_CODE:             CallbackQueryHandler(self._daily, pattern="update_daily"),
# REMOVED_UNUSED_CODE:             CallbackQueryHandler(self._weekly, pattern="update_weekly"),
# REMOVED_UNUSED_CODE:             CallbackQueryHandler(self._monthly, pattern="update_monthly"),
# REMOVED_UNUSED_CODE:             CallbackQueryHandler(self._profit, pattern="update_profit"),
# REMOVED_UNUSED_CODE:             CallbackQueryHandler(self._balance, pattern="update_balance"),
# REMOVED_UNUSED_CODE:             CallbackQueryHandler(self._performance, pattern="update_performance"),
# REMOVED_UNUSED_CODE:             CallbackQueryHandler(
# REMOVED_UNUSED_CODE:                 self._enter_tag_performance, pattern="update_enter_tag_performance"
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:             CallbackQueryHandler(
# REMOVED_UNUSED_CODE:                 self._exit_reason_performance, pattern="update_exit_reason_performance"
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:             CallbackQueryHandler(self._mix_tag_performance, pattern="update_mix_tag_performance"),
# REMOVED_UNUSED_CODE:             CallbackQueryHandler(self._count, pattern="update_count"),
# REMOVED_UNUSED_CODE:             CallbackQueryHandler(self._force_exit_inline, pattern=r"force_exit__\S+"),
# REMOVED_UNUSED_CODE:             CallbackQueryHandler(self._force_enter_inline, pattern=r"force_enter__\S+"),
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         for handle in handles:
# REMOVED_UNUSED_CODE:             self._app.add_handler(handle)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for callback in callbacks:
# REMOVED_UNUSED_CODE:             self._app.add_handler(callback)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.info(
# REMOVED_UNUSED_CODE:             "rpc.telegram is listening for following commands: %s",
# REMOVED_UNUSED_CODE:             [[x for x in sorted(h.commands)] for h in handles],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         self._loop.run_until_complete(self._startup_telegram())
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _startup_telegram(self) -> None:
# REMOVED_UNUSED_CODE:         await self._app.initialize()
# REMOVED_UNUSED_CODE:         await self._app.start()
# REMOVED_UNUSED_CODE:         if self._app.updater:
# REMOVED_UNUSED_CODE:             await self._app.updater.start_polling(
# REMOVED_UNUSED_CODE:                 bootstrap_retries=-1,
# REMOVED_UNUSED_CODE:                 timeout=20,
# REMOVED_UNUSED_CODE:                 # read_latency=60,  # Assumed transmission latency
# REMOVED_UNUSED_CODE:                 drop_pending_updates=True,
# REMOVED_UNUSED_CODE:                 # stop_signals=[],  # Necessary as we don't run on the main thread
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             while True:
# REMOVED_UNUSED_CODE:                 await asyncio.sleep(10)
# REMOVED_UNUSED_CODE:                 if not self._app.updater.running:
# REMOVED_UNUSED_CODE:                     break
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _cleanup_telegram(self) -> None:
# REMOVED_UNUSED_CODE:         if self._app.updater:
# REMOVED_UNUSED_CODE:             await self._app.updater.stop()
# REMOVED_UNUSED_CODE:         await self._app.stop()
# REMOVED_UNUSED_CODE:         await self._app.shutdown()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def cleanup(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Stops all running telegram threads.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # This can take up to `timeout` from the call to `start_polling`.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         asyncio.run_coroutine_threadsafe(self._cleanup_telegram(), self._loop)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._thread.join()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _exchange_from_msg(self, msg: RPCOrderMsg) -> str:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Extracts the exchange name from the given message.
# REMOVED_UNUSED_CODE:         :param msg: The message to extract the exchange name from.
# REMOVED_UNUSED_CODE:         :return: The exchange name.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return f"{msg['exchange']}{' (dry)' if self._config['dry_run'] else ''}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _add_analyzed_candle(self, pair: str) -> str:
# REMOVED_UNUSED_CODE:         candle_val = (
# REMOVED_UNUSED_CODE:             self._config["telegram"].get("notification_settings", {}).get("show_candle", "off")
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         if candle_val != "off":
# REMOVED_UNUSED_CODE:             if candle_val == "ohlc":
# REMOVED_UNUSED_CODE:                 analyzed_df, _ = self._rpc._freqtrade.dataprovider.get_analyzed_dataframe(
# REMOVED_UNUSED_CODE:                     pair, self._config["timeframe"]
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 candle = analyzed_df.iloc[-1].squeeze() if len(analyzed_df) > 0 else None
# REMOVED_UNUSED_CODE:                 if candle is not None:
# REMOVED_UNUSED_CODE:                     return (
# REMOVED_UNUSED_CODE:                         f"*Candle OHLC*: `{candle['open']}, {candle['high']}, "
# REMOVED_UNUSED_CODE:                         f"{candle['low']}, {candle['close']}`\n"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return ""
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _format_entry_msg(self, msg: RPCEntryMsg) -> str:
# REMOVED_UNUSED_CODE:         is_fill = msg["type"] in [RPCMessageType.ENTRY_FILL]
# REMOVED_UNUSED_CODE:         emoji = "\N{CHECK MARK}" if is_fill else "\N{LARGE BLUE CIRCLE}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         terminology = {
# REMOVED_UNUSED_CODE:             "1_enter": "New Trade",
# REMOVED_UNUSED_CODE:             "1_entered": "New Trade filled",
# REMOVED_UNUSED_CODE:             "x_enter": "Increasing position",
# REMOVED_UNUSED_CODE:             "x_entered": "Position increase filled",
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         key = f"{'x' if msg['sub_trade'] else '1'}_{'entered' if is_fill else 'enter'}"
# REMOVED_UNUSED_CODE:         wording = terminology[key]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         message = (
# REMOVED_UNUSED_CODE:             f"{emoji} *{self._exchange_from_msg(msg)}:*"
# REMOVED_UNUSED_CODE:             f" {wording} (#{msg['trade_id']})\n"
# REMOVED_UNUSED_CODE:             f"*Pair:* `{msg['pair']}`\n"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         message += self._add_analyzed_candle(msg["pair"])
# REMOVED_UNUSED_CODE:         message += f"*Enter Tag:* `{msg['enter_tag']}`\n" if msg.get("enter_tag") else ""
# REMOVED_UNUSED_CODE:         message += f"*Amount:* `{round_value(msg['amount'], 8)}`\n"
# REMOVED_UNUSED_CODE:         message += f"*Direction:* `{msg['direction']}"
# REMOVED_UNUSED_CODE:         if msg.get("leverage") and msg.get("leverage", 1.0) != 1.0:
# REMOVED_UNUSED_CODE:             message += f" ({msg['leverage']:.3g}x)"
# REMOVED_UNUSED_CODE:         message += "`\n"
# REMOVED_UNUSED_CODE:         message += f"*Open Rate:* `{fmt_coin2(msg['open_rate'], msg['quote_currency'])}`\n"
# REMOVED_UNUSED_CODE:         if msg["type"] == RPCMessageType.ENTRY and msg["current_rate"]:
# REMOVED_UNUSED_CODE:             message += (
# REMOVED_UNUSED_CODE:                 f"*Current Rate:* `{fmt_coin2(msg['current_rate'], msg['quote_currency'])}`\n"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         profit_fiat_extra = self.__format_profit_fiat(msg, "stake_amount")  # type: ignore
# REMOVED_UNUSED_CODE:         total = fmt_coin(msg["stake_amount"], msg["quote_currency"])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         message += f"*{'New ' if msg['sub_trade'] else ''}Total:* `{total}{profit_fiat_extra}`"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return message
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _format_exit_msg(self, msg: RPCExitMsg) -> str:
# REMOVED_UNUSED_CODE:         duration = msg["close_date"].replace(microsecond=0) - msg["open_date"].replace(
# REMOVED_UNUSED_CODE:             microsecond=0
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         duration_min = duration.total_seconds() / 60
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         leverage_text = (
# REMOVED_UNUSED_CODE:             f" ({msg['leverage']:.3g}x)"
# REMOVED_UNUSED_CODE:             if msg.get("leverage") and msg.get("leverage", 1.0) != 1.0
# REMOVED_UNUSED_CODE:             else ""
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         profit_fiat_extra = self.__format_profit_fiat(msg, "profit_amount")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         profit_extra = (
# REMOVED_UNUSED_CODE:             f" ({msg['gain']}: {fmt_coin(msg['profit_amount'], msg['quote_currency'])}"
# REMOVED_UNUSED_CODE:             f"{profit_fiat_extra})"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         is_fill = msg["type"] == RPCMessageType.EXIT_FILL
# REMOVED_UNUSED_CODE:         is_sub_trade = msg.get("sub_trade")
# REMOVED_UNUSED_CODE:         is_sub_profit = msg["profit_amount"] != msg.get("cumulative_profit")
# REMOVED_UNUSED_CODE:         is_final_exit = msg.get("is_final_exit", False) and is_sub_profit
# REMOVED_UNUSED_CODE:         profit_prefix = "Sub " if is_sub_trade else ""
# REMOVED_UNUSED_CODE:         cp_extra = ""
# REMOVED_UNUSED_CODE:         exit_wording = "Exited" if is_fill else "Exiting"
# REMOVED_UNUSED_CODE:         if is_sub_trade or is_final_exit:
# REMOVED_UNUSED_CODE:             cp_fiat = self.__format_profit_fiat(msg, "cumulative_profit")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if is_final_exit:
# REMOVED_UNUSED_CODE:                 profit_prefix = "Sub "
# REMOVED_UNUSED_CODE:                 cp_extra = (
# REMOVED_UNUSED_CODE:                     f"*Final Profit:* `{msg['final_profit_ratio']:.2%} "
# REMOVED_UNUSED_CODE:                     f"({msg['cumulative_profit']:.8f} {msg['quote_currency']}{cp_fiat})`\n"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 exit_wording = f"Partially {exit_wording.lower()}"
# REMOVED_UNUSED_CODE:                 if msg["cumulative_profit"]:
# REMOVED_UNUSED_CODE:                     cp_extra = (
# REMOVED_UNUSED_CODE:                         f"*Cumulative Profit:* `"
# REMOVED_UNUSED_CODE:                         f"{fmt_coin(msg['cumulative_profit'], msg['stake_currency'])}{cp_fiat}`\n"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:         enter_tag = f"*Enter Tag:* `{msg['enter_tag']}`\n" if msg.get("enter_tag") else ""
# REMOVED_UNUSED_CODE:         message = (
# REMOVED_UNUSED_CODE:             f"{self._get_exit_emoji(msg)} *{self._exchange_from_msg(msg)}:* "
# REMOVED_UNUSED_CODE:             f"{exit_wording} {msg['pair']} (#{msg['trade_id']})\n"
# REMOVED_UNUSED_CODE:             f"{self._add_analyzed_candle(msg['pair'])}"
# REMOVED_UNUSED_CODE:             f"*{f'{profit_prefix}Profit' if is_fill else f'Unrealized {profit_prefix}Profit'}:* "
# REMOVED_UNUSED_CODE:             f"`{msg['profit_ratio']:.2%}{profit_extra}`\n"
# REMOVED_UNUSED_CODE:             f"{cp_extra}"
# REMOVED_UNUSED_CODE:             f"{enter_tag}"
# REMOVED_UNUSED_CODE:             f"*Exit Reason:* `{msg['exit_reason']}`\n"
# REMOVED_UNUSED_CODE:             f"*Direction:* `{msg['direction']}"
# REMOVED_UNUSED_CODE:             f"{leverage_text}`\n"
# REMOVED_UNUSED_CODE:             f"*Amount:* `{round_value(msg['amount'], 8)}`\n"
# REMOVED_UNUSED_CODE:             f"*Open Rate:* `{fmt_coin2(msg['open_rate'], msg['quote_currency'])}`\n"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         if msg["type"] == RPCMessageType.EXIT and msg["current_rate"]:
# REMOVED_UNUSED_CODE:             message += (
# REMOVED_UNUSED_CODE:                 f"*Current Rate:* `{fmt_coin2(msg['current_rate'], msg['quote_currency'])}`\n"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             if msg["order_rate"]:
# REMOVED_UNUSED_CODE:                 message += f"*Exit Rate:* `{fmt_coin2(msg['order_rate'], msg['quote_currency'])}`"
# REMOVED_UNUSED_CODE:         elif msg["type"] == RPCMessageType.EXIT_FILL:
# REMOVED_UNUSED_CODE:             message += f"*Exit Rate:* `{fmt_coin2(msg['close_rate'], msg['quote_currency'])}`"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if is_sub_trade:
# REMOVED_UNUSED_CODE:             stake_amount_fiat = self.__format_profit_fiat(msg, "stake_amount")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             rem = fmt_coin(msg["stake_amount"], msg["quote_currency"])
# REMOVED_UNUSED_CODE:             message += f"\n*Remaining:* `{rem}{stake_amount_fiat}`"
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             message += f"\n*Duration:* `{duration} ({duration_min:.1f} min)`"
# REMOVED_UNUSED_CODE:         return message
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __format_profit_fiat(
# REMOVED_UNUSED_CODE:         self, msg: RPCExitMsg, key: Literal["stake_amount", "profit_amount", "cumulative_profit"]
# REMOVED_UNUSED_CODE:     ) -> str:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Format Fiat currency to append to regular profit output
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         profit_fiat_extra = ""
# REMOVED_UNUSED_CODE:         if self._rpc._fiat_converter and (fiat_currency := msg.get("fiat_currency")):
# REMOVED_UNUSED_CODE:             profit_fiat = self._rpc._fiat_converter.convert_amount(
# REMOVED_UNUSED_CODE:                 msg[key], msg["stake_currency"], fiat_currency
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             profit_fiat_extra = f" / {profit_fiat:.3f} {fiat_currency}"
# REMOVED_UNUSED_CODE:         return profit_fiat_extra
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def compose_message(self, msg: RPCSendMsg) -> str | None:
# REMOVED_UNUSED_CODE:         if msg["type"] == RPCMessageType.ENTRY or msg["type"] == RPCMessageType.ENTRY_FILL:
# REMOVED_UNUSED_CODE:             message = self._format_entry_msg(msg)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         elif msg["type"] == RPCMessageType.EXIT or msg["type"] == RPCMessageType.EXIT_FILL:
# REMOVED_UNUSED_CODE:             message = self._format_exit_msg(msg)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         elif (
# REMOVED_UNUSED_CODE:             msg["type"] == RPCMessageType.ENTRY_CANCEL or msg["type"] == RPCMessageType.EXIT_CANCEL
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             message_side = "enter" if msg["type"] == RPCMessageType.ENTRY_CANCEL else "exit"
# REMOVED_UNUSED_CODE:             message = (
# REMOVED_UNUSED_CODE:                 f"\N{WARNING SIGN} *{self._exchange_from_msg(msg)}:* "
# REMOVED_UNUSED_CODE:                 f"Cancelling {'partial ' if msg.get('sub_trade') else ''}"
# REMOVED_UNUSED_CODE:                 f"{message_side} Order for {msg['pair']} "
# REMOVED_UNUSED_CODE:                 f"(#{msg['trade_id']}). Reason: {msg['reason']}."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         elif msg["type"] == RPCMessageType.PROTECTION_TRIGGER:
# REMOVED_UNUSED_CODE:             message = (
# REMOVED_UNUSED_CODE:                 f"*Protection* triggered due to {msg['reason']}. "
# REMOVED_UNUSED_CODE:                 f"`{msg['pair']}` will be locked until `{msg['lock_end_time']}`."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         elif msg["type"] == RPCMessageType.PROTECTION_TRIGGER_GLOBAL:
# REMOVED_UNUSED_CODE:             message = (
# REMOVED_UNUSED_CODE:                 f"*Protection* triggered due to {msg['reason']}. "
# REMOVED_UNUSED_CODE:                 f"*All pairs* will be locked until `{msg['lock_end_time']}`."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         elif msg["type"] == RPCMessageType.STATUS:
# REMOVED_UNUSED_CODE:             message = f"*Status:* `{msg['status']}`"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         elif msg["type"] == RPCMessageType.WARNING:
# REMOVED_UNUSED_CODE:             message = f"\N{WARNING SIGN} *Warning:* `{msg['status']}`"
# REMOVED_UNUSED_CODE:         elif msg["type"] == RPCMessageType.EXCEPTION:
# REMOVED_UNUSED_CODE:             # Errors will contain exceptions, which are wrapped in triple ticks.
# REMOVED_UNUSED_CODE:             message = f"\N{WARNING SIGN} *ERROR:* \n {msg['status']}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         elif msg["type"] == RPCMessageType.STARTUP:
# REMOVED_UNUSED_CODE:             message = f"{msg['status']}"
# REMOVED_UNUSED_CODE:         elif msg["type"] == RPCMessageType.STRATEGY_MSG:
# REMOVED_UNUSED_CODE:             message = f"{msg['msg']}"
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.debug("Unknown message type: %s", msg["type"])
# REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE:         return message
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _message_loudness(self, msg: RPCSendMsg) -> str:
# REMOVED_UNUSED_CODE:         """Determine the loudness of the message - on, off or silent"""
# REMOVED_UNUSED_CODE:         default_noti = "on"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         msg_type = msg["type"]
# REMOVED_UNUSED_CODE:         noti = ""
# REMOVED_UNUSED_CODE:         if msg["type"] == RPCMessageType.EXIT or msg["type"] == RPCMessageType.EXIT_FILL:
# REMOVED_UNUSED_CODE:             sell_noti = (
# REMOVED_UNUSED_CODE:                 self._config["telegram"].get("notification_settings", {}).get(str(msg_type), {})
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # For backward compatibility sell still can be string
# REMOVED_UNUSED_CODE:             if isinstance(sell_noti, str):
# REMOVED_UNUSED_CODE:                 noti = sell_noti
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 default_noti = sell_noti.get("*", default_noti)
# REMOVED_UNUSED_CODE:                 noti = sell_noti.get(str(msg["exit_reason"]), default_noti)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             noti = (
# REMOVED_UNUSED_CODE:                 self._config["telegram"]
# REMOVED_UNUSED_CODE:                 .get("notification_settings", {})
# REMOVED_UNUSED_CODE:                 .get(str(msg_type), default_noti)
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return noti
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def send_msg(self, msg: RPCSendMsg) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Send a message to telegram channel"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         noti = self._message_loudness(msg)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if noti == "off":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.info(f"Notification '{msg['type']}' not sent.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Notification disabled
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         message = self.compose_message(deepcopy(msg))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if message:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             asyncio.run_coroutine_threadsafe(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._send_msg(message, disable_notification=(noti == "silent")), self._loop
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _get_exit_emoji(self, msg):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get emoji for exit-messages
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if float(msg["profit_ratio"]) >= 0.05:
# REMOVED_UNUSED_CODE:             return "\N{ROCKET}"
# REMOVED_UNUSED_CODE:         elif float(msg["profit_ratio"]) >= 0.0:
# REMOVED_UNUSED_CODE:             return "\N{EIGHT SPOKED ASTERISK}"
# REMOVED_UNUSED_CODE:         elif msg["exit_reason"] == "stop_loss":
# REMOVED_UNUSED_CODE:             return "\N{WARNING SIGN}"
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return "\N{CROSS MARK}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _prepare_order_details(self, filled_orders: list, quote_currency: str, is_open: bool):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Prepare details of trade with entry adjustment enabled
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         lines_detail: list[str] = []
# REMOVED_UNUSED_CODE:         if len(filled_orders) > 0:
# REMOVED_UNUSED_CODE:             first_avg = filled_orders[0]["safe_price"]
# REMOVED_UNUSED_CODE:         order_nr = 0
# REMOVED_UNUSED_CODE:         for order in filled_orders:
# REMOVED_UNUSED_CODE:             lines: list[str] = []
# REMOVED_UNUSED_CODE:             if order["is_open"] is True:
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE:             order_nr += 1
# REMOVED_UNUSED_CODE:             wording = "Entry" if order["ft_is_entry"] else "Exit"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             cur_entry_amount = order["filled"] or order["amount"]
# REMOVED_UNUSED_CODE:             cur_entry_average = order["safe_price"]
# REMOVED_UNUSED_CODE:             lines.append("  ")
# REMOVED_UNUSED_CODE:             lines.append(f"*{wording} #{order_nr}:*")
# REMOVED_UNUSED_CODE:             if order_nr == 1:
# REMOVED_UNUSED_CODE:                 lines.append(
# REMOVED_UNUSED_CODE:                     f"*Amount:* {round_value(cur_entry_amount, 8)} "
# REMOVED_UNUSED_CODE:                     f"({fmt_coin(order['cost'], quote_currency)})"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 lines.append(f"*Average Price:* {round_value(cur_entry_average, 8)}")
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 # TODO: This calculation ignores fees.
# REMOVED_UNUSED_CODE:                 price_to_1st_entry = (cur_entry_average - first_avg) / first_avg
# REMOVED_UNUSED_CODE:                 if is_open:
# REMOVED_UNUSED_CODE:                     lines.append("({})".format(dt_humanize_delta(order["order_filled_date"])))
# REMOVED_UNUSED_CODE:                 lines.append(
# REMOVED_UNUSED_CODE:                     f"*Amount:* {round_value(cur_entry_amount, 8)} "
# REMOVED_UNUSED_CODE:                     f"({fmt_coin(order['cost'], quote_currency)})"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 lines.append(
# REMOVED_UNUSED_CODE:                     f"*Average {wording} Price:* {round_value(cur_entry_average, 8)} "
# REMOVED_UNUSED_CODE:                     f"({price_to_1st_entry:.2%} from 1st entry rate)"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 lines.append(f"*Order Filled:* {order['order_filled_date']}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             lines_detail.append("\n".join(lines))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return lines_detail
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _order(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /order.
# REMOVED_UNUSED_CODE:         Returns the orders of the trade
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trade_ids = []
# REMOVED_UNUSED_CODE:         if context.args and len(context.args) > 0:
# REMOVED_UNUSED_CODE:             trade_ids = [int(i) for i in context.args if i.isnumeric()]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         results = self._rpc._rpc_trade_status(trade_ids=trade_ids)
# REMOVED_UNUSED_CODE:         for r in results:
# REMOVED_UNUSED_CODE:             lines = ["*Order List for Trade #*`{trade_id}`"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             lines_detail = self._prepare_order_details(
# REMOVED_UNUSED_CODE:                 r["orders"], r["quote_currency"], r["is_open"]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             lines.extend(lines_detail if lines_detail else "")
# REMOVED_UNUSED_CODE:             await self.__send_order_msg(lines, r)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def __send_order_msg(self, lines: list[str], r: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Send status message.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         msg = ""
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for line in lines:
# REMOVED_UNUSED_CODE:             if line:
# REMOVED_UNUSED_CODE:                 if (len(msg) + len(line) + 1) < MAX_MESSAGE_LENGTH:
# REMOVED_UNUSED_CODE:                     msg += line + "\n"
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     await self._send_msg(msg.format(**r))
# REMOVED_UNUSED_CODE:                     msg = "*Order List for Trade #*`{trade_id}` - continued\n" + line + "\n"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         await self._send_msg(msg.format(**r))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _status(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /status.
# REMOVED_UNUSED_CODE:         Returns the current TradeThread status
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if context.args and "table" in context.args:
# REMOVED_UNUSED_CODE:             await self._status_table(update, context)
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             await self._status_msg(update, context)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _status_msg(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         handler for `/status` and `/status <id>`.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Check if there's at least one numerical ID provided.
# REMOVED_UNUSED_CODE:         # If so, try to get only these trades.
# REMOVED_UNUSED_CODE:         trade_ids = []
# REMOVED_UNUSED_CODE:         if context.args and len(context.args) > 0:
# REMOVED_UNUSED_CODE:             trade_ids = [int(i) for i in context.args if i.isnumeric()]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         results = self._rpc._rpc_trade_status(trade_ids=trade_ids)
# REMOVED_UNUSED_CODE:         position_adjust = self._config.get("position_adjustment_enable", False)
# REMOVED_UNUSED_CODE:         max_entries = self._config.get("max_entry_position_adjustment", -1)
# REMOVED_UNUSED_CODE:         for r in results:
# REMOVED_UNUSED_CODE:             r["open_date_hum"] = dt_humanize_delta(r["open_date"])
# REMOVED_UNUSED_CODE:             r["num_entries"] = len([o for o in r["orders"] if o["ft_is_entry"]])
# REMOVED_UNUSED_CODE:             r["num_exits"] = len(
# REMOVED_UNUSED_CODE:                 [
# REMOVED_UNUSED_CODE:                     o
# REMOVED_UNUSED_CODE:                     for o in r["orders"]
# REMOVED_UNUSED_CODE:                     if not o["ft_is_entry"] and not o["ft_order_side"] == "stoploss"
# REMOVED_UNUSED_CODE:                 ]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             r["exit_reason"] = r.get("exit_reason", "")
# REMOVED_UNUSED_CODE:             r["stake_amount_r"] = fmt_coin(r["stake_amount"], r["quote_currency"])
# REMOVED_UNUSED_CODE:             r["max_stake_amount_r"] = fmt_coin(
# REMOVED_UNUSED_CODE:                 r["max_stake_amount"] or r["stake_amount"], r["quote_currency"]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             r["profit_abs_r"] = fmt_coin(r["profit_abs"], r["quote_currency"])
# REMOVED_UNUSED_CODE:             r["realized_profit_r"] = fmt_coin(r["realized_profit"], r["quote_currency"])
# REMOVED_UNUSED_CODE:             r["total_profit_abs_r"] = fmt_coin(r["total_profit_abs"], r["quote_currency"])
# REMOVED_UNUSED_CODE:             lines = [
# REMOVED_UNUSED_CODE:                 "*Trade ID:* `{trade_id}`" + (" `(since {open_date_hum})`" if r["is_open"] else ""),
# REMOVED_UNUSED_CODE:                 "*Current Pair:* {pair}",
# REMOVED_UNUSED_CODE:                 (
# REMOVED_UNUSED_CODE:                     f"*Direction:* {'`Short`' if r.get('is_short') else '`Long`'}"
# REMOVED_UNUSED_CODE:                     + " ` ({leverage}x)`"
# REMOVED_UNUSED_CODE:                     if r.get("leverage")
# REMOVED_UNUSED_CODE:                     else ""
# REMOVED_UNUSED_CODE:                 ),
# REMOVED_UNUSED_CODE:                 "*Amount:* `{amount} ({stake_amount_r})`",
# REMOVED_UNUSED_CODE:                 "*Total invested:* `{max_stake_amount_r}`" if position_adjust else "",
# REMOVED_UNUSED_CODE:                 "*Enter Tag:* `{enter_tag}`" if r["enter_tag"] else "",
# REMOVED_UNUSED_CODE:                 "*Exit Reason:* `{exit_reason}`" if r["exit_reason"] else "",
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if position_adjust:
# REMOVED_UNUSED_CODE:                 max_buy_str = f"/{max_entries + 1}" if (max_entries > 0) else ""
# REMOVED_UNUSED_CODE:                 lines.extend(
# REMOVED_UNUSED_CODE:                     [
# REMOVED_UNUSED_CODE:                         "*Number of Entries:* `{num_entries}" + max_buy_str + "`",
# REMOVED_UNUSED_CODE:                         "*Number of Exits:* `{num_exits}`",
# REMOVED_UNUSED_CODE:                     ]
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             lines.extend(
# REMOVED_UNUSED_CODE:                 [
# REMOVED_UNUSED_CODE:                     f"*Open Rate:* `{round_value(r['open_rate'], 8)}`",
# REMOVED_UNUSED_CODE:                     f"*Close Rate:* `{round_value(r['close_rate'], 8)}`" if r["close_rate"] else "",
# REMOVED_UNUSED_CODE:                     "*Open Date:* `{open_date}`",
# REMOVED_UNUSED_CODE:                     "*Close Date:* `{close_date}`" if r["close_date"] else "",
# REMOVED_UNUSED_CODE:                     (
# REMOVED_UNUSED_CODE:                         f" \n*Current Rate:* `{round_value(r['current_rate'], 8)}`"
# REMOVED_UNUSED_CODE:                         if r["is_open"]
# REMOVED_UNUSED_CODE:                         else ""
# REMOVED_UNUSED_CODE:                     ),
# REMOVED_UNUSED_CODE:                     ("*Unrealized Profit:* " if r["is_open"] else "*Close Profit: *")
# REMOVED_UNUSED_CODE:                     + "`{profit_ratio:.2%}` `({profit_abs_r})`",
# REMOVED_UNUSED_CODE:                 ]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if r["is_open"]:
# REMOVED_UNUSED_CODE:                 if r.get("realized_profit"):
# REMOVED_UNUSED_CODE:                     lines.extend(
# REMOVED_UNUSED_CODE:                         [
# REMOVED_UNUSED_CODE:                             "*Realized Profit:* `{realized_profit_ratio:.2%} "
# REMOVED_UNUSED_CODE:                             "({realized_profit_r})`",
# REMOVED_UNUSED_CODE:                             "*Total Profit:* `{total_profit_ratio:.2%} ({total_profit_abs_r})`",
# REMOVED_UNUSED_CODE:                         ]
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 # Append empty line to improve readability
# REMOVED_UNUSED_CODE:                 lines.append(" ")
# REMOVED_UNUSED_CODE:                 if (
# REMOVED_UNUSED_CODE:                     r["stop_loss_abs"] != r["initial_stop_loss_abs"]
# REMOVED_UNUSED_CODE:                     and r["initial_stop_loss_ratio"] is not None
# REMOVED_UNUSED_CODE:                 ):
# REMOVED_UNUSED_CODE:                     # Adding initial stoploss only if it is different from stoploss
# REMOVED_UNUSED_CODE:                     lines.append(
# REMOVED_UNUSED_CODE:                         "*Initial Stoploss:* `{initial_stop_loss_abs:.8f}` "
# REMOVED_UNUSED_CODE:                         "`({initial_stop_loss_ratio:.2%})`"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 # Adding stoploss and stoploss percentage only if it is not None
# REMOVED_UNUSED_CODE:                 lines.append(
# REMOVED_UNUSED_CODE:                     f"*Stoploss:* `{round_value(r['stop_loss_abs'], 8)}` "
# REMOVED_UNUSED_CODE:                     + ("`({stop_loss_ratio:.2%})`" if r["stop_loss_ratio"] else "")
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 lines.append(
# REMOVED_UNUSED_CODE:                     f"*Stoploss distance:* `{round_value(r['stoploss_current_dist'], 8)}` "
# REMOVED_UNUSED_CODE:                     "`({stoploss_current_dist_ratio:.2%})`"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 if r.get("open_orders"):
# REMOVED_UNUSED_CODE:                     lines.append(
# REMOVED_UNUSED_CODE:                         "*Open Order:* `{open_orders}`"
# REMOVED_UNUSED_CODE:                         + ("- `{exit_order_status}`" if r["exit_order_status"] else "")
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             await self.__send_status_msg(lines, r)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def __send_status_msg(self, lines: list[str], r: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Send status message.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         msg = ""
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for line in lines:
# REMOVED_UNUSED_CODE:             if line:
# REMOVED_UNUSED_CODE:                 if (len(msg) + len(line) + 1) < MAX_MESSAGE_LENGTH:
# REMOVED_UNUSED_CODE:                     msg += line + "\n"
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     await self._send_msg(msg.format(**r))
# REMOVED_UNUSED_CODE:                     msg = "*Trade ID:* `{trade_id}` - continued\n" + line + "\n"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         await self._send_msg(msg.format(**r))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _status_table(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /status table.
# REMOVED_UNUSED_CODE:         Returns the current TradeThread status in table format
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         fiat_currency = self._config.get("fiat_display_currency", "")
# REMOVED_UNUSED_CODE:         statlist, head, fiat_profit_sum, fiat_total_profit_sum = self._rpc._rpc_status_table(
# REMOVED_UNUSED_CODE:             self._config["stake_currency"], fiat_currency
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         show_total = not isnan(fiat_profit_sum) and len(statlist) > 1
# REMOVED_UNUSED_CODE:         show_total_realized = (
# REMOVED_UNUSED_CODE:             not isnan(fiat_total_profit_sum) and len(statlist) > 1 and fiat_profit_sum
# REMOVED_UNUSED_CODE:         ) != fiat_total_profit_sum
# REMOVED_UNUSED_CODE:         max_trades_per_msg = 50
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Calculate the number of messages of 50 trades per message
# REMOVED_UNUSED_CODE:         0.99 is used to make sure that there are no extra (empty) messages
# REMOVED_UNUSED_CODE:         As an example with 50 trades, there will be int(50/50 + 0.99) = 1 message
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         messages_count = max(int(len(statlist) / max_trades_per_msg + 0.99), 1)
# REMOVED_UNUSED_CODE:         for i in range(0, messages_count):
# REMOVED_UNUSED_CODE:             trades = statlist[i * max_trades_per_msg : (i + 1) * max_trades_per_msg]
# REMOVED_UNUSED_CODE:             if show_total and i == messages_count - 1:
# REMOVED_UNUSED_CODE:                 # append total line
# REMOVED_UNUSED_CODE:                 trades.append(["Total", "", "", f"{fiat_profit_sum:.2f} {fiat_currency}"])
# REMOVED_UNUSED_CODE:                 if show_total_realized:
# REMOVED_UNUSED_CODE:                     trades.append(
# REMOVED_UNUSED_CODE:                         [
# REMOVED_UNUSED_CODE:                             "Total",
# REMOVED_UNUSED_CODE:                             "(incl. realized Profits)",
# REMOVED_UNUSED_CODE:                             "",
# REMOVED_UNUSED_CODE:                             f"{fiat_total_profit_sum:.2f} {fiat_currency}",
# REMOVED_UNUSED_CODE:                         ]
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             message = tabulate(trades, headers=head, tablefmt="simple")
# REMOVED_UNUSED_CODE:             if show_total and i == messages_count - 1:
# REMOVED_UNUSED_CODE:                 # insert separators line between Total
# REMOVED_UNUSED_CODE:                 lines = message.split("\n")
# REMOVED_UNUSED_CODE:                 offset = 2 if show_total_realized else 1
# REMOVED_UNUSED_CODE:                 message = "\n".join(lines[:-offset] + [lines[1]] + lines[-offset:])
# REMOVED_UNUSED_CODE:             await self._send_msg(
# REMOVED_UNUSED_CODE:                 f"<pre>{message}</pre>",
# REMOVED_UNUSED_CODE:                 parse_mode=ParseMode.HTML,
# REMOVED_UNUSED_CODE:                 reload_able=True,
# REMOVED_UNUSED_CODE:                 callback_path="update_status_table",
# REMOVED_UNUSED_CODE:                 query=update.callback_query,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _timeunit_stats(self, update: Update, context: CallbackContext, unit: str) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /daily <n>
# REMOVED_UNUSED_CODE:         Returns a daily profit (in BTC) over the last n days.
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         vals = {
# REMOVED_UNUSED_CODE:             "days": TimeunitMappings("Day", "Daily", "days", "update_daily", 7, "%Y-%m-%d"),
# REMOVED_UNUSED_CODE:             "weeks": TimeunitMappings(
# REMOVED_UNUSED_CODE:                 "Monday", "Weekly", "weeks (starting from Monday)", "update_weekly", 8, "%Y-%m-%d"
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:             "months": TimeunitMappings("Month", "Monthly", "months", "update_monthly", 6, "%Y-%m"),
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:         val = vals[unit]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         stake_cur = self._config["stake_currency"]
# REMOVED_UNUSED_CODE:         fiat_disp_cur = self._config.get("fiat_display_currency", "")
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             timescale = int(context.args[0]) if context.args else val.default
# REMOVED_UNUSED_CODE:         except (TypeError, ValueError, IndexError):
# REMOVED_UNUSED_CODE:             timescale = val.default
# REMOVED_UNUSED_CODE:         stats = self._rpc._rpc_timeunit_profit(timescale, stake_cur, fiat_disp_cur, unit)
# REMOVED_UNUSED_CODE:         stats_tab = tabulate(
# REMOVED_UNUSED_CODE:             [
# REMOVED_UNUSED_CODE:                 [
# REMOVED_UNUSED_CODE:                     f"{period['date']:{val.dateformat}} ({period['trade_count']})",
# REMOVED_UNUSED_CODE:                     f"{fmt_coin(period['abs_profit'], stats['stake_currency'])}",
# REMOVED_UNUSED_CODE:                     f"{period['fiat_value']:.2f} {stats['fiat_display_currency']}",
# REMOVED_UNUSED_CODE:                     f"{period['rel_profit']:.2%}",
# REMOVED_UNUSED_CODE:                 ]
# REMOVED_UNUSED_CODE:                 for period in stats["data"]
# REMOVED_UNUSED_CODE:             ],
# REMOVED_UNUSED_CODE:             headers=[
# REMOVED_UNUSED_CODE:                 f"{val.header} (count)",
# REMOVED_UNUSED_CODE:                 f"{stake_cur}",
# REMOVED_UNUSED_CODE:                 f"{fiat_disp_cur}",
# REMOVED_UNUSED_CODE:                 "Profit %",
# REMOVED_UNUSED_CODE:                 "Trades",
# REMOVED_UNUSED_CODE:             ],
# REMOVED_UNUSED_CODE:             tablefmt="simple",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         message = (
# REMOVED_UNUSED_CODE:             f"<b>{val.message} Profit over the last {timescale} {val.message2}</b>:\n"
# REMOVED_UNUSED_CODE:             f"<pre>{stats_tab}</pre>"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         await self._send_msg(
# REMOVED_UNUSED_CODE:             message,
# REMOVED_UNUSED_CODE:             parse_mode=ParseMode.HTML,
# REMOVED_UNUSED_CODE:             reload_able=True,
# REMOVED_UNUSED_CODE:             callback_path=val.callback,
# REMOVED_UNUSED_CODE:             query=update.callback_query,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _daily(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /daily <n>
# REMOVED_UNUSED_CODE:         Returns a daily profit (in BTC) over the last n days.
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         await self._timeunit_stats(update, context, "days")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _weekly(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /weekly <n>
# REMOVED_UNUSED_CODE:         Returns a weekly profit (in BTC) over the last n weeks.
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         await self._timeunit_stats(update, context, "weeks")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _monthly(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /monthly <n>
# REMOVED_UNUSED_CODE:         Returns a monthly profit (in BTC) over the last n months.
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         await self._timeunit_stats(update, context, "months")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _profit(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /profit.
# REMOVED_UNUSED_CODE:         Returns a cumulative profit statistics.
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         stake_cur = self._config["stake_currency"]
# REMOVED_UNUSED_CODE:         fiat_disp_cur = self._config.get("fiat_display_currency", "")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         start_date = datetime.fromtimestamp(0)
# REMOVED_UNUSED_CODE:         timescale = None
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             if context.args:
# REMOVED_UNUSED_CODE:                 timescale = int(context.args[0]) - 1
# REMOVED_UNUSED_CODE:                 today_start = datetime.combine(date.today(), datetime.min.time())
# REMOVED_UNUSED_CODE:                 start_date = today_start - timedelta(days=timescale)
# REMOVED_UNUSED_CODE:         except (TypeError, ValueError, IndexError):
# REMOVED_UNUSED_CODE:             pass
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         stats = self._rpc._rpc_trade_statistics(stake_cur, fiat_disp_cur, start_date)
# REMOVED_UNUSED_CODE:         profit_closed_coin = stats["profit_closed_coin"]
# REMOVED_UNUSED_CODE:         profit_closed_ratio_mean = stats["profit_closed_ratio_mean"]
# REMOVED_UNUSED_CODE:         profit_closed_percent = stats["profit_closed_percent"]
# REMOVED_UNUSED_CODE:         profit_closed_fiat = stats["profit_closed_fiat"]
# REMOVED_UNUSED_CODE:         profit_all_coin = stats["profit_all_coin"]
# REMOVED_UNUSED_CODE:         profit_all_ratio_mean = stats["profit_all_ratio_mean"]
# REMOVED_UNUSED_CODE:         profit_all_percent = stats["profit_all_percent"]
# REMOVED_UNUSED_CODE:         profit_all_fiat = stats["profit_all_fiat"]
# REMOVED_UNUSED_CODE:         trade_count = stats["trade_count"]
# REMOVED_UNUSED_CODE:         first_trade_date = f"{stats['first_trade_humanized']} ({stats['first_trade_date']})"
# REMOVED_UNUSED_CODE:         latest_trade_date = f"{stats['latest_trade_humanized']} ({stats['latest_trade_date']})"
# REMOVED_UNUSED_CODE:         avg_duration = stats["avg_duration"]
# REMOVED_UNUSED_CODE:         best_pair = stats["best_pair"]
# REMOVED_UNUSED_CODE:         best_pair_profit_ratio = stats["best_pair_profit_ratio"]
# REMOVED_UNUSED_CODE:         best_pair_profit_abs = fmt_coin(stats["best_pair_profit_abs"], stake_cur)
# REMOVED_UNUSED_CODE:         winrate = stats["winrate"]
# REMOVED_UNUSED_CODE:         expectancy = stats["expectancy"]
# REMOVED_UNUSED_CODE:         expectancy_ratio = stats["expectancy_ratio"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if stats["trade_count"] == 0:
# REMOVED_UNUSED_CODE:             markdown_msg = f"No trades yet.\n*Bot started:* `{stats['bot_start_date']}`"
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # Message to display
# REMOVED_UNUSED_CODE:             if stats["closed_trade_count"] > 0:
# REMOVED_UNUSED_CODE:                 markdown_msg = (
# REMOVED_UNUSED_CODE:                     "*ROI:* Closed trades\n"
# REMOVED_UNUSED_CODE:                     f"∙ `{fmt_coin(profit_closed_coin, stake_cur)} "
# REMOVED_UNUSED_CODE:                     f"({profit_closed_ratio_mean:.2%}) "
# REMOVED_UNUSED_CODE:                     f"({profit_closed_percent} \N{GREEK CAPITAL LETTER SIGMA}%)`\n"
# REMOVED_UNUSED_CODE:                     f"∙ `{fmt_coin(profit_closed_fiat, fiat_disp_cur)}`\n"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 markdown_msg = "`No closed trade` \n"
# REMOVED_UNUSED_CODE:             fiat_all_trades = (
# REMOVED_UNUSED_CODE:                 f"∙ `{fmt_coin(profit_all_fiat, fiat_disp_cur)}`\n" if fiat_disp_cur else ""
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             markdown_msg += (
# REMOVED_UNUSED_CODE:                 f"*ROI:* All trades\n"
# REMOVED_UNUSED_CODE:                 f"∙ `{fmt_coin(profit_all_coin, stake_cur)} "
# REMOVED_UNUSED_CODE:                 f"({profit_all_ratio_mean:.2%}) "
# REMOVED_UNUSED_CODE:                 f"({profit_all_percent} \N{GREEK CAPITAL LETTER SIGMA}%)`\n"
# REMOVED_UNUSED_CODE:                 f"{fiat_all_trades}"
# REMOVED_UNUSED_CODE:                 f"*Total Trade Count:* `{trade_count}`\n"
# REMOVED_UNUSED_CODE:                 f"*Bot started:* `{stats['bot_start_date']}`\n"
# REMOVED_UNUSED_CODE:                 f"*{'First Trade opened' if not timescale else 'Showing Profit since'}:* "
# REMOVED_UNUSED_CODE:                 f"`{first_trade_date}`\n"
# REMOVED_UNUSED_CODE:                 f"*Latest Trade opened:* `{latest_trade_date}`\n"
# REMOVED_UNUSED_CODE:                 f"*Win / Loss:* `{stats['winning_trades']} / {stats['losing_trades']}`\n"
# REMOVED_UNUSED_CODE:                 f"*Winrate:* `{winrate:.2%}`\n"
# REMOVED_UNUSED_CODE:                 f"*Expectancy (Ratio):* `{expectancy:.2f} ({expectancy_ratio:.2f})`"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             if stats["closed_trade_count"] > 0:
# REMOVED_UNUSED_CODE:                 markdown_msg += (
# REMOVED_UNUSED_CODE:                     f"\n*Avg. Duration:* `{avg_duration}`\n"
# REMOVED_UNUSED_CODE:                     f"*Best Performing:* `{best_pair}: {best_pair_profit_abs} "
# REMOVED_UNUSED_CODE:                     f"({best_pair_profit_ratio:.2%})`\n"
# REMOVED_UNUSED_CODE:                     f"*Trading volume:* `{fmt_coin(stats['trading_volume'], stake_cur)}`\n"
# REMOVED_UNUSED_CODE:                     f"*Profit factor:* `{stats['profit_factor']:.2f}`\n"
# REMOVED_UNUSED_CODE:                     f"*Max Drawdown:* `{stats['max_drawdown']:.2%} "
# REMOVED_UNUSED_CODE:                     f"({fmt_coin(stats['max_drawdown_abs'], stake_cur)})`\n"
# REMOVED_UNUSED_CODE:                     f"    from `{stats['max_drawdown_start']} "
# REMOVED_UNUSED_CODE:                     f"({fmt_coin(stats['drawdown_high'], stake_cur)})`\n"
# REMOVED_UNUSED_CODE:                     f"    to `{stats['max_drawdown_end']} "
# REMOVED_UNUSED_CODE:                     f"({fmt_coin(stats['drawdown_low'], stake_cur)})`\n"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:         await self._send_msg(
# REMOVED_UNUSED_CODE:             markdown_msg,
# REMOVED_UNUSED_CODE:             reload_able=True,
# REMOVED_UNUSED_CODE:             callback_path="update_profit",
# REMOVED_UNUSED_CODE:             query=update.callback_query,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _stats(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /stats
# REMOVED_UNUSED_CODE:         Show stats of recent trades
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         stats = self._rpc._rpc_stats()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         reason_map = {
# REMOVED_UNUSED_CODE:             "roi": "ROI",
# REMOVED_UNUSED_CODE:             "stop_loss": "Stoploss",
# REMOVED_UNUSED_CODE:             "trailing_stop_loss": "Trail. Stop",
# REMOVED_UNUSED_CODE:             "stoploss_on_exchange": "Stoploss",
# REMOVED_UNUSED_CODE:             "exit_signal": "Exit Signal",
# REMOVED_UNUSED_CODE:             "force_exit": "Force Exit",
# REMOVED_UNUSED_CODE:             "emergency_exit": "Emergency Exit",
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:         exit_reasons_tabulate = [
# REMOVED_UNUSED_CODE:             [reason_map.get(reason, reason), sum(count.values()), count["wins"], count["losses"]]
# REMOVED_UNUSED_CODE:             for reason, count in stats["exit_reasons"].items()
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         exit_reasons_msg = "No trades yet."
# REMOVED_UNUSED_CODE:         for reason in chunks(exit_reasons_tabulate, 25):
# REMOVED_UNUSED_CODE:             exit_reasons_msg = tabulate(reason, headers=["Exit Reason", "Exits", "Wins", "Losses"])
# REMOVED_UNUSED_CODE:             if len(exit_reasons_tabulate) > 25:
# REMOVED_UNUSED_CODE:                 await self._send_msg(f"```\n{exit_reasons_msg}```", ParseMode.MARKDOWN)
# REMOVED_UNUSED_CODE:                 exit_reasons_msg = ""
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         durations = stats["durations"]
# REMOVED_UNUSED_CODE:         duration_msg = tabulate(
# REMOVED_UNUSED_CODE:             [
# REMOVED_UNUSED_CODE:                 [
# REMOVED_UNUSED_CODE:                     "Wins",
# REMOVED_UNUSED_CODE:                     (
# REMOVED_UNUSED_CODE:                         str(timedelta(seconds=durations["wins"]))
# REMOVED_UNUSED_CODE:                         if durations["wins"] is not None
# REMOVED_UNUSED_CODE:                         else "N/A"
# REMOVED_UNUSED_CODE:                     ),
# REMOVED_UNUSED_CODE:                 ],
# REMOVED_UNUSED_CODE:                 [
# REMOVED_UNUSED_CODE:                     "Losses",
# REMOVED_UNUSED_CODE:                     (
# REMOVED_UNUSED_CODE:                         str(timedelta(seconds=durations["losses"]))
# REMOVED_UNUSED_CODE:                         if durations["losses"] is not None
# REMOVED_UNUSED_CODE:                         else "N/A"
# REMOVED_UNUSED_CODE:                     ),
# REMOVED_UNUSED_CODE:                 ],
# REMOVED_UNUSED_CODE:             ],
# REMOVED_UNUSED_CODE:             headers=["", "Avg. Duration"],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         msg = f"""```\n{exit_reasons_msg}```\n```\n{duration_msg}```"""
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         await self._send_msg(msg, ParseMode.MARKDOWN)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _balance(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """Handler for /balance"""
# REMOVED_UNUSED_CODE:         full_result = context.args and "full" in context.args
# REMOVED_UNUSED_CODE:         result = self._rpc._rpc_balance(
# REMOVED_UNUSED_CODE:             self._config["stake_currency"], self._config.get("fiat_display_currency", "")
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         balance_dust_level = self._config["telegram"].get("balance_dust_level", 0.0)
# REMOVED_UNUSED_CODE:         if not balance_dust_level:
# REMOVED_UNUSED_CODE:             balance_dust_level = DUST_PER_COIN.get(self._config["stake_currency"], 1.0)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         output = ""
# REMOVED_UNUSED_CODE:         if self._config["dry_run"]:
# REMOVED_UNUSED_CODE:             output += "*Warning:* Simulated balances in Dry Mode.\n"
# REMOVED_UNUSED_CODE:         starting_cap = fmt_coin(result["starting_capital"], self._config["stake_currency"])
# REMOVED_UNUSED_CODE:         output += f"Starting capital: `{starting_cap}`"
# REMOVED_UNUSED_CODE:         starting_cap_fiat = (
# REMOVED_UNUSED_CODE:             fmt_coin(result["starting_capital_fiat"], self._config["fiat_display_currency"])
# REMOVED_UNUSED_CODE:             if result["starting_capital_fiat"] > 0
# REMOVED_UNUSED_CODE:             else ""
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         output += (f" `, {starting_cap_fiat}`.\n") if result["starting_capital_fiat"] > 0 else ".\n"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         total_dust_balance = 0
# REMOVED_UNUSED_CODE:         total_dust_currencies = 0
# REMOVED_UNUSED_CODE:         for curr in result["currencies"]:
# REMOVED_UNUSED_CODE:             curr_output = ""
# REMOVED_UNUSED_CODE:             if (curr["is_position"] or curr["est_stake"] > balance_dust_level) and (
# REMOVED_UNUSED_CODE:                 full_result or curr["is_bot_managed"]
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 if curr["is_position"]:
# REMOVED_UNUSED_CODE:                     curr_output = (
# REMOVED_UNUSED_CODE:                         f"*{curr['currency']}:*\n"
# REMOVED_UNUSED_CODE:                         f"\t`{curr['side']}: {curr['position']:.8f}`\n"
# REMOVED_UNUSED_CODE:                         f"\t`Est. {curr['stake']}: "
# REMOVED_UNUSED_CODE:                         f"{fmt_coin(curr['est_stake'], curr['stake'], False)}`\n"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     est_stake = fmt_coin(
# REMOVED_UNUSED_CODE:                         curr["est_stake" if full_result else "est_stake_bot"], curr["stake"], False
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                     curr_output = (
# REMOVED_UNUSED_CODE:                         f"*{curr['currency']}:*\n"
# REMOVED_UNUSED_CODE:                         f"\t`Available: {curr['free']:.8f}`\n"
# REMOVED_UNUSED_CODE:                         f"\t`Balance: {curr['balance']:.8f}`\n"
# REMOVED_UNUSED_CODE:                         f"\t`Pending: {curr['used']:.8f}`\n"
# REMOVED_UNUSED_CODE:                         f"\t`Bot Owned: {curr['bot_owned']:.8f}`\n"
# REMOVED_UNUSED_CODE:                         f"\t`Est. {curr['stake']}: {est_stake}`\n"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             elif curr["est_stake"] <= balance_dust_level:
# REMOVED_UNUSED_CODE:                 total_dust_balance += curr["est_stake"]
# REMOVED_UNUSED_CODE:                 total_dust_currencies += 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Handle overflowing message length
# REMOVED_UNUSED_CODE:             if len(output + curr_output) >= MAX_MESSAGE_LENGTH:
# REMOVED_UNUSED_CODE:                 await self._send_msg(output)
# REMOVED_UNUSED_CODE:                 output = curr_output
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 output += curr_output
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if total_dust_balance > 0:
# REMOVED_UNUSED_CODE:             output += (
# REMOVED_UNUSED_CODE:                 f"*{total_dust_currencies} Other "
# REMOVED_UNUSED_CODE:                 f"{plural(total_dust_currencies, 'Currency', 'Currencies')} "
# REMOVED_UNUSED_CODE:                 f"(< {balance_dust_level} {result['stake']}):*\n"
# REMOVED_UNUSED_CODE:                 f"\t`Est. {result['stake']}: "
# REMOVED_UNUSED_CODE:                 f"{fmt_coin(total_dust_balance, result['stake'], False)}`\n"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         tc = result["trade_count"] > 0
# REMOVED_UNUSED_CODE:         stake_improve = f" `({result['starting_capital_ratio']:.2%})`" if tc else ""
# REMOVED_UNUSED_CODE:         fiat_val = f" `({result['starting_capital_fiat_ratio']:.2%})`" if tc else ""
# REMOVED_UNUSED_CODE:         value = fmt_coin(result["value" if full_result else "value_bot"], result["symbol"], False)
# REMOVED_UNUSED_CODE:         total_stake = fmt_coin(
# REMOVED_UNUSED_CODE:             result["total" if full_result else "total_bot"], result["stake"], False
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         output += (
# REMOVED_UNUSED_CODE:             f"\n*Estimated Value{' (Bot managed assets only)' if not full_result else ''}*:\n"
# REMOVED_UNUSED_CODE:             f"\t`{result['stake']}: {total_stake}`{stake_improve}\n"
# REMOVED_UNUSED_CODE:             f"\t`{result['symbol']}: {value}`{fiat_val}\n"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         await self._send_msg(
# REMOVED_UNUSED_CODE:             output, reload_able=True, callback_path="update_balance", query=update.callback_query
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _start(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /start.
# REMOVED_UNUSED_CODE:         Starts TradeThread
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         msg = self._rpc._rpc_start()
# REMOVED_UNUSED_CODE:         await self._send_msg(f"Status: `{msg['status']}`")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _stop(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /stop.
# REMOVED_UNUSED_CODE:         Stops TradeThread
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         msg = self._rpc._rpc_stop()
# REMOVED_UNUSED_CODE:         await self._send_msg(f"Status: `{msg['status']}`")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _reload_config(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /reload_config.
# REMOVED_UNUSED_CODE:         Triggers a config file reload
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         msg = self._rpc._rpc_reload_config()
# REMOVED_UNUSED_CODE:         await self._send_msg(f"Status: `{msg['status']}`")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _stopentry(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /stop_buy.
# REMOVED_UNUSED_CODE:         Sets max_open_trades to 0 and gracefully sells all open trades
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         msg = self._rpc._rpc_stopentry()
# REMOVED_UNUSED_CODE:         await self._send_msg(f"Status: `{msg['status']}`")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _reload_trade_from_exchange(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /reload_trade <tradeid>.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not context.args or len(context.args) == 0:
# REMOVED_UNUSED_CODE:             raise RPCException("Trade-id not set.")
# REMOVED_UNUSED_CODE:         trade_id = int(context.args[0])
# REMOVED_UNUSED_CODE:         msg = self._rpc._rpc_reload_trade_from_exchange(trade_id)
# REMOVED_UNUSED_CODE:         await self._send_msg(f"Status: `{msg['status']}`")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _force_exit(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /forceexit <id>.
# REMOVED_UNUSED_CODE:         Sells the given trade at current price
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if context.args:
# REMOVED_UNUSED_CODE:             trade_id = context.args[0]
# REMOVED_UNUSED_CODE:             await self._force_exit_action(trade_id)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             fiat_currency = self._config.get("fiat_display_currency", "")
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 statlist, _, _, _ = self._rpc._rpc_status_table(
# REMOVED_UNUSED_CODE:                     self._config["stake_currency"], fiat_currency
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             except RPCException:
# REMOVED_UNUSED_CODE:                 await self._send_msg(msg="No open trade found.")
# REMOVED_UNUSED_CODE:                 return
# REMOVED_UNUSED_CODE:             trades = []
# REMOVED_UNUSED_CODE:             for trade in statlist:
# REMOVED_UNUSED_CODE:                 trades.append((trade[0], f"{trade[0]} {trade[1]} {trade[2]} {trade[3]}"))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             trade_buttons = [
# REMOVED_UNUSED_CODE:                 InlineKeyboardButton(text=trade[1], callback_data=f"force_exit__{trade[0]}")
# REMOVED_UNUSED_CODE:                 for trade in trades
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE:             buttons_aligned = self._layout_inline_keyboard(trade_buttons, cols=1)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             buttons_aligned.append(
# REMOVED_UNUSED_CODE:                 [InlineKeyboardButton(text="Cancel", callback_data="force_exit__cancel")]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             await self._send_msg(msg="Which trade?", keyboard=buttons_aligned)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _force_exit_action(self, trade_id: str):
# REMOVED_UNUSED_CODE:         if trade_id != "cancel":
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 loop = asyncio.get_running_loop()
# REMOVED_UNUSED_CODE:                 # Workaround to avoid nested loops
# REMOVED_UNUSED_CODE:                 await loop.run_in_executor(None, safe_async_db(self._rpc._rpc_force_exit), trade_id)
# REMOVED_UNUSED_CODE:             except RPCException as e:
# REMOVED_UNUSED_CODE:                 await self._send_msg(str(e))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _force_exit_inline(self, update: Update, _: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         if update.callback_query:
# REMOVED_UNUSED_CODE:             query = update.callback_query
# REMOVED_UNUSED_CODE:             if query.data and "__" in query.data:
# REMOVED_UNUSED_CODE:                 # Input data is "force_exit__<tradid|cancel>"
# REMOVED_UNUSED_CODE:                 trade_id = query.data.split("__")[1].split(" ")[0]
# REMOVED_UNUSED_CODE:                 if trade_id == "cancel":
# REMOVED_UNUSED_CODE:                     await query.answer()
# REMOVED_UNUSED_CODE:                     await query.edit_message_text(text="Force exit canceled.")
# REMOVED_UNUSED_CODE:                     return
# REMOVED_UNUSED_CODE:                 trade: Trade | None = Trade.get_trades(trade_filter=Trade.id == trade_id).first()
# REMOVED_UNUSED_CODE:                 await query.answer()
# REMOVED_UNUSED_CODE:                 if trade:
# REMOVED_UNUSED_CODE:                     await query.edit_message_text(
# REMOVED_UNUSED_CODE:                         text=f"Manually exiting Trade #{trade_id}, {trade.pair}"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     await self._force_exit_action(trade_id)
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     await query.edit_message_text(text=f"Trade {trade_id} not found.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _force_enter_action(self, pair, price: float | None, order_side: SignalDirection):
# REMOVED_UNUSED_CODE:         if pair != "cancel":
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 @safe_async_db
# REMOVED_UNUSED_CODE:                 def _force_enter():
# REMOVED_UNUSED_CODE:                     self._rpc._rpc_force_entry(pair, price, order_side=order_side)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 loop = asyncio.get_running_loop()
# REMOVED_UNUSED_CODE:                 # Workaround to avoid nested loops
# REMOVED_UNUSED_CODE:                 await loop.run_in_executor(None, _force_enter)
# REMOVED_UNUSED_CODE:             except RPCException as e:
# REMOVED_UNUSED_CODE:                 logger.exception("Forcebuy error!")
# REMOVED_UNUSED_CODE:                 await self._send_msg(str(e), ParseMode.HTML)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _force_enter_inline(self, update: Update, _: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         if update.callback_query:
# REMOVED_UNUSED_CODE:             query = update.callback_query
# REMOVED_UNUSED_CODE:             if query.data and "__" in query.data:
# REMOVED_UNUSED_CODE:                 # Input data is "force_enter__<pair|cancel>_<side>"
# REMOVED_UNUSED_CODE:                 payload = query.data.split("__")[1]
# REMOVED_UNUSED_CODE:                 if payload == "cancel":
# REMOVED_UNUSED_CODE:                     await query.answer()
# REMOVED_UNUSED_CODE:                     await query.edit_message_text(text="Force enter canceled.")
# REMOVED_UNUSED_CODE:                     return
# REMOVED_UNUSED_CODE:                 if payload and "_||_" in payload:
# REMOVED_UNUSED_CODE:                     pair, side = payload.split("_||_")
# REMOVED_UNUSED_CODE:                     order_side = SignalDirection(side)
# REMOVED_UNUSED_CODE:                     await query.answer()
# REMOVED_UNUSED_CODE:                     await query.edit_message_text(text=f"Manually entering {order_side} for {pair}")
# REMOVED_UNUSED_CODE:                     await self._force_enter_action(pair, None, order_side)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def _layout_inline_keyboard(
# REMOVED_UNUSED_CODE:         buttons: list[InlineKeyboardButton], cols=3
# REMOVED_UNUSED_CODE:     ) -> list[list[InlineKeyboardButton]]:
# REMOVED_UNUSED_CODE:         return [buttons[i : i + cols] for i in range(0, len(buttons), cols)]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _force_enter(
# REMOVED_UNUSED_CODE:         self, update: Update, context: CallbackContext, order_side: SignalDirection
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /forcelong <asset> <price> and `/forceshort <asset> <price>
# REMOVED_UNUSED_CODE:         Buys a pair trade at the given or current price
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if context.args:
# REMOVED_UNUSED_CODE:             pair = context.args[0]
# REMOVED_UNUSED_CODE:             price = float(context.args[1]) if len(context.args) > 1 else None
# REMOVED_UNUSED_CODE:             await self._force_enter_action(pair, price, order_side)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             whitelist = self._rpc._rpc_whitelist()["whitelist"]
# REMOVED_UNUSED_CODE:             pair_buttons = [
# REMOVED_UNUSED_CODE:                 InlineKeyboardButton(
# REMOVED_UNUSED_CODE:                     text=pair, callback_data=f"force_enter__{pair}_||_{order_side}"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 for pair in sorted(whitelist)
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE:             buttons_aligned = self._layout_inline_keyboard(pair_buttons)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             buttons_aligned.append(
# REMOVED_UNUSED_CODE:                 [InlineKeyboardButton(text="Cancel", callback_data="force_enter__cancel")]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             await self._send_msg(
# REMOVED_UNUSED_CODE:                 msg="Which pair?", keyboard=buttons_aligned, query=update.callback_query
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _trades(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /trades <n>
# REMOVED_UNUSED_CODE:         Returns last n recent trades.
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         stake_cur = self._config["stake_currency"]
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             nrecent = int(context.args[0]) if context.args else 10
# REMOVED_UNUSED_CODE:         except (TypeError, ValueError, IndexError):
# REMOVED_UNUSED_CODE:             nrecent = 10
# REMOVED_UNUSED_CODE:         nonspot = self._config.get("trading_mode", TradingMode.SPOT) != TradingMode.SPOT
# REMOVED_UNUSED_CODE:         trades = self._rpc._rpc_trade_history(nrecent)
# REMOVED_UNUSED_CODE:         trades_tab = tabulate(
# REMOVED_UNUSED_CODE:             [
# REMOVED_UNUSED_CODE:                 [
# REMOVED_UNUSED_CODE:                     dt_humanize_delta(dt_from_ts(trade["close_timestamp"])),
# REMOVED_UNUSED_CODE:                     f"{trade['pair']} (#{trade['trade_id']}"
# REMOVED_UNUSED_CODE:                     f"{(' ' + ('S' if trade['is_short'] else 'L')) if nonspot else ''})",
# REMOVED_UNUSED_CODE:                     f"{(trade['close_profit']):.2%} ({trade['close_profit_abs']})",
# REMOVED_UNUSED_CODE:                 ]
# REMOVED_UNUSED_CODE:                 for trade in trades["trades"]
# REMOVED_UNUSED_CODE:             ],
# REMOVED_UNUSED_CODE:             headers=[
# REMOVED_UNUSED_CODE:                 "Close Date",
# REMOVED_UNUSED_CODE:                 "Pair (ID L/S)" if nonspot else "Pair (ID)",
# REMOVED_UNUSED_CODE:                 f"Profit ({stake_cur})",
# REMOVED_UNUSED_CODE:             ],
# REMOVED_UNUSED_CODE:             tablefmt="simple",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         message = f"<b>{min(trades['trades_count'], nrecent)} recent trades</b>:\n" + (
# REMOVED_UNUSED_CODE:             f"<pre>{trades_tab}</pre>" if trades["trades_count"] > 0 else ""
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         await self._send_msg(message, parse_mode=ParseMode.HTML)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _delete_trade(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /delete <id>.
# REMOVED_UNUSED_CODE:         Delete the given trade
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not context.args or len(context.args) == 0:
# REMOVED_UNUSED_CODE:             raise RPCException("Trade-id not set.")
# REMOVED_UNUSED_CODE:         trade_id = int(context.args[0])
# REMOVED_UNUSED_CODE:         msg = self._rpc._rpc_delete(trade_id)
# REMOVED_UNUSED_CODE:         await self._send_msg(
# REMOVED_UNUSED_CODE:             f"`{msg['result_msg']}`\n"
# REMOVED_UNUSED_CODE:             "Please make sure to take care of this asset on the exchange manually."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _cancel_open_order(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /cancel_open_order <id>.
# REMOVED_UNUSED_CODE:         Cancel open order for tradeid
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not context.args or len(context.args) == 0:
# REMOVED_UNUSED_CODE:             raise RPCException("Trade-id not set.")
# REMOVED_UNUSED_CODE:         trade_id = int(context.args[0])
# REMOVED_UNUSED_CODE:         self._rpc._rpc_cancel_open_order(trade_id)
# REMOVED_UNUSED_CODE:         await self._send_msg("Open order canceled.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _performance(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /performance.
# REMOVED_UNUSED_CODE:         Shows a performance statistic from finished trades
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         trades = self._rpc._rpc_performance()
# REMOVED_UNUSED_CODE:         output = "<b>Performance:</b>\n"
# REMOVED_UNUSED_CODE:         for i, trade in enumerate(trades):
# REMOVED_UNUSED_CODE:             stat_line = (
# REMOVED_UNUSED_CODE:                 f"{i + 1}.\t <code>{trade['pair']}\t"
# REMOVED_UNUSED_CODE:                 f"{fmt_coin(trade['profit_abs'], self._config['stake_currency'])} "
# REMOVED_UNUSED_CODE:                 f"({trade['profit_ratio']:.2%}) "
# REMOVED_UNUSED_CODE:                 f"({trade['count']})</code>\n"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if len(output + stat_line) >= MAX_MESSAGE_LENGTH:
# REMOVED_UNUSED_CODE:                 await self._send_msg(output, parse_mode=ParseMode.HTML)
# REMOVED_UNUSED_CODE:                 output = stat_line
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 output += stat_line
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         await self._send_msg(
# REMOVED_UNUSED_CODE:             output,
# REMOVED_UNUSED_CODE:             parse_mode=ParseMode.HTML,
# REMOVED_UNUSED_CODE:             reload_able=True,
# REMOVED_UNUSED_CODE:             callback_path="update_performance",
# REMOVED_UNUSED_CODE:             query=update.callback_query,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _enter_tag_performance(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /entries PAIR .
# REMOVED_UNUSED_CODE:         Shows a performance statistic from finished trades
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         pair = None
# REMOVED_UNUSED_CODE:         if context.args and isinstance(context.args[0], str):
# REMOVED_UNUSED_CODE:             pair = context.args[0]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trades = self._rpc._rpc_enter_tag_performance(pair)
# REMOVED_UNUSED_CODE:         output = "*Entry Tag Performance:*\n"
# REMOVED_UNUSED_CODE:         for i, trade in enumerate(trades):
# REMOVED_UNUSED_CODE:             stat_line = (
# REMOVED_UNUSED_CODE:                 f"{i + 1}.\t `{trade['enter_tag']}\t"
# REMOVED_UNUSED_CODE:                 f"{fmt_coin(trade['profit_abs'], self._config['stake_currency'])} "
# REMOVED_UNUSED_CODE:                 f"({trade['profit_ratio']:.2%}) "
# REMOVED_UNUSED_CODE:                 f"({trade['count']})`\n"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if len(output + stat_line) >= MAX_MESSAGE_LENGTH:
# REMOVED_UNUSED_CODE:                 await self._send_msg(output, parse_mode=ParseMode.MARKDOWN)
# REMOVED_UNUSED_CODE:                 output = stat_line
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 output += stat_line
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         await self._send_msg(
# REMOVED_UNUSED_CODE:             output,
# REMOVED_UNUSED_CODE:             parse_mode=ParseMode.MARKDOWN,
# REMOVED_UNUSED_CODE:             reload_able=True,
# REMOVED_UNUSED_CODE:             callback_path="update_enter_tag_performance",
# REMOVED_UNUSED_CODE:             query=update.callback_query,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _exit_reason_performance(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /exits.
# REMOVED_UNUSED_CODE:         Shows a performance statistic from finished trades
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         pair = None
# REMOVED_UNUSED_CODE:         if context.args and isinstance(context.args[0], str):
# REMOVED_UNUSED_CODE:             pair = context.args[0]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trades = self._rpc._rpc_exit_reason_performance(pair)
# REMOVED_UNUSED_CODE:         output = "*Exit Reason Performance:*\n"
# REMOVED_UNUSED_CODE:         for i, trade in enumerate(trades):
# REMOVED_UNUSED_CODE:             stat_line = (
# REMOVED_UNUSED_CODE:                 f"{i + 1}.\t `{trade['exit_reason']}\t"
# REMOVED_UNUSED_CODE:                 f"{fmt_coin(trade['profit_abs'], self._config['stake_currency'])} "
# REMOVED_UNUSED_CODE:                 f"({trade['profit_ratio']:.2%}) "
# REMOVED_UNUSED_CODE:                 f"({trade['count']})`\n"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if len(output + stat_line) >= MAX_MESSAGE_LENGTH:
# REMOVED_UNUSED_CODE:                 await self._send_msg(output, parse_mode=ParseMode.MARKDOWN)
# REMOVED_UNUSED_CODE:                 output = stat_line
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 output += stat_line
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         await self._send_msg(
# REMOVED_UNUSED_CODE:             output,
# REMOVED_UNUSED_CODE:             parse_mode=ParseMode.MARKDOWN,
# REMOVED_UNUSED_CODE:             reload_able=True,
# REMOVED_UNUSED_CODE:             callback_path="update_exit_reason_performance",
# REMOVED_UNUSED_CODE:             query=update.callback_query,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _mix_tag_performance(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /mix_tags.
# REMOVED_UNUSED_CODE:         Shows a performance statistic from finished trades
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         pair = None
# REMOVED_UNUSED_CODE:         if context.args and isinstance(context.args[0], str):
# REMOVED_UNUSED_CODE:             pair = context.args[0]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trades = self._rpc._rpc_mix_tag_performance(pair)
# REMOVED_UNUSED_CODE:         output = "*Mix Tag Performance:*\n"
# REMOVED_UNUSED_CODE:         for i, trade in enumerate(trades):
# REMOVED_UNUSED_CODE:             stat_line = (
# REMOVED_UNUSED_CODE:                 f"{i + 1}.\t `{trade['mix_tag']}\t"
# REMOVED_UNUSED_CODE:                 f"{fmt_coin(trade['profit_abs'], self._config['stake_currency'])} "
# REMOVED_UNUSED_CODE:                 f"({trade['profit_ratio']:.2%}) "
# REMOVED_UNUSED_CODE:                 f"({trade['count']})`\n"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if len(output + stat_line) >= MAX_MESSAGE_LENGTH:
# REMOVED_UNUSED_CODE:                 await self._send_msg(output, parse_mode=ParseMode.MARKDOWN)
# REMOVED_UNUSED_CODE:                 output = stat_line
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 output += stat_line
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         await self._send_msg(
# REMOVED_UNUSED_CODE:             output,
# REMOVED_UNUSED_CODE:             parse_mode=ParseMode.MARKDOWN,
# REMOVED_UNUSED_CODE:             reload_able=True,
# REMOVED_UNUSED_CODE:             callback_path="update_mix_tag_performance",
# REMOVED_UNUSED_CODE:             query=update.callback_query,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _count(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /count.
# REMOVED_UNUSED_CODE:         Returns the number of trades running
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         counts = self._rpc._rpc_count()
# REMOVED_UNUSED_CODE:         message = tabulate(
# REMOVED_UNUSED_CODE:             {k: [v] for k, v in counts.items()},
# REMOVED_UNUSED_CODE:             headers=["current", "max", "total stake"],
# REMOVED_UNUSED_CODE:             tablefmt="simple",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         message = f"<pre>{message}</pre>"
# REMOVED_UNUSED_CODE:         logger.debug(message)
# REMOVED_UNUSED_CODE:         await self._send_msg(
# REMOVED_UNUSED_CODE:             message,
# REMOVED_UNUSED_CODE:             parse_mode=ParseMode.HTML,
# REMOVED_UNUSED_CODE:             reload_able=True,
# REMOVED_UNUSED_CODE:             callback_path="update_count",
# REMOVED_UNUSED_CODE:             query=update.callback_query,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _locks(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /locks.
# REMOVED_UNUSED_CODE:         Returns the currently active locks
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         rpc_locks = self._rpc._rpc_locks()
# REMOVED_UNUSED_CODE:         if not rpc_locks["locks"]:
# REMOVED_UNUSED_CODE:             await self._send_msg("No active locks.", parse_mode=ParseMode.HTML)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for locks in chunks(rpc_locks["locks"], 25):
# REMOVED_UNUSED_CODE:             message = tabulate(
# REMOVED_UNUSED_CODE:                 [
# REMOVED_UNUSED_CODE:                     [lock["id"], lock["pair"], lock["lock_end_time"], lock["reason"]]
# REMOVED_UNUSED_CODE:                     for lock in locks
# REMOVED_UNUSED_CODE:                 ],
# REMOVED_UNUSED_CODE:                 headers=["ID", "Pair", "Until", "Reason"],
# REMOVED_UNUSED_CODE:                 tablefmt="simple",
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             message = f"<pre>{escape(message)}</pre>"
# REMOVED_UNUSED_CODE:             logger.debug(message)
# REMOVED_UNUSED_CODE:             await self._send_msg(message, parse_mode=ParseMode.HTML)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _delete_locks(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /delete_locks.
# REMOVED_UNUSED_CODE:         Returns the currently active locks
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         arg = context.args[0] if context.args and len(context.args) > 0 else None
# REMOVED_UNUSED_CODE:         lockid = None
# REMOVED_UNUSED_CODE:         pair = None
# REMOVED_UNUSED_CODE:         if arg:
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 lockid = int(arg)
# REMOVED_UNUSED_CODE:             except ValueError:
# REMOVED_UNUSED_CODE:                 pair = arg
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._rpc._rpc_delete_lock(lockid=lockid, pair=pair)
# REMOVED_UNUSED_CODE:         await self._locks(update, context)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _whitelist(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /whitelist
# REMOVED_UNUSED_CODE:         Shows the currently active whitelist
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         whitelist = self._rpc._rpc_whitelist()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if context.args:
# REMOVED_UNUSED_CODE:             if "sorted" in context.args:
# REMOVED_UNUSED_CODE:                 whitelist["whitelist"] = sorted(whitelist["whitelist"])
# REMOVED_UNUSED_CODE:             if "baseonly" in context.args:
# REMOVED_UNUSED_CODE:                 whitelist["whitelist"] = [pair.split("/")[0] for pair in whitelist["whitelist"]]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         message = f"Using whitelist `{whitelist['method']}` with {whitelist['length']} pairs\n"
# REMOVED_UNUSED_CODE:         message += f"`{', '.join(whitelist['whitelist'])}`"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.debug(message)
# REMOVED_UNUSED_CODE:         await self._send_msg(message)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _blacklist(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /blacklist
# REMOVED_UNUSED_CODE:         Shows the currently active blacklist
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         await self.send_blacklist_msg(self._rpc._rpc_blacklist(context.args))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def send_blacklist_msg(self, blacklist: dict):
# REMOVED_UNUSED_CODE:         errmsgs = []
# REMOVED_UNUSED_CODE:         for _, error in blacklist["errors"].items():
# REMOVED_UNUSED_CODE:             errmsgs.append(f"Error: {error['error_msg']}")
# REMOVED_UNUSED_CODE:         if errmsgs:
# REMOVED_UNUSED_CODE:             await self._send_msg("\n".join(errmsgs))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         message = f"Blacklist contains {blacklist['length']} pairs\n"
# REMOVED_UNUSED_CODE:         message += f"`{', '.join(blacklist['blacklist'])}`"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.debug(message)
# REMOVED_UNUSED_CODE:         await self._send_msg(message)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _blacklist_delete(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /bl_delete
# REMOVED_UNUSED_CODE:         Deletes pair(s) from current blacklist
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         await self.send_blacklist_msg(self._rpc._rpc_blacklist_delete(context.args or []))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _logs(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /logs
# REMOVED_UNUSED_CODE:         Shows the latest logs
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             limit = int(context.args[0]) if context.args else 10
# REMOVED_UNUSED_CODE:         except (TypeError, ValueError, IndexError):
# REMOVED_UNUSED_CODE:             limit = 10
# REMOVED_UNUSED_CODE:         logs = RPC._rpc_get_logs(limit)["logs"]
# REMOVED_UNUSED_CODE:         msgs = ""
# REMOVED_UNUSED_CODE:         msg_template = "*{}* {}: {} \\- `{}`"
# REMOVED_UNUSED_CODE:         for logrec in logs:
# REMOVED_UNUSED_CODE:             msg = msg_template.format(
# REMOVED_UNUSED_CODE:                 escape_markdown(logrec[0], version=2),
# REMOVED_UNUSED_CODE:                 escape_markdown(logrec[2], version=2),
# REMOVED_UNUSED_CODE:                 escape_markdown(logrec[3], version=2),
# REMOVED_UNUSED_CODE:                 escape_markdown(logrec[4], version=2),
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             if len(msgs + msg) + 10 >= MAX_MESSAGE_LENGTH:
# REMOVED_UNUSED_CODE:                 # Send message immediately if it would become too long
# REMOVED_UNUSED_CODE:                 await self._send_msg(msgs, parse_mode=ParseMode.MARKDOWN_V2)
# REMOVED_UNUSED_CODE:                 msgs = msg + "\n"
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 # Append message to messages to send
# REMOVED_UNUSED_CODE:                 msgs += msg + "\n"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if msgs:
# REMOVED_UNUSED_CODE:             await self._send_msg(msgs, parse_mode=ParseMode.MARKDOWN_V2)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _edge(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /edge
# REMOVED_UNUSED_CODE:         Shows information related to Edge
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         edge_pairs = self._rpc._rpc_edge()
# REMOVED_UNUSED_CODE:         if not edge_pairs:
# REMOVED_UNUSED_CODE:             message = "<b>Edge only validated following pairs:</b>"
# REMOVED_UNUSED_CODE:             await self._send_msg(message, parse_mode=ParseMode.HTML)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for chunk in chunks(edge_pairs, 25):
# REMOVED_UNUSED_CODE:             edge_pairs_tab = tabulate(chunk, headers="keys", tablefmt="simple")
# REMOVED_UNUSED_CODE:             message = f"<b>Edge only validated following pairs:</b>\n<pre>{edge_pairs_tab}</pre>"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             await self._send_msg(message, parse_mode=ParseMode.HTML)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _help(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /help.
# REMOVED_UNUSED_CODE:         Show commands of the bot
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         force_enter_text = (
# REMOVED_UNUSED_CODE:             "*/forcelong <pair> [<rate>]:* `Instantly buys the given pair. "
# REMOVED_UNUSED_CODE:             "Optionally takes a rate at which to buy "
# REMOVED_UNUSED_CODE:             "(only applies to limit orders).` \n"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         if self._rpc._freqtrade.trading_mode != TradingMode.SPOT:
# REMOVED_UNUSED_CODE:             force_enter_text += (
# REMOVED_UNUSED_CODE:                 "*/forceshort <pair> [<rate>]:* `Instantly shorts the given pair. "
# REMOVED_UNUSED_CODE:                 "Optionally takes a rate at which to sell "
# REMOVED_UNUSED_CODE:                 "(only applies to limit orders).` \n"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         message = (
# REMOVED_UNUSED_CODE:             "_Bot Control_\n"
# REMOVED_UNUSED_CODE:             "------------\n"
# REMOVED_UNUSED_CODE:             "*/start:* `Starts the trader`\n"
# REMOVED_UNUSED_CODE:             "*/stop:* `Stops the trader`\n"
# REMOVED_UNUSED_CODE:             "*/stopentry:* `Stops entering, but handles open trades gracefully` \n"
# REMOVED_UNUSED_CODE:             "*/forceexit <trade_id>|all:* `Instantly exits the given trade or all trades, "
# REMOVED_UNUSED_CODE:             "regardless of profit`\n"
# REMOVED_UNUSED_CODE:             "*/fx <trade_id>|all:* `Alias to /forceexit`\n"
# REMOVED_UNUSED_CODE:             f"{force_enter_text if self._config.get('force_entry_enable', False) else ''}"
# REMOVED_UNUSED_CODE:             "*/delete <trade_id>:* `Instantly delete the given trade in the database`\n"
# REMOVED_UNUSED_CODE:             "*/reload_trade <trade_id>:* `Reload trade from exchange Orders`\n"
# REMOVED_UNUSED_CODE:             "*/cancel_open_order <trade_id>:* `Cancels open orders for trade. "
# REMOVED_UNUSED_CODE:             "Only valid when the trade has open orders.`\n"
# REMOVED_UNUSED_CODE:             "*/coo <trade_id>|all:* `Alias to /cancel_open_order`\n"
# REMOVED_UNUSED_CODE:             "*/whitelist [sorted] [baseonly]:* `Show current whitelist. Optionally in "
# REMOVED_UNUSED_CODE:             "order and/or only displaying the base currency of each pairing.`\n"
# REMOVED_UNUSED_CODE:             "*/blacklist [pair]:* `Show current blacklist, or adds one or more pairs "
# REMOVED_UNUSED_CODE:             "to the blacklist.` \n"
# REMOVED_UNUSED_CODE:             "*/blacklist_delete [pairs]| /bl_delete [pairs]:* "
# REMOVED_UNUSED_CODE:             "`Delete pair / pattern from blacklist. Will reset on reload_conf.` \n"
# REMOVED_UNUSED_CODE:             "*/reload_config:* `Reload configuration file` \n"
# REMOVED_UNUSED_CODE:             "*/unlock <pair|id>:* `Unlock this Pair (or this lock id if it's numeric)`\n"
# REMOVED_UNUSED_CODE:             "_Current state_\n"
# REMOVED_UNUSED_CODE:             "------------\n"
# REMOVED_UNUSED_CODE:             "*/show_config:* `Show running configuration` \n"
# REMOVED_UNUSED_CODE:             "*/locks:* `Show currently locked pairs`\n"
# REMOVED_UNUSED_CODE:             "*/balance:* `Show bot managed balance per currency`\n"
# REMOVED_UNUSED_CODE:             "*/balance total:* `Show account balance per currency`\n"
# REMOVED_UNUSED_CODE:             "*/logs [limit]:* `Show latest logs - defaults to 10` \n"
# REMOVED_UNUSED_CODE:             "*/count:* `Show number of active trades compared to allowed number of trades`\n"
# REMOVED_UNUSED_CODE:             "*/edge:* `Shows validated pairs by Edge if it is enabled` \n"
# REMOVED_UNUSED_CODE:             "*/health* `Show latest process timestamp - defaults to 1970-01-01 00:00:00` \n"
# REMOVED_UNUSED_CODE:             "*/marketdir [long | short | even | none]:* `Updates the user managed variable "
# REMOVED_UNUSED_CODE:             "that represents the current market direction. If no direction is provided `"
# REMOVED_UNUSED_CODE:             "`the currently set market direction will be output.` \n"
# REMOVED_UNUSED_CODE:             "*/list_custom_data <trade_id> <key>:* `List custom_data for Trade ID & Key combo.`\n"
# REMOVED_UNUSED_CODE:             "`If no Key is supplied it will list all key-value pairs found for that Trade ID.`\n"
# REMOVED_UNUSED_CODE:             "_Statistics_\n"
# REMOVED_UNUSED_CODE:             "------------\n"
# REMOVED_UNUSED_CODE:             "*/status <trade_id>|[table]:* `Lists all open trades`\n"
# REMOVED_UNUSED_CODE:             "         *<trade_id> :* `Lists one or more specific trades.`\n"
# REMOVED_UNUSED_CODE:             "                        `Separate multiple <trade_id> with a blank space.`\n"
# REMOVED_UNUSED_CODE:             "         *table :* `will display trades in a table`\n"
# REMOVED_UNUSED_CODE:             "                `pending buy orders are marked with an asterisk (*)`\n"
# REMOVED_UNUSED_CODE:             "                `pending sell orders are marked with a double asterisk (**)`\n"
# REMOVED_UNUSED_CODE:             "*/entries <pair|none>:* `Shows the enter_tag performance`\n"
# REMOVED_UNUSED_CODE:             "*/exits <pair|none>:* `Shows the exit reason performance`\n"
# REMOVED_UNUSED_CODE:             "*/mix_tags <pair|none>:* `Shows combined entry tag + exit reason performance`\n"
# REMOVED_UNUSED_CODE:             "*/trades [limit]:* `Lists last closed trades (limited to 10 by default)`\n"
# REMOVED_UNUSED_CODE:             "*/profit [<n>]:* `Lists cumulative profit from all finished trades, "
# REMOVED_UNUSED_CODE:             "over the last n days`\n"
# REMOVED_UNUSED_CODE:             "*/performance:* `Show performance of each finished trade grouped by pair`\n"
# REMOVED_UNUSED_CODE:             "*/daily <n>:* `Shows profit or loss per day, over the last n days`\n"
# REMOVED_UNUSED_CODE:             "*/weekly <n>:* `Shows statistics per week, over the last n weeks`\n"
# REMOVED_UNUSED_CODE:             "*/monthly <n>:* `Shows statistics per month, over the last n months`\n"
# REMOVED_UNUSED_CODE:             "*/stats:* `Shows Wins / losses by Sell reason as well as "
# REMOVED_UNUSED_CODE:             "Avg. holding durations for buys and sells.`\n"
# REMOVED_UNUSED_CODE:             "*/help:* `This help message`\n"
# REMOVED_UNUSED_CODE:             "*/version:* `Show version`\n"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         await self._send_msg(message, parse_mode=ParseMode.MARKDOWN)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _health(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /health
# REMOVED_UNUSED_CODE:         Shows the last process timestamp
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         health = self._rpc.health()
# REMOVED_UNUSED_CODE:         message = f"Last process: `{health['last_process_loc']}`\n"
# REMOVED_UNUSED_CODE:         message += f"Initial bot start: `{health['bot_start_loc']}`\n"
# REMOVED_UNUSED_CODE:         message += f"Last bot restart: `{health['bot_startup_loc']}`"
# REMOVED_UNUSED_CODE:         await self._send_msg(message)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _version(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /version.
# REMOVED_UNUSED_CODE:         Show version information
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         strategy_version = self._rpc._freqtrade.strategy.version()
# REMOVED_UNUSED_CODE:         version_string = f"*Version:* `{__version__}`"
# REMOVED_UNUSED_CODE:         if strategy_version is not None:
# REMOVED_UNUSED_CODE:             version_string += f"\n*Strategy version: * `{strategy_version}`"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         await self._send_msg(version_string)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _show_config(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /show_config.
# REMOVED_UNUSED_CODE:         Show config information information
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         val = RPC._rpc_show_config(self._config, self._rpc._freqtrade.state)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if val["trailing_stop"]:
# REMOVED_UNUSED_CODE:             sl_info = (
# REMOVED_UNUSED_CODE:                 f"*Initial Stoploss:* `{val['stoploss']}`\n"
# REMOVED_UNUSED_CODE:                 f"*Trailing stop positive:* `{val['trailing_stop_positive']}`\n"
# REMOVED_UNUSED_CODE:                 f"*Trailing stop offset:* `{val['trailing_stop_positive_offset']}`\n"
# REMOVED_UNUSED_CODE:                 f"*Only trail above offset:* `{val['trailing_only_offset_is_reached']}`\n"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             sl_info = f"*Stoploss:* `{val['stoploss']}`\n"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if val["position_adjustment_enable"]:
# REMOVED_UNUSED_CODE:             pa_info = (
# REMOVED_UNUSED_CODE:                 f"*Position adjustment:* On\n"
# REMOVED_UNUSED_CODE:                 f"*Max enter position adjustment:* `{val['max_entry_position_adjustment']}`\n"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             pa_info = "*Position adjustment:* Off\n"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         await self._send_msg(
# REMOVED_UNUSED_CODE:             f"*Mode:* `{'Dry-run' if val['dry_run'] else 'Live'}`\n"
# REMOVED_UNUSED_CODE:             f"*Exchange:* `{val['exchange']}`\n"
# REMOVED_UNUSED_CODE:             f"*Market: * `{val['trading_mode']}`\n"
# REMOVED_UNUSED_CODE:             f"*Stake per trade:* `{val['stake_amount']} {val['stake_currency']}`\n"
# REMOVED_UNUSED_CODE:             f"*Max open Trades:* `{val['max_open_trades']}`\n"
# REMOVED_UNUSED_CODE:             f"*Minimum ROI:* `{val['minimal_roi']}`\n"
# REMOVED_UNUSED_CODE:             f"*Entry strategy:* ```\n{json.dumps(val['entry_pricing'])}```\n"
# REMOVED_UNUSED_CODE:             f"*Exit strategy:* ```\n{json.dumps(val['exit_pricing'])}```\n"
# REMOVED_UNUSED_CODE:             f"{sl_info}"
# REMOVED_UNUSED_CODE:             f"{pa_info}"
# REMOVED_UNUSED_CODE:             f"*Timeframe:* `{val['timeframe']}`\n"
# REMOVED_UNUSED_CODE:             f"*Strategy:* `{val['strategy']}`\n"
# REMOVED_UNUSED_CODE:             f"*Current state:* `{val['state']}`"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _list_custom_data(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /list_custom_data <id> <key>.
# REMOVED_UNUSED_CODE:         List custom_data for specified trade (and key if supplied).
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             if not context.args or len(context.args) == 0:
# REMOVED_UNUSED_CODE:                 raise RPCException("Trade-id not set.")
# REMOVED_UNUSED_CODE:             trade_id = int(context.args[0])
# REMOVED_UNUSED_CODE:             key = None if len(context.args) < 2 else str(context.args[1])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             results = self._rpc._rpc_list_custom_data(trade_id, key)
# REMOVED_UNUSED_CODE:             messages = []
# REMOVED_UNUSED_CODE:             if len(results) > 0:
# REMOVED_UNUSED_CODE:                 messages.append("Found custom-data entr" + ("ies: " if len(results) > 1 else "y: "))
# REMOVED_UNUSED_CODE:                 for result in results:
# REMOVED_UNUSED_CODE:                     lines = [
# REMOVED_UNUSED_CODE:                         f"*Key:* `{result['cd_key']}`",
# REMOVED_UNUSED_CODE:                         f"*ID:* `{result['id']}`",
# REMOVED_UNUSED_CODE:                         f"*Trade ID:* `{result['ft_trade_id']}`",
# REMOVED_UNUSED_CODE:                         f"*Type:* `{result['cd_type']}`",
# REMOVED_UNUSED_CODE:                         f"*Value:* `{result['cd_value']}`",
# REMOVED_UNUSED_CODE:                         f"*Create Date:* `{format_date(result['created_at'])}`",
# REMOVED_UNUSED_CODE:                         f"*Update Date:* `{format_date(result['updated_at'])}`",
# REMOVED_UNUSED_CODE:                     ]
# REMOVED_UNUSED_CODE:                     # Filter empty lines using list-comprehension
# REMOVED_UNUSED_CODE:                     messages.append("\n".join([line for line in lines if line]))
# REMOVED_UNUSED_CODE:                 for msg in messages:
# REMOVED_UNUSED_CODE:                     if len(msg) > MAX_MESSAGE_LENGTH:
# REMOVED_UNUSED_CODE:                         msg = "Message dropped because length exceeds "
# REMOVED_UNUSED_CODE:                         msg += f"maximum allowed characters: {MAX_MESSAGE_LENGTH}"
# REMOVED_UNUSED_CODE:                         logger.warning(msg)
# REMOVED_UNUSED_CODE:                     await self._send_msg(msg)
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 message = f"Didn't find any custom-data entries for Trade ID: `{trade_id}`"
# REMOVED_UNUSED_CODE:                 message += f" and Key: `{key}`." if key is not None else ""
# REMOVED_UNUSED_CODE:                 await self._send_msg(message)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         except RPCException as e:
# REMOVED_UNUSED_CODE:             await self._send_msg(str(e))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _update_msg(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         query: CallbackQuery,
# REMOVED_UNUSED_CODE:         msg: str,
# REMOVED_UNUSED_CODE:         callback_path: str = "",
# REMOVED_UNUSED_CODE:         reload_able: bool = False,
# REMOVED_UNUSED_CODE:         parse_mode: str = ParseMode.MARKDOWN,
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         if reload_able:
# REMOVED_UNUSED_CODE:             reply_markup = InlineKeyboardMarkup(
# REMOVED_UNUSED_CODE:                 [
# REMOVED_UNUSED_CODE:                     [InlineKeyboardButton("Refresh", callback_data=callback_path)],
# REMOVED_UNUSED_CODE:                 ]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             reply_markup = InlineKeyboardMarkup([[]])
# REMOVED_UNUSED_CODE:         msg += f"\nUpdated: {datetime.now().ctime()}"
# REMOVED_UNUSED_CODE:         if not query.message:
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             await query.edit_message_text(
# REMOVED_UNUSED_CODE:                 text=msg, parse_mode=parse_mode, reply_markup=reply_markup
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         except BadRequest as e:
# REMOVED_UNUSED_CODE:             if "not modified" in e.message.lower():
# REMOVED_UNUSED_CODE:                 pass
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 logger.warning("TelegramError: %s", e.message)
# REMOVED_UNUSED_CODE:         except TelegramError as telegram_err:
# REMOVED_UNUSED_CODE:             logger.warning("TelegramError: %s! Giving up on that message.", telegram_err.message)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _send_msg(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         msg: str,
# REMOVED_UNUSED_CODE:         parse_mode: str = ParseMode.MARKDOWN,
# REMOVED_UNUSED_CODE:         disable_notification: bool = False,
# REMOVED_UNUSED_CODE:         keyboard: list[list[InlineKeyboardButton]] | None = None,
# REMOVED_UNUSED_CODE:         callback_path: str = "",
# REMOVED_UNUSED_CODE:         reload_able: bool = False,
# REMOVED_UNUSED_CODE:         query: CallbackQuery | None = None,
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Send given markdown message
# REMOVED_UNUSED_CODE:         :param msg: message
# REMOVED_UNUSED_CODE:         :param bot: alternative bot
# REMOVED_UNUSED_CODE:         :param parse_mode: telegram parse mode
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup
# REMOVED_UNUSED_CODE:         if query:
# REMOVED_UNUSED_CODE:             await self._update_msg(
# REMOVED_UNUSED_CODE:                 query=query,
# REMOVED_UNUSED_CODE:                 msg=msg,
# REMOVED_UNUSED_CODE:                 parse_mode=parse_mode,
# REMOVED_UNUSED_CODE:                 callback_path=callback_path,
# REMOVED_UNUSED_CODE:                 reload_able=reload_able,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE:         if reload_able and self._config["telegram"].get("reload", True):
# REMOVED_UNUSED_CODE:             reply_markup = InlineKeyboardMarkup(
# REMOVED_UNUSED_CODE:                 [[InlineKeyboardButton("Refresh", callback_data=callback_path)]]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             if keyboard is not None:
# REMOVED_UNUSED_CODE:                 reply_markup = InlineKeyboardMarkup(keyboard)
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 reply_markup = ReplyKeyboardMarkup(self._keyboard, resize_keyboard=True)
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 await self._app.bot.send_message(
# REMOVED_UNUSED_CODE:                     self._config["telegram"]["chat_id"],
# REMOVED_UNUSED_CODE:                     text=msg,
# REMOVED_UNUSED_CODE:                     parse_mode=parse_mode,
# REMOVED_UNUSED_CODE:                     reply_markup=reply_markup,
# REMOVED_UNUSED_CODE:                     disable_notification=disable_notification,
# REMOVED_UNUSED_CODE:                     message_thread_id=self._config["telegram"].get("topic_id"),
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             except NetworkError as network_err:
# REMOVED_UNUSED_CODE:                 # Sometimes the telegram server resets the current connection,
# REMOVED_UNUSED_CODE:                 # if this is the case we send the message again.
# REMOVED_UNUSED_CODE:                 logger.warning(
# REMOVED_UNUSED_CODE:                     "Telegram NetworkError: %s! Trying one more time.", network_err.message
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 await self._app.bot.send_message(
# REMOVED_UNUSED_CODE:                     self._config["telegram"]["chat_id"],
# REMOVED_UNUSED_CODE:                     text=msg,
# REMOVED_UNUSED_CODE:                     parse_mode=parse_mode,
# REMOVED_UNUSED_CODE:                     reply_markup=reply_markup,
# REMOVED_UNUSED_CODE:                     disable_notification=disable_notification,
# REMOVED_UNUSED_CODE:                     message_thread_id=self._config["telegram"].get("topic_id"),
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:         except TelegramError as telegram_err:
# REMOVED_UNUSED_CODE:             logger.warning("TelegramError: %s! Giving up on that message.", telegram_err.message)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @authorized_only
# REMOVED_UNUSED_CODE:     async def _changemarketdir(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handler for /marketdir.
# REMOVED_UNUSED_CODE:         Updates the bot's market_direction
# REMOVED_UNUSED_CODE:         :param bot: telegram bot
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if context.args and len(context.args) == 1:
# REMOVED_UNUSED_CODE:             new_market_dir_arg = context.args[0]
# REMOVED_UNUSED_CODE:             old_market_dir = self._rpc._get_market_direction()
# REMOVED_UNUSED_CODE:             new_market_dir = None
# REMOVED_UNUSED_CODE:             if new_market_dir_arg == "long":
# REMOVED_UNUSED_CODE:                 new_market_dir = MarketDirection.LONG
# REMOVED_UNUSED_CODE:             elif new_market_dir_arg == "short":
# REMOVED_UNUSED_CODE:                 new_market_dir = MarketDirection.SHORT
# REMOVED_UNUSED_CODE:             elif new_market_dir_arg == "even":
# REMOVED_UNUSED_CODE:                 new_market_dir = MarketDirection.EVEN
# REMOVED_UNUSED_CODE:             elif new_market_dir_arg == "none":
# REMOVED_UNUSED_CODE:                 new_market_dir = MarketDirection.NONE
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if new_market_dir is not None:
# REMOVED_UNUSED_CODE:                 self._rpc._update_market_direction(new_market_dir)
# REMOVED_UNUSED_CODE:                 await self._send_msg(
# REMOVED_UNUSED_CODE:                     "Successfully updated market direction"
# REMOVED_UNUSED_CODE:                     f" from *{old_market_dir}* to *{new_market_dir}*."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 raise RPCException(
# REMOVED_UNUSED_CODE:                     "Invalid market direction provided. \n"
# REMOVED_UNUSED_CODE:                     "Valid market directions: *long, short, even, none*"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:         elif context.args is not None and len(context.args) == 0:
# REMOVED_UNUSED_CODE:             old_market_dir = self._rpc._get_market_direction()
# REMOVED_UNUSED_CODE:             await self._send_msg(f"Currently set market direction: *{old_market_dir}*")
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             raise RPCException(
# REMOVED_UNUSED_CODE:                 "Invalid usage of command /marketdir. \n"
# REMOVED_UNUSED_CODE:                 "Usage: */marketdir [short |  long | even | none]*"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _tg_info(self, update: Update, context: CallbackContext) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Intentionally unauthenticated Handler for /tg_info.
# REMOVED_UNUSED_CODE:         Returns information about the current telegram chat - even if chat_id does not
# REMOVED_UNUSED_CODE:         correspond to this chat.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param update: message update
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not update.message:
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE:         chat_id = update.message.chat_id
# REMOVED_UNUSED_CODE:         topic_id = update.message.message_thread_id
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         msg = f"""Freqtrade Bot Info:
# REMOVED_UNUSED_CODE:         ```json
# REMOVED_UNUSED_CODE:             {{
# REMOVED_UNUSED_CODE:                 "enabled": true,
# REMOVED_UNUSED_CODE:                 "token": "********",
# REMOVED_UNUSED_CODE:                 "chat_id": "{chat_id}",
# REMOVED_UNUSED_CODE:                 {f'"topic_id": "{topic_id}"' if topic_id else ""}
# REMOVED_UNUSED_CODE:             }}
# REMOVED_UNUSED_CODE:         ```
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             await context.bot.send_message(
# REMOVED_UNUSED_CODE:                 chat_id=chat_id,
# REMOVED_UNUSED_CODE:                 text=msg,
# REMOVED_UNUSED_CODE:                 parse_mode=ParseMode.MARKDOWN_V2,
# REMOVED_UNUSED_CODE:                 message_thread_id=topic_id,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         except TelegramError as telegram_err:
# REMOVED_UNUSED_CODE:             logger.warning("TelegramError: %s! Giving up on that message.", telegram_err.message)
