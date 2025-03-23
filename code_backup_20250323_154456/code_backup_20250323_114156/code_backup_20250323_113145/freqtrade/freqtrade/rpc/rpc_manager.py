"""
This module contains class to manage RPC communications (Telegram, API, ...)
"""

import logging
from collections import deque

from freqtrade.constants import Config
from freqtrade.enums import NO_ECHO_MESSAGES, RPCMessageType
from freqtrade.rpc import RPC, RPCHandler
from freqtrade.rpc.rpc_types import RPCSendMsg


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class RPCManager:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Class to manage RPC objects (Telegram, API, ...)
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, freqtrade) -> None:
# REMOVED_UNUSED_CODE:         """Initializes all enabled rpc modules"""
# REMOVED_UNUSED_CODE:         self.registered_modules: list[RPCHandler] = []
# REMOVED_UNUSED_CODE:         self._rpc = RPC(freqtrade)
# REMOVED_UNUSED_CODE:         config = freqtrade.config
# REMOVED_UNUSED_CODE:         # Enable telegram
# REMOVED_UNUSED_CODE:         if config.get("telegram", {}).get("enabled", False):
# REMOVED_UNUSED_CODE:             logger.info("Enabling rpc.telegram ...")
# REMOVED_UNUSED_CODE:             from freqtrade.rpc.telegram import Telegram
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.registered_modules.append(Telegram(self._rpc, config))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Enable discord
# REMOVED_UNUSED_CODE:         if config.get("discord", {}).get("enabled", False):
# REMOVED_UNUSED_CODE:             logger.info("Enabling rpc.discord ...")
# REMOVED_UNUSED_CODE:             from freqtrade.rpc.discord import Discord
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.registered_modules.append(Discord(self._rpc, config))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Enable Webhook
# REMOVED_UNUSED_CODE:         if config.get("webhook", {}).get("enabled", False):
# REMOVED_UNUSED_CODE:             logger.info("Enabling rpc.webhook ...")
# REMOVED_UNUSED_CODE:             from freqtrade.rpc.webhook import Webhook
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.registered_modules.append(Webhook(self._rpc, config))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Enable local rest api server for cmd line control
# REMOVED_UNUSED_CODE:         if config.get("api_server", {}).get("enabled", False):
# REMOVED_UNUSED_CODE:             logger.info("Enabling rpc.api_server")
# REMOVED_UNUSED_CODE:             from freqtrade.rpc.api_server import ApiServer
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             apiserver = ApiServer(config)
# REMOVED_UNUSED_CODE:             apiserver.add_rpc_handler(self._rpc)
# REMOVED_UNUSED_CODE:             self.registered_modules.append(apiserver)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def cleanup(self) -> None:
# REMOVED_UNUSED_CODE:         """Stops all enabled rpc modules"""
# REMOVED_UNUSED_CODE:         logger.info("Cleaning up rpc modules ...")
# REMOVED_UNUSED_CODE:         while self.registered_modules:
# REMOVED_UNUSED_CODE:             mod = self.registered_modules.pop()
# REMOVED_UNUSED_CODE:             logger.info("Cleaning up rpc.%s ...", mod.name)
# REMOVED_UNUSED_CODE:             mod.cleanup()
# REMOVED_UNUSED_CODE:             del mod
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def send_msg(self, msg: RPCSendMsg) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Send given message to all registered rpc modules.
# REMOVED_UNUSED_CODE:         A message consists of one or more key value pairs of strings.
# REMOVED_UNUSED_CODE:         e.g.:
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             'status': 'stopping bot'
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if msg.get("type") not in NO_ECHO_MESSAGES:
# REMOVED_UNUSED_CODE:             logger.info("Sending rpc message: %s", msg)
# REMOVED_UNUSED_CODE:         for mod in self.registered_modules:
# REMOVED_UNUSED_CODE:             logger.debug("Forwarding message to rpc.%s", mod.name)
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 mod.send_msg(msg)
# REMOVED_UNUSED_CODE:             except NotImplementedError:
# REMOVED_UNUSED_CODE:                 logger.error(f"Message type '{msg['type']}' not implemented by handler {mod.name}.")
# REMOVED_UNUSED_CODE:             except Exception:
# REMOVED_UNUSED_CODE:                 logger.exception("Exception occurred within RPC module %s", mod.name)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def process_msg_queue(self, queue: deque) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Process all messages in the queue.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         while queue:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             msg = queue.popleft()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.info("Sending rpc strategy_msg: %s", msg)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for mod in self.registered_modules:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if mod._config.get(mod.name, {}).get("allow_custom_messages", False):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     mod.send_msg(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             "type": RPCMessageType.STRATEGY_MSG,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             "msg": msg,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def startup_messages(self, config: Config, pairlist, protections) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if config["dry_run"]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.send_msg(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "type": RPCMessageType.WARNING,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "status": "Dry run is enabled. All trades are simulated.",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stake_currency = config["stake_currency"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stake_amount = config["stake_amount"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         minimal_roi = config["minimal_roi"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stoploss = config["stoploss"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trailing_stop = config["trailing_stop"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         timeframe = config["timeframe"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         exchange_name = config["exchange"]["name"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         strategy_name = config.get("strategy", "")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pos_adjust_enabled = "On" if config["position_adjustment_enable"] else "Off"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.send_msg(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "type": RPCMessageType.STARTUP,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "status": f"*Exchange:* `{exchange_name}`\n"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"*Stake per trade:* `{stake_amount} {stake_currency}`\n"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"*Minimum ROI:* `{minimal_roi}`\n"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"*{'Trailing ' if trailing_stop else ''}Stoploss:* `{stoploss}`\n"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"*Position adjustment:* `{pos_adjust_enabled}`\n"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"*Timeframe:* `{timeframe}`\n"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"*Strategy:* `{strategy_name}`",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.send_msg(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "type": RPCMessageType.STARTUP,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "status": f"Searching for {stake_currency} pairs to buy and sell "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"based on {pairlist.short_desc()}",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if len(protections.name_list) > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             prots = "\n".join([p for prot in protections.short_desc() for k, p in prot.items()])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.send_msg(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 {"type": RPCMessageType.STARTUP, "status": f"Using Protections: \n{prots}"}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
