"""
Freqtrade is the main module of this bot. It contains the class Freqtrade()
"""

import logging
import traceback
from copy import deepcopy
from datetime import datetime, time, timedelta, timezone
from math import isclose
from threading import Lock
from time import sleep
from typing import Any

from schedule import Scheduler

from freqtrade import constants
from freqtrade.configuration import validate_config_consistency
from freqtrade.constants import BuySell, Config, EntryExecuteMode, ExchangeConfig, LongShort
from freqtrade.data.converter import order_book_to_dataframe
from freqtrade.data.dataprovider import DataProvider
from freqtrade.edge import Edge
from freqtrade.enums import (
    ExitCheckTuple,
    ExitType,
    MarginMode,
    RPCMessageType,
    SignalDirection,
    State,
    TradingMode,
)
from freqtrade.exceptions import (
    DependencyException,
    ExchangeError,
    InsufficientFundsError,
    InvalidOrderException,
    PricingError,
)
from freqtrade.exchange import (
    ROUND_DOWN,
    ROUND_UP,
    remove_exchange_credentials,
    timeframe_to_minutes,
    timeframe_to_next_date,
    timeframe_to_seconds,
)
from freqtrade.exchange.exchange_types import CcxtOrder
from freqtrade.leverage.liquidation_price import update_liquidation_prices
from freqtrade.misc import safe_value_fallback, safe_value_fallback2
from freqtrade.mixins import LoggingMixin
from freqtrade.persistence import Order, PairLocks, Trade, init_db
from freqtrade.persistence.key_value_store import set_startup_time
from freqtrade.plugins.pairlistmanager import PairListManager
from freqtrade.plugins.protectionmanager import ProtectionManager
from freqtrade.resolvers import ExchangeResolver, StrategyResolver
from freqtrade.rpc import RPCManager
from freqtrade.rpc.external_message_consumer import ExternalMessageConsumer
from freqtrade.rpc.rpc_types import (
    ProfitLossStr,
    RPCCancelMsg,
    RPCEntryMsg,
    RPCExitCancelMsg,
    RPCExitMsg,
    RPCProtectionMsg,
)
from freqtrade.strategy.interface import IStrategy
from freqtrade.strategy.strategy_wrapper import strategy_safe_wrapper
from freqtrade.util import FtPrecise, MeasureTime, dt_from_ts
from freqtrade.util.migrations.binance_mig import migrate_binance_futures_names
from freqtrade.wallets import Wallets


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class FreqtradeBot(LoggingMixin):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Freqtrade is the main class of the bot.
# REMOVED_UNUSED_CODE:     This is from here the bot start its logic.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Init all variables and objects the bot needs to work
# REMOVED_UNUSED_CODE:         :param config: configuration dict, you can use Configuration.get_config()
# REMOVED_UNUSED_CODE:         to get the config dict.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.active_pair_whitelist: list[str] = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Init bot state
# REMOVED_UNUSED_CODE:         self.state = State.STOPPED
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Init objects
# REMOVED_UNUSED_CODE:         self.config = config
# REMOVED_UNUSED_CODE:         exchange_config: ExchangeConfig = deepcopy(config["exchange"])
# REMOVED_UNUSED_CODE:         # Remove credentials from original exchange config to avoid accidental credential exposure
# REMOVED_UNUSED_CODE:         remove_exchange_credentials(config["exchange"], True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.strategy: IStrategy = StrategyResolver.load_strategy(self.config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Check config consistency here since strategies can set certain options
# REMOVED_UNUSED_CODE:         validate_config_consistency(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.exchange = ExchangeResolver.load_exchange(
# REMOVED_UNUSED_CODE:             self.config, exchange_config=exchange_config, load_leverage_tiers=True
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         init_db(self.config["db_url"])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.wallets = Wallets(self.config, self.exchange)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         PairLocks.timeframe = self.config["timeframe"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.trading_mode: TradingMode = self.config.get("trading_mode", TradingMode.SPOT)
# REMOVED_UNUSED_CODE:         self.margin_mode: MarginMode = self.config.get("margin_mode", MarginMode.NONE)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.last_process: datetime | None = None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # RPC runs in separate threads, can start handling external commands just after
# REMOVED_UNUSED_CODE:         # initialization, even before Freqtradebot has a chance to start its throttling,
# REMOVED_UNUSED_CODE:         # so anything in the Freqtradebot instance should be ready (initialized), including
# REMOVED_UNUSED_CODE:         # the initial state of the bot.
# REMOVED_UNUSED_CODE:         # Keep this at the end of this initialization method.
# REMOVED_UNUSED_CODE:         self.rpc: RPCManager = RPCManager(self)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.dataprovider = DataProvider(self.config, self.exchange, rpc=self.rpc)
# REMOVED_UNUSED_CODE:         self.pairlists = PairListManager(self.exchange, self.config, self.dataprovider)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.dataprovider.add_pairlisthandler(self.pairlists)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Attach Dataprovider to strategy instance
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.strategy.dp = self.dataprovider
# REMOVED_UNUSED_CODE:         # Attach Wallets to strategy instance
# REMOVED_UNUSED_CODE:         self.strategy.wallets = self.wallets
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Initializing Edge only if enabled
# REMOVED_UNUSED_CODE:         self.edge = (
# REMOVED_UNUSED_CODE:             Edge(self.config, self.exchange, self.strategy)
# REMOVED_UNUSED_CODE:             if self.config.get("edge", {}).get("enabled", False)
# REMOVED_UNUSED_CODE:             else None
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Init ExternalMessageConsumer if enabled
# REMOVED_UNUSED_CODE:         self.emc = (
# REMOVED_UNUSED_CODE:             ExternalMessageConsumer(self.config, self.dataprovider)
# REMOVED_UNUSED_CODE:             if self.config.get("external_message_consumer", {}).get("enabled", False)
# REMOVED_UNUSED_CODE:             else None
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.active_pair_whitelist = self._refresh_active_whitelist()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Set initial bot state from config
# REMOVED_UNUSED_CODE:         initial_state = self.config.get("initial_state")
# REMOVED_UNUSED_CODE:         self.state = State[initial_state.upper()] if initial_state else State.STOPPED
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Protect exit-logic from forcesell and vice versa
# REMOVED_UNUSED_CODE:         self._exit_lock = Lock()
# REMOVED_UNUSED_CODE:         timeframe_secs = timeframe_to_seconds(self.strategy.timeframe)
# REMOVED_UNUSED_CODE:         LoggingMixin.__init__(self, logger, timeframe_secs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._schedule = Scheduler()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES:
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             def update():
# REMOVED_UNUSED_CODE:                 self.update_funding_fees()
# REMOVED_UNUSED_CODE:                 self.update_all_liquidation_prices()
# REMOVED_UNUSED_CODE:                 self.wallets.update()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # This would be more efficient if scheduled in utc time, and performed at each
# REMOVED_UNUSED_CODE:             # funding interval, specified by funding_fee_times on the exchange classes
# REMOVED_UNUSED_CODE:             # However, this reduces the precision - and might therefore lead to problems.
# REMOVED_UNUSED_CODE:             for time_slot in range(0, 24):
# REMOVED_UNUSED_CODE:                 for minutes in [1, 31]:
# REMOVED_UNUSED_CODE:                     t = str(time(time_slot, minutes, 2))
# REMOVED_UNUSED_CODE:                     self._schedule.every().day.at(t).do(update)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._schedule.every().day.at("00:02").do(self.exchange.ws_connection_reset)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.strategy.ft_bot_start()
# REMOVED_UNUSED_CODE:         # Initialize protections AFTER bot start - otherwise parameters are not loaded.
# REMOVED_UNUSED_CODE:         self.protections = ProtectionManager(self.config, self.strategy.protections)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         def log_took_too_long(duration: float, time_limit: float):
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 f"Strategy analysis took {duration:.2f}s, more than 25% of the timeframe "
# REMOVED_UNUSED_CODE:                 f"({time_limit:.2f}s). This can lead to delayed orders and missed signals."
# REMOVED_UNUSED_CODE:                 "Consider either reducing the amount of work your strategy performs "
# REMOVED_UNUSED_CODE:                 "or reduce the amount of pairs in the Pairlist."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._measure_execution = MeasureTime(log_took_too_long, timeframe_secs * 0.25)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def notify_status(self, msg: str, msg_type=RPCMessageType.STATUS) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Public method for users of this class (worker, etc.) to send notifications
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         via RPC about changes in the bot status.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.rpc.send_msg({"type": msg_type, "status": msg})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def cleanup(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Cleanup pending resources on an already stopped bot
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         logger.info("Cleaning up modules ...")
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             # Wrap db activities in shutdown to avoid problems if database is gone,
# REMOVED_UNUSED_CODE:             # and raises further exceptions.
# REMOVED_UNUSED_CODE:             if self.config["cancel_open_orders_on_exit"]:
# REMOVED_UNUSED_CODE:                 self.cancel_all_open_orders()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.check_for_open_trades()
# REMOVED_UNUSED_CODE:         except Exception as e:
# REMOVED_UNUSED_CODE:             logger.warning(f"Exception during cleanup: {e.__class__.__name__} {e}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         finally:
# REMOVED_UNUSED_CODE:             self.strategy.ft_bot_cleanup()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.rpc.cleanup()
# REMOVED_UNUSED_CODE:         if self.emc:
# REMOVED_UNUSED_CODE:             self.emc.shutdown()
# REMOVED_UNUSED_CODE:         self.exchange.close()
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             Trade.commit()
# REMOVED_UNUSED_CODE:         except Exception:
# REMOVED_UNUSED_CODE:             # Exceptions here will be happening if the db disappeared.
# REMOVED_UNUSED_CODE:             # At which point we can no longer commit anyway.
# REMOVED_UNUSED_CODE:             logger.exception("Error during cleanup")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def startup(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Called on startup and after reloading the bot - triggers notifications and
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         performs startup tasks
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         migrate_binance_futures_names(self.config)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         set_startup_time()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.rpc.startup_messages(self.config, self.pairlists, self.protections)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Update older trades with precision and precision mode
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.startup_backpopulate_precision()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not self.edge:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Adjust stoploss if it was changed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             Trade.stoploss_reinitialization(self.strategy.stoploss)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Only update open orders on startup
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # This will update the database after the initial migration
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.startup_update_open_orders()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.update_all_liquidation_prices()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.update_funding_fees()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def process(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Queries the persistence layer for open trades and handles them,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         otherwise a new trade is created.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: True if one or more trades has been created or closed, False otherwise
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Check whether markets have to be reloaded and reload them when it's needed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.exchange.reload_markets()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.update_trades_without_assigned_fees()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Query trades from persistence layer
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trades: list[Trade] = Trade.get_open_trades()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.active_pair_whitelist = self._refresh_active_whitelist(trades)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Refreshing candles
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.dataprovider.refresh(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.pairlists.create_pair_list(self.active_pair_whitelist),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.strategy.gather_informative_pairs(),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         strategy_safe_wrapper(self.strategy.bot_loop_start, supress_error=True)(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_time=datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with self._measure_execution:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.strategy.analyze(self.active_pair_whitelist)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with self._exit_lock:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Check for exchange cancellations, timeouts and user requested replace
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.manage_open_orders()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Protect from collisions with force_exit.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Without this, freqtrade may try to recreate stoploss_on_exchange orders
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # while exiting is in process, since telegram messages arrive in an different thread.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with self._exit_lock:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trades = Trade.get_open_trades()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # First process current opened trades (positions)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.exit_positions(trades)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Check if we need to adjust our current positions before attempting to enter new trades.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.strategy.position_adjustment_enable:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             with self._exit_lock:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.process_open_trade_positions()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Then looking for entry opportunities
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.get_free_open_trades():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.enter_positions()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._schedule.run_pending()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Trade.commit()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.rpc.process_msg_queue(self.dataprovider._msg_queue)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.last_process = datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def process_stopped(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Close all orders that were left open
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.config["cancel_open_orders_on_exit"]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.cancel_all_open_orders()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def check_for_open_trades(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Notify the user when the bot is stopped (not reloaded)
# REMOVED_UNUSED_CODE:         and there are still open trades active.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         open_trades = Trade.get_open_trades()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if len(open_trades) != 0 and self.state != State.RELOAD_CONFIG:
# REMOVED_UNUSED_CODE:             msg = {
# REMOVED_UNUSED_CODE:                 "type": RPCMessageType.WARNING,
# REMOVED_UNUSED_CODE:                 "status": f"{len(open_trades)} open trades active.\n\n"
# REMOVED_UNUSED_CODE:                 f"Handle these trades manually on {self.exchange.name}, "
# REMOVED_UNUSED_CODE:                 f"or '/start' the bot again and use '/stopentry' "
# REMOVED_UNUSED_CODE:                 f"to handle open trades gracefully. \n"
# REMOVED_UNUSED_CODE:                 f"{'Note: Trades are simulated (dry run).' if self.config['dry_run'] else ''}",
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE:             self.rpc.send_msg(msg)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _refresh_active_whitelist(self, trades: list[Trade] | None = None) -> list[str]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Refresh active whitelist from pairlist or edge and extend it with
# REMOVED_UNUSED_CODE:         pairs that have open trades.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Refresh whitelist
# REMOVED_UNUSED_CODE:         _prev_whitelist = self.pairlists.whitelist
# REMOVED_UNUSED_CODE:         self.pairlists.refresh_pairlist()
# REMOVED_UNUSED_CODE:         _whitelist = self.pairlists.whitelist
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Calculating Edge positioning
# REMOVED_UNUSED_CODE:         if self.edge:
# REMOVED_UNUSED_CODE:             self.edge.calculate(_whitelist)
# REMOVED_UNUSED_CODE:             _whitelist = self.edge.adjust(_whitelist)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if trades:
# REMOVED_UNUSED_CODE:             # Extend active-pair whitelist with pairs of open trades
# REMOVED_UNUSED_CODE:             # It ensures that candle (OHLCV) data are downloaded for open trades as well
# REMOVED_UNUSED_CODE:             _whitelist.extend([trade.pair for trade in trades if trade.pair not in _whitelist])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Called last to include the included pairs
# REMOVED_UNUSED_CODE:         if _prev_whitelist != _whitelist:
# REMOVED_UNUSED_CODE:             self.rpc.send_msg({"type": RPCMessageType.WHITELIST, "data": _whitelist})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return _whitelist
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_free_open_trades(self) -> int:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Return the number of free open trades slots or 0 if
# REMOVED_UNUSED_CODE:         max number of open trades reached
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         open_trades = Trade.get_open_trade_count()
# REMOVED_UNUSED_CODE:         return max(0, self.config["max_open_trades"] - open_trades)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def update_all_liquidation_prices(self) -> None:
# REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES and self.margin_mode == MarginMode.CROSS:
# REMOVED_UNUSED_CODE:             # Update liquidation prices for all trades in cross margin mode
# REMOVED_UNUSED_CODE:             update_liquidation_prices(
# REMOVED_UNUSED_CODE:                 exchange=self.exchange,
# REMOVED_UNUSED_CODE:                 wallets=self.wallets,
# REMOVED_UNUSED_CODE:                 stake_currency=self.config["stake_currency"],
# REMOVED_UNUSED_CODE:                 dry_run=self.config["dry_run"],
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def update_funding_fees(self) -> None:
# REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES:
# REMOVED_UNUSED_CODE:             trades: list[Trade] = Trade.get_open_trades()
# REMOVED_UNUSED_CODE:             for trade in trades:
# REMOVED_UNUSED_CODE:                 trade.set_funding_fees(
# REMOVED_UNUSED_CODE:                     self.exchange.get_funding_fees(
# REMOVED_UNUSED_CODE:                         pair=trade.pair,
# REMOVED_UNUSED_CODE:                         amount=trade.amount,
# REMOVED_UNUSED_CODE:                         is_short=trade.is_short,
# REMOVED_UNUSED_CODE:                         open_date=trade.date_last_filled_utc,
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def startup_backpopulate_precision(self) -> None:
# REMOVED_UNUSED_CODE:         trades = Trade.get_trades([Trade.contract_size.is_(None)])
# REMOVED_UNUSED_CODE:         for trade in trades:
# REMOVED_UNUSED_CODE:             if trade.exchange != self.exchange.id:
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade.precision_mode = self.exchange.precisionMode
# REMOVED_UNUSED_CODE:             trade.precision_mode_price = self.exchange.precision_mode_price
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade.amount_precision = self.exchange.get_precision_amount(trade.pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade.price_precision = self.exchange.get_precision_price(trade.pair)
# REMOVED_UNUSED_CODE:             trade.contract_size = self.exchange.get_contract_size(trade.pair)
# REMOVED_UNUSED_CODE:         Trade.commit()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def startup_update_open_orders(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Updates open orders based on order list kept in the database.
# REMOVED_UNUSED_CODE:         Mainly updates the state of orders - but may also close trades
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self.config["dry_run"] or self.config["exchange"].get("skip_open_order_update", False):
# REMOVED_UNUSED_CODE:             # Updating open orders in dry-run does not make sense and will fail.
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         orders = Order.get_open_orders()
# REMOVED_UNUSED_CODE:         logger.info(f"Updating {len(orders)} open orders.")
# REMOVED_UNUSED_CODE:         for order in orders:
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 fo = self.exchange.fetch_order_or_stoploss_order(
# REMOVED_UNUSED_CODE:                     order.order_id, order.ft_pair, order.ft_order_side == "stoploss"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 if not order.trade:
# REMOVED_UNUSED_CODE:                     # This should not happen, but it does if trades were deleted manually.
# REMOVED_UNUSED_CODE:                     # This can only incur on sqlite, which doesn't enforce foreign constraints.
# REMOVED_UNUSED_CODE:                     logger.warning(
# REMOVED_UNUSED_CODE:                         f"Order {order.order_id} has no trade attached. "
# REMOVED_UNUSED_CODE:                         "This may suggest a database corruption. "
# REMOVED_UNUSED_CODE:                         f"The expected trade ID is {order.ft_trade_id}. Ignoring this order."
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     continue
# REMOVED_UNUSED_CODE:                 self.update_trade_state(
# REMOVED_UNUSED_CODE:                     order.trade,
# REMOVED_UNUSED_CODE:                     order.order_id,
# REMOVED_UNUSED_CODE:                     fo,
# REMOVED_UNUSED_CODE:                     stoploss_order=(order.ft_order_side == "stoploss"),
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             except InvalidOrderException as e:
# REMOVED_UNUSED_CODE:                 logger.warning(f"Error updating Order {order.order_id} due to {e}.")
# REMOVED_UNUSED_CODE:                 if order.order_date_utc - timedelta(days=5) < datetime.now(timezone.utc):
# REMOVED_UNUSED_CODE:                     logger.warning(
# REMOVED_UNUSED_CODE:                         "Order is older than 5 days. Assuming order was fully cancelled."
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     fo = order.to_ccxt_object()
# REMOVED_UNUSED_CODE:                     fo["status"] = "canceled"
# REMOVED_UNUSED_CODE:                     self.handle_cancel_order(
# REMOVED_UNUSED_CODE:                         fo, order, order.trade, constants.CANCEL_REASON["TIMEOUT"]
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             except ExchangeError as e:
# REMOVED_UNUSED_CODE:                 logger.warning(f"Error updating Order {order.order_id} due to {e}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def update_trades_without_assigned_fees(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Update closed trades without close fees assigned.
# REMOVED_UNUSED_CODE:         Only acts when Orders are in the database, otherwise the last order-id is unknown.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self.config["dry_run"]:
# REMOVED_UNUSED_CODE:             # Updating open orders in dry-run does not make sense and will fail.
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trades: list[Trade] = Trade.get_closed_trades_without_assigned_fees()
# REMOVED_UNUSED_CODE:         for trade in trades:
# REMOVED_UNUSED_CODE:             if not trade.is_open and not trade.fee_updated(trade.exit_side):
# REMOVED_UNUSED_CODE:                 # Get sell fee
# REMOVED_UNUSED_CODE:                 order = trade.select_order(trade.exit_side, False, only_filled=True)
# REMOVED_UNUSED_CODE:                 if not order:
# REMOVED_UNUSED_CODE:                     order = trade.select_order("stoploss", False)
# REMOVED_UNUSED_CODE:                 if order:
# REMOVED_UNUSED_CODE:                     logger.info(
# REMOVED_UNUSED_CODE:                         f"Updating {trade.exit_side}-fee on trade {trade}"
# REMOVED_UNUSED_CODE:                         f"for order {order.order_id}."
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     self.update_trade_state(
# REMOVED_UNUSED_CODE:                         trade,
# REMOVED_UNUSED_CODE:                         order.order_id,
# REMOVED_UNUSED_CODE:                         stoploss_order=order.ft_order_side == "stoploss",
# REMOVED_UNUSED_CODE:                         send_msg=False,
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trades = Trade.get_open_trades_without_assigned_fees()
# REMOVED_UNUSED_CODE:         for trade in trades:
# REMOVED_UNUSED_CODE:             with self._exit_lock:
# REMOVED_UNUSED_CODE:                 if trade.is_open and not trade.fee_updated(trade.entry_side):
# REMOVED_UNUSED_CODE:                     order = trade.select_order(trade.entry_side, False, only_filled=True)
# REMOVED_UNUSED_CODE:                     open_order = trade.select_order(trade.entry_side, True)
# REMOVED_UNUSED_CODE:                     if order and open_order is None:
# REMOVED_UNUSED_CODE:                         logger.info(
# REMOVED_UNUSED_CODE:                             f"Updating {trade.entry_side}-fee on trade {trade}"
# REMOVED_UNUSED_CODE:                             f"for order {order.order_id}."
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:                         self.update_trade_state(trade, order.order_id, send_msg=False)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def handle_insufficient_funds(self, trade: Trade):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Try refinding a lost trade.
# REMOVED_UNUSED_CODE:         Only used when InsufficientFunds appears on exit orders (stoploss or long sell/short buy).
# REMOVED_UNUSED_CODE:         Tries to walk the stored orders and updates the trade state if necessary.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         logger.info(f"Trying to refind lost order for {trade}")
# REMOVED_UNUSED_CODE:         for order in trade.orders:
# REMOVED_UNUSED_CODE:             logger.info(f"Trying to refind {order}")
# REMOVED_UNUSED_CODE:             fo = None
# REMOVED_UNUSED_CODE:             if not order.ft_is_open:
# REMOVED_UNUSED_CODE:                 logger.debug(f"Order {order} is no longer open.")
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 fo = self.exchange.fetch_order_or_stoploss_order(
# REMOVED_UNUSED_CODE:                     order.order_id, order.ft_pair, order.ft_order_side == "stoploss"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 if fo:
# REMOVED_UNUSED_CODE:                     logger.info(f"Found {order} for trade {trade}.")
# REMOVED_UNUSED_CODE:                     self.update_trade_state(
# REMOVED_UNUSED_CODE:                         trade, order.order_id, fo, stoploss_order=order.ft_order_side == "stoploss"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             except ExchangeError:
# REMOVED_UNUSED_CODE:                 logger.warning(f"Error updating {order.order_id}.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def handle_onexchange_order(self, trade: Trade) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Try refinding a order that is not in the database.
# REMOVED_UNUSED_CODE:         Only used balance disappeared, which would make exiting impossible.
# REMOVED_UNUSED_CODE:         :return: True if the trade was deleted, False otherwise
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             orders = self.exchange.fetch_orders(
# REMOVED_UNUSED_CODE:                 trade.pair, trade.open_date_utc - timedelta(seconds=10)
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             prev_exit_reason = trade.exit_reason
# REMOVED_UNUSED_CODE:             prev_trade_state = trade.is_open
# REMOVED_UNUSED_CODE:             prev_trade_amount = trade.amount
# REMOVED_UNUSED_CODE:             for order in orders:
# REMOVED_UNUSED_CODE:                 trade_order = [o for o in trade.orders if o.order_id == order["id"]]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 if trade_order:
# REMOVED_UNUSED_CODE:                     # We knew this order, but didn't have it updated properly
# REMOVED_UNUSED_CODE:                     order_obj = trade_order[0]
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     logger.info(f"Found previously unknown order {order['id']} for {trade.pair}.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                     order_obj = Order.parse_from_ccxt_object(order, trade.pair, order["side"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     order_obj.order_filled_date = dt_from_ts(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         safe_value_fallback(order, "lastTradeTimestamp", "timestamp")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     trade.orders.append(order_obj)
# REMOVED_UNUSED_CODE:                     Trade.commit()
# REMOVED_UNUSED_CODE:                     trade.exit_reason = ExitType.SOLD_ON_EXCHANGE.value
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 self.update_trade_state(trade, order["id"], order, send_msg=False)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 logger.info(f"handled order {order['id']}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Refresh trade from database
# REMOVED_UNUSED_CODE:             Trade.session.refresh(trade)
# REMOVED_UNUSED_CODE:             if not trade.is_open:
# REMOVED_UNUSED_CODE:                 # Trade was just closed
# REMOVED_UNUSED_CODE:                 trade.close_date = trade.date_last_filled_utc
# REMOVED_UNUSED_CODE:                 self.order_close_notify(
# REMOVED_UNUSED_CODE:                     trade,
# REMOVED_UNUSED_CODE:                     order_obj,
# REMOVED_UNUSED_CODE:                     order_obj.ft_order_side == "stoploss",
# REMOVED_UNUSED_CODE:                     send_msg=prev_trade_state != trade.is_open,
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 trade.exit_reason = prev_exit_reason
# REMOVED_UNUSED_CODE:                 total = (
# REMOVED_UNUSED_CODE:                     self.wallets.get_owned(trade.pair, trade.base_currency)
# REMOVED_UNUSED_CODE:                     if trade.base_currency
# REMOVED_UNUSED_CODE:                     else 0
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 if total < trade.amount:
# REMOVED_UNUSED_CODE:                     if trade.fully_canceled_entry_order_count == len(trade.orders):
# REMOVED_UNUSED_CODE:                         logger.warning(
# REMOVED_UNUSED_CODE:                             f"Trade only had fully canceled entry orders. "
# REMOVED_UNUSED_CODE:                             f"Removing {trade} from database."
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                         self._notify_enter_cancel(
# REMOVED_UNUSED_CODE:                             trade,
# REMOVED_UNUSED_CODE:                             order_type=self.strategy.order_types["entry"],
# REMOVED_UNUSED_CODE:                             reason=constants.CANCEL_REASON["FULLY_CANCELLED"],
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:                         trade.delete()
# REMOVED_UNUSED_CODE:                         return True
# REMOVED_UNUSED_CODE:                     if total > trade.amount * 0.98:
# REMOVED_UNUSED_CODE:                         logger.warning(
# REMOVED_UNUSED_CODE:                             f"{trade} has a total of {trade.amount} {trade.base_currency}, "
# REMOVED_UNUSED_CODE:                             f"but the Wallet shows a total of {total} {trade.base_currency}. "
# REMOVED_UNUSED_CODE:                             f"Adjusting trade amount to {total}. "
# REMOVED_UNUSED_CODE:                             "This may however lead to further issues."
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:                         trade.amount = total
# REMOVED_UNUSED_CODE:                     else:
# REMOVED_UNUSED_CODE:                         logger.warning(
# REMOVED_UNUSED_CODE:                             f"{trade} has a total of {trade.amount} {trade.base_currency}, "
# REMOVED_UNUSED_CODE:                             f"but the Wallet shows a total of {total} {trade.base_currency}. "
# REMOVED_UNUSED_CODE:                             "Refusing to adjust as the difference is too large. "
# REMOVED_UNUSED_CODE:                             "This may however lead to further issues."
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:                 if prev_trade_amount != trade.amount:
# REMOVED_UNUSED_CODE:                     # Cancel stoploss on exchange if the amount changed
# REMOVED_UNUSED_CODE:                     trade = self.cancel_stoploss_on_exchange(trade)
# REMOVED_UNUSED_CODE:             Trade.commit()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         except ExchangeError:
# REMOVED_UNUSED_CODE:             logger.warning("Error finding onexchange order.")
# REMOVED_UNUSED_CODE:         except Exception:
# REMOVED_UNUSED_CODE:             # catching https://github.com/freqtrade/freqtrade/issues/9025
# REMOVED_UNUSED_CODE:             logger.warning("Error finding onexchange order", exc_info=True)
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     #
# REMOVED_UNUSED_CODE:     # enter positions / open trades logic and methods
# REMOVED_UNUSED_CODE:     #
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def enter_positions(self) -> int:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Tries to execute entry orders for new trades (positions)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         trades_created = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         whitelist = deepcopy(self.active_pair_whitelist)
# REMOVED_UNUSED_CODE:         if not whitelist:
# REMOVED_UNUSED_CODE:             self.log_once("Active pair whitelist is empty.", logger.info)
# REMOVED_UNUSED_CODE:             return trades_created
# REMOVED_UNUSED_CODE:         # Remove pairs for currently opened trades from the whitelist
# REMOVED_UNUSED_CODE:         for trade in Trade.get_open_trades():
# REMOVED_UNUSED_CODE:             if trade.pair in whitelist:
# REMOVED_UNUSED_CODE:                 whitelist.remove(trade.pair)
# REMOVED_UNUSED_CODE:                 logger.debug("Ignoring %s in pair whitelist", trade.pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not whitelist:
# REMOVED_UNUSED_CODE:             self.log_once(
# REMOVED_UNUSED_CODE:                 "No currency pair in active pair whitelist, but checking to exit open trades.",
# REMOVED_UNUSED_CODE:                 logger.info,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             return trades_created
# REMOVED_UNUSED_CODE:         if PairLocks.is_global_lock(side="*"):
# REMOVED_UNUSED_CODE:             # This only checks for total locks (both sides).
# REMOVED_UNUSED_CODE:             # per-side locks will be evaluated by `is_pair_locked` within create_trade,
# REMOVED_UNUSED_CODE:             # once the direction for the trade is clear.
# REMOVED_UNUSED_CODE:             lock = PairLocks.get_pair_longest_lock("*")
# REMOVED_UNUSED_CODE:             if lock:
# REMOVED_UNUSED_CODE:                 self.log_once(
# REMOVED_UNUSED_CODE:                     f"Global pairlock active until "
# REMOVED_UNUSED_CODE:                     f"{lock.lock_end_time.strftime(constants.DATETIME_PRINT_FORMAT)}. "
# REMOVED_UNUSED_CODE:                     f"Not creating new trades, reason: {lock.reason}.",
# REMOVED_UNUSED_CODE:                     logger.info,
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 self.log_once("Global pairlock active. Not creating new trades.", logger.info)
# REMOVED_UNUSED_CODE:             return trades_created
# REMOVED_UNUSED_CODE:         # Create entity and execute trade for each pair from whitelist
# REMOVED_UNUSED_CODE:         for pair in whitelist:
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 with self._exit_lock:
# REMOVED_UNUSED_CODE:                     trades_created += self.create_trade(pair)
# REMOVED_UNUSED_CODE:             except DependencyException as exception:
# REMOVED_UNUSED_CODE:                 logger.warning("Unable to create trade for %s: %s", pair, exception)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not trades_created:
# REMOVED_UNUSED_CODE:             logger.debug("Found no enter signals for whitelisted currencies. Trying again...")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return trades_created
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def create_trade(self, pair: str) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check the implemented trading strategy for entry signals.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         If the pair triggers the enter signal a new trade record gets created
# REMOVED_UNUSED_CODE:         and the entry-order opening the trade gets issued towards the exchange.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :return: True if a trade has been created.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         logger.debug(f"create_trade for pair {pair}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         analyzed_df, _ = self.dataprovider.get_analyzed_dataframe(pair, self.strategy.timeframe)
# REMOVED_UNUSED_CODE:         nowtime = analyzed_df.iloc[-1]["date"] if len(analyzed_df) > 0 else None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # get_free_open_trades is checked before create_trade is called
# REMOVED_UNUSED_CODE:         # but it is still used here to prevent opening too many trades within one iteration
# REMOVED_UNUSED_CODE:         if not self.get_free_open_trades():
# REMOVED_UNUSED_CODE:             logger.debug(f"Can't open a new trade for {pair}: max number of trades is reached.")
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # running get_signal on historical data fetched
# REMOVED_UNUSED_CODE:         (signal, enter_tag) = self.strategy.get_entry_signal(
# REMOVED_UNUSED_CODE:             pair, self.strategy.timeframe, analyzed_df
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if signal:
# REMOVED_UNUSED_CODE:             if self.strategy.is_pair_locked(pair, candle_date=nowtime, side=signal):
# REMOVED_UNUSED_CODE:                 lock = PairLocks.get_pair_longest_lock(pair, nowtime, signal)
# REMOVED_UNUSED_CODE:                 if lock:
# REMOVED_UNUSED_CODE:                     self.log_once(
# REMOVED_UNUSED_CODE:                         f"Pair {pair} {lock.side} is locked until "
# REMOVED_UNUSED_CODE:                         f"{lock.lock_end_time.strftime(constants.DATETIME_PRINT_FORMAT)} "
# REMOVED_UNUSED_CODE:                         f"due to {lock.reason}.",
# REMOVED_UNUSED_CODE:                         logger.info,
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     self.log_once(f"Pair {pair} is currently locked.", logger.info)
# REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE:             stake_amount = self.wallets.get_trade_stake_amount(
# REMOVED_UNUSED_CODE:                 pair, self.config["max_open_trades"], self.edge
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             bid_check_dom = self.config.get("entry_pricing", {}).get("check_depth_of_market", {})
# REMOVED_UNUSED_CODE:             if (bid_check_dom.get("enabled", False)) and (
# REMOVED_UNUSED_CODE:                 bid_check_dom.get("bids_to_ask_delta", 0) > 0
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 if self._check_depth_of_market(pair, bid_check_dom, side=signal):
# REMOVED_UNUSED_CODE:                     return self.execute_entry(
# REMOVED_UNUSED_CODE:                         pair,
# REMOVED_UNUSED_CODE:                         stake_amount,
# REMOVED_UNUSED_CODE:                         enter_tag=enter_tag,
# REMOVED_UNUSED_CODE:                         is_short=(signal == SignalDirection.SHORT),
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             return self.execute_entry(
# REMOVED_UNUSED_CODE:                 pair, stake_amount, enter_tag=enter_tag, is_short=(signal == SignalDirection.SHORT)
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     #
# REMOVED_UNUSED_CODE:     # Modify positions / DCA logic and methods
# REMOVED_UNUSED_CODE:     #
# REMOVED_UNUSED_CODE:     def process_open_trade_positions(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Tries to execute additional buy or sell orders for open trades (positions)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Walk through each pair and check if it needs changes
# REMOVED_UNUSED_CODE:         for trade in Trade.get_open_trades():
# REMOVED_UNUSED_CODE:             # If there is any open orders, wait for them to finish.
# REMOVED_UNUSED_CODE:             # TODO Remove to allow mul open orders
# REMOVED_UNUSED_CODE:             if trade.has_open_position or trade.has_open_orders:
# REMOVED_UNUSED_CODE:                 # Do a wallets update (will be ratelimited to once per hour)
# REMOVED_UNUSED_CODE:                 self.wallets.update(False)
# REMOVED_UNUSED_CODE:                 try:
# REMOVED_UNUSED_CODE:                     self.check_and_call_adjust_trade_position(trade)
# REMOVED_UNUSED_CODE:                 except DependencyException as exception:
# REMOVED_UNUSED_CODE:                     logger.warning(
# REMOVED_UNUSED_CODE:                         f"Unable to adjust position of trade for {trade.pair}: {exception}"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def check_and_call_adjust_trade_position(self, trade: Trade):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check the implemented trading strategy for adjustment command.
# REMOVED_UNUSED_CODE:         If the strategy triggers the adjustment, a new order gets issued.
# REMOVED_UNUSED_CODE:         Once that completes, the existing trade is modified to match new data.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         current_entry_rate, current_exit_rate = self.exchange.get_rates(
# REMOVED_UNUSED_CODE:             trade.pair, True, trade.is_short
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         current_entry_profit = trade.calc_profit_ratio(current_entry_rate)
# REMOVED_UNUSED_CODE:         current_exit_profit = trade.calc_profit_ratio(current_exit_rate)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         min_entry_stake = self.exchange.get_min_pair_stake_amount(
# REMOVED_UNUSED_CODE:             trade.pair, current_entry_rate, 0.0
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         min_exit_stake = self.exchange.get_min_pair_stake_amount(
# REMOVED_UNUSED_CODE:             trade.pair, current_exit_rate, self.strategy.stoploss
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         max_entry_stake = self.exchange.get_max_pair_stake_amount(trade.pair, current_entry_rate)
# REMOVED_UNUSED_CODE:         stake_available = self.wallets.get_available_stake_amount()
# REMOVED_UNUSED_CODE:         logger.debug(f"Calling adjust_trade_position for pair {trade.pair}")
# REMOVED_UNUSED_CODE:         stake_amount, order_tag = self.strategy._adjust_trade_position_internal(
# REMOVED_UNUSED_CODE:             trade=trade,
# REMOVED_UNUSED_CODE:             current_time=datetime.now(timezone.utc),
# REMOVED_UNUSED_CODE:             current_rate=current_entry_rate,
# REMOVED_UNUSED_CODE:             current_profit=current_entry_profit,
# REMOVED_UNUSED_CODE:             min_stake=min_entry_stake,
# REMOVED_UNUSED_CODE:             max_stake=min(max_entry_stake, stake_available),
# REMOVED_UNUSED_CODE:             current_entry_rate=current_entry_rate,
# REMOVED_UNUSED_CODE:             current_exit_rate=current_exit_rate,
# REMOVED_UNUSED_CODE:             current_entry_profit=current_entry_profit,
# REMOVED_UNUSED_CODE:             current_exit_profit=current_exit_profit,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if stake_amount is not None and stake_amount > 0.0:
# REMOVED_UNUSED_CODE:             # We should increase our position
# REMOVED_UNUSED_CODE:             if self.strategy.max_entry_position_adjustment > -1:
# REMOVED_UNUSED_CODE:                 count_of_entries = trade.nr_of_successful_entries
# REMOVED_UNUSED_CODE:                 if count_of_entries > self.strategy.max_entry_position_adjustment:
# REMOVED_UNUSED_CODE:                     logger.debug(f"Max adjustment entries for {trade.pair} has been reached.")
# REMOVED_UNUSED_CODE:                     return
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     logger.debug("Max adjustment entries is set to unlimited.")
# REMOVED_UNUSED_CODE:             self.execute_entry(
# REMOVED_UNUSED_CODE:                 trade.pair,
# REMOVED_UNUSED_CODE:                 stake_amount,
# REMOVED_UNUSED_CODE:                 price=current_entry_rate,
# REMOVED_UNUSED_CODE:                 trade=trade,
# REMOVED_UNUSED_CODE:                 is_short=trade.is_short,
# REMOVED_UNUSED_CODE:                 mode="pos_adjust",
# REMOVED_UNUSED_CODE:                 enter_tag=order_tag,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if stake_amount is not None and stake_amount < 0.0:
# REMOVED_UNUSED_CODE:             # We should decrease our position
# REMOVED_UNUSED_CODE:             amount = self.exchange.amount_to_contract_precision(
# REMOVED_UNUSED_CODE:                 trade.pair,
# REMOVED_UNUSED_CODE:                 abs(
# REMOVED_UNUSED_CODE:                     float(
# REMOVED_UNUSED_CODE:                         FtPrecise(stake_amount)
# REMOVED_UNUSED_CODE:                         * FtPrecise(trade.amount)
# REMOVED_UNUSED_CODE:                         / FtPrecise(trade.stake_amount)
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 ),
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if amount == 0.0:
# REMOVED_UNUSED_CODE:                 logger.info(
# REMOVED_UNUSED_CODE:                     f"Wanted to exit of {stake_amount} amount, "
# REMOVED_UNUSED_CODE:                     "but exit amount is now 0.0 due to exchange limits - not exiting."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             remaining = (trade.amount - amount) * current_exit_rate
# REMOVED_UNUSED_CODE:             if min_exit_stake and remaining != 0 and remaining < min_exit_stake:
# REMOVED_UNUSED_CODE:                 logger.info(
# REMOVED_UNUSED_CODE:                     f"Remaining amount of {remaining} would be smaller "
# REMOVED_UNUSED_CODE:                     f"than the minimum of {min_exit_stake}."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.execute_trade_exit(
# REMOVED_UNUSED_CODE:                 trade,
# REMOVED_UNUSED_CODE:                 current_exit_rate,
# REMOVED_UNUSED_CODE:                 exit_check=ExitCheckTuple(exit_type=ExitType.PARTIAL_EXIT),
# REMOVED_UNUSED_CODE:                 sub_trade_amt=amount,
# REMOVED_UNUSED_CODE:                 exit_tag=order_tag,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _check_depth_of_market(self, pair: str, conf: dict, side: SignalDirection) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Checks depth of market before executing an entry
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         conf_bids_to_ask_delta = conf.get("bids_to_ask_delta", 0)
# REMOVED_UNUSED_CODE:         logger.info(f"Checking depth of market for {pair} ...")
# REMOVED_UNUSED_CODE:         order_book = self.exchange.fetch_l2_order_book(pair, 1000)
# REMOVED_UNUSED_CODE:         order_book_data_frame = order_book_to_dataframe(order_book["bids"], order_book["asks"])
# REMOVED_UNUSED_CODE:         order_book_bids = order_book_data_frame["b_size"].sum()
# REMOVED_UNUSED_CODE:         order_book_asks = order_book_data_frame["a_size"].sum()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         entry_side = order_book_bids if side == SignalDirection.LONG else order_book_asks
# REMOVED_UNUSED_CODE:         exit_side = order_book_asks if side == SignalDirection.LONG else order_book_bids
# REMOVED_UNUSED_CODE:         bids_ask_delta = entry_side / exit_side
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         bids = f"Bids: {order_book_bids}"
# REMOVED_UNUSED_CODE:         asks = f"Asks: {order_book_asks}"
# REMOVED_UNUSED_CODE:         delta = f"Delta: {bids_ask_delta}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.info(
# REMOVED_UNUSED_CODE:             f"{bids}, {asks}, {delta}, Direction: {side.value} "
# REMOVED_UNUSED_CODE:             f"Bid Price: {order_book['bids'][0][0]}, Ask Price: {order_book['asks'][0][0]}, "
# REMOVED_UNUSED_CODE:             f"Immediate Bid Quantity: {order_book['bids'][0][1]}, "
# REMOVED_UNUSED_CODE:             f"Immediate Ask Quantity: {order_book['asks'][0][1]}."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         if bids_ask_delta >= conf_bids_to_ask_delta:
# REMOVED_UNUSED_CODE:             logger.info(f"Bids to asks delta for {pair} DOES satisfy condition.")
# REMOVED_UNUSED_CODE:             return True
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.info(f"Bids to asks delta for {pair} does not satisfy condition.")
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def execute_entry(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         stake_amount: float,
# REMOVED_UNUSED_CODE:         price: float | None = None,
# REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE:         is_short: bool = False,
# REMOVED_UNUSED_CODE:         ordertype: str | None = None,
# REMOVED_UNUSED_CODE:         enter_tag: str | None = None,
# REMOVED_UNUSED_CODE:         trade: Trade | None = None,
# REMOVED_UNUSED_CODE:         mode: EntryExecuteMode = "initial",
# REMOVED_UNUSED_CODE:         leverage_: float | None = None,
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Executes an entry for the given pair
# REMOVED_UNUSED_CODE:         :param pair: pair for which we want to create a LIMIT order
# REMOVED_UNUSED_CODE:         :param stake_amount: amount of stake-currency for the pair
# REMOVED_UNUSED_CODE:         :return: True if an entry order is created, False if it fails.
# REMOVED_UNUSED_CODE:         :raise: DependencyException or it's subclasses like ExchangeError.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         time_in_force = self.strategy.order_time_in_force["entry"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         side: BuySell = "sell" if is_short else "buy"
# REMOVED_UNUSED_CODE:         name = "Short" if is_short else "Long"
# REMOVED_UNUSED_CODE:         trade_side: LongShort = "short" if is_short else "long"
# REMOVED_UNUSED_CODE:         pos_adjust = trade is not None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         enter_limit_requested, stake_amount, leverage = self.get_valid_enter_price_and_stake(
# REMOVED_UNUSED_CODE:             pair, price, stake_amount, trade_side, enter_tag, trade, mode, leverage_
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not stake_amount:
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         msg = (
# REMOVED_UNUSED_CODE:             f"Position adjust: about to create a new order for {pair} with stake_amount: "
# REMOVED_UNUSED_CODE:             f"{stake_amount} for {trade}"
# REMOVED_UNUSED_CODE:             if mode == "pos_adjust"
# REMOVED_UNUSED_CODE:             else (
# REMOVED_UNUSED_CODE:                 f"Replacing {side} order: about create a new order for {pair} with stake_amount: "
# REMOVED_UNUSED_CODE:                 f"{stake_amount} ..."
# REMOVED_UNUSED_CODE:                 if mode == "replace"
# REMOVED_UNUSED_CODE:                 else f"{name} signal found: about create a new trade for {pair} with stake_amount: "
# REMOVED_UNUSED_CODE:                 f"{stake_amount} ..."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         logger.info(msg)
# REMOVED_UNUSED_CODE:         amount = (stake_amount / enter_limit_requested) * leverage
# REMOVED_UNUSED_CODE:         order_type = ordertype or self.strategy.order_types["entry"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if mode == "initial" and not strategy_safe_wrapper(
# REMOVED_UNUSED_CODE:             self.strategy.confirm_trade_entry, default_retval=True
# REMOVED_UNUSED_CODE:         )(
# REMOVED_UNUSED_CODE:             pair=pair,
# REMOVED_UNUSED_CODE:             order_type=order_type,
# REMOVED_UNUSED_CODE:             amount=amount,
# REMOVED_UNUSED_CODE:             rate=enter_limit_requested,
# REMOVED_UNUSED_CODE:             time_in_force=time_in_force,
# REMOVED_UNUSED_CODE:             current_time=datetime.now(timezone.utc),
# REMOVED_UNUSED_CODE:             entry_tag=enter_tag,
# REMOVED_UNUSED_CODE:             side=trade_side,
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             logger.info(f"User denied entry for {pair}.")
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if trade and self.handle_similar_open_order(trade, enter_limit_requested, amount, side):
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         order = self.exchange.create_order(
# REMOVED_UNUSED_CODE:             pair=pair,
# REMOVED_UNUSED_CODE:             ordertype=order_type,
# REMOVED_UNUSED_CODE:             side=side,
# REMOVED_UNUSED_CODE:             amount=amount,
# REMOVED_UNUSED_CODE:             rate=enter_limit_requested,
# REMOVED_UNUSED_CODE:             reduceOnly=False,
# REMOVED_UNUSED_CODE:             time_in_force=time_in_force,
# REMOVED_UNUSED_CODE:             leverage=leverage,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         order_obj = Order.parse_from_ccxt_object(order, pair, side, amount, enter_limit_requested)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         order_obj.ft_order_tag = enter_tag
# REMOVED_UNUSED_CODE:         order_id = order["id"]
# REMOVED_UNUSED_CODE:         order_status = order.get("status")
# REMOVED_UNUSED_CODE:         logger.info(f"Order {order_id} was created for {pair} and status is {order_status}.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # we assume the order is executed at the price requested
# REMOVED_UNUSED_CODE:         enter_limit_filled_price = enter_limit_requested
# REMOVED_UNUSED_CODE:         amount_requested = amount
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if order_status == "expired" or order_status == "rejected":
# REMOVED_UNUSED_CODE:             # return false if the order is not filled
# REMOVED_UNUSED_CODE:             if float(order["filled"]) == 0:
# REMOVED_UNUSED_CODE:                 logger.warning(
# REMOVED_UNUSED_CODE:                     f"{name} {time_in_force} order with time in force {order_type} "
# REMOVED_UNUSED_CODE:                     f"for {pair} is {order_status} by {self.exchange.name}."
# REMOVED_UNUSED_CODE:                     " zero amount is fulfilled."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 # the order is partially fulfilled
# REMOVED_UNUSED_CODE:                 # in case of IOC orders we can check immediately
# REMOVED_UNUSED_CODE:                 # if the order is fulfilled fully or partially
# REMOVED_UNUSED_CODE:                 logger.warning(
# REMOVED_UNUSED_CODE:                     "%s %s order with time in force %s for %s is %s by %s."
# REMOVED_UNUSED_CODE:                     " %s amount fulfilled out of %s (%s remaining which is canceled).",
# REMOVED_UNUSED_CODE:                     name,
# REMOVED_UNUSED_CODE:                     time_in_force,
# REMOVED_UNUSED_CODE:                     order_type,
# REMOVED_UNUSED_CODE:                     pair,
# REMOVED_UNUSED_CODE:                     order_status,
# REMOVED_UNUSED_CODE:                     self.exchange.name,
# REMOVED_UNUSED_CODE:                     order["filled"],
# REMOVED_UNUSED_CODE:                     order["amount"],
# REMOVED_UNUSED_CODE:                     order["remaining"],
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 amount = safe_value_fallback(order, "filled", "amount", amount)
# REMOVED_UNUSED_CODE:                 enter_limit_filled_price = safe_value_fallback(
# REMOVED_UNUSED_CODE:                     order, "average", "price", enter_limit_filled_price
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # in case of FOK the order may be filled immediately and fully
# REMOVED_UNUSED_CODE:         elif order_status == "closed":
# REMOVED_UNUSED_CODE:             amount = safe_value_fallback(order, "filled", "amount", amount)
# REMOVED_UNUSED_CODE:             enter_limit_filled_price = safe_value_fallback(
# REMOVED_UNUSED_CODE:                 order, "average", "price", enter_limit_requested
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Fee is applied twice because we make a LIMIT_BUY and LIMIT_SELL
# REMOVED_UNUSED_CODE:         fee = self.exchange.get_fee(symbol=pair, taker_or_maker="maker")
# REMOVED_UNUSED_CODE:         base_currency = self.exchange.get_pair_base_currency(pair)
# REMOVED_UNUSED_CODE:         open_date = datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         funding_fees = self.exchange.get_funding_fees(
# REMOVED_UNUSED_CODE:             pair=pair,
# REMOVED_UNUSED_CODE:             amount=amount + trade.amount if trade else amount,
# REMOVED_UNUSED_CODE:             is_short=is_short,
# REMOVED_UNUSED_CODE:             open_date=trade.date_last_filled_utc if trade else open_date,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # This is a new trade
# REMOVED_UNUSED_CODE:         if trade is None:
# REMOVED_UNUSED_CODE:             trade = Trade(
# REMOVED_UNUSED_CODE:                 pair=pair,
# REMOVED_UNUSED_CODE:                 base_currency=base_currency,
# REMOVED_UNUSED_CODE:                 stake_currency=self.config["stake_currency"],
# REMOVED_UNUSED_CODE:                 stake_amount=stake_amount,
# REMOVED_UNUSED_CODE:                 amount=0,
# REMOVED_UNUSED_CODE:                 is_open=True,
# REMOVED_UNUSED_CODE:                 amount_requested=amount_requested,
# REMOVED_UNUSED_CODE:                 fee_open=fee,
# REMOVED_UNUSED_CODE:                 fee_close=fee,
# REMOVED_UNUSED_CODE:                 open_rate=enter_limit_filled_price,
# REMOVED_UNUSED_CODE:                 open_rate_requested=enter_limit_requested,
# REMOVED_UNUSED_CODE:                 open_date=open_date,
# REMOVED_UNUSED_CODE:                 exchange=self.exchange.id,
# REMOVED_UNUSED_CODE:                 strategy=self.strategy.get_strategy_name(),
# REMOVED_UNUSED_CODE:                 enter_tag=enter_tag,
# REMOVED_UNUSED_CODE:                 timeframe=timeframe_to_minutes(self.config["timeframe"]),
# REMOVED_UNUSED_CODE:                 leverage=leverage,
# REMOVED_UNUSED_CODE:                 is_short=is_short,
# REMOVED_UNUSED_CODE:                 trading_mode=self.trading_mode,
# REMOVED_UNUSED_CODE:                 funding_fees=funding_fees,
# REMOVED_UNUSED_CODE:                 amount_precision=self.exchange.get_precision_amount(pair),
# REMOVED_UNUSED_CODE:                 price_precision=self.exchange.get_precision_price(pair),
# REMOVED_UNUSED_CODE:                 precision_mode=self.exchange.precisionMode,
# REMOVED_UNUSED_CODE:                 precision_mode_price=self.exchange.precision_mode_price,
# REMOVED_UNUSED_CODE:                 contract_size=self.exchange.get_contract_size(pair),
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             stoploss = self.strategy.stoploss if not self.edge else self.edge.get_stoploss(pair)
# REMOVED_UNUSED_CODE:             trade.adjust_stop_loss(trade.open_rate, stoploss, initial=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # This is additional entry, we reset fee_open_currency so timeout checking can work
# REMOVED_UNUSED_CODE:             trade.is_open = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade.fee_open_currency = None
# REMOVED_UNUSED_CODE:             trade.set_funding_fees(funding_fees)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trade.orders.append(order_obj)
# REMOVED_UNUSED_CODE:         trade.recalc_trade_from_orders()
# REMOVED_UNUSED_CODE:         Trade.session.add(trade)
# REMOVED_UNUSED_CODE:         Trade.commit()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Updating wallets
# REMOVED_UNUSED_CODE:         self.wallets.update()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._notify_enter(trade, order_obj, order_type, sub_trade=pos_adjust)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if pos_adjust:
# REMOVED_UNUSED_CODE:             if order_status == "closed":
# REMOVED_UNUSED_CODE:                 logger.info(f"DCA order closed, trade should be up to date: {trade}")
# REMOVED_UNUSED_CODE:                 trade = self.cancel_stoploss_on_exchange(trade)
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 logger.info(f"DCA order {order_status}, will wait for resolution: {trade}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Update fees if order is non-opened
# REMOVED_UNUSED_CODE:         if order_status in constants.NON_OPEN_EXCHANGE_STATES:
# REMOVED_UNUSED_CODE:             fully_canceled = self.update_trade_state(trade, order_id, order)
# REMOVED_UNUSED_CODE:             if fully_canceled and mode != "replace":
# REMOVED_UNUSED_CODE:                 # Fully canceled orders, may happen with some time in force setups (IOC).
# REMOVED_UNUSED_CODE:                 # Should be handled immediately.
# REMOVED_UNUSED_CODE:                 self.handle_cancel_enter(
# REMOVED_UNUSED_CODE:                     trade, order, order_obj, constants.CANCEL_REASON["TIMEOUT"]
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def cancel_stoploss_on_exchange(self, trade: Trade) -> Trade:
# REMOVED_UNUSED_CODE:         # First cancelling stoploss on exchange ...
# REMOVED_UNUSED_CODE:         for oslo in trade.open_sl_orders:
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 logger.info(f"Cancelling stoploss on exchange for {trade} order: {oslo.order_id}")
# REMOVED_UNUSED_CODE:                 co = self.exchange.cancel_stoploss_order_with_result(
# REMOVED_UNUSED_CODE:                     oslo.order_id, trade.pair, trade.amount
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 self.update_trade_state(trade, oslo.order_id, co, stoploss_order=True)
# REMOVED_UNUSED_CODE:             except InvalidOrderException:
# REMOVED_UNUSED_CODE:                 logger.exception(
# REMOVED_UNUSED_CODE:                     f"Could not cancel stoploss order {oslo.order_id} for pair {trade.pair}"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:         return trade
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_valid_enter_price_and_stake(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         price: float | None,
# REMOVED_UNUSED_CODE:         stake_amount: float,
# REMOVED_UNUSED_CODE:         trade_side: LongShort,
# REMOVED_UNUSED_CODE:         entry_tag: str | None,
# REMOVED_UNUSED_CODE:         trade: Trade | None,
# REMOVED_UNUSED_CODE:         mode: EntryExecuteMode,
# REMOVED_UNUSED_CODE:         leverage_: float | None,
# REMOVED_UNUSED_CODE:     ) -> tuple[float, float, float]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Validate and eventually adjust (within limits) limit, amount and leverage
# REMOVED_UNUSED_CODE:         :return: Tuple with (price, amount, leverage)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if price:
# REMOVED_UNUSED_CODE:             enter_limit_requested = price
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # Calculate price
# REMOVED_UNUSED_CODE:             enter_limit_requested = self.exchange.get_rate(
# REMOVED_UNUSED_CODE:                 pair, side="entry", is_short=(trade_side == "short"), refresh=True
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         if mode != "replace":
# REMOVED_UNUSED_CODE:             # Don't call custom_entry_price in order-adjust scenario
# REMOVED_UNUSED_CODE:             custom_entry_price = strategy_safe_wrapper(
# REMOVED_UNUSED_CODE:                 self.strategy.custom_entry_price, default_retval=enter_limit_requested
# REMOVED_UNUSED_CODE:             )(
# REMOVED_UNUSED_CODE:                 pair=pair,
# REMOVED_UNUSED_CODE:                 trade=trade,
# REMOVED_UNUSED_CODE:                 current_time=datetime.now(timezone.utc),
# REMOVED_UNUSED_CODE:                 proposed_rate=enter_limit_requested,
# REMOVED_UNUSED_CODE:                 entry_tag=entry_tag,
# REMOVED_UNUSED_CODE:                 side=trade_side,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             enter_limit_requested = self.get_valid_price(custom_entry_price, enter_limit_requested)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not enter_limit_requested:
# REMOVED_UNUSED_CODE:             raise PricingError("Could not determine entry price.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.trading_mode != TradingMode.SPOT and trade is None:
# REMOVED_UNUSED_CODE:             max_leverage = self.exchange.get_max_leverage(pair, stake_amount)
# REMOVED_UNUSED_CODE:             if leverage_:
# REMOVED_UNUSED_CODE:                 leverage = leverage_
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 leverage = strategy_safe_wrapper(self.strategy.leverage, default_retval=1.0)(
# REMOVED_UNUSED_CODE:                     pair=pair,
# REMOVED_UNUSED_CODE:                     current_time=datetime.now(timezone.utc),
# REMOVED_UNUSED_CODE:                     current_rate=enter_limit_requested,
# REMOVED_UNUSED_CODE:                     proposed_leverage=1.0,
# REMOVED_UNUSED_CODE:                     max_leverage=max_leverage,
# REMOVED_UNUSED_CODE:                     side=trade_side,
# REMOVED_UNUSED_CODE:                     entry_tag=entry_tag,
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             # Cap leverage between 1.0 and max_leverage.
# REMOVED_UNUSED_CODE:             leverage = min(max(leverage, 1.0), max_leverage)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # Changing leverage currently not possible
# REMOVED_UNUSED_CODE:             leverage = trade.leverage if trade else 1.0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Min-stake-amount should actually include Leverage - this way our "minimal"
# REMOVED_UNUSED_CODE:         # stake- amount might be higher than necessary.
# REMOVED_UNUSED_CODE:         # We do however also need min-stake to determine leverage, therefore this is ignored as
# REMOVED_UNUSED_CODE:         # edge-case for now.
# REMOVED_UNUSED_CODE:         min_stake_amount = self.exchange.get_min_pair_stake_amount(
# REMOVED_UNUSED_CODE:             pair,
# REMOVED_UNUSED_CODE:             enter_limit_requested,
# REMOVED_UNUSED_CODE:             self.strategy.stoploss if not mode == "pos_adjust" else 0.0,
# REMOVED_UNUSED_CODE:             leverage,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         max_stake_amount = self.exchange.get_max_pair_stake_amount(
# REMOVED_UNUSED_CODE:             pair, enter_limit_requested, leverage
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not self.edge and trade is None:
# REMOVED_UNUSED_CODE:             stake_available = self.wallets.get_available_stake_amount()
# REMOVED_UNUSED_CODE:             stake_amount = strategy_safe_wrapper(
# REMOVED_UNUSED_CODE:                 self.strategy.custom_stake_amount, default_retval=stake_amount
# REMOVED_UNUSED_CODE:             )(
# REMOVED_UNUSED_CODE:                 pair=pair,
# REMOVED_UNUSED_CODE:                 current_time=datetime.now(timezone.utc),
# REMOVED_UNUSED_CODE:                 current_rate=enter_limit_requested,
# REMOVED_UNUSED_CODE:                 proposed_stake=stake_amount,
# REMOVED_UNUSED_CODE:                 min_stake=min_stake_amount,
# REMOVED_UNUSED_CODE:                 max_stake=min(max_stake_amount, stake_available),
# REMOVED_UNUSED_CODE:                 leverage=leverage,
# REMOVED_UNUSED_CODE:                 entry_tag=entry_tag,
# REMOVED_UNUSED_CODE:                 side=trade_side,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         stake_amount = self.wallets.validate_stake_amount(
# REMOVED_UNUSED_CODE:             pair=pair,
# REMOVED_UNUSED_CODE:             stake_amount=stake_amount,
# REMOVED_UNUSED_CODE:             min_stake_amount=min_stake_amount,
# REMOVED_UNUSED_CODE:             max_stake_amount=max_stake_amount,
# REMOVED_UNUSED_CODE:             trade_amount=trade.stake_amount if trade else None,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return enter_limit_requested, stake_amount, leverage
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _notify_enter(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE:         order: Order,
# REMOVED_UNUSED_CODE:         order_type: str | None,
# REMOVED_UNUSED_CODE:         fill: bool = False,
# REMOVED_UNUSED_CODE:         sub_trade: bool = False,
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Sends rpc notification when a entry order occurred.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         open_rate = order.safe_price
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if open_rate is None:
# REMOVED_UNUSED_CODE:             open_rate = trade.open_rate
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         current_rate = self.exchange.get_rate(
# REMOVED_UNUSED_CODE:             trade.pair, side="entry", is_short=trade.is_short, refresh=False
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         stake_amount = trade.stake_amount
# REMOVED_UNUSED_CODE:         if not fill and trade.nr_of_successful_entries > 0:
# REMOVED_UNUSED_CODE:             # If we have open orders, we need to add the stake amount of the open orders
# REMOVED_UNUSED_CODE:             # as it's not yet included in the trade.stake_amount
# REMOVED_UNUSED_CODE:             stake_amount += sum(
# REMOVED_UNUSED_CODE:                 o.stake_amount for o in trade.open_orders if o.ft_order_side == trade.entry_side
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         msg: RPCEntryMsg = {
# REMOVED_UNUSED_CODE:             "trade_id": trade.id,
# REMOVED_UNUSED_CODE:             "type": RPCMessageType.ENTRY_FILL if fill else RPCMessageType.ENTRY,
# REMOVED_UNUSED_CODE:             "buy_tag": trade.enter_tag,
# REMOVED_UNUSED_CODE:             "enter_tag": trade.enter_tag,
# REMOVED_UNUSED_CODE:             "exchange": trade.exchange.capitalize(),
# REMOVED_UNUSED_CODE:             "pair": trade.pair,
# REMOVED_UNUSED_CODE:             "leverage": trade.leverage if trade.leverage else None,
# REMOVED_UNUSED_CODE:             "direction": "Short" if trade.is_short else "Long",
# REMOVED_UNUSED_CODE:             "limit": open_rate,  # Deprecated (?)
# REMOVED_UNUSED_CODE:             "open_rate": open_rate,
# REMOVED_UNUSED_CODE:             "order_type": order_type or "unknown",
# REMOVED_UNUSED_CODE:             "stake_amount": stake_amount,
# REMOVED_UNUSED_CODE:             "stake_currency": self.config["stake_currency"],
# REMOVED_UNUSED_CODE:             "base_currency": self.exchange.get_pair_base_currency(trade.pair),
# REMOVED_UNUSED_CODE:             "quote_currency": self.exchange.get_pair_quote_currency(trade.pair),
# REMOVED_UNUSED_CODE:             "fiat_currency": self.config.get("fiat_display_currency", None),
# REMOVED_UNUSED_CODE:             "amount": order.safe_amount_after_fee if fill else (order.safe_amount or trade.amount),
# REMOVED_UNUSED_CODE:             "open_date": trade.open_date_utc or datetime.now(timezone.utc),
# REMOVED_UNUSED_CODE:             "current_rate": current_rate,
# REMOVED_UNUSED_CODE:             "sub_trade": sub_trade,
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Send the message
# REMOVED_UNUSED_CODE:         self.rpc.send_msg(msg)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _notify_enter_cancel(
# REMOVED_UNUSED_CODE:         self, trade: Trade, order_type: str, reason: str, sub_trade: bool = False
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Sends rpc notification when a entry order cancel occurred.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         current_rate = self.exchange.get_rate(
# REMOVED_UNUSED_CODE:             trade.pair, side="entry", is_short=trade.is_short, refresh=False
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         msg: RPCCancelMsg = {
# REMOVED_UNUSED_CODE:             "trade_id": trade.id,
# REMOVED_UNUSED_CODE:             "type": RPCMessageType.ENTRY_CANCEL,
# REMOVED_UNUSED_CODE:             "buy_tag": trade.enter_tag,
# REMOVED_UNUSED_CODE:             "enter_tag": trade.enter_tag,
# REMOVED_UNUSED_CODE:             "exchange": trade.exchange.capitalize(),
# REMOVED_UNUSED_CODE:             "pair": trade.pair,
# REMOVED_UNUSED_CODE:             "leverage": trade.leverage,
# REMOVED_UNUSED_CODE:             "direction": "Short" if trade.is_short else "Long",
# REMOVED_UNUSED_CODE:             "limit": trade.open_rate,
# REMOVED_UNUSED_CODE:             "order_type": order_type,
# REMOVED_UNUSED_CODE:             "stake_amount": trade.stake_amount,
# REMOVED_UNUSED_CODE:             "open_rate": trade.open_rate,
# REMOVED_UNUSED_CODE:             "stake_currency": self.config["stake_currency"],
# REMOVED_UNUSED_CODE:             "base_currency": self.exchange.get_pair_base_currency(trade.pair),
# REMOVED_UNUSED_CODE:             "quote_currency": self.exchange.get_pair_quote_currency(trade.pair),
# REMOVED_UNUSED_CODE:             "fiat_currency": self.config.get("fiat_display_currency", None),
# REMOVED_UNUSED_CODE:             "amount": trade.amount,
# REMOVED_UNUSED_CODE:             "open_date": trade.open_date,
# REMOVED_UNUSED_CODE:             "current_rate": current_rate,
# REMOVED_UNUSED_CODE:             "reason": reason,
# REMOVED_UNUSED_CODE:             "sub_trade": sub_trade,
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Send the message
# REMOVED_UNUSED_CODE:         self.rpc.send_msg(msg)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     #
# REMOVED_UNUSED_CODE:     # SELL / exit positions / close trades logic and methods
# REMOVED_UNUSED_CODE:     #
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def exit_positions(self, trades: list[Trade]) -> int:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Tries to execute exit orders for open trades (positions)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         trades_closed = 0
# REMOVED_UNUSED_CODE:         for trade in trades:
# REMOVED_UNUSED_CODE:             if (
# REMOVED_UNUSED_CODE:                 not trade.has_open_orders
# REMOVED_UNUSED_CODE:                 and not trade.has_open_sl_orders
# REMOVED_UNUSED_CODE:                 and not self.wallets.check_exit_amount(trade)
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 logger.warning(
# REMOVED_UNUSED_CODE:                     f"Not enough {trade.safe_base_currency} in wallet to exit {trade}. "
# REMOVED_UNUSED_CODE:                     "Trying to recover."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 if self.handle_onexchange_order(trade):
# REMOVED_UNUSED_CODE:                     # Trade was deleted. Don't continue.
# REMOVED_UNUSED_CODE:                     continue
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 try:
# REMOVED_UNUSED_CODE:                     if self.strategy.order_types.get(
# REMOVED_UNUSED_CODE:                         "stoploss_on_exchange"
# REMOVED_UNUSED_CODE:                     ) and self.handle_stoploss_on_exchange(trade):
# REMOVED_UNUSED_CODE:                         trades_closed += 1
# REMOVED_UNUSED_CODE:                         Trade.commit()
# REMOVED_UNUSED_CODE:                         continue
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 except InvalidOrderException as exception:
# REMOVED_UNUSED_CODE:                     logger.warning(
# REMOVED_UNUSED_CODE:                         f"Unable to handle stoploss on exchange for {trade.pair}: {exception}"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 # Check if we can exit our current position for this trade
# REMOVED_UNUSED_CODE:                 if trade.has_open_position and trade.is_open and self.handle_trade(trade):
# REMOVED_UNUSED_CODE:                     trades_closed += 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             except DependencyException as exception:
# REMOVED_UNUSED_CODE:                 logger.warning(f"Unable to exit trade {trade.pair}: {exception}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Updating wallets if any trade occurred
# REMOVED_UNUSED_CODE:         if trades_closed:
# REMOVED_UNUSED_CODE:             self.wallets.update()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return trades_closed
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def handle_trade(self, trade: Trade) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Exits the current pair if the threshold is reached and updates the trade record.
# REMOVED_UNUSED_CODE:         :return: True if trade has been sold/exited_short, False otherwise
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not trade.is_open:
# REMOVED_UNUSED_CODE:             raise DependencyException(f"Attempt to handle closed trade: {trade}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.debug("Handling %s ...", trade)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         (enter, exit_) = (False, False)
# REMOVED_UNUSED_CODE:         exit_tag = None
# REMOVED_UNUSED_CODE:         exit_signal_type = "exit_short" if trade.is_short else "exit_long"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.config.get("use_exit_signal", True) or self.config.get(
# REMOVED_UNUSED_CODE:             "ignore_roi_if_entry_signal", False
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             analyzed_df, _ = self.dataprovider.get_analyzed_dataframe(
# REMOVED_UNUSED_CODE:                 trade.pair, self.strategy.timeframe
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             (enter, exit_, exit_tag) = self.strategy.get_exit_signal(
# REMOVED_UNUSED_CODE:                 trade.pair, self.strategy.timeframe, analyzed_df, is_short=trade.is_short
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.debug("checking exit")
# REMOVED_UNUSED_CODE:         exit_rate = self.exchange.get_rate(
# REMOVED_UNUSED_CODE:             trade.pair, side="exit", is_short=trade.is_short, refresh=True
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         if self._check_and_execute_exit(trade, exit_rate, enter, exit_, exit_tag):
# REMOVED_UNUSED_CODE:             return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.debug(f"Found no {exit_signal_type} signal for %s.", trade)
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _check_and_execute_exit(
# REMOVED_UNUSED_CODE:         self, trade: Trade, exit_rate: float, enter: bool, exit_: bool, exit_tag: str | None
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check and execute trade exit
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         exits: list[ExitCheckTuple] = self.strategy.should_exit(
# REMOVED_UNUSED_CODE:             trade,
# REMOVED_UNUSED_CODE:             exit_rate,
# REMOVED_UNUSED_CODE:             datetime.now(timezone.utc),
# REMOVED_UNUSED_CODE:             enter=enter,
# REMOVED_UNUSED_CODE:             exit_=exit_,
# REMOVED_UNUSED_CODE:             force_stoploss=self.edge.get_stoploss(trade.pair) if self.edge else 0,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         for should_exit in exits:
# REMOVED_UNUSED_CODE:             if should_exit.exit_flag:
# REMOVED_UNUSED_CODE:                 exit_tag1 = exit_tag if should_exit.exit_type == ExitType.EXIT_SIGNAL else None
# REMOVED_UNUSED_CODE:                 logger.info(
# REMOVED_UNUSED_CODE:                     f"Exit for {trade.pair} detected. Reason: {should_exit.exit_type}"
# REMOVED_UNUSED_CODE:                     f"{f' Tag: {exit_tag1}' if exit_tag1 is not None else ''}"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 exited = self.execute_trade_exit(trade, exit_rate, should_exit, exit_tag=exit_tag1)
# REMOVED_UNUSED_CODE:                 if exited:
# REMOVED_UNUSED_CODE:                     return True
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def create_stoploss_order(self, trade: Trade, stop_price: float) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Abstracts creating stoploss orders from the logic.
# REMOVED_UNUSED_CODE:         Handles errors and updates the trade database object.
# REMOVED_UNUSED_CODE:         Force-sells the pair (using EmergencySell reason) in case of Problems creating the order.
# REMOVED_UNUSED_CODE:         :return: True if the order succeeded, and False in case of problems.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             stoploss_order = self.exchange.create_stoploss(
# REMOVED_UNUSED_CODE:                 pair=trade.pair,
# REMOVED_UNUSED_CODE:                 amount=trade.amount,
# REMOVED_UNUSED_CODE:                 stop_price=stop_price,
# REMOVED_UNUSED_CODE:                 order_types=self.strategy.order_types,
# REMOVED_UNUSED_CODE:                 side=trade.exit_side,
# REMOVED_UNUSED_CODE:                 leverage=trade.leverage,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             order_obj = Order.parse_from_ccxt_object(
# REMOVED_UNUSED_CODE:                 stoploss_order, trade.pair, "stoploss", trade.amount, stop_price
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             trade.orders.append(order_obj)
# REMOVED_UNUSED_CODE:             return True
# REMOVED_UNUSED_CODE:         except InsufficientFundsError as e:
# REMOVED_UNUSED_CODE:             logger.warning(f"Unable to place stoploss order {e}.")
# REMOVED_UNUSED_CODE:             # Try to figure out what went wrong
# REMOVED_UNUSED_CODE:             self.handle_insufficient_funds(trade)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         except InvalidOrderException as e:
# REMOVED_UNUSED_CODE:             logger.error(f"Unable to place a stoploss order on exchange. {e}")
# REMOVED_UNUSED_CODE:             logger.warning("Exiting the trade forcefully")
# REMOVED_UNUSED_CODE:             self.emergency_exit(trade, stop_price)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         except ExchangeError:
# REMOVED_UNUSED_CODE:             logger.exception("Unable to place a stoploss order on exchange.")
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def handle_stoploss_on_exchange(self, trade: Trade) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check if trade is fulfilled in which case the stoploss
# REMOVED_UNUSED_CODE:         on exchange should be added immediately if stoploss on exchange
# REMOVED_UNUSED_CODE:         is enabled.
# REMOVED_UNUSED_CODE:         # TODO: liquidation price always on exchange, even without stoploss_on_exchange
# REMOVED_UNUSED_CODE:         # Therefore fetching account liquidations for open pairs may make sense.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.debug("Handling stoploss on exchange %s ...", trade)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         stoploss_orders = []
# REMOVED_UNUSED_CODE:         for slo in trade.open_sl_orders:
# REMOVED_UNUSED_CODE:             stoploss_order = None
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 # First we check if there is already a stoploss on exchange
# REMOVED_UNUSED_CODE:                 stoploss_order = (
# REMOVED_UNUSED_CODE:                     self.exchange.fetch_stoploss_order(slo.order_id, trade.pair)
# REMOVED_UNUSED_CODE:                     if slo.order_id
# REMOVED_UNUSED_CODE:                     else None
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             except InvalidOrderException as exception:
# REMOVED_UNUSED_CODE:                 logger.warning("Unable to fetch stoploss order: %s", exception)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if stoploss_order:
# REMOVED_UNUSED_CODE:                 stoploss_orders.append(stoploss_order)
# REMOVED_UNUSED_CODE:                 self.update_trade_state(trade, slo.order_id, stoploss_order, stoploss_order=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # We check if stoploss order is fulfilled
# REMOVED_UNUSED_CODE:             if stoploss_order and stoploss_order["status"] in ("closed", "triggered"):
# REMOVED_UNUSED_CODE:                 trade.exit_reason = ExitType.STOPLOSS_ON_EXCHANGE.value
# REMOVED_UNUSED_CODE:                 self._notify_exit(trade, "stoploss", True)
# REMOVED_UNUSED_CODE:                 self.handle_protections(trade.pair, trade.trade_direction)
# REMOVED_UNUSED_CODE:                 return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not trade.has_open_position or not trade.is_open:
# REMOVED_UNUSED_CODE:             # The trade can be closed already (sell-order fill confirmation came in this iteration)
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # If enter order is fulfilled but there is no stoploss, we add a stoploss on exchange
# REMOVED_UNUSED_CODE:         if len(stoploss_orders) == 0:
# REMOVED_UNUSED_CODE:             stop_price = trade.stoploss_or_liquidation
# REMOVED_UNUSED_CODE:             if self.edge:
# REMOVED_UNUSED_CODE:                 stoploss = self.edge.get_stoploss(pair=trade.pair)
# REMOVED_UNUSED_CODE:                 stop_price = (
# REMOVED_UNUSED_CODE:                     trade.open_rate * (1 - stoploss)
# REMOVED_UNUSED_CODE:                     if trade.is_short
# REMOVED_UNUSED_CODE:                     else trade.open_rate * (1 + stoploss)
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if self.create_stoploss_order(trade=trade, stop_price=stop_price):
# REMOVED_UNUSED_CODE:                 # The above will return False if the placement failed and the trade was force-sold.
# REMOVED_UNUSED_CODE:                 # in which case the trade will be closed - which we must check below.
# REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.manage_trade_stoploss_orders(trade, stoploss_orders)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def handle_trailing_stoploss_on_exchange(self, trade: Trade, order: CcxtOrder) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check to see if stoploss on exchange should be updated
# REMOVED_UNUSED_CODE:         in case of trailing stoploss on exchange
# REMOVED_UNUSED_CODE:         :param trade: Corresponding Trade
# REMOVED_UNUSED_CODE:         :param order: Current on exchange stoploss order
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         stoploss_norm = self.exchange.price_to_precision(
# REMOVED_UNUSED_CODE:             trade.pair,
# REMOVED_UNUSED_CODE:             trade.stoploss_or_liquidation,
# REMOVED_UNUSED_CODE:             rounding_mode=ROUND_DOWN if trade.is_short else ROUND_UP,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.exchange.stoploss_adjust(stoploss_norm, order, side=trade.exit_side):
# REMOVED_UNUSED_CODE:             # we check if the update is necessary
# REMOVED_UNUSED_CODE:             update_beat = self.strategy.order_types.get("stoploss_on_exchange_interval", 60)
# REMOVED_UNUSED_CODE:             upd_req = datetime.now(timezone.utc) - timedelta(seconds=update_beat)
# REMOVED_UNUSED_CODE:             if trade.stoploss_last_update_utc and upd_req >= trade.stoploss_last_update_utc:
# REMOVED_UNUSED_CODE:                 # cancelling the current stoploss on exchange first
# REMOVED_UNUSED_CODE:                 logger.info(
# REMOVED_UNUSED_CODE:                     f"Cancelling current stoploss on exchange for pair {trade.pair} "
# REMOVED_UNUSED_CODE:                     f"(orderid:{order['id']}) in order to add another one ..."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 self.cancel_stoploss_on_exchange(trade)
# REMOVED_UNUSED_CODE:                 if not trade.is_open:
# REMOVED_UNUSED_CODE:                     logger.warning(
# REMOVED_UNUSED_CODE:                         f"Trade {trade} is closed, not creating trailing stoploss order."
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 # Create new stoploss order
# REMOVED_UNUSED_CODE:                 if not self.create_stoploss_order(trade=trade, stop_price=stoploss_norm):
# REMOVED_UNUSED_CODE:                     logger.warning(
# REMOVED_UNUSED_CODE:                         f"Could not create trailing stoploss order for pair {trade.pair}."
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def manage_trade_stoploss_orders(self, trade: Trade, stoploss_orders: list[CcxtOrder]):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Perform required actions according to existing stoploss orders of trade
# REMOVED_UNUSED_CODE:         :param trade: Corresponding Trade
# REMOVED_UNUSED_CODE:         :param stoploss_orders: Current on exchange stoploss orders
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # If all stoploss ordered are canceled for some reason we add it again
# REMOVED_UNUSED_CODE:         canceled_sl_orders = [
# REMOVED_UNUSED_CODE:             o for o in stoploss_orders if o["status"] in ("canceled", "cancelled")
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             trade.is_open
# REMOVED_UNUSED_CODE:             and len(stoploss_orders) > 0
# REMOVED_UNUSED_CODE:             and len(stoploss_orders) == len(canceled_sl_orders)
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             if self.create_stoploss_order(trade=trade, stop_price=trade.stoploss_or_liquidation):
# REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 logger.warning("All Stoploss orders are cancelled, but unable to recreate one.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         active_sl_orders = [o for o in stoploss_orders if o not in canceled_sl_orders]
# REMOVED_UNUSED_CODE:         if len(active_sl_orders) > 0:
# REMOVED_UNUSED_CODE:             last_active_sl_order = active_sl_orders[-1]
# REMOVED_UNUSED_CODE:             # Finally we check if stoploss on exchange should be moved up because of trailing.
# REMOVED_UNUSED_CODE:             # Triggered Orders are now real orders - so don't replace stoploss anymore
# REMOVED_UNUSED_CODE:             if (
# REMOVED_UNUSED_CODE:                 trade.is_open
# REMOVED_UNUSED_CODE:                 and last_active_sl_order.get("status_stop") != "triggered"
# REMOVED_UNUSED_CODE:                 and (
# REMOVED_UNUSED_CODE:                     self.config.get("trailing_stop", False)
# REMOVED_UNUSED_CODE:                     or self.config.get("use_custom_stoploss", False)
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 # if trailing stoploss is enabled we check if stoploss value has changed
# REMOVED_UNUSED_CODE:                 # in which case we cancel stoploss order and put another one with new
# REMOVED_UNUSED_CODE:                 # value immediately
# REMOVED_UNUSED_CODE:                 self.handle_trailing_stoploss_on_exchange(trade, last_active_sl_order)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def manage_open_orders(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Management of open orders on exchange. Unfilled orders might be cancelled if timeout
# REMOVED_UNUSED_CODE:         was met or replaced if there's a new candle and user has requested it.
# REMOVED_UNUSED_CODE:         Timeout setting takes priority over limit order adjustment request.
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         for trade in Trade.get_open_trades():
# REMOVED_UNUSED_CODE:             open_order: Order
# REMOVED_UNUSED_CODE:             for open_order in trade.open_orders:
# REMOVED_UNUSED_CODE:                 try:
# REMOVED_UNUSED_CODE:                     order = self.exchange.fetch_order(open_order.order_id, trade.pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 except ExchangeError:
# REMOVED_UNUSED_CODE:                     logger.info(
# REMOVED_UNUSED_CODE:                         "Cannot query order for %s due to %s", trade, traceback.format_exc()
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     continue
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 fully_cancelled = self.update_trade_state(trade, open_order.order_id, order)
# REMOVED_UNUSED_CODE:                 not_closed = order["status"] == "open" or fully_cancelled
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 if not_closed:
# REMOVED_UNUSED_CODE:                     if fully_cancelled or (
# REMOVED_UNUSED_CODE:                         open_order
# REMOVED_UNUSED_CODE:                         and self.strategy.ft_check_timed_out(
# REMOVED_UNUSED_CODE:                             trade, open_order, datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:                     ):
# REMOVED_UNUSED_CODE:                         self.handle_cancel_order(
# REMOVED_UNUSED_CODE:                             order, open_order, trade, constants.CANCEL_REASON["TIMEOUT"]
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:                     else:
# REMOVED_UNUSED_CODE:                         self.replace_order(order, open_order, trade)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def handle_cancel_order(
# REMOVED_UNUSED_CODE:         self, order: CcxtOrder, order_obj: Order, trade: Trade, reason: str
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check if current analyzed order timed out and cancel if necessary.
# REMOVED_UNUSED_CODE:         :param order: Order dict grabbed with exchange.fetch_order()
# REMOVED_UNUSED_CODE:         :param order_obj: Order object from the database.
# REMOVED_UNUSED_CODE:         :param trade: Trade object.
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if order["side"] == trade.entry_side:
# REMOVED_UNUSED_CODE:             self.handle_cancel_enter(trade, order, order_obj, reason)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             canceled = self.handle_cancel_exit(trade, order, order_obj, reason)
# REMOVED_UNUSED_CODE:             canceled_count = trade.get_canceled_exit_order_count()
# REMOVED_UNUSED_CODE:             max_timeouts = self.config.get("unfilledtimeout", {}).get("exit_timeout_count", 0)
# REMOVED_UNUSED_CODE:             if canceled and max_timeouts > 0 and canceled_count >= max_timeouts:
# REMOVED_UNUSED_CODE:                 logger.warning(
# REMOVED_UNUSED_CODE:                     f"Emergency exiting trade {trade}, as the exit order "
# REMOVED_UNUSED_CODE:                     f"timed out {max_timeouts} times. force selling {order['amount']}."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 self.emergency_exit(trade, order["price"], order["amount"])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def emergency_exit(
# REMOVED_UNUSED_CODE:         self, trade: Trade, price: float, sub_trade_amt: float | None = None
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             self.execute_trade_exit(
# REMOVED_UNUSED_CODE:                 trade,
# REMOVED_UNUSED_CODE:                 price,
# REMOVED_UNUSED_CODE:                 exit_check=ExitCheckTuple(exit_type=ExitType.EMERGENCY_EXIT),
# REMOVED_UNUSED_CODE:                 sub_trade_amt=sub_trade_amt,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         except DependencyException as exception:
# REMOVED_UNUSED_CODE:             logger.warning(f"Unable to emergency exit trade {trade.pair}: {exception}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def replace_order_failed(self, trade: Trade, msg: str) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Order replacement fail handling.
# REMOVED_UNUSED_CODE:         Deletes the trade if necessary.
# REMOVED_UNUSED_CODE:         :param trade: Trade object.
# REMOVED_UNUSED_CODE:         :param msg: Error message.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         logger.warning(msg)
# REMOVED_UNUSED_CODE:         if trade.nr_of_successful_entries == 0:
# REMOVED_UNUSED_CODE:             # this is the first entry and we didn't get filled yet, delete trade
# REMOVED_UNUSED_CODE:             logger.warning(f"Removing {trade} from database.")
# REMOVED_UNUSED_CODE:             self._notify_enter_cancel(
# REMOVED_UNUSED_CODE:                 trade,
# REMOVED_UNUSED_CODE:                 order_type=self.strategy.order_types["entry"],
# REMOVED_UNUSED_CODE:                 reason=constants.CANCEL_REASON["REPLACE_FAILED"],
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             trade.delete()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def replace_order(self, order: CcxtOrder, order_obj: Order | None, trade: Trade) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check if current analyzed entry order should be replaced or simply cancelled.
# REMOVED_UNUSED_CODE:         To simply cancel the existing order(no replacement) adjust_entry_price() should return None
# REMOVED_UNUSED_CODE:         To maintain existing order adjust_entry_price() should return order_obj.price
# REMOVED_UNUSED_CODE:         To replace existing order adjust_entry_price() should return desired price for limit order
# REMOVED_UNUSED_CODE:         :param order: Order dict grabbed with exchange.fetch_order()
# REMOVED_UNUSED_CODE:         :param order_obj: Order object.
# REMOVED_UNUSED_CODE:         :param trade: Trade object.
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         analyzed_df, _ = self.dataprovider.get_analyzed_dataframe(
# REMOVED_UNUSED_CODE:             trade.pair, self.strategy.timeframe
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         latest_candle_open_date = analyzed_df.iloc[-1]["date"] if len(analyzed_df) > 0 else None
# REMOVED_UNUSED_CODE:         latest_candle_close_date = timeframe_to_next_date(
# REMOVED_UNUSED_CODE:             self.strategy.timeframe, latest_candle_open_date
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         # Check if new candle
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             order_obj
# REMOVED_UNUSED_CODE:             and order_obj.side == trade.entry_side
# REMOVED_UNUSED_CODE:             and latest_candle_close_date > order_obj.order_date_utc
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             # New candle
# REMOVED_UNUSED_CODE:             proposed_rate = self.exchange.get_rate(
# REMOVED_UNUSED_CODE:                 trade.pair, side="entry", is_short=trade.is_short, refresh=True
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             adjusted_entry_price = strategy_safe_wrapper(
# REMOVED_UNUSED_CODE:                 self.strategy.adjust_entry_price, default_retval=order_obj.safe_placement_price
# REMOVED_UNUSED_CODE:             )(
# REMOVED_UNUSED_CODE:                 trade=trade,
# REMOVED_UNUSED_CODE:                 order=order_obj,
# REMOVED_UNUSED_CODE:                 pair=trade.pair,
# REMOVED_UNUSED_CODE:                 current_time=datetime.now(timezone.utc),
# REMOVED_UNUSED_CODE:                 proposed_rate=proposed_rate,
# REMOVED_UNUSED_CODE:                 current_order_rate=order_obj.safe_placement_price,
# REMOVED_UNUSED_CODE:                 entry_tag=trade.enter_tag,
# REMOVED_UNUSED_CODE:                 side=trade.trade_direction,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             replacing = True
# REMOVED_UNUSED_CODE:             cancel_reason = constants.CANCEL_REASON["REPLACE"]
# REMOVED_UNUSED_CODE:             if not adjusted_entry_price:
# REMOVED_UNUSED_CODE:                 replacing = False
# REMOVED_UNUSED_CODE:                 cancel_reason = constants.CANCEL_REASON["USER_CANCEL"]
# REMOVED_UNUSED_CODE:             if order_obj.safe_placement_price != adjusted_entry_price:
# REMOVED_UNUSED_CODE:                 # cancel existing order if new price is supplied or None
# REMOVED_UNUSED_CODE:                 res = self.handle_cancel_enter(
# REMOVED_UNUSED_CODE:                     trade, order, order_obj, cancel_reason, replacing=replacing
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 if not res:
# REMOVED_UNUSED_CODE:                     self.replace_order_failed(
# REMOVED_UNUSED_CODE:                         trade, f"Could not fully cancel order for {trade}, therefore not replacing."
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     return
# REMOVED_UNUSED_CODE:                 if adjusted_entry_price:
# REMOVED_UNUSED_CODE:                     # place new order only if new price is supplied
# REMOVED_UNUSED_CODE:                     try:
# REMOVED_UNUSED_CODE:                         if not self.execute_entry(
# REMOVED_UNUSED_CODE:                             pair=trade.pair,
# REMOVED_UNUSED_CODE:                             stake_amount=(
# REMOVED_UNUSED_CODE:                                 order_obj.safe_remaining * order_obj.safe_price / trade.leverage
# REMOVED_UNUSED_CODE:                             ),
# REMOVED_UNUSED_CODE:                             price=adjusted_entry_price,
# REMOVED_UNUSED_CODE:                             trade=trade,
# REMOVED_UNUSED_CODE:                             is_short=trade.is_short,
# REMOVED_UNUSED_CODE:                             mode="replace",
# REMOVED_UNUSED_CODE:                         ):
# REMOVED_UNUSED_CODE:                             self.replace_order_failed(
# REMOVED_UNUSED_CODE:                                 trade, f"Could not replace order for {trade}."
# REMOVED_UNUSED_CODE:                             )
# REMOVED_UNUSED_CODE:                     except DependencyException as exception:
# REMOVED_UNUSED_CODE:                         logger.warning(f"Unable to replace order for {trade.pair}: {exception}")
# REMOVED_UNUSED_CODE:                         self.replace_order_failed(trade, f"Could not replace order for {trade}.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def cancel_open_orders_of_trade(
# REMOVED_UNUSED_CODE:         self, trade: Trade, sides: list[str], reason: str, replacing: bool = False
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Cancel trade orders of specified sides that are currently open
# REMOVED_UNUSED_CODE:         :param trade: Trade object of the trade we're analyzing
# REMOVED_UNUSED_CODE:         :param reason: The reason for that cancellation
# REMOVED_UNUSED_CODE:         :param sides: The sides where cancellation should take place
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for open_order in trade.open_orders:
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 order = self.exchange.fetch_order(open_order.order_id, trade.pair)
# REMOVED_UNUSED_CODE:             except ExchangeError:
# REMOVED_UNUSED_CODE:                 logger.info("Can't query order for %s due to %s", trade, traceback.format_exc())
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if order["side"] in sides:
# REMOVED_UNUSED_CODE:                 if order["side"] == trade.entry_side:
# REMOVED_UNUSED_CODE:                     self.handle_cancel_enter(trade, order, open_order, reason, replacing)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 elif order["side"] == trade.exit_side:
# REMOVED_UNUSED_CODE:                     self.handle_cancel_exit(trade, order, open_order, reason)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def cancel_all_open_orders(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Cancel all orders that are currently open
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for trade in Trade.get_open_trades():
# REMOVED_UNUSED_CODE:             self.cancel_open_orders_of_trade(
# REMOVED_UNUSED_CODE:                 trade, [trade.entry_side, trade.exit_side], constants.CANCEL_REASON["ALL_CANCELLED"]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         Trade.commit()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def handle_similar_open_order(
# REMOVED_UNUSED_CODE:         self, trade: Trade, price: float, amount: float, side: str
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Keep existing open order if same amount and side otherwise cancel
# REMOVED_UNUSED_CODE:         :param trade: Trade object of the trade we're analyzing
# REMOVED_UNUSED_CODE:         :param price: Limit price of the potential new order
# REMOVED_UNUSED_CODE:         :param amount: Quantity of assets of the potential new order
# REMOVED_UNUSED_CODE:         :param side: Side of the potential new order
# REMOVED_UNUSED_CODE:         :return: True if an existing similar order was found
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if trade.has_open_orders:
# REMOVED_UNUSED_CODE:             oo = trade.select_order(side, True)
# REMOVED_UNUSED_CODE:             if oo is not None:
# REMOVED_UNUSED_CODE:                 if (price == oo.price) and (side == oo.side) and (amount == oo.amount):
# REMOVED_UNUSED_CODE:                     logger.info(
# REMOVED_UNUSED_CODE:                         f"A similar open order was found for {trade.pair}. "
# REMOVED_UNUSED_CODE:                         f"Keeping existing {trade.exit_side} order. {price=},  {amount=}"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     return True
# REMOVED_UNUSED_CODE:             # cancel open orders of this trade if order is different
# REMOVED_UNUSED_CODE:             self.cancel_open_orders_of_trade(
# REMOVED_UNUSED_CODE:                 trade,
# REMOVED_UNUSED_CODE:                 [trade.entry_side, trade.exit_side],
# REMOVED_UNUSED_CODE:                 constants.CANCEL_REASON["REPLACE"],
# REMOVED_UNUSED_CODE:                 True,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             Trade.commit()
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def handle_cancel_enter(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE:         order: CcxtOrder,
# REMOVED_UNUSED_CODE:         order_obj: Order,
# REMOVED_UNUSED_CODE:         reason: str,
# REMOVED_UNUSED_CODE:         replacing: bool | None = False,
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         entry cancel - cancel order
# REMOVED_UNUSED_CODE:         :param order_obj: Order object from the database.
# REMOVED_UNUSED_CODE:         :param replacing: Replacing order - prevent trade deletion.
# REMOVED_UNUSED_CODE:         :return: True if trade was fully cancelled
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         was_trade_fully_canceled = False
# REMOVED_UNUSED_CODE:         order_id = order_obj.order_id
# REMOVED_UNUSED_CODE:         side = trade.entry_side.capitalize()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if order["status"] not in constants.NON_OPEN_EXCHANGE_STATES:
# REMOVED_UNUSED_CODE:             filled_val: float = order.get("filled", 0.0) or 0.0
# REMOVED_UNUSED_CODE:             filled_stake = filled_val * trade.open_rate
# REMOVED_UNUSED_CODE:             minstake = self.exchange.get_min_pair_stake_amount(
# REMOVED_UNUSED_CODE:                 trade.pair, trade.open_rate, self.strategy.stoploss
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if filled_val > 0 and minstake and filled_stake < minstake:
# REMOVED_UNUSED_CODE:                 logger.warning(
# REMOVED_UNUSED_CODE:                     f"Order {order_id} for {trade.pair} not cancelled, "
# REMOVED_UNUSED_CODE:                     f"as the filled amount of {filled_val} would result in an unexitable trade."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE:             corder = self.exchange.cancel_order_with_result(order_id, trade.pair, trade.amount)
# REMOVED_UNUSED_CODE:             order_obj.ft_cancel_reason = reason
# REMOVED_UNUSED_CODE:             # if replacing, retry fetching the order 3 times if the status is not what we need
# REMOVED_UNUSED_CODE:             if replacing:
# REMOVED_UNUSED_CODE:                 retry_count = 0
# REMOVED_UNUSED_CODE:                 while (
# REMOVED_UNUSED_CODE:                     corder.get("status") not in constants.NON_OPEN_EXCHANGE_STATES
# REMOVED_UNUSED_CODE:                     and retry_count < 3
# REMOVED_UNUSED_CODE:                 ):
# REMOVED_UNUSED_CODE:                     sleep(0.5)
# REMOVED_UNUSED_CODE:                     corder = self.exchange.fetch_order(order_id, trade.pair)
# REMOVED_UNUSED_CODE:                     retry_count += 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Avoid race condition where the order could not be cancelled coz its already filled.
# REMOVED_UNUSED_CODE:             # Simply bailing here is the only safe way - as this order will then be
# REMOVED_UNUSED_CODE:             # handled in the next iteration.
# REMOVED_UNUSED_CODE:             if corder.get("status") not in constants.NON_OPEN_EXCHANGE_STATES:
# REMOVED_UNUSED_CODE:                 logger.warning(f"Order {order_id} for {trade.pair} not cancelled.")
# REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # Order was cancelled already, so we can reuse the existing dict
# REMOVED_UNUSED_CODE:             corder = order
# REMOVED_UNUSED_CODE:             if order_obj.ft_cancel_reason is None:
# REMOVED_UNUSED_CODE:                 order_obj.ft_cancel_reason = constants.CANCEL_REASON["CANCELLED_ON_EXCHANGE"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.info(f"{side} order {order_obj.ft_cancel_reason} for {trade}.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Using filled to determine the filled amount
# REMOVED_UNUSED_CODE:         filled_amount = safe_value_fallback2(corder, order, "filled", "filled")
# REMOVED_UNUSED_CODE:         if isclose(filled_amount, 0.0, abs_tol=constants.MATH_CLOSE_PREC):
# REMOVED_UNUSED_CODE:             was_trade_fully_canceled = True
# REMOVED_UNUSED_CODE:             # if trade is not partially completed and it's the only order, just delete the trade
# REMOVED_UNUSED_CODE:             open_order_count = len(
# REMOVED_UNUSED_CODE:                 [order for order in trade.orders if order.ft_is_open and order.order_id != order_id]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             if open_order_count < 1 and trade.nr_of_successful_entries == 0 and not replacing:
# REMOVED_UNUSED_CODE:                 logger.info(f"{side} order fully cancelled. Removing {trade} from database.")
# REMOVED_UNUSED_CODE:                 trade.delete()
# REMOVED_UNUSED_CODE:                 order_obj.ft_cancel_reason += f", {constants.CANCEL_REASON['FULLY_CANCELLED']}"
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 self.update_trade_state(trade, order_id, corder)
# REMOVED_UNUSED_CODE:                 logger.info(f"{side} Order timeout for {trade}.")
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # update_trade_state (and subsequently recalc_trade_from_orders) will handle updates
# REMOVED_UNUSED_CODE:             # to the trade object
# REMOVED_UNUSED_CODE:             self.update_trade_state(trade, order_id, corder)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             logger.info(f"Partial {trade.entry_side} order timeout for {trade}.")
# REMOVED_UNUSED_CODE:             order_obj.ft_cancel_reason += f", {constants.CANCEL_REASON['PARTIALLY_FILLED']}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.wallets.update()
# REMOVED_UNUSED_CODE:         self._notify_enter_cancel(
# REMOVED_UNUSED_CODE:             trade, order_type=self.strategy.order_types["entry"], reason=order_obj.ft_cancel_reason
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         return was_trade_fully_canceled
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def handle_cancel_exit(
# REMOVED_UNUSED_CODE:         self, trade: Trade, order: CcxtOrder, order_obj: Order, reason: str
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         exit order cancel - cancel order and update trade
# REMOVED_UNUSED_CODE:         :return: True if exit order was cancelled, false otherwise
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         order_id = order_obj.order_id
# REMOVED_UNUSED_CODE:         cancelled = False
# REMOVED_UNUSED_CODE:         # Cancelled orders may have the status of 'canceled' or 'closed'
# REMOVED_UNUSED_CODE:         if order["status"] not in constants.NON_OPEN_EXCHANGE_STATES:
# REMOVED_UNUSED_CODE:             filled_amt: float = order.get("filled", 0.0) or 0.0
# REMOVED_UNUSED_CODE:             # Filled val is in quote currency (after leverage)
# REMOVED_UNUSED_CODE:             filled_rem_stake = trade.stake_amount - (filled_amt * trade.open_rate / trade.leverage)
# REMOVED_UNUSED_CODE:             minstake = self.exchange.get_min_pair_stake_amount(
# REMOVED_UNUSED_CODE:                 trade.pair, trade.open_rate, self.strategy.stoploss
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             # Double-check remaining amount
# REMOVED_UNUSED_CODE:             if filled_amt > 0:
# REMOVED_UNUSED_CODE:                 reason = constants.CANCEL_REASON["PARTIALLY_FILLED"]
# REMOVED_UNUSED_CODE:                 if minstake and filled_rem_stake < minstake:
# REMOVED_UNUSED_CODE:                     logger.warning(
# REMOVED_UNUSED_CODE:                         f"Order {order_id} for {trade.pair} not cancelled, as "
# REMOVED_UNUSED_CODE:                         f"the filled amount of {filled_amt} would result in an unexitable trade."
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     reason = constants.CANCEL_REASON["PARTIALLY_FILLED_KEEP_OPEN"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                     self._notify_exit_cancel(
# REMOVED_UNUSED_CODE:                         trade,
# REMOVED_UNUSED_CODE:                         order_type=self.strategy.order_types["exit"],
# REMOVED_UNUSED_CODE:                         reason=reason,
# REMOVED_UNUSED_CODE:                         order_id=order["id"],
# REMOVED_UNUSED_CODE:                         sub_trade=trade.amount != order["amount"],
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     return False
# REMOVED_UNUSED_CODE:             order_obj.ft_cancel_reason = reason
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 order = self.exchange.cancel_order_with_result(
# REMOVED_UNUSED_CODE:                     order["id"], trade.pair, trade.amount
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             except InvalidOrderException:
# REMOVED_UNUSED_CODE:                 logger.exception(f"Could not cancel {trade.exit_side} order {order_id}")
# REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Set exit_reason for fill message
# REMOVED_UNUSED_CODE:             exit_reason_prev = trade.exit_reason
# REMOVED_UNUSED_CODE:             trade.exit_reason = trade.exit_reason + f", {reason}" if trade.exit_reason else reason
# REMOVED_UNUSED_CODE:             # Order might be filled above in odd timing issues.
# REMOVED_UNUSED_CODE:             if order.get("status") in ("canceled", "cancelled"):
# REMOVED_UNUSED_CODE:                 trade.exit_reason = None
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 trade.exit_reason = exit_reason_prev
# REMOVED_UNUSED_CODE:             cancelled = True
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             if order_obj.ft_cancel_reason is None:
# REMOVED_UNUSED_CODE:                 order_obj.ft_cancel_reason = constants.CANCEL_REASON["CANCELLED_ON_EXCHANGE"]
# REMOVED_UNUSED_CODE:             trade.exit_reason = None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.update_trade_state(trade, order["id"], order)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.info(
# REMOVED_UNUSED_CODE:             f"{trade.exit_side.capitalize()} order {order_obj.ft_cancel_reason} for {trade}."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade.close_rate = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade.close_rate_requested = None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._notify_exit_cancel(
# REMOVED_UNUSED_CODE:             trade,
# REMOVED_UNUSED_CODE:             order_type=self.strategy.order_types["exit"],
# REMOVED_UNUSED_CODE:             reason=order_obj.ft_cancel_reason,
# REMOVED_UNUSED_CODE:             order_id=order["id"],
# REMOVED_UNUSED_CODE:             sub_trade=trade.amount != order["amount"],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         return cancelled
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _safe_exit_amount(self, trade: Trade, pair: str, amount: float) -> float:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get sellable amount.
# REMOVED_UNUSED_CODE:         Should be trade.amount - but will fall back to the available amount if necessary.
# REMOVED_UNUSED_CODE:         This should cover cases where get_real_amount() was not able to update the amount
# REMOVED_UNUSED_CODE:         for whatever reason.
# REMOVED_UNUSED_CODE:         :param trade: Trade we're working with
# REMOVED_UNUSED_CODE:         :param pair: Pair we're trying to sell
# REMOVED_UNUSED_CODE:         :param amount: amount we expect to be available
# REMOVED_UNUSED_CODE:         :return: amount to sell
# REMOVED_UNUSED_CODE:         :raise: DependencyException: if available balance is not within 2% of the available amount.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Update wallets to ensure amounts tied up in a stoploss is now free!
# REMOVED_UNUSED_CODE:         self.wallets.update()
# REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES:
# REMOVED_UNUSED_CODE:             # A safe exit amount isn't needed for futures, you can just exit/close the position
# REMOVED_UNUSED_CODE:             return amount
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trade_base_currency = self.exchange.get_pair_base_currency(pair)
# REMOVED_UNUSED_CODE:         # Free + Used - open orders will eventually still be canceled.
# REMOVED_UNUSED_CODE:         wallet_amount = self.wallets.get_free(trade_base_currency) + self.wallets.get_used(
# REMOVED_UNUSED_CODE:             trade_base_currency
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.debug(f"{pair} - Wallet: {wallet_amount} - Trade-amount: {amount}")
# REMOVED_UNUSED_CODE:         if wallet_amount >= amount:
# REMOVED_UNUSED_CODE:             return amount
# REMOVED_UNUSED_CODE:         elif wallet_amount > amount * 0.98:
# REMOVED_UNUSED_CODE:             logger.info(f"{pair} - Falling back to wallet-amount {wallet_amount} -> {amount}.")
# REMOVED_UNUSED_CODE:             trade.amount = wallet_amount
# REMOVED_UNUSED_CODE:             return wallet_amount
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             raise DependencyException(
# REMOVED_UNUSED_CODE:                 f"Not enough amount to exit trade. Trade-amount: {amount}, Wallet: {wallet_amount}"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def execute_trade_exit(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE:         limit: float,
# REMOVED_UNUSED_CODE:         exit_check: ExitCheckTuple,
# REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE:         exit_tag: str | None = None,
# REMOVED_UNUSED_CODE:         ordertype: str | None = None,
# REMOVED_UNUSED_CODE:         sub_trade_amt: float | None = None,
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Executes a trade exit for the given trade and limit
# REMOVED_UNUSED_CODE:         :param trade: Trade instance
# REMOVED_UNUSED_CODE:         :param limit: limit rate for the sell order
# REMOVED_UNUSED_CODE:         :param exit_check: CheckTuple with signal and reason
# REMOVED_UNUSED_CODE:         :return: True if it succeeds False
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         trade.set_funding_fees(
# REMOVED_UNUSED_CODE:             self.exchange.get_funding_fees(
# REMOVED_UNUSED_CODE:                 pair=trade.pair,
# REMOVED_UNUSED_CODE:                 amount=trade.amount,
# REMOVED_UNUSED_CODE:                 is_short=trade.is_short,
# REMOVED_UNUSED_CODE:                 open_date=trade.date_last_filled_utc,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         exit_type = "exit"
# REMOVED_UNUSED_CODE:         exit_reason = exit_tag or exit_check.exit_reason
# REMOVED_UNUSED_CODE:         if exit_check.exit_type in (
# REMOVED_UNUSED_CODE:             ExitType.STOP_LOSS,
# REMOVED_UNUSED_CODE:             ExitType.TRAILING_STOP_LOSS,
# REMOVED_UNUSED_CODE:             ExitType.LIQUIDATION,
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             exit_type = "stoploss"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # set custom_exit_price if available
# REMOVED_UNUSED_CODE:         proposed_limit_rate = limit
# REMOVED_UNUSED_CODE:         current_profit = trade.calc_profit_ratio(limit)
# REMOVED_UNUSED_CODE:         custom_exit_price = strategy_safe_wrapper(
# REMOVED_UNUSED_CODE:             self.strategy.custom_exit_price, default_retval=proposed_limit_rate
# REMOVED_UNUSED_CODE:         )(
# REMOVED_UNUSED_CODE:             pair=trade.pair,
# REMOVED_UNUSED_CODE:             trade=trade,
# REMOVED_UNUSED_CODE:             current_time=datetime.now(timezone.utc),
# REMOVED_UNUSED_CODE:             proposed_rate=proposed_limit_rate,
# REMOVED_UNUSED_CODE:             current_profit=current_profit,
# REMOVED_UNUSED_CODE:             exit_tag=exit_reason,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         limit = self.get_valid_price(custom_exit_price, proposed_limit_rate)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # First cancelling stoploss on exchange ...
# REMOVED_UNUSED_CODE:         trade = self.cancel_stoploss_on_exchange(trade)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         order_type = ordertype or self.strategy.order_types[exit_type]
# REMOVED_UNUSED_CODE:         if exit_check.exit_type == ExitType.EMERGENCY_EXIT:
# REMOVED_UNUSED_CODE:             # Emergency sells (default to market!)
# REMOVED_UNUSED_CODE:             order_type = self.strategy.order_types.get("emergency_exit", "market")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         amount = self._safe_exit_amount(trade, trade.pair, sub_trade_amt or trade.amount)
# REMOVED_UNUSED_CODE:         time_in_force = self.strategy.order_time_in_force["exit"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             exit_check.exit_type != ExitType.LIQUIDATION
# REMOVED_UNUSED_CODE:             and not sub_trade_amt
# REMOVED_UNUSED_CODE:             and not strategy_safe_wrapper(self.strategy.confirm_trade_exit, default_retval=True)(
# REMOVED_UNUSED_CODE:                 pair=trade.pair,
# REMOVED_UNUSED_CODE:                 trade=trade,
# REMOVED_UNUSED_CODE:                 order_type=order_type,
# REMOVED_UNUSED_CODE:                 amount=amount,
# REMOVED_UNUSED_CODE:                 rate=limit,
# REMOVED_UNUSED_CODE:                 time_in_force=time_in_force,
# REMOVED_UNUSED_CODE:                 exit_reason=exit_reason,
# REMOVED_UNUSED_CODE:                 sell_reason=exit_reason,  # sellreason -> compatibility
# REMOVED_UNUSED_CODE:                 current_time=datetime.now(timezone.utc),
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             logger.info(f"User denied exit for {trade.pair}.")
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if trade.has_open_orders:
# REMOVED_UNUSED_CODE:             if self.handle_similar_open_order(trade, limit, amount, trade.exit_side):
# REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             # Execute sell and update trade record
# REMOVED_UNUSED_CODE:             order = self.exchange.create_order(
# REMOVED_UNUSED_CODE:                 pair=trade.pair,
# REMOVED_UNUSED_CODE:                 ordertype=order_type,
# REMOVED_UNUSED_CODE:                 side=trade.exit_side,
# REMOVED_UNUSED_CODE:                 amount=amount,
# REMOVED_UNUSED_CODE:                 rate=limit,
# REMOVED_UNUSED_CODE:                 leverage=trade.leverage,
# REMOVED_UNUSED_CODE:                 reduceOnly=self.trading_mode == TradingMode.FUTURES,
# REMOVED_UNUSED_CODE:                 time_in_force=time_in_force,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         except InsufficientFundsError as e:
# REMOVED_UNUSED_CODE:             logger.warning(f"Unable to place order {e}.")
# REMOVED_UNUSED_CODE:             # Try to figure out what went wrong
# REMOVED_UNUSED_CODE:             self.handle_insufficient_funds(trade)
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         order_obj = Order.parse_from_ccxt_object(order, trade.pair, trade.exit_side, amount, limit)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         order_obj.ft_order_tag = exit_reason
# REMOVED_UNUSED_CODE:         trade.orders.append(order_obj)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trade.exit_order_status = ""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade.close_rate_requested = limit
# REMOVED_UNUSED_CODE:         trade.exit_reason = exit_reason
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._notify_exit(trade, order_type, sub_trade=bool(sub_trade_amt), order=order_obj)
# REMOVED_UNUSED_CODE:         # In case of market sell orders the order can be closed immediately
# REMOVED_UNUSED_CODE:         if order.get("status", "unknown") in ("closed", "expired"):
# REMOVED_UNUSED_CODE:             self.update_trade_state(trade, order_obj.order_id, order)
# REMOVED_UNUSED_CODE:         Trade.commit()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _notify_exit(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE:         order_type: str | None,
# REMOVED_UNUSED_CODE:         fill: bool = False,
# REMOVED_UNUSED_CODE:         sub_trade: bool = False,
# REMOVED_UNUSED_CODE:         order: Order | None = None,
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Sends rpc notification when a sell occurred.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Use cached rates here - it was updated seconds ago.
# REMOVED_UNUSED_CODE:         current_rate = (
# REMOVED_UNUSED_CODE:             self.exchange.get_rate(trade.pair, side="exit", is_short=trade.is_short, refresh=False)
# REMOVED_UNUSED_CODE:             if not fill
# REMOVED_UNUSED_CODE:             else None
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # second condition is for mypy only; order will always be passed during sub trade
# REMOVED_UNUSED_CODE:         if sub_trade and order is not None:
# REMOVED_UNUSED_CODE:             amount = order.safe_filled if fill else order.safe_amount
# REMOVED_UNUSED_CODE:             order_rate: float = order.safe_price
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             profit = trade.calculate_profit(order_rate, amount, trade.open_rate)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             order_rate = trade.safe_close_rate
# REMOVED_UNUSED_CODE:             profit = trade.calculate_profit(rate=order_rate)
# REMOVED_UNUSED_CODE:             amount = trade.amount
# REMOVED_UNUSED_CODE:         gain: ProfitLossStr = "profit" if profit.profit_ratio > 0 else "loss"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         msg: RPCExitMsg = {
# REMOVED_UNUSED_CODE:             "type": (RPCMessageType.EXIT_FILL if fill else RPCMessageType.EXIT),
# REMOVED_UNUSED_CODE:             "trade_id": trade.id,
# REMOVED_UNUSED_CODE:             "exchange": trade.exchange.capitalize(),
# REMOVED_UNUSED_CODE:             "pair": trade.pair,
# REMOVED_UNUSED_CODE:             "leverage": trade.leverage,
# REMOVED_UNUSED_CODE:             "direction": "Short" if trade.is_short else "Long",
# REMOVED_UNUSED_CODE:             "gain": gain,
# REMOVED_UNUSED_CODE:             "limit": order_rate,  # Deprecated
# REMOVED_UNUSED_CODE:             "order_rate": order_rate,
# REMOVED_UNUSED_CODE:             "order_type": order_type or "unknown",
# REMOVED_UNUSED_CODE:             "amount": amount,
# REMOVED_UNUSED_CODE:             "open_rate": trade.open_rate,
# REMOVED_UNUSED_CODE:             "close_rate": order_rate,
# REMOVED_UNUSED_CODE:             "current_rate": current_rate,
# REMOVED_UNUSED_CODE:             "profit_amount": profit.profit_abs,
# REMOVED_UNUSED_CODE:             "profit_ratio": profit.profit_ratio,
# REMOVED_UNUSED_CODE:             "buy_tag": trade.enter_tag,
# REMOVED_UNUSED_CODE:             "enter_tag": trade.enter_tag,
# REMOVED_UNUSED_CODE:             "exit_reason": trade.exit_reason,
# REMOVED_UNUSED_CODE:             "open_date": trade.open_date_utc,
# REMOVED_UNUSED_CODE:             "close_date": trade.close_date_utc or datetime.now(timezone.utc),
# REMOVED_UNUSED_CODE:             "stake_amount": trade.stake_amount,
# REMOVED_UNUSED_CODE:             "stake_currency": self.config["stake_currency"],
# REMOVED_UNUSED_CODE:             "base_currency": self.exchange.get_pair_base_currency(trade.pair),
# REMOVED_UNUSED_CODE:             "quote_currency": self.exchange.get_pair_quote_currency(trade.pair),
# REMOVED_UNUSED_CODE:             "fiat_currency": self.config.get("fiat_display_currency"),
# REMOVED_UNUSED_CODE:             "sub_trade": sub_trade,
# REMOVED_UNUSED_CODE:             "cumulative_profit": trade.realized_profit,
# REMOVED_UNUSED_CODE:             "final_profit_ratio": trade.close_profit if not trade.is_open else None,
# REMOVED_UNUSED_CODE:             "is_final_exit": trade.is_open is False,
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Send the message
# REMOVED_UNUSED_CODE:         self.rpc.send_msg(msg)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _notify_exit_cancel(
# REMOVED_UNUSED_CODE:         self, trade: Trade, order_type: str, reason: str, order_id: str, sub_trade: bool = False
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Sends rpc notification when a sell cancel occurred.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if trade.exit_order_status == reason:
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             trade.exit_order_status = reason
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         order_or_none = trade.select_order_by_order_id(order_id)
# REMOVED_UNUSED_CODE:         order = self.order_obj_or_raise(order_id, order_or_none)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         profit_rate: float = trade.safe_close_rate
# REMOVED_UNUSED_CODE:         profit = trade.calculate_profit(rate=profit_rate)
# REMOVED_UNUSED_CODE:         current_rate = self.exchange.get_rate(
# REMOVED_UNUSED_CODE:             trade.pair, side="exit", is_short=trade.is_short, refresh=False
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         gain: ProfitLossStr = "profit" if profit.profit_ratio > 0 else "loss"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         msg: RPCExitCancelMsg = {
# REMOVED_UNUSED_CODE:             "type": RPCMessageType.EXIT_CANCEL,
# REMOVED_UNUSED_CODE:             "trade_id": trade.id,
# REMOVED_UNUSED_CODE:             "exchange": trade.exchange.capitalize(),
# REMOVED_UNUSED_CODE:             "pair": trade.pair,
# REMOVED_UNUSED_CODE:             "leverage": trade.leverage,
# REMOVED_UNUSED_CODE:             "direction": "Short" if trade.is_short else "Long",
# REMOVED_UNUSED_CODE:             "gain": gain,
# REMOVED_UNUSED_CODE:             "limit": profit_rate or 0,
# REMOVED_UNUSED_CODE:             "order_type": order_type,
# REMOVED_UNUSED_CODE:             "amount": order.safe_amount_after_fee,
# REMOVED_UNUSED_CODE:             "open_rate": trade.open_rate,
# REMOVED_UNUSED_CODE:             "current_rate": current_rate,
# REMOVED_UNUSED_CODE:             "profit_amount": profit.profit_abs,
# REMOVED_UNUSED_CODE:             "profit_ratio": profit.profit_ratio,
# REMOVED_UNUSED_CODE:             "buy_tag": trade.enter_tag,
# REMOVED_UNUSED_CODE:             "enter_tag": trade.enter_tag,
# REMOVED_UNUSED_CODE:             "exit_reason": trade.exit_reason,
# REMOVED_UNUSED_CODE:             "open_date": trade.open_date,
# REMOVED_UNUSED_CODE:             "close_date": trade.close_date or datetime.now(timezone.utc),
# REMOVED_UNUSED_CODE:             "stake_currency": self.config["stake_currency"],
# REMOVED_UNUSED_CODE:             "base_currency": self.exchange.get_pair_base_currency(trade.pair),
# REMOVED_UNUSED_CODE:             "quote_currency": self.exchange.get_pair_quote_currency(trade.pair),
# REMOVED_UNUSED_CODE:             "fiat_currency": self.config.get("fiat_display_currency", None),
# REMOVED_UNUSED_CODE:             "reason": reason,
# REMOVED_UNUSED_CODE:             "sub_trade": sub_trade,
# REMOVED_UNUSED_CODE:             "stake_amount": trade.stake_amount,
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Send the message
# REMOVED_UNUSED_CODE:         self.rpc.send_msg(msg)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def order_obj_or_raise(self, order_id: str, order_obj: Order | None) -> Order:
# REMOVED_UNUSED_CODE:         if not order_obj:
# REMOVED_UNUSED_CODE:             raise DependencyException(
# REMOVED_UNUSED_CODE:                 f"Order_obj not found for {order_id}. This should not have happened."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         return order_obj
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     #
# REMOVED_UNUSED_CODE:     # Common update trade state methods
# REMOVED_UNUSED_CODE:     #
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def update_trade_state(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE:         order_id: str | None,
# REMOVED_UNUSED_CODE:         action_order: CcxtOrder | None = None,
# REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE:         stoploss_order: bool = False,
# REMOVED_UNUSED_CODE:         send_msg: bool = True,
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Checks trades with open orders and updates the amount if necessary
# REMOVED_UNUSED_CODE:         Handles closing both buy and sell orders.
# REMOVED_UNUSED_CODE:         :param trade: Trade object of the trade we're analyzing
# REMOVED_UNUSED_CODE:         :param order_id: Order-id of the order we're analyzing
# REMOVED_UNUSED_CODE:         :param action_order: Already acquired order object
# REMOVED_UNUSED_CODE:         :param send_msg: Send notification - should always be True except in "recovery" methods
# REMOVED_UNUSED_CODE:         :return: True if order has been cancelled without being filled partially, False otherwise
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not order_id:
# REMOVED_UNUSED_CODE:             logger.warning(f"Orderid for trade {trade} is empty.")
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Update trade with order values
# REMOVED_UNUSED_CODE:         if not stoploss_order:
# REMOVED_UNUSED_CODE:             logger.info(f"Found open order for {trade}")
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             order = action_order or self.exchange.fetch_order_or_stoploss_order(
# REMOVED_UNUSED_CODE:                 order_id, trade.pair, stoploss_order
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         except InvalidOrderException as exception:
# REMOVED_UNUSED_CODE:             logger.warning("Unable to fetch order %s: %s", order_id, exception)
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trade.update_order(order)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.exchange.check_order_canceled_empty(order):
# REMOVED_UNUSED_CODE:             # Trade has been cancelled on exchange
# REMOVED_UNUSED_CODE:             # Handling of this will happen in handle_cancel_order.
# REMOVED_UNUSED_CODE:             return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         order_obj_or_none = trade.select_order_by_order_id(order_id)
# REMOVED_UNUSED_CODE:         order_obj = self.order_obj_or_raise(order_id, order_obj_or_none)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.handle_order_fee(trade, order_obj, order)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trade.update_trade(order_obj, not send_msg)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trade = self._update_trade_after_fill(trade, order_obj, send_msg)
# REMOVED_UNUSED_CODE:         Trade.commit()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.order_close_notify(trade, order_obj, stoploss_order, send_msg)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _update_trade_after_fill(self, trade: Trade, order: Order, send_msg: bool) -> Trade:
# REMOVED_UNUSED_CODE:         if order.status in constants.NON_OPEN_EXCHANGE_STATES:
# REMOVED_UNUSED_CODE:             strategy_safe_wrapper(self.strategy.order_filled, default_retval=None)(
# REMOVED_UNUSED_CODE:                 pair=trade.pair, trade=trade, order=order, current_time=datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             # If a entry order was closed, force update on stoploss on exchange
# REMOVED_UNUSED_CODE:             if order.ft_order_side == trade.entry_side:
# REMOVED_UNUSED_CODE:                 if send_msg:
# REMOVED_UNUSED_CODE:                     # Don't cancel stoploss in recovery modes immediately
# REMOVED_UNUSED_CODE:                     trade = self.cancel_stoploss_on_exchange(trade)
# REMOVED_UNUSED_CODE:                 if not self.edge:
# REMOVED_UNUSED_CODE:                     # TODO: should shorting/leverage be supported by Edge,
# REMOVED_UNUSED_CODE:                     # then this will need to be fixed.
# REMOVED_UNUSED_CODE:                     trade.adjust_stop_loss(trade.open_rate, self.strategy.stoploss, initial=True)
# REMOVED_UNUSED_CODE:             if (
# REMOVED_UNUSED_CODE:                 order.ft_order_side == trade.entry_side
# REMOVED_UNUSED_CODE:                 or (trade.amount > 0 and trade.is_open)
# REMOVED_UNUSED_CODE:                 or self.margin_mode == MarginMode.CROSS
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 # Must also run for partial exits
# REMOVED_UNUSED_CODE:                 # TODO: Margin will need to use interest_rate as well.
# REMOVED_UNUSED_CODE:                 # interest_rate = self.exchange.get_interest_rate()
# REMOVED_UNUSED_CODE:                 update_liquidation_prices(
# REMOVED_UNUSED_CODE:                     trade,
# REMOVED_UNUSED_CODE:                     exchange=self.exchange,
# REMOVED_UNUSED_CODE:                     wallets=self.wallets,
# REMOVED_UNUSED_CODE:                     stake_currency=self.config["stake_currency"],
# REMOVED_UNUSED_CODE:                     dry_run=self.config["dry_run"],
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 if self.strategy.use_custom_stoploss:
# REMOVED_UNUSED_CODE:                     current_rate = self.exchange.get_rate(
# REMOVED_UNUSED_CODE:                         trade.pair, side="exit", is_short=trade.is_short, refresh=True
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     profit = trade.calc_profit_ratio(current_rate)
# REMOVED_UNUSED_CODE:                     self.strategy.ft_stoploss_adjust(
# REMOVED_UNUSED_CODE:                         current_rate, trade, datetime.now(timezone.utc), profit, 0, after_fill=True
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:             # Updating wallets when order is closed
# REMOVED_UNUSED_CODE:             self.wallets.update()
# REMOVED_UNUSED_CODE:         return trade
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def order_close_notify(self, trade: Trade, order: Order, stoploss_order: bool, send_msg: bool):
# REMOVED_UNUSED_CODE:         """send "fill" notifications"""
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if order.ft_order_side == trade.exit_side:
# REMOVED_UNUSED_CODE:             # Exit notification
# REMOVED_UNUSED_CODE:             if send_msg and not stoploss_order and order.order_id not in trade.open_orders_ids:
# REMOVED_UNUSED_CODE:                 self._notify_exit(
# REMOVED_UNUSED_CODE:                     trade, order.order_type, fill=True, sub_trade=trade.is_open, order=order
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             if not trade.is_open:
# REMOVED_UNUSED_CODE:                 self.handle_protections(trade.pair, trade.trade_direction)
# REMOVED_UNUSED_CODE:         elif send_msg and order.order_id not in trade.open_orders_ids and not stoploss_order:
# REMOVED_UNUSED_CODE:             sub_trade = not isclose(
# REMOVED_UNUSED_CODE:                 order.safe_amount_after_fee, trade.amount, abs_tol=constants.MATH_CLOSE_PREC
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             # Enter fill
# REMOVED_UNUSED_CODE:             self._notify_enter(trade, order, order.order_type, fill=True, sub_trade=sub_trade)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def handle_protections(self, pair: str, side: LongShort) -> None:
# REMOVED_UNUSED_CODE:         # Lock pair for one candle to prevent immediate re-entries
# REMOVED_UNUSED_CODE:         self.strategy.lock_pair(pair, datetime.now(timezone.utc), reason="Auto lock", side=side)
# REMOVED_UNUSED_CODE:         prot_trig = self.protections.stop_per_pair(pair, side=side)
# REMOVED_UNUSED_CODE:         if prot_trig:
# REMOVED_UNUSED_CODE:             msg: RPCProtectionMsg = {
# REMOVED_UNUSED_CODE:                 "type": RPCMessageType.PROTECTION_TRIGGER,
# REMOVED_UNUSED_CODE:                 "base_currency": self.exchange.get_pair_base_currency(prot_trig.pair),
# REMOVED_UNUSED_CODE:                 **prot_trig.to_json(),  # type: ignore
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE:             self.rpc.send_msg(msg)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         prot_trig_glb = self.protections.global_stop(side=side)
# REMOVED_UNUSED_CODE:         if prot_trig_glb:
# REMOVED_UNUSED_CODE:             msg = {
# REMOVED_UNUSED_CODE:                 "type": RPCMessageType.PROTECTION_TRIGGER_GLOBAL,
# REMOVED_UNUSED_CODE:                 "base_currency": self.exchange.get_pair_base_currency(prot_trig_glb.pair),
# REMOVED_UNUSED_CODE:                 **prot_trig_glb.to_json(),  # type: ignore
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE:             self.rpc.send_msg(msg)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def apply_fee_conditional(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         trade: Trade,
# REMOVED_UNUSED_CODE:         trade_base_currency: str,
# REMOVED_UNUSED_CODE:         amount: float,
# REMOVED_UNUSED_CODE:         fee_abs: float,
# REMOVED_UNUSED_CODE:         order_obj: Order,
# REMOVED_UNUSED_CODE:     ) -> float | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Applies the fee to amount (either from Order or from Trades).
# REMOVED_UNUSED_CODE:         Can eat into dust if more than the required asset is available.
# REMOVED_UNUSED_CODE:         In case of trade adjustment orders, trade.amount will not have been adjusted yet.
# REMOVED_UNUSED_CODE:         Can't happen in Futures mode - where Fees are always in settlement currency,
# REMOVED_UNUSED_CODE:         never in base currency.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.wallets.update()
# REMOVED_UNUSED_CODE:         amount_ = trade.amount
# REMOVED_UNUSED_CODE:         if order_obj.ft_order_side == trade.exit_side or order_obj.ft_order_side == "stoploss":
# REMOVED_UNUSED_CODE:             # check against remaining amount!
# REMOVED_UNUSED_CODE:             amount_ = trade.amount - amount
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if trade.nr_of_successful_entries >= 1 and order_obj.ft_order_side == trade.entry_side:
# REMOVED_UNUSED_CODE:             # In case of re-entry's, trade.amount doesn't contain the amount of the last entry.
# REMOVED_UNUSED_CODE:             amount_ = trade.amount + amount
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if fee_abs != 0 and self.wallets.get_free(trade_base_currency) >= amount_:
# REMOVED_UNUSED_CODE:             # Eat into dust if we own more than base currency
# REMOVED_UNUSED_CODE:             logger.info(
# REMOVED_UNUSED_CODE:                 f"Fee amount for {trade} was in base currency - Eating Fee {fee_abs} into dust."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         elif fee_abs != 0:
# REMOVED_UNUSED_CODE:             logger.info(f"Applying fee on amount for {trade}, fee={fee_abs}.")
# REMOVED_UNUSED_CODE:             return fee_abs
# REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def handle_order_fee(self, trade: Trade, order_obj: Order, order: CcxtOrder) -> None:
# REMOVED_UNUSED_CODE:         # Try update amount (binance-fix)
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             fee_abs = self.get_real_amount(trade, order, order_obj)
# REMOVED_UNUSED_CODE:             if fee_abs is not None:
# REMOVED_UNUSED_CODE:                 order_obj.ft_fee_base = fee_abs
# REMOVED_UNUSED_CODE:         except DependencyException as exception:
# REMOVED_UNUSED_CODE:             logger.warning("Could not update trade amount: %s", exception)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_real_amount(self, trade: Trade, order: CcxtOrder, order_obj: Order) -> float | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Detect and update trade fee.
# REMOVED_UNUSED_CODE:         Calls trade.update_fee() upon correct detection.
# REMOVED_UNUSED_CODE:         Returns modified amount if the fee was taken from the destination currency.
# REMOVED_UNUSED_CODE:         Necessary for exchanges which charge fees in base currency (e.g. binance)
# REMOVED_UNUSED_CODE:         :return: Absolute fee to apply for this order or None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Init variables
# REMOVED_UNUSED_CODE:         order_amount = safe_value_fallback(order, "filled", "amount")
# REMOVED_UNUSED_CODE:         # Only run for closed orders
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             trade.fee_updated(order.get("side", ""))
# REMOVED_UNUSED_CODE:             or order["status"] == "open"
# REMOVED_UNUSED_CODE:             or order_obj.ft_fee_base
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trade_base_currency = self.exchange.get_pair_base_currency(trade.pair)
# REMOVED_UNUSED_CODE:         # use fee from order-dict if possible
# REMOVED_UNUSED_CODE:         if self.exchange.order_has_fee(order):
# REMOVED_UNUSED_CODE:             fee_cost, fee_currency, fee_rate = self.exchange.extract_cost_curr_rate(
# REMOVED_UNUSED_CODE:                 order["fee"], order["symbol"], order["cost"], order_obj.safe_filled
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             logger.info(
# REMOVED_UNUSED_CODE:                 f"Fee for Trade {trade} [{order_obj.ft_order_side}]: "
# REMOVED_UNUSED_CODE:                 f"{fee_cost:.8g} {fee_currency} - rate: {fee_rate}"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             if fee_rate is None or fee_rate < 0.02:
# REMOVED_UNUSED_CODE:                 # Reject all fees that report as > 2%.
# REMOVED_UNUSED_CODE:                 # These are most likely caused by a parsing bug in ccxt
# REMOVED_UNUSED_CODE:                 # due to multiple trades (https://github.com/ccxt/ccxt/issues/8025)
# REMOVED_UNUSED_CODE:                 trade.update_fee(fee_cost, fee_currency, fee_rate, order.get("side", ""))
# REMOVED_UNUSED_CODE:                 if trade_base_currency == fee_currency:
# REMOVED_UNUSED_CODE:                     # Apply fee to amount
# REMOVED_UNUSED_CODE:                     return self.apply_fee_conditional(
# REMOVED_UNUSED_CODE:                         trade,
# REMOVED_UNUSED_CODE:                         trade_base_currency,
# REMOVED_UNUSED_CODE:                         amount=order_amount,
# REMOVED_UNUSED_CODE:                         fee_abs=fee_cost,
# REMOVED_UNUSED_CODE:                         order_obj=order_obj,
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 return None
# REMOVED_UNUSED_CODE:         return self.fee_detection_from_trades(
# REMOVED_UNUSED_CODE:             trade, order, order_obj, order_amount, order.get("trades", [])
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _trades_valid_for_fee(self, trades: list[dict[str, Any]]) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check if trades are valid for fee detection.
# REMOVED_UNUSED_CODE:         :return: True if trades are valid for fee detection, False otherwise
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not trades:
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE:         # We expect amount and cost to be present in all trade objects.
# REMOVED_UNUSED_CODE:         if any(trade.get("amount") is None or trade.get("cost") is None for trade in trades):
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE:         return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fee_detection_from_trades(
# REMOVED_UNUSED_CODE:         self, trade: Trade, order: CcxtOrder, order_obj: Order, order_amount: float, trades: list
# REMOVED_UNUSED_CODE:     ) -> float | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         fee-detection fallback to Trades.
# REMOVED_UNUSED_CODE:         Either uses provided trades list or the result of fetch_my_trades to get correct fee.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not self._trades_valid_for_fee(trades):
# REMOVED_UNUSED_CODE:             trades = self.exchange.get_trades_for_order(
# REMOVED_UNUSED_CODE:                 self.exchange.get_order_id_conditional(order), trade.pair, order_obj.order_date
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if len(trades) == 0:
# REMOVED_UNUSED_CODE:             logger.info("Applying fee on amount for %s failed: myTrade-dict empty found", trade)
# REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE:         fee_currency = None
# REMOVED_UNUSED_CODE:         amount = 0
# REMOVED_UNUSED_CODE:         fee_abs = 0.0
# REMOVED_UNUSED_CODE:         fee_cost = 0.0
# REMOVED_UNUSED_CODE:         trade_base_currency = self.exchange.get_pair_base_currency(trade.pair)
# REMOVED_UNUSED_CODE:         fee_rate_array: list[float] = []
# REMOVED_UNUSED_CODE:         for exectrade in trades:
# REMOVED_UNUSED_CODE:             amount += exectrade["amount"]
# REMOVED_UNUSED_CODE:             if self.exchange.order_has_fee(exectrade):
# REMOVED_UNUSED_CODE:                 # Prefer singular fee
# REMOVED_UNUSED_CODE:                 fees = [exectrade["fee"]]
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 fees = exectrade.get("fees", [])
# REMOVED_UNUSED_CODE:             for fee in fees:
# REMOVED_UNUSED_CODE:                 fee_cost_, fee_currency, fee_rate_ = self.exchange.extract_cost_curr_rate(
# REMOVED_UNUSED_CODE:                     fee, exectrade["symbol"], exectrade["cost"], exectrade["amount"]
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 fee_cost += fee_cost_
# REMOVED_UNUSED_CODE:                 if fee_rate_ is not None:
# REMOVED_UNUSED_CODE:                     fee_rate_array.append(fee_rate_)
# REMOVED_UNUSED_CODE:                 # only applies if fee is in quote currency!
# REMOVED_UNUSED_CODE:                 if trade_base_currency == fee_currency:
# REMOVED_UNUSED_CODE:                     fee_abs += fee_cost_
# REMOVED_UNUSED_CODE:         # Ensure at least one trade was found:
# REMOVED_UNUSED_CODE:         if fee_currency:
# REMOVED_UNUSED_CODE:             # fee_rate should use mean
# REMOVED_UNUSED_CODE:             fee_rate = sum(fee_rate_array) / float(len(fee_rate_array)) if fee_rate_array else None
# REMOVED_UNUSED_CODE:             if fee_rate is not None and fee_rate < 0.02:
# REMOVED_UNUSED_CODE:                 # Only update if fee-rate is < 2%
# REMOVED_UNUSED_CODE:                 trade.update_fee(fee_cost, fee_currency, fee_rate, order.get("side", ""))
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 logger.warning(
# REMOVED_UNUSED_CODE:                     f"Not updating {order.get('side', '')}-fee - rate: {fee_rate}, {fee_currency}."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not isclose(amount, order_amount, abs_tol=constants.MATH_CLOSE_PREC):
# REMOVED_UNUSED_CODE:             # * Leverage could be a cause for this warning
# REMOVED_UNUSED_CODE:             logger.warning(f"Amount {amount} does not match amount {trade.amount}")
# REMOVED_UNUSED_CODE:             raise DependencyException("Half bought? Amounts don't match")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if fee_abs != 0:
# REMOVED_UNUSED_CODE:             return self.apply_fee_conditional(
# REMOVED_UNUSED_CODE:                 trade, trade_base_currency, amount=amount, fee_abs=fee_abs, order_obj=order_obj
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_valid_price(self, custom_price: float, proposed_price: float) -> float:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Return the valid price.
# REMOVED_UNUSED_CODE:         Check if the custom price is of the good type if not return proposed_price
# REMOVED_UNUSED_CODE:         :return: valid price for the order
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if custom_price:
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 valid_custom_price = float(custom_price)
# REMOVED_UNUSED_CODE:             except ValueError:
# REMOVED_UNUSED_CODE:                 valid_custom_price = proposed_price
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             valid_custom_price = proposed_price
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         cust_p_max_dist_r = self.config.get("custom_price_max_distance_ratio", 0.02)
# REMOVED_UNUSED_CODE:         min_custom_price_allowed = proposed_price - (proposed_price * cust_p_max_dist_r)
# REMOVED_UNUSED_CODE:         max_custom_price_allowed = proposed_price + (proposed_price * cust_p_max_dist_r)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Bracket between min_custom_price_allowed and max_custom_price_allowed
# REMOVED_UNUSED_CODE:         return max(min(valid_custom_price, max_custom_price_allowed), min_custom_price_allowed)
