"""
This module manages webhook communication
"""

import logging
import time
from typing import Any

from requests import RequestException, post

from freqtrade.constants import Config
from freqtrade.enums import RPCMessageType
from freqtrade.rpc import RPC, RPCHandler
from freqtrade.rpc.rpc_types import RPCSendMsg


logger = logging.getLogger(__name__)

logger.debug("Included module rpc.webhook ...")


# REMOVED_UNUSED_CODE: class Webhook(RPCHandler):
# REMOVED_UNUSED_CODE:     """This class handles all webhook communication"""
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, rpc: RPC, config: Config) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Init the Webhook class, and init the super class RPCHandler
# REMOVED_UNUSED_CODE:         :param rpc: instance of RPC Helper class
# REMOVED_UNUSED_CODE:         :param config: Configuration object
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         super().__init__(rpc, config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._url = self._config["webhook"]["url"]
# REMOVED_UNUSED_CODE:         self._format = self._config["webhook"].get("format", "form")
# REMOVED_UNUSED_CODE:         self._retries = self._config["webhook"].get("retries", 0)
# REMOVED_UNUSED_CODE:         self._retry_delay = self._config["webhook"].get("retry_delay", 0.1)
# REMOVED_UNUSED_CODE:         self._timeout = self._config["webhook"].get("timeout", 10)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def cleanup(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Cleanup pending module resources.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This will do nothing for webhooks, they will simply not be called anymore
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pass
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _get_value_dict(self, msg: RPCSendMsg) -> dict[str, Any] | None:
# REMOVED_UNUSED_CODE:         whconfig = self._config["webhook"]
# REMOVED_UNUSED_CODE:         if msg["type"].value in whconfig:
# REMOVED_UNUSED_CODE:             # Explicit types should have priority
# REMOVED_UNUSED_CODE:             valuedict = whconfig.get(msg["type"].value)
# REMOVED_UNUSED_CODE:         # Deprecated 2022.10 - only keep generic method.
# REMOVED_UNUSED_CODE:         elif msg["type"] in [RPCMessageType.ENTRY]:
# REMOVED_UNUSED_CODE:             valuedict = whconfig.get("webhookentry")
# REMOVED_UNUSED_CODE:         elif msg["type"] in [RPCMessageType.ENTRY_CANCEL]:
# REMOVED_UNUSED_CODE:             valuedict = whconfig.get("webhookentrycancel")
# REMOVED_UNUSED_CODE:         elif msg["type"] in [RPCMessageType.ENTRY_FILL]:
# REMOVED_UNUSED_CODE:             valuedict = whconfig.get("webhookentryfill")
# REMOVED_UNUSED_CODE:         elif msg["type"] == RPCMessageType.EXIT:
# REMOVED_UNUSED_CODE:             valuedict = whconfig.get("webhookexit")
# REMOVED_UNUSED_CODE:         elif msg["type"] == RPCMessageType.EXIT_FILL:
# REMOVED_UNUSED_CODE:             valuedict = whconfig.get("webhookexitfill")
# REMOVED_UNUSED_CODE:         elif msg["type"] == RPCMessageType.EXIT_CANCEL:
# REMOVED_UNUSED_CODE:             valuedict = whconfig.get("webhookexitcancel")
# REMOVED_UNUSED_CODE:         elif msg["type"] in (
# REMOVED_UNUSED_CODE:             RPCMessageType.STATUS,
# REMOVED_UNUSED_CODE:             RPCMessageType.STARTUP,
# REMOVED_UNUSED_CODE:             RPCMessageType.EXCEPTION,
# REMOVED_UNUSED_CODE:             RPCMessageType.WARNING,
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             valuedict = whconfig.get("webhookstatus")
# REMOVED_UNUSED_CODE:         elif msg["type"] in (
# REMOVED_UNUSED_CODE:             RPCMessageType.PROTECTION_TRIGGER,
# REMOVED_UNUSED_CODE:             RPCMessageType.PROTECTION_TRIGGER_GLOBAL,
# REMOVED_UNUSED_CODE:             RPCMessageType.WHITELIST,
# REMOVED_UNUSED_CODE:             RPCMessageType.ANALYZED_DF,
# REMOVED_UNUSED_CODE:             RPCMessageType.NEW_CANDLE,
# REMOVED_UNUSED_CODE:             RPCMessageType.STRATEGY_MSG,
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             # Don't fail for non-implemented types
# REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE:         return valuedict
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def send_msg(self, msg: RPCSendMsg) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Send a message to telegram channel"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             valuedict = self._get_value_dict(msg)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not valuedict:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.debug("Message type '%s' not configured for webhooks", msg["type"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             payload = {key: value.format(**msg) for (key, value) in valuedict.items()}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._send_msg(payload)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         except KeyError as exc:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.exception(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "Problem calling Webhook. Please check your webhook configuration. Exception: %s",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 exc,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _send_msg(self, payload: dict) -> None:
# REMOVED_UNUSED_CODE:         """do the actual call to the webhook"""
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         success = False
# REMOVED_UNUSED_CODE:         attempts = 0
# REMOVED_UNUSED_CODE:         while not success and attempts <= self._retries:
# REMOVED_UNUSED_CODE:             if attempts:
# REMOVED_UNUSED_CODE:                 if self._retry_delay:
# REMOVED_UNUSED_CODE:                     time.sleep(self._retry_delay)
# REMOVED_UNUSED_CODE:                 logger.info("Retrying webhook...")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             attempts += 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 if self._format == "form":
# REMOVED_UNUSED_CODE:                     response = post(self._url, data=payload, timeout=self._timeout)
# REMOVED_UNUSED_CODE:                 elif self._format == "json":
# REMOVED_UNUSED_CODE:                     response = post(self._url, json=payload, timeout=self._timeout)
# REMOVED_UNUSED_CODE:                 elif self._format == "raw":
# REMOVED_UNUSED_CODE:                     response = post(
# REMOVED_UNUSED_CODE:                         self._url,
# REMOVED_UNUSED_CODE:                         data=payload["data"],
# REMOVED_UNUSED_CODE:                         headers={"Content-Type": "text/plain"},
# REMOVED_UNUSED_CODE:                         timeout=self._timeout,
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     raise NotImplementedError(f"Unknown format: {self._format}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 # Throw a RequestException if the post was not successful
# REMOVED_UNUSED_CODE:                 response.raise_for_status()
# REMOVED_UNUSED_CODE:                 success = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             except RequestException as exc:
# REMOVED_UNUSED_CODE:                 logger.warning("Could not call webhook url. Exception: %s", exc)
